import unittest
from process_data import LEC, Match
from data import matches

class Test_LEC(unittest.TestCase):
    def setUp(self):
        match_list = []
        for match in matches:
            match_list.append(Match(match[0], match[1], match[2]))
        self.lec = LEC(match_list)

    def test_create_standings(self):
        self.lec.create_standings()
        self.assertIn('xl', self.lec.standings[1])
        self.assertIn('vit', self.lec.standings[1])
        self.assertIn('s04', self.lec.standings[1])
        self.assertIn('rge', self.lec.standings[1])
        self.assertIn('mad', self.lec.standings[1])
        self.assertIn('sk', self.lec.standings[6])
        self.assertIn('og', self.lec.standings[6])
        self.assertIn('g2', self.lec.standings[6])
        self.assertIn('msf', self.lec.standings[6])
        self.assertIn('fnc', self.lec.standings[6])

    def test_create_table(self):
        self.lec.create_table()
        self.assertEqual(self.lec.table['xl']['wins'], 1)
        self.assertEqual(self.lec.table['vit']['wins'], 1)
        self.assertEqual(self.lec.table['s04']['wins'], 1)
        self.assertEqual(self.lec.table['rge']['wins'], 1)
        self.assertEqual(self.lec.table['mad']['wins'], 1)