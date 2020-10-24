from unittest import TestCase
from hypyxel import Api

from datetime import datetime


class ResourcesGuilds(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.a = Api('http://localhost:8000')

    def test_guilds_achievements(self):

        c = self.a.resources.guilds.achievements

        self.assertTrue(c.last_update == datetime(2019, 10, 11, 2, 36, 38, 669000),
                        'Unexpected last_update')

        d = (
            ('PRESTIGE', 'Prestige'),
            ('EXPERIENCE_KINGS', 'Experience Kings'),
            ('WINNERS', 'Winners'),
            ('ONLINE_PLAYERS', 'What are you doing here?'),
        )

        self.assertTrue(len(c.tiered) == len(d), 'Unexpected tiered achievements number')
        v = tuple((i.name, i.display_name) for i in c.tiered)

        self.assertTrue(v == d, 'Unexpected tiered achievements')

        self.assertTrue(len(c.one_time) == 0,
                        'Unexpected one time achievements')

    def test_guilds_permissions(self):

        c = self.a.resources.guilds.permissions

        self.assertTrue(c.last_update == datetime(2019, 10, 11, 2, 36, 38, 669000),
                        'Invalid last_update')

        d = (
            ('Modify Guild Name', 'name_tag', 'Change the guild\'s name.'),
            ('Modify Guild MOTD', 'paper', 'Change the guild\'s message of the day.'),
            ('Modify Guild Tag', 'sign', 'Change the guild\'s tag.'),
            ('Change ranks', 'crafting_table', 'Promote or demote members (up to their own rank).'),
            ('Guild Finder options', 'book', 'Change how the guild is shown in the Guild Finder, if at all.'),
            ('Officer Chat', 'emerald', 'Send and receive messages in the officer chat.'),
            ('Kick Members', 'barrier', 'Kick members from the guild.'),
            ('Mute Members', 'redstone', 'Mute guild members.'),
            ('Invite members', 'arrow', 'Invite members to the guild.'),
            ('Audit Log', 'lever', 'View the audit log.'),
            ('View Stats', 'diamond', 'View a guild member\'s stats.'),
            ('Guild Party', 'chest', 'Start a guild party.'),
            ('Guild Settings', 'comparator', 'Change the guild settings.'),
            ('Change Guild Discord', 'filled_map', 'Change the guild\'s Discord join link.'),
        )

        self.assertTrue(len(c.permissions) == len(d),
                        'Unexpected number of permissions')

        v = tuple((i.name, i.item_name, i.desc) for i in c.permissions)

        self.assertTrue(v == d, 'Unexpected permissions')
