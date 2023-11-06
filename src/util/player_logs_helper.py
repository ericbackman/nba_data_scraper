import bs4
import pandas as pd
from src.util.selenium_helper import get_webpage_html
from src.util.util_dicts import home_map, player_games_log_col_order
import logging
logging.basicConfig(filename='logging.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')



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
    df.loc[:, 'PM'] = df['PM'].astype(float)  # E.G Lebron missing +/- leads to error when parsing
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
    df = df[df[
                'GS'] != 'Did Not Dress'].copy()  # Remove rows where player was not active (for player stats research would want to keep, but for ML not needed
    df = df[df['GS'] != 'Did Not Play'].copy()  # Remove rows where player was not active, mutual decision? lol
    df = df[df['GS'] != 'Not With Team'].copy()  # Remove rows where player was not with team?

    df.loc[:, 'home'] = df['home'].replace(home_map)  # Map home to a bool column, true = home

    # Split and clean up compound columns
    df[['age_yrs', 'age_days']] = df['age'].str.split('-', expand=True)
    df[['result', 'score_diff']] = df['result'].str.split('(', expand=True)
    df['score_diff'] = df['score_diff'].str.rstrip(')')
    df = df.drop(columns=['age'])

    df = column_type_conversion(df)  # Convert all columns to required type
    df['gameID'] = df['date'].apply(extract_date) + df["Tm"] + df["Opp"]  # Create gameID column

    df = df[player_games_log_col_order]  # Order because cleaner
    return df


# Specific for the player game log table
# TODO, investigate try/catch for this in case missing values?
def adv_column_type_conversion(df):
    df.loc[:, 'tm_game_num'] = df['tm_game_num'].astype(int)
    df.loc[:, 'p_game_num'] = df['p_game_num'].astype(int)
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
    df.loc[:, 'ORtg'] = df['ORtg'].astype(int)
    df.loc[:, 'DRtg'] = df['DRtg'].astype(int)
    df.loc[:, 'GmSc'] = df['GmSc'].astype(float)
    df.loc[:, 'BPM'] = df['BPM'].astype(float)
    df.loc[:, 'age_yrs'] = df['age_yrs'].astype(int)
    df.loc[:, 'age_days'] = df['age_days'].astype(int)
    df.loc[:, 'score_diff'] = df['score_diff'].astype(int)
    if type(df.date[1]) == str:
        df.loc[:, 'date'] = pd.to_datetime(df['date'], format='mixed')
    return df


def get_player_adv_season_games_log(first, last, season):
    player_code = player_name_to_bbref_code(first, last)
    url = f"https://www.basketball-reference.com/players/{player_code}/gamelog-advanced/{season}"
    html = get_webpage_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'pgl_advanced')
    try:
        df = pd.read_html(str(table))[0]
    except ValueError:
        logging.warning(f"No table found for player {first} {last} in {season}")
    finally:
        df = None
    return df


def clean_player_adv_games_log(df):
    col_order = ['gameID', 'tm_game_num', 'p_game_num', 'date', 'age_yrs', 'age_days', 'Tm', 'home', 'Opp',
                 'result', 'score_diff', 'GS', 'MP', 'TS%', 'eFG%', 'ORB%', 'DRB%', 'TRB%', 'AST%',
                 'STL%', 'BLK%', 'TOV%', 'USG%', 'ORtg', 'DRtg', 'GmSc', 'BPM']

    df = df[df['G'] != 'G'].copy()  # remove formatting rows
    column_rename = {'Rk': 'tm_game_num', 'G': 'p_game_num', 'Date': 'date', 'Age': 'age', 'Unnamed: 5': 'home',
                     'Unnamed: 7': 'result'}
    df.rename(columns=column_rename, inplace=True)  # Rename necessary columns

    df = df[df['GS'] != 'Inactive'].copy()  # Remove rows where the player was inactive for the game
    df = df[df['GS'] != 'Did Not Dress'].copy()  # Remove rows where player was not active (for player stats research would want to keep, but for ML not needed
    df = df[df['GS'] != 'Did Not Play'].copy()  # Remove rows where player was not active, mutual decision? lol
    df = df[df['GS'] != 'Not With Team'].copy()  # Remove rows where player was not with team?

    # NOTE: Will be more of these to drop, e.g. did not dress
    df.loc[:, 'home'] = df['home'].replace(home_map)  # Map home to a bool column, true = home

    # Split compound columns
    df[['age_yrs', 'age_days']] = df['age'].str.split('-', expand=True)
    df[['result', 'score_diff']] = df['result'].str.split('(', expand=True)
    df['score_diff'] = df['score_diff'].str.rstrip(')')

    df = df.drop(columns=['age'])

    df = adv_column_type_conversion(df)

    df['gameID'] = df['date'].apply(extract_date) + df["Tm"] + df["Opp"]

    df = df[col_order]
    return df


def merge_gamelogs(df, df_adv):
    df_adv = df_adv.drop(columns=['tm_game_num', 'p_game_num', 'date', 'age_yrs', 'age_days',
                                  'Tm', 'home', 'Opp', 'result', 'score_diff', 'GS', 'MP',
                                  'GmSc'])  # Drop duplicate cols
    merged_df = pd.merge(df, df_adv, on='gameID', how='inner')
    return merged_df


def get_and_merge_all_logs(first, last, season):
    df_adv = get_player_adv_season_games_log(first, last, season)
    if df_adv:
        df_adv = clean_player_adv_games_log(df_adv)
    df = get_player_season_games_log(first, last, season)
    df = clean_player_games_log(df)
    return merge_gamelogs(df, df_adv)

