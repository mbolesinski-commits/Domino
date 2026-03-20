from .Player import ClassPlayer


class ClsMinUniqAgent(ClassPlayer):
    def __init__(self):
        super().__init__()
        self.name = "Diogenes"

    def say_hello(self):
        print('hello')

    def chose_piece_2_play(self, **kwargs):
        uniq_endpoints_list = kwargs['uniq_endpoints_list']
        usable_pieces_list = kwargs['usable_pieces']
        chosen_piece, chosen_endpoint_number = None, None
        for piece in usable_pieces_list:
            if piece[0].is_twin:
                if piece[0].left_number in uniq_endpoints_list and chosen_piece == None:
                    chosen_piece = piece[0]
                    chosen_endpoint_number = piece[1]
            else:
                for site in piece[0].endpiece_number:
                    # do sprawdzenia czy to obsługuje double # nie obsługiwał więc dodałem if na górze
                    if site != piece[1]:
                        if site in uniq_endpoints_list:
                            chosen_piece = piece[0]
                            chosen_endpoint_number = piece[1]

        if not chosen_piece:
            # Jeżeli nie znalazłem kafelka to wybieram max(cell_sum)
            chosen_piece = kwargs['usable_pieces'][0][0]
            for piece in kwargs['usable_pieces']:
                if piece[0].cell_sum >= chosen_piece.cell_sum:
                    chosen_piece = piece[0]
                    chosen_endpoint_number = piece[1]
        return chosen_piece, chosen_endpoint_number


if __name__ == '__main__':

    pass
