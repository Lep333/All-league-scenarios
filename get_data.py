import re
import json
import os
import requests
from bs4 import BeautifulSoup
from process_data import Match

class GamepediaScraper:
    default_beautifulsoup_parser= 'html.parser'
    lec_gamepedia_url = 'https://lol.gamepedia.com/LEC/2020_Season/Summer_Season'
    output_file_name = 'matches.json'

    def runner(self):
        if not os.path.exists(self.output_file_name):
            self._get_matches()
            self._save_matches()

    def _get_matches(self):
        response = requests.get(self.lec_gamepedia_url)
        soup = BeautifulSoup(response.content, self.default_beautifulsoup_parser)

        self.matches = []
        wiki_tables = soup.find_all('table', class_='wikitable matchlist')
        for wiki_table in wiki_tables:
            week = wiki_table.find('th').get_text()
            p = re.compile('\d')
            week = p.findall(week)[0]
            matches_row = wiki_table.find_all('tr', class_='ml-row')
            for match in matches_row:
                teams = match.find_all('span', class_='teamname')
                teams = [team.get_text() for team in teams]
                print(teams)
                
                results = match.find_all('td', class_='matchlist-score')
                
                result = [result.get_text() for result in results]
                print(result)
                self.matches.append(Match(teams, int(week), self._get_winner(teams, result)))

    def _get_winner(self, teams, results):
        if not results:
            return
        if results[0] == '1':
            return teams[0]
        else:
            return teams[1]

    
    def _save_matches(self):
        matches = [match.__dict__ for match in self.matches]
        with open(self.output_file_name, 'w') as f:
            json.dump(matches, f, indent=4, sort_keys=True)

scraper = GamepediaScraper()
scraper._get_matches()