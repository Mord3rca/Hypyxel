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
        self._globalPercentUnlocked =\
            self._data.get("globalPercentUnlocked", None)
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
        self._rewards =\
            tuple(HypixelChallengeReward(i)
                  for i in self._data.get('rewards', list()))

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


class HypixelObjective:

    def __init__(self, data: dict):

        self.__data = data
        self._id = None
        self._type = None
        self._amount = -1

        self.__parse_data()

    def __parse_data(self):

        self._id = self.__data.get('id', None)
        self._type = self.__data.get('type', None)
        self._amount = self.__data.get('integer', -1)

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def amount(self):
        return self._amount


class HypixelQuest:

    def __init__(self, gname, data: dict):
        self.__data = data

        self._id = None
        self._name = None
        self._desc = None
        self._game = gname

        self._rewards = tuple()
        self._objectives = tuple()
        self._requirements = tuple()

        self.__parse_data()

    def __parse_data(self):

        self._id = self.__data.get('id', None)
        self._name = self.__data.get('name', None)
        self._desc = self.__data.get('description', None)

        self._requirements = tuple(
            i.get('type', None) for i in self.__data.get('requirements', [])
        )
        self._rewards = tuple(
            HypixelChallengeReward(i) for i in self.__data.get('rewards', [])
        )
        self._objectives = tuple(
            HypixelObjective(i) for i in self.__data.get('objectives', [])
        )

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._desc

    @property
    def game(self):
        return self._game

    @property
    def rewards(self):
        return self._rewards

    @property
    def objectives(self):
        return self._objectives

    @property
    def requirements(self):
        return self._requirements


class HypixelPermission:

    def __init__(self, data: dict):
        self.__data = data

        self._name = None
        self._desc = None
        self._item_name = None

        self.__parse_data()

    def __parse_data(self):
        info = self.__data.get('en_us', None)

        self._name = info.get('name', None)
        self._desc = info.get('description', None)
        self._item_name = info.get('item', {}).get('name', None)

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def item_name(self):
        return self._item_name


class HypixelSkyblockItemTier:

    def __init__(self, data: dict):
        self.__data = data

        self.__tier = -1
        self.__amountRequired = -1
        self.__unlocks = tuple()

        self.__parse_data()

    def __parse_data(self):
        self.__tier = self.__data.get('tier', -1)
        self.__amountRequired = self.__data.get('amountRequired', -1)
        self.__unlocks = tuple(
            self.__data.get('unlocks', [])
        )

    @property
    def tier(self):
        return self.__tier

    @property
    def amount_required(self):
        return self.__amountRequired

    @property
    def unlocks(self):
        return self.__unlocks


class HypixelSkyblockItemCollection:

    def __init__(self, id: str, data: dict):
        self.__data = data

        self.__id = id
        self.__name = None
        self.__maxTier = -1
        self.__tiers = tuple()

        self.__parse_data()

    def __parse_data(self):
        self.__name = self.__data.get('name', None)
        self.__maxTier = self.__data.get('maxTiers', -1)
        self.__tiers = tuple(
            HypixelSkyblockItemTier(i) for i in self.__data.get('tiers', [])
        )

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def max_tier(self):
        return self.__maxTier

    @property
    def tiers(self):
        return self.__tiers


class HypixelSkyblockCollection:

    def __init__(self, id: str, data: dict):

        self._data = data

        self._id = id
        self._name = None
        self._items = tuple()

        self.__parse_data()

    def __parse_data(self):

        self._name = self._data.get('name', None)

        self._items = tuple(
            HypixelSkyblockItemCollection(i, self._data.get('items')[i])
            for i in self._data.get('items', {}).keys()
        )

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return self._items


class HypixelSkyblockSkillLevel:
    def __init__(self, data: dict):
        self.__data = data

        self.__level = -1
        self.__exprequired = -1
        self.__unlocks = tuple()

        self.__parse_data()

    def __parse_data(self):
        self.__level = self.__data.get('level', -1)
        self.__exprequired = self.__data.get('totalExpRequired', -1)
        self.__unlocks = tuple(
            self.__data.get('unlocks')
        )

    @property
    def level(self):
        return self.__level

    @property
    def required_experience(self):
        return self.__exprequired

    @property
    def unlocks(self):
        return self.__unlocks


class HypixelSkyblockSkill:
    def __init__(self, id: str, data: dict):
        self.__data = data

        self.__id = id
        self.__name = None
        self.__desc = None
        self.__maxlevel = -1
        self.__levels = -1

        self.__parse_data()

    def __parse_data(self):
        self.__name = self.__data.get('name', None)
        self.__desc = self.__data.get('description', None)
        self.__maxlevel = self.__data.get('maxLevel', -1)
        self.__levels = tuple(
            HypixelSkyblockSkillLevel(i) for i in self.__data.get('levels', ())
        )

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__desc

    @property
    def max_level(self):
        return self.__maxlevel

    @property
    def levels(self):
        return self.__levels
