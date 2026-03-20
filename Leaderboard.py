import pandas as pd


class Leaderboard:
    def __init__(self, possible_players_names_list):
        self.df_players = pd.DataFrame(
            columns=['Player Name', 'Score', 'Won Games'])
        self.df_games = pd.DataFrame(
            columns=['Player_1', 'Player_2', 'Player_3',
                     'Player_4', 'Player5', 'Winner', 'GameScore', 'Game Rounds', 'Game Seed']
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
