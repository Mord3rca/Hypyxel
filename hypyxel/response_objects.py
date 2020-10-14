from typing import Dict, Tuple


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

        self._tiers = tuple(HypixelAchievementTier(i)
                            for i in data.get("tiers", [])
                            )

    @property
    def tiers(self) -> Tuple[HypixelAchievementTier]:
        """
        Get tiers for this achievements
        :return: Return table of HypixelAchievementTier
        """
        return self._tiers


class HypixelChallenge:

    def __init__(self, gname:str, data: dict):
        self._gname = gname
        self._id = None
        self._name = None
        self._rewards = tuple()

        self.__parse_challenge_data(data)

    def __parse_challenge_data(self, data: dict):
        self._id = data.get('id', None)
        self._name = data.get('name', None)
        self._rewards = []

