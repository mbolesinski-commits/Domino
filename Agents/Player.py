
class ClassPlayer:
    def __init__(self, cell_count=0, name='Default Player'):
        self.cell_count = cell_count
        self.name = name
        self.cell_list = []
        self.drew_count = -5
        self.moves_count = 0
        self.last_chosen_piece = None
        self.all_cell_sides = []

    def say_hello(self):
        print('hello')

    def clear_player(self):
        self.cell_count = 0
        self.cell_list = []
        self.drew_count = -5
        self.moves_count = 0
        self.last_chosen_piece = None
        self.all_cell_sides = []

    def introduce_yourself(self):
        cell_names_list = []
        for cell in self.cell_list:
            cell_names_list.append(cell.introduce_your_number(True))
        print(
            f'========================={self.name}===============================')
        print(
            f'Hello, I have {len(self.cell_list)} cells, which are: {cell_names_list}')
        print(
            f'I\'ve made {self.moves_count} moves, last one was: {self.last_chosen_piece} and drew {self.drew_count-5} times')
        print('==================================================================\n')

    def draw_piece(self, piece_obj):
        self.cell_list.append(piece_obj)
        self.cell_count += 1
        self.drew_count += 1
        self.all_cell_sides.append(piece_obj.endpiece_number)

    def get_usable_pieces(self, endpoints_list: list):
        usable_pieces = []
        for cell in self.cell_list:
            if cell.right_number in endpoints_list:
                usable_pieces.append([cell, cell.right_number])
            elif cell.left_number in endpoints_list:
                usable_pieces.append([cell, cell.left_number])
        return usable_pieces

    def search_starting_piece(self, is_twin=True,  looking_for=6):
        got_it = False
        for piece in self.cell_list:
            if is_twin:
                if piece.is_twin and piece.left_number == looking_for:
                    got_it = True
                    piece = self._play_piece(piece, -1)
                    return got_it, piece
            else:
                if not piece.is_twin and piece.cell_sum == looking_for:
                    got_it = True
                    piece = self._play_piece(piece, -1)
                    return got_it, piece
        return got_it, None

    def player_turn(self, endpoints_list: list, uniq_endpoints_list: list, locked_pieces_list: list, connected_pieces_list: list):
        usable_pieces = self.get_usable_pieces(endpoints_list)
        if not usable_pieces:
            return None, None
        chosen_piece, chosen_endpoint_number = self.chose_piece_2_play(
            usable_pieces=usable_pieces, uniq_endpoints_list=uniq_endpoints_list, locked_pieces_list=locked_pieces_list, connected_pieces_list=connected_pieces_list)
        self._play_piece(chosen_piece, chosen_endpoint_number)
        return chosen_piece, chosen_endpoint_number

    def chose_piece_2_play(self, **kwargs):
        # do zmiany na *args dla agentów którzy potrzebują więcej danych. | dobre miejsce na użycie dekoratora
        # albo zrobić funkcję w player o tej samej nazwie i nadpisywać ją u agentów
        chosen = kwargs['usable_pieces'][0]
        chosen_piece = chosen[0]
        chosen_endpoint_number = chosen[1]

        return chosen_piece, chosen_endpoint_number

    def _play_piece(self, chosen_piece, target_piece_number: int):
        self.last_chosen_piece = chosen_piece.introduce_your_number(
            return_val=True)
        self.moves_count += 1
        chosen_piece.owner = 'Board'
        self.cell_list.remove(chosen_piece)
        self.cell_count -= 1
        self.all_cell_sides.remove(chosen_piece.endpiece_number)
        if not chosen_piece.is_twin:
            chosen_piece.remove_endpiece_number(target_piece_number)
        return chosen_piece


if __name__ == '__main__':
    CP = ClassPlayer()

    print(CP.cell_count)
    pass
