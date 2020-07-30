import json
from typing import List
# from src.get_data import GamepediaScraper

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
            if match.result[index] == 1:
                wins += 1

        return wins

class League:
    output_file_name = 'src/matches.json'

    def __init__(self, teams: dict, gamepedia_tournament_url: str):
        self.teams = teams
        #self.tiebreaker = tiebreaker
        self.gamepedia_tournament_url = gamepedia_tournament_url
        self.table = {}
        self.standings = {}
    
    def runner(self):
        # scraper = GamepediaScraper(self.gamepedia_tournament_url, self.output_file_name)
        # scraper.runner()
        self.create_standings()

    def create_standings(self):
        self.create_table()
        team_wins = self.teams_by_wins()

        next_place = 1
        for wins, teams in sorted(team_wins.items(), reverse=True):
            place = next_place
            for team in teams:
                if not self.standings.get(place):
                    self.standings[place] = []
                self.standings[place].append(team)
                next_place += 1

        # tiebraker:
        # 1) head to head (3+ teams aggregate wins against other teams)
        # 2) wins in second half of the split
        # -> tiebraker game(s)

    def create_table(self):
        for team in self.teams.values():
            self.table[team.name] = team.get_wins()
            
    def teams_by_wins(self) -> dict:
        wins = {}
        for team, record in self.table.items():
            if not wins.get(record):
                wins[record] = []
            wins[record].append(team)

        return wins

    @classmethod
    def from_json(cls, gamepedia_tournament_url):
        with open(cls.output_file_name, 'r') as f:
            matches = json.load(f)

        return cls.from_matches(matches, gamepedia_tournament_url)


    @classmethod
    def from_matches(cls, matches: List[Match], gamepedia_tournament_url: str):
        teams = {}
        for match in matches:
            match_obj = Match(match['teams'], match['week'], match['result'])
            for team in match['teams']:
                if not teams.get(team):
                    teams[team] = Team(team, [match_obj])
                else:
                    teams[team].matches.append(match_obj)
        
        return cls(teams, gamepedia_tournament_url)

    @classmethod
    def from_matches_2(cls, matches: List[Match], gamepedia_tournament_url: str):
        teams = {}
        for match in matches:
            for team in match.teams:
                if not teams.get(team):
                    teams[team] = Team(team, [match])
                else:
                    teams[team].matches.append(match)
        
        return cls(teams, gamepedia_tournament_url)