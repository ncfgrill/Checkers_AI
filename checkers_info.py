'''
Checkers information relevant to both the AI and the player.
'''

pieces, kings = ['r', 'b'], ['R', 'B']
board_start = [['  +-----------------+'],
               ['1 |',' ','r',' ','r',' ','r',' ','r','|','r'],
               ['2 |','r',' ','r',' ','r',' ','r',' ','|','|'],
               ['3 |',' ','r',' ','r',' ','r',' ','r','|','v'],
               ['4 |',' ',' ',' ',' ',' ',' ',' ',' ','|'],
               ['5 |',' ',' ',' ',' ',' ',' ',' ',' ','|'],
               ['6 |','b',' ','b',' ','b',' ','b',' ','|','^'],
               ['7 |',' ','b',' ','b',' ','b',' ','b','|','|'],
               ['8 |','b',' ','b',' ','b',' ','b',' ','|','b'],
               ['  +-----------------+'],
               ['    A B C D E F G H']]

def get_piece(t):
  return pieces[t % 2]

def get_king(t):
  return kings[t % 2]

def get_board():
    return board_start
