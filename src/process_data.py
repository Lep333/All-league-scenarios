import json
import copy
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
            if len(match.result) > index:
                if match.result[index] == 1:
                    wins += 1

        return wins
    
    def get_head_to_head_wins(self, other_teams):
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
            if match.week > 4
        ]
        wins = 0
        for match in second_half_matches:
            index = match.teams.index(self.name)
            if match.result[index] == 1:
                wins += 1
        
        return wins

class League:
    def __init__(self, teams: dict, gamepedia_tournament_url: str):
        self.teams = teams
        #self.tiebreaker = tiebreaker
        self.gamepedia_tournament_url = gamepedia_tournament_url
        self.table = {}
        self.standings = {}
    
    def runner(self):
        self.create_standings()

    def create_standings(self):
        self.create_table()
        team_wins = self.teams_by_wins(self.table.items())
        self.place_teams(team_wins, self.standings)

        self.tiebraker()

    def place_teams(self, team_wins, output, next_place=1):
        next_place = next_place
        for wins, teams in sorted(team_wins.items(), reverse=True):
            place = next_place
            for team in teams:
                if not output.get(place):
                    output[place] = []
                output[place].append(team)
                next_place += 1

    def create_table(self):
        for team in self.teams.values():
            self.table[team.name] = team.get_wins()
            
    def teams_by_wins(self, team_wins) -> dict:
        wins = {}
        for team, record in team_wins:
            if not wins.get(record):
                wins[record] = []
            wins[record].append(team)

        return wins

    def tiebraker(self):
        # 1) head to head (3+ teams aggregate wins against other teams)
        self.head_to_head()
        # 2) wins in second half of the split
        self.wins_in_second_half()
        # -> tiebraker game(s)

    def head_to_head(self):
        standings = copy.deepcopy(self.standings)
        for standing, teams in standings.items():
            team_wins = []
            if len(teams) > 1:
                for i, team in enumerate(teams):
                    teams_copy = copy.copy(teams)
                    teams_copy.pop(i)
                    team_wins.append((team, self.teams[team].get_head_to_head_wins(teams_copy)))
                
                team_wins = self.teams_by_wins(team_wins)
                head_to_head_placing = {}
                self.place_teams(team_wins, head_to_head_placing, next_place=0)
                for placing, teams in head_to_head_placing.items():
                    for team in teams:
                        if placing == 0:
                            continue
                        self.reset_standing_for_team(team)
                        self.set_standing_for_team(team, standing + placing)

    def wins_in_second_half(self):
        standings = copy.deepcopy(self.standings)
        for standing, teams in standings.items():
            team_wins = []
            if len(teams) > 1:
                for i, team in enumerate(teams):
                    teams_copy = copy.copy(teams)
                    teams_copy.pop(i)
                    team_wins.append((team, self.teams[team].get_wins_in_second_half()))

                team_wins = self.teams_by_wins(team_wins)
                wins_in_second_half_placing = {}
                self.place_teams(team_wins, wins_in_second_half_placing, next_place=0)
                for placing, teams in wins_in_second_half_placing.items():
                    for team in teams:
                        if placing == 0:
                            continue
                        self.reset_standing_for_team(team)
                        self.set_standing_for_team(team, standing + placing)
        
    def reset_standing_for_team(self, team_to_reset):
        for standing, teams in self.standings.items():
            if team_to_reset in teams:
                index = self.standings[standing].index(team_to_reset)
                self.standings[standing].pop(index)
                if not self.standings[standing]:
                    del self.standings[standing]
                break

    def set_standing_for_team(self, team, standing):
        if not self.standings.get(standing):
            self.standings[standing] = []
        self.standings[standing].append(team)

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