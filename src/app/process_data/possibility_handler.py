import itertools
from multiprocessing import Pool, Manager, Queue
from functools import partial
import copy
import time
from typing import List, Dict
from src.app.process_data.league import League
from src.app.process_data.match import Match
from src.app.process_data.team import Team

class PossibilityHandler:
    template_file = 'src/app/files/output_template.txt'
    
    def __init__(self, League: League):
        matches = Match.from_json(League.matches_file)
        self.finished_matches = []
        self.upcomming_matches = []
        self.cumulated_outcomes = {}
        self.League = League
        for match in matches:
            if match.result:
                self.finished_matches.append(match)
            else:
                self.upcomming_matches.append(match)

    def run(self):
        start_time = time.time()

        self.multiprocess_possibilities()

        finish_time = time.time()
        time_delta = finish_time - start_time

        self.create_output(time_delta)

    def multiprocess_possibilities(self):
        possibilities = itertools.product([0, 1], repeat=len(self.upcomming_matches))
        with Manager() as manager:
            q = manager.Queue()
            p = Pool()
            func = partial(self.get_possibilities, q)
            p.map_async(func, possibilities)
            # cumulate results while async multiprocessing them
            self.cumulate_results(q)
            p.close()
            p.join()
        
    def get_possibilities(self, q: Queue, possibility: List):
        prediction = copy.deepcopy(self.upcomming_matches)
        self.get_outcome(prediction, possibility)
        league = self.League.from_matches(self.finished_matches + prediction)
        league.create_standings()
        self.cumulate_outcome(q, league.standings)

        # good position to output possibilities for specific teams e.g.:
        # if lec.standings.get(10):
        #     if 'G2' in lec.standings[10]:
        #         dict_matches = [match.__dict__ for match in prediction]
        #         with open('src/g8_10.json', 'a') as f:
        #             json.dump(dict_matches, f)

    def get_outcome(self, upcomming_matches: List[Match], possibility: List):
        for i, match in enumerate(upcomming_matches):
            if possibility[i] == 1:
                upcomming_matches[i].result = [1, 0]
            elif possibility[i] == 0:
                upcomming_matches[i].result = [0, 1]

    def cumulate_outcome(self, q: Queue, standings: Dict):
        cumulated_results = {}
        for standing, teams in standings.items():
            for team in teams:
                if not cumulated_results.get(team):
                    cumulated_results[team] = {}
                if not cumulated_results[team].get(standing):
                    cumulated_results[team][standing] = 1
                else:
                    cumulated_results[team][standing] += 1
        q.put(cumulated_results)
    
    def cumulate_results(self, q: Queue):
        # give producer some time to start
        time.sleep(3)
        while True:
            if q.empty():
                break
            result = q.get()
            for team, standings in result.items():
                if not self.cumulated_outcomes.get(team):
                    self.cumulated_outcomes[team] = {}
                for standing, amount in standings.items():
                    if not self.cumulated_outcomes[team].get(standing):
                        self.cumulated_outcomes[team][standing] = 0
                    self.cumulated_outcomes[team][standing] += 1

    def create_output(self, process_time: float):
        relative_rows = ''
        absolute_rows = ''
        for team, standings in sorted(self.cumulated_outcomes.items(),
                                        key=self.sort_result,
                                        reverse=True
                                    ):
            relative_row = ''
            absolute_row = ''
            total = sum(standings.values())
            playoff_probab = 0
            for i in range(1, 11):  
                if not standings.get(i):
                    standings[i] = 0
                if i <= self.League.playoff_teams:
                    playoff_probab += standings[i]
                relative_row = f'{relative_row} | {round(standings[i] / total * 100, 2)}'
                absolute_row = f'{absolute_row} | {standings[i]:,}'
            relative_row = f'| {team} {relative_row} | {str(round(playoff_probab / total * 100, 2))} |'
            relative_rows = ''.join([relative_rows, relative_row, '\n'])
            absolute_row = f'| {team} {absolute_row} | {total:,} |'
            absolute_rows = ''.join([absolute_rows, absolute_row, '\n'])

        with open(self.template_file, 'r') as template:
            output_template = template.read()
        
        output = output_template.format(
            explanation=self.League.explanation,
            relative_rows=relative_rows,
            absolute_rows=absolute_rows,
            process_time=round(process_time, 0)
        )

        with open(self.League.output_file, 'a') as f:
            f.write(output)

    @staticmethod
    def sort_result(item):
        for i in range(1, 11):
            if not item[1].get(i):
                item[1][i] = 0
                
        return [item[1][i] for i in range(1, 11)]