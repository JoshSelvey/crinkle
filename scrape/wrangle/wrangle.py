import pandas as pd


def reverse_dict(dictionary):
    reverse_dict = {}
    for k, v in dictionary.items():
        for x in v:
            reverse_dict.setdefault(x, []).append(str(k))
    return reverse_dict


def played_with(player_to_match, player1, player2):
  if not player1 == player2:
    for match in player_to_match[player1]:
      if match in player_to_match[player2]:
        return True
  return False


def get_player_to_player(player_to_match):
  return {player1: [player2 for player2 in player_to_match if played_with(player_to_match, player1, player2)] for player1 in player_to_match}


def dict_list_to_string(dictionary):
  return {k: ','.join(v) for k, v in dictionary.items()}


def wrangle_teams(teams):
  for team in teams:
    print(team)
    player_to_match_strings = pd.read_csv(f'Data/Player_to_Match/{team}.csv', index_col=['id'], usecols=['id', 'matches']).to_dict()['matches']
    player_to_match = {player: matches.split(',') for player, matches in player_to_match_strings.items()}
    match_to_player = reverse_dict(player_to_match)
    match_to_player_exclusive = {match: players for match, players in match_to_player.items() if len(players) >= 11}
    player_to_match_exclusive = reverse_dict(match_to_player_exclusive)
    player_to_player_exclusive = get_player_to_player(player_to_match_exclusive)
    pd.DataFrame.from_dict(dict_list_to_string(player_to_match_exclusive), orient='index', columns=['matches']).rename_axis('player').to_csv(f'Data/Player_to_Match_Exclusive/{team}.csv')
    pd.DataFrame.from_dict(dict_list_to_string(match_to_player_exclusive), orient='index', columns=['players']).rename_axis('match').to_csv(f'Data/Match_to_Player/{team}.csv')
    pd.DataFrame.from_dict(dict_list_to_string(player_to_player_exclusive), orient='index', columns=['players']).rename_axis('player').to_csv(f'Data/Player_to_Player/{team}.csv')


def wrangle_world(teams):
  player_to_match_strings = pd.concat([pd.read_csv(f'Data/Player_to_Match/{team}.csv', index_col=['id'], usecols=['id', 'matches']) for team in teams]).to_dict()['matches']
  player_info = pd.concat([pd.read_csv(f'Data/Team_to_Player/{team}.csv', index_col=['id'], usecols=['id', 'name']) for team in teams])
  player_info = player_info[~player_info.index.duplicated(keep='last')]
  player_to_match = {str(player): matches.split(',') for player, matches in player_to_match_strings.items()}
  match_to_player = reverse_dict(player_to_match)
  player_to_player = get_player_to_player(player_to_match)
  pd.DataFrame.from_dict(dict_list_to_string(player_to_match), orient='index', columns=['matches']).rename_axis('player').to_csv('Data/Player_to_Match_Exclusive/World.csv')
  pd.DataFrame.from_dict(dict_list_to_string(match_to_player), orient='index', columns=['players']).rename_axis('match').to_csv('Data/Match_to_Player/World.csv')
  pd.DataFrame.from_dict(dict_list_to_string(player_to_player), orient='index', columns=['players']).rename_axis('player').to_csv('Data/Player_to_Player/World.csv')
  player_info.to_csv('Data/Team_to_Player/World.csv')
