from random import *

BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

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

INITIAL_UPDATE = parse('''
c l i w k i l f
p p p p p p p -
- - - - - - - p
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

# makeMove(currentState, currentRemark, timeLimit=10000). This is probably your most important function. 
# It should return a list of the form [[move, newState], newRemark]. The move is a data item 
# describing the chosen move, and you may choose to return the empty string for this "". 
# (It is included for compatibility with possible future versions of this assignment.) 
# The newState is the result of making the move from the given currentState. It must be a 
# complete state and not just a board. The currentRemark argument is a string representing a remark 
# from the opponent on its last move. (This may be ignored, and it's a placeholder for possible use 
#   in future versions of this assignment.) The timeLimit represents the number of milliseconds available for computing and returning the move.
# The newRemark to be returned must be a string. During a game, the strings from your agent and 
# its opponent comprise a dialog. (However, you may simply return a fixed string, such as "Your move!" For extra credit, you may make this more elaborate and context-sensitive, commenting on the current state or the direction in which the game seems to be heading.)

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
# { evaluation_value: 0, ply: 0}
# "evaluation_value" is the previously calculated static evaluation 
# function value and "ply" is the ply at which the value was
# calculated. 
PREVIOUS_STATES = {}


# def init_zobrist_table():
#   global ZOBRIST_NUM_TABLE
#   for i in range(PIECES):
#     for j in range(POSITIONS):
#       ZOBRIST_NUM_TABLE[i][j] = randint(0, 9223372036854775807)

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
        
def store_state_value(zobrist_hash, evaluation_value, ply=0):
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
       "ply": ply}

def get_state_value(zobrist_hash):
  ''' 
  Returns the static evaluation value of a previously encountered
  state. If the state doesn't exist, a value of -1 is returned.
  '''
  if zobrist_hash in PREVIOUS_STATES:
    return PREVIOUS_STATES[zobrist_hash]
  return -1

def staticEvalBasic(state):
  state_zobrist_hash = calculate_zobrist_hash(state)
  state_eval_value = get_state_value(state_zobrist_hash)
  if state_eval_value == -1:
    # if the static eval value hasn't been calculated before
    state_eval_value = 0
    store_state_value(state_zobrist_hash, state_eval_value)
  # else return the previously calculated static eval value
  return state_eval_value


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
