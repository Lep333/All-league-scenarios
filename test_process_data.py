import unittest
import json
from process_data import LEC, Match
from test_data import matches_one_day, matches_two_days

class Test_LEC(unittest.TestCase):
    def setUp(self):
        match_list = []
        for match in matches_one_day:
            match_list.append(Match(match[0], match[1], match[2]))
        self.lec = LEC(match_list)

    def test_create_standings_one_day(self):
        self.lec.create_standings()
        self.assertIn('XL', self.lec.standings[1])
        self.assertIn('VIT', self.lec.standings[1])
        self.assertIn('S04', self.lec.standings[1])
        self.assertIn('RGE', self.lec.standings[1])
        self.assertIn('MAD', self.lec.standings[1])
        self.assertIn('SK', self.lec.standings[6])
        self.assertIn('OG', self.lec.standings[6])
        self.assertIn('G2', self.lec.standings[6])
        self.assertIn('MSF', self.lec.standings[6])
        self.assertIn('FNC', self.lec.standings[6])

    def test_create_standings_two_days(self):
        match_list = []
        for match in matches_two_days:
            match_list.append(Match(match[0], match[1], match[2]))
        lec = LEC(match_list)
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
        with open('matches.json', 'r') as f:
            matches = json.load(f)

        match_list = []
        for match in matches:
            match_list.append(Match(match['teams'], match['week'], match['winner']))
        lec = LEC(match_list)
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
        self.lec.create_table()
        self.assertEqual(self.lec.table['XL']['wins'], 1)
        self.assertEqual(self.lec.table['VIT']['wins'], 1)
        self.assertEqual(self.lec.table['S04']['wins'], 1)
        self.assertEqual(self.lec.table['RGE']['wins'], 1)
        self.assertEqual(self.lec.table['MAD']['wins'], 1)

    def test_create_table_two_days(self):
        match_list = []
        for match in matches_two_days:
            match_list.append(Match(match[0], match[1], match[2]))
        lec = LEC(match_list)
        lec.create_table()
        self.assertEqual(lec.table['RGE']['wins'], 2)
        self.assertEqual(lec.table['MAD']['wins'], 2)
        self.assertEqual(lec.table['XL']['wins'], 1)
        self.assertEqual(lec.table['VIT']['wins'], 1)
        self.assertEqual(lec.table['S04']['wins'], 1)
        self.assertEqual(lec.table['OG']['wins'], 1)
        self.assertEqual(lec.table['FNC']['wins'], 1)
        self.assertEqual(lec.table['SK']['wins'], 1)

    def test_create_table_season(self):
        with open('matches.json', 'r') as f:
            matches = json.load(f)

        match_list = []
        for match in matches:
            match_list.append(Match(match['teams'], match['week'], match['winner']))
        lec = LEC(match_list)
        lec.create_table()
        self.assertEqual(lec.table['RGE']['wins'], 10)
        self.assertEqual(lec.table['MAD']['wins'], 10)
        self.assertEqual(lec.table['XL']['wins'], 6)
        self.assertEqual(lec.table['VIT']['wins'], 5)
        self.assertEqual(lec.table['S04']['wins'], 3)
        self.assertEqual(lec.table['OG']['wins'], 6)
        self.assertEqual(lec.table['FNC']['wins'], 7)
        self.assertEqual(lec.table['SK']['wins'], 7)