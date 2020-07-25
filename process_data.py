from typing import List

class Match:
    def __init__(self, winner: str, loser: str, week: int):
        self.winner = winner
        self.loser = loser
        self.week = week
    
class LEC:
    def __init__(self, matches: List[Match]):
        self.matches = matches

    def create_standings(self):
        self.create_table()
        wins = self.teams_by_wins()

        self.standings = {}
        next_place = 1
        for wins, teams in wins.items():
            place = next_place
            for team in teams:
                # list comprehension
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
            self.table[match.winner] = { 
                'wins': self.cumulate_matches(match.winner, 'wins'),
            }
            self.table[match.loser] = { 
                'losses': self.cumulate_matches(match.loser, 'losses'),
            }

    def cumulate_matches(self, current_team, win_or_loss):
        try: 
            return self.table[current_team][win_or_loss] + 1
        except:
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