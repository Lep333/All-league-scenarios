from get_data import GamepediaScraper
from possibility_handler import PossibilityHandler
from process_data import LEC, LCS

def main():
    League = LCS #League = LEC
    matches_file = 'src/matches.json'
    scraper = GamepediaScraper(League.gamepedia_url, matches_file)
    scraper.runner()

    handler = PossibilityHandler(League)
    handler.run()

if __name__ == '__main__':
    main()