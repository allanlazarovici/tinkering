import sys

INF = 10000

def main():
    """This is a breadth-first brute force search of all the possible sequences of moves.
    Each possible sequence is stored in all_paths. A path is a list of [state, action, state,
    action, ..., state, action]

    States are represented as tuples because we need the states to be hashable. This is because we
    use a set data structure to keep track of visited states"""

    N, k = map(int, sys.stdin.readline().split())
    initial_state = tuple( map(int, sys.stdin.readline().split()) )
    final_state = tuple( map(int, sys.stdin.readline().split()) )

    init_path = [initial_state]
    all_paths = [init_path]

    visited_states = set()
    visited_states.add(initial_state)

    while all_paths:
        popped_path = all_paths.pop(0)
        current_state = popped_path[-1]

        if current_state == final_state:
            solution = popped_path
            break

        for state, action in generate_moves(current_state, N, k).items():
            if state not in visited_states:
                visited_states.add(state)
                new_path = popped_path + [action,state]
                all_paths.append(new_path)

    display_solution(solution)

def generate_moves(cur_state, N, k):
    """Notes: 
    1. Everything is one-indexed
    2. A peg with no disks is implemented as containing a disk of size INF"""
    cur_state_list = list(cur_state)
    cur_state_list.insert(0,-1)

    min_on_peg = [-1] + [INF]*k

    poss_moves = {}

    for i in reversed(range(1,N+1)):
        min_on_peg[ cur_state_list[i] ] = i

    #Check all possible ways to move from peg i to peg j
    for i in range(1, k+1):
        for j in range(1, k+1):
            if i is not j and min_on_peg[i] > 0 and min_on_peg[i] < min_on_peg[j]:
                action = (i, j)
                new_state = list(cur_state_list)
                new_state[min_on_peg[i]] = j
                new_state = tuple(new_state[1:])
                poss_moves[new_state] = action

    return poss_moves

def display_solution(solution):
    actions = solution[1::2]
    
    print str(len(actions))

    for i in actions:
        print str(i[0]) + " " + str(i[1])
    

if __name__ == "__main__":
    main()
