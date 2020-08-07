import unittest
import json
from src.app.process_data.league import LEC
from src.app.process_data.match import Match
from tests.test_data import matches_one_day, matches_two_days, head_to_head, wins_in_second_half

class TestLeague(unittest.TestCase):
    def test_create_standings_one_day(self):
        test_matches = []
        for match in matches_one_day:
            test_matches.append(Match(match['teams'], match['week'], match['result']))
        lec = LEC.from_matches(test_matches)
        lec.create_standings()
        self.assertIn('XL', lec.standings[1])
        self.assertIn('VIT', lec.standings[1])
        self.assertIn('S04', lec.standings[1])
        self.assertIn('RGE', lec.standings[1])
        self.assertIn('MAD', lec.standings[1])
        self.assertIn('SK', lec.standings[6])
        self.assertIn('OG', lec.standings[6])
        self.assertIn('G2', lec.standings[6])
        self.assertIn('MSF', lec.standings[6])
        self.assertIn('FNC', lec.standings[6])

    def test_create_standings_two_days(self):
        test_matches = []
        for match in matches_two_days:
            test_matches.append(Match(match['teams'], match['week'], match['result']))
        lec = LEC.from_matches(test_matches)
        lec.create_standings()
        self.assertIn('XL', lec.standings[3])
        self.assertIn('VIT', lec.standings[3])
        self.assertIn('S04', lec.standings[7])
        self.assertIn('RGE', lec.standings[1])
        self.assertIn('MAD', lec.standings[1])
        self.assertIn('SK', lec.standings[3])
        self.assertIn('OG', lec.standings[7])
        self.assertIn('G2', lec.standings[9])
        self.assertIn('MSF', lec.standings[9])
        self.assertIn('FNC', lec.standings[3])

    def test_create_standings_season(self):
        matches = Match.from_json('src/tests/lec_test_matches.json')
        lec = LEC.from_matches(matches)
        lec.create_standings()
        self.assertIn('XL', lec.standings[6])
        self.assertIn('VIT', lec.standings[7])
        self.assertIn('S04', lec.standings[10])
        self.assertIn('RGE', lec.standings[2])
        self.assertIn('MAD', lec.standings[1])
        self.assertIn('SK', lec.standings[3])
        self.assertIn('OG', lec.standings[9])
        self.assertIn('G2', lec.standings[4])
        self.assertIn('MSF', lec.standings[8])
        self.assertIn('FNC', lec.standings[5])

    def test_create_table_one_day(self):
        test_matches = []
        for match in matches_one_day:
            test_matches.append(Match(match['teams'], match['week'], match['result']))
        lec = LEC.from_matches(test_matches)
        lec.create_table()
        self.assertEqual(lec.table['XL'], 1)
        self.assertEqual(lec.table['VIT'], 1)
        self.assertEqual(lec.table['S04'], 1)
        self.assertEqual(lec.table['RGE'], 1)
        self.assertEqual(lec.table['MAD'], 1)

    def test_create_table_two_days(self):
        test_matches = []
        for match in matches_two_days:
            test_matches.append(Match(match['teams'], match['week'], match['result']))
        lec = LEC.from_matches(test_matches)
        lec.create_table()
        self.assertEqual(lec.table['RGE'], 2)
        self.assertEqual(lec.table['MAD'], 2)
        self.assertEqual(lec.table['XL'], 1)
        self.assertEqual(lec.table['VIT'], 1)
        self.assertEqual(lec.table['S04'], 1)
        self.assertEqual(lec.table['OG'], 1)
        self.assertEqual(lec.table['FNC'], 1)
        self.assertEqual(lec.table['SK'], 1)

    def test_create_table_season(self):
        matches = Match.from_json('src/tests/lec_test_matches.json')
        lec = LEC.from_matches(matches)
        lec.create_table()
        self.assertEqual(lec.table['RGE'], 11)
        self.assertEqual(lec.table['MAD'], 11)
        self.assertEqual(lec.table['XL'], 7)
        self.assertEqual(lec.table['VIT'], 6)
        self.assertEqual(lec.table['S04'], 5)
        self.assertEqual(lec.table['OG'], 6)
        self.assertEqual(lec.table['FNC'], 7)
        self.assertEqual(lec.table['SK'], 8)
        self.assertEqual(lec.table['G2'], 8)
        self.assertEqual(lec.table['MSF'], 6)

    def test_head_to_head(self):
        test_matches = []
        for match in head_to_head:
            test_matches.append(Match(match['teams'], match['week'], match['result']))
        lec = LEC.from_matches(test_matches)
        lec.create_standings()
        self.assertIn('OG', lec.standings[1])
        self.assertIn('G2', lec.standings[1])
        self.assertIn('FNC', lec.standings[1])

    def test_wins_in_second_half(self):
        test_matches = []
        for match in wins_in_second_half:
            test_matches.append(Match(match['teams'], match['week'], match['result']))
        lec = LEC.from_matches(test_matches)
        lec.create_standings()
        self.assertIn('FNC', lec.standings[1])
        self.assertIn('OG', lec.standings[2])
        self.assertIn('G2', lec.standings[3])