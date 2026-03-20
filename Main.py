import GameManager
from Leaderboard import Leaderboard
from Agents.Random_choice import ClsRandomAgent
from Agents.HighestPossible import ClsHighestPossibleAgent
from Agents.LowestPossible import ClsLowestPossibleAgent
from Agents.MinUniq import ClsMinUniqAgent
from Agents.CellCounting import ClsCellCounting
import random
from itertools import combinations
import pandas as pd
import xlsxwriter


class Main():
    def __init__(self):
        self.GM = GameManager.ClassGameManager()
        self.PlayerRandom = ClsRandomAgent()
        self.PlayerHigh = ClsHighestPossibleAgent()
        self.PlayerLow = ClsLowestPossibleAgent()
        self.PlayerMinUniq = ClsMinUniqAgent()
        self.PlayerCellCounting = ClsCellCounting()
        self.list_of_all_players = [self.PlayerRandom,
                                    self.PlayerHigh, self.PlayerLow, self.PlayerMinUniq, self.PlayerCellCounting]
        self.list_of_all_players_names = [
            player.name for player in self.list_of_all_players]
        self.game_leaderboard = Leaderboard(self.list_of_all_players_names)

    def play_whole_game(self, list_of_players, game_seed, random_players: bool):
        game_seed *= 100
        list_of_players_names = [
            player.name for player in list_of_players]
        self.game_leaderboard.add_players_to_dict(list_of_players_names)
        games_played = 0
        while max(self.game_leaderboard.game_dict.values()) <= 100:
            random.seed(game_seed)
            game_winner_name, player_points = self.GM.play_game(player_list=list_of_players, random_players=random_players,
                                                                how_many_cells=5, print_game_moves=False)
            self.game_leaderboard.add_points_to_dict(
                game_winner_name, player_points)

            cells_on_table = len(self.GM.Board.locked_pieces_list) + \
                len(self.GM.Board.connected_pieces_list)
            cells_undrawn = len(self.GM.Board.free_pieces_list)
            player_data = [(player.name, player.drew_count, player.cell_count)
                           for player in list_of_players]
            self.game_leaderboard.add_single_game_to_df(
                OpeningPlayer=self.GM.first_player.name, Winner=game_winner_name, Game_Score=self.game_leaderboard.game_dict[
                    game_winner_name], GameTurns=self.GM.round_count, GameSeed=game_seed,
                CellsUndrawn=cells_undrawn, CellsOnTable=cells_on_table, player_data=player_data
            )

            games_played += 1
            game_seed += 1
        return game_winner_name, player_points, games_played, self.GM.player_list

    def get_random_players(self, how_many: int):
        possible_players = self.list_of_all_players.copy()
        list_of_players = []
        for i in range(how_many):
            chosen_player = random.choice(possible_players)
            possible_players.remove(chosen_player)
            list_of_players.append(chosen_player)
        return list_of_players

    def games_loop(self, how_many_loops: int, how_many_players: int, specific_game_seed: int, random_players: bool, player_list):
        for game in range(how_many_loops):
            if specific_game_seed:
                random.seed(specific_game_seed)
            else:
                random.seed(game)
                game_seed = game

            list_of_players = []
            if random_players:
                list_of_players = self.get_random_players(how_many_players)
            else:
                for player_index in player_list:
                    list_of_players.append(
                        self.list_of_all_players[player_index])

            game_winner_name, player_points, games_played, this_game_player_list = self.play_whole_game(
                list_of_players, game_seed, random_players)
            list_of_players_names = [None, None, None, None, None]
            for index, player in enumerate(this_game_player_list):
                list_of_players_names[index] = player.name
            self.game_leaderboard.update_player_df(
                game_winner_name, player_points)
            self.game_leaderboard.add_game_to_df(
                Player_1=list_of_players_names[0], Player_2=list_of_players_names[1], Player_3=list_of_players_names[2], Player_4=list_of_players_names[3], Player_5=list_of_players_names[4], Winner=game_winner_name, Game_Score=self.game_leaderboard.game_dict[game_winner_name], Game_Rounds=games_played, Game_seed=game_seed)
            self.print_game_results(
                game_winner_name, player_points, games_played)

    def play_all_possible_games(self, how_many_loops_for_setup: int):
        list_of_all_players_index = [
            x for x, y in enumerate(self.list_of_all_players_names)]
        for combination_count in range(3, 6):
            player_list = list(combinations(
                list_of_all_players_index, combination_count))
            for player_combination in player_list:
                self.games_loop(how_many_loops_for_setup, len(
                    player_list), None, False, player_list=list(player_combination))

    def print_game_results(self, game_winner_name, player_points, games_played):
        print(
            f'Game winner: {game_winner_name}, gained {player_points} points')
        print(self.game_leaderboard.game_dict)
        print(f'Games played: {games_played}')


if __name__ == '__main__':
    MyGame = Main()

    # PlayerRandom = 0 PlayerHigh = 1 PlayerLow = 2 PlayerMinUniq = 3 PlayerCellCounting = 4

    """     print(MyGame.game_leaderboard.df_players.head())
    print(MyGame.game_leaderboard.df_games.head())
    MyGame.games_loop(how_many_loops=10, how_many_players=5,
                  specific_game_seed=None, random_players=True, player_list=[4])

    print(MyGame.game_leaderboard.df_players.head())
    print(MyGame.game_leaderboard.df_games.head(
        10).sort_index(ascending=False)) """

    MyGame.play_all_possible_games(10)

    with pd.ExcelWriter('D:\Projekty\Domino\Excel\Pierwsze_wyniki.xlsx') as writer:
        MyGame.game_leaderboard.df_games.to_excel(
            writer, sheet_name='Game', index=False)
        MyGame.game_leaderboard.df_players.to_excel(
            writer,  sheet_name='Players', index=False)
        MyGame.game_leaderboard.df_single_games.to_excel(
            writer,  sheet_name='All games details', index=False)
        workbook = writer.book
        writer.sheets['Game'].autofit()
        writer.sheets['Players'].autofit()
        writer.sheets['All games details'].autofit()
