import pandas as pd
import bs4
from util.player_logs_helper import get_webpage_html


def player_name_to_bbref_code(first, last):
    try:
        if len(last) >= 5:
            return "{}/{}{}01".format(last[:1], last[:5], first[:2]).lower()
        else:
            return "{}/{}{}01".format(last[:1], last, first[:2]).lower()
    except:
        print(f"Nice try {first} {last}")
        return None


if __name__ == "__main__":

    nba_players = pd.read_csv('~/github/nba_data_scraper/src/raw_data/nba_players_list.csv')
    nba_players['bbref'] = ""
    i = 0
    total = nba_players.shape[0]
    print(total)
    for index, row in nba_players.iterrows():
        first = row['first_name']
        last = row['last_name']
        season = int(row['From'])
        i += 1
        try:
            player_code = player_name_to_bbref_code(first, last)
            url = f"https://www.basketball-reference.com/players/{player_code}/gamelog/{season}"
            html = get_webpage_html(url)
            soup = bs4.BeautifulSoup(html, 'html.parser')
            table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'pgl_basic')
            row['bbref'] = player_code
            print(i, first, last, player_code)
        except ValueError:
            row['bbref'] = None
            print("MISSING!!!", first, last)

    nba_players.to_csv("~/github/nba_data_scraper/src/raw_data/nba_player_codes.csv", index=False)
