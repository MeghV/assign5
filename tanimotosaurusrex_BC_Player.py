from random import *

# Ryan Chui, Megh Vakharia
# Assignment 5 
# Tanimoto
# CSE 415

BLACK = 0
WHITE = 1
PLAYER = 0

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

LAST_MOVE = ""

def who(piece): return piece % 2

def parse(bs): # bs is board string
  '''Translate a board string into the list of lists representation.'''
  b = [[0,0,0,0,0,0,0,0] for r in range(8)]
  rs9 = bs.split("\n")
  rs8 = rs9[1:] # eliminate the empty first item.
  for iy in range(8):
    rss = rs8[iy].split(' ');
    for jx in range(8):
      b[iy][jx] = INIT_TO_CODE[rss[jx]]
  return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')
	
class BC_state:
  def __init__(self, old_board=INITIAL, whose_move=WHITE):
    new_board = [r[:] for r in old_board]
    self.board = new_board
    self.whose_move = whose_move;

  def __repr__(self):
    s = ''
    for r in range(8):
      for c in range(8):
        s += CODE_TO_INIT[self.board[r][c]] + " "
      s += "\n"
    if self.whose_move==WHITE: s += "WHITE's move"
    else: s += "BLACK's move"
    s += "\n"
    return s

def test_starting_board():
  init_state = BC_state(INITIAL, WHITE)
  print(init_state)

test_starting_board()

def introduce():
  # Returns a string that introduces the Baroque Chess playing agent.
  return "I AM TANIMOTOSAURUS REX, THE WORLD'S BEST BAROQUE CHESS PLAYER!\n" +\
          "MY CREATORS ARE RYAN CHUI (rchui) AND MEGH VAKHARIA (meghv). LET'S RUMBLEEEEEE!"

def nickname():
  # Returns the nickname of the Baroque Chess playing agent.
  return "Tanimotosaurus"

def prepare(nickname):
    pass

def DEEP_COPY(old):
  new = []
  for i in old:
    temp = []
    for j in i:
      temp.append(j)
    new.append(temp)
  return new

def DEEP_EQUALS(list1, list2):
  new1 = DEEP_COPY(list1)
  new2 = DEEP_COPY(list2)
  if new1 == new2:
    return True
  else:
    return False

def move(s, from_row, from_column, to_row, to_column):
  new = DEEP_COPY(s)
  hold = new[from_row][from_column]
  new[from_row][from_column] = 0
  new[to_row][to_column] = hold
  new = remove_piece(new, from_row, from_column, to_row, to_column, hold)
  return new

def is_opponent(piece_id):
  global PLAYER
  if piece_id != 0:
    if PLAYER == 1:
      if piece_id % 2 == 0:
        return False
    else:
      if piece_id % 2 != 0:
        return False
  return True

def find_king(new):
  row = -1
  column = -1
  for i in range(8):
    for j in range(8):
      if new[i][j] in [12, 13]:
        if not is_opponent(new[i][j]):
          row = i
          column = j
  return (row, column)\

def pincer_kill(new, from_row, from_column, to_row, to_column, hold):
  if to_row + 1 < 8 and is_opponent(new[to_row + 1][to_column]):
    if to_row + 2 < 8 and not is_opponent(new[to_row + 2][to_column]):
      new[to_row + 1][to_column] = 0
  if to_row - 1 >= 0 and is_opponent(new[to_row - 1][to_column]):
    if to_row - 2 >= 0 and not is_opponent(new[to_row - 2][to_column]):
      new[to_row - 1][to_column] = 0
  if to_column + 1 < 8 and is_opponent(new[to_row][to_column + 1]):
    if to_column + 2 < 8 and not is_opponent(new[to_row][to_column + 2]):
      new[to_row][to_column + 1] = 0
  if to_column - 1 >= 0 and is_opponent(new[to_row][to_column - 1]):
    if to_column - 2 >= 0 and not is_opponent(new[to_row][to_column - 2]):
      new[to_row][to_column - 1] = 0

def leaper_kill(new, from_row, from_column, to_row, to_column, hold):
  if to_row + 1 < 8 and is_opponent(new[to_row + 1][to_column]) and (from_column == to_column):
    if to_row + 2 < 8 and new[to_row + 2][to_column] == 0:
      new[to_row + 1][to_column] = 0
      new[to_row + 2][to_column] = hold
      new[to_row][to_column] = 0
  elif to_row - 1 >= 0 and is_opponent(new[to_row - 1][to_column]) and (from_column == to_column):
    if to_row - 2 >= 0 and new[to_row - 2][to_column] == 0:
      new[to_row - 1][to_column] = 0
      new[to_row - 2][to_column] = hold
      new[to_row][to_column] = 0
  elif to_column + 1 < 8 and is_opponent(new[to_row][to_column + 1]) and (from_row == to_row):
    if to_column + 2 < 8 and new[to_row][to_column + 2] == 0:
      new[to_row][to_column + 1] = 0
      new[to_row][to_column + 2] = hold
      new[to_row][to_column] = 0
  elif to_column - 1 >= 0 and is_opponent(new[to_row][to_column - 1]) and (from_row == to_row):
    if to_column - 2 >= 0 and new[to_row][to_column - 2] == 0:
      new[to_row][to_column - 1] = 0
      new[to_row][to_column - 2] = hold
      new[to_row][to_column] = 0
  elif to_row + 1 < 8 and to_column + 1 < 8 and is_opponent(new[to_row + 1][to_column + 1]) and (from_column < to_column) and (from_row < to_row):
    if to_row + 2 < 8 and to_column + 2 < 8 and new[to_row + 2][to_column + 2] == 0:
      new[to_row + 1][to_column + 1] = 0
      new[to_row + 2][to_column + 2] = hold
      new[to_row][to_column] = 0
  elif to_row - 1 >= 0 and to_column - 1 >= 0 and is_opponent(new[to_row - 1][to_column - 1]) and (from_column > to_column) and (from_row > to_row):
    if to_row - 2 >= 0 and to_column - 2 >= 0 and new[to_row - 2][to_column - 2] == 0:
      new[to_row - 1][to_column - 1] = 0
      new[to_row - 2][to_column - 2] = hold
      new[to_row][to_column] = 0
  elif to_row - 1 >= 0 and to_column + 1 < 8 and is_opponent(new[to_row - 1][to_column + 1]) and (from_column < to_column) and (from_row > to_row):
    if to_row - 2 >= 0 and to_column + 2 < 8 and new[to_row - 2][to_column + 2] == 0:
      new[to_row - 1][to_column + 1] = 0
      new[to_row - 2][to_column + 2] = hold
      new[to_row][to_column] = 0
  elif to_row + 1 < 8 and to_column - 1 >= 0 and is_opponent(new[to_row + 1][to_column - 1]) and (from_column > to_column) and (from_row < to_row):
    if to_row + 2 < 8 and to_column - 2 >= 0 and new[to_row + 2][to_column - 2] == 0:
      new[to_row + 1][to_column - 1] = 0
      new[to_row + 2][to_column - 2] = hold
      new[to_row][to_column] = 0

def coordinator_kill(new, from_row, from_column, to_row, to_column, hold):
  (king_row, king_column) = find_king(new)
  if is_opponent(new[king_row][to_column]):
    new[king_row][to_column] = 0
  if is_opponent(new[to_row][king_column]):
    new[to_row][king_column] = 0

def withdrawer_kill(new, from_row, from_column, to_row, to_column, hold):
  if from_row + 1 < 8:
    if is_opponent(new[from_row + 1][from_column]) and (from_column == to_column):
      new[from_row + 1][from_column] = 0
  if from_row - 1 >= 0:
    if is_opponent(new[from_row - 1][from_column]) and (from_column == to_column):
      new[from_row - 1][from_column] = 0
  if from_column + 1 < 8:
    if is_opponent(new[from_row][from_column + 1]) and (from_row == to_row):
     new[from_row][from_column + 1] = 0
  if from_column - 1 >= 0:
    if is_opponent(new[from_row][from_column - 1]) and (from_row == to_row):
     new[from_row][from_column - 1] = 0
  if from_column + 1 < 8:
    if from_row + 1 < 8 and is_opponent(new[from_row + 1][from_column + 1]) and (from_column > to_column) and (from_row > to_row):
     new[from_row + 1][from_column + 1] = 0
  if from_column - 1 >= 0 and from_row + 1 < 8:
    if is_opponent(new[from_row + 1][from_column - 1]) and (from_column > to_column) and (from_row < to_row):
      new[from_row + 1][from_column - 1] = 0
  if from_column + 1 < 8 and from_row - 1 < 8:
    if is_opponent(new[from_row - 1][from_column + 1]) and (from_column < to_column) and (from_row > to_row):
      new[from_row - 1][from_column + 1] = 0
  if from_column - 1 < 8 and from_row - 1 < 8:
    if is_opponent(new[from_row - 1][from_column - 1]) and (from_column < to_column) and (from_row < to_row):
     new[from_row - 1][from_column - 1] = 0

def imitator_kill(new, from_row, from_column, to_row, to_column, hold):
  if to_row + 1 < 8 and is_opponent(new[to_row + 1][to_column]):
    if new[to_row + 1][to_column] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row + 1][to_column] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row + 1][to_column] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_row - 1 >= 0 and is_opponent(new[to_row - 1][to_column]):
    if new[to_row - 1][to_column] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row - 1][to_column] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row - 1][to_column] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_column + 1 < 8 and is_opponent(new[to_row][to_column + 1]):
    if new[to_row][to_column + 1] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row][to_column + 1] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row][to_column + 1] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_column - 1 >= 0 and is_opponent(new[to_row][to_column - 1]):
    if new[to_row][to_column - 1] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row][to_column - 1] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row][to_column - 1] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_row + 1 < 8 and to_column + 1 < 8 and is_opponent(new[to_row + 1][to_column + 1]):
    if new[to_row + 1][to_column + 1] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row + 1][to_column + 1] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row + 1][to_column + 1] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_row - 1 >= 0 and to_column - 1 >= 0 and is_opponent(new[to_row - 1][to_column - 1]):
    if new[to_row - 1][to_column - 1] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row - 1][to_column - 1] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row - 1][to_column - 1] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_row - 1 >= 0 and to_column + 1 < 8 and is_opponent(new[to_row - 1][to_column + 1]):
    if new[to_row - 1][to_column + 1] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row - 1][to_column + 1] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row - 1][to_column + 1] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif to_row + 1 < 8 and to_column - 1 >= 0 and is_opponent(new[to_row + 1][to_column - 1]):
    if new[to_row + 1][to_column - 1] in [2, 3]:
      pincer_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row + 1][to_column - 1] in [4, 5]:
      coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
    elif new[to_row + 1][to_column - 1] in [6, 7]:
      leaper_kill(new, from_row, from_column, to_row, to_column, hold)

  if from_row + 1 < 8 and is_opponent(new[from_row + 1][from_column]):
    if new[from_row + 1][from_column] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_row - 1 >= 0 and is_opponent(new[from_row - 1][from_column]):
    if new[from_row - 1][from_column] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_column + 1 < 8 and is_opponent(new[from_row][from_column + 1]):
    if new[from_row][from_column + 1] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_column - 1 >= 0 and is_opponent(new[from_row][from_column - 1]):
    if new[from_row][from_column - 1] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_row + 1 < 8 and from_column + 1 < 8 and is_opponent(new[from_row + 1][from_column + 1]):
    if new[from_row + 1][from_column + 1] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_row + 1 < 8 and from_column - 1 >= 0 and is_opponent(new[from_row + 1][from_column - 1]):
    if new[from_row + 1][from_column - 1] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_row - 1 >= 0 and from_column + 1 < 8 and is_opponent(new[from_row - 1][from_column + 1]):
    if new[from_row - 1][from_column + 1] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif from_row - 1 >= 0 and from_column - 1 >= 0 and is_opponent(new[from_row - 1][from_column - 1]):
    if new[from_row - 1][from_column - 1] in [10, 11]:
      withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)

def remove_piece(new, from_row, from_column, to_row, to_column, hold):
  if hold in [2, 3]:
    pincer_kill(new, from_row, from_column, to_row, to_column, hold)
  elif hold in [4, 5]:
    coordinator_kill(new, from_row, from_column, to_row, to_column, hold)
  elif hold in [6, 7]:
    leaper_kill(new, from_row, from_column, to_row, to_column, hold)
  elif hold in [8, 9]:
    imitator_kill(new, from_row, from_column, to_row, to_column, hold)
  elif hold in [10, 11]:
    withdrawer_kill(new, from_row, from_column, to_row, to_column, hold)
  return new

# Checks that the horizontal path is clear.
def clear_path_vertical(s, from_row, from_column, to_row, to_column):
  check_row = from_row
  while check_row != to_row:
    if from_row > to_row:
      check_row -= 1
    else:
      check_row += 1
    if s[check_row][from_column] != 0:
      return False
  return True

# Chceks that the vertical path is clear.
def clear_path_horizontal(s, from_row, from_column, to_row, to_column):
  check_column = from_column
  while check_column != to_column:
    if from_column > to_column:
      check_column -= 1
    else:
      check_column += 1
    if s[from_row][check_column] != 0:
      return False
  return True

# Checks that the diagonal path is clear.
def clear_path_diagonal(s, from_row, from_column, to_row, to_column):
  check_row = from_row
  check_column = from_column
  while check_row != to_row and check_column != to_column:
    if from_row > to_row:
      check_row -= 1
    else:
      check_row += 1
    if from_column > to_column:
      check_column -= 1
    else:
      check_column += 1
    if s[check_row][check_column] != 0:
      return False
  return True

# Checks that there are empty spaces around the piece.
def can_move(s, from_row, from_column, to_row, to_column):
  global PLAYER
  if s[from_row][from_column] != 0:
    if not((from_row + 1 < 8 and from_column + 1 < 8 and s[from_row + 1][from_column + 1] in [14, 15]) or 
       (from_row + 1 < 8 and from_column - 1 >= 0 and s[from_row + 1][from_column - 1] in [14, 15]) or 
       (from_row - 1 >= 0 and from_column - 1 >= 0 and s[from_row - 1][from_column - 1] in [14, 15]) or 
       (from_row - 1 >= 0 and from_column + 1 < 8 and s[from_row - 1][from_column + 1] in [14, 15]) or 
       (from_row + 1 < 8 and s[from_row + 1][from_column] in [14, 15]) or 
       (from_row - 1 >= 0 and s[from_row - 1][from_column] in [14, 15]) or 
       (from_column + 1 < 8 and s[from_row][from_column + 1] in [14, 15]) or
       (from_column - 1 >= 0 and s[from_row][from_column - 1] in [14, 15])):
      if PLAYER == 1:
        if s[from_row][from_column] % 2 == 0:
          return False
      else:
        if s[from_row][from_column] % 2 != 0:
          return False
      if not ((from_row != to_row) and (from_column != to_column)):
        if s[from_row][from_column] in [12, 13]:
          if (abs(from_row - to_row) <= 1) and (abs(from_column - to_column) <= 1):
            if is_opponent(s[to_row][to_column]):
              return True
          return False
      if s[to_row][to_column] == 0 and not ((from_row != to_row) and (from_column != to_column)):
        # print ("can_move", from_row, from_column, to_row, to_column)
        if (from_row == to_row):
          if clear_path_horizontal(s, from_row, from_column, to_row, to_column):
            return True
        elif (from_column == to_column):
          if clear_path_vertical(s, from_row, from_column, to_row, to_column):
            return True
        elif s[from_row][from_column] not in [2, 3]:
          if (abs(from_row - to_row) == abs(from_column - to_column)):
            if clear_path_diagonal(s, from_row, from_column, to_row, to_column):
              return True
  return False

# print can_move(INITIAL, 2, 0, 3, 0)

# Checks to see if the board has already occured.
def occurs_in(new_state, test_list):
  for i in test_list:
    if DEEP_EQUALS(new_state, i):
      return True
  return False

# Makes unique Hashcode for board state.
def HASHCODE(s):
  resp = ""
  for i in s[:-1]:
    resp += str(i) + ";"
  resp += str(s[-1])
  return resp

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

move_combinations = []
for i in range(8):
  for j in range(8):
    for k in range(8):
      for l in range(8):
        move_combinations.append((i, j, k, l))

OPERATORS = [Operator("Move piece at " + str(p) + ", " + str(q) + " to " + str(m) + ", " + str(n),
                      lambda s, p = p, q = q, m = m, n = n: can_move(s, p, q, m, n),
                      lambda s, p = p, q = q, m = m, n = n: move(s, p, q, m, n))
                      for (p, q, m, n) in move_combinations]

# Alpha Beta to find the optimal board move.
def makeMove(currentState, currentRemark, timeLimit = 10000):
  import math
  import time
  LAST_MOVE = BC_state(currentState.board, currentState.whose_move)
  last_board = DEEP_COPY(currentState.board)
  infinity = math.inf
  global PLAYER
  PLAYER = currentState.whose_move
  cutoff = 1
  limit = 0.40
  t0 = time.clock()

  def successors(state):
    S = state
    L = []
    for op in OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        if not DEEP_EQUALS(new_state, S):
          L.append(new_state)
    return L
  first_moves = successors(last_board)

  def max_value(state, alpha, beta, depth):
    elapsed = (time.clock() - t0)
    if elapsed > limit:
      return staticEval(state)
    if depth > cutoff:
      return staticEval(state)
    v = -infinity
    for s in successors(state):
      v = max(v, min_value(s, alpha, beta, depth + 1))
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v

  def min_value(state, alpha, beta, depth):
    elapsed = (time.clock() - t0)
    if elapsed > limit:
      return staticEval(state)
    if depth > cutoff:
      return staticEval(state)
    v = infinity
    for s in successors(state):
      v = min(v, max_value(s, alpha, beta, depth + 1))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v

  best = []
  for i in first_moves:
    best.append(min_value(i, -infinity, infinity, 0))
    elapsed = (time.clock() - t0)
    if elapsed > limit:
      break
  import operator
  index, value = max(enumerate(best), key=operator.itemgetter(1))

  if currentState.whose_move == 1:
    player_move = 0
  else:
    player_move = 1

  elapsed = (time.clock() - t0)
  if elapsed > limit:
    import random
    next_move = random.choice(first_moves)
    NEW_MOVE = BC_state(next_move, player_move)
  else:
    NEW_MOVE = BC_state(first_moves[index], player_move)

  return [["", NEW_MOVE], "RAWR! YOUR MOVE PUNY HUMAN!"]

# 14 x 64 table to represent the different pieces
# (7 on each side) as well as the different positions
# (8x8 == 64 total)
PIECES = 14
POSITIONS = 64

# Adds random values to the 14 x 64 ZOBRIST_NUM_TABLE table 
# representing all 14 black & white pieces and the 64 positions
# they can be in. # 64-bit integers are recommended for Chess 
# as the collision probability is ~1 in 4 billion positions
ZOBRIST_NUM_TABLE = [ [ randint(0, 9223372036854775807) ] * POSITIONS ] * PIECES

# Stores previous states keyed by their Zobrist hash values.
# The value of each state is represented as follows:
# { evaluation_value: 0, ply: 0, cutoff_value: cutoff_value}
# "evaluation_value" is the previously calculated static evaluation 
# function value, "ply" is the ply at which the value was
# calculated, and "cutoff_value" is the value that resulted in
# a cutoff of the state branch.
PREVIOUS_STATES = {}

def calculate_zobrist_hash(state):
  '''
  Calculates the Zobrist hash of a state by XORing together all of
  the random values which represent each piece and position to 
  produce a hash representing the state. 
  '''
  global ZOBRIST_NUM_TABLE
  hash = 0
  for row_idx, row in enumerate(state):
    for piece_idx, piece in enumerate(row):
      # the numbers 2 - 15 represent black / white pieces on the
      # gameboard, so subtracting by 2 can represent indices (0 - 13) 
      # in the ZOBRIST_NUM_TABLE
      piece_hash_index = piece - 2
      # ensure we're not dealing with an empty spot
      if piece_hash_index >= 0:
        piece_col = (row_idx + 1) * (piece_idx + 1) - 1
        hash ^= ZOBRIST_NUM_TABLE[piece_hash_index][piece_col]
  return hash
        
def store_transposition_table_value(zobrist_hash, evaluation_value, cutoff_value, ply):
  '''
  Caches the static evaluation function value for a unique state
  to avoid recomputing evaluation values for transpositions in 
  future searches. The ply at which the static evaluation value 
  was calculated is also stored.
  '''
  global PREVIOUS_STATES
  # ensures duplicate values aren't stored
  if zobrist_hash not in PREVIOUS_STATES:
    PREVIOUS_STATES[zobrist_hash] =\
      {"evaluation_value": evaluation_value,\
       "ply": ply, "cutoff_value": cutoff_value}

def get_transposition_table_value(zobrist_hash):
  ''' 
  Returns the static evaluation value, ply, and cutoff of a 
  previously encountered state. If the state doesn't exist,
  None is returned.
  '''
  if zobrist_hash in PREVIOUS_STATES:
    return PREVIOUS_STATES[zobrist_hash]
  return None

# Represents piece values to be used in the
# static evaluation function. A pawn is worth 100
# and a king is worth 100x that - 10000 - as the king
# (and the death of a king) is worth the most. Between 
# those values, the Immobilizer is worth the most at 750.
# The Immobilizer is one of the most powerful pieces in
# the game and as such, is valued 2nd highest. Other pieces
# are valued less based on their attack capabilities. Movement
# abilites are only taken into account for the Pawn (and King)
# as every other piece can move in any direction.
PIECE_VALUES = {
  "2": -100,   # Black / Pawn
  "3":  100,   # White / Pawn
  "4": -250,   # Black / Coordinator
  "5":  250,   # White / Coordinator
  "6": -300,   # Black / Leaper
  "7":  300,   # White / Leaper
  "8": -350,   # Black / Imitator
  "9":  350,   # White / Imitator
  "10": -500,  # Black / Withdrawer
  "11":  500,  # White / Withdrawer
  "12": -10000,  # Black / King
  "13":  10000,  # White / King
  "14": -750,  # Black / Immobilizer
  "15": 750  # White / Immobilizer
}

WHITE_PIECES = [3,15,7,9,11,13,9,7,5]
BLACK_PIECES = [4,6,8,10,12,8,6,14,2]
def is_white_piece(piece_number):
  return piece_number in WHITE_PIECES

def is_black_piece(piece_number):
  return piece_number in BLACK_PIECES

def staticEval(state):
  score = float(0)
  for row_idx, row in enumerate(state):
    for piece_idx, piece in enumerate(row):
      if piece != 0:
        # Killing pieces counts for the most
        # points
        piece_value = PIECE_VALUES[str(piece)]
        score += piece_value

        upper_piece = -1
        bottom_piece = -1
        right_piece = -1
        left_piece = -1
        upper_left_corner_piece = -1
        upper_right_corner_piece = -1
        bottom_left_corner_piece = -1
        bottom_right_corner_piece = -1
        upper_space = row_idx > 0
        bottom_space = row_idx < 7
        left_space = piece_idx > 0
        right_space = piece_idx < 7

        if upper_space:
          upper_piece = state[row_idx - 1][piece_idx]
        if left_space:
          left_piece = state[row_idx][piece_idx - 1]
        if right_space:
          right_piece = state[row_idx][piece_idx + 1]
        if bottom_space:
          bottom_piece = state[row_idx + 1][piece_idx]
        if upper_space and left_space:
          upper_left_corner_piece = state[row_idx - 1][piece_idx - 1]
        if upper_space and right_space:
          upper_right_corner_piece = state[row_idx - 1][piece_idx + 1]
        if bottom_space and left_space:
          bottom_left_corner_piece = state[row_idx + 1][piece_idx - 1]
        if bottom_space and right_space:
          bottom_right_corner_piece = state[row_idx + 1][piece_idx + 1]
        
        # Boost for immobilizations 
        if piece in [14,15]:
          score += immobilizer_boost(piece, upper_piece, bottom_piece, right_piece, left_piece, \
                                     upper_right_corner_piece, upper_left_corner_piece, bottom_right_corner_piece, bottom_left_corner_piece)
        # Boost for withdrawers
        elif piece in [10,11]:
          score += withdrawer_boost(piece, upper_piece, bottom_piece, right_piece, left_piece, \
                                     upper_right_corner_piece, upper_left_corner_piece, bottom_right_corner_piece, bottom_left_corner_piece)

  return score

def is_opposite_color(piece_a, piece_b):
  return (PIECE_VALUES[str(piece_a)] *  PIECE_VALUES[str(piece_b)]) < 0


def withdrawer_boost(withdrawer_piece, upper_piece=-1, lower_piece=-1, right_piece=-1, left_piece=-1,\
                      upper_right_corner_piece=-1, upper_left_corner_piece=-1, bottom_right_corner_piece=-1, bottom_left_corner_piece=-1):
  '''
  Gives a boost to the player if their withdrawer is next to an enemy piece.
  '''
  score_boost = float(0)
  withdrawer_boost = lambda withdrawer_target, withdrawer: PIECE_VALUES[str(withdrawer_target)] * 0.04

  if upper_piece not in [-1,0] and is_opposite_color(upper_piece, withdrawer_piece):
    # print("Withdrawer above piece: " + str(upper_piece) + ", " + str(PIECE_VALUES[str(upper_piece)]))
    score_boost += withdrawer_boost(upper_piece, withdrawer_piece)

  if lower_piece not in [-1,0] and is_opposite_color(lower_piece, withdrawer_piece):
    # print("Withdrawer Below: " + str(lower_piece) + ", " + str(PIECE_VALUES[str(lower_piece)]))
    score_boost += withdrawer_boost(lower_piece, withdrawer_piece)

  if right_piece not in [-1,0] and is_opposite_color(right_piece, withdrawer_piece):
    # print("Withdrawer Right: " + str(right_piece) + ", " + str(PIECE_VALUES[str(right_piece)]))
    score_boost += withdrawer_boost(right_piece, withdrawer_piece)

  if left_piece not in [-1,0] and is_opposite_color(left_piece, withdrawer_piece):
    # print("Withdrawer Left: " + str(left_piece) + ", " + str(PIECE_VALUES[str(left_piece)]))
    score_boost += withdrawer_boost(left_piece, withdrawer_piece)

  if upper_right_corner_piece not in [-1,0] and is_opposite_color(upper_right_corner_piece, withdrawer_piece):
    # print("Withdrawer Upper Right: " + str(upper_right_corner_piece) + ", " + str(PIECE_VALUES[str(upper_right_corner_piece)]))
    score_boost += withdrawer_boost(upper_right_corner_piece, withdrawer_piece)

  if upper_left_corner_piece not in [-1,0] and is_opposite_color(upper_left_corner_piece, withdrawer_piece):
    # print("Withdrawer Upper Left: " + str(upper_left_corner_piece) + ", " + str(PIECE_VALUES[str(upper_left_corner_piece)]))
    score_boost += withdrawer_boost(upper_left_corner_piece, withdrawer_piece)

  if bottom_left_corner_piece not in [-1,0] and is_opposite_color(bottom_left_corner_piece, withdrawer_piece):
    # print("Withdrawer Bottom Left: "+ str(bottom_left_corner_piece) + ", " + str(PIECE_VALUES[str(bottom_left_corner_piece)]))
    score_boost += withdrawer_boost(bottom_left_corner_piece, withdrawer_piece)

  if bottom_right_corner_piece not in [-1,0] and is_opposite_color(bottom_right_corner_piece, withdrawer_piece):
    # print("Withdrawer Bottom Right: " + str(bottom_right_corner_piece) + ", " + str(PIECE_VALUES[str(bottom_right_corner_piece)]))
    score_boost += withdrawer_boost(bottom_right_corner_piece, withdrawer_piece)

  # Swap sign if player is WHITE piece to give positive boost
  if is_white_piece(withdrawer_piece): score_boost *= -1
  return score_boost


def immobilizer_boost(immobilizer_piece, upper_piece=-1, lower_piece=-1, right_piece=-1, left_piece=-1,\
                      upper_right_corner_piece=-1, upper_left_corner_piece=-1, bottom_right_corner_piece=-1, bottom_left_corner_piece=-1):
  global PIECE_VALUES
  '''
  Gives a boost to a player if their immobilizer has immobilized pieces.
  The boost is relative to the value of the immobilizied piece(s).
  '''
  score_boost = float(0)
  # Boost function: value of immobilized piece / value of immobilizier (this will always be negative)
  immobilizer_boost = lambda immobilized_piece, immobilizer: PIECE_VALUES[str(immobilized_piece)] * 0.06

  if upper_piece not in [-1,0] and is_opposite_color(upper_piece, immobilizer_piece):
    # print("Immobilizer Above: " + str(upper_piece) + ", " + str(PIECE_VALUES[str(upper_piece)]))
    score_boost += immobilizer_boost(upper_piece, immobilizer_piece)

  if lower_piece not in [-1,0] and is_opposite_color(lower_piece, immobilizer_piece):
    # print("Immobilizer Below: " + str(lower_piece) + ", " + str(PIECE_VALUES[str(lower_piece)]))
    score_boost += immobilizer_boost(lower_piece, immobilizer_piece)

  if right_piece not in [-1,0] and is_opposite_color(right_piece, immobilizer_piece):
    # print("Immobilizer Right: " + str(right_piece) + ", " + str(PIECE_VALUES[str(right_piece)]))
    score_boost += immobilizer_boost(right_piece, immobilizer_piece)

  if left_piece not in [-1,0] and is_opposite_color(left_piece, immobilizer_piece):
    # print("Immobilizer Left: " + str(left_piece) + ", " + str(PIECE_VALUES[str(left_piece)]))
    score_boost += immobilizer_boost(left_piece, immobilizer_piece)

  if upper_right_corner_piece not in [-1,0] and is_opposite_color(upper_right_corner_piece, immobilizer_piece):
    # print("Immobilizer Upper Right: " + str(upper_right_corner_piece) + ", " + str(PIECE_VALUES[str(upper_right_corner_piece)]))
    score_boost += immobilizer_boost(upper_right_corner_piece, immobilizer_piece)

  if upper_left_corner_piece not in [-1,0] and is_opposite_color(upper_left_corner_piece, immobilizer_piece):
    # print("Immobilizer Upper Left: " + str(upper_left_corner_piece) + ", " + str(PIECE_VALUES[str(upper_left_corner_piece)]))
    score_boost += immobilizer_boost(upper_left_corner_piece, immobilizer_piece)

  if bottom_left_corner_piece not in [-1,0] and is_opposite_color(bottom_left_corner_piece, immobilizer_piece):
    # print("Immobilizer Bottom Left: "+ str(bottom_left_corner_piece) + ", " + str(PIECE_VALUES[str(bottom_left_corner_piece)]))
    score_boost += immobilizer_boost(bottom_left_corner_piece, immobilizer_piece)

  if bottom_right_corner_piece not in [-1,0] and is_opposite_color(bottom_right_corner_piece, immobilizer_piece):
    # print("Immobilizer Bottom Right: " + str(bottom_right_corner_piece) + ", " + str(PIECE_VALUES[str(bottom_right_corner_piece)]))
    score_boost += immobilizer_boost(bottom_right_corner_piece, immobilizer_piece)

  # Swap sign if player is WHITE piece to give positive boost
  if is_white_piece(immobilizer_piece): score_boost *= -1
  return score_boost

def pretty_print_state(state):
  '''
  Prints each row in a state on its own line.
  Used for debugging purposes.
  '''
  for row in state:
    print(row)

def immobilizerDebuggerSetup():
  global INITIAL
  INITIAL[7][0]=0
  INITIAL[4][0]=15
  INITIAL[1][0]=0
  INITIAL[3][0]=2

# staticEval(state). This function will perform a static evaluation of the given state. 
# The value returned should be high if the state is good for WHITE and low if the state is 
# good for BLACK. Although you may wish to extend the BC_state class to make staticEval a member of 
# that, it's not necessary, and we do need to be able to call your staticEval function directly, for example using

# import The_Roman_BC_Player as player
# staticResult = player.stateEval(some_state)   