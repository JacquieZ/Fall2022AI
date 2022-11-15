#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import numpy as np

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def variable_selection(board):
    min_legal_value = 9
    candidates_result = []
    position_result = {}
    for key in board.keys():
        list_candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        legal_value = 9

        # variable needs to be filled with
        if board[key] == 0:
            positions_list = []
            row_num = key[0]
            col_num = key[1]

            # find positions in the same row as board[key]
            for col in COL:
                positions_list.append(row_num + col)

            # find positions in the same column as board[key]
            for row in ROW:
                positions_list.append(row + col_num)

            # find positions in the same 3x3 box as board[key]

            # find box index
            # the box with box_row = 0, box_col = 0 is the 3x3 box on the left upper corner
            # i.e the box with positions: A1,A2,A3,B1,B2,B3,C1,C2,C3
            box_row = ROW.index(row_num) // 3
            box_col = COL.index(col_num) // 3
            for i in range(3):
                for j in range(3):
                    # in 3x3 box, append from left to right, up to bottom
                    positions_list.append(ROW[i+box_row * 3] + COL[j+box_col * 3])

            # all positions that will be checking if board[key] is selected
            positions = list(set(positions_list))

            # checking in every position
            for i in range(len(positions)):
                # if the number on that position is not 0, this means board[key] cannot be filled with that number
                # i.e. candidates-1
                if board[positions[i]] in list_candidates:
                    list_candidates.remove(board[positions[i]])
                    legal_value -= 1

                # to find the board[key] with minimum number of candidates
                if legal_value < min_legal_value:
                    min_legal_value = legal_value
                    position = row_num + col_num
                    candidates_result = list_candidates
                    position_result = positions

    # return: 1. the position of the variable that needs to be filled with number
    #         2. the list candidates to that variable
    #         3. the list of positions on the board relate to that variable
    return position, candidates_result, position_result


def forward_checking(board, position):
    # much same as above
    list_candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if board[position] == 0:
        positions_list = []
        row_num = position[0]
        col_num = position[1]
        for col in COL:
            positions_list.append(row_num + col)
        for row in ROW:
            positions_list.append(row + col_num)

        box_row = ROW.index(row_num) // 3
        box_col = COL.index(col_num) // 3
        for i in range(3):
            for j in range(3):
                positions_list.append(ROW[i+box_row * 3] + COL[j+box_col * 3])

        positions = list(set(positions_list))

        for i in range(len(positions)):
            if board[positions[i]] in list_candidates:
                list_candidates.remove(board[positions[i]])

    # return the number of candidates the variable has
    return len(list_candidates)


def backtracking(board):
    """Takes a board and returns solved board."""
    # the board is complete
    if 0 not in list(board.values()):
        return board

    # variable_position: the position of the variable that needs to be filled with number
    # domain_values: the list candidates to that variable
    # positions: the list of positions on the board relate to that variable
    variable_position, domain_values, positions = variable_selection(board)

    for i in domain_values:
        # assign candidate number to that variable_position
        board[variable_position] = i
        forward_result = True

        # check whether related unassigned positions has candidates to pick when board[variable_position] = i
        for position in positions:
            if board[position] == 0:
                candidate_domain_values = forward_checking(board, position)

                # no candidates -> false
                if candidate_domain_values == 0:
                    forward_result = False

        if forward_result:
            backward_result = backtracking(board)
            if backward_result:
                return backward_result

        # board[variable_position] = i is not correct
        # turn that position back to unassigned
        board[variable_position] = 0

    return False


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        num_solved = 0
        time_list = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()

            if solved_board:
                num_solved += 1
            run_time = end_time - start_time
            time_list.append(run_time)

            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")

        mean_time = np.mean(time_list)
        variance = np.var(time_list)
        std = np.std(time_list)
        maximum = max(time_list)
        minimum = min(time_list)
        print("Number of sudoku solved is " + str(num_solved))
        print("Running Time Statistics")
        print("Mean: " + str(mean_time))
        print("Max: " + str(maximum))
        print("Min: " + str(minimum))
        print("Variance: " + str(variance))
        print("Standard Deviation: " + str(std))
