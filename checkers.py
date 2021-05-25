from copy import deepcopy
from random import choice
from time import sleep
from sys import exit
from checkers_ai import choose_move, get_succ
import checkers_info as ci

class CheckersPlayer:
    '''
    An object representation for an AI game player for the game checkers.
    '''
    cols = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
    mod_board = []

    def __init__(self):
        i = choice([0, 1])
        self.my_piece, self.my_king = ci.get_piece(i), ci.get_king(i)
        self.opp_p, self.opp_k = ci.get_piece((i+1)%2), ci.get_king((i+1)%2)
        self.mod_board = ci.get_board()

    def print_board(self):
        print('\n'.join(' '.join(l) for l in self.mod_board))

    def check_win(self, t):
        return len(get_succ(self.mod_board, t))

    def validate_move(self, f, t, turn):
        errors = ["You don't have a piece there!",
                  "Invalid row.",
                  "Invalid column.",
                  "Must specify at least one move.",
                  "Invalid move.",
                  "Invalid multi-move.",
                  "Non-legal move."]

        if len(f) != 2: return 0, errors[0]
  
        try: frow = int(f[1])
        except ValueError: return 0, errors[1]
        if frow < 1 or frow > 8: return 0, errors[1]

        try: fcol = self.cols[f[0].upper()]
        except KeyError: return 0, errors[2]

        n_moves = len(t)
        if n_moves == 0: return 0, errors[3]

        b = deepcopy(self.mod_board)
        for m in t:
            if len(m) != 2: return 0, errors[4]

            try: trow = int(m[1])
            except ValueError: return 0, errors[1]
            if trow < 1 or trow > 8: return 0, errors[1]

            try: tcol = self.cols[m[0].upper()]
            except KeyError: return 0, errors[2]

            d1 = trow - frow # row change
            d2 = tcol - fcol # col change
  
            if abs(d1) != 1 and abs(d1) != 2 or abs(d1) != abs(d2):
                return 0, errors[4]
            if n_moves > 1 and abs(d1) < 2: return 0, errors[5]

            if trow != 1 and trow != 8: b[trow][tcol] = b[frow][fcol]
            else:                       b[trow][tcol] = ci.get_king(turn)
            b[frow][fcol] = ' '
            if abs(d1) == 2: b[(trow+frow)//2][(tcol+fcol)//2] = ' '

            frow = trow
            fcol = tcol

        if b in get_succ(self.mod_board, turn): self.mod_board = b
        else: return 0, errors[6]

        return 1, ''

    def rules(self):
        print('''
How to play Checkers!
  ++Basic Rules++
    1. Players alternate turns, moving only their own pieces.
    2. A move consists of moving a piece diagonally to an adjacent
       unoccupied space.
    3. A piece can only move foward based on the player's starting
       direction.
    4. If the adjacent space contains an opponent's piece, and the
       space immediately beyond it is vacant, the piece may be
       captured (and removed) by jumping over it.
  ++Advanced Rules++
    1. Multiple enemy pieces can be captured in a single turn by
       successive jumps made by a single piece. Jumps may be along a
       diagonal, or \"zig-zag\" across the board.
    2. When a regular piece reaches the farthest opposite row, it is
       upgraded to a King.
    3. Kings can move and capture pieces (regular and Kings) both
       forwards and backwards.
  ++Winning the Game++
    The game ends when one player has no pieces left on the board
    or cannot make any moves due to being blocked.
        ''')
        input("Press enter when done.\n")

    def leave(self):
        print("Farewell!")
        exit()

#################
#               #
# GAMEPLAY CODE #
#               #
#################

def main():
    ai, turn = CheckersPlayer(), 0
    print('Welcome to Checkers!\n')
    while True:
        print('Please select an option:\n  1. Play Game\n  2. Rules\n  3. Exit')
        mode = input('Option: ')
        if len(mode) != 1 or mode not in '123':
            print('Invalid input.')
            continue

        if mode == '1': break
        elif mode == '2': ai.rules()
        else: ai.leave()

    print('\nI will play ' + ai.my_piece + '. You will play ' + ai.opp_p + '.')
    sleep(0.5)

    # Game will end when player of current turn has no successive states
    while ai.check_win(turn) != 0:
        print('\nMy turn!') if ci.get_piece(turn) == ai.my_piece else\
            print('\nYour turn!')
        ai.print_board()

        if ai.my_piece == ci.get_piece(turn):
            ai.mod_board = choose_move(ai.mod_board, turn)
            sleep(1)
        else:
            move_made = False
            while not move_made:
                print("""
Select a piece to move (e.g. B3) and location to move.
Separate locations with a comma (e.g. C4,B6).
Type 'rules' to see the Rules or 'resign' to leave the game.
                """)
                f = input("Piece: ").strip()
                if f.lower().strip() == "rules":
                    ai.rules()
                    ai.print_board()
                    continue
                elif f.lower().strip() == "resign":
                    print("You are no match for me.")
                    ai.leave()
    
                t = input("Move to: ").strip().split(',')
                valid, msg = ai.validate_move(f, t, turn)
                if not valid:
                    print(msg, "Please try again.\n")
                    ai.print_board()
                else: move_made = True
        turn = (turn + 1) % 2

    # Game has ended. Print final board and AI message
    ai.print_board()
    print('\nYou have defeated me...\n') if\
        ci.get_piece(turn) == ai.my_piece else\
        print('The AI takeover begins now...')

if __name__ == "__main__":
    main()
