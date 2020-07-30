import unittest
from src.main import main
from src.process_data import Match

class TestMain(unittest.TestCase):
    def test_get_possibilities(self):
        main()