import bs4
import pandas as pd
import numpy as np
import time
from src.util.selenium_helper import get_webpage_html
from src.util.util_dicts import home_map, player_games_log_col_order


rate_limited = "We apologize, but you have triggered rate limiting by our cloud service provider."
not_found = "We apologize, but this page could not be found."


def extract_date(dt):  # To create gameID column
    return dt.date().strftime("%Y%m%d")


def get_player_season_games_log(season, code):
    url = f"https://www.basketball-reference.com/players/{code}/gamelog/{season}"
    html = get_webpage_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    try:
        table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'pgl_basic')
        df = pd.read_html(str(table))[0]
    except ValueError:
        print(f"Unable to find {season} for {code}")
        df = None
        if rate_limited in soup.body.findAll(string=rate_limited): # When we hit the rate limited check
            for i in range(1,62):
                print(f"Sleeping {i}")
                time.sleep(60)
        if not_found in soup.body.findAll(string=not_found):
            print("-----------------------------------------------------------------------")
            print(f"404 error for {code} during {season}")
            print("-----------------------------------------------------------------------")
    return df


def get_player_adv_season_games_log(season, code):
    url = f"https://www.basketball-reference.com/players/{code}/gamelog-advanced/{season}"
    html = get_webpage_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    try:
        table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'pgl_advanced')
        df = pd.read_html(str(table))[0]
    except ValueError:
        print(f"Unable to find {season} for {code}")
        df = None
    return df


# Specific for the player game log table
# TODO, investigate try/catch for this in case missing values?
# Specific for the player game log table
# TODO, investigate try/catch for this in case missing values?
def column_type_conversion(df):
    df.loc[:, 'tm_game_num'] = df['tm_game_num'].astype(float)
    df.loc[:, 'p_game_num'] = df['p_game_num'].astype(float)
    df.loc[:, 'home'] = df['home'].astype(bool)
    df.loc[:, 'GS'] = df['GS'].astype(bool)
    df.loc[:, 'FG'] = df['FG'].astype(float)
    df.loc[:, 'FGA'] = df['FGA'].astype(float)
    df.loc[:, 'FG%'] = df['FG%'].astype(float)
    df.loc[:, '3P'] = df['3P'].astype(float)
    df.loc[:, '3PA'] = df['3PA'].astype(float)
    df.loc[:, '3P%'] = df['3P%'].astype(float)
    df.loc[:, 'FT'] = df['FT'].astype(float)
    df.loc[:, 'FTA'] = df['FTA'].astype(float)
    df.loc[:, 'FT%'] = df['FT%'].astype(float)
    df.loc[:, 'ORB'] = df['ORB'].astype(float)
    df.loc[:, 'DRB'] = df['DRB'].astype(float)
    df.loc[:, 'TRB'] = df['TRB'].astype(float)
    df.loc[:, 'AST'] = df['AST'].astype(float)
    df.loc[:, 'STL'] = df['STL'].astype(float)
    df.loc[:, 'BLK'] = df['BLK'].astype(float)
    df.loc[:, 'TOV'] = df['TOV'].astype(float)
    df.loc[:, 'PF'] = df['PF'].astype(float)
    df.loc[:, 'PTS'] = df['PTS'].astype(float)
    df.loc[:, 'GmSc'] = df['GmSc'].astype(float)
    df.loc[:, 'PM'] = df['PM'].astype(float)  # E.G Lebron missing +/- leads to error when parsing
    df.loc[:, 'age_yrs'] = df['age_yrs'].astype(float)
    df.loc[:, 'age_days'] = df['age_days'].astype(float)
    df.loc[:, 'score_diff'] = df['score_diff'].astype(float)
    if type(df.iloc[0]['date']) == str:
        df.loc[:, 'date'] = pd.to_datetime(df['date'], format='mixed')
    return df


# Specific for the player game log table
# TODO, investigate try/catch for this in case missing values?
# Specific for the player game log table
# TODO, investigate try/catch for this in case missing values?
def adv_column_type_conversion(df):
    df.loc[:, 'tm_game_num'] = df['tm_game_num'].astype(float)
    df.loc[:, 'p_game_num'] = df['p_game_num'].astype(float)
    df.loc[:, 'home'] = df['home'].astype(bool)
    df.loc[:, 'GS'] = df['GS'].astype(bool)
    df.loc[:, 'TS%'] = df['TS%'].astype(float)
    df.loc[:, 'eFG%'] = df['eFG%'].astype(float)
    df.loc[:, 'ORB%'] = df['ORB%'].astype(float)
    df.loc[:, 'DRB%'] = df['DRB%'].astype(float)
    df.loc[:, 'TRB%'] = df['TRB%'].astype(float)
    df.loc[:, 'AST%'] = df['AST%'].astype(float)
    df.loc[:, 'STL%'] = df['STL%'].astype(float)
    df.loc[:, 'BLK%'] = df['BLK%'].astype(float)
    df.loc[:, 'TOV%'] = df['TOV%'].astype(float)
    df.loc[:, 'USG%'] = df['USG%'].astype(float)
    df.loc[:, 'ORtg'] = df['ORtg'].astype(float)
    df.loc[:, 'DRtg'] = df['DRtg'].astype(float)
    df.loc[:, 'GmSc'] = df['GmSc'].astype(float)
    df.loc[:, 'BPM'] = df['BPM'].astype(float)
    df.loc[:, 'age_yrs'] = df['age_yrs'].astype(int)
    df.loc[:, 'age_days'] = df['age_days'].astype(int)
    df.loc[:, 'score_diff'] = df['score_diff'].astype(int)
    if type(df.iloc[0]['date']) == str:
        df.loc[:, 'date'] = pd.to_datetime(df['date'], format='mixed')
    return df


def year_correction(df, season):
    if season < 1997:
        df['PM'] = np.nan
    if season < 1980:
        df['3P'] = np.nan
        df['3PA'] = np.nan
        df['3P%'] = np.nan
    if season < 1974:
        df['ORB'] = np.nan
        df['DRB'] = np.nan
        df['STL'] = np.nan
        df['BLK'] = np.nan
    if season < 1978:
        df['TOV'] = np.nan
        df['GmSc'] = np.nan
    return df


def adv_year_correction(df, season):
    if season < 1985:
        df['BPM'] = np.nan
    if season < 1983:
        df['ORB%'] = np.nan
        df['DRB%'] = np.nan
        df['TRB%'] = np.nan
        df['AST%'] = np.nan
        df['ORtg'] = np.nan
        df['DRtg'] = np.nan
    if season < 1980:
        df['eFG%'] = np.nan
    if season < 1978:
        df['GmSc'] = np.nan
        df['TOV%'] = np.nan
        df['USG%'] = np.nan
    if season < 1974:
        df['STL%'] = np.nan
        df['BLK%'] = np.nan
    return df


def clean_player_games_log(df, season):
    df = df[df['G'] != 'G'].copy()  # remove formatting rows
    column_rename = {'Rk': 'tm_game_num', 'G': 'p_game_num', 'Date': 'date', 'Age': 'age', 'Unnamed: 5': 'home',
                     'Unnamed: 7': 'result', '+/-': 'PM'}
    df.rename(columns=column_rename, inplace=True)  # Rename necessary columns

    df = remove_inactive(df)

    if df.shape[0] == 0:
        print("No active games for given season")
        return None

    df.loc[:, 'home'] = df['home'].replace(home_map)  # Map home to a bool column, true = home

    # Split and clean up compound columns
    df[['age_yrs', 'age_days']] = df['age'].str.split('-', expand=True)
    df[['result', 'score_diff']] = df['result'].str.split('(', expand=True)
    df['score_diff'] = df['score_diff'].str.rstrip(')')
    df = df.drop(columns=['age'])

    df = year_correction(df, season)

    df = column_type_conversion(df)  # Convert all columns to required type
    df['gameID'] = df['date'].apply(extract_date) + df["Tm"] + df["Opp"]  # Create gameID column

    df = df[player_games_log_col_order]  # Order because cleaner
    return df


def clean_player_adv_games_log(df, season):
    col_order = ['gameID', 'tm_game_num', 'p_game_num', 'date', 'age_yrs', 'age_days', 'Tm', 'home', 'Opp',
                 'result', 'score_diff', 'GS', 'MP', 'TS%', 'eFG%', 'ORB%', 'DRB%', 'TRB%', 'AST%',
                 'STL%', 'BLK%', 'TOV%', 'USG%', 'ORtg', 'DRtg', 'GmSc', 'BPM']

    df = df[df['G'] != 'G'].copy()  # remove formatting rows
    column_rename = {'Rk': 'tm_game_num', 'G': 'p_game_num', 'Date': 'date', 'Age': 'age', 'Unnamed: 5': 'home',
                     'Unnamed: 7': 'result'}
    df.rename(columns=column_rename, inplace=True)  # Rename necessary columns

    df = remove_inactive(df)


    # NOTE: Will be more of these to drop, e.g. did not dress
    df.loc[:, 'home'] = df['home'].replace(home_map)  # Map home to a bool column, true = home

    # Split compound columns
    df[['age_yrs', 'age_days']] = df['age'].str.split('-', expand=True)
    df[['result', 'score_diff']] = df['result'].str.split('(', expand=True)
    df['score_diff'] = df['score_diff'].str.rstrip(')')

    df = df.drop(columns=['age'])

    df = adv_year_correction(df, season)

    df = adv_column_type_conversion(df)

    df['gameID'] = df['date'].apply(extract_date) + df["Tm"] + df["Opp"]

    df = df[col_order]
    return df


def remove_inactive(df):
    df = df[df['GS'] != 'Inactive'].copy()  # Remove rows where the player was inactive for the game
    df = df[df['GS'] != 'Did Not Dress'].copy()  # Remove rows where player was not active (for player stats research would want to keep, but for ML not needed
    df = df[df['GS'] != 'Did Not Play'].copy()  # Remove rows where player was not active, mutual decision? lol
    df = df[df['GS'] != 'Not With Team'].copy()  # Remove rows where player was not with team?
    df = df[df['GS'] != 'Player Suspended'].copy()  # Remove rows where player was suspended and did not play
    df = df[df['GS'] != 'DNP'].copy()  # Remove rows where player was suspended and did not play
    return df



def merge_gamelogs(df, df_adv):
    df_adv = df_adv.drop(columns=['tm_game_num', 'p_game_num', 'date', 'age_yrs', 'age_days',
                                  'Tm', 'home', 'Opp', 'result', 'score_diff', 'GS', 'MP',
                                  'GmSc'])  # Drop duplicate cols
    merged_df = pd.merge(df, df_adv, on='gameID', how='inner')
    return merged_df


def get_and_merge_all_logs(season, code):
    print(season)
    df = get_player_season_games_log(season, code)
    if df is None:
        return None
    df = clean_player_games_log(df, season)
    if df is None:
        return None
    df_adv = get_player_adv_season_games_log(season, code)
    if df_adv is None:
        return None
    df_adv = clean_player_adv_games_log(df_adv, season)
    return merge_gamelogs(df, df_adv)