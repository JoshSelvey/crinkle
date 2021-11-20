from scrape.scrape.match import scrape_player_matches
from scrape.scrape.team import scrape_team_players


teams = ['England', 'Australia', 'South_Africa', 'West_Indies', 'New_Zealand', 'India', 'Pakistan', 'Sri_Lanka', 'Zimbabwe', 'Bangladesh', 'Ireland', 'Afghanistan']

scrape_team_players(teams)
scrape_player_matches(teams)
