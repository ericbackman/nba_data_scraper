from src.util import util_dicts
import pandas as pd
from selenium.webdriver.chrome.options import Options
from src.util.game_logs_helper import team_year_to_df

# Options for selenium
options = Options()
options.page_load_strategy = 'eager'  # Faster load, so it does not wait for video ads to render
options.add_argument("--headless")  # Run Chrome in headless mode


# File to loop over teams and years and grab their games log
# This is in its own file/function because there are a lot of specific conditions for team name/code
# These conditions are due to some teams moving (NJ Nets -> Brooklyn Nets), Charlotte Hornets joining in 2004,
# and team code changes (CHA -> CHO on BBref for some reason?), etc
def create_team_log_df():
    nba_teams = util_dicts.nba_teams_post_2000
    master_df = pd.DataFrame()
    for team in nba_teams.values():
        print("-----------------------------Processing {}-----------------------------".format(team))
        if team == "CHA":  # Charlotte bobcats expansion = 2004/05 season so need different first season for them
            for year in range(2005, 2015):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "CHO":  # Charlotte Hornets changed acronym
            for year in range(2015, 2024):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "NJN":  # New Jersey Nets up until 2013
            for year in range(2001, 2013):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "BRK":  # Became Brooklyn Nets in 2013
            for year in range(2013, 2024):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "VAN":  # Vancouver Grizzlies up until 2001
            year = 2001
            df_clean = team_year_to_df(team, year)
            master_df = pd.concat([master_df, df_clean])
            print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "MEM":
            for year in range(2002, 2024):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "NOH":  # New Orleans Hornets for two stints, before and after hurricane Katrina
            for year in range(2003, 2006):  # New orleans officially a team in 2003, previously Charlotte bobcats
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
            for year in range(2008, 2014):  # Back to NOH after brief OKC stint
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "NOK":
            for year in range(2006, 2008):  # Relocated to OKC for 2 years change of code
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "NOP":
            for year in range(2014, 2024):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "SEA":  # Seattle Supersonics up until 2009
            for year in range(2001, 2009):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        elif team == "OKC":  # Moved to OKC in 2009
            for year in range(2009, 2024):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
        else:  # All remaining teams that did not move
            for year in range(2001, 2024):
                df_clean = team_year_to_df(team, year)
                master_df = pd.concat([master_df, df_clean])
                print("-------------------Appended {} + {} -------------------".format(team, year))
    print("Done looping")
    print(master_df.shape)
    return master_df

