import bs4
import pandas as pd
import numpy as np
from util_dicts import nba_teams_post_2000, home_map
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import warnings

# Ignore subset copy warnings from pandas
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
# Ignore dateutil warnings when constructing pandas datetime stamps
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

# Options for selenium
options = Options()
options.page_load_strategy = 'eager'  # Faster load so it does not wait for video ads to render
options.add_argument("--headless")  # Run Chrome in headless mode


def team_year_to_df(team, year):
    driver = webdriver.Chrome(options=options)
    df_raw = getScheduleResultsDF(driver, team, str(year))
    driver.close()
    df_clean = cleanScheduleResultsDF(df_raw, team)
    return df_clean


def get_webpage_html(temp_driver, url):
    temp_driver.get(url)
    html = temp_driver.page_source
    return html


def getScheduleResultsDF(temp_driver, team, year):
    url = f"https://www.basketball-reference.com/teams/{team}/{year}_games.html"
    html = get_webpage_html(temp_driver, url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'games')
    df = pd.read_html(str(table))[0]
    return df


def extract_date(dt):
    return dt.date().strftime("%Y%m%d")


def cleanScheduleResultsDF(df, input_team):
    # There is a switch case we need to account for, table is different for years prior to 2001.
    # From 2001 on, the table is different because it includes start time as a column.

    df = df[df['G'] != 'G'].copy()  # remove formatting rows
    column_rename = {"G": "gameNum", "Date": "datetime", "Unnamed: 5": "home", "Opponent": "opponent",
                     "Result": "result", "Tm": "ptsf", "Opp": "ptsa", "Unnamed: 7": "result", "W": "wins",
                     "L": "losses", "Streak": "streak"}
    df.rename(columns=column_rename, inplace=True)
    df.loc[:, 'datetime'] = pd.to_datetime(df['datetime'] + " " + df['Start (ET)'], format='mixed')

    home_away_map = {np.nan: "home", "@": "away"}
    df.loc[:, 'home'] = df['home'].replace(home_map)

    labels = ['Start (ET)', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 8', 'Notes', 'gameNum']
    df.drop(columns=labels, inplace=True)  # Remove useless columns

    # Convert columns into desired data type
    df = column_type_conversion(df)
    df.loc[:, 'team'] = input_team

    # Convert team names to team codes
    df.loc[:, "opponent"] = df['opponent'].replace(nba_teams_post_2000)
    df.loc[:, "team"] = df['team'].replace(nba_teams_post_2000)
    df['gameID'] = df['datetime'].apply(extract_date) + df["team"] + df["opponent"]

    return df


def column_type_conversion(df):
    df.loc[:, 'home'] = df['home'].astype(bool)
    df.loc[:, 'ptsf'] = df['ptsf'].astype(int)
    df.loc[:, 'ptsa'] = df['ptsa'].astype(int)
    df.loc[:, 'wins'] = df['wins'].astype(int)
    df.loc[:, 'losses'] = df['losses'].astype(int)
    if type(df.datetime[1]) == str:
        df.loc[:, 'datetime'] = pd.to_datetime(df['datetime'], format='mixed')
    return df
