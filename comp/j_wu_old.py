import numpy as np

import random as rand


def get_surrounding(field, row, col, value):
    """Finds how many mines are in surrounding squares of a certain coordinate"""
    count = 0
    # checks surrounding squares
    for i in range(row - 1, row + 2):
        for k in range(col - 1, col + 2):
            # checks if the current coordinate is on the field and is the value
            if 0 <= i < field.shape[0] and 0 <= k < field.shape[1] and field[i, k] == value:
                count += 1
    return count


def generate_num_field(field):
    """Generates an array of the number of surrounding mines"""
    num_field = np.zeros(field.shape, dtype=int)
    for i in range(field.shape[0]):
        for k in range(field.shape[1]):
            num_field[i, k] = get_surrounding(field, i, k, 1)
    return num_field


def generate_minefield(dimension, num_mines, starting):  # dimension and starting are [row, col], ADD STARTING
    """Generates an array where 0 = empty and 1 = bomb"""

    field = np.zeros(dimension, dtype=int)  # generates empty field
    # squares_left accounts for squares surrounding the starting point that must be mine free
    squares_left = int(dimension[0]*dimension[1]) - get_surrounding(field, starting[0], starting[1], 0)

    # places mines randomly, iterating through every square
    for row in range(dimension[0]):
        for col in range(dimension[1]):
            if num_mines == 0:  # when all mines have been placed
                break
            if abs(row - starting[0]) <= 1 and abs(col - starting[1]) <= 1:  # no mines surrounding the starting point
                pass
            elif rand.randint(1, squares_left) <= num_mines:  # num_mine/squares_left % chance of mine
                field[row, col] = 1
                num_mines -= 1
            squares_left -= 1
    return field


def generate_user_field(dimension):
    """Generates the field the user sees, ? = hidden squares, ! = flagged, 0-9 = num surrounding mines"""
    return np.array([["?" for i in range(dimension[1])] for k in range(dimension[0])])


def flood_reveal(user_field, num_field, row, col):
    """Reveals empty squares on player's choice row col by using recursive flood fill"""
    # if the square has already been revealed
    if user_field[row, col] != "?":
        return
    # if there are mines surrounding the square and it's not adjacent to an already revealed empty square
    elif num_field[row, col] != 0 and get_surrounding(user_field, row, col, "0") == 0:
        return
    else:
        # gets the number for surrounding mines from num_field
        user_field[row, col] = str(num_field[row, col])
    # if the coordinates are in bound, then recurse in 4 directions (up, down, left, right)
    if row != np.shape(user_field)[0] - 1:
        flood_reveal(user_field, num_field, row + 1, col)
    if row != 0:
        flood_reveal(user_field, num_field, row - 1, col)
    if col != np.shape(user_field)[1] - 1:
        flood_reveal(user_field, num_field, row, col + 1)
    if col != 0:
        flood_reveal(user_field, num_field, row, col - 1)
    return


def user_input_coords(string):
    """Converts user coordinate input from string to list"""
    return list(map(int, input(string).split()))


def print_array(array):
    """Prints 2d array without all the quotes and brackets"""
    # prints top x axis
    print("   ", end="")
    for i in range(array.shape[1]):
        if i < 10:  # accounts for how one/two digit numbers take up different spaces
            print("\033[94m" + str(i) + "\033[0m", end="  ")  # axis are blue :)
        else:
            print("\033[94m" + str(i) + "\033[0m", end=" ")
    print()
    # prints array and left y axis
    for i in range(array.shape[0]):
        if i < 10:  # accounts for how one/two digit numbers take up different spaces
            print("\033[94m" + str(i) + "\033[0m", end="  ")
        else:
            print("\033[94m" + str(i) + "\033[0m", end=" ")
        for k in array[i]:
            if k == "?":
                print("\033[91m" + k + "\033[0m", end="  ")
            elif k == "!":
                print("\033[93m" + k + "\033[0m", end="  ")
            elif k != "0":
                print("\033[32m" + k + "\033[0m", end="  ")
            else:
                print(k, end="  ")
        print()


def main():
    # set up all the variables
    difficulty = input("""Welcome to minesweeper, choose the difficulty (b for beginner, m for medium, h for hard).
Beginner is 10x10 with 10 mines, medium is 16x16 with 40 mines, hard is 30x16 with 99 mines.""")
    diff_list = [["b", "m", "h"], [[10, 10], [16, 16], [30, 16]], [10, 40, 99]]
    dimension = diff_list[1][diff_list[0].index(difficulty)]
    num_mines = diff_list[2][diff_list[0].index(difficulty)]
    flags_left = num_mines

    # creates the field the user sees with hidden spots
    user_field = generate_user_field(dimension)
    print_array(user_field)

    # gets the starting point
    starting = user_input_coords("Choose a starting point (eg. type 0 12 to get 1st row 13th column)")

    # fields
    minefield = generate_minefield(dimension, num_mines, starting)
    num_field = generate_num_field(minefield)

    flood_reveal(user_field, num_field, starting[0], starting[1])
    print_array(user_field)

    while True:
        choose_square = user_input_coords("Choose a square to flag or reveal")
        row = choose_square[0]
        col = choose_square[1]

        square_decision = input("Type f to flag, c to remove flag, or r to reveal")

        if np.count_nonzero(user_field == "?") + np.count_nonzero(user_field == "!") == num_mines:  # if you win
            user_field[user_field == "!"] = "*"
            user_field[user_field == "?"] = "*"
            print_array(user_field)
            print("Good job, you won!!")
            break

        if square_decision == "r":
            if minefield[row, col] == 1:  # if you reveal a mine, you're bad and you lost
                user_field[row, col] = "*"
                print_array(user_field)
                print("Oops you uncovered a mine, you're bad AND you lost, try again.")
                break

            elif num_field[row, col] > 0:  # if you reveal a square with surrounding mines, no flood_reveal
                user_field[row, col] = num_field[row, col]
                print_array(user_field)

            elif num_field[row, col] == 0:
                flood_reveal(user_field, num_field, row, col)
                print_array(user_field)

        elif square_decision == "f":
            user_field[row, col] = "!"
            print_array(user_field)
            flags_left -= 1
            print("Flags left:", flags_left)

        elif square_decision == "c":
            user_field[row, col] = "?"
            print_array(user_field)
            flags_left += 1
            print("Flags left:", flags_left)


main()
