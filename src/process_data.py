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
    
# TODO: create Team class
class Team:
    def __init__(self, name: str, matches: List[Match] = None):
        self.name = name
        self.matches = matches

class LEC:
    def __init__(self, matches: List[Match]):
        self.matches = matches
        self.table = {}
        self.teams = []

    def create_standings(self):
        self.create_table()
        team_wins = self.teams_by_wins()

        self.standings = {}
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
        for match in self.matches:
            if not match.result:
                continue
            if not self.table.get(match.teams[0]):
                self.table[match.teams[0]] = { 'wins': 0 }
            if not self.table.get(match.teams[1]):
                self.table[match.teams[1]] = { 'wins': 0 }
            self.table[match.get_winner()]['wins'] += 1

    def teams_by_wins(self) -> dict:
        wins = {}
        for team, record in self.table.items():
            if not record.get('wins'):
                record['wins'] = 0
            if not wins.get(record['wins']):
                wins[record['wins']] = []
            wins[record['wins']].append(team)

        return wins

    # TODO: factory pattern from json