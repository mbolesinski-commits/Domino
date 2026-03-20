import random
from Cell import ClassCell


class ClassBoardManager:
    def __init__(self):
        self.free_pieces_list = []  # nie pobrane
        self.locked_pieces_list = []
        self.connected_pieces_list = []  # dostępne
        self.uniq_endpoints_list = []

    def update_board_velues(self):
        # pobiera pierwszą wartość z endpointów bo 2 powinny być tylko przy doublach
        self.uniq_endpoints_list = []
        for piece in self.connected_pieces_list:
            for number in piece.endpiece_number:
                self.uniq_endpoints_list.append(number)
        self.uniq_endpoints_list = list(set(self.uniq_endpoints_list))

    def show_board_info(self):
        undrawn = self.return_pieces_list('undrawn')
        locked = self.return_pieces_list('locked')
        connected = self.return_pieces_list('connected')
        print(f'State of the board:')
        print(f'Undrawn({len(undrawn)}): {undrawn}')
        print(f'Locked({len(locked)}): {locked}')
        print(f'Connected({len(connected)}): {connected}')
        print(
            f'There are {len(self.uniq_endpoints_list)} unique endpoints, which are: {self.uniq_endpoints_list}')
        print('')

    def fill_free_pieces_list(self):
        i = 0
        for left in range(0, 7):
            for right in range(i, 7):
                self.free_pieces_list.append(ClassCell(left, right))
            i += 1

    def return_rand_free_piece(self):
        chosen_piece = random.choice(self.free_pieces_list)
        chosen_piece.is_drawn = False
        self.free_pieces_list.remove(chosen_piece)
        return chosen_piece

    def return_pieces_list(self, which_list):
        pieces_lists = {
            'undrawn': self.free_pieces_list,
            'locked': self.locked_pieces_list,
            'connected': self.connected_pieces_list
        }

        introduction_list = []
        for piece in pieces_lists[which_list]:
            introduction_list.append(piece.introduce_your_number(True))

        return introduction_list

    def place_opening_piece(self, chosen_piece):
        self.connected_pieces_list.append(chosen_piece)

    def place_piece(self, chosen_piece, target_piece_number: int):
        target_piece = None
        for placed_piece in self.connected_pieces_list:
            for endpiece_number in placed_piece.endpiece_number:
                if endpiece_number == target_piece_number:
                    target_piece = placed_piece
                    break
        if not target_piece:
            raise ValueError(
                f'Target piece not found for this target number: {target_piece_number}')
        target_piece.remove_endpiece_number(target_piece.endpiece_number[0])
        if len(target_piece.endpiece_number) == 0:
            self.locked_pieces_list.append(target_piece)
            self.connected_pieces_list.remove(target_piece)

        self.connected_pieces_list.append(chosen_piece)


if __name__ == '__main__':
    CBM = ClassBoardManager()
    CBM.fill_free_pieces_list()

    mylist = CBM.return_pieces_list('undrawn')
    print(len(mylist))
    print(mylist)

    chosen_piece = CBM.return_rand_free_piece()
    chosen_piece.introduce_your_number()

    mylist = CBM.return_pieces_list('undrawn')
    print(mylist)

    pass
