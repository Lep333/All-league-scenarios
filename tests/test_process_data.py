import unittest
import json
from src.process_data import League, Match
from tests.test_data import matches_one_day, matches_two_days

class Test_League(unittest.TestCase):
    def test_create_standings_one_day(self):
        lec = League.from_matches(matches_one_day, '')
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
        lec = League.from_matches(matches_two_days, '')
        lec.create_standings()
        self.assertIn('XL', lec.standings[3])
        self.assertIn('VIT', lec.standings[3])
        self.assertIn('S04', lec.standings[3])
        self.assertIn('RGE', lec.standings[1])
        self.assertIn('MAD', lec.standings[1])
        self.assertIn('SK', lec.standings[3])
        self.assertIn('OG', lec.standings[3])
        self.assertIn('G2', lec.standings[9])
        self.assertIn('MSF', lec.standings[9])
        self.assertIn('FNC', lec.standings[3])

    def test_create_standings_season(self):
        lec = League.from_json('https://lol.gamepedia.com/LEC/2020_Season/Summer_Season')
        lec.create_standings()
        self.assertIn('XL', lec.standings[5])
        self.assertIn('VIT', lec.standings[8])
        self.assertIn('S04', lec.standings[10])
        self.assertIn('RGE', lec.standings[1])
        self.assertIn('MAD', lec.standings[1])
        self.assertIn('SK', lec.standings[3])
        self.assertIn('OG', lec.standings[5])
        self.assertIn('G2', lec.standings[5])
        self.assertIn('MSF', lec.standings[8])
        self.assertIn('FNC', lec.standings[3])

    def test_create_table_one_day(self):
        lec = League.from_matches(matches_one_day, '')
        lec.create_table()
        self.assertEqual(lec.table['XL'], 1)
        self.assertEqual(lec.table['VIT'], 1)
        self.assertEqual(lec.table['S04'], 1)
        self.assertEqual(lec.table['RGE'], 1)
        self.assertEqual(lec.table['MAD'], 1)

    def test_create_table_two_days(self):
        lec = League.from_matches(matches_two_days, '')
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
        lec = League.from_json('https://lol.gamepedia.com/LEC/2020_Season/Summer_Season')
        lec.create_table()
        self.assertEqual(lec.table['RGE'], 10)
        self.assertEqual(lec.table['MAD'], 10)
        self.assertEqual(lec.table['XL'], 6)
        self.assertEqual(lec.table['VIT'], 5)
        self.assertEqual(lec.table['S04'], 3)
        self.assertEqual(lec.table['OG'], 6)
        self.assertEqual(lec.table['FNC'], 7)
        self.assertEqual(lec.table['SK'], 7)

    def test_from_json(self):
        lec = League.from_json('https://lol.gamepedia.com/LEC/2020_Season/Summer_Season')