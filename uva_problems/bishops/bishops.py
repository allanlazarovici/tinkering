import sys

def main():
    """I will comment this code more thoroughly at some point in the future. In the 
    meantime, it should be fairly straightforward to see what is going on if you 
    load this file into a REPL

    The key idea is that we consider the white and black squares separately. This is because 
    a bishop on a white square cannot attack any bishop on a black square"""

    n, k = map(int, sys.stdin.readline().split())
    print str( k_bishops(n, k) )

def k_bishops(n, k):
    if n == 1:
        return 1 if k <= 1 else 0
    elif k > 2*(n-1):
        return 0
    else:
        possible_pairs, max_val, min_val = gen_possible_pairs(n, k)
        first_board, second_board = get_valid_spots(n)

        fb_dict, sb_dict = {}, {}

        for i in range(min_val, max_val + 1):
            fb_dict[i] = find_num_arrangements(first_board, i)
            sb_dict[i] = fb_dict[i] if n %2 == 0 else find_num_arrangements(second_board, i)

        return sum( [fb_dict[i]*sb_dict[j] for i,j in set(possible_pairs)])


def find_num_arrangements(board, i):
    total = [0]
    find_num_arrangements_recursive(board, i, [], total)
    return total[0]


def find_num_arrangements_recursive(board, pieces_left, piece_positions, total):
    if pieces_left is 0:
        total[0] = total[0] + 1
    else:
        remaining_rows_to_fill = len(board) - len(piece_positions) - 1
        
        #should we allow an empty row?
        if pieces_left <= remaining_rows_to_fill:
            find_num_arrangements_recursive(board, pieces_left, piece_positions + [0], total)

        candidates = generate_candidates(board, piece_positions)
        for j in candidates:
            find_num_arrangements_recursive(board, pieces_left-1, piece_positions + [j], total)


def generate_candidates(board, piece_positions):
    row = len(piece_positions)
    return list( set(board[row]) - set(piece_positions) )


def gen_possible_pairs(n, k):
    max_val = min(n-1, k)
    min_val = k - max_val

    list_of_pairs = [ (max_val - i, min_val + i) for i in range(0,k+1) if max_val - i >= min_val + i]
    reversed_pairs = map(lambda x: x[::-1], list_of_pairs)

    return [list_of_pairs + reversed_pairs, max_val, min_val]


def get_valid_spots(n):
    first, second = gen_sequences(n)

    f_list = map(lambda x: gen_nums(n)[:x], first)
    s_list = map(lambda x: gen_nums(n-1)[:x], second)

    return [f_list, s_list] if n % 2 == 1 else [f_list, f_list]


def gen_sequences(n):
    arith_seq = [1 + 2*(i-1) for i in range(1,(n-1)/2 + 2)]

    main_sequence = arith_seq + arith_seq[(n/2 - 1)::-1]
    second_sequence = get_avgs(main_sequence)

    return [main_sequence, second_sequence]


def get_avgs(seq):
    return [ (seq[i+1] + seq[i])/2 for i in range(len(seq)-1)]

        
def gen_nums(n):
    first_num = (n+1)/2

    pairs = [ [first_num - i, first_num + 1 + i] for i in range(n) if first_num - i >= 1]
    flattened_pairs = sum(pairs, [])

    return flattened_pairs[:n]

if __name__ == "__main__":
    main()
