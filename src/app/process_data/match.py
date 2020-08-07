import json
from typing import List

class Match:
    def __init__(self, teams: List[str], week: int, result: List[int] = None):
        self.teams = teams
        self.week = week
        self.result = result

    def get_winner(self):
        if not self.result:
            return
        if self.result[0]:
            return self.teams[0]
        else:
            return self.teams[1]

    @classmethod
    def from_json(cls, file_name: str):
        with open(file_name, 'r') as f:
            matches = json.load(f)

        matches = [cls(match['teams'], match['week'], match['result']) for match in matches]
        return matches