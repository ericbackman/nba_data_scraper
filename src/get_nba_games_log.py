from src.util.create_team_log_df import create_team_log_df

# Get and compile nba games log dataframe
master_df = create_team_log_df()

print("Attempting write to CSV")
master_df.to_csv('raw_data/post2000_games_log.csv', index=False)
print("Wrote to CSV")
