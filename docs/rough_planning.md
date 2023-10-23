# Rough Planning Document

Goal of this repository is to brush up on coding skills and work on a fun project that touches on a variety of software development skills. 

This will be a learning experience, and will likely lead down some dead end paths, but push through and attempt to match or exceed the NBA upset rate. Currently 32.1% of NBA games result in an upset during the regular season, and 22% upset rate in the NBA finals. Matching or exceeding these values from an ML model would consititute a massive success.

For a given NBA game, feed it combination of recent team data, recent player data and historical player data to create prediction for outcome of game. The majority of the work will be in determining what data we need, and how I will assemble and feed it to the ML model. 

## Rough breakdown of steps required

1. Python Selenium scripts to open and screen scrape historical data from basketball reference (https://www.basketball-reference.com/). Lots of experimentation will be required to determine which data works best, will need to revisit these scripts often so good coding practices to make work repeatable and easy is a priority. 
2. Python code to parse selenium HTML data and extract relevant data into an easy to use format (thinking Pandas dataframe)
3. Take cleaned raw data and write it to external storage. Most familiar with Google BigQuery or BigTable, but may use AWS to learn new framework. For now assume GCP will be platform of choice
4. Scripts to extract stored data, transform data if necessary for ML models (to be researched, investigate what is current cutting edge in sports/statisctical analysis)
5. Train ML models, google cloud run, google cloud functions, will be chosen later
6. Evalute models, play with data, see if we can get any improvements.


## Selecting Features for our model.

Others who have tackled this problem. Provides a strong starting point to build from.
- https://towardsdatascience.com/predicting-the-outcome-of-nba-games-with-machine-learning-a810bb768f20
2021 article detailing a similar approach, feeding a combination of team statistics, player stats and rolling averages of recent games to create prediction. Does not include pregame lines. 

Would like to include betting pregame lines and other statistics to improve models.


### Current Work

Step 1. use jupyter labs to experiment and pull per game data for a given team. Would like to end up with a series of data frames I can store for a team (toronto raptors for example). End result should be a game number (ID), all relevant stats for the team in game. Off the top of my head, PTS for, PTS against, 3pts made, 3pts attempted, FG made, FG attempted.

### Oct 4th Thinking

First type of predictions i want to tackle is game outcome, for a given game, feed in relevant statistics to create guess.
Stats required (first draft):
- team stats for previous season
- team stats for current season
- rolling avg of last 3, 5, 7, 10 games
- player stats for each team (roster is 15 deep, rarely go deeper than 12?)

Based on this draft, will need a raw stats storage that includes:
- Team standings for all seasons
- Team game logs
- Player aggregate stats
- Player game logs

Need to convert this into a series of data sets and tables. Gives rough framework for what data i need to scrape.
Functions to needed for selenium:
- Team aggregate stats from a season (better to get from standings from a given season?)
- Given team and season, pull all boxscores (will give team data and player data)
- Given player name, pull aggregate stats for all seasons

### Oct 23rd thinking

Team logs completed, now need to tackle the more difficult player stats.

To predict a game we need to use player information, this becomes much more difficult because for each game the player averages need to be compiled TO DATE. 
Not useful to input player stats from present day, means we will need some way to either find or calculate player averages prior to each game of the season.
Could be accomplished by compiling player raw game logs, then writing BQ script to append the average stats for each game (thinking this for now)

In terms of todays work, means we will need to start by getting:
- List of all players who have played since 2000
- Using that list of players to pull all game logs for each player

Projected Rough schema:
- Player name, first name, last name (complicated with name changes e.g. ron artest)
- gameID, would like to match gameID used in team table
- all counting stats

First lets work on pulling this raw game log into a single table, will likely need to also spend some time making some
supporting linking tables (e.g. team name -> team code)



