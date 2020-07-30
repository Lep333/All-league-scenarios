import itertools
import copy
from typing import List
from src.process_data import Match, League

def main():
    #lec_gamepedia_url = 'https://lol.gamepedia.com/LEC/2020_Season/Summer_Season'
    matches = Match.from_json('src/matches.json')
    finished_matches = []
    upcomming_matches = []
    for match in matches:
        if match.result:
            finished_matches.append(match)
        else:
            upcomming_matches.append(match)
    
    cumulated_outcomes = get_possibilities(upcomming_matches, finished_matches)
    
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
        print(f'Possibility {i} of {total_possibilities}')

    return cumulate_outcomes

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
                cumulated_outcomes[team][standing] = standing
            else:
                cumulated_outcomes[team][standing] += 1

if __name__ == '__main__':
    main()