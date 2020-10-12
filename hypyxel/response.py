from typing import Dict, Tuple
from .utils import timestamp_to_datetime, datetime


class APIResponse:
    def __init__(self, raw: dict):
        self._raw = raw

    @property
    def success(self):
        return self._raw["success"]

    @property
    def error_message(self):
        return self._raw.get("cause", None)


class AchievementsResourceResponse(APIResponse):

    class HypixelBaseAchievement:

        def __init__(self, gname, name, data):
            self._name = name
            self._gname = gname
            self._data = data

            self._desc = ""
            self._clean_name = ""
            self._gamePercentUnlocked = -1
            self._globalPercentUnlocked = -1

            self._secret = False
            self._legacy = False

            self._parse_data()

        def __str__(self):
            return f"{type(self).__name__}(\"{self.display_name}\")"

        def _parse_data(self):
            self._desc = self._data["description"]
            self._clean_name = self._data["name"]

            # Those ones are not always there.
            self._gamePercentUnlocked = self._data.get("gamePercentUnlocked", None)
            self._globalPercentUnlocked = self._data.get("globalPercentUnlocked", None)
            self._secret = self._data.get("secret", False)
            self._legacy = self._data.get("legacy", False)

        @property
        def display_name(self) -> str:
            """
            Get achievement display name
            :return: Achievement display name as string
            """
            return self._clean_name

        @property
        def description(self) -> str:
            """
            Get achievement description
            :return: Achievement description as string
            """
            return self._desc

    class HypixelOneTimeAchievement(HypixelBaseAchievement):

        def __init__(self, gname, name, data):
            super().__init__(gname, name, data)

            self._point = self._data.get("points", -1)

        @property
        def point(self) -> int:
            """
            Get Achievement point
            :return: Number of point as int
            """
            return self._point

    class HypixelAchievementTier:

        def __init__(self, data):
            self._tier = data.get("tier")
            self._points = data.get("points")
            self._amount = data.get("amount")

        @property
        def tier(self) -> int:
            """
            Get tier number
            :return: Return tier as int
            """
            return self._tier

        @property
        def points(self) -> int:
            """
            Get Points for this tier
            :return: Return points as int
            """
            return self._points

        @property
        def amount(self) -> int:
            """
            Get required amount for this tier
            :return: Return required amount as int
            """
            return self._amount

    class HypixelTieredAchievement(HypixelBaseAchievement):

        def __init__(self, gname, name, data):
            super().__init__(gname, name, data)

            self._tiers = tuple(AchievementsResourceResponse.HypixelAchievementTier(i)
                                for i in data.get("tiers", [])
                                )

        @property
        def tiers(self) -> Tuple:
            """
            Get tiers for this achievements
            :return: Return table of HypixelAchievementTier
            """
            return self._tiers

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._one_time = dict()
        self._tiered = dict()

        self._points = dict()
        self._legacy_points = dict()

        self._last_update = -1

        self._parse_data()

    def _parse_data(self):

        self._last_update = self._raw.get("lastUpdated", -1)

        self._one_time = {j: [AchievementsResourceResponse.HypixelOneTimeAchievement(j, *i)
                              for i in self._raw["achievements"][j]["one_time"].items()]
                          for j in self._raw["achievements"].keys()}

        self._tiered = {j: [AchievementsResourceResponse.HypixelTieredAchievement(j, *i)
                            for i in self._raw["achievements"][j]["one_time"].items()]
                        for j in self._raw["achievements"].keys()}

        self._points = {
            j: self._raw["achievements"][j].get("total_points", -1) for j in self._raw["achievements"].keys()
        }

        self._legacy_points = {
            j: self._raw["achievements"][j].get("total_legacy_points", -1) for j in self._raw["achievements"].keys()
        }

    @property
    def one_time(self) -> Dict[str, HypixelOneTimeAchievement]:
        """
        Get One Time Achievement list
        :return: Dict of HypixelOneTimeAchievements as value and GameType as key
        """
        return self._one_time

    @property
    def tiered(self) -> Dict[str, HypixelTieredAchievement]:
        """
        Get Tiered Achievement list
        :return: Dict of HypixelTieredAchievement as value and GameType as key
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
        Get a dictionary containing game name as key & total legacy points as value
        :return: Dictionary of gamename : legacy points
        """
        return self._legacy_points

    @property
    def last_update(self) -> datetime:
        """
        Get the last update date
        :return: datetime object or None in case of error
        """
        return timestamp_to_datetime(self._last_update)\
            if self._last_update != -1 else None
