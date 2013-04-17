import numpy as np
import sys

def main():
    N = int(sys.stdin.readline())
    calorie_book = []

    #store input in calorie_book, which is a list of tuples
    for line in sys.stdin:
        activity, calories = line.rstrip().split()
        calorie_book.append( (activity, int(calories)) )

    grand_dict = {}
    grand_dict[0] = [-1]

    """This is a dynamic programming algorithm
    grand_dict is a dictionary that stores ways to get 
    activities that sum up to a certain number. The keys
    are the number and the values are lists of activities"""

    for i in range(N):
        act, cals = calorie_book[i]
        
        for j in grand_dict.keys():
            old_path = grand_dict[j]
            new_path = old_path + [i]
            grand_dict[j + cals] = new_path
            
    #if you found a way to get activities to sum to 0, print them out
    if len(grand_dict[0]) > 1:
        for item in grand_dict[0][1:]:
            act, cal = calorie_book[item]
            print act

if __name__ == "__main__":
    main()
