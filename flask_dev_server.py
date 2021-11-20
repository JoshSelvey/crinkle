import json

from flask import Flask

from link.link import get_link

app = Flask(__name__)

@app.route('/api/get_player_dropdown')
def get_player_dropdown():
  with open('JSON/Dropdown.json') as f:
    return {'data': json.load(f)}


@app.route('/api/get_team_dropdown')
def get_team_dropdown():
  with open('JSON/Teams.json') as f:
    return {'data': json.load(f)}


@app.route('/api/get_link_data/<team>/<player1>/<player2>')
def get_link_data(team, player1, player2):
  return get_link(team, player1, player2)