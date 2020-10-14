from typing import Dict, Tuple
from .response_objects import *
from .utils import timestamp_to_datetime, datetime


class APIResponse:
    def __init__(self, raw: dict):
        self._raw = raw
        self._success = False
        self._error_message = None

    def __parse_data(self):

        self._success = self._raw.get("success")
        self._error_message = self._raw.get('cause', None)

    @property
    def success(self) -> bool:
        return self._raw["success"]

    @property
    def error_message(self) -> str:
        return self._raw.get("cause", None)


class ResourceResponse(APIResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._last_update = -1

    def __parse_resource_data(self):
        self._lastUpdated = self._raw.get('lastUpdated', -1)

    @property
    def last_update(self) -> datetime:
        """
        Get the last update date
        :return: datetime object or None in case of error
        """
        return timestamp_to_datetime(self._last_update) \
            if self._last_update != -1 else None


class AchievementsResourceResponse(ResourceResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._one_time = dict()
        self._tiered = dict()

        self._points = dict()
        self._legacy_points = dict()

        self._last_update = -1

        self.__parse_achievements_data()

    def __parse_achievements_data(self):

        self._last_update = self._raw.get("lastUpdated", -1)

        self._one_time = {j: [HypixelOneTimeAchievement(j, *i)
                              for i in self._raw["achievements"][j]["one_time"].items()]
                          for j in self._raw["achievements"].keys()}

        self._tiered = {j: [HypixelTieredAchievement(j, *i)
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


class ChallengesResourceResponse(ResourceResponse):

    def __init__(self, raw: dict):
        super().__init__(raw)

        self._challenges = dict()
