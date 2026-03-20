from .Player import ClassPlayer
import random


class ClsRandomAgent(ClassPlayer):
    def __init__(self):
        super().__init__()
        self.name = "Whateva"
        # self.cell_list

    def say_hello(self):
        print('hello')

    def chose_piece_2_play(self, **kwargs):
        chosen = random.choice(kwargs['usable_pieces'])
        chosen_piece = chosen[0]
        chosen_endpoint_number = chosen[1]

        return chosen_piece, chosen_endpoint_number


if __name__ == '__main__':
    RA = ClsRandomAgent(0, 'random')
    print(RA.name)
    # print(RA.cell_count)

    pass
