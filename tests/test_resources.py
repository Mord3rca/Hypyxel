from hypyxel import Api
from unittest import TestCase

from datetime import datetime


class ResourcesEndpoints(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = Api(host='http://localhost:8000', key='test-key-ftw')

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

    def test_challenges(self):
        c = self.api.resources.challenges

        self.assertTrue(c.last_update == datetime(2020, 10, 15, 16, 53, 4, 751000),
                        'Wrong datetime for last_update')

        v = tuple((i.name, i.id, i.game) for i in c.challenges)

        d = (
            ('Farm Hunt Challenge', 'ARCADE__farm_hunt_challenge', 'arcade'),
            ('Blocking Dead Challenge', 'ARCADE__blocking_dead_challenge', 'arcade'),
            ('Bounty Hunter Challenge', 'ARCADE__bounty_hunter_challenge', 'arcade'),
            ('Creeper Attack Challenge', 'ARCADE__creeper_attack_challenge', 'arcade'),
            ('Dragon Wars Challenge', 'ARCADE__dragon_wars_challenge', 'arcade'),
            ('Ender Spleef Challenge', 'ARCADE__ender_spleef_challenge', 'arcade'),
            ('Galaxy Wars Challenge', 'ARCADE__galaxy_wars_challenge', 'arcade'),
            ('Throw Out Challenge', 'ARCADE__throw_out_challenge', 'arcade'),
            ('Hole in the Wall Challenge', 'ARCADE__hole_in_the_wall_challenge', 'arcade'),
            ('Hypixel Says Challenge', 'ARCADE__hypixel_says_challenge', 'arcade'),
            ('Pixel Painters Challenge', 'ARCADE__pixel_painters_challenge', 'arcade'),
            ('Party Games Challenge', 'ARCADE__party_games_challenge', 'arcade'),
            ('Football Challenge', 'ARCADE__football_challenge', 'arcade'),
            ('Mini Walls Challenge', 'ARCADE__mini_walls_challenge', 'arcade'),
            ('Capture the Wool Challenge', 'ARCADE__capture_the_wool_challenge', 'arcade'),
            ('Zombies Challenge', 'ARCADE__zombies_challenge', 'arcade'),
            ('Hide and Seek Challenge', 'ARCADE__hide_and_seek_challenge', 'arcade'),
            ('WHERE IS IT Challenge', 'ARENA__where_is_it_challenge', 'arena'),
            ('Triple Kill Challenge', 'ARENA__triple_kill_challenge', 'arena'),
            ('No Ultimate Challenge', 'ARENA__no_ultimate_challenge', 'arena'),
            ('Cooperation Challenge', 'ARENA__cooperation_challenge', 'arena'),
            ('Defensive', 'BEDWARS__defensive', 'bedwars'),
            ('Support', 'BEDWARS__support', 'bedwars'),
            ('Offensive', 'BEDWARS__offensive', 'bedwars'),
            ('Star Challenge', 'SURVIVAL_GAMES__star_challenge', 'hungergames'),
            ('Iron Man Challenge', 'SURVIVAL_GAMES__iron_man_challenge', 'hungergames'),
            ('Blitz Challenge', 'SURVIVAL_GAMES__blitz_challenge', 'hungergames'),
            ('Resistance Challenge', 'SURVIVAL_GAMES__resistance_challenge', 'hungergames'),
            ('Top 3 Challenge', 'BUILD_BATTLE__top_3_challenge', 'buildbattle'),
            ('Guesser Challenge', 'BUILD_BATTLE__guesser_challenge', 'buildbattle'),
            ('Rampage Challenge', 'TRUE_COMBAT__rampage_challenge', 'truecombat'),
            ('Samples Challenge', 'TRUE_COMBAT__samples_challenge', 'truecombat'),
            ('Archer Challenge', 'TRUE_COMBAT__archer_challenge', 'truecombat'),
            ('Super Lucky Challenge', 'TRUE_COMBAT__super_lucky_challenge', 'truecombat'),
            ('Feed The Void Challenge', 'DUELS__feed_the_void_challenge', 'duels'),
            ('Teams Challenge', 'DUELS__teams_challenge', 'duels'),
            ('Target Practice Challenge', 'DUELS__target_practice_challenge', 'duels'),
            ('Pistol Challenge', 'MCGO__pistol_challenge', 'mcgo'),
            ('Knife Challenge', 'MCGO__knife_challenge', 'mcgo'),
            ('Grenade Challenge', 'MCGO__grenade_challenge', 'mcgo'),
            ('Killing Spree Challenge', 'MCGO__killing_spree_challenge', 'mcgo'),
            ('Murder Spree', 'MURDER_MYSTERY__murder_spree', 'murdermystery'),
            ('Sherlock', 'MURDER_MYSTERY__sherlock', 'murdermystery'),
            ('Hero', 'MURDER_MYSTERY__hero', 'murdermystery'),
            ('Serial Killer', 'MURDER_MYSTERY__serial_killer', 'murdermystery'),
            ('Kill Streak Challenge', 'PAINTBALL__kill_streak_challenge', 'paintball'),
            ('Killing Spree Challenge', 'PAINTBALL__killing_spree_challenge', 'paintball'),
            ('Nuke Challenge', 'PAINTBALL__nuke_challenge', 'paintball'),
            ('Finish Challenge', 'PAINTBALL__finish_challenge', 'paintball'),
            ('Powerup Challenge', 'QUAKECRAFT__powerup_challenge', 'quake'),
            ('Killing Streak Challenge', 'QUAKECRAFT__killing_streak_challenge', 'quake'),
            ('Don\'t Blink Challenge', 'QUAKECRAFT__don\'t_blink_challenge', 'quake'),
            ('Combo Challenge', 'QUAKECRAFT__combo_challenge', 'quake'),
            ('Enderchest Challenge', 'SKYCLASH__enderchest_challenge', 'skyclash'),
            ('Teamwork Challenge', 'SKYCLASH__teamwork_challenge', 'skyclash'),
            ('Fighter Challenge', 'SKYCLASH__fighter_challenge', 'skyclash'),
            ('Monster Killer Challenge', 'SKYCLASH__monster_killer_challenge', 'skyclash'),
            ('Feeding the Void Challenge', 'SKYWARS__feeding_the_void_challenge', 'skywars'),
            ('Rush Challenge', 'SKYWARS__rush_challenge', 'skywars'),
            ('Ranked Challenge', 'SKYWARS__ranked_challenge', 'skywars'),
            ('Enderman Challenge', 'SKYWARS__enderman_challenge', 'skywars'),
            ('Leaderboard Challenge', 'SUPER_SMASH__leaderboard_challenge', 'supersmash'),
            ('Crystal Challenge', 'SUPER_SMASH__crystal_challenge', 'supersmash'),
            ('Smash Challenge', 'SUPER_SMASH__smash_challenge', 'supersmash'),
            ('Flawless Challenge', 'SUPER_SMASH__flawless_challenge', 'supersmash'),
            ('Alchemist Challenge', 'SPEED_UHC__alchemist_challenge', 'speeduhc'),
            ('Wizard Challenge', 'SPEED_UHC__wizard_challenge', 'speeduhc'),
            ('Marksman Challenge', 'SPEED_UHC__marksman_challenge', 'speeduhc'),
            ('Nether Challenge', 'SPEED_UHC__nether_challenge', 'speeduhc'),
            ('Coin Challenge', 'GINGERBREAD__coin_challenge', 'gingerbread'),
            ('First Place Challenge', 'GINGERBREAD__first_place_challenge', 'gingerbread'),
            ('Banana Challenge', 'GINGERBREAD__banana_challenge', 'gingerbread'),
            ('Leaderboard Challenge', 'GINGERBREAD__leaderboard_challenge', 'gingerbread'),
            ('TNT Run Challenge', 'TNTGAMES__tnt_run_challenge', 'tntgames'),
            ('PVP Run Challenge', 'TNTGAMES__pvp_run_challenge', 'tntgames'),
            ('Bow Spleef Challenge', 'TNTGAMES__bow_spleef_challenge', 'tntgames'),
            ('TNT Tag Challenge', 'TNTGAMES__tnt_tag_challenge', 'tntgames'),
            ('TNT Wizards Challenge', 'TNTGAMES__tnt_wizards_challenge', 'tntgames'),
            ('TNT Wizards Challenge', 'TNTGAMES__tnt_wizards_challenge', 'tntgames'),
            ('TNT Run Challenge', 'TNTGAMES__tnt_run_challenge', 'tntgames'),
            ('TNT Wizard Challenge', 'TNTGAMES__tnt_wizard_challenge', 'tntgames'),
            ('Bow Spleef Challenge', 'TNTGAMES__bow_spleef_challenge', 'tntgames'),
            ('TNT Tag Challenge', 'TNTGAMES__tnt_tag_challenge', 'tntgames'),
            ('Longshot Challenge', 'UHC__longshot_challenge', 'uhc'),
            ('Perfect Start Challenge', 'UHC__perfect_start_challenge', 'uhc'),
            ('Hunter Challenge', 'UHC__hunter_challenge', 'uhc'),
            ('Threat Challenge', 'UHC__threat_challenge', 'uhc'),
            ('Fang Challenge', 'VAMPIREZ__fang_challenge', 'vampirez'),
            ('Gold Challenge', 'VAMPIREZ__gold_challenge', 'vampirez'),
            ('Purifying Challenge', 'VAMPIREZ__purifying_challenge', 'vampirez'),
            ('Last Stand Challenge', 'VAMPIREZ__last_stand_challenge', 'vampirez'),
            ('Wither Challenge', 'WALLS3__wither_challenge', 'walls3'),
            ('Protector Challenge', 'WALLS3__protector_challenge', 'walls3'),
            ('Berserk Challenge', 'WALLS3__berserk_challenge', 'walls3'),
            ('Comeback Challenge', 'WALLS3__comeback_challenge', 'walls3'),
            ('First Blood Challenge', 'WALLS__first_blood_challenge', 'walls'),
            ('Powerhouse Challenge', 'WALLS__powerhouse_challenge', 'walls'),
            ('Looting Challenge', 'WALLS__looting_challenge', 'walls'),
            ('Double Kill Challenge', 'WALLS__double_kill_challenge', 'walls'),
            ('Support Challenge', 'BATTLEGROUND__support_challenge', 'battleground'),
            ('Brute Challenge', 'BATTLEGROUND__brute_challenge', 'battleground'),
            ('Capture Challenge', 'BATTLEGROUND__capture_challenge', 'battleground'),
            ('Carry Challenge', 'BATTLEGROUND__carry_challenge', 'battleground'),
        )

        self.assertTrue(v == d, 'Unexpected challenge list')

        v = c.challenges[40]

        self.assertTrue(v.name == 'Killing Spree Challenge', f'Unexpected name for challenge[40], got: {v.name}')
        self.assertTrue(v.id == 'MCGO__killing_spree_challenge', f'Unexpected id for challenge[40], got: {v.id}')
        self.assertTrue(v.game == 'mcgo', f'Unexpected game for challenge[40], got: {v.game}')

    def test_guilds_achievements(self):

        c = self.api.resources.guilds.achievements

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

        c = self.api.resources.guilds.permissions

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

    def test_resources_quests(self):
        c = self.api.resources.quests

        self.assertTrue(
            c.last_update == datetime(2020, 10, 21, 11, 10, 58, 771000),
            'Datetime invalid'
        )

        self.assertTrue(len(c.quests) == 120,
                        'Unexpected number of quests')

        d = (
            ('quake_daily_play', 'Daily Quest: Quake Player', 'quake'),
            ('quake_daily_kill', 'Daily Quest: Sniper', 'quake'),
            ('quake_daily_win', 'Daily Quest: Winner', 'quake'),
            ('quake_weekly_play', 'Weekly Quest: Bazinga!', 'quake'),
            ('walls_daily_play', 'Daily Quest: Waller', 'walls'),
            ('walls_daily_kill', 'Daily Quest: Kills', 'walls'),
            ('walls_daily_win', 'Daily Quest: Win', 'walls'),
            ('walls_weekly', 'Weekly Quest: Walls Weekly', 'walls'),
            ('paintballer', 'Daily Quest: Paintballer', 'paintball'),
            ('paintball_killer', 'Daily Quest: Paintball Killer', 'paintball'),
            ('paintball_expert', 'Weekly Quest: Paintball Expert', 'paintball'),
            ('blitz_game_of_the_day', 'Daily Quest: Game of the Day', 'hungergames'),
            ('blitz_win', 'Daily Quest: Win Normal', 'hungergames'),
            ('blitz_loot_chest_daily', 'Daily Quest: Chest Looter', 'hungergames'),
            ('blitz_kills', 'Daily Quest: Kills', 'hungergames'),
            ('blitz_weekly_master', 'Weekly Quest: Blitz Master', 'hungergames'),
            ('blitz_loot_chest_weekly', 'Weekly Quest: Blitz Expert', 'hungergames'),
            ('tnt_daily_win', 'Daily Quest: TNT Winner', 'tntgames'),
            ('tnt_weekly_play', 'Weekly Quest: Explosive Fanatic', 'tntgames'),
            ('tnt_tntrun_daily', 'Daily Quest: TNT Run', 'tntgames'),
            ('tnt_tntrun_weekly', 'Weekly Quest: TNT Run', 'tntgames'),
            ('tnt_pvprun_daily', 'Daily Quest: PVP Run', 'tntgames'),
            ('tnt_pvprun_weekly', 'Weekly Quest: PVP Run', 'tntgames'),
            ('tnt_bowspleef_daily', 'Daily Quest: Bow Spleef', 'tntgames'),
            ('tnt_bowspleef_weekly', 'Weekly Quest: Bow Spleef', 'tntgames'),
            ('tnt_tnttag_daily', 'Daily Quest: TNT Tag', 'tntgames'),
            ('tnt_tnttag_weekly', 'Weekly Quest: TNT Tag', 'tntgames'),
            ('tnt_wizards_daily', 'Daily Quest: TNT Wizards', 'tntgames'),
            ('tnt_wizards_weekly', 'Weekly Quest: TNT Wizards', 'tntgames'),
            ('vampirez_daily_play', 'Daily Quest: VampireZ', 'vampirez'),
            ('vampirez_daily_kill', 'Daily Quest: Blood Drinker', 'vampirez'),
            ('vampirez_daily_human_kill', 'Daily Quest: Human Killer', 'vampirez'),
            ('vampirez_daily_win', 'Daily Quest: VampireZ Daily Win', 'vampirez'),
            ('vampirez_weekly_win', 'Weekly Quest: Vampire Winner', 'vampirez'),
            ('vampirez_weekly_kill', 'Weekly Quest: Vampire Slayer', 'vampirez'),
            ('vampirez_weekly_human_kill', 'Weekly Quest: Human Slayer', 'vampirez'),
            ('mega_walls_play', 'Daily Quest: Game of the Day', 'walls3'),
            ('mega_walls_win', 'Daily Quest: Win', 'walls3'),
            ('mega_walls_kill', 'Daily Quest: Kills', 'walls3'),
            ('mega_walls_weekly', 'Weekly Quest: Mega Waller', 'walls3'),
            ('mega_walls_faithful', 'Mythic Quest: Faithful', 'walls3'),
            ('arcade_gamer', 'Daily Quest: Arcade Gamer', 'arcade'),
            ('arcade_winner', 'Daily Quest: Arcade Winner', 'arcade'),
            ('arcade_specialist', 'Weekly Quest: Arcade Specialist', 'arcade'),
            ('arena_daily_play', 'Daily Quest: Play Arena', 'arena'),
            ('arena_daily_kills', 'Daily Quest: Arena Kills', 'arena'),
            ('arena_daily_wins', 'Daily Quest: Arena Wins', 'arena'),
            ('arena_weekly_play', 'Weekly Quest: Play Arena', 'arena'),
            ('uhc_team', 'Daily Quest: Team UHC Champions', 'uhc'),
            ('uhc_solo', 'Daily Quest: Solo UHC Champions', 'uhc'),
            ('uhc_dm', 'Daily Quest: UHC Deathmatch', 'uhc'),
            ('uhc_weekly', 'Weekly Quest: UHC Champions', 'uhc'),
            ('solo_brawler', 'Daily Quest: Solo Speed Brawler', 'uhc'),
            ('team_brawler', 'Daily Quest: Team Speed Brawler', 'uhc'),
            ('uhc_madness', 'Weekly Quest: SpeedUHC Madness', 'uhc'),
            ('cvc_win_daily_normal', 'Daily Quest: Win a game! (Defusal)', 'mcgo'),
            ('cvc_kill_daily_normal', 'Daily Quest: Kill 15 players! (Defusal)', 'mcgo'),
            ('cvc_kill', 'Daily Quest: Get 300 points! (Deathmatch)', 'mcgo'),
            ('cvc_win_daily_deathmatch', 'Daily Quest: Win a game! (Deathmatch)', 'mcgo'),
            ('cvc_kill_weekly', 'Weekly Quest: 100 kills and 1,500 points', 'mcgo'),
            ('warlords_ctf', 'Daily Quest: Capture the Flag', 'battleground'),
            ('warlords_tdm', 'Daily Quest: Team Deathmatch', 'battleground'),
            ('warlords_domination', 'Daily Quest: Domination', 'battleground'),
            ('warlords_victorious', 'Daily Quest: Victorious', 'battleground'),
            ('warlords_objectives', 'Daily Quest: Carry, Secured!', 'battleground'),
            ('warlords_dedication', 'Weekly Quest: Dedication', 'battleground'),
            ('warlords_all_star', 'Weekly Quest: All Star', 'battleground'),
            ('supersmash_solo_win', 'Daily Quest: Smash Heroes Solo Win', 'supersmash'),
            ('supersmash_solo_kills', 'Daily Quest: Smash Heroes Solo Kills', 'supersmash'),
            ('supersmash_team_win', 'Daily Quest: Smash Heroes Team Win', 'supersmash'),
            ('supersmash_team_kills', 'Daily Quest: Smash Heroes Team Kills', 'supersmash'),
            ('supersmash_weekly_kills', 'Weekly Quest: Smash Heroes Weekly Kills', 'supersmash'),
            ('gingerbread_bling_bling', 'Daily Quest: Bling Bling', 'gingerbread'),
            ('gingerbread_maps', 'Daily Quest: International Championship', 'gingerbread'),
            ('gingerbread_racer', 'Daily Quest: Racer', 'gingerbread'),
            ('gingerbread_mastery', 'Weekly Quest: Turbo Kart Racers', 'gingerbread'),
            ('skywars_solo_win', 'Daily Quest: Skywars Solo Win', 'skywars'),
            ('skywars_solo_kills', 'Daily Quest: Skywars Solo Kills', 'skywars'),
            ('skywars_team_win', 'Daily Quest: Skywars Doubles Win', 'skywars'),
            ('skywars_team_kills', 'Daily Quest: Skywars Doubles Kills', 'skywars'),
            ('skywars_arcade_win', 'Daily Quest: Skywars Lab Win', 'skywars'),
            ('skywars_corrupt_win', 'Daily Quest: Skywars Corrupted Win', 'skywars'),
            ('skywars_weekly_kills', 'Weekly Quest: Skywars Weekly Kills', 'skywars'),
            ('skywars_weekly_arcade_win_all', 'Weekly Quest: Skywars Scientist', 'skywars'),
            ('skywars_daily_tokens', 'Daily Quest: Tokens!', 'skywars'),
            ('skywars_weekly_free_loot_chest', 'Weekly Quest: Free Loot Chest', 'skywars'),
            ('skywars_halloween_harvest_2020', 'Special Quest: Harvest Season', 'skywars'),
            ('crazy_walls_daily_play', 'Daily Quest: Crazy Games', 'truecombat'),
            ('crazy_walls_daily_kill', 'Daily Quest: Kills', 'truecombat'),
            ('crazy_walls_daily_win', 'Daily Quest: Win', 'truecombat'),
            ('crazy_walls_weekly', 'Weekly Quest: Crazy Walls Weekly', 'truecombat'),
            ('skyclash_play_games', 'Daily Quest: SkyClash Playtime', 'skyclash'),
            ('skyclash_kills', 'Daily Quest: SkyClash Kills', 'skyclash'),
            ('skyclash_play_points', 'Daily Quest: SkyClash Play Points', 'skyclash'),
            ('skyclash_void', 'Daily Quest: SkyClash Void', 'skyclash'),
            ('skyclash_weekly_kills', 'Weekly Quest: SkyClash Weekly Kills', 'skyclash'),
            ('prototype_pit_daily_kills', 'Daily Quest: Hunter', 'prototype'),
            ('prototype_pit_daily_contract', 'Daily Quest: Contracted', 'prototype'),
            ('prototype_pit_weekly_gold', 'Weekly Quest: Double Up', 'prototype'),
            ('bedwars_daily_win', 'Daily Quest: First Win of the Day', 'bedwars'),
            ('bedwars_daily_one_more', 'Daily Quest: One More Game!', 'bedwars'),
            ('bedwars_weekly_bed_elims', 'Weekly: Bed Removal Co.', 'bedwars'),
            ('bedwars_weekly_dream_win', 'Weekly Quest: Sleep Tight.', 'bedwars'),
            ('bedwars_daily_nightmares', 'Special Daily: Nightmares', 'bedwars'),
            ('bedwars_weekly_pumpkinator', 'Special Weekly: Pumpkinator', 'bedwars'),
            ('mm_daily_win', 'Daily Quest: Winner', 'murdermystery'),
            ('mm_daily_power_play', 'Daily Quest: Power Play', 'murdermystery'),
            ('mm_daily_target_kill', 'Daily Quest: Hitman', 'murdermystery'),
            ('mm_weekly_murderer_kills', 'Weekly Quest: Professional', 'murdermystery'),
            ('mm_weekly_wins', 'Weekly Quest: Big Winner', 'murdermystery'),
            ('mm_special_weekly_killer_instinct_2020', 'Special Quest: Killer Instinct', 'murdermystery'),
            ('build_battle_player', 'Daily Quest: Build Battle Player', 'buildbattle'),
            ('build_battle_winner', 'Daily Quest: Build Battle Winner', 'buildbattle'),
            ('build_battle_weekly', 'Weekly Quest: Master Architect', 'buildbattle'),
            ('build_battle_halloween', 'Special Daily: Hyper', 'buildbattle'),
            ('duels_player', 'Daily Quest: Duels Player', 'duels'),
            ('duels_killer', 'Daily Quest: Duels Killer', 'duels'),
            ('duels_winner', 'Daily Quest: Duels Winner', 'duels'),
            ('duels_weekly_kills', 'Weekly Quest: Duels Weekly Kills', 'duels'),
            ('duels_weekly_wins', 'Weekly Quest: Duels Weekly Wins', 'duels'),
        )

        v = tuple((i.id, i.name, i.game) for i in c.quests)

        self.assertTrue(v == d, 'Unexpected Quests list')

    def test_skyblock_collections(self):

        c = self.api.resources.skyblock.collections

        self.assertTrue(c.version == '0.9.102', 'Unexpected Skyblock version')

        self.assertTrue(c.last_update == datetime(2020, 10, 23, 8, 55, 58, 805000),
                        'Unexpected last update')

        d = ('FARMING', 'MINING', 'COMBAT', 'FORAGING', 'FISHING')

        self.assertTrue(tuple(c.collections.keys()) == d, 'Unexpected collection keys')

        self.assertTrue(len(c.collections.values()) == 5,
                        'Unexpected number of collection values')

    def test_skyblock_skills(self):

        c = self.api.resources.skyblock.skills

        self.assertTrue(c.version == '0.9.102', 'Unexpected Skyblock version')

        self.assertTrue(c.last_update == datetime(2020, 10, 23, 8, 55, 58, 825000),
                        'Unexpected last update')

        d = ('FARMING', 'MINING', 'COMBAT',
             'DUNGEONEERING', 'FORAGING', 'FISHING',
             'ENCHANTING', 'ALCHEMY', 'CARPENTRY',
             'RUNECRAFTING', 'TAMING')

        self.assertTrue(tuple(c.skills.keys()) == d, 'Unexpected skills keys')
