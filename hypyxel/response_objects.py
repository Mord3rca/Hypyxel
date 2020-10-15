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
    def game(self) -> str:
        """
        Get the achievement game name
        :return:
        """
        return self._gname

    @property
    def name(self) -> str:
        """
        Get the Achievement DB name
        :return: Achievement DB name
        """
        return self._name

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


class HypixelChallengeReward:
    """
    Object representing challenge reward data
    """

    def __init__(self, data: dict):
        self.__data = data

        self._type = None
        self._amount = None

        self.__parse_data()

    def __parse_data(self):

        self._type = self.__data.get('type', None)
        self._amount = self.__data.get('amount', -1)

    @property
    def type(self) -> str:
        return self._type

    @property
    def amount(self) -> int:
        return self._amount


class HypixelChallenge:
    """
    Object representing challenge data
    """

    def __init__(self, gname: str, data: dict):
        self._gname = gname
        self._data = data
        self._id = None
        self._name = None
        self._rewards = tuple()

        self.__parse_challenge_data()

    def __parse_challenge_data(self):
        self._id = self._data.get('id', None)
        self._name = self._data.get('name', None)
        self._rewards = tuple(HypixelChallengeReward(i) for i in self._data.get('rewards', list()))

    @property
    def id(self) -> str:
        """
        Get the challenge DB id
        :return: Challenge DB id as string
        """
        return self._id

    @property
    def game(self) -> str:
        """
        Get the related challenge game name
        :return: Game name as string
        """
        return self._gname

    @property
    def name(self) -> str:
        """
        Get the challenge name
        :return: Challenge name
        """
        return self._name

    @property
    def rewards(self) -> Tuple[HypixelChallengeReward]:
        """
        Get the rewards list
        :return: Rewards list
        """
        return self._rewards
