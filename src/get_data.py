import re
import json
import os
import requests
from bs4 import BeautifulSoup
import src.process_data as process_data

class GamepediaScraper:
    default_beautifulsoup_parser= 'html.parser'

    def __init__(self, lec_gamepedia_url: str, output_file_name: str):
        self.lec_gamepedia_url = lec_gamepedia_url
        self.output_file_name = output_file_name
        self.matches = []

    def runner(self):
        if not os.path.exists(self.output_file_name):
            self._get_matches()
            self._save_matches()

    def _get_matches(self):
        response = requests.get(self.lec_gamepedia_url)
        soup = BeautifulSoup(response.content, self.default_beautifulsoup_parser)

        wiki_tables = soup.find_all('table', class_='wikitable matchlist')
        for wiki_table in wiki_tables:
            week = wiki_table.find('th').get_text()
            week_pattern = re.compile('\d')
            week = week_pattern.findall(week)[0]
            matches_row = wiki_table.find_all('tr', class_='ml-row')
            for match in matches_row:
                teams_html = match.find_all('span', class_='teamname')
                teams = [team.get_text() for team in teams_html]
                result_html = match.find_all('td', class_='matchlist-score')
                result = [int(result.get_text()) for result in result_html]
                self.matches.append(process_data.Match(teams, int(week), result))
    
    def _save_matches(self):
        matches = [match.__dict__ for match in self.matches]
        with open(self.output_file_name, 'w') as f:
            json.dump(matches, f, indent=4, sort_keys=True)