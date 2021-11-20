import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def get_player_matches(player_id):
  url = f'https://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class=1;template=results;type=allround;view=results'
  soup = bs(requests.get(url).content, 'html.parser')
  table = soup.find('div', {'id': 'ciHomeContentlhs'}).find_all('table', {'class': 'engineTable'})[3].find('tbody')
  if table:
    return [row.find_all('td')[-1].find('a')['href'].split('/')[-1][:-5] for row in table.find_all('tr', {'class': 'data1'})]
  return ''


def scrape_player_matches(teams):
  for team in teams:
    print(team)
    player_ids = list(pd.read_csv(f'Data/Team_to_Player/{team}.csv', usecols=['id'])['id'])
    player_matches = [{
      'id': player_id,
      'matches': ','.join(get_player_matches(player_id))
    } for player_id in player_ids]
    player_matches = [player for player in player_matches if player['matches']]
    pd.DataFrame.from_dict(player_matches).to_csv(f'Data/Player_to_Match/{team}.csv')
