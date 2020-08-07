import unittest
from src.app.get_data.get_data import GamepediaScraper

class TestGetData(unittest.TestCase):
    def test_scraper(self):
        scraper = GamepediaScraper('https://lol.gamepedia.com/LEC/2020_Season/Summer_Season', 'src/matches.json')
        scraper._get_matches()
        g2_mad = [match for match in scraper.matches if match.teams == ['MAD', 'G2']][0]
        self.assertEquals(g2_mad.get_winner(), 'G2')