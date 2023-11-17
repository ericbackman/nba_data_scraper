import pandas as pd
from util.player_logs_helper import get_and_merge_all_logs

import logging
import sys
import os

logging.basicConfig(filename='raw_data/logging.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Planning
#
# This file will need to do:
# TODO import players who did not play in the 2000s
# TODO add player names to rows, repetitive but needed for searching
# TODO create pre col conversion check to convert np.nan to 0 for int cols

if __name__ == "__main__":
    nba_players = pd.read_csv('raw_data/nba_player_codes_v2.csv')
    total_entries = nba_players.shape[0]

    directory_path = f"{os.getcwd()}/raw_data/player_career_game_logs"
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    # Rough looping example
    for idx, row in nba_players.iterrows():
        first = row['first_name']
        last = row['last_name']
        if first == "Terry" and last == "Cummings":
            print("skipping terry because he missing info")
            continue
        start_year = int(row['From'])
        end_year = int(row['To'])
        filename = f"{first}_{last}_game_logs.csv"
        if filename in files:
            print(f"Skipping {first} {last}. CSV exists")
            continue
        if start_year >= 2000 or end_year >= 2000:
            df_master = pd.DataFrame()
            print(f"Collecting {first} {last}, played {start_year} to {end_year}")
            for season in range(start_year, end_year + 1):
                df = get_and_merge_all_logs(season, row['bbref'])
                df_master = pd.concat([df_master, df])
            if not df_master.empty:
                df_master['first_name'] = first
                df_master['last_name'] = last
                df_master.to_csv(f"{directory_path}/{filename}")
        else:
            print(f"Skipping {first} {last} played from {start_year} to {end_year}")
        print(f"{100*(idx/total_entries)}")