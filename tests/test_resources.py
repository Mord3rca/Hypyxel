from hypyxel import Api
from .utils import *

from datetime import datetime


class ResourcesEndpoints(HypyxelTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = Api(host='http://localhost:8000', key='test-key-ftw')

    def test_achievements(self):
        # Will except in case of parsing error
        achievements = self.api.resources.achievements
        t, o = [achievements.tiered, achievements.one_time]

        self.properties_full_check(achievements, {
            "last_update": datetime.fromtimestamp(1602342327386 / 1000),
            "tiered": self.SkipValue,
            "one_time": self.SkipValue,
            "total_points": {'skyblock': 1700},
            "total_legacy_points": {'skyblock': 0}
        }, self.API_RESPONSE_PROPERTIES)

        with self.subTest('Tiered achievements'):
            expected = {
                "name": "MINION_LOVER",
                "game": "skyblock",
                "display_name": "Minion Lover",
                "description": "[Coop or you] Craft %s unique minions",
                "tiers": self.SkipValue
            }

            self.properties_full_check(t['skyblock'][0], expected)

            tiers = t['skyblock'][0].tiers

            expected = (
                {
                    "tier": 1,
                    "points": 5,
                    "amount": 10
                },
                {
                    "tier": 2,
                    "points": 10,
                    "amount": 25
                },
                {
                    "tier": 3,
                    "points": 15,
                    "amount": 100
                },
                {
                    "tier": 4,
                    "points": 20,
                    "amount": 250
                },
                {
                    "tier": 5,
                    "points": 25,
                    "amount": 500
                }
            )

            for i in range(len(expected)):
                self.properties_full_check(tiers[i], expected[i])

        with self.subTest('One Time achievements'):
            expected = (
                {
                    'name': "EXPLOSIVE_ENDING",
                    'game': 'skyblock',
                    "point": 5,
                    'secret': False,
                    'legacy': False,
                    "display_name": "Explosive Ending",
                    "description":
                        "Survive the Blast from the Unstable Dragon",
                    "game_percent_unlocked": 3.270266309767166,
                    "global_percent_unlocked": 1.0118791009020422
                },
                {
                    'name': "I_AM_SUPERIOR",
                    'game': 'skyblock',
                    "point": 10,
                    "display_name": "I am Superior",
                    "description": "???",
                    "secret": True,
                    'legacy': False,
                    "game_percent_unlocked": 1.9991501533629066,
                    "global_percent_unlocked": 0.6185729442618582
                }
            )

            for i in range(len(o['skyblock'])):
                self.properties_full_check(o['skyblock'][i], expected[i])

    def test_challenges(self):
        c = self.api.resources.challenges

        self.properties_full_check(c, {
            "last_update": datetime.fromtimestamp(1602773584751 / 1000),
            "challenges": self.SkipValue
        }, self.API_RESPONSE_PROPERTIES)

        expected = (
            {
                "id": "UHC__longshot_challenge",
                "game": "uhc",
                "name": "Longshot Challenge",
                "rewards": self.SkipValue
            },
            {
                "id": "UHC__perfect_start_challenge",
                "game": "uhc",
                "name": "Perfect Start Challenge",
                "rewards": self.SkipValue
            },
            {
                "id": "UHC__hunter_challenge",
                "game": "uhc",
                "name": "Hunter Challenge",
                "rewards": self.SkipValue
            },
            {
                "id": "UHC__threat_challenge",
                "game": "uhc",
                "name": "Threat Challenge",
                "rewards": self.SkipValue
            }
        )

        for i in range(len(expected)):
            self.properties_full_check(c.challenges[i], expected[i])

        self.properties_full_check(c.challenges[0].rewards[0],
                                   {
                                       "type": "MultipliedExperienceReward",
                                       "amount": 3360
                                   })

    def test_guilds_achievements(self):

        a = self.api.resources.guilds.achievements

        t, o = [a.tiered, a.one_time]

        self.properties_full_check(a, {
            "last_update": datetime.fromtimestamp(1570754198669 / 1000),
            "one_time": tuple(),
            "tiered": self.SkipValue
        }, self.API_RESPONSE_PROPERTIES)

        expected = (
            {
                "name": "PRESTIGE",
                "game": None,
                "display_name": "Prestige",
                "description": "Reach Guild level %s",
                "tiers": self.SkipValue
            },
            {
                "name": "EXPERIENCE_KINGS",
                "game": None,
                "display_name": "Experience Kings",
                "description": "get %s Guild Exp in one day",
                "tiers": self.SkipValue
            }
        )

        for i in range(len(expected)):
            self.properties_full_check(t[i], expected[i])

        expected = (
            {
                "tier": 1,
                "amount": 20,
                "points": None
            },
            {
                "tier": 2,
                "amount": 40,
                "points": None
            },
            {
                "tier": 3,
                "amount": 60,
                "points": None
            },
            {
                "tier": 4,
                "amount": 80,
                "points": None
            },
            {
                "tier": 5,
                "amount": 100,
                "points": None
            }
        )

        for i in range(len(expected)):
            self.properties_full_check(t[0].tiers[i], expected[i])

    def test_guilds_permissions(self):

        p = self.api.resources.guilds.permissions

        self.properties_full_check(p, {
            "last_update": datetime.fromtimestamp(1570754198669 / 1000),
            "permissions": self.SkipValue
        }, self.API_RESPONSE_PROPERTIES)

        expected = (
            {
                "name": "Modify Guild Name",
                "desc": "Change the guild's name.",
                "item_name": "name_tag"
            },
            {
                "name": "Modify Guild MOTD",
                "desc": "Change the guild's message of the day.",
                "item_name": "paper"
            }
        )

        for i in range(len(expected)):
            self.properties_full_check(p.permissions[i], expected[i])

    def test_resources_quests(self):
        c = self.api.resources.quests

        self.properties_full_check(c, {
            'last_update': datetime.fromtimestamp(1603271458771 / 1000),
            'quests': self.SkipValue
        }, self.API_RESPONSE_PROPERTIES)

        c = c.quests

        expected = (
            {
                "id": "skywars_solo_win",
                "game": "skywars",
                "name": "Daily Quest: Skywars Solo Win",
                "rewards": self.SkipValue,
                "objectives": self.SkipValue,
                "requirements": self.SkipValue,
                "description": "Win a game in Solo Mode"
            },
            {
                "id": "skywars_weekly_arcade_win_all",
                "game": "skywars",
                "name": "Weekly Quest: Skywars Scientist",
                "rewards": self.SkipValue,
                "objectives": self.SkipValue,
                "requirements": self.SkipValue,
                "description": "Win 10 games in any lab mode"
            }
        )

        for i in range(len(expected)):
            self.properties_full_check(c[i], expected[i])

        expected = (
            {
                "type": "MultipliedExperienceReward",
                "amount": 3000
            },
            {
                "type": "MultipliedCoinReward",
                "amount": 1500
            },
            {
                "type": "SkyWarsSoulReward",
                "amount": 1
            }
        )

        for i in range(len(expected)):
            self.properties_full_check(c[0].rewards[i], expected[i])

        expected = {
                "id": "skywars_solo_win",
                "type": "IntegerObjective",
                "amount": 1
        }

        self.properties_full_check(c[0].objectives[0], expected)

        self.assertTrue(c[0].requirements[0] == "DailyResetQuestRequirement",
                        'Unexpected value for requirements')

    def test_skyblock_collections(self):

        c = self.api.resources.skyblock.collections

        self.properties_full_check(c, {
            "last_update": datetime.fromtimestamp(1603436158805 / 1000),
            "version": "0.9.102",
            "collections": self.SkipValue
        }, self.API_RESPONSE_PROPERTIES)

        c = c.collections["FARMING"]

        self.properties_full_check(c, {
            "id": "FARMING",
            "name": "Farming",
            "items": self.SkipValue
        })

        c = c.items[0]

        self.properties_full_check(c, {
            "id": "POTATO_ITEM",
            "name": "Potato",
            "max_tier": 9,
            "tiers": self.SkipValue
        })

        self.assertTrue(len(c.tiers) == c.max_tier)

        c = c.tiers[0]

        self.properties_full_check(c, {
            "tier": 1,
            "amount_required": 100,
            "unlocks": ("Potato Minion Recipes",)
        })

    def test_skyblock_skills(self):

        s = self.api.resources.skyblock.skills

        self.properties_full_check(s, {
            "last_update": datetime.fromtimestamp(1603436158825 / 1000),
            "version": "0.9.102",
            "skills": self.SkipValue
        }, self.API_RESPONSE_PROPERTIES)

        s = s.skills["MINING"]

        self.properties_full_check(s, {
            "id": "MINING",
            "name": "Mining",
            "description":
                "Spelunk islands for ores and valuable materials to earn Mining XP!",
            "max_level": 50,
            "levels": self.SkipValue
        })

        self.assertTrue(len(s.levels) == s.max_level)

        s = s.levels[0]

        self.properties_full_check(s, {
            "level": 1,
            "required_experience": 50.0,
            "unlocks": (
                "Spelunker I   4% chance to get double ores.",
                "+1 \u2748 Defense",
                "Access to Gold Mine",
                "+25 Coins"
            )
        })
