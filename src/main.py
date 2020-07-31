from get_data import GamepediaScraper
from possibility_handler import PossibilityHandler

def main():
    url = 'https://lol.gamepedia.com/LEC/2020_Season/Summer_Season'
    matches_file = 'src/matches.json'
    scraper = GamepediaScraper(url, matches_file)
    scraper.runner()

    handler = PossibilityHandler()
    handler.run()

if __name__ == '__main__':
    main()