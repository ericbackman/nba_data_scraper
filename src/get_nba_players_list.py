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


def clean_players_table_post_2000(df):
    df = df[df['From'] != 'From']
    cols_to_drop = ['Colleges', 'Birth Date', 'Wt', 'Ht', 'Pos']
    df = df.drop(columns=cols_to_drop)
    df[['first_name', 'last_name']] = df['Player'].str.split(' ', n=1, expand=True)
    df['last_name'] = df['last_name'].str.rstrip('*')
    df['From'] = df['From'].astype(int)
    df['To'] = df['To'].astype(int)
    df = df[['first_name', 'last_name', 'From', 'To']]
    return df


def clean_players_table_all(df):
    df = df[df['From'] != 'From'].copy()
    cols_to_rename = {'Birth Date': 'birth_date', 'Colleges': 'college'}
    df.rename(columns=cols_to_rename, inplace=True)
    df[['first_name', 'last_name']] = df['Player'].str.split(' ', n=1, expand=True)
    df['hall_of_fame'] = df['last_name'].str.endswith('*')  # Keep track of hall of fame as a bool column
    df['last_name'] = df['last_name'].str.rstrip('*')
    df['From'] = df['From'].astype(int)
    df['To'] = df['To'].astype(int)
    df['Wt'] = df['Wt'].astype(float)
    if type(df.birth_date[1]) == str:
        df.loc[:, 'birth_date'] = pd.to_datetime(df['birth_date'], format='mixed')
    df = df[['first_name', 'last_name', 'From', 'To', 'Pos', 'Ht', 'Wt', 'birth_date', 'college', 'hall_of_fame']]
    return df


if __name__ == "__main__":

    players_df = pd.DataFrame()
    for i in range(ord('a'), ord('z') + 1):
        print(chr(i))
        if chr(i) == 'x':
            continue
        temp = get_player_years_active(chr(i))
        players_df = pd.concat([players_df, temp])
        num = random.randint(1, 3)  # Otherwise might get lockout from basketball ref for bot, keeps under req limit
        print(f"sleeping {num}")
        time.sleep(num)

    players_df_2000 = clean_players_table_post_2000(players_df)
    players_df_2000 = players_df_2000[(players_df_2000['From'] > 2000) | (players_df_2000['To'] > 2000)]
    players_df_all = clean_players_table_all(players_df)

    players_df_2000.to_csv('raw_data/players_active_in_2000s.csv')
    players_df_all.to_csv('raw_data/nba_players_list.csv')


