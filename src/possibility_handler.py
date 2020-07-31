import itertools
from multiprocessing import Pool, Manager, Queue
from functools import partial
import copy
import time
from typing import List
from process_data import Match, League

class PossibilityHandler:
    def __init__(self):
        matches = Match.from_json('src/matches.json')
        self.finished_matches = []
        self.upcomming_matches = []
        self.result = {}
        self.cumulated_outcomes = {}
        for match in matches:
            if match.result:
                self.finished_matches.append(match)
            else:
                self.upcomming_matches.append(match)

    def run(self):
        start_time = time.time()
        possibilities = itertools.product([0, 1], repeat=len(self.upcomming_matches))
        with Manager() as manager:
            q = manager.Queue()
            p = Pool()
            func = partial(self.get_possibilities, q)
            #tut = pool.map(func, possibilities)
            p.map_async(func, possibilities)
            #self.cumulated_outcomes = reduce(self.cumulate_results, result)
            self.cumulate_results(q)
            p.close()
            p.join()
        finish_time = time.time()
        time_delta = finish_time - start_time
        self.create_output('src/output.md', time_delta)
        
    def get_possibilities(self, q, possibility):
        prediction = copy.deepcopy(self.upcomming_matches)
        self.get_outcome(prediction, possibility)
        lec = League.from_matches_2(self.finished_matches + prediction, '')
        lec.create_standings()
        self.cumulate_outcomes(q, lec.standings)

    def get_outcome(self, upcomming_matches: List[Match], possibility):
        for i, match in enumerate(upcomming_matches):
            if possibility[i] == 1:
                upcomming_matches[i].result = [1, 0]
            elif possibility[i] == 0:
                upcomming_matches[i].result = [0, 1]

    def cumulate_outcomes(self, q, standings):
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
    
    def cumulate_results(self, q):
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

    def create_output(self, output_file_name, process_time):
        string  = ''.join(['## Relative: \n', '| Team | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Playoff % | \n',
        '| ---  | --- | --- | --- | --- | ---  | --- | --- | --- | --- | --- | --- | \n'])
        for team, standings in sorted(self.cumulated_outcomes.items(), key=self.sort_result, reverse=True):
            output_string = ''
            total = sum(standings.values())
            playoff_probab = 0
            for i in range(1, 11):  
                if not standings.get(i):
                    standings[i] = 0
                if i <= 6:
                    playoff_probab += standings[i]
                output_string = '| '.join([output_string, str(round(standings[i] / total * 100, 2))])
            output_string = f'| {team} {output_string} | {str(round(playoff_probab / total * 100, 2))} |'
            string = ''.join([string, output_string, '\n'])

        with open(output_file_name, 'a') as f:
            f.write(string)

        string  = ''.join(['\n\n', '## Absolute: \n', '| Team | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Total | \n',
        '| ---  | --- | --- | --- | --- | ---  | --- | --- | --- | --- | --- | --- | \n'])
        for team, standings in sorted(self.cumulated_outcomes.items(), key=self.sort_result, reverse=True):
            output_string = ''
            for i in range(1, 11):  
                if not standings.get(i):
                    standings[i] = 0
                output_string = f'{output_string} | {standings[i]:,}'
            output_string = f'| {team} {output_string} | {sum(standings.values()):,} |'
            string = ''.join([string, output_string, '\n'])
        
        string = ''.join([string, 'Process Time: ', str(round(process_time, 2)), 's'])

        with open(output_file_name, 'a') as f:
            f.write(string)

    @staticmethod
    def sort_result(item):
        for i in range(1, 11):
            if not item[1].get(i):
                item[1][i] = 0
        return (
            item[1][1],
            item[1][2],
            item[1][3],
            item[1][4],
            item[1][5],
            item[1][6],
            item[1][7],
            item[1][8],
            item[1][9],
            item[1][10]
        )