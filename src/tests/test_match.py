import unittest
from src.app.process_data.match import Match

class TestMatch(unittest.TestCase):
    def test_get_winner_left(self):
        match = Match(['Winner', 'Loser'], 0, [1, 0])
        self.assertEqual(match.get_winner(), 'Winner')

    def test_get_winner_right(self):
        match = Match(['Loser', 'Winner'], 0, [0, 1])
        self.assertEqual(match.get_winner(), 'Winner')

    def test_get_winner_no_result(self):
        match = Match(['Loser', 'Winner'], 0)
        self.assertIsNone(match.get_winner())