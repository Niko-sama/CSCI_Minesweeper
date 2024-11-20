'''
Notes

made it so the first cell choice reveals a larger portion of the board (at least one '0' cell)
    limits minimum board size to 3 by 3 so first input does not immediately win
    limits maximum mines to account for the initial (at least) 3 by 3 area
time is now displayed as minutes and seconds
added a reccomendation for number of mines based on an extrapolated formula for the mine density of common minesweeper boards
'''

import random
import time

# Generates values for each cell on the board
def generate_board(width, height, mines):
    board = [[' ' for x in range(width)] for x in range(height)]
    mine_positions = set()

    # Initial user input will avoid mines
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

    while len(mine_positions) < mines:
        row_mine = random.randint(0, height - 1)
        col_mine = random.randint(0, width - 1)
        if ((row_mine, col_mine) not in mine_positions) and not ((row_mine in range(row - 1, row + 2)) and (col_mine in range(col - 1, col + 2))):
            mine_positions.add((row_mine, col_mine))
            board[row_mine][col_mine] = '•'

    return board, mine_positions, row, col

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
        print(f'{row_num} — ' + ''.join(f'[{cell}]' for cell in board[x]) + f' — {row_num}')
    
    # Displays bottom row of numbers
    print(' ' * 5 + ' | ' * width)
    if width <= 9:
        print(' ' * 6 + '  '.join(str(num) for num in range(1, width + 1)))
    else:
        print(' ' * 6 + '  '.join(str(num) for num in range(1, 10)), ' '.join(str(num) for num in range(10, width + 1)))

# Find the number of mines around each cell
def count_mines(board, row, col):
    mine_count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if (r in range(len(board))) and (c in range(len(board[0]))) and (board[r][c] == '•'):
                mine_count += 1

    return mine_count

# Reveal the value of a cell and surrounding 0s (if any)
def show_cell(board, display, row, col):
    if display[row][col] != ' ':
        return
    
    mine_count = count_mines(board, row, col)
    
    if mine_count == 0:
        display[row][col] = '0'
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r in range(len(board))) and (c in range(len(board[0]))) and (display[r][c] == ' '):
                    show_cell(board, display, r, c)
    else:
        display[row][col] = str(mine_count)

# Checks to see if user has won
def win(display, mine_positions):
    for r in range(len(display)):
        for c in range(len(display[0])):
            if (display[r][c] == ' ') and ((r, c) not in mine_positions):
                return False
    return True

# Prints the time elapsed from when the board is generated to when the code is done running
def measure_time(start_time):
    if (time.time() - start_time) >= 60:
        print(f'Your time: {int((time.time() - start_time) // 60)}min {((time.time() - start_time) % 60):.2f}s')
    else:
        print(f'Your time: {(time.time() - start_time):.2f}s')

# Organizes variables and functions to play the game
def play():
    # Define the number of rows, columns, and mines with input. Denies invalid inputs
    '''
    width = 10
    height = 10
    mines = 5
    '''
    
    while True:
        try:
            width = int(input('Number of columns (4-99): '))
            while width not in range(4, 100):
                print('Not a valid number')
                width = int(input('Number of columns (4-99): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break

    while True:
        try:
            height = int(input('Number of rows (4-99): '))
            while height not in range(4, 100):
                print('Not a valid number')
                height = int(input('Number of rows (4-99): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break

    while True:
        try:
            mines = int(input(f'Number of mines (1-{width * height - 9}, {round((0.0002 * (width * height) ** 2 + 0.0938 * (width * height) + 0.8937))} recommended): '))
            while mines not in range(1, width * height - 8):
                print('Not a valid number')
                mines = int(input(f'Number of mines (1-{width * height - 9}, {round((0.0002 * (width * height) ** 2 + 0.0938 * (width * height) + 0.8937))} reccommended): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break
    
    # Prepares the board and places mines randomly, the first row and column inputs will reveal a chunk of the board instead of having a chance to lose immediately
    print('-' * 40)
    display = [[' ' for x in range(width)] for x in range(height)]
    display_board(display, width, height)
    start_time = time.time()
    
    board, mine_positions, row, col = generate_board(width, height, mines) #
    show_cell(board, display, row, col)
    print('-' * 40)
    display_board(display, width, height)
    
    # Takes inputs and displays new board
    while True:
        # Checks if user has won
        if win(display, mine_positions):
            print(' -----')
            print('| WIN |')
            print(' -----')
            break

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

        # Ends the game if user hits a mine
        if board[row][col] == '•':
            for r in range(0, len(board)):
                for c in range(0, len(board[0])):
                    if board[r][c] == ' ':
                        board[r][c] = display[r][c]
            print('-' * 40)
            display_board(board, width, height)
            print(' ------')
            print('| LOSE |')
            print(' ------')
            break
        
        # Separates board states in the terminal
        print('-' * 40)

        # Generates a board updated with the next state
        show_cell(board, display, row, col)
        display_board(display, width, height)

    # Tells the user how long the board took to complete
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