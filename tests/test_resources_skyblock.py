from unittest import TestCase
from hypyxel import Api

from datetime import datetime


class ResourcesSkyblock(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.a = Api('http://localhost:8000')

    def test_skyblock_collections(self):

        c = self.a.resources.skyblock.collections

        self.assertTrue(c.version == '0.9.102', 'Unexpected Skyblock version')

        self.assertTrue(c.last_update == datetime(2020, 10, 23, 8, 55, 58, 805000),
                        'Unexpected last update')

        d = ('FARMING', 'MINING', 'COMBAT', 'FORAGING', 'FISHING')

        self.assertTrue(tuple(c.collections.keys()) == d, 'Unexpected collection keys')

        self.assertTrue(len(c.collections.values()) == 5,
                        'Unexpected number of collection values')

    def test_skyblock_skills(self):

        c = self.a.resources.skyblock.skills

        self.assertTrue(c.version == '0.9.102', 'Unexpected Skyblock version')

        self.assertTrue(c.last_update == datetime(2020, 10, 23, 8, 55, 58, 825000),
                        'Unexpected last update')

        d = ('FARMING', 'MINING', 'COMBAT',
             'DUNGEONEERING', 'FORAGING', 'FISHING',
             'ENCHANTING', 'ALCHEMY', 'CARPENTRY',
             'RUNECRAFTING', 'TAMING')

        self.assertTrue(tuple(c.skills.keys()) == d, 'Unexpected skills keys')
