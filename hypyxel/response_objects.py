from typing import Dict, Tuple, Union
from .utils import timestamp_to_datetime, datetime


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
    """
    Object representing a Objective
    """

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
    def id(self) -> str:
        """
        Get the objective ID
        :return: Objective ID
        """
        return self._id

    @property
    def type(self) -> str:
        """
        Get the objective type
        :return: Objective type
        """
        return self._type

    @property
    def amount(self) -> int:
        """
        Get the objective amount
        :return: Objective amount
        """
        return self._amount


class HypixelQuest:
    """
    Object representing a Quest
    """

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
    def id(self) -> str:
        """
        Get the Quest's ID
        :return: Quest ID
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get the Quest's name
        :return: Quest name
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Get the Quest's description
        :return: Quest description
        """
        return self._desc

    @property
    def game(self) -> str:
        """
        Get the related game for this quest
        :return: Related game for quest
        """
        return self._game

    @property
    def rewards(self) -> Tuple[HypixelChallengeReward]:
        """
        Get the rewards list
        :return: Rewards list
        """
        return self._rewards

    @property
    def objectives(self) -> Tuple[HypixelObjective]:
        """
        Get the Objective list
        :return: Objective list
        """
        return self._objectives

    @property
    def requirements(self) -> Tuple[str]:
        """
        Get the requirement list
        :return: Requirement list
        """
        return self._requirements


class HypixelPermission:
    """
    Object representing a Permission
    """

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
    def name(self) -> str:
        """
        Get Permission's name
        :return: Permission name
        """
        return self._name

    @property
    def desc(self) -> str:
        """
        Get Permission's description
        :return: Permission description
        """
        return self._desc

    @property
    def item_name(self) -> str:
        """
        Get Permission's item
        :return: Permission item
        """
        return self._item_name


class HypixelSkyblockItemTier:
    """
    Object representing a Skyblock Item Tier
    """

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
    def tier(self) -> int:
        """
        Get the tier number
        :return: Tier
        """
        return self.__tier

    @property
    def amount_required(self) -> int:
        """
        Get the amount of item required
        :return: Item amount
        """
        return self.__amountRequired

    @property
    def unlocks(self) -> Tuple[str]:
        """
        Get unlock list
        :return: Unlock list
        """
        return self.__unlocks


class HypixelSkyblockItemCollection:
    """
    Object representing a Skyblock Item Collection
    """

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
    def id(self) -> str:
        """
        Get the item collection ID
        :return: Collection ID
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Get the item collection name
        :return: Collection Name
        """
        return self.__name

    @property
    def max_tier(self) -> int:
        """
        Get the item Collection's maximum tier
        :return: Collection max tier
        """
        return self.__maxTier

    @property
    def tiers(self) -> Tuple[HypixelSkyblockItemTier]:
        """
        Get the item collection tier list
        :return: Tier list
        """
        return self.__tiers


class HypixelSkyblockCollection:
    """
    Object representing a Skyblock Collection
    """

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
    def id(self) -> str:
        """
        Get collection ID
        :return: Collection ID
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get collection name
        :return: Collection Name
        """
        return self._name

    @property
    def items(self) -> Tuple[HypixelSkyblockItemCollection]:
        """
        Get Collection's item
        :return: Collection Items
        """
        return self._items


class HypixelSkyblockSkillLevel:
    """
    Object representing a Skyblock Skill Level
    """

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
    def level(self) -> int:
        """
        Get skill level
        :return: Skill level
        """
        return self.__level

    @property
    def required_experience(self) -> int:
        """
        Get skill required experience
        :return: Skill Required Experience
        """
        return self.__exprequired

    @property
    def unlocks(self) -> Tuple[str]:
        """
        Get unlock list
        :return: Unlock list
        """
        return self.__unlocks


class HypixelSkyblockSkill:
    """
    Object representing a Skyblock Skill
    """

    def __init__(self, id: str, data: dict):
        self.__data = data

        self.__id = id
        self.__name = None
        self.__desc = None
        self.__maxlevel = -1
        self.__levels = tuple()

        self.__parse_data()

    def __parse_data(self):
        self.__name = self.__data.get('name', None)
        self.__desc = self.__data.get('description', None)
        self.__maxlevel = self.__data.get('maxLevel', -1)
        self.__levels = tuple(
            HypixelSkyblockSkillLevel(i) for i in self.__data.get('levels', ())
        )

    @property
    def id(self) -> str:
        """
        Get Skill ID
        :return: skill ID
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Get skill name
        :return: Skill name
        """
        return self.__name

    @property
    def description(self) -> str:
        """
        Get skill description
        :return: Skill description
        """
        return self.__desc

    @property
    def max_level(self) -> int:
        """
        Get skill max level
        :return: Skill max level
        """
        return self.__maxlevel

    @property
    def levels(self) -> Tuple[HypixelSkyblockSkillLevel]:
        """
        Get level list
        :return: Skill level list
        """
        return self.__levels


class RecentGame:

    def __init__(self, data: dict):

        self.__data = data

        self.__begin = -1
        self.__end = -1
        self.__game = None
        self.__mode = None
        self.__map = None

        self.__parse_data()

    def __parse_data(self):

        self.__begin = self.__data.get('date', None)
        self.__end = self.__data.get('ended', None)
        self.__game = self.__data.get('gameType', None)
        self.__mode = self.__data.get('mode', None)
        self.__map = self.__data.get('map', None)

    @property
    def begin(self) -> datetime:
        return timestamp_to_datetime(self.__begin)

    @property
    def end(self) -> datetime:
        return timestamp_to_datetime(self.__end)

    @property
    def game(self) -> str:
        return self.__game

    @property
    def mode(self) -> str:
        return self.__mode

    @property
    def map(self) -> str:
        return self.__map

    def still_playing(self) -> bool:
        return self.__end == -1


class Booster:

    def __init__(self, data: dict):

        self.__data = data

        self.__id = None
        self.__purchaser_uuid = None
        self.__amount = -1
        self.__original_length = -1
        self.__length = -1
        self.__game = -1
        self.__date_activated = -1
        self.__stacked = None

        self.__parse_data()

    def __parse_data(self):
        self.__id = self.__data.get('_id', None)
        self.__purchaser_uuid = self.__data.get('purchaserUuid', None)
        self.__amount = self.__data.get('amount', -1)
        self.__original_length = self.__data.get('originalLength', -1)
        self.__length = self.__data.get('length', -1)
        self.__game = self.__data.get('gameType', -1)
        self.__date_activated = self.__data.get('dateActivated', None)

        stacked = self.__data.get('stacked', False)
        self.__stacked = stacked if\
            type(stacked) == bool else (i for i in stacked)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def purchaser(self) -> str:
        return self.__purchaser_uuid

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def original_length(self) -> int:
        return self.__original_length

    @property
    def remaining_length(self) -> int:
        return self.__length

    @property
    def game(self) -> int:
        return self.__game

    @property
    def date(self) -> datetime:
        return timestamp_to_datetime(self.__date_activated)

    @property
    def stacked(self) -> Union[bool, Tuple[str]]:
        return self.__stacked


class GuildMember:

    def __init__(self, data: dict):
        self.__data = data

        self.__uuid = None
        self.__rank = None
        self.__joined = -1
        self.__quests_part = -1
        self.__exp_hist = dict()

        self.__parse_data()

    def __parse_data(self):
        self.__uuid = self.__data.get('uuid', None)
        self.__rank = self.__data.get('rank', None)
        self.__joined = self.__data.get('joined', None)
        self.__quests_part = self.__data.get('questParticipation', -1)
        self.__exp_hist = self.__data.get('expHistory', {})

    @property
    def id(self) -> str:
        return self.__uuid

    @property
    def rank(self) -> str:
        return self.__rank

    @property
    def joined(self) -> datetime:
        return timestamp_to_datetime(self.__joined)

    @property
    def quests_participation(self) -> int:
        return self.__quests_part

    @property
    def exp_history(self) -> Dict[str, int]:
        return self.__exp_hist


class GuildRank:

    def __init__(self, data: dict):
        self.__data = data

        self.__name = None
        self.__default = None
        self.__tag = None
        self.__created = None
        self.__priority = -1

        self.__parse_data()

    def __parse_data(self):
        self.__name = self.__data.get('name', None)
        self.__default = self.__data.get('default', None)
        self.__tag = self.__data.get('tag', None)
        self.__created = self.__data.get('created', None)
        self.__priority = self.__data.get('priority', None)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def default(self) -> bool:
        return self.__default

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def created(self) -> datetime:
        return timestamp_to_datetime(self.__created)

    @property
    def priority(self) -> int:
        return self.__priority


class Friend:

    def __init__(self, data: dict):
        self.__data = data

        self.__id = None
        self.__sender = None
        self.__receiv = None
        self.__started = None

        self.__parse_data()

    def __parse_data(self):
        self.__id = self.__data.get('_id', None)
        self.__sender = self.__data.get('uuidSender', None)
        self.__receiv = self.__data.get('uuidReceiver', None)
        self.__started = self.__data.get('started', None)

    @property
    def id(self):
        return self.__id

    @property
    def sender(self):
        return self.__sender

    @property
    def receiver(self):
        return self.__receiv

    @property
    def started(self) -> datetime:
        return timestamp_to_datetime(self.__started)


class GameStatus:

    def __init__(self, data: dict):
        self.__data = data

        self.__players = None
        self.__modes = None

        self.__parse_data()

    def __parse_data(self):
        self.__players = self.__data.get('players', None)
        self.__modes = self.__data.get('modes', {})

    @property
    def players(self) -> int:
        return self.__players

    @property
    def modes(self) -> Dict[str, int]:
        return self.__modes


class Leaderboard:

    def __init__(self, data: dict):
        self.__data = data

        self.__path = None
        self.__prefix = None
        self.__title = None
        self.__location = None
        self.__count = None
        self.__leaders = None

        self.__parse_data()

    def __parse_data(self):
        self.__path = self.__data.get('path', None)
        self.__prefix = self.__data.get('prefix', None)
        self.__title = self.__data.get('title', None)
        self.__location = tuple(
            int(i) for i in self.__data.get('location', ",,").split(',')
        )
        self.__count = self.__data.get('count', None)
        self.__leaders = tuple(
            i for i in self.__data.get('leaders', ())
        )

    @property
    def path(self) -> str:
        return self.__path

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def title(self) -> str:
        return self.__title

    @property
    def location(self) -> Tuple[int, int, int]:
        return self.__location

    @property
    def count(self) -> int:
        return self.__count

    @property
    def leaders(self) -> Tuple[str]:
        return self.__leaders
