import copy
from abc import ABC, abstractmethod
from typing import List, Dict
from src.app.process_data.match import Match
from src.app.process_data.team import Team

class League(ABC):
    matches_file = 'src/app/files/matches.json'
    output_file = 'src/app/files/output.md'

    def __init__(self, teams: Dict):
        self.teams = teams
        self.table = {}
        self.standings = {}

    def create_standings(self):
        self.create_table()
        team_wins = self.teams_by_wins(self.table.items())
        self.place_teams(team_wins, self.standings)

        self.tiebraker()

    def place_teams(self, team_wins: Dict, output: Dict, next_place:int=1):
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
            
    def teams_by_wins(self, team_wins: Dict) -> Dict:
        wins = {}
        for team, record in team_wins:
            if not wins.get(record):
                wins[record] = []
            wins[record].append(team)

        return wins

    @abstractmethod
    def tiebraker(self):
        raise NotImplementedError

    def set_standing_for_team(self, team: str, standing: int):
        if not self.standings.get(standing):
            self.standings[standing] = []
        self.standings[standing].append(team)

    def reset_standing_for_team(self, team_to_reset: str):
        for standing, teams in self.standings.items():
            if team_to_reset in teams:
                index = self.standings[standing].index(team_to_reset)
                self.standings[standing].pop(index)
                if not self.standings[standing]:
                    del self.standings[standing]
                break

    @classmethod
    def from_matches(cls, matches: List[Match]):
        teams = {}
        for match in matches:
            for team in match.teams:
                if not teams.get(team):
                    teams[team] = Team(team, [match])
                else:
                    teams[team].matches.append(match)
        
        return cls(teams)

class LEC(League):
    matches_file = 'src/app/files/lec_matches.json'
    output_file = 'src/app/files/lec_output.md'
    playoff_teams = 6
    gamepedia_url = 'https://lol.gamepedia.com/LEC/2021_Season/Spring_Season'
    explanation = '''# All LEC regular season scenarios:
    With accounting for the following tiebreaker rules:
    1) by tied standings the team with the favored head-to-head 
    record gets the higher standing
    2) If that doesnt resolve the tie, the team with more wins
    in the 2nd half of the split gets the higher placing.

    If the tiebreaker is after 2) not solved tiebreaker game(s)
    will be played but are not represented here.
    Which leads to an uneven distribution of the places.
    '''

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

class LCS(League):
    matches_file = 'src/app/files/lcs_matches.json'
    output_file = 'src/app/files/lcs_output.md'
    playoff_teams = 6
    gamepedia_url = 'https://lol.gamepedia.com/LCS/2021_Season/Spring_Season'
    explanation = '''# All LCS Playoff scenarios:
    With accounting for the following tiebreaker rule:
    1) by tied standings the team with the favored 
    head-to-head record gets the higher standing (2 and 3 way ties)
    
    In my calculation teams can end up tied in standings 
    (regular season - before tiebreaker games).
    Which leads up to columns that don't sum up to 100.
    '''

    def tiebraker(self):
        # head to head (2 and 3-way ties)
        self.head_to_head()
        # -> tiebraker game(s)

    def head_to_head(self):
        standings = copy.deepcopy(self.standings)
        for standing, teams in standings.items():
            team_wins = []
            tied_teams = len(teams)
            if tied_teams in [3]:
                for i, team in enumerate(teams):
                    teams_copy = copy.copy(teams)
                    teams_copy.pop(i)
                    head_to_head_wins = self.teams[team].get_head_to_head_wins(teams_copy)
                    team_wins.append((team, head_to_head_wins))
                
                team_wins = self.teams_by_wins(team_wins)
                head_to_head_placing = {}
                self.place_teams_lcs(team_wins, head_to_head_placing, tied_teams, next_place=0)
                for placing, teams in head_to_head_placing.items():
                    for team in teams:
                        if placing == 0:
                            continue
                        self.reset_standing_for_team(team)
                        self.set_standing_for_team(team, standing + placing)
    
    def place_teams_lcs(self, team_wins: Dict, output: Dict, tied_teams: int, next_place: int = 1):
        next_place = next_place
        for wins, teams in sorted(team_wins.items(), reverse=True):
            place = next_place
            for team in teams:
                if not output.get(place):
                    output[place] = []
                if tied_teams == 3 and wins == 4:
                    output[place].append(team)
                    next_place += 1
                elif tied_teams == 3 and next_place > 0:
                    output[place].append(team)
                elif tied_teams == 3:
                    break
                if tied_teams == 2:
                    output[place].append(team)
                    next_place += 1