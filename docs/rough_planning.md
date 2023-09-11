# Rough Planning Document

Goal of this repository is to brush up on coding skills and work on a fun project that touches on a variety of software development skills. 

This will be a learning experience, and will likely lead down some dead end paths, but push through and attempt to match or exceed the NBA upset rate. Currently 32.1% of NBA games result in an upset during the regular season, and 22% upset rate in the NBA finals. Matching or exceeding these values from an ML model would consititute a massive success.

For a given NBA game, feed it combination of recent team data, recent player data and historical player data to create prediction for outcome of game. The majority of the work will be in determining what data we need, and how I will assemble and feed it to the ML model. 

## Rough breakdown of steps required

1. Python Selenium scripts to open and screen scrape historical data from basketball reference (https://www.basketball-reference.com/). Lots of experimentation will be required to determine which data works best, will need to revisit these scripts often so good coding practices to make work repeatable and easy is a priority. 
2. Python code to parse selenium HTML data and extract relevant data into an easy to use format (thinking Pandas dataframe)
3. Take cleaned data and write it to external storage. Most familiar with Google BigQuery or BigTable, but may use AWS to learn new framework. For now assume GCP will be platform of choice
4. Scripts to extract stored data, transform data if necessary for ML models (to be researched, investigate what is current cutting edge in sports/statisctical analysis)
5. Train ML models, google cloud run, google cloud functions, will be chosen later
6. Evalute models, play with data, see if we can get any improvements.


## Selecting Features for our model.

Others who have tackled this problem. Provides a strong starting point to build from.
- https://towardsdatascience.com/predicting-the-outcome-of-nba-games-with-machine-learning-a810bb768f20
2021 article detailing a similar approach, feeding a combination of team statistics, player stats and rolling averages of recent games to create prediction. Does not include pregame lines. 

Would like to include betting pregame lines and other statistics to improve models.


### Current Work

Step 1. use jupyter labs to experiment and pull per game data for a given team. Would like to end up with a series of data frames I can store for a team (toronto raptors for example). End result should be a game number (ID), all relevant stats for the team in game. Off the top of my head, PTS for, PTS against, 3pts made, 3pts attempted, FG made, FG attempted, 