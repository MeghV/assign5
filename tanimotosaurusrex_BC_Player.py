# Immobilized Pieces

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

def move(s, row, column, move_to):
  print("move")
  hold = s[row][column]
  s[row][column] = 0
  # Pawns
  if hold in [2, 3]:
    print ("Is Pawn")
    if clear_path_vertical(s, row, column, move_to, column):
      s[row][column] = 0
      s[move_to][column] = hold
    elif clear_path_horizontal(s, row, column, row, move_to):
      s[row][column] = 0
      s[row][move_to] = hold
  # Kings
  elif hold in [13, 14]:
    print ("Is King")
    if s[row + 1][column] == 0:
      s[row + 1][column] = hold
    elif s[row + 1][column + 1] == 0:
      s[row + 1][column + 1] = hold
    elif s[row + 1][column - 1] == 0:
      s[row + 1][column - 1] = hold
    elif s[row][column + 1] == 0:
      s[row][column + 1] = hold
    elif s[row][column - 1] == 0:
      s[row][column - 1] = hold
    elif s[row - 1][column] == 0:
      s[row - 1][column] = hold
    elif s[row - 1][column + 1] == 0:
      s[row - 1][column + 1] = hold
    elif s[row - 1][column - 1] == 0:
      s[row - 1][column - 1] = hold
  # All other pieces
  else:
    print ("else")
    if clear_path_vertical(s, row, column, move_to, column):
      s[move_to][column] = hold
      print ("a")
    elif clear_path_horizontal(s, row, column, row, move_to):
      s[row][move_to] = hold
      print ("b")
    print ("f")
    if row - move_to >= 0 and column - move_to >= 0:
      print ("c")
      if clear_path_diagonal(s, row, column, row - move_to, column - move_to):
        s[row - move_to][column - move_to] = hold
      print ("1")
    elif row + move_to < 8 and column - move_to >= 0:
      print ("l")
      if clear_path_diagonal(s, row, column, row + move_to, column - move_to):
        s[row + move_to, column - move_to] = hold
      print ("2")
    elif row - move_to >= 0 and column + move_to < 8:
      if clear_path_diagonal(s, row, column, row - move_to, column + move_to):
        s[r - move_to, column + move_to] = hold
      print ("3")
    elif row + move_to < 8 and column + move_to < 8:
      if clear_path_diagonal(s, row, column, row + move_to, column + move_to):
        s[r + move_to, column + move_to]
      print ("4")
    print ("end")
  print ("returning")
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
  while from_row != to_row and from_column != to_column:
    if from_row > to_row:
      check_row -= 1
    else:
      check_row += 1
    if from_column > to_column:
      check_column -= 1
    else:
      check_column += 1
    if s[check_row, check_column] != 0:
      return False
  return True

# Checks that there are empty spaces around the piece.
def can_move(s, row, column):
  print ("can_move")
  if row + 1 < 8 and s[row + 1][column] == 0:
    return True
  if column + 1 < 8 and s[row][column + 1] == 0:
    return True
  if column - 1 >= 0 and s[row][column - 1] == 0:
    return True
  if row - 1 >= 0 and s[row - 1][column] == 0:
    return True
  if s[row][column] not in [2, 3]:
    if row + 1 < 8 and column + 1 < 8 and s[row + 1][column + 1] == 0:
      return True
    if row - 1 >= 0 and column + 1 < 8 and s[row - 1][column + 1] == 0:
      return True
    if row + 1 < 8 and column - 1 >= 0 and s[row + 1][column - 1] == 0:
      return True
    if row - 1 >= 0 and column - 1 >= 0 and s[row - 1][column - 1] == 0:
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

# Iterative Deepening to find the optimal board move.
def makeMove(currentState, currentRemark, timeLimit = 10000):
  LAST_MOVE = BC_state(currentState.board, currentState.whose_move)
  new = DEEP_COPY(currentState.board)
  OPEN = [new]
  CLOSED = {}

  while OPEN != []:
    S = OPEN[0]
    del OPEN[0]

    L = []
    for i in range(8):
      for j in range(8):
        if S[i][i] != 0:
          if can_move(S, i, j):
            for k in range(8):
              new_state = move(S, i, j, k)
              if not occurs_in(HASHCODE(new_state), CLOSED.keys()):
                L.append(new_state)

    for i in L:
      CLOSED[HASHCODE(i)] = S
      for j in range(len(OPEN)):
        if DEEP_EQUALS(i, OPEN[j]):
          del OPEN[j]; break

    OPEN = OPEN + L


  return [["", currentState], "RAWR! YOUR MOVE PUNY HUMAN!"]

# staticEval(state). This function will perform a static evaluation of the given state. 
# The value returned should be high if the state is good for WHITE and low if the state is 
# good for BLACK. Although you may wish to extend the BC_state class to make staticEval a member of 
# that, it's not necessary, and we do need to be able to call your staticEval function directly, for example using

# import The_Roman_BC_Player as player
# staticResult = player.stateEval(some_state)    
