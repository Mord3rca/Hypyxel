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

        self.__parse_resource_data()

    def __parse_resource_data(self):
        self._last_update = self._raw.get('lastUpdated', -1)

    @property
    def last_update(self) -> datetime:
        """
        Get the last update date
        :return: datetime object or None in case of error
        """
        return timestamp_to_datetime(self._last_update) \
            if self._last_update != -1 else None


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
