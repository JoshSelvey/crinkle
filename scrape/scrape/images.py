import pandas as pd
import requests


def save_images(teams):
  base_url = 'https://img1.hscicdn.com/image/upload/f_auto,t_h_100/lsci'
  for team in teams:
    print(team)
    player_info = pd.read_csv(f'Data/Team_to_Player/{team}.csv', usecols=['id', 'image'])
    player_with_image_info = player_info[player_info['image'] != 'false'].to_dict('list')
    print(player_info.head())
    for x in range(len(player_with_image_info['id'])):
      image_data = requests.get(f'{base_url}{player_with_image_info["image"][x]}').content
      with open(f'./public/images/players/{player_with_image_info["id"][x]}.jpg', 'wb') as image_file:
        image_file.write(image_data)
