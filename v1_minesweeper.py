'''
Notes

generates a display board
'''

import random


col = 10
row = 10
mines = 10


def display_board(col, row):
    # Displays the top of the board with column numbers
    if col <= 9:
        print(' ' * 6 + '  '.join(str(num) for num in range(1, col + 1)))
    else:
        print(' ' * 6 + '  '.join(str(num) for num in range(1, 10)), ' '.join(str(num) for num in range(10, col + 1)))
    print(' ' * 5 + ' | ' * col)
    
    # Displays the row numbers and cells
    for x in range(row):
        row_num = (' ' if x + 1 < 10 else '') + f'{x + 1}'
        print(f'{row_num} — ' + '[ ]' * col + '')

def play():
    # Define the number of rows, columns, and mines with input
    '''
    col = int(input('Number of columns (1-99): '))
    while col not in range(1, 100):
        print('Not a valid number')
        col = int(input('Number of columns (1-99): '))
    row = int(input('Number of rows (1-99): '))
    while row not in range(1, 100):
        print('Not a valid number')
        row = int(input('Number of rows (1-99): '))
    mines = int(input(f'Number of mines (1-{col * row}): '))
    while mines not in range(1, col * row + 1):
        print('Not a valid number')
        mines = int(input(f'Number of mines (1-{col * row}): '))
    '''

    display_board(col, row)


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