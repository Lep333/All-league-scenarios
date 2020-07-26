import unittest
from src.get_data import GamepediaScraper

class Test_Get_Data(unittest.TestCase):
    def test_runner(self):
        scraper = GamepediaScraper()
        scraper.runner()

    def test_scraper(self):
        scraper = GamepediaScraper()
        scraper._get_matches()
        g2_mad = [match for match in scraper.matches if match.teams == ['MAD', 'G2']][0]
        self.assertEquals(g2_mad.get_winner(), 'G2')