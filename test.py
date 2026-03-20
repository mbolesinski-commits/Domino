from Agents.Random_choice import ClsRandomAgent
from Agents.HighestPossible import ClsHighestPossibleAgent
import Agents.Player
import Cell
from Board import ClassBoardManager

if __name__ == '__main__':

    i = 0
    for left in range(0, 7):
        for right in range(left, 7):
            i += 1
    print(i)

    a = [([left, right] for right in range(left, 7)) for left in range(0, 7)]
    print(a)
    pass
