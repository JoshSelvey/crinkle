import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def add_players(data):
  valid_players = list(data['objects']['debutMatches'].keys())
  return ([{
        'id': person['objectId'],
        'name': person['name'].strip(' (1234567890)'),
        'image': person['image']['url'] if person['image'] else 'false',
        'valid': str(person['id']) in valid_players
    } for person in data['results']])


def get_team_players_new(team):
  team_dict = {
        'England': '1',
        'Australia': '2',
        'South_Africa': '3',
        'West_Indies': '4',
        'New_Zealand': '5',
        'India': '6',
        'Pakistan': '7',
        'Sri_Lanka': '8',
        'Zimbabwe': '9',
        'Bangladesh': '25',
        'Ireland': '29',
        'Afghanistan': '40',
    }

  base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/player/search?mode=BOTH&page='
  end_api_url = f'&records=40&sort=ALPHA_DESC&filterTeamId={team_dict[team]}&filterClassId=1&filterDebut=true&selectDebut=true'
  data = requests.get(f'{base_api_url}1{end_api_url}').json()
  n_players = data['total']
  n_fetch = int((n_players - 1) / 40) + 1
  info = add_players(data)
  for page_n in range(2, n_fetch+1):
    url = f'{base_api_url}{page_n}{end_api_url}'
    data = requests.get(url).json()
    info += add_players(data)
  df = pd.DataFrame(info)
  df['image_path'] = df['id'].mask(df['image'] == 'false', 'default')
  df = df.set_index('id')
  return df[df['valid']][['name', 'image', 'image_path']]

def scrape_team_players(teams):
  for team in teams:
    print(team)
    get_team_players_new(team).to_csv(f'Data/Team_to_Player/{team}.csv')
