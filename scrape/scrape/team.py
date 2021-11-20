import pandas as pd
from bs4 import BeautifulSoup as bs


def get_team_players(team):
  with open(f'Pages/Caps/{team}.html') as page:
    soup = bs(page, 'html.parser')
  table = [player.find_all('div') for player in soup.find_all('div', {'class': 'player-row'})]
  player_info_dict = [{
    'id': row[1].find('a')['href'].split('-')[-1],
    'name': row[1].text.strip('(1234567890)').strip()
  } for row in table]
  return pd.DataFrame(player_info_dict).set_index('id')


def scrape_team_players(teams):
  for team in teams:
    print(team)
    get_team_players(team).to_csv(f'Data/Team_to_Player/{team}.csv')
