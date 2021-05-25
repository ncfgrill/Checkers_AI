'''
AI checkers player functionality.

This module implements the artificial checkers player. It implements an
alpha-beta purning mini-max search algorithm of depth 6.
'''

from copy import deepcopy
from random import randint
from checkers_info import get_piece, get_king

def choose_move(b, t):
    s, v = max_value(b, -100, 100, t, 6)
    return s

def get_succ(b, t):
    '''Get successor states of a given board for a given turn.
    Params:
        b: current board state
        t: current turn
    Returns:
        list of successor states to given state b
    '''
    succ = []
    l_p, l_k = get_locs(b, t) # list of piece and king locations, respectively

    # direction pieces moving on board (1 if r, -1 if b)
    d = 1 if t % 2 == 0 else -1

    for p in l_p:
        r, c = p[0], p[1]
    
        copy_simple_state(succ, b, r, c, d, t, 0)
        copy_jump_state(succ, b, r, c, d, t, 0)

    for k in l_k:
        r, c = k[0], k[1]

        copy_simple_state(succ, b, r, c, d, t, 1)
        copy_jump_state(succ, b, r, c, d, t, 1)
    
    if b in succ: succ.remove(b)
    return succ

def copy_simple_state(s, b, r, c, d, t, p):
    '''Gets simple successor states.
    This function returns all successor states created by moving
    only one piece to one adjacent space.
    Params:
        s: list of successor states
        b: current board state
        r: row of piece to be moved
        c: col of piece to be moved
        d: piece direction (1 if r is moving, -1 if b)
        t: current turn
        p: if piece moving is regular piece or king
    '''
    r_disp = r + d # row displacement
    if r_disp > 0 and r_disp < 9:
        c_disp = c - 1 # col displacement
        if c > 1 and b[r_disp][c_disp] == ' ':
            m = deepcopy(b)
            if r_disp != 1 and r_disp != 8: m[r_disp][c_disp] = m[r][c]
            else:                           m[r_disp][c_disp] = get_king(t)
            m[r][c] = ' '
            s.append(m)

        c_disp = c + 1
        if c < 8 and b[r_disp][c_disp] == ' ':
            m = deepcopy(b)
            if r_disp != 1 and r_disp != 8: m[r_disp][c_disp] = m[r][c]
            else:                           m[r_disp][c_disp] = get_king(t)
            m[r][c] = ' '
            s.append(m)
  
    r_disp = r - d
    if p == 1 and r_disp > 0 and r_disp < 9:
        c_disp = c - 1
        if c > 1 and b[r_disp][c_disp] == ' ':
            m = deepcopy(b)
            m[r_disp][c_disp], m[r][c] = m[r][c], ' '
            s.append(m)

        c_disp = c + 1
        if c < 8 and b[r_disp][c_disp] == ' ':
            m = deepcopy(b)
            m[r_disp][c_disp], m[r][c] = m[r][c], ' '
            s.append(m)

def copy_jump_state(s, b, r, c, d, t, p):
    '''Gets complicated successor states.
    This function returns all successor states created by jumping
    one piece over at least one other opposing piece.
    Params:
        s: list of successor states
        b: current board state
        r: row of piece to be moved
        c: col of piece to be moved
        d: piece direction (1 if r is moving, -1 if b)
        t: current turn
        p: if piece moving is regular piece or king
    '''
    cont = 0 # 0 if state has no successors, 1 otherwise

    # r_disp1 is one row displacement, r_disp2 is two rows displacement
    r_disp1, r_disp2 = r + d, r + 2*d
    if r_disp2 > 0 and r_disp2 < 9: # displaced rows are on board
        # c_disp1 is one col displament, c_disp2 is two cols displacement
        c_disp1, c_disp2 = c - 1, c - 2
        if c > 2 and\
          (b[r_disp1][c_disp1] == get_piece(t+1) or\
           b[r_disp1][c_disp1] == get_king(t+1)) and\
           b[r_disp2][c_disp2] == ' ':
            m = deepcopy(b)
            if r_disp2 != 1 and r_disp2 != 8: m[r_disp2][c_disp2] = m[r][c]
            else:                             m[r_disp2][c_disp2] = get_king(t)
            m[r][c] = m[r_disp1][c_disp1] = ' '

            cont = 1 # successor exists, don't add this state
            if b[r][c] == get_king(t): p_n = 1
            else:                      p_n = 0
            copy_jump_state(s, m, r_disp2, c_disp2, d, t, p_n)

        c_disp1, c_disp2 = c + 1, c + 2
        if c < 7 and\
          (b[r_disp1][c_disp1] == get_piece(t+1) or\
           b[r_disp1][c_disp1] == get_king(t+1)) and\
           b[r_disp2][c_disp2] == ' ':
            m = deepcopy(b)
            if r_disp2 != 1 and r_disp2 != 8: m[r_disp2][c_disp2] = m[r][c]
            else:                             m[r_disp2][c_disp2] = get_king(t)
            m[r][c] = m[r_disp1][c_disp1] = ' '
      
            cont = 1
            if b[r][c] == get_king(t): p_n = 1
            else:                      p_n = 0
            copy_jump_state(s, m, r_disp2, c_disp2, d, t, p_n)

    r_disp1, r_disp2 = r - d, r - 2*d
    if p == 1 and r_disp2 > 0 and r_disp2 < 9:
        c_disp1, c_disp2 = c - 1, c - 2
        if c > 2 and\
          (b[r_disp1][c_disp1] == get_piece(t+1) or\
           b[r_disp1][c_disp1] == get_king(t+1)) and\
           b[r_disp2][c_disp2] == ' ':
            m = deepcopy(b)
            m[r_disp2][c_disp2] = m[r][c]
            m[r][c], m[r_disp1][c_disp1] = ' ', ' '

            cont = 1
            copy_jump_state(s, m, r_disp2, c_disp2, d, t, 1)

        c_disp1, c_disp2 = c + 1, c + 2
        if c < 7 and\
          (b[r_disp1][c_disp1] == get_piece(t+1) or\
           b[r_disp1][c_disp1] == get_king(t+1)) and\
           b[r_disp2][c_disp2] == ' ':
            m = deepcopy(b)
            m[r_disp2][c_disp2] = m[r][c]
            m[r][c], m[r_disp1][c_disp1] = ' ', ' '

            cont = 1
            copy_jump_state(s, m, r_disp2, c_disp2, d, t, 1)
  
    if cont == 0 and b not in s: s.append(b)

def get_locs(b, t):
    '''Get piece locations.
    This function returns the (row,col) locations of all
    regular pieces and kings of a given board position
    on a given turn.
    Params:
        b: current board state
        t: current turn
    Returns:
        l_p: list of regular piece locations
        l_k: list of king piece locations
    '''
    p, k, l_p, l_k = get_piece(t), get_king(t), [], []
  
    for i in range(1, 9):
        for j in range(1, 9):
            if b[i][j] == p: l_p.append((i, j))
            elif b[i][j] == k: l_k.append((i, j))

    return l_p, l_k

def max_value(b, alpha, beta, t, d):
    value = game_value(b, t)
    if value == 1: return b, value

    best_states = []
    if d > 0:
        for s in get_succ(b, t):
            c_s, c_a = min_value(s, alpha, beta, t+1, d-1)
            if c_a == 1 or c_a == -1: return s, c_a
            if c_a >= alpha:
                if c_a > alpha:
                    alpha = c_a
                    best_states.clear()
                best_states.append(s)

            if alpha >= beta: return b, alpha

        if len(best_states) == 0: return b, value
        best = best_states[randint(0, len(best_states) - 1)]
    else: return b, value

    return best, alpha

def min_value(b, alpha, beta, t, d):
    value = game_value(b, t)
    if value == -1: return b, value

    best_states = []
    if d > 0:
        for s in get_succ(b, t):
            c_s, c_b = max_value(s, alpha, beta, t+1, d-1)
            if c_b == 1 or c_b == -1: return s, c_b
            if c_b <= beta:
                if c_b < beta:
                    beta = c_b
                    best_states.clear()
                best_states.append(s)

            if alpha >= beta: return b, beta

        if len(best_states) == 0: return b, value
        best = best_states[randint(0, len(best_states) - 1)]
    else: return b, value

    return best, beta

def game_value(b, t):
    my_p, my_k = get_locs(b, t)
    opp_p, opp_k = get_locs(b, t+1)
    n = (len(my_p) + len(my_k), len(opp_p) + len(opp_k))
    if n[0] == 0: return -1
    if n[1] == 0: return 1

    total, num_m, num_o = 0, 0, 0

    for p in my_p:
        num_m += 1
        if p[0] == 1 or p[0] == 8:
            if len(my_p) > 6: total += 15
            else:             total += 2
        elif (p[0] < 5 and t % 2 == 1) or\
             (p[0] > 4 and t % 2 == 0): total += 3
        else: total += 1
    for k in my_k:
        num_m += 1
        total += 5

    for p in opp_p:
        num_o += 1
        if p[0] == 1 or p[0] == 8:
            if len(opp_p) > 6: total -= 5
            else:              total -= 2
        elif (p[0] < 5 and t % 2 == 1) or\
             (p[0] > 4 and t % 2 == 0): total -= 3
        else: total -= 1
    for k in opp_k:
        num_o += 1
        total -= 5

    if num_m == n[0]: total += 4
    else:             total -= 4
    if num_o < n[1]:  total += 5
    else:             total -= 5

    if num_m > num_o: total += 2
    else:             total -= 2

    return total/200
