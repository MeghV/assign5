from random import *

# Immobilized Pieces
# Black White move checker
# Finding best move

BLACK = 0
WHITE = 1

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
  hold = s[from_row][from_column]
  s[from_row][from_column] = 0
  s[to_row][to_column] = hold
  return s

# Checks that the horizontal path is clear.
def clear_path_horizontal(s, from_row, from_column, to_row, to_column):
  check_row = from_row
  while from_row != to_row:
    if from_row > to_row:
      check_row -= 1
    else:
      check_row += 1
    if s[check_row, from_column] != 0:
      return False
  return True

# Chceks that the vertical path is clear.
def clear_path_vertical(s, from_row, from_column, to_row, to_column):
  check_column = from_column
  while from_column != to_column:
    if from_column > to_column:
      check_column -= 1
    else:
      check_column += 1
    if s[from_row, check_column] != 0:
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
  if s[to_row][to_column] == 0 and (from_row != to_row and from_column != to_column):
    if s[from_row][from_column] in [12, 13]:
      if (abs(from_row - to_row) <= 1) and (abs(from_column - to_column) <= 1):
        return True
      return False
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
print (move_combinations)

OPERATORS = [Operator("Move piece at " + str(p) + ", " + str(q) + " to " + str(m) + ", " + str(n),
                      lambda s, p = p, q = q, m = m, n = n: can_move(s, p, q, m, n),
                      lambda s, p = p, q = q, m = m, n = n: move(s, p, q, m, n))
                      for (p, q, m, n) in move_combinations]

# Iterative Deepening to find the optimal board move.
def makeMove(currentState, currentRemark, timeLimit = 10000):
  LAST_MOVE = BC_state(currentState.board, currentState.whose_move)
  last_board = DEEP_COPY(currentState.board)

  player = currentState.whose_move

  def successors(state):
    S = state
    L = []
    for op in OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        L.append(new_state)
    return L

  first_moves = successors(last_board)

  def max_value(state, alpha, beta, depth):
    if depth > 4:
      return staticEval(state)
    v = -infinity
    for s in successors(state):
      v = max(v, min_value(s, alpha, beta, depth + 1))
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v

  def min_value(state, alpha, beta, depth):
    if depth > 4:
      return staticEval(state)
    v = -infinity
    for s in successors(state):
      v = min(v, max_value(s, alpha, beta, depth + 1))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v
  
  # new = DEEP_COPY(currentState.board)
  # OPEN = [new]
  # CLOSED = {}

  # while OPEN != []:
  #   S = OPEN[0]
  #   del OPEN[0]

  #   L = []
  #   for i in range(8):
  #     for j in range(8):
  #       if S[i][i] != 0:
  #         if can_move(S, i, j):
  #           for k in range(8):
  #             new_state = move(S, i, j, k)
  #             if not occurs_in(HASHCODE(new_state), CLOSED.keys()):
  #               L.append(new_state)

  #   for i in L:
  #     CLOSED[HASHCODE(i)] = S
  #     for j in range(len(OPEN)):
  #       if DEEP_EQUALS(i, OPEN[j]):
  #         del OPEN[j]; break

  #   OPEN = L + OPEN

  return [["", currentState], "RAWR! YOUR MOVE PUNY HUMAN!"]

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

def staticEval(state):
  # TODO
  return randint(0, 100)


def pretty_print_state(state):
  '''
  Prints each row in a state on its own line.
  Used for debugging purposes.
  '''
  for row in state:
    print(row)

# staticEval(state). This function will perform a static evaluation of the given state. 
# The value returned should be high if the state is good for WHITE and low if the state is 
# good for BLACK. Although you may wish to extend the BC_state class to make staticEval a member of 
# that, it's not necessary, and we do need to be able to call your staticEval function directly, for example using

# import The_Roman_BC_Player as player
# staticResult = player.stateEval(some_state)    
