from google.oauth2 import service_account
from pandas_gbq import to_gbq
import pandas as pd
import helper_funcs as hf


# Setting up for Google cloud bigquery insert, private project, do not attempt to write
project_id = 'nba-data-playground-401815'
dataset_id = 'nba_raw_data'
table_name = 'team_games_log'

# Service account credentials, will need to create your own + BQ backend
credentials = service_account.Credentials.from_service_account_file(
    '/Users/ericbackman/github/nba_data_scraper/keys/nba-data-playground-401815-d4af34cc8cda.json',
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Import csv to df
df_to_write = pd.read_csv("post2000_games_log.csv")
df_to_write = hf.column_type_conversion(df_to_write)

# Write to csv
to_gbq(
    dataframe=df_to_write,
    destination_table=f'{project_id}.{dataset_id}.{table_name}',
    project_id=project_id,
    if_exists='append',  # 'replace' will replace the table if it already exists
    credentials=credentials
)
print("Completed writing to BQ")