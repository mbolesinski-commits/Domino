from .Player import ClassPlayer


class ClsHighestPossibleAgent(ClassPlayer):
    def __init__(self):
        super().__init__()
        self.name = "Rocket"

    def say_hello(self):
        print('hello')

    def chose_piece_2_play(self, **kwargs):
        # nieoptymalne z podwójnym [0][0]
        chosen_piece = kwargs['usable_pieces'][0][0]
        for piece in kwargs['usable_pieces']:
            if piece[0].cell_sum >= chosen_piece.cell_sum:
                chosen_piece = piece[0]
                chosen_endpoint_number = piece[1]

        return chosen_piece, chosen_endpoint_number


if __name__ == '__main__':

    pass
