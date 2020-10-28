import requests
import json

from .response import *


class Guild:
    """
    Object managing /resources/guild/* endpoints
    """

    def __init__(self, root) -> None:
        self.__root = root

    @property
    def root(self):
        """
        Get root API object
        :return: API object
        """
        return self.__root

    @property
    def achievements(self) -> GuildAchievementsResourceResponse:
        """
        Perform GET request on /resources/guild/achievements endpoint
        :return: GuildAchievementsResponse object
        """
        return GuildAchievementsResourceResponse(
            self.root.get('/resources/guilds/achievements', public=True)
        )

    @property
    def permissions(self) -> PermissionsResourceResponse:
        """
        Perform GET request on /resources/guild/permissions endpoint
        :return: GuildPermissionResponse object
        """
        return PermissionsResourceResponse(
            self.root.get('/resources/guilds/permissions', public=True)
        )


class Skyblock:
    """
    Object managing /resources/skyblock/* endpoints
    """

    def __init__(self, root) -> None:
        self.__root = root

    @property
    def root(self):
        """
        Get root API object
        :return: API object
        """
        return self.__root

    @property
    def collections(self) -> SkyblockCollectionsResponse:
        """
        Perform GET request on /resources/skyblock/collections endpoint
        :return: SyblockCollectionsResponse object
        """
        return SkyblockCollectionsResponse(
            self.root.get('/resources/skyblock/collections', public=True)
        )

    @property
    def skills(self) -> SkyblockSkillsResponse:
        """
        Perform GET requests on /resources/skyblock/skills endpoint
        :return: SkyblockSkillsResponse object
        """
        return SkyblockSkillsResponse(
            self.root.get('/resources/skyblock/skills', public=True)
        )


class Resources:
    """
    Object managing /resources/* endpoints
    """

    def __init__(self, root) -> None:
        self._root = root

    @property
    def root(self):
        """
        Get Root API object
        :return: API object
        """
        return self._root

    @property
    def achievements(self) -> AchievementsResourceResponse:
        """
        Perform GET request on /resources/achievements endpoint
        :return: AchievementsResourceResponse object
        """
        return AchievementsResourceResponse(
            self.root.get("/resources/achievements", public=True)
        )

    @property
    def challenges(self) -> ChallengesResourceResponse:
        """
        Perform GET request on /resources/challenges endpoint
        :return: ChallengesResourceResponse object
        """
        return ChallengesResourceResponse(
            self.root.get("/resources/challenges", public=True)
        )

    @property
    def quests(self) -> QuestsResourceResponse:
        """
        Perform GET request on /resources/quests endpoint
        :return: QuestsResourceResponse object
        """
        return QuestsResourceResponse(
            self.root.get("/resources/quests", public=True)
        )

    @property
    def guilds(self) -> Guild:
        """
        Get an object responsible for /resources/guilds/* endpoints
        :return: Guild object
        """
        return Guild(self._root)

    @property
    def skyblock(self) -> Skyblock:
        """
        Get an object responsible for /resources/skyblock/* endpoints
        :return: Skyblock object
        """
        return Skyblock(self._root)


class Api:
    """
    Main Hypyxel object
    Managing all connections with requests library
    """

    class ApiException(BaseException):
        pass

    def __init__(self, key, host="https://api.hypixel.net") -> None:
        self._session = requests.Session()
        self._host = host
        self._key = key

        self._resources = Resources(self)

    def get(self, path: str,
            params: dict = None,
            public=False,
            except_on_failure=True) -> json:
        """
        Perform a GET request on the REST API

        :param path: REST endpoint to GET
        :param params: Parameters needed for the request
        :param public: Precise if the Endpoint require a key or not
        :param except_on_failure: Raise an Exception on failure
        :return: Json object obtain from the request response
        """
        if type(path) is not str:
            raise ValueError("get(): path should be a string")

        if params and type(params) is not dict:
            raise ValueError("get(): params should be a dictionary")

        if not params:
            params = {}

        if not public:
            params["key"] = self._key

        r = self._session.get(f"{self._host}{path}", params=params)
        if except_on_failure and r.status_code != 200:
            try:
                j = json.loads(r.text)
                raise self.ApiException(
                    f"Hypyxel: {j.get('message', 'Unknown Error')}"
                )
            except:
                raise self.ApiException("Hypyxel: Unknown Error")

        return json.loads(r.text)

    def post(self, path: str) -> json:
        """
        Execute a POST request
        :param path: REST endpoint to POST
        :return: Json object
        """

        raise Exception("Hypyxel: POST are not supported")

    @property
    def resources(self) -> Resources:
        """
        Get the object responsible for resources/* requests
        :return: Resources object
        """
        return self._resources

    def status(self, uuid: str) -> StatusResponse:
        """
        Get player status
        :param uuid: Player UUID
        :return: Status Response
        """
        return StatusResponse(
            self.get('/status', params={'uuid': uuid})
        )

    @property
    def watchdog(self) -> WatchdogResponse:
        """
        Get Watchdog Status
        :return: Watchdog object
        """
        return WatchdogResponse(
            self.get('/watchdogstats')
        )

    @property
    def key(self) -> KeyResponse:
        """
        Get Key Info
        :return: Key object
        """
        return KeyResponse(
            self.get('/key')
        )

    @property
    def player_count(self) -> int:
        """
        Get the number of online player
        :return: Online player
        """
        r = self.get('/playerCount')
        return r.get('playerCount')

    def find_guild(self, name: str = None, uuid: str = None) -> str:
        """
        Get Guild ID
        :param name: Find by name
        :param uuid: Find by player UUID
        :return: Guild ID
        """
        if not bool(name) ^ bool(uuid):
            raise ValueError("One of uuid or name need to be set")

        p = {'byName': name} if name else {'byUuid': uuid}
        r = self.get('/findGuild', params=p)
        return r.get('guild', None)

    @property
    def boosters(self) -> BoostersResponse:
        """
        Get booster list
        :return: BoostersResponse
        """
        return BoostersResponse(
            self.get('/boosters')
        )

    def guild(self, id: str = None,
              player: str = None,
              name: str = None) -> GuildResponse:
        """
        Get Guild information
        Only one of the three parameter can be set
        :param id: Find guild by ID
        :param player: Find guild by player name
        :param name: Find guild by its name
        :return: GuildResponse object
        """
        if not bool(id) ^ bool(player) ^ bool(name):
            ValueError('One of id, player or name need to be set')

        p = {}
        for k, v in (('id', id), ('player', player), ('name', name)):
            if v:
                p = {k: v}
                break

        return GuildResponse(
            self.get('/guild', params=p)
        )

    def friends(self, uuid: str) -> FriendResponse:
        """
        Get player's friends list
        :param uuid: Player UUID
        :return: FriendResponse object
        """
        return FriendResponse(
            self.get('/friends', params={'uuid': uuid})
        )

    @property
    def game_counts(self) -> GameCountsResponse:
        """
        Get the number of player online for each game
        :return: GameCountsResponse
        """
        return GameCountsResponse(
            self.get('/gameCounts')
        )

    def recent_games(self, uuid: str) -> RecentGamesResponse:
        """
        Get player's recent games
        :param uuid: Player UUID
        :return: RecentGamesResponse
        """
        return RecentGamesResponse(
            self.get('/recentGames', params={'uuid': uuid})
        )

    @property
    def leaderboards(self) -> LeaderboardResponse:
        """
        Get Leaderboards information
        :return: LeaderboardResponse object
        """
        return LeaderboardResponse(
            self.get('/leaderboards')
        )
