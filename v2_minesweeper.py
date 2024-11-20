'''
Notes

player can now make inputs for the selected cell
randomly generates a hidden board for all mine locations
each display cell is defined as a variable, rather than as a string ' '
added a function to count mines in a 3 by 3 area around the selected cell
function to reveal the value of a selected cell and neighboring cells if a '0' is revealed
time it takes the player to finish is measured (cannot currently win or lose)
'''

import random
import time

# Generates values for each cell on the board
def generate_board(width, height, mines):
    board = [[' ' for x in range(width)] for x in range(height)]
    mine_positions = set()

    while len(mine_positions) < mines:
        row = random.randint(0, height - 1)
        col = random.randint(0, width - 1)
        if (row, col) not in mine_positions:
            mine_positions.add((row, col))
            board[row][col] = '•'

    return board, mine_positions

# Displays the state of the board
def display_board(board, width, height):
    # Displays the top of the board with column numbers
    if width <= 9:
        print(' ' * 6 + '  '.join(str(num) for num in range(1, width + 1)))
    else:
        print(' ' * 6 + '  '.join(str(num) for num in range(1, 10)), ' '.join(str(num) for num in range(10, width + 1)))
    print(' ' * 5 + ' | ' * width)

    # Displays the row numbers and cells
    for x in range(height):
        row_num = (' ' if x + 1 < 10 else '') + f'{x + 1}'
        print(f'{row_num} — ' + ''.join(f'[{cell}]' for cell in board[x]))

# Find the number of mines around each cell
def count_mines(board, col, row):
    mine_count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if (r in range(0, len(board))) and (c in range(0, len(board[0]))) and (board[r][c] == '•'):
                mine_count += 1

    return mine_count

# Reveal the value of a cell
def show_cell(board, display, row, col):
    if display[row, col] != ' ':
        return
    
    mine_count = count_mines(board, row, col)
    if mine_count == 0:
        display[row][col] = '0'
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r in range(0, len(board))) and (c in range(0, len(board[0]))) and (display[r][c] == ' '):
                    show_cell(board, display, row, col)
    else:
        display[row, col] = mine_count

# Prints the time elapsed from when the board is generated to when the code is done running
def measure_time(start_time):
    print(f'Your time: {(time.time() - start_time):.2f}s')

# Organizes variables and functions to play the game
def play():
    # Define the number of rows, columns, and mines with input. Denies invalid inputs
    '''
    width = 10
    height = 10
    mines = 10
    '''

    while True:
        try:
            width = int(input('Number of columns (1-99): '))
            while width not in range(1, 100):
                print('Not a valid number')
                width = int(input('Number of columns (1-99): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break

    while True:
        try:
            height = int(input('Number of rows (1-99): '))
            while height not in range(1, 100):
                print('Not a valid number')
                height = int(input('Number of rows (1-99): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break

    while True:
        try:
            mines = int(input(f'Number of mines (1-{width * height}): '))
            while mines not in range(1, width * height + 1):
                print('Not a valid number')
                mines = int(input(f'Number of mines (1-{width * height}): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break

    # Prepares the board and places mines randomly
    board, mine_positions = generate_board(width, height, mines)
    display = [[' ' for x in range(width)] for x in range(height)]

    display_board(display, width, height)
    start_time = time.time()

    # Prompts the user for a row and column to select
    while True:
        try:
            row = int(input('Enter the row: '))
            while row not in range(1, height + 1):
                print('Invalid row')
                row = int(input('Enter the row: '))
        except ValueError:
            print('Invalid row')
        else:
            row -= 1
            break

    while True:
        try:
            col = int(input('Enter the column: '))
            while col not in range(1, width + 1):
                print('Invalid column')
                col = int(input('Enter the column: '))
        except ValueError:
            print('Invalid column')
        else:
            col -= 1
            break
    
    

    mine_count = count_mines(board, col, row)
    print(mine_count)
    measure_time(start_time)


play()

'''
      1  2  3  4  5  6  7  8  9
      |  |  |  |  |  |  |  |  |
 1 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 2 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 3 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 4 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 5 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 6 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 7 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 8 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
 9 — [ ][ ][ ][ ][ ][ ][ ][ ][ ]
'''