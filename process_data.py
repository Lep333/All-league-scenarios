from typing import List

class Match:
    def __init__(self, teams: List[str], week: int, winner: str = None):
        self.teams = teams
        self.week = week
        self.winner = winner
    
class LEC:
    def __init__(self, matches: List[Match]):
        self.matches = matches

    def create_standings(self):
        self.create_table()
        team_wins = self.teams_by_wins()

        self.standings = {}
        next_place = 1
        for wins, teams in sorted(team_wins.items(), reverse=True):
            place = next_place
            for team in teams:
                # TODO: list comprehension
                if not self.standings.get(place):
                    self.standings[place] = []
                self.standings[place].append(team)
                next_place += 1

        # tiebraker:
        # 1) head to head (3+ teams aggregate wins against other teams)
        # 2) wins in second half of the split
        # -> tiebraker game(s)

    def create_table(self):
        self.table = {}
        for match in self.matches:
            if match.winner == None:
                continue
            if not self.table.get(match.teams[0]):
                self.table[match.teams[0]] = { 'wins': 0 }
            if not self.table.get(match.teams[1]):
                self.table[match.teams[1]] = { 'wins': 0 }
            self.table[match.winner]['wins'] = self.cumulate_matches(match.winner)

    def cumulate_matches(self, current_team):
        if self.table.get(current_team, {}).get('wins'):
            return self.table[current_team]['wins'] + 1
        else:
            return 1

    def teams_by_wins(self):
        wins = {}
        for team, record in self.table.items():
            if not record.get('wins'):
                record['wins'] = 0
            if not wins.get(record['wins']):
                wins[record['wins']] = []
            wins[record['wins']].append(team)

        return wins