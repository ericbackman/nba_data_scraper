import cleaning_dictionaries
import pandas as pd
import helper_funcs


# File to loop over teams and years and grab their games log
# This is in its own file/function because there are a lot of specific conditions for team name/code
# These conditions are due to some teams moving (NJ Nets -> Brooklyn Nets), Charlotte Hornets joining in 2004,
# and team code changes (CHA -> CHO on BBref for some reason?), etc

def create_team_log_df():
    nba_teams = cleaning_dictionaries.nba_teams_first_season
    master_df = pd.DataFrame()

    for team in nba_teams:
        print("-----------------------------Processing {}-----------------------------".format(team))
        if team == "CHA":  # Charlotte bobcats expansion = 2004/05 season so need different first season for them
            for year in range(2005, 2015):
                df_clean = helper_funcs.team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
            for year in range(2015, 2024):
                df_clean = helper_funcs.team_year_to_df("CHO", year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "BRK":  # Brooklyn moved from NJ in 2012/13
            for year in range(2001, 2013):
                df_clean = helper_funcs.team_year_to_df("NJN", year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format("NJN", year))
            for year in range(2013, 2024):
                df_clean = helper_funcs.team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "MEM":  # Memphis moved from Vancouver in 2002
            year = 2001
            df_clean = helper_funcs.team_year_to_df("VAN", year)
            master_df = pd.concat([master_df, df_clean])
            print("-------------------Appended {} + {} -------------------".format("VAN", year))
            for year in range(2002, 2024):
                df_clean = helper_funcs.team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "NOP":  # New Orleans name change from Hornets to Pelicans in 2014
            for year in range(2003,
                              2006):  # New orleans officially a team in 2003, previously Charlotte bobcats, confusing.
                df_clean = helper_funcs.team_year_to_df("NOH", year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format("NOH", year))
            for year in range(2006, 2008):  # Relocated to OKC for 2 years change of code
                df_clean = helper_funcs.team_year_to_df("NOK", year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format("NOK", year))
            for year in range(2008, 2014):  # Back to NOH until pelicans swap
                df_clean = helper_funcs.team_year_to_df("NOH", year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format("NOH", year))
            for year in range(2014, 2024):
                df_clean = helper_funcs.team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "OKC":  # OKC moved from Seattle in 2009
            for year in range(2001, 2009):
                df_clean = helper_funcs.team_year_to_df("SEA", year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format("SEA", year))
            for year in range(2009, 2024):
                df_clean = helper_funcs.team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        else:
            for year in range(2001, 2024):
                df_clean = helper_funcs.team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
    print("Done looping")
    print(master_df.shape)
    return master_df
