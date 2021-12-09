from scrape.scrape.images import save_images
from scrape.wrangle.wrangle import wrangle_teams, wrangle_world
from scrape.wrangle.json import get_json

teams = ['England', 'Australia', 'South_Africa', 'West_Indies', 'New_Zealand', 'India', 'Pakistan', 'Sri_Lanka', 'Zimbabwe', 'Bangladesh', 'Ireland', 'Afghanistan']

save_images(teams)
wrangle_teams(teams)
wrangle_world(teams)
get_json(teams)
