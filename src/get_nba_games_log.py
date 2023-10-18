
import pandas as pd

from google.oauth2 import service_account
from pandas_gbq import to_gbq
import warnings

import cleaning_dictionaries
from create_team_log_df import create_team_log_df



# Setting up for google cloud bigquery insert
project_id = 'nba-data-playground-401815'
dataset_id = 'nba_raw_data'
table_name = 'team_games_log'

credentials = service_account.Credentials.from_service_account_file(
    '/Users/ericbackman/github/nba_data_scraper/keys/nba-data-playground-401815-d4af34cc8cda.json',
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)



# Get and compile nba games log dataframe

nba_teams = cleaning_dictionaries.nba_teams_first_season
master_df = create_team_log_df()


# print("Attempting write")
#
# to_gbq(
#     dataframe=master_df,
#     destination_table=f'{project_id}.{dataset_id}.{table_name}',
#     project_id=project_id,
#     if_exists='append',  # 'replace' will replace the table if it already exists
#     credentials=credentials
# )
#
# print("well...?")

