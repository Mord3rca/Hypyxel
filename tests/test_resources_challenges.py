import hypyxel
from unittest import TestCase
from datetime import datetime


class ResourcesChallenges(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a = hypyxel.Api(host='http://localhost:8000', key='test-key-ftw')

    def test_challenges(self):
        c = self.a.resources.challenges

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
