import pandas as pd


def get_link(team, player1, player2):
  player_to_player = pd.read_csv(f'Data/Player_to_Player/{team}.csv', dtype=str).set_index('player').to_dict()['players']
  player_to_player = {player: players.split(',') for player, players in player_to_player.items()}
  player_info = pd.read_csv(f'Data/Team_to_Player/{team}.csv', dtype=str).set_index('id').to_dict()['name']
  dag, groups = bfs(player1, player2, player_to_player)
  reduced_dag = get_reduced_dag(dag, {}, [player2])
  data = {
    'nodes': [{'id': s, 'group': groups[s], 'name': player_info[s]} for s in reduced_dag],
    'links': [{"source": s, "target": e, "value": 1} for s in reduced_dag for e in reduced_dag[s]]
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


def get_reduced_dag(dag, reduced_dag, nodes):
  if nodes:
    for node in nodes:
      reduced_dag[node] = dag[node]
    reduced_node = [link for links in reduced_dag.values() for link in links if not link in reduced_dag]
    return get_reduced_dag(dag, reduced_dag, reduced_node)
  return reduced_dag