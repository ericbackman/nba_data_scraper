import time
import random
import bs4
import pandas as pd
from util.selenium_helper import get_webpage_html


def make_df_row(text, bbref):
    if "*" in text:
        text.pop(1)
        hof = True
    else:
        hof = False

    if len(text) == 7:
        college = None
    elif len(text) == 10:
        college = f"{text[7]}, {text[9]}"
    elif len(text) == 9:
        college = text[8]
    elif len(text) == 6:
        college = text[5]
        text.insert(5, None)
        text.insert(6, None)
    else:
        college = text[7]

    name = text[0].split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    row = {"first_name": name[0],
           "last_name": name[1],
           "From": text[1],
           "To": text[2],
           "Position": text[3],
           "Ht": text[4],
           "Wt": text[5],
           "birthdate": text[6],
           "college": college,
           "hall_of_fame": hof,
           "bbref": bbref}
    return row


def soup_to_player_df(soup):
    columns = ["first_name", "last_name", "From", "To", "Position", "Ht", "Wt", "birthdate", "college", "hall_of_fame",
               "bbref"]
    df = pd.DataFrame(columns=columns)

    rows = soup.select('table > tbody > tr')

    for row in rows[1:]:  # omit header row
        cols = row.find_all('td')
        fields = [td.text.strip() for td in cols if td.text.strip()]

        if fields:  # if the row is not empty
            text = row.findAll(string=True)
            link = row.find('a')['href'][9:].rstrip(".html")

            row = make_df_row(text, link)
            df.loc[len(df.index)] = row
    return df


def get_player_years_active(letter):
    url = f"https://www.basketball-reference.com/players/{letter}"
    html = get_webpage_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    df = soup_to_player_df(soup)
    return df



if __name__ == "__main__":

    players_df = pd.DataFrame()

    for i in range(ord('a'), ord('z') + 1):
        print(chr(i))
        if chr(i) == 'x':
            continue
        temp = get_player_years_active(chr(i))
        players_df = pd.concat([players_df, temp])
        random_number = random.randint(1, 3)
        time.sleep(random_number)

    players_df.to_csv('raw_data/nba_player_codes_v2.csv', index=False)



