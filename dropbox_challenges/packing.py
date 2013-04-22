import sys
import pprint

class Tree(object):
    def __init__(self, data, data_cum):
        self.left = None
        self.right = None
        self.data = data
        self.data_cum = data_cum

def main():
    """ This is a heuristic algorithm
    At the beginning, shapes are sorted in descending order based on area.

    The first shape is placed in the bottom left hand corner.

    For every other shape, we search for possible insertion sports. A valid insertion
    spot is a spot that is directly above or to the left of an existing shape

    We use a tree data structure to keep track of the board layout. We also use board_occupancies,
    which is a list of lists. Each list contains four numbers, the bottom left and top right
    corners of each retangle on the board"""

    N = int(sys.stdin.readline())
    shapes = []

    for line in sys.stdin:
        l, w = line.rstrip().split()
        shapes.append( [int(l), int(w)] )

    #shapes are sorted in descending order based on area
    shapes = sorted(shapes, key = lambda x: x[0]*x[1], reverse=True)

    first_shape = shapes.pop(0)

    board_tree = Tree(first_shape, [0,0])
    board_occupancies = [ [0, 0] + first_shape]

    while shapes:
        cur_shape = shapes.pop(0)
        
        max_x = max(board_occupancies, key= lambda x: x[2])[2]
        max_y = max(board_occupancies, key= lambda x: x[3])[3]
        max_vals = [max_x, max_y]

        all_paths = []
        current_path = []
        generate_all_insertion_paths(board_tree, board_occupancies, cur_shape, max_vals, current_path, all_paths)

        min_area, shape, best_path = min(all_paths, key = lambda x: x[0])
        insert_shape(board_tree, board_occupancies, shape, best_path)

    print str(min_area)

def generate_all_insertion_paths(board_tree, board_occupancies, shape, max_vals, current_path, all_paths):
    """We check for all possible insertion spots for a given shape

    I realize that the two if-else statements are somewhat similar, and should be generalized somehow"""


    path = list(current_path) + [0]
    if board_tree.left is None:
        bottom_left_corner = list(board_tree.data_cum)
        bottom_left_corner[0] = bottom_left_corner[0] + board_tree.data[0]
        update_all_paths(board_occupancies, shape, bottom_left_corner, max_vals, path, all_paths)
        update_all_paths(board_occupancies, shape[::-1], bottom_left_corner, max_vals, path, all_paths)
    else:
        generate_all_insertion_paths(board_tree.left, board_occupancies, shape, max_vals, path, all_paths)

    path = list(current_path) + [1]
    if board_tree.right is None:
        bottom_left_corner = list(board_tree.data_cum)
        bottom_left_corner[1] = bottom_left_corner[1] + board_tree.data[1]
        update_all_paths(board_occupancies, shape, bottom_left_corner, max_vals, path, all_paths)
        update_all_paths(board_occupancies, shape[::-1], bottom_left_corner, max_vals, path, all_paths)
    else:
        generate_all_insertion_paths(board_tree.right, board_occupancies, shape, max_vals, path, all_paths)

def update_all_paths(board_occupancies, shape, bottom_left, max_vals, path, all_paths):
    """Given a suggested insertion spot and orientation, we update all_paths

    In this method, we see the only real use for board_occupancies. We use it to make sure that
    a proposed insertion does not intersect any current squares"""
    
    max_values = list(max_vals)

    top_right_corner = [x+y for x,y in zip(shape, bottom_left)]

    for i in range(2):
        max_values[i] = max_vals[i] if max_vals[i] > top_right_corner[i] else top_right_corner[i]

    area = max_values[0]*max_values[1]

    current_square = bottom_left + top_right_corner
    intersections = map( lambda x: do_squares_intersect(current_square, x), board_occupancies)
    no_intersections = not any(intersections)

    if no_intersections:
        all_paths.append([area, shape, path])
    
def do_squares_intersect(square1, square2):
    """A simple method for checking whether two squares intersect"""
    s1_x1, s1_y1, s1_x2, s1_y2 = square1
    s2_x1, s2_y1, s2_x2, s2_y2 = square2

    dont_intersect = s1_y2 <= s2_y1 or s2_y2 <= s1_y1 or s1_x2 <= s2_x1 or s2_x2 <= s1_x1

    return not dont_intersect

def insert_shape(board_tree, board_occupancies, shape, path):
    """This method only gets called once the optimal insertion spot and orientation has been determined

    This method updates the tree data struture and the board_occupancies list of lists"""

    new_bottom_left_corner = list(board_tree.data_cum)

    move = path.pop(0)
    new_bottom_left_corner[move] = new_bottom_left_corner[move] + board_tree.data[move]

    if len(path) is 0:
        top_right_corner = [x+y for x,y in zip(new_bottom_left_corner, shape)]
        board_occupancies.append(new_bottom_left_corner + top_right_corner)
        if move is 0:
            board_tree.left = Tree(shape, new_bottom_left_corner)
        else:
            board_tree.right = Tree(shape, new_bottom_left_corner)
        
    else:
        next_tree = board_tree.left if move is 0 else board_tree.right
        insert_shape(next_tree, board_occupancies, shape, path)


if __name__ == "__main__":
    main()

"""
board_occupancies = [ [0,0,8,8] ]
board_tree = Tree( [8, 8], [0, 0] )

board_tree.left = Tree( [3,4], [8,0])

current_path = []
all_paths = []
shape = [3,4]
max_vals = [11,8]

#update_all_paths(board_occupancies, [1,2], [4,0], [0, 0], [], [])

board_occupancies = [[0,0,4,3]]
board_tree = Tree( [4,3], [0,0] )

insert_shape(board_tree, board_occupancies, [1,2], [0])
insert_shape(board_tree, board_occupancies, [2,2], [1])
insert_shape(board_tree, board_occupancies, [1,8], [0,1])
"""

