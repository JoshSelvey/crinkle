import shutil

from bs4 import BeautifulSoup as bs


def save_images(teams):
  for team in teams:
    print(team)
    with open(f'Pages/Caps/{team}.html') as f:
        soup = bs(f, 'html.parser')
    table = [player.find_all('div') for player in soup.find_all('div', {'class': 'player-row'})]
    image_source_dict = [{
      'id': row[1].find('a')['href'].split('-')[-1],
      'source': row[2].find('img')['src']
    } for row in table]
    for player in image_source_dict:
      shutil.copyfile(f'Pages/Caps/{player["source"][2:]}', f'public/images/{player["id"]}.jpg')
