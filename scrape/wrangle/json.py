import pandas as pd
import json


def get_json(teams):
  dropdown = []
  teams.append('World')
  for team in teams:
    print(team)
    data = pd.read_csv(f'Data/Team_to_Player/{team}.csv')
    data = pd.DataFrame.to_dict(data, orient='index')
    dropdown += [{
      'value': player['id'],
      'label': player['name'],
      'team': team
    } for player in data.values()]
  with open(f'JSON/Dropdown.json', 'w') as f:
    json.dump(dropdown, f)
