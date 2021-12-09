import pandas as pd
import requests


def save_images(teams):
  base_url = 'https://img1.hscicdn.com/image/upload/f_auto,t_h_100/lsci'
  for team in teams:
    print(team)
    player_info = pd.read_csv(f'Data/Team_to_Player/{team}.csv', usecols=['id', 'image'])
    player_with_image_info = player_info[player_info['image'] != 'False'].to_dict()
    print(player_info.head())
    for id, url in player_with_image_info['image'].items():
      image_data = requests.get(f'{base_url}{url}').content
      with open(f'./public/images/players/{id}.jpg', 'wb') as image_file:
        image_file.write(image_data)
