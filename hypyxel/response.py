from typing import Dict, Tuple
from .response_objects import *
from .utils import timestamp_to_datetime, datetime


class APIResponse:
    def __init__(self, raw: dict):
        self._raw = raw
        self._success = False
        self._error_message = None

        self.__parse_data()

    def __parse_data(self):

        self._success = self._raw.get("success")
        self._error_message = self._raw.get('cause', None)

    @property
    def raw(self) -> dict:
        return self._raw

    @property
    def success(self) -> bool:
        return self._success

    @property
    def error_message(self) -> str:
        return self._error_message


class ResourceResponse(APIResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._last_update = None

        self.__parse_resource_data()

    def __parse_resource_data(self):
        self._last_update = self._raw.get('lastUpdated', None)

    @property
    def last_update(self) -> datetime:
        """
        Get the last update date
        :return: datetime object or None in case of error
        """
        return timestamp_to_datetime(self._last_update)


class GuildAchievementsResourceResponse(ResourceResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._one_time = tuple()
        self._tiered = tuple()

        self.__parse_guild_achievements_data()

    def __parse_guild_achievements_data(self):

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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._one_time = dict()
        self._tiered = dict()

        self._points = dict()
        self._legacy_points = dict()

        self.__parse_achievements_data()

    def __parse_achievements_data(self):

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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._challenges = tuple()

        self.__parse_challenges_data()

    def __parse_challenges_data(self):
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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._quests = tuple()

        self.__parse_quests_data()

    def __parse_quests_data(self):
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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._permissions = tuple()

        self.__parse_permissions_data()

    def __parse_permissions_data(self):
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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__version = None

        self.__parse_skyblock_data()

    def __parse_skyblock_data(self):
        self.__version = self._raw.get('version', None)

    @property
    def version(self) -> str:
        """
        Get Skyblock version
        :return: skyblock version
        """
        return self.__version


class SkyblockCollectionsResponse(SkyblockResourceResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__collections = dict()

        self.__parse_collections_data()

    def __parse_collections_data(self):

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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__skills = dict()

        self.__parse_skills_data()

    def __parse_skills_data(self):
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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__online = None
        self.__game_type = None
        self.__mode = None
        self.__map = None

        self.__parse_status_data()

    def __parse_status_data(self):
        d = self._raw.get('session', {})

        self.__online = d.get('online', False)
        self.__game_type = d.get('gameType', None)
        self.__mode = d.get('mode', None)
        self.__map = d.get('map', None)

    @property
    def online(self) -> bool:
        return self.__online

    @property
    def game(self) -> str:
        return self.__game_type

    @property
    def mode(self) -> str:
        return self.__mode

    @property
    def map(self) -> str:
        return self.__map


class KeyResponse(APIResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__key = None
        self.__owner = None
        self.__limit = -1
        self.__queries = -1
        self.__total_queries = -1

        self.__parse_key_data()

    def __parse_key_data(self):
        d = self._raw.get('record', {})

        self.__key = d.get('key', None)
        self.__owner = d.get('owner', None)
        self.__limit = d.get('limit', -1)
        self.__queries = d.get('queriesInPastMin', -1)
        self.__total_queries = d.get('totalQueries', -1)

    @property
    def key(self) -> str:
        return self.__key

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def limit(self) -> int:
        return self.__limit

    @property
    def queries(self) -> int:
        return self.__queries

    @property
    def total_queries(self) -> int:
        return self.__total_queries


class WatchdogResponse(APIResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__last_minute = -1
        self.__staff_rolling = -1
        self.__total = -1
        self.__rolling = -1
        self.__staff_total = -1

        self.__parse_watchdog_data()

    def __parse_watchdog_data(self):

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

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__games = tuple()

        self.__parse_recent_game_data()

    def __parse_recent_game_data(self):

        self.__games = tuple(
            RecentGame(i) for i in self.raw.get('games', ())
        )

    @property
    def games(self) -> Tuple[RecentGame]:
        return self.__games


class BoostersResponse(APIResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.__boosters = tuple()
        self.__decrementing = None

        self.__parse_boosters_data()

    def __parse_boosters_data(self):
        self.__boosters = tuple(Booster(i) for i in self.raw.get('boosters'))
        self.__decrementing = self.raw.get('boosterState').get('decrementing')

    @property
    def boosters(self) -> Tuple[Booster]:
        return self.__boosters

    @property
    def decrementing(self) -> bool:
        return self.__decrementing


class GuildResponse(APIResponse):

    def __init__(self, raw: dict):
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

    def __parse_guild_data(self):
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
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def coins(self) -> int:
        return self.__coins

    @property
    def max_coins(self) -> int:
        return self.__max_coins

    @property
    def created(self) -> datetime:
        return timestamp_to_datetime(self.__created)

    @property
    def members(self) ->  Tuple[GuildMember]:
        return self.__members

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def achievements(self) -> Dict[str, int]:
        return self.__achievements

    @property
    def exp(self) -> int:
        return self.__exp

    @property
    def legacy_rank(self) -> int:
        return self.__legacy_ranking

    @property
    def ranks(self) -> Tuple[GuildRank]:
        return self.__ranks

    @property
    def chat_mute(self) -> int:
        return self.__chat_mute

    @property
    def preferred_games(self) -> Tuple[str]:
        return self.__pref_games

    @property
    def publicly_listed(self) -> bool:
        return self.__public_listed

    @property
    def tag_color(self) -> str:
        return self.__tag_color

    @property
    def exp_by_game(self) -> Dict[str, int]:
        return self.__exp_by_game
