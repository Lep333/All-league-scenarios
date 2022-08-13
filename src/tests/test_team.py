import unittest
from src.app.process_data.team import Team
from src.app.process_data.match import Match
from src.app.process_data.league import League, LEC

class TestTeam(unittest.TestCase):
    def test_get_wins(self):
        matches = Match.from_json('src/tests/lec_test.json')
        lec = LEC.from_matches(matches)
        rge_wins = lec.teams['RGE'].get_wins()
        g2_wins = lec.teams['G2'].get_wins()
        s04_wins = lec.teams['S04'].get_wins()

        self.assertEqual(rge_wins, 11)
        self.assertEqual(g2_wins, 8)
        self.assertEqual(s04_wins, 5)