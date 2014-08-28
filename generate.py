import math
import sys

class PuzzleState(object):
    """
    Eight-Puzzle state object
    """
    
    def __init__(self, board=None):
        """
        Initialize with board layout, otherwise provide default 3x3 board
        """
        self.board = board or [1,2,3,4,5,6,7,8,0]
        self.dimension = int(math.sqrt(len(self.board)))
    
    def __repr__(self):
        """
        String representation useable by Graphviz dot file
        """
        return "S_{0}".format("_".join(map(str, self.board)))
    
    def expand(self):
        """
        Expands a list of all possible moves from the current state
        """
        loc = self.locate()
        row, col = self.location_to_coordinates(loc)
        
        moves = []
        
        if row > 0:
            moves.append(('up', self.move(row - 1, col), self))
        
        if col < self.dimension-1:
            moves.append(('right', self.move(row, col + 1), self))
        
        if row < self.dimension-1:
            moves.append(('down', self.move(row + 1, col), self))
        
        if col > 0:
            moves.append(('left', self.move(row, col -1), self))
        
        return moves
    
    def locate(self):
        """
        Provides the raw numerical index of the empty piece (0)
        """
        return self.board.index(0)
        
    def location_to_coordinates(self, location):
        """
        Converts raw numerical index to (row, col) cooridnate
        """
        return (
            int(math.floor(location / self.dimension)),  # row
            int(location % self.dimension)               # col
        )
    
    def coordinates_to_location(self, row, col):
        """
        Converts (row, col) coordinate to raw numerical index
        """
        return (row * self.dimension) + col
    
    def move(self, to_row, to_col):
        """
        Produces a new state by moving the empty piece (0) to the new row, col
        """
        loc1 = self.locate()
        loc2 = self.coordinates_to_location(to_row, to_col)
        
        #clone board
        board = self.board[:]
        
        tmp = board[loc1]
        board[loc1] = board[loc2]
        board[loc2] = tmp
        
        return PuzzleState(board)

def chunks(l, n):
    """
    Chunk list l into n pieces
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def define_state(state):
    """
    Produce Graphviz dot-file node definition
    """
    label = []
    for chunk in chunks(state.board, state.dimension):
        label.append("{{{0}}}".format("|".join(map(str, chunk))))
    return "{1} [shape=record,label=\"{0}\"];".format("|".join(label), repr(state))


def draw_move(start, end, direction):
    """
    Produce Graphviz dot-file edge definition
    """
    return "{0} -> {1};".format(repr(start), repr(end))


# Initialize de-duplication lookup tables
found = {}
moves = {}

# Initialize Puzzle State
start = PuzzleState()

# Print opening stanza of Graphviz dot-file
print "digraph EightPuzzle {"

i = 0
# Initialize the BFS stack
stack = [('init', start, None)]
while len(stack) > 0:
    # Obtain move from stack
    move = stack.pop(0)
    direction, state, parent = move
    
    if repr(state) not in found:
        # Print definition if we have not seen this state before
        print define_state(state)
        found[repr(state)] = True
        
        # As we have not seen this state before, refill the stack by expanding 
        # the current state
        stack = stack + state.expand()
        
        # Display a progress indicator
        print >> sys.stderr, i
        i = i + 1
    
    if parent is not None:
        # If this is a valid move (e.g. has a parent)...
        drawn_move = draw_move(parent, state, direction)
        
        move_hash1 = repr(parent) + repr(state)
        move_hash2 = repr(state) + repr(parent)
        
        if move_hash1 not in moves and move_hash2 not in moves:
            # Print move if we have not seen it (in any direction)
            print drawn_move
            moves[move_hash1] = True

# Print closing stanza of Graphviz dot-file
print "}"


print >> sys.stderr, ""
print >> sys.stderr, "Finished!"
