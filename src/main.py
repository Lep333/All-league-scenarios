from get_data.get_data import GamepediaScraper
from process_data.possibility_handler import PossibilityHandler
from process_data.league import LEC, LCS

def main():
    League = LEC #League = LCS
    scraper = GamepediaScraper(League.gamepedia_url, League.matches_file)
    scraper.runner()

    handler = PossibilityHandler(League)
    handler.run()

if __name__ == '__main__':
    main()