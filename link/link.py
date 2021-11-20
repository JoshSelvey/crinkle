import pandas as pd


class Link:

  def __init__(self, team, player1, player2):
    self.player1 = player1
    self.player2 = player2
    self.player_to_player = pd.read_csv(f'Data/Player_to_Player/{team}.csv', dtype=str).set_index('player').to_dict()['players']
    self.player_to_player = {player: players.split(',') for player, players in self.player_to_player.items()}
    self.player_info = pd.read_csv(f'Data/Team_to_Player/{team}.csv', dtype=str).set_index('id').to_dict()['name']
    self.players = {self.player1}
    self.dag, self.numbered = self.bfs()
    self.paths(self.dag, self.player2)
    self.dag = {p: [a for a in self.dag[p] if a in self.players] for p in self.players}
    self.data = {
      'nodes': [{'id': s, 'group': self.numbered[s], 'name': self.player_info[s]} for s in self.dag],
      'links': [{"source": s, "target": e, "value": 1} for s in self.dag for e in self.dag[s]]
      }

  def bfs(self):
    parent = {self.player1: [self.player1]}
    queue = [self.player1]
    visited = {self.player1: 1}
    while queue:
      current_node = queue.pop(0)
      if current_node == self.player2:
        return parent, visited
      for node in self.player_to_player[current_node]:
        if node not in visited:
          visited[node] = visited[current_node] + 1
          queue.append(node)
          parent[node] = [current_node]
        elif visited[current_node] == visited[parent[node][0]]:
          parent[node].append(current_node)
    return False, {}

  def paths(self, dag, end):
    if end == self.player1:
      return [end]
    result = []
    for e in dag[end]:
      subpaths = self.paths(dag, e)
      for subpath in subpaths:
        result.append(f'{end},{subpaths}')
        self.players.add(end)
    return result

#####

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
