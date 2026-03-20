import pandas as pd


class Leaderboard:
    def __init__(self, possible_players_names_list):
        self.df_players = pd.DataFrame(
            columns=['Player Name', 'Score', 'Won Games'])
        self.df_games = pd.DataFrame(
            columns=['Player_1', 'Player_2', 'Player_3',
                     'Player_4', 'Player5', 'Winner', 'GameScore', 'Game Rounds', 'Game Seed']
        )
        self.df_single_games = pd.DataFrame(
            columns=['Player_1_name', 'Player_1_draws', 'Player_1_cells_left', 'Player_2_name', 'Player_2_draws', 'Player_2_cells_left', 'Player_3_name', 'Player_3_draws', 'Player_3_cells_left', 'Player_4_name', 'Player_4_draws',
                     'Player_4_cells_left', 'Player_5_name', 'Player_5_draws', 'Player_5_cells_left', 'OpeningPlayer', 'Winner', 'GameScore', 'GameTurns', 'GameSeed', 'CellsUndrawn', 'CellsOnTable', 'CellsAmountCheck']
        )
        self.game_dict = {}
        for player in possible_players_names_list:
            self.df_players = pd.concat([pd.DataFrame(
                [[player, 0, 0]], columns=self.df_players.columns), self.df_players], ignore_index=True)

    def add_players_to_dict(self, player_list):
        self.game_dict = {}
        for player in player_list:
            self.game_dict[player] = 0

    def add_points_to_dict(self, player_name, points):
        self.game_dict[player_name] += points

    def add_game_to_df(self, Player_1, Player_2, Player_3,
                       Player_4, Player_5, Winner, Game_Score, Game_Rounds, Game_seed):
        self.df_games = pd.concat([pd.DataFrame(
            [[Player_1, Player_2, Player_3,
              Player_4, Player_5, Winner, Game_Score, Game_Rounds, Game_seed]], columns=self.df_games.columns), self.df_games], ignore_index=True)

    def add_single_game_to_df(self, OpeningPlayer, Winner, Game_Score, GameTurns, GameSeed, CellsUndrawn, CellsOnTable, player_data: list):
        player_stats = [[None, None, None], [None, None, None], [
            None, None, None], [None, None, None], [None, None, None]]

        CellsAmountCheck = CellsUndrawn + CellsOnTable
        for index, arg in enumerate(player_data):
            player_stats[index] = arg
            CellsAmountCheck += arg[1]

        self.df_single_games = pd.concat([pd.DataFrame(
            [[player_stats[0][0], player_stats[0][1], player_stats[0][2], player_stats[1][0], player_stats[1][1], player_stats[1][2], player_stats[2][0], player_stats[2][1], player_stats[2][2],
              player_stats[3][0], player_stats[3][1], player_stats[3][2], player_stats[4][0], player_stats[4][1], player_stats[4][2],
              OpeningPlayer, Winner, Game_Score, GameTurns,
              GameSeed, CellsUndrawn,
              CellsOnTable,
              CellsAmountCheck,
              ]], columns=self.df_single_games.columns), self.df_single_games], ignore_index=True)

    def update_player_df(self, player_name, score):
        self.df_players.loc[self.df_players['Player Name']
                            == player_name, 'Score'] += score
        self.df_players.loc[self.df_players['Player Name']
                            == player_name, 'Won Games'] += 1


if __name__ == '__main__':
    GameLeaderboard = Leaderboard(['Whateva', 'Rocket', 'Krecik'])
    print(GameLeaderboard.df_players.head())

    print(GameLeaderboard.update_player_df('Whateva', 1))

    print(GameLeaderboard.df_players.head())

    print(GameLeaderboard.update_player_df('Whateva', 1))

    print(GameLeaderboard.df_players.head())

    pass
