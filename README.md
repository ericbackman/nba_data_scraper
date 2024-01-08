# nba_data_scraper
The purpose of this repository is to create a simple web scraper that can compile publicly available NBA statistics into
csv form so that it can be imported simply into jupyter notebooks or in the cloud on GCP for ML based projects.

This repository is written in Python and uses Selenium to navigate and pull the desired Basketball Reference pages. 
Beautiful soup, pandas and numpy are used to parse the html and clean the data before saving as a series of csv files.

## What can this repository pull?

This repository has scripts that will allow you to collect the following information:
- List of all players that played in the NBA/ABA that have a page on basketball reference
- NBA box scores for all games after the 1999-2000 NBA season (TODO pull all games)
- Pull all player game logs for all games. (i.e for each player, will have 1 row for each game played)

## Getting Started

Once repo is cloned, navigate to directory in terminal and activate virtualenv using following commands

    pip install virtualenv 
    virtualenv venv 
    source venv/bin/activate 
    pip install -r requirements.txt

### Installing Selenium

To use these python scripts you will need to have selenium installed. Go to [Selenium Web Driver Getting Started](
https://www.selenium.dev/documentation/webdriver/getting_started/) to download and install the required web driver.


## Using the Scripts

All scripts are located in the `src` folder. Before running any of them, make sure you create an output folder for the 
csv's titled `raw_data`


### NBA/ABA Players List `src/get_nba_players_list.py`

Run the python script `src/get_nba_players_list.py`. It will take a few minutes to complete. For each player you will 
have a row containing the following information:

| first_name  | last_name | From | To | Position | Ht  | Wt  | birthdate | college | hall_of_fame | bbref | 
|-------------|-----------|------|----|----------|-----|-----|-----------|---------|--------------|-------|


### Player Career Game Logs

This is a larger and much longer script. It will take approximately 24 hours to complete and requires you to have 
already run the `src/get_nba_players_list.py` to generate the NBA players list including their player codes. 

Before running this script, make sure you create an output folder for the csv's titled `raw_data/player_career_game_logs`

Run the python script `src/get_players_game_log.py` and let it go. If it misses some on the first run due to bbref 
lockouts just run the script an additional time. It will check the output file and only search for missing players.

It will take 24+ hours to complete. For each player you will have a row containing the following information:

| gameID | tm_game_num | p_game_num | date | age_yrs | age_days | Tm  | Opp | home | result | score_diff | GS | MP | FG | FGA | FG% | 3P | 3PA | 3P% | FT | FTA | FT% | ORB | DRB | TRB | AST | STL | BLK | TOV | PF | PTS | GmSc | PM | TS% | eFG% | ORB% | DRB% | TRB% | AST% | STL% | BLK% | TOV% | USG% | ORtg | DRtg | BPM | first_name | last_name |
|--------|-------------|------------|------|---------|----------|-----|-----|------|--------|------------|----|----|----|-----|-----|----|-----|-----|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|----|-----|------|----|-----|------|------|------|------|------|------|------|------|------|------|------|-----|------------|-----------|

More detailed information about each statistic can be found on [Basketball Reference](https://www.basketball-reference.com/)


### NBA Box Scores `src/get_nba_games_log.py`

Run the python script `src/get_nba_games_log.py`. It will take a while to complete. For each game, you will end up with 
a row of the form:






