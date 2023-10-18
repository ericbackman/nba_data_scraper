import numpy as np

nba_teams = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BRK',
    'Charlotte Hornets': 'CHA',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'LA Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHO',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}

nba_teams_first_season = {
    'ATL': {'team': 'Atlanta Hawks', 'first_season': 1949},
    'BOS': {'team': 'Boston Celtics', 'first_season': 1946},
    'BRK': {'team': 'Brooklyn Nets', 'first_season': 1976},
    'CHA': {'team': 'Charlotte Hornets', 'first_season': 1988},
    'CHI': {'team': 'Chicago Bulls', 'first_season': 1966},
    'CLE': {'team': 'Cleveland Cavaliers', 'first_season': 1970},
    'DAL': {'team': 'Dallas Mavericks', 'first_season': 1980},
    'DEN': {'team': 'Denver Nuggets', 'first_season': 1976},
    'DET': {'team': 'Detroit Pistons', 'first_season': 1948},
    'GSW': {'team': 'Golden State Warriors', 'first_season': 1946},
    'HOU': {'team': 'Houston Rockets', 'first_season': 1967},
    'IND': {'team': 'Indiana Pacers', 'first_season': 1967},
    'LAC': {'team': 'LA Clippers', 'first_season': 1970},
    'LAL': {'team': 'Los Angeles Lakers', 'first_season': 1948},
    'MEM': {'team': 'Memphis Grizzlies', 'first_season': 1995},
    'MIA': {'team': 'Miami Heat', 'first_season': 1988},
    'MIL': {'team': 'Milwaukee Bucks', 'first_season': 1968},
    'MIN': {'team': 'Minnesota Timberwolves', 'first_season': 1989},
    'NOP': {'team': 'New Orleans Pelicans', 'first_season': 2002},
    'NYK': {'team': 'New York Knicks', 'first_season': 1946},
    'OKC': {'team': 'Oklahoma City Thunder', 'first_season': 1967},
    'ORL': {'team': 'Orlando Magic', 'first_season': 1989},
    'PHI': {'team': 'Philadelphia 76ers', 'first_season': 1949},
    'PHO': {'team': 'Phoenix Suns', 'first_season': 1968},
    'POR': {'team': 'Portland Trail Blazers', 'first_season': 1970},
    'SAC': {'team': 'Sacramento Kings', 'first_season': 1948},
    'SAS': {'team': 'San Antonio Spurs', 'first_season': 1967},
    'TOR': {'team': 'Toronto Raptors', 'first_season': 1995},
    'UTA': {'team': 'Utah Jazz', 'first_season': 1974},
    'WAS': {'team': 'Washington Wizards', 'first_season': 1961}
}

home_map = {np.nan : 1, "@" : 0}
