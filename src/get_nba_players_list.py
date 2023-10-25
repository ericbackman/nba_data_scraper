import time
import random
import bs4
import pandas as pd
from util.selenium_helper import get_webpage_html


def get_player_years_active(letter):
    url = f"https://www.basketball-reference.com/players/{letter}"
    html = get_webpage_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'players')
    df = pd.read_html(str(table))[0]
    return df


def clean_players_table(df):
    df = df[df['From'] != 'From']
    cols_to_drop = ['Colleges', 'Birth Date', 'Wt', 'Ht', 'Pos']
    df = df.drop(columns=cols_to_drop)
    df[['first_name', 'last_name']] = df['Player'].str.split(' ', n=1, expand=True)
    df['last_name'] = df['last_name'].str.rstrip('*')
    df['From'] = df['From'].astype(int)
    df['To'] = df['To'].astype(int)
    df = df[['first_name', 'last_name', 'From', 'To']]
    return df


if __name__ == "__main__":
    players_df = pd.DataFrame()
    for i in range(ord('a'), ord('z') + 1):
        print(chr(i))
        if chr(i) == 'x':
            continue
        temp = get_player_years_active(chr(i))
        players_df = pd.concat([players_df, temp])
        num = random.randint(1, 3)  # Otherwise might have basketball ref find out you are a bot
        print(f"sleeping {num}")
        time.sleep(num)

    players_df = clean_players_table(players_df)
    players_df = players_df[(players_df['From'] > 2000) | (players_df['To'] > 2000)]
    players_df.to_csv('players_active_in_2000s.csv')
