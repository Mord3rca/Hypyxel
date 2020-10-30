from hypyxel import Api
from datetime import datetime

from .utils import *


class GeneralEndpoints(HypyxelTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = Api(host='http://localhost:8000', key='test-key-ftw')

    def test_api_key(self):

        failure = Api(host='http://localhost:8000', key='invalid-key')
        success = self.api

        self.assertTrue(success.boosters.success, 'Success object failed')

        try:
            failure.boosters
        except Api.ApiException as e:
            pass
        else:
            self.assertTrue(False,
                            'Statement should have except for invalid API key')

    def test_boosters(self):

        b = self.api.boosters

        self.check_properties(b, ['boosters', 'decrementing'] +
                              self.API_RESPONSE_PROPERTIES)

        self.properties_full_check(b.boosters[0], {
            'id': '5c197fadc8f245280926413d',
            'purchaser': '978ddb705a8e43618e41749178c020b0',
            'amount': 2,
            'original_length': 3600,
            'remaining_length': 3595,
            'game': 24,
            'date': datetime.fromtimestamp(1545244519133 / 1000),
            'stacked': True
        })

        self.properties_full_check(b.boosters[1], {
            "id": "5f9929d344f4665db084ef57",
            "purchaser": "87c8b8c89e2d427bac5768557d3b7720",
            "amount": 3,
            "original_length": 3600,
            "remaining_length": 458,
            "game": 20,
            "date": datetime.fromtimestamp(1603873260661 / 1000),
            "stacked": (
                "add30e95-2e60-434f-aa86-9632f8d27561",
                "a76c3c84-d7a5-4d95-9d3e-f62d3818b958",
                "b5bad6c0-4c83-4e65-b238-dbbb7b1c7d75",
                "cdfd2c7e-daef-41de-bd78-7ff0e19de820",
                "3ac9f094-c48f-45a9-9c70-31ae9104ecbb",
                "d556c264-3225-42ca-9f62-a2c49852f695",
                "3d7d3b69-891a-4b40-949d-831c1f0c9929",
                "cb4c167b-be39-40e0-827a-9f4b437752b6",
                "b7a129db-29ea-44d4-be12-a2657b18e469",
                "0bb82300-2936-4607-a037-191dd92e8f9e"
            )
        })

        self.properties_full_check(b.boosters[2], {
            "id": "5f993cd30cf246888410b023",
            "purchaser": "fa78c39ef75c40f6beaf6df36a04c743",
            "amount": 2,
            "original_length": 3600,
            "remaining_length": 3600,
            "game": 20,
            "date": datetime.fromtimestamp(1603878202968 / 1000),
            "stacked": False
        })

    def test_find_guild(self):

        self.assertTrue(self.api.find_guild(name='This is a test'),
                        '553490650cf26f12ae5bac8f')

    def test_friends(self):

        f = self.api.friends('this-is-not-supported-by-test-server')

        self.properties_full_check(f,
                                   {
                                       'friends': self.SkipValue
                                   }, self.API_RESPONSE_PROPERTIES)

        self.properties_full_check(f.friends[0], {
                "id": "5f5898540cf29d31caa82593",
                "sender": "46c2bebc24ee44585894a73bd029f637",
                "receiver": "21071c044ecb43728a630fb49797a152",
                "started": datetime.fromtimestamp(1599641684473/1000)
        })

    def test_game_count(self):

        g = self.api.game_counts

        self.properties_full_check(g, {
            'games': self.SkipValue,
            'player_count': 59875
        }, self.API_RESPONSE_PROPERTIES)

        expected = {
            "MAIN_LOBBY": {
                "players": 278,
                'modes': {}
            },
            "SKYBLOCK": {
                "players": 29857,
                "modes": {
                    "combat_1": 803,
                    "dungeon_hub": 680,
                    "foraging_1": 936,
                    "hub": 10666,
                    "mining_2": 788,
                    "dungeon": 1524,
                    "combat_2": 145,
                    "farming_2": 120,
                    "mining_1": 227,
                    "farming_1": 106,
                    "combat_3": 1651,
                    "dynamic": 12212
                }
            },
            "SKYWARS": {
                "players": 3363,
                "modes": {
                    "solo_insane_lucky": 6,
                    "solo_insane_slime": 73,
                    "teams_insane_slime": 2,
                    "teams_insane_rush": 1,
                    "teams_insane": 265,
                    "solo_normal": 828,
                    "solo_insane_hunters_vs_beasts": 13,
                    "ranked_normal": 193,
                    "solo_insane_tnt_madness": 2,
                    "mega_doubles": 14,
                    "solo_insane_rush": 15,
                    "solo_insane": 1002,
                    "teams_normal": 363,
                    "mega_normal": 1
                }
            }
        }

        for i in g.games.keys():
            self.properties_full_check(g.games[i], expected[i])

    def test_guild(self):

        g = self.api.guild(name='unsupported-by-test-server')
        m, r = [g.members, g.ranks]

        self.properties_full_check(g, {
            "id": "553490650cf26f12ae5bac8f",
            "name": "Mini Squid",
            "coins": 425310,
            "max_coins": 1835310,
            "created": datetime.fromtimestamp(1429508197967/1000),
            "members": self.SkipValue,
            "tag": "\u00a7a1\u00a7e2\u00a7c3\u00a77",
            "tag_color": "GRAY",
            "achievements": {
                "WINNERS": 1080,
                "EXPERIENCE_KINGS": 316804,
                "ONLINE_PLAYERS": 125
            },
            "exp": 272653286,
            "legacy_rank": 2891,
            "ranks": self.SkipValue,
            "chat_mute": 0,
            "preferred_games": [
                "SKYWARS"
            ],
            "publicly_listed": True,
            "exp_by_game": {
                "DUELS": 25140197,
                "BUILD_BATTLE": 10760738,
                "HOUSING": 22466784,
            }
        }, self.API_RESPONSE_PROPERTIES)

        with self.subTest('Testing member object'):
            expected = (
                {
                    "id": "20934ef9488c465180a78f861586b4cf",
                    "rank": "GUILDMASTER",
                    "joined": datetime.fromtimestamp(1429508197967/1000),
                    "quests_participation": 139,
                    "exp_history": {
                        "2020-10-31": 0,
                        "2020-10-30": 0,
                        "2020-10-29": 513,
                        "2020-10-28": 0,
                        "2020-10-27": 454,
                        "2020-10-26": 0,
                        "2020-10-25": 617
                    }
                },
                {
                    "id": "6a12d6f63e134c8bbebc70d90a797281",
                    "rank": "Famous",
                    "joined": datetime.fromtimestamp(1518021755919/1000),
                    "quests_participation": 311,
                    "exp_history": {
                        "2020-10-31": 0,
                        "2020-10-30": 975,
                        "2020-10-29": 6022,
                        "2020-10-28": 157,
                        "2020-10-27": 0,
                        "2020-10-26": 0,
                        "2020-10-25": 0
                    }
                },
                {
                    "id": "a99d9661fe2d4594a6b3d910c85cc4a4",
                    "rank": "MEMBER",
                    "joined": datetime.fromtimestamp(1530770040736/1000),
                    "quests_participation": 800,
                    "exp_history": {
                        "2020-10-31": 0,
                        "2020-10-30": 0,
                        "2020-10-29": 0,
                        "2020-10-28": 0,
                        "2020-10-27": 0,
                        "2020-10-26": 0,
                        "2020-10-25": 0
                    }
                }
            )

            for i in range(len(m)):
                self.properties_full_check(m[i], expected[i])

        with self.subTest('Testing rank object'):

            expected = (
                {
                    "name": "Famous",
                    "default": False,
                    "tag": "F",
                    "created": datetime.fromtimestamp(1562382958149/1000),
                    "priority": 3
                },
                {
                    "name": "Member",
                    "default": True,
                    "tag": None,
                    "created": datetime.fromtimestamp(1562383012859/1000),
                    "priority": 2
                }
            )

            for i in range(len(r)):
                self.properties_full_check(r[i], expected[i])

    def test_key(self):

        self.properties_full_check(self.api.key, {
            'key': 'test-key-ftw',
            'limit': 120,
            'owner': '1337-G4M3R',
            'queries': 99,
            'total_queries': 42
        }, self.API_RESPONSE_PROPERTIES)

    def test_player(self):
        pass

    def test_player_count(self):

        self.assertTrue(self.api.player_count == 49567,
                        'Unexpected player count')

    def test_status(self):

        s = self.api.status('not-supported')

        self.properties_full_check(s, {
            "online": True,
            "game": "SKYBLOCK",
            "map": None,
            "mode": "dynamic"
        }, self.API_RESPONSE_PROPERTIES)

    def test_watchdogstats(self):

        self.properties_full_check(self.api.watchdog, {
            'last_minute': 3,
            'staff_rolling': 2441,
            'total': 5643086,
            'rolling': 3976,
            'staff_total': 1899760
        }, self.API_RESPONSE_PROPERTIES)
