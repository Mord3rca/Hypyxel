import hypyxel
import unittest


class ResourcesAchievements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = hypyxel.Api(host='http://localhost:8000', key='test-key-ftw')

    def test_one_time_achievements(self):
        # Will except in case of parsing error
        achievements = self.api.resources.achievements

        self.assertTrue(len(achievements.one_time) == 30 and
                        len(achievements.tiered) == 30 and
                        len(achievements.total_points) == 30 and
                        len(achievements.total_legacy_points) == 30,
                        'Wrong number of games.')

        t = []
        for k, v in achievements.one_time.items():
            t += [(k, len(v))]

        r = [
            ("arcade", 70), ("arena", 36), ("bedwars", 43),
            ("blitz", 56), ("buildbattle", 23), ("christmas2017", 47),
            ("copsandcrims", 51), ("duels", 44), ("easter", 29), ("general", 16),
            ("gingerbread", 37), ("halloween2017", 64), ("housing", 11), ("murdermystery", 54),
            ("paintball", 34), ("pit", 62), ("quake", 57), ("skyblock", 125), ("skyclash", 40),
            ("skywars", 62), ("speeduhc", 26), ("summer", 11), ("supersmash", 27), ("tntgames", 86),
            ("truecombat", 35), ("uhc", 45), ("vampirez", 29), ("walls", 27), ("walls3", 144), ("warlords", 45),
        ]

        self.assertTrue(t == r, 'Games / number of achievements does not match')
