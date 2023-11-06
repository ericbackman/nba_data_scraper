import pandas as pd
from util.player_logs_helper import get_and_merge_all_logs

import logging
import sys
logging.basicConfig(filename='raw_data/logging.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))



# Planning
#
# This file will need to do:
# TODO import post 2000s player csv and create looping logic
# TODO for each player and for each season, pull basic and advanced game stats
# TODO take cleaned df's and merge
# TODO append to larger df, write to CSV, go by last name letter to start? end up with 2


if __name__ == "__main__":
    nba_players = pd.read_csv('raw_data/players_active_in_2000s.csv')
    df_master = pd.DataFrame()

    # Rough looping example
    for index, row in nba_players.iterrows():
        first = row['first_name']
        last = row['last_name']
        start_year = int(row['From'])
        end_year = int(row['To'])
        for season in range(start_year, end_year+1):
            print(first, last, season)
            df = get_and_merge_all_logs(first, last, season)
            df_master = pd.concat([df_master, df])





