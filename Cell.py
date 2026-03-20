
class ClassCell:
    def __init__(self, left_number, right_number, is_drawn=False, owner='board'):
        self.left_number = left_number
        self.right_number = right_number

        self.endpiece_number = [left_number, right_number]

        self.is_drawn = is_drawn
        if left_number == right_number:
            self.is_twin = True
        else:
            self.is_twin = False
        self.connected_count = 0

        self.owner = owner
        self.cell_sum = left_number + right_number

    def remove_endpiece_number(self, chosen_number):
        if chosen_number in self.endpiece_number:
            self.endpiece_number.remove(chosen_number)
        elif chosen_number == -1:
            pass
        else:
            raise ValueError(
                f'chosen number {chosen_number} is not on the cell {self.left_number}|{self.right_number}')

    def introduce_your_number(self, return_val=False):
        if return_val:
            return f'{self.left_number}|{self.right_number}'
        else:
            print(f'{self.left_number}|{self.right_number}')

    def read_your_init(self):
        print(f'{self.left_number}|{self.right_number}, Owner:{self.owner}, Endpiece:{self.endpiece_number}, Drawn:{self.is_drawn}')


if __name__ == '__main__':
    Cell = ClassCell(1, 2)
    Cell.introduce_your_number()
    Cell.read_your_init()

    pass
