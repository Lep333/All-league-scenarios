from typing import List
from src.app.process_data.match import Match

class Team:
    def __init__(self, name: str, matches: List[Match] = None):
        self.name = name
        self.matches = matches

    def get_wins(self) -> int:
        wins = 0
        for match in self.matches:
            if not match.result:
                continue
            index = match.teams.index(self.name)
            if len(match.result) > index:
                if match.result[index] == 1:
                    wins += 1

        return wins
    
    def get_head_to_head_wins(self, other_teams: List):
        wins = 0
        for other_team in other_teams:
            matchups = [
                        match for match in self.matches
                        if self.name in match.teams and other_team in match.teams
                    ]

            for match in matchups:
                index = match.teams.index(self.name)
                if len(match.result) > index:
                    if match.result[index] == 1:
                        wins += 1
        
        return wins

    def get_wins_in_second_half(self):
        second_half_matches = [
            match for match in self.matches
            if match.week > 4 and match.result # TODO: remove hardcoded week
        ]
        wins = 0
        for match in second_half_matches:
            index = match.teams.index(self.name)
            if match.result[index] == 1:
                wins += 1
        
        return wins