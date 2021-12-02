import time

import pandas as pd


def get_link(team, player1, player2):
  player_to_player = pd.read_csv(f'Data/Player_to_Player/{team}.csv', dtype=str).set_index('player').to_dict()['players']
  player_to_player = {player: players.split(',') for player, players in player_to_player.items()}
  player_info = pd.read_csv(f'Data/Team_to_Player/{team}.csv', dtype=str).set_index('id').to_dict()['name']
  dag, groups = bfs(player1, player2, player_to_player)
  if not dag:
    return {'nodes':[], 'links':[]}
  reduced_dag, n_paths = get_reduced_dag(dag, player1, player2)
  data = {
    'nodes': [{'id': s, 'group': groups[s], 'name': player_info[s]} for s in reduced_dag],
    'links': [{"source": s, "target": e, "value": 1} for s in reduced_dag for e in reduced_dag[s]],
    'n_paths': n_paths
    }
  return data


def bfs(player1, player2, player_to_player):
  parent = {player1: [player1]}
  queue = [player1]
  visited = {player1: 1}
  while queue:
    current_node = queue.pop(0)
    if current_node == player2:
      return parent, visited
    for node in player_to_player[current_node]:
      if node not in visited:
        visited[node] = visited[current_node] + 1
        queue.append(node)
        parent[node] = [current_node]
      elif visited[current_node] == visited[parent[node][0]]:
        parent[node].append(current_node)
  return False, {}


def get_paths(dag, end, start, players):
  if end == start:
    return players, 1
  count = 0
  for e in dag[end]:
    players, sub_count = get_paths(dag, e, start, players=players)
    players.add(end)
    count += sub_count
  return players, count


def get_reduced_dag(dag, player1, player2):
  players, n_paths = get_paths(dag, player2, player1, {player1})
  reduced_dag = {player: [a for a in dag[player] if a in players] for player in players}
  return reduced_dag, n_paths
