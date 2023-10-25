import bs4
import pandas as pd
from selenium_helper import get_webpage_html
from src.util.util_dicts import home_map, player_games_log_col_order



def player_name_to_bbref_code(first, last):
    if len(last) >= 5:
        return "{}/{}{}01".format(last[:1], last[:5], first[:2]).lower()
    else:
        return "{}/{}{}01".format(last[:1], last, first[:2]).lower()


def get_player_season_games_log(first, last, season):
    player_code = player_name_to_bbref_code(first, last)
    url = f"https://www.basketball-reference.com/players/{player_code}/gamelog/{season}"
    html = get_webpage_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'pgl_basic')
    df = pd.read_html(str(table))[0]
    return df


# Specific for the player game log table
# TODO, investigate try/catch for this in case missing values?
def column_type_conversion(df):
    df.loc[:, 'tm_game_num'] = df['tm_game_num'].astype(int)
    df.loc[:, 'p_game_num'] = df['p_game_num'].astype(int)
    df.loc[:, 'home'] = df['home'].astype(bool)
    df.loc[:, 'GS'] = df['GS'].astype(bool)
    df.loc[:, 'FG'] = df['FG'].astype(int)
    df.loc[:, 'FGA'] = df['FGA'].astype(int)
    df.loc[:, 'FG%'] = df['FG%'].astype(float)
    df.loc[:, '3P'] = df['3P'].astype(int)
    df.loc[:, '3PA'] = df['3PA'].astype(int)
    df.loc[:, '3P%'] = df['3P%'].astype(float)
    df.loc[:, 'FT'] = df['FT'].astype(int)
    df.loc[:, 'FTA'] = df['FTA'].astype(int)
    df.loc[:, 'FT%'] = df['FT%'].astype(float)
    df.loc[:, 'ORB'] = df['ORB'].astype(int)
    df.loc[:, 'DRB'] = df['DRB'].astype(int)
    df.loc[:, 'TRB'] = df['TRB'].astype(int)
    df.loc[:, 'AST'] = df['AST'].astype(int)
    df.loc[:, 'STL'] = df['STL'].astype(int)
    df.loc[:, 'BLK'] = df['BLK'].astype(int)
    df.loc[:, 'TOV'] = df['TOV'].astype(int)
    df.loc[:, 'PF'] = df['PF'].astype(int)
    df.loc[:, 'PTS'] = df['PTS'].astype(int)
    df.loc[:, 'GmSc'] = df['GmSc'].astype(float)
    df.loc[:, 'PM'] = df['PM'].astype(int) # E.G Lebron missing +/- leads to error when parsing
    df.loc[:, 'age_yrs'] = df['age_yrs'].astype(int)
    df.loc[:, 'age_days'] = df['age_days'].astype(int)
    df.loc[:, 'score_diff'] = df['score_diff'].astype(int)
    if type(df.date[1]) == str:
        df.loc[:, 'date'] = pd.to_datetime(df['date'], format='mixed')
    return df


def extract_date(dt):  # To create gameID column
    return dt.date().strftime("%Y%m%d")


def clean_player_games_log(df):
    df = df[df['G'] != 'G'].copy()  # remove formatting rows
    column_rename = {'Rk': 'tm_game_num', 'G': 'p_game_num', 'Date': 'date', 'Age': 'age', 'Unnamed: 5': 'home',
                     'Unnamed: 7': 'result', '+/-': 'PM'}
    df.rename(columns=column_rename, inplace=True)  # Rename necessary columns

    df = df[df['GS'] != 'Inactive'].copy()  # Remove rows where the player was inactive for the game
    df = df[df['GS'] != 'Did Not Dress'].copy()  # Remove rows where player was not active (for player stats research would want to keep, but for ML not needed
    df = df[df['GS'] != 'Did Not Play'].copy()  # Remove rows where player was not active, mutual decision? lol
    df = df[df['GS'] != 'Not With Team'].copy()  # Remove rows where player was not with team?

    df.loc[:, 'home'] = df['home'].replace(home_map)  # Map home to a bool column, true = home

    # Split and clean up compound columns
    df[['age_yrs', 'age_days']] = df['age'].str.split('-', expand=True)
    df[['result', 'score_diff']] = df['result'].str.split('(', expand=True)
    df['score_diff'] = df['score_diff'].str.rstrip(')')
    df = df.drop(columns=['age'])

    df = column_type_conversion(df) # Convert all columns to required type

    df['gameID'] = df['date'].apply(extract_date) + df["Tm"] + df["Opp"] # Create gameID column

    df = df[player_games_log_col_order] # Order because cleaner
    return df
