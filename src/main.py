import itertools
import copy
import time
from typing import List
from process_data import Match, League

def main():
    #lec_gamepedia_url = 'https://lol.gamepedia.com/LEC/2020_Season/Summer_Season'
    start_time = time.time()
    matches = Match.from_json('src/matches.json')
    finished_matches = []
    upcomming_matches = []
    for match in matches:
        if match.result:
            finished_matches.append(match)
        else:
            upcomming_matches.append(match)
    
    cumulated_outcomes = get_possibilities(upcomming_matches, finished_matches)
    finish_time = time.time()
    time_delta = finish_time - start_time
    create_output('src/output.md', cumulated_outcomes, time_delta)
    
def get_possibilities(upcomming_matches, finished_matches):
    cumulated_outcomes = {}
    total_possibilities = pow(2, len(upcomming_matches))
    possibilities = itertools.product([0, 1], repeat=len(upcomming_matches))
    for i, possibility in enumerate(possibilities, 1):
        prediction = copy.deepcopy(upcomming_matches)
        get_outcome(prediction, possibility)
        lec = League.from_matches_2(finished_matches + prediction, '')
        lec.create_standings()
        cumulate_outcomes(cumulated_outcomes, lec.standings)

    return cumulated_outcomes

def get_outcome(upcomming_matches: List[Match], possibility, recursive_depth=0):
    if recursive_depth == len(upcomming_matches):
        return upcomming_matches

    if possibility[recursive_depth] == 1:
        upcomming_matches[recursive_depth].result = [1, 0]
    elif possibility[recursive_depth] == 0:
        upcomming_matches[recursive_depth].result = [0, 1]

    get_outcome(
        upcomming_matches,
        possibility,
        recursive_depth=recursive_depth + 1
    )

def cumulate_outcomes(cumulated_outcomes, standings):
    for standing, teams in standings.items():
        for team in teams:
            if not cumulated_outcomes.get(team):
                cumulated_outcomes[team] = {}
            if not cumulated_outcomes[team].get(standing):
                cumulated_outcomes[team][standing] = 1
            else:
                cumulated_outcomes[team][standing] += 1

def create_output(output_file_name, cumulated_outcomes, process_time):
    string  = ''.join(['| Team | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Total | \n',
    '| ---  | --- | --- | --- | --- | ---  | --- | --- | --- | --- | --- | --- | \n'])
    for team, standings in sorted(cumulated_outcomes.items(), key=sort_result, reverse=True):
        output_string = ''
        for i in range(1, 11):  
            if not standings.get(i):
                standings[i] = 0
            output_string = '| '.join([output_string, str(standings[i])])
        output_string = f'| {team} {output_string} | {str(sum(standings.values()))}'
        string = ''.join([string, output_string, '\n'])
    
    string = ''.join([string, 'Process Time: ', str(round(process_time, 2)), 's'])

    with open(output_file_name, 'w') as f:
        f.write(string)

def sort_result(item):
    for i in range(1, 11):
        if not item[1].get(i):
            item[1][i] = 0
    return item[1][1], item[1][2], item[1][3], item[1][4], item[1][5], item[1][6], item[1][7], item[1][8], item[1][9], item[1][10]

if __name__ == '__main__':
    main()