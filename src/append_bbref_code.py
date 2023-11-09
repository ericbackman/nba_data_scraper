import pandas as pd
import bs4
from util.player_logs_helper import get_webpage_html


def name_to_code(row):
    first = row['first_name']
    last = row['last_name']
    if type(last) == float:
        return f"h/hilarne01"
    if len(last) >= 5:
        return "{}/{}{}01".format(last[:1], last[:5], first[:2]).lower()
    else:
        return "{}/{}{}01".format(last[:1], last, first[:2]).lower()


if __name__ == "__main__":

    # Goal of this is to properly populate all bbref codes, by end each row should have a unique bbref code

    df = pd.read_csv('~/github/nba_data_scraper/src/raw_data/nba_players_list.csv')  # Read in names of players
    df.loc[:, 'bbref'] = df.apply(name_to_code, axis=1)  # First pass, leads to duplicates

    value_counts = df.bbref.value_counts()  # Get all value counts
    duplicate_ids = value_counts[value_counts > 1].index.tolist()  # get all ids that show multiple times

    print(f"There are {len(duplicate_ids)} to correct, stage 1")

    # Stage 1, fix duplicate ID's that have unique names
    for idx, id in enumerate(duplicate_ids):  # Iterate all over bbref codes that show in multiple rows
        temp = df[df['bbref'] == id].copy()  # create a temp copy with just the rows for given id
        last = temp.head(1)['last_name'].item()  # get common last name
        url = f"https://www.basketball-reference.com/players/{last[0].lower()}/"
        html = get_webpage_html(url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        player_strings = soup.select('a[href^="/players/"]')
        for index, row in temp.iterrows():  # iterate over players with identical bbref codes
            full = f"{row['first_name']} {row['last_name']}"
            out = soup.select('a[href^="/players/"]')
            result = list(filter(lambda x: full in x, out))
            if len(result) == 1:  # If unique name is using a duplicate ID, we can find and fix
                entry = result[0]
                full_name = str(entry.string)
                first, last = full_name.split(' ', maxsplit=1)
                code = entry['href'].lstrip("/players/").rstrip(".html")
                df.loc[(df['first_name'] == first) & (df['last_name'] == last), 'bbref'] = code
        print(f"{100*(idx/len(duplicate_ids))}%")

    # Stage 2, fix duplicate ID's that have non-unique names
    dupe_names = pd.read_csv("~/github/nba_data_scraper/src/raw_data/duplicate_names.csv")
    for index, row in dupe_names.iterrows():
        df.loc[(df['first_name'] == row['first_name']) & (df['last_name'] == row['last_name'])
               & (df['From'] == int(row['From'])) & (df['To'] == int(row['To'])), 'bbref'] = row['bbref']

    # Stage 3, Fuck you Tony Mitchell for needing more info, also for some reason Kenyon Martin Jr. == KJ Martin
    df.loc[(df['first_name'] == "Tony") & (df['last_name'] == "Mitchell") & (
            df['college'] == 'Alabama'), 'bbref'] = "m/mitchto03"
    df.loc[(df['first_name'] == "Tony") & (df['last_name'] == "Mitchell") & (
            df['college'] == 'University of North Texas'), 'bbref'] = "m/mitchto02"
    df.loc[(df['first_name'] == "Kenyon") & (df['last_name'] == "Martin Jr."), 'first_name'] = "KJ"
    df.loc[(df['first_name'] == "KJ") & (df['last_name'] == "Martin Jr."), 'last_name'] = "Martin"

    # Write output file so we have a unique mapping of player names -> bbref codes + seasons active
    df.to_csv("~/github/nba_data_scraper/src/raw_data/nba_player_codes.csv", index=False)
