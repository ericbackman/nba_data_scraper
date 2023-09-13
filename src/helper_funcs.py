def get_webpage_html(temp_driver, url):
    temp_driver.get(url)
    html=temp_driver.page_source    
    return html

def getScheduleResultsDF(temp_driver, team, year):
    url = f"https://www.basketball-reference.com/teams/{team}/{year}_games.html"
    html = get_webpage_html(temp_driver, url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(lambda tag:tag.name=='table' and tag.has_attr('id') and tag['id']=='games')
    df = pd.read_html(str(table))[0]
    return df

def cleanScheduleResultsDF(df):
    df = df[df['G'] != 'G'] 
    column_rename = {"G": "GameNum", "Date":"datetime", "Unnamed: 5" : "home", "Opponent":"opponent", "Result":"result", "Tm":"ptsf","Opp":"ptsa", "Unnamed: 7" : "Result"}
    df.rename(columns=column_rename, inplace=True)

    df['datetime'] = pd.to_datetime(df['datetime'] +" " +df['Start (ET)'])
    home_away_map = {np.nan : "home", "@" : "away"}
    df['home'] = df['home'].replace(temp)

    labels = ['Start (ET)','Unnamed: 3', 'Unnamed: 4','Unnamed: 8', 'Notes']
    df.drop(columns=labels,inplace=True) #Remove useless columns
    
    df['GameNum'] = df['GameNum'].astype(int)
    df['home'] = df['home'].astype(int)
    df['ptsf'] = df['ptsf'].astype(int)
    df['ptsa'] = df['ptsa'].astype(int)
    df['W'] = df['W'].astype(int)
    df['L'] = df['L'].astype(int)
    df.set_index("GameNum", inplace=True)
    return df