# nba_data_scraper
The purpose of this repository is to create a simple web scraper that can compile publicly available NBA statistics. 

This repository is written in Python and can be considered the first step in a personal project to use ML to 
predict the outcome of NBA games.

## Getting Started

Once repo is cloned, navigate to directory in terminal and activate virtualenv using following commands

    pip install virtualenv 
    virtualenv venv 
    source venv/bin/activate 
    pip install -r requirements.txt

## What can this repository pull?

This repository has scripts that will allow you to collect the following information:
- NBA box scores for all games after the 1999-2000 NBA season
- NBA/ABA players list
- Player career game logs (games post 1984)

## How to use the scripts

Depending on the information you want to pull, their maybe intermediary steps before you will be able to scrape the 
data. For each of the aforementioned use cases, here is how you should approach collecting this information.

### NBA Box Scores

The box scores are the easiest to compile as there are no additional steps needed. You simply need to open and run the 
file `src/get_nba_games_log.py`. Make sure you have given a valid output path to write the CSV at the end, and the util
scripts will handle the rest. For each game, you will end up with a row that looks like the following:
TODO sample row of NBA team game log

### NBA/ABA Players List

Compiling a list of all NBA/ABA players is not difficult, the trouble comes when creating a unique mapping of NBA 
players to basketball reference (bbref) codes (used in the URLs to pull single season game logs). There are a series of scripts 
that need to be create a CSV that uniquely maps player names to bbref codes. 

TODO steps required to pull and clean the player codes

TODO sample row of player to codes mapping

### Player Career Game Logs

This is the largest and most difficult component of this repository. To pull player game logs you must first compile 
the NBA/ABA players list and run the additional cleaning scripts to create the `nba_player_codes.csv` file that is used
as input to this scraper. 

`nba_player_codes.csv` contains a dataframe that has:
- Player name, first and last
- Player first year in league
- Player last year in league
- Height
- Weight
- College (if applicable)
- Hall of fame

To collect player game logs, the real thing we need is 

###








