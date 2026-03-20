from Agents.RandomChoice import ClsRandomAgent
from Agents.HighestPossible import ClsHighestPossibleAgent
from Agents.LowestPossible import ClsLowestPossibleAgent
from Agents.MinUniq import ClsMinUniqAgent
from Agents.CellCounting import ClsCellCounting
from Board import ClassBoardManager
import random


class ClassGameManager:
    def __init__(self, how_many_players=4):
        self.Board = None
        self.how_many_players = how_many_players
        self.player_list = []
        self.player_pieces_count = []
        self.round_count = 0
        self.game_winner_name = None
        self.first_player = None
        self.draw_count = 0

    def say_hello(self):
        print('hello')

    def prepare_gameboard(self):
        self.Board = ClassBoardManager()
        self.Board.fill_free_pieces_list()

    def change_player_order(self, starting_player):
        player_index = self.player_list.index(starting_player)
        if player_index < len(self.player_list) - 1:
            player_index += 1
        else:
            player_index = 0
        new_player_list = self.player_list[player_index:]
        new_player_list.extend(self.player_list[:player_index])
        self.player_list = new_player_list

    def check_player_pieces_count(self):
        self.player_pieces_count = []
        for player in self.player_list:
            self.player_pieces_count.append(player.cell_count)

    def welcome_players(self, list_of_players, random_payers=True):
        if random_payers:
            self.PlayerRandom = ClsRandomAgent()
            self.PlayerHigh = ClsHighestPossibleAgent()
            self.PlayerLow = ClsLowestPossibleAgent()
            self.PlayerMinUniq = ClsMinUniqAgent()
            self.PlayerCellCounting = ClsCellCounting()
            list_of_players = [self.PlayerRandom,
                               self.PlayerHigh, self.PlayerLow, self.PlayerMinUniq, self.PlayerCellCounting]

        for player in list_of_players:
            player.clear_player()
            self.player_list.append(player)
        self.how_many_players = len(list_of_players)

    def cell_draw(self, how_many, drawing_player_list):
        if not self.player_list[0]:
            raise Exception('Player list empty for cell draw')
        if not self.Board:
            raise Exception('Game Board not initiated for cell draw')
        if len(self.Board.free_pieces_list) == 0:
            raise Exception(
                'Unable to draw more cells, free pieces stack is empty')

        for i in range(how_many):
            for player in drawing_player_list:
                piece = self.Board.return_rand_free_piece()
                piece.owner = player.name
                player.draw_piece(piece)

    def read_gameboard(self):
        if not self.Board:
            raise Exception('Game Board not initiated for read!')
        else:
            self.Board.show_board_info()

    def read_players(self, player_or_list):
        if type(player_or_list) == list:
            for player in player_or_list:
                player.introduce_yourself()
        else:
            player_or_list.introduce_yourself()

    def opening_move(self):
        # potencjalne miejsce do optymalizacji, aktualnie przeszukuje wszystko za każdym razem, przy remisie dla sumy liczb biorę pierwszą znalezioną
        for looking_for in range(6, -1, -1):
            for player in self.player_list:
                first_player_found, found_piece = player.search_starting_piece(
                    True, looking_for)
                if first_player_found:
                    self.first_player = player
                    self.change_player_order(self.first_player)
                    self.Board.place_opening_piece(found_piece)
                    self.Board.update_board_velues()

                    return None

        for looking_for in range(11, -1, -1):
            first_player_found, found_piece = player.search_starting_piece(
                False, looking_for)
            if first_player_found:
                self.first_player = player
                self.change_player_order(self.first_player)
                self.Board.place_opening_piece(found_piece)
                self.Board.update_board_velues()

                return None

    def player_turn(self, player, endpoints_list):
        chosen_piece, target_endpoint_number = player.player_turn(
            endpoints_list, self.Board.uniq_endpoints_list, self.Board.locked_pieces_list, self.Board.connected_pieces_list)
        if not chosen_piece:
            if len(self.Board.free_pieces_list) > 0:
                player.draw_piece(self.Board.return_rand_free_piece())
                self.draw_count += 1
                chosen_piece, target_endpoint_number = player.player_turn(
                    endpoints_list, self.Board.uniq_endpoints_list, self.Board.locked_pieces_list, self.Board.connected_pieces_list)
        return chosen_piece, target_endpoint_number

    def game_over(self):
        player_points = 0
        player_dict = {}
        for player in self.player_list:
            player_points_sum = 0
            for cell in player.cell_list:
                player_points_sum += cell.cell_sum
            player_dict[player.name] = player_points_sum

        self.game_winner_name = min(player_dict, key=player_dict.get)
        for player in player_dict:
            if player != self.game_winner_name:
                player_points += player_dict[player]
        player_points -= player_dict[self.game_winner_name]
        return player_points

    def game_loop(self, print_turns: bool):
        while len(self.Board.free_pieces_list) > 0 and 0 not in self.player_pieces_count:
            self.round_count += 1
            for player in self.player_list:
                chosen_piece, target_endpoint_number = self.player_turn(
                    player, self.Board.uniq_endpoints_list)
                if chosen_piece:
                    self.Board.place_piece(
                        chosen_piece, target_endpoint_number)
                    self.Board.update_board_velues()
                    self.check_player_pieces_count()
                    if print_turns:
                        print(
                            f'Round {self.round_count}, playing: {player.name}\n')
                        self.read_players(player)
                        self.read_gameboard()
                else:
                    if print_turns:
                        print(
                            f'Round {self.round_count}, playing: {player.name}\n')
                        print(f'Player {player.name} draw and got nothing')
                        self.read_players(player)
                        self.read_gameboard()
                    if len(self.Board.free_pieces_list) == 0:
                        return None
                if player.cell_count == 0:
                    return None

        draw = False
        if len(self.Board.free_pieces_list) == 0:
            draw = True
        return draw

    def clear_geme(self):
        self.Board = None
        self.player_list = []
        self.player_pieces_count = []
        self.round_count = 0
        self.game_winner_name = None

    def play_game(self, player_list, random_players: bool, how_many_cells: int, print_game_moves: bool):
        self.clear_geme()
        self.prepare_gameboard()
        self.welcome_players(player_list, random_payers=random_players)
        self.cell_draw(how_many_cells, self.player_list)
        self.opening_move()
        self.game_loop(print_game_moves)
        player_points = self.game_over()
        return self.game_winner_name, player_points


if __name__ == '__main__':
    # seed 27 i 74(2 graczy), 8(3 graczy): remis
    # bugi:
    # lowest i highest możliwe że porównuje każdy klocek do pierwszego (do weryfikacji)
    draw_seed = 0
    for i in range(29, 30):
        random.seed(i)
        print('SEED:' + str(i))

        GM = ClassGameManager()
        GM.prepare_gameboard()
        GM.welcome_players()
        GM.cell_draw(5, GM.player_list)
        GM.read_gameboard()
        GM.read_players(GM.player_list)

        GM.opening_move()
        GM.first_player.introduce_yourself()
        GM.read_gameboard()

        draw = GM.game_loop(True)
        if draw:
            draw_seed = i

        player_points = GM.game_over()
        GM.read_players(GM.player_list)
        GM.read_gameboard()
        print(
            f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!Game winner: {GM.game_winner_name}, earned: {player_points} points !!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    pass
