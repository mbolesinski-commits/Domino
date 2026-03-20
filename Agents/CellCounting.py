from .Player import ClassPlayer


class ClsCellCounting(ClassPlayer):
    def __init__(self):
        super().__init__()
        self.name = "Protokół Zgredek"
        self.numbers_dict = {'0': 7, '1': 7,
                             '2': 7, '3': 7, '4': 7, '5': 7, '6': 7}

    def say_hello(self):
        print('hello')

    def chose_piece_2_play(self, **kwargs):
        usable_pieces_list = kwargs['usable_pieces']
        board_pieces = self.cell_list.copy()
        board_pieces.extend(
            kwargs['connected_pieces_list'] + kwargs['locked_pieces_list'])
        temp_numbers_dict = self.numbers_dict.copy()

        for cell in board_pieces:
            temp_numbers_dict[str(cell.left_number)] -= 1
            temp_numbers_dict[str(cell.right_number)] -= 1

        max_waight = 7
        for piece in usable_pieces_list:
            if piece[0].is_twin:
                if temp_numbers_dict[str(piece[0].left_number)] <= max_waight:
                    max_waight = temp_numbers_dict[str(piece[0].left_number)]
                    chosen_piece = piece[0]
                    chosen_endpoint_number = piece[1]
            else:
                for site in piece[0].endpiece_number:
                    if site != piece[1]:
                        if temp_numbers_dict[str(site)] <= max_waight:
                            max_waight = temp_numbers_dict[str(site)]
                            chosen_piece = piece[0]
                            chosen_endpoint_number = piece[1]
        return chosen_piece, chosen_endpoint_number


if __name__ == '__main__':

    pass
