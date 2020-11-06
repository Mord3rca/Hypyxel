from typing import Dict, Tuple
from .response_objects import *
from .utils import timestamp_to_datetime, datetime

from datetime import timedelta


class APIResponse:
    """
    BaseObject for API response
    Managing potential API error messages
    """
    def __init__(self, raw: dict) -> None:
        self._raw = raw
        self._success = False
        self._error_message = None

        self.__parse_data()

    def __parse_data(self) -> None:

        self._success = self._raw.get("success")
        self._error_message = self._raw.get('cause', None)

    @property
    def raw(self) -> dict:
        """
        Get the response json object
        :return: json object
        """
        return self._raw

    @property
    def success(self) -> bool:
        """
        Get success
        :return: bool
        """
        return self._success

    @property
    def error_message(self) -> str:
        """
        Get error message in case of failure
        :return: Error message
        """
        return self._error_message


class ResourceResponse(APIResponse):
    """
    Object managing update property for resources endpoints
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self._last_update = None

        self.__parse_resource_data()

    def __parse_resource_data(self) -> None:
        self._last_update = self._raw.get('lastUpdated', None)

    @property
    def last_update(self) -> datetime:
        """
        Get the last update date
        :return: datetime object or None in case of error
        """
        return timestamp_to_datetime(self._last_update)


class GuildAchievementsResourceResponse(ResourceResponse):
    """
    Object parsing data for /resources/guild/achievements endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self._one_time = tuple()
        self._tiered = tuple()

        self.__parse_guild_achievements_data()

    def __parse_guild_achievements_data(self) -> None:

        self._one_time = tuple(
            HypixelOneTimeAchievement(None, *i)
            for i in self._raw.get('one_time').items()
        )

        self._tiered = tuple(
            HypixelTieredAchievement(None, *i)
            for i in self._raw.get('tiered').items()
        )

    @property
    def one_time(self) -> Tuple[HypixelOneTimeAchievement]:
        """
        Get One Time Achievement list
        :return: List of HypixelOneTimeAchievement
        """
        return self._one_time

    @property
    def tiered(self) -> Tuple[HypixelTieredAchievement]:
        """
        Get Tiered Achievement list
        :return: List of HypixelTieredAchievement
        """
        return self._tiered


class AchievementsResourceResponse(ResourceResponse):
    """
    Object parsing data for /resources/achievements endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self._one_time = dict()
        self._tiered = dict()

        self._points = dict()
        self._legacy_points = dict()

        self.__parse_achievements_data()

    def __parse_achievements_data(self) -> None:

        self._one_time = {
            j: [HypixelOneTimeAchievement(j, *i)
                for i in self._raw["achievements"][j]["one_time"].items()]
            for j in self._raw["achievements"].keys()
        }

        self._tiered = {
            j: [HypixelTieredAchievement(j, *i)
                for i in self._raw["achievements"][j]["tiered"].items()]
            for j in self._raw["achievements"].keys()
        }

        self._points = {
            j: self._raw["achievements"][j].get("total_points", -1)
            for j in self._raw["achievements"].keys()
        }

        self._legacy_points = {
            j: self._raw["achievements"][j].get("total_legacy_points", -1)
            for j in self._raw["achievements"].keys()
        }

    @property
    def one_time(self) -> Dict[str, HypixelOneTimeAchievement]:
        """
        Get One Time Achievement list
        :return: Dict of HypixelOneTimeAchievements as value
                 and GameType as key
        """
        return self._one_time

    @property
    def tiered(self) -> Dict[str, HypixelTieredAchievement]:
        """
        Get Tiered Achievement list
        :return: Dict of HypixelTieredAchievement as value
                 and GameType as key
        """
        return self._tiered

    @property
    def total_points(self) -> Dict[str, int]:
        """
        Get a dictionary containing game name as key & total points as value
        :return: Dictionary of gamename : points
        """
        return self._points

    @property
    def total_legacy_points(self) -> Dict[str, int]:
        """
        Get a dictionary containing game name as key &
        total legacy points as value
        :return: Dictionary of gamename : legacy points
        """
        return self._legacy_points


class ChallengesResourceResponse(ResourceResponse):
    """
    Object parsing data for /resources/challenges endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self._challenges = tuple()

        self.__parse_challenges_data()

    def __parse_challenges_data(self) -> None:
        self._challenges = tuple(HypixelChallenge(j, i)
                                 for j in self._raw.get('challenges').keys()
                                 for i in self._raw.get('challenges')[j]
                                 )

    @property
    def challenges(self) -> Tuple[HypixelChallenge]:
        """
        Get challenges list
        :return: Challenge list
        """
        return self._challenges


class QuestsResourceResponse(ResourceResponse):
    """
    Object parsing data for /resources/quests endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self._quests = tuple()

        self.__parse_quests_data()

    def __parse_quests_data(self) -> None:
        self._quests = tuple(HypixelQuest(j, i)
                             for j in self._raw.get('quests').keys()
                             for i in self._raw.get('quests')[j]
                             )

    @property
    def quests(self) -> Tuple[HypixelQuest]:
        """
        Get quests list
        :return: Quest list
        """
        return self._quests


class PermissionsResourceResponse(ResourceResponse):
    """
    Object parsing data for /resources/permissions endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self._permissions = tuple()

        self.__parse_permissions_data()

    def __parse_permissions_data(self) -> None:
        self._permissions = tuple(HypixelPermission(i)
                                  for i in self._raw.get('permissions'))

    @property
    def permissions(self) -> Tuple[HypixelPermission]:
        """
        Get permission list
        :return: Permission list
        """
        return self._permissions


class SkyblockResourceResponse(ResourceResponse):
    """
    Object parsing data in common for /resources/skyblock/* endpoints
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__version = None

        self.__parse_skyblock_data()

    def __parse_skyblock_data(self) -> None:
        self.__version = self._raw.get('version', None)

    @property
    def version(self) -> str:
        """
        Get Skyblock version
        :return: skyblock version
        """
        return self.__version


class SkyblockCollectionsResponse(SkyblockResourceResponse):
    """
    Object parsing data for /resources/skyblock/collections endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__collections = dict()

        self.__parse_collections_data()

    def __parse_collections_data(self) -> None:

        self.__collections = {
            i: HypixelSkyblockCollection(i, self._raw.get('collections')[i])
            for i in self._raw.get('collections', {}).keys()
        }

    @property
    def collections(self) -> Dict[str, HypixelSkyblockCollection]:
        """
        Get Skyblock collections
        :return: Skyblock Collection as a dict (collection ID as key)
        """
        return self.__collections


class SkyblockSkillsResponse(SkyblockResourceResponse):
    """
    Object parsing data for /resources/skyblock/skills endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__skills = dict()

        self.__parse_skills_data()

    def __parse_skills_data(self) -> None:
        self.__skills = {
            i: HypixelSkyblockSkill(i, self._raw.get('collections')[i])
            for i in self._raw.get('collections', {}).keys()
        }

    @property
    def skills(self) -> Dict[str, HypixelSkyblockSkill]:
        """
        Get skills collections
        :return: Skyblock skill collections as a dict (skill ID as key)
        """
        return self.__skills


class StatusResponse(APIResponse):
    """
    Object parsing data for /status endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__online = None
        self.__game_type = None
        self.__mode = None
        self.__map = None

        self.__parse_status_data()

    def __parse_status_data(self) -> None:
        d = self._raw.get('session', {})

        self.__online = d.get('online', False)
        self.__game_type = d.get('gameType', None)
        self.__mode = d.get('mode', None)
        self.__map = d.get('map', None)

    @property
    def online(self) -> bool:
        """
        Get in player is online
        :return: bool
        """
        return self.__online

    @property
    def game(self) -> str:
        """
        Get in which game the player is on
        :return: gameType
        """
        return self.__game_type

    @property
    def mode(self) -> str:
        """
        Get in which mode (if available)
        :return: game mode
        """
        return self.__mode

    @property
    def map(self) -> str:
        """
        Get on which map (if available)
        :return: game map
        """
        return self.__map


class KeyResponse(APIResponse):
    """
    Object parsing /key endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__key = None
        self.__owner = None
        self.__limit = -1
        self.__queries = -1
        self.__total_queries = -1

        self.__parse_key_data()

    def __parse_key_data(self) -> None:
        d = self._raw.get('record', {})

        self.__key = d.get('key', None)
        self.__owner = d.get('owner', None)
        self.__limit = d.get('limit', -1)
        self.__queries = d.get('queriesInPastMin', -1)
        self.__total_queries = d.get('totalQueries', -1)

    @property
    def key(self) -> str:
        """
        Get the key ID
        :return: key ID
        """
        return self.__key

    @property
    def owner(self) -> str:
        """
        Get the owner UUID
        :return: Player UUID
        """
        return self.__owner

    @property
    def limit(self) -> int:
        """
        Get the query limit for this key
        :return: query limit
        """
        return self.__limit

    @property
    def queries(self) -> int:
        """
        Get the number of query for the last minute
        :return: number of query
        """
        return self.__queries

    @property
    def total_queries(self) -> int:
        """
        Get the number of query made with this key
        :return: number of query
        """
        return self.__total_queries


class WatchdogResponse(APIResponse):
    """
    Object parsing /watchdogstats endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__last_minute = -1
        self.__staff_rolling = -1
        self.__total = -1
        self.__rolling = -1
        self.__staff_total = -1

        self.__parse_watchdog_data()

    def __parse_watchdog_data(self) -> None:

        self.__last_minute = self.raw.get('watchdog_lastMinute', -1)
        self.__staff_rolling = self.raw.get('staff_rollingDaily', -1)
        self.__total = self.raw.get('watchdog_total', -1)
        self.__rolling = self.raw.get('watchdog_rollingDaily', -1)
        self.__staff_total = self.raw.get('staff_total', -1)

    @property
    def last_minute(self) -> int:
        return self.__last_minute

    @property
    def staff_rolling(self) -> int:
        return self.__staff_rolling

    @property
    def total(self) -> int:
        return self.__total

    @property
    def rolling(self) -> int:
        return self.__rolling

    @property
    def staff_total(self) -> int:
        return self.__staff_total


class RecentGamesResponse(APIResponse):
    """
    Object parsing /recentGames endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__games = tuple()

        self.__parse_recent_game_data()

    def __parse_recent_game_data(self) -> None:

        self.__games = tuple(
            RecentGame(i) for i in self.raw.get('games', ())
        )

    @property
    def games(self) -> Tuple[RecentGame]:
        """
        Get the recent games list
        :return: RecentGame list
        """
        return self.__games


class BoostersResponse(APIResponse):
    """
    Object parsing /boosters endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__boosters = tuple()
        self.__decrementing = None

        self.__parse_boosters_data()

    def __parse_boosters_data(self) -> None:
        self.__boosters = tuple(Booster(i) for i in self.raw.get('boosters'))
        self.__decrementing = self.raw.get('boosterState').get('decrementing')

    @property
    def boosters(self) -> Tuple[Booster]:
        """
        Get the current booster list
        :return: Booster List
        """
        return self.__boosters

    @property
    def decrementing(self) -> bool:
        """
        Get decrementing booster status
        :return: Bool
        """
        return self.__decrementing


class GuildResponse(APIResponse):
    """
    Object parsing /guild endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__id = None
        self.__name = None
        self.__coins = -1
        self.__max_coins = -1
        self.__created = -1
        self.__members = tuple()
        self.__tag = None
        self.__achievements = dict()
        self.__exp = -1
        self.__legacy_ranking = -1
        self.__ranks = tuple()
        self.__chat_mute = -1
        self.__pref_games = tuple()
        self.__public_listed = None
        self.__tag_color = None
        self.__exp_by_game = dict()

        self.__parse_guild_data()

    def __parse_guild_data(self) -> None:
        d = self.raw.get('guild', {})

        self.__id = d.get('_id', None)
        self.__name = d.get('name', None)
        self.__coins = d.get('coins', -1)
        self.__max_coins = d.get('coinsEver', -1)
        self.__created = d.get('created', None)
        self.__members = tuple(
            GuildMember(i) for i in d.get('members', ())
        )
        self.__tag = d.get('tag', None)
        self.__achievements = d.get('achievements', None)
        self.__exp = d.get('exp', -1)
        self.__legacy_ranking = d.get('legacyRanking', -1)
        self.__ranks = tuple(
            GuildRank(i) for i in d.get('ranks', ())
        )
        self.__chat_mute = d.get('chatMute', -1)
        self.__pref_games = d.get('preferredGames', None)
        self.__public_listed = d.get('publiclyListed', None)
        self.__tag_color = d.get('tagColor', None)
        self.__exp_by_game = d.get('guildExpByGameType', None)

    @property
    def id(self) -> str:
        """
        Get guild ID
        :return: Guild ID
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Get guild name
        :return: Guild name
        """
        return self.__name

    @property
    def coins(self) -> int:
        """
        Get current number of coins
        :return: Guild's coins
        """
        return self.__coins

    @property
    def max_coins(self) -> int:
        """
        Get guild maximum number of coins
        :return: Guild's max coins
        """
        return self.__max_coins

    @property
    def created(self) -> datetime:
        """
        Get guild's creation date
        :return:
        """
        return timestamp_to_datetime(self.__created)

    @property
    def members(self) -> Tuple[GuildMember]:
        """
        Get guild's member list
        :return: Member List
        """
        return self.__members

    @property
    def tag(self) -> str:
        """
        Get guild's tag
        :return: guild tag
        """
        return self.__tag

    @property
    def achievements(self) -> Dict[str, int]:
        """
        Get guild's achievements stat
        :return: Guild achievements stat
        """
        return self.__achievements

    @property
    def exp(self) -> int:
        """
        Get guild EXP
        :return: Guild EXP
        """
        return self.__exp

    @property
    def legacy_rank(self) -> int:
        """
        Get guild's legacy rank
        :return: legacy rank
        """
        return self.__legacy_ranking

    @property
    def ranks(self) -> Tuple[GuildRank]:
        """
        Get guild's rank list
        :return: rank list
        """
        return self.__ranks

    @property
    def chat_mute(self) -> int:
        """
        Get guild's chat mute
        :return: chat mute
        """
        return self.__chat_mute

    @property
    def preferred_games(self) -> Tuple[str]:
        """
        Get guild's preferred games list
        :return: preferred games list
        """
        return self.__pref_games

    @property
    def publicly_listed(self) -> bool:
        """
        Get if the guild is publicly listed
        :return: True if public
        """
        return self.__public_listed

    @property
    def tag_color(self) -> str:
        """
        Get guild's tag color
        :return: Tag color as string
        """
        return self.__tag_color

    @property
    def exp_by_game(self) -> Dict[str, int]:
        """
        Get guild's exp dict by gametype
        :return: EXP by gameType
        """
        return self.__exp_by_game


class FriendResponse(APIResponse):
    """
    Object parsing /friend endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__friends = tuple()

        self.__parse_friend_data()

    def __parse_friend_data(self) -> None:
        self.__friends = tuple(
            Friend(i) for i in self.raw.get('records', ())
        )

    @property
    def friends(self) -> Tuple[Friend]:
        """
        Get Friends list
        :return: Friend list
        """
        return self.__friends


class GameCountsResponse(APIResponse):
    """
    Object parsing /gameCounts endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__games = None
        self.__player_count = None

        self.__parse_gamecounts_data()

    def __parse_gamecounts_data(self) -> None:
        self.__games = {
            k: GameStatus(v) for k, v in self.raw.get('games', {}).items()
        }
        self.__player_count = self.raw.get('playerCount', None)

    @property
    def games(self) -> Dict[str, GameStatus]:
        """
        Get game status by gameType
        :return: game status by gameType
        """
        return self.__games

    @property
    def player_count(self) -> int:
        """
        Get total player count
        :return: player count
        """
        return self.__player_count


class LeaderboardResponse(APIResponse):
    """
    Object parsing /leaderboards endpoint
    """

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__boards = None

        self.__parse_board_data()

    def __parse_board_data(self) -> None:

        b = self.raw.get('leaderboards', {})
        self.__boards = {
            k: Leaderboard(v) for k in b.keys() for v in b.get(k)
        }

    @property
    def leaderboards(self) -> Dict[str, Tuple[Leaderboard]]:
        """
        Get the leaderboards for each gametype
        :return: leaderboards for each gameType
        """
        return self.__boards


class PlayerResponse(APIResponse):

    def __init__(self, raw: dict) -> None:
        super().__init__(raw)

        self.__id = None
        self.__display_name = None
        self.__known_aliases = tuple()
        self.__known_aliases_lower = tuple()
        self.__player_name = None
        self.__stats = dict()
        self.__uuid = None
        self.__last_login = None
        self.__last_logout = None
        self.__achievements_one_time = tuple()
        self.__achievements_tracking = tuple()
        self.__achievements_tiered = dict()
        self.__achievement_points = None
        self.__network_exp = None
        self.__pet_consumable = dict()
        self.__hypixel_level = None
        self.__rank = None

        self.__parse_player_data()

    def __parse_player_data(self):
        d = self._raw.get("player", {})

        self.__id = d.get("_id", None)
        self.__display_name = d.get('displayname')
        self.__known_aliases = tuple(d.get("knownAliases", ()))
        self.__known_aliases_lower = tuple(d.get('knownAliasesLower', ()))
        self.__player_name = d.get('playername', None)
        self.__uuid = d.get('uuid', None)
        self.__last_login = d.get('lastLogin', None)
        self.__last_logout = d.get('lastLogout', None)
        self.__achievements_one_time = tuple(d.get('achievementsOneTime', ()))
        self.__achievements_tracking = tuple(d.get('achievementTracking', ()))
        self.__achievements_tiered = d.get('achievements', {})
        self.__achievement_points = d.get('achievementPoints', None)
        self.__network_exp = d.get('networkExp', None)
        self.__pet_consumable = d.get('petConsumables', {})
        self.__rank = d.get('newPackageRank', None)

        # Parse Hypixel Level
        levels = [int(i.split('_')[1]) for i in
                  filter(lambda x: x.startswith('levelingReward_'), d.keys())]
        self.__hypixel_level = max(levels) + 1

        self.__stats = {
            k: game_mode_to_player_stat_obj.get(k, NotImplementedPlayerStat)(v)
            for k, v in d.get('stats', {}).items()
        }

    @property
    def id(self) -> str:
        """
        Get player ID
        :return: Player ID
        """
        return self.__id

    @property
    def display_name(self) -> str:
        """
        Get player's display name
        :return: Player's display name
        """
        return self.__display_name

    @property
    def known_aliases(self) -> Tuple[str]:
        """
        Get player's aliases list
        :return: Aliases List
        """
        return self.__known_aliases

    @property
    def known_aliases_lower(self) -> Tuple[str]:
        """
        Get player's aliases list
        :return: Aliases list (to lower)
        """
        return self.__known_aliases_lower

    @property
    def playername(self) -> str:
        """
        Get player name
        :return: Player name
        """
        return self.__player_name

    @property
    def uuid(self) -> str:
        """
        Get player UUID
        :return: UUID
        """
        return self.__uuid

    @property
    def last_login(self) -> datetime:
        """
        Get last login
        :return: Last login
        """
        return timestamp_to_datetime(self.__last_login)

    @property
    def last_logout(self) -> datetime:
        """
        Get last logout
        :return: Last Logout
        """
        return timestamp_to_datetime(self.__last_logout)

    @property
    def is_online(self) -> bool:
        return self.__last_login > self.__last_logout

    @property
    def last_session_duration(self) -> timedelta:
        if self.is_online:
            raise ValueError("Session still in progress")

        return timedelta(
            milliseconds=self.__last_logout - self.__last_login
        )

    @property
    def achievements_one_time(self) -> Tuple[str]:
        """
        Get player's one time achivements
        :return: One Time Achievements
        """
        return self.__achievements_one_time

    @property
    def achievements_tiered(self) -> Dict[str, int]:
        """
        Get player tiered achievements data
        :return: Player tiered achievements data
        """
        return self.__achievements_tiered

    @property
    def tracked_achievements(self) -> Tuple[str]:
        """
        Get player tracked achievements list
        :return: Tracked Achievements
        """
        return self.__achievements_tracking

    @property
    def achievement_points(self) -> int:
        """
        Get player achievement points
        :return: Achievement Points
        """
        return self.__achievement_points

    @property
    def network_exp(self) -> int:
        """
        Get player network exp
        :return: Network exp
        """
        return self.__network_exp

    @property
    def network_level(self) -> int:
        return self.__hypixel_level

    @property
    def pet_consumable(self) -> Dict[str, int]:
        """
        Get pet consumable available
        :return: Pet Consumable
        """
        return self.__pet_consumable

    @property
    def stats(self) -> Dict[str, object]:
        """
        Get stats by games
        :return: Stats
        """
        return self.__stats

    def is_achievement_unlocked(self, a: HypixelOneTimeAchievement) -> bool:
        if not isinstance(a, HypixelOneTimeAchievement):
            raise ValueError("Achievement need to be a One Time Achievement")

        return f"{a.game.lower()}_{a.name.lower()}"\
               in self.achievements_one_time
