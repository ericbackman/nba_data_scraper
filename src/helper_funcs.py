import bs4
import pandas as pd
import numpy as np

def get_webpage_html(temp_driver, url):
    temp_driver.get(url)
    html=temp_driver.page_source    
    return html

def getScheduleResultsDF(temp_driver, team, year):
    url = f"https://www.basketball-reference.com/teams/{team}/{year}_games.html"
    html = get_webpage_html(temp_driver, url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag:tag.name=='table' and tag.has_attr('id') and tag['id']=='games')
    df = pd.read_html(str(table))[0]
    return df


def extract_date(dt):
    return dt.date().strftime("%Y%m%d")


def cleanScheduleResultsDF(df, input_team):
    df = df[df['G'] != 'G']  # remove formatting columns/rows
    column_rename = {"G": "gameNum", "Date": "datetime", "Unnamed: 5": "home", "Opponent": "opponent",
                     "Result": "result", "Tm": "ptsf", "Opp": "ptsa", "Unnamed: 7": "result", "W": "wins",
                     "L": "losses", "Streak": "streak"}
    df.rename(columns=column_rename, inplace=True)
    df.loc[:, 'datetime'] = pd.to_datetime(df['datetime'] + " " + df['Start (ET)'], errors='coerce')

    home_map = {np.nan: "home", "@": "away"}
    df.loc[:, 'home'] = df['home'].replace(home_map)

    labels = ['Start (ET)', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 8', 'Notes']
    df.drop(columns=labels, inplace=True)  # Remove useless columns

    # Convert columns into desired data type
    df.loc[:, 'gameNum'] = df['gameNum'].astype(int)
    df.loc[:, 'home'] = df['home'].astype(int)
    df.loc[:, 'ptsf'] = df['ptsf'].astype(int)
    df.loc[:, 'ptsa'] = df['ptsa'].astype(int)
    df.loc[:, 'wins'] = df['wins'].astype(int)
    df.loc[:, 'losses'] = df['losses'].astype(int)
    df.loc[:, 'team'] = input_team
    df.set_index("gameNum", inplace=True)

    # Convert team names to team codes
    df.loc[:, "opponent"] = df['opponent'].replace(nba_teams)
    df.loc[:, "team"] = df['team'].replace(nba_teams)
    df['gameID'] = df['datetime'].apply(extract_date) + df["team"] + df["opponent"]

    return df