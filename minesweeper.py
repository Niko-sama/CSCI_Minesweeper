'''
Notes

To do:
    add print function to track number of flagged mines
    limit the board area / minimum mines relative to board area to not get a recursion error
    (maybe) try to prevent situations where a cell selection being a mine is chance
'''

import random
import time
import pygame
pygame.init()


# Measures the time elapsed from when the board is generated to when the code is done running
# Returns elapsed time in (min, sec)
def measure_time(start_time):
    return int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)


# Terminal-based functions

# Find the number of mines around each cell
# Returns mine count
def count_mines_terminal(board, row, col):
    mine_count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if (r in range(len(board))) and (c in range(len(board[0]))) and (board[r][c] == '•'):
                mine_count += 1

    return mine_count

# Generates values for each cell on the board, the first terminal inputs are present in this function to place mines around the first cell
# Return board, mine positions, and initial row and col selections
def generate_terminal_board(width, height, mines):
    board = [[' ' for x in range(width)] for x in range(height)]
    mine_positions = set()

    # Initial user input will avoid mines
    while True:
            try:
                print()
                row = int(input('Enter the row: '))
                if int(row) in range(1, height + 1):
                    row = int(row)
                else:
                    print('Invalid row (not in range)')
                    continue
            except ValueError:
                print('Invalid row (not an integer)')
            else:
                row -= 1
                break
    
    while True:
            try:
                col = int(input('Enter the column: '))
                if int(col) in range(1, width + 1):
                    col = int(col)
                else:
                    print('Invalid row (not in range)')
                    continue
            except ValueError:
                print('Invalid column (not an integer)')
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
# Prints board state to the terminal
def display_terminal_board(board, width, height):
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

# Reveal the value of a cell and surrounding 0s (if any)
# Updates display board
def show_cell(board, display, row, col, flag):
    if (display[row][col] != ' ') and (display[row][col] != '*'):
        return
    
    mine_count = count_mines_terminal(board, row, col)
    
    if flag == 1:
        if display[row][col] == ' ':
            display[row][col] = '*'
        elif display[row][col] == '*':
            display[row][col] = ' '
    elif mine_count == 0:
        display[row][col] = '0'
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r in range(len(board))) and (c in range(len(board[0]))) and (display[r][c] == ' ' or display[r][c] == '*'):
                    show_cell(board, display, r, c, flag)
    elif display[row][col] == ' ':
        display[row][col] = str(mine_count)

# Checks to see if user has won
# Returns bool true if display board has all non-mine positions revealed
def check_win(display, mine_positions):
    for r in range(len(display)):
        for c in range(len(display[0])):
            if (display[r][c] == ' ') and ((r, c) not in mine_positions):
                return False
    return True

# Organizes variables and functions to play the game with text
# Runs game for the terminal
def terminal_play():
    # Define the number of rows, columns, and mines with input. Denies invalid inputs
    '''
    width = 10
    height = 10
    mines = 5
    '''
    flag = 0

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
            mines = int(input(f'Number of mines (1-{width * height - 9}, {round((width * height) * .181)} recommended): '))
            while mines not in range(1, width * height - 8):
                print('Not a valid number')
                mines = int(input(f'Number of mines (1-{width * height - 9}, {round((width * height) * .181)} reccommended): '))
        except ValueError:
            print('Invalid input, type an integer')
        else:
            break
    
    # Prepares the board and places mines randomly, the first row and column inputs will reveal a chunk of the board instead of having a chance to lose immediately
    print('-' * (width * 3 + 10))
    display = [[' ' for x in range(width)] for x in range(height)]
    display_terminal_board(display, width, height)
    start_time = time.time()
    
    board, mine_positions, row, col = generate_terminal_board(width, height, mines)
    show_cell(board, display, row, col, flag)
    print('-' * (width * 3 + 10))
    display_terminal_board(display, width, height)
    
    # Takes inputs and displays new board
    while True:
        # Checks if user has won
        if check_win(display, mine_positions):
            print(' -----')
            print('| WIN |')
            print(' -----')
            break

        # Prompts the user for a row and column to select
        while True:
            try:
                print()
                if flag == 1:
                    print('Flagging: Yes')
                else:
                    print('Flagging: No')
                # Checks if the user wants to flag or not
                # An input that results in an error will retry the code
                row = input('Enter the row (type "*" to toggle flag): ')
                if row == '*':
                    if not flag:
                        flag = 1
                    else:
                        flag = 0
                    continue
                elif int(row) in range(1, height + 1):
                    row = int(row)
                else:
                    print('Invalid row (not in range)')
                    continue
            except ValueError:
                print('Invalid row (not an integer)')
            else:
                row -= 1
                break
        
        while True:
            try:
                col = int(input('Enter the column: '))
                if int(col) in range(1, width + 1):
                    col = int(col)
                else:
                    print('Invalid row (not in range)')
                    continue
            except ValueError:
                print('Invalid column (not an integer)')
            else:
                col -= 1
                break

        # Ends the game if user hits a mine
        if (board[row][col] == '•') and (flag == 0) and (display[row][col] != '*'):
            for r in range(0, len(board)):
                for c in range(0, len(board[0])):
                    if board[r][c] == ' ':
                        board[r][c] = display[r][c]
            print('-' * (width * 3 + 10))
            display_terminal_board(board, width, height)
            print(' ------')
            print('| LOSE |')
            print(' ------')
            break
        
        # Separates board states in the terminal
        print('-' * (width * 3 + 10))

        # Generates a board updated with the next state
        show_cell(board, display, row, col, flag)
        display_terminal_board(display, width, height)
        flag = 0

    # Tells the user how long the board took to complete
    if measure_time(start_time)[0] > 0:
        print(f'Your time: {measure_time(start_time)[0]}min {measure_time(start_time)[1]:.2f}s')
    else:
        print(f'Your time: {measure_time(start_time)[1]:.2f}s')


# Pygame-based functions

# Enables text to be drawn on the screen
def draw_text(screen, text, font, text_color, x, y):
    text_image = font.render(text, True, text_color)
    screen.blit(text_image, (x - text_image.get_width() / 2, y - text_image.get_height() / 2))

# Lets user move sliders to select board values
# Returns width, height, mines
def get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()

    if screen.get_width() * .35 <= mouse_x <= screen.get_width() * .85:
        # Sets condition for holding a certain value bar
        if (screen.get_height() * .302 - screen.get_height() // 90) <= mouse_y <= (screen.get_height() * .302 + screen.get_height() // 90):
            holding_width_bar = True
        if (screen.get_height() * .502 - screen.get_height() // 90) <= mouse_y <= (screen.get_height() * .502 + screen.get_height() // 90):
            holding_height_bar = True
        if (screen.get_height() * .702 - screen.get_height() // 90) <= mouse_y <= (screen.get_height() * .702 + screen.get_height() // 90):
            holding_mines_bar = True
        
        # Changes value depending on condition
        if holding_width_bar:
            width = round(((mouse_x / screen.get_width() - .35) / .5) * 95 + 4)
        elif holding_height_bar:
            height = round(((mouse_x / screen.get_width() - .35) / .5) * 95 + 4)
        elif holding_mines_bar:
            mines = round(((mouse_x / screen.get_width() - .35) / .5) * (width * height - 10) + 1)

    # Sets a value to min or max if out of bar bounds
    elif mouse_x < screen.get_width() * .35:
        if holding_width_bar:
            width = 4
        elif holding_height_bar:
            height = 4
        elif holding_mines_bar:
            mines = 1
    elif mouse_x > screen.get_width() * .85:
        if holding_width_bar:
            width = 99
        elif holding_height_bar:
            height = 99
        elif holding_mines_bar:
            mines = width * height - 9
    
    # Limits value of mines if width or height parameters are changed
    if mines > width * height - 9:
        mines = width * height - 9

    return width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar

# Gets board dimensions and number of mines
def draw_board_value_prompt(screen, width, height, mines):
    text_font = 'mono'
    
    # Intro text and done button
    intro_text_box = pygame.Rect(screen.get_width() * .1, 
                                 screen.get_height() * .05, 
                                 screen.get_width() * .8, 
                                 screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', intro_text_box)
    pygame.draw.rect(screen, 'grey30', intro_text_box, screen.get_height() // 150)
    draw_text(screen, 'Select board dimensions and number of mines', 
              pygame.font.SysFont(text_font, screen.get_height() // 19), 
              'black', screen.get_width() * .5, screen.get_height() * .1)
    
    done_box = pygame.Rect(screen.get_width() * .45, 
                           screen.get_height() * .85, 
                           screen.get_width() * .1, 
                           screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', done_box)
    pygame.draw.rect(screen, 'grey30', done_box, screen.get_height() // 150)
    draw_text(screen, 'DONE', 
              pygame.font.SysFont(text_font, screen.get_height() // 19), 
              'black', screen.get_width() * .5, screen.get_height() * .9)
    

    # Width input
    # bg box
    width_box = pygame.Rect(screen.get_width() * .1, 
                            screen.get_height() * .25, 
                            screen.get_width() * .2, 
                            screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', width_box)
    pygame.draw.rect(screen, 'grey30', width_box, screen.get_height() // 150)
    draw_text(screen, f'WIDTH: {width}', 
              pygame.font.SysFont(text_font, screen.get_height() // 21, True), 
              'black', screen.get_width() * .2, screen.get_height() * .3)

    width_bar = pygame.Rect(screen.get_width() * .3,
                            screen.get_height() * .25,
                            screen.get_width() * .6, 
                            screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', width_bar)
    pygame.draw.rect(screen, 'grey30', width_bar, screen.get_height() // 150)

    # input bar
    draw_text(screen, '04', pygame.font.SysFont(text_font, screen.get_height() // 30), 
              'black', screen.get_width() * .325, screen.get_height() * .3)
    
    pygame.draw.line(screen, 'grey59', 
                     (screen.get_width() * .35, screen.get_height() * .3), 
                     (screen.get_width() * .85, screen.get_height() * .3), 
                     screen.get_height() // 90)
    pygame.draw.line(screen, 'grey30', 
                     (screen.get_width() * .35, screen.get_height() * .3), 
                     (screen.get_width() * (.35 + .5 * (width - 4) / 95), screen.get_height() * .3), 
                     screen.get_height() // 90)
    pygame.draw.circle(screen, 'grey30', 
                       (screen.get_width() * (.35 + .5 * (width - 4) / 95), screen.get_height() * .302), 
                       screen.get_height() // 90)
    
    draw_text(screen, '99', pygame.font.SysFont(text_font, screen.get_height() // 30), 
              'black', screen.get_width() * .875, screen.get_height() * .3)


    # Height input
    # bg box
    height_box = pygame.Rect(screen.get_width() * .1, 
                             screen.get_height() * .45, 
                             screen.get_width() * .2, 
                             screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', height_box)
    pygame.draw.rect(screen, 'grey30', height_box, screen.get_height() // 150)
    draw_text(screen, f'HEIGHT: {height}', 
              pygame.font.SysFont(text_font, screen.get_height() // 21, True), 
              'black', screen.get_width() * .2, screen.get_height() * .5)

    height_bar = pygame.Rect(screen.get_width() * .3,
                            screen.get_height() * .45,
                            screen.get_width() * .6, 
                            screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', height_bar)
    pygame.draw.rect(screen, 'grey30', height_bar, screen.get_height() // 150)

    # input bar
    draw_text(screen, '04', pygame.font.SysFont(text_font, screen.get_height() // 30), 
              'black', screen.get_width() * .325, screen.get_height() * .5)
    
    pygame.draw.line(screen, 'grey59', 
                     (screen.get_width() * .35, screen.get_height() * .5), 
                     (screen.get_width() * .85, screen.get_height() * .5), 
                     screen.get_height() // 90)
    pygame.draw.line(screen, 'grey30', 
                     (screen.get_width() * .35, screen.get_height() * .5), 
                     (screen.get_width() * (.35 + .5 * (height - 4) / 95), screen.get_height() * .5), 
                     screen.get_height() // 90)
    pygame.draw.circle(screen, 'grey30', 
                       (screen.get_width() * (.35 + .5 * (height - 4) / 95), screen.get_height() * .502), 
                       screen.get_height() // 90)
    
    draw_text(screen, '99', pygame.font.SysFont(text_font, screen.get_height() // 30), 
              'black', screen.get_width() * .875, screen.get_height() * .5)


    # Mines input
    # bg box
    mines_box = pygame.Rect(screen.get_width() * .1, 
                            screen.get_height() * .65, 
                            screen.get_width() * .2, 
                            screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', mines_box)
    pygame.draw.rect(screen, 'grey30', mines_box, screen.get_height() // 150)
    draw_text(screen, f'MINES: {mines}', 
              pygame.font.SysFont(text_font, screen.get_height() // 21, True), 
              'black', screen.get_width() * .2, screen.get_height() * .7)

    mines_bar = pygame.Rect(screen.get_width() * .3,
                            screen.get_height() * .65,
                            screen.get_width() * .6, 
                            screen.get_height() * .1)
    pygame.draw.rect(screen, 'lightgrey', mines_bar)
    pygame.draw.rect(screen, 'grey30', mines_bar, screen.get_height() // 150)

    recommended_box = pygame.Rect(screen.get_width() * .1, 
                                  screen.get_height() * .75, 
                                  screen.get_width() * .2, 
                                  screen.get_height() * .05)
    pygame.draw.rect(screen, 'lightgrey', recommended_box)
    pygame.draw.rect(screen, 'grey30', recommended_box, screen.get_height() // 150)
    draw_text(screen, f'Recommended: {round((width * height) * .181)}', 
              pygame.font.SysFont(text_font, screen.get_height() // 40), 
              'black', screen.get_width() * .2, screen.get_height() * .775)

    # input bar
    draw_text(screen, '01', pygame.font.SysFont(text_font, screen.get_height() // 35), 
              'black', screen.get_width() * .325, screen.get_height() * .7)
    
    pygame.draw.line(screen, 'grey59', 
                     (screen.get_width() * .35, screen.get_height() * .7), 
                     (screen.get_width() * .85, screen.get_height() * .7), 
                     screen.get_height() // 90)
    pygame.draw.line(screen, 'grey30', 
                     (screen.get_width() * .35, screen.get_height() * .7), 
                     (screen.get_width() * (.35 + .5 * (mines - 1) / (width * height - 10)), screen.get_height() * .7), 
                     screen.get_height() // 90)
    pygame.draw.circle(screen, 'grey30', 
                       (screen.get_width() * (.35 + .5 * (mines - 1) / (width * height - 10)), screen.get_height() * .702), 
                       screen.get_height() // 90)
    
    draw_text(screen, f'{"0" * (4 - len(str(width * height - 9)))}{width * height - 9}', 
              pygame.font.SysFont(text_font, screen.get_height() // 35), 
              'black', screen.get_width() * .875, screen.get_height() * .7)

# Checks if user pressed done button when choosing values
def clicked_done(screen, width, height, screen_res):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()

    if screen.get_width() * .45 <= mouse_x <= screen.get_width() * .55:
        if screen.get_height() * .85 <= mouse_y <= screen.get_height() * .95:
            board = [[0 for _ in range(width)] for _ in range(height)]
            display = [[0 for _ in range(width)] for _ in range(height)]

            border_size = (screen_res * 3 / 4) * 4 / (max(len(display[0]), len(display)))
            cell_scale = min((screen.get_width() - border_size * 2 - (screen.get_width() / 36)) / len(display[0]), 
                             (screen.get_height() - border_size * 2 - (screen.get_height() / 64) - (screen.get_height() / 9.6)) / len(display))
            
            game_is_going = True

            return board, display, border_size, cell_scale, game_is_going
    
    return ([None for _ in range(5)])

# Creates a hidden board with mine positions
def generate_board(screen, board, mines, cell_scale):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    
    # Centers the board
    board_x = (screen.get_width() - len(board[0]) * cell_scale) / 2
    board_y = (screen.get_height() + (screen.get_height() / 9.6) - len(board) * cell_scale) / 2
    
    if (board_x <= mouse_x < board_x + len(board[0]) * cell_scale) and (board_y <= mouse_y < board_y + len(board) * cell_scale):
        # Determines cell position using mouse position
        col = int((mouse_x - board_x) // cell_scale)
        row = int((mouse_y - board_y) // cell_scale)
    
        mine_positions = set()
        
        # adds mine positions to hidden board
        # aviods 9x9 area around first input
        # rerolls position if taken already
        while len(mine_positions) < mines:
            row_mine = random.randint(0, len(board) - 1)
            col_mine = random.randint(0, len(board[0]) - 1)
            if ((row_mine, col_mine) not in mine_positions) and not ((row_mine in range(row - 1, row + 2)) and (col_mine in range(col - 1, col + 2))):
                mine_positions.add((row_mine, col_mine))
                board[row_mine][col_mine] = '*'
    
        # counts mines around each cell and updates board with info
        '''
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] != '*':
                    mine_count = 0
                    for r in range(row - 1, row + 2):
                        for c in range(col - 1, col + 2):
                            if (r in range(len(board))) and (c in range(len(board[0]))) and (board[r][c] == '*'):
                                mine_count += 1
                    board[row][col] = mine_count
        '''
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == '*':
                    for r in range(row - 1, row + 2):
                        for c in range(col - 1, col + 2):
                            if (r in range(len(board))) and (c in range(len(board[0]))) and (board[r][c] != '*'):
                                board[r][c] += 1

        first_move = False
        start_time = time.time()

        return board, first_move, start_time
    
    first_move = True
    start_time = 0

    return board, first_move, start_time

# Draws game board scaled depending on board size
def draw_board(screen, display, border_size, cell_scale):
    # Defines variable for hidden and shown cell images
    hidden_cell = pygame.image.load('images/minesweeper_hidden_cell.png').convert()
    hidden_cell = pygame.transform.scale(hidden_cell, (cell_scale, cell_scale))

    shown_cell = pygame.image.load('images/minesweeper_shown_cell.png').convert()
    shown_cell = pygame.transform.scale(shown_cell, (cell_scale, cell_scale))
    
    # Centers the board
    board_x = (screen.get_width() - len(display[0]) * cell_scale) / 2
    board_y = (screen.get_height() + (screen.get_height() / 9.6) - len(display) * cell_scale) / 2

    # Draws board border and cells    
    pygame.draw.polygon(screen, 'grey24', [(board_x - border_size, board_y + len(display) * cell_scale + border_size),
                                           (board_x - border_size, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2)])
    pygame.draw.polygon(screen, 'grey24', [(board_x - border_size, board_y + cell_scale / 2),
                                           (board_x + cell_scale / 2, board_y + cell_scale / 2),
                                           (board_x + cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x - border_size, board_y + len(display) * cell_scale - cell_scale / 2)])
    pygame.draw.polygon(screen, 'grey24', [(board_x - border_size, board_y - border_size),
                                           (board_x + cell_scale / 2, board_y + cell_scale / 2),
                                           (board_x - border_size, board_y + cell_scale / 2)])
    
    pygame.draw.polygon(screen, 'grey30', [(board_x + len(display[0]) * cell_scale + border_size, board_y - border_size),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y - border_size),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + cell_scale / 2)])
    pygame.draw.polygon(screen, 'grey30', [(board_x + cell_scale / 2, board_y - border_size),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y - border_size),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + cell_scale / 2),
                                           (board_x + cell_scale / 2, board_y + cell_scale / 2)])
    pygame.draw.polygon(screen, 'grey30', [(board_x - border_size, board_y - border_size),
                                           (board_x + cell_scale / 2, board_y - border_size),
                                           (board_x + cell_scale / 2, board_y + cell_scale / 2)])
    
    pygame.draw.polygon(screen, 'grey52', [(board_x - border_size, board_y + len(display) * cell_scale + border_size),
                                           (board_x + cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + cell_scale / 2, board_y + len(display) * cell_scale + border_size)])
    pygame.draw.polygon(screen, 'grey52', [(board_x + cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + len(display) * cell_scale + border_size),
                                           (board_x + cell_scale / 2, board_y + len(display) * cell_scale + border_size)])
    pygame.draw.polygon(screen, 'grey52', [(board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale + border_size, board_y + len(display) * cell_scale + border_size),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + len(display) * cell_scale + border_size)])

    pygame.draw.polygon(screen, 'grey68', [(board_x + len(display[0]) * cell_scale + border_size, board_y - border_size),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale + border_size, board_y + cell_scale / 2)])
    pygame.draw.polygon(screen, 'grey68', [(board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale + border_size, board_y + cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale + border_size, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2)])
    pygame.draw.polygon(screen, 'grey68', [(board_x + len(display[0]) * cell_scale - cell_scale / 2, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale + border_size, board_y + len(display) * cell_scale - cell_scale / 2),
                                           (board_x + len(display[0]) * cell_scale + border_size, board_y + len(display) * cell_scale + border_size)])

    pygame.draw.polygon(screen, 'grey40', [(board_x, board_y),
                                           (board_x + len(display[0]) * cell_scale, board_y),
                                           (board_x + len(display[0]) * cell_scale, board_y + len(display) * cell_scale),
                                           (board_x, board_y + len(display) * cell_scale)])

    for x in range(len(display[0])):
        for y in range(len(display)):
            if display[y][x] == 0:
                screen.blit(hidden_cell, (board_x + x * cell_scale, board_y + y * cell_scale))
            elif display[y][x] == 1:
                screen.blit(shown_cell, (board_x + x * cell_scale, board_y + y * cell_scale))
            elif display[y][x] == '*':
                screen.blit(hidden_cell, (board_x + x * cell_scale, board_y + y * cell_scale))
                pygame.draw.circle(screen, 'red', (board_x + cell_scale * (x + .5), board_y + cell_scale * (y + .5)), cell_scale / 4)

# Draws mine counts for revealed cells
def draw_mine_count(screen, board, display, cell_scale):
    # Centers the board
    board_x = (screen.get_width() - len(display[0]) * cell_scale) / 2
    board_y = (screen.get_height() + (screen.get_height() / 9.6) - len(display) * cell_scale) / 2
    
    num_colors = {1:'blue',
                  2:'green',
                  3:'red',
                  4:'indigo',
                  5:'crimson',
                  6:'teal',
                  7:'purple',
                  8:'grey24'
                  }
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    colors = ['blue',
              'green',
              'red',
              'indigo',
              'crimson',
              'teal',
              'purple',
              'grey24']
    
    # Iterates through every cell and reveals value
    for x in range(len(display[0])):
        for y in range(len(display)):
            if display[y][x] == 1:
                if board[y][x] in range(1, 9):
                    draw_text(screen, str(board[y][x]),
                              pygame.font.SysFont('Pixelify Sans', int(cell_scale)), 
                              num_colors[board[y][x]], 
                              board_x + cell_scale * (x + .5), 
                              board_y + cell_scale * (y + .5))
                if board[y][x] == '*':
                    pygame.draw.circle(screen, 'black', (board_x + cell_scale * (x + .5), board_y + cell_scale * (y + .5)), cell_scale / 4)

# If a reavealed cell is 0, ajdacent cells will also be revealed
def reveal_adjacent(board, display):
    for x in range(len(display[0])):
        for y in range(len(display)):
            if display[y][x] == 1 and board[y][x] == 0:
                for r in range(y - 1, y + 2):
                    for c in range(x - 1, x + 2):
                        if (r in range(len(board))) and (c in range(len(board[0]))):
                            display[r][c] = 1

# checks if user has won or lost
def check_win_lose(board, display):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if display[y][x] == 1 and board[y][x] == '*':
                return False, True
            
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != '*' and display[y][x] != 1:
                return False, False
    
    return True, False

# shows mine positions if user has won or lost
def show_mines(screen, board, display, cell_scale):
    board_x = (screen.get_width() - len(display[0]) * cell_scale) / 2
    board_y = (screen.get_height() + (screen.get_height() / 9.6) - len(display) * cell_scale) / 2
    
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == '*' and display[r][c] == 0:
                display[r][c] = 1
            if board[r][c] != '*' and display[r][c] == '*':
                pygame.draw.line(screen, 'black',
                                 (board_x + cell_scale * (c + .2), board_y + cell_scale * (r + .2)),
                                 (board_x + cell_scale * (c + .8), board_y + cell_scale * (r + .8)),
                                 int(cell_scale / 10))

# Draws ui for mine count, time, and reset button
def draw_ui(screen, mines, start_time, current_time, flags, win, lose, first_move, game_is_going):
    # Backdrop on top of screen
    ui_bg = pygame.Rect(0, 0, screen.get_width(), (screen.get_height() / 9.6))
    pygame.draw.rect(screen, 'grey36',  ui_bg)

    ui_text_bg = pygame.Rect(screen.get_width() * .35, screen.get_height() * .01, screen.get_width() * .3, screen.get_height() / 11.5)
    pygame.draw.rect(screen, 'black', ui_text_bg)

    # Icons
    if not win and not lose:
        reset_button = pygame.image.load('images/minesweeper_reset_button.png').convert()
        reset_button = pygame.transform.scale(reset_button, (screen.get_height() / 11.5, screen.get_height() / 11.5))
        screen.blit(reset_button, (screen.get_width() / 2 - screen.get_height() / 23, screen.get_height() * .01))
    if win:
        win_icon = pygame.image.load('images/minesweeper_win_icon.png').convert()
        win_icon = pygame.transform.scale(win_icon, (screen.get_height() / 11.5, screen.get_height() / 11.5))
        screen.blit(win_icon, (screen.get_width() / 2 - screen.get_height() / 23, screen.get_height() * .01))
    if lose:
        lose_icon = pygame.image.load('images/minesweeper_lose_icon.png').convert()
        lose_icon = pygame.transform.scale(lose_icon, (screen.get_height() / 11.5, screen.get_height() / 11.5))
        screen.blit(lose_icon, (screen.get_width() / 2 - screen.get_height() / 23, screen.get_height() * .01))

    # mine count
    draw_text(screen, f'{"0" * (len(str(mines)) - len(str(mines - flags)))}{mines - flags}',
                       pygame.font.SysFont('mono', screen.get_height() // 15, True), 'red',
                       (screen.get_width() - screen.get_width() * .15 - screen.get_height() / 23) / 2,
                       screen.get_height() / 19.2)
    
    # measures time, stops if win or lose
    if first_move:
        min = 0
        sec = 0
    if win or lose:
        (min, sec) = current_time
    else:
        if game_is_going and not first_move:
            current_time = measure_time(start_time)
            (min, sec) = current_time
    min_fstring = f'{"0" * (2 - len(str(min)))}{(min)}'
    sec_fstring = f'{"0" * (2 - len(str(sec)))}{sec}'
    
    draw_text(screen, f'{min_fstring}:{sec_fstring}',
                      pygame.font.SysFont('mono', screen.get_height() // 15, True), 'red',
                      (screen.get_width() + screen.get_width() * .15 + screen.get_height() / 23) / 2,
                      screen.get_height() / 19.2)
    
    # Draws quit button
    quit_button = pygame.Rect(screen.get_width() * .9, screen.get_height() * .02, screen.get_width() * .085, screen.get_height() * 19 / 300)
    pygame.draw.rect(screen, 'lightgrey', quit_button)
    pygame.draw.rect(screen, 'grey30', quit_button, screen.get_height() // 150)

    draw_text(screen, 'QUIT', 
              pygame.font.SysFont('mono', screen.get_height() // 25, True), 'black',
              screen.get_width() * .9 + screen.get_width() * .085 / 2,
              screen.get_height() * .02 + screen.get_height() * 19 / 600)
    
    return current_time

# resets game if button is pressed
# returns conditionals for events
def reset_game():
    start_time = 0
    current_time = (0, 0)
    flags = 0

    game_is_going = False

    first_move = True

    win = False
    lose = False
    
    return start_time, current_time, flags, game_is_going, first_move, win, lose

# Draw text or bomb over revealed cells
# Returns number of flags placed
def update_display(screen, display, cell_scale, flags, first_move):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    
    # Centers the board
    board_x = (screen.get_width() - len(display[0]) * cell_scale) / 2
    board_y = (screen.get_height() + (screen.get_height() / 9.6) - len(display) * cell_scale) / 2
    
    #only when in range of grid
    if (board_x <= mouse_x < board_x + len(display[0]) * cell_scale) and (board_y <= mouse_y < board_y + len(display) * cell_scale):
        # Determines cell position using mouse position
        col = int((mouse_x - board_x) // cell_scale)
        row = int((mouse_y - board_y) // cell_scale)
        
        # Reveal cell
        if pygame.mouse.get_pressed()[0]:
            # Updates the list with grid values
            if display[row][col] == 0:
                display[row][col] = 1
        
        # Flag cell
        elif pygame.mouse.get_pressed()[2] and not first_move:
            if display[row][col] == 0:
                display[row][col] = '*'
                flags += 1
            elif display[row][col] == '*':
                display[row][col] = 0
                flags -= 1
    
    return flags

# Organizes graphics and functions to play on a screen
# Runs game for pygame
def pygame_play():
    # Defines screen width and height
    # 80x:  720x1280
    # 120x: 1920x1080
    while True:
        try:
            print('Enter screen resolution multiple (16x9)')
            print('ie. 80:  1280x720')
            print('    120: 1920x1080')
            screen_res = int(input('Screen res: '))
            print()
            while screen_res < 0:
                print('Not a valid resolution scale')
                print('Enter screen resolution multiple (16x9)')
                print('ie. 80:  1280x720')
                print('    120: 1920x1080')
                screen_res = int(input('Screen res: '))
            break
        except ValueError:
            print()
            print('Invalid, enter an integer')

    screen_width = 16 * screen_res
    screen_height = 9 * screen_res
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Defines coordinate bounds for the quit button
    screen.get_width() * .9, screen.get_height() * .02, screen.get_width() * .085, screen.get_height() * 19 / 300
    quit_bounds = ((screen.get_width() * .9, screen.get_width() * (.9 + .085)),
                   (screen.get_height() * .02, screen.get_height() * (.02 + 19 / 300)))

    # Declares variable for board width, height, and number of mines
    size_mult = 5
    width = 2 * size_mult
    height = 1 * size_mult
    mines = round((width * height) * .181)

    # Declares variable for start time and number of flags for ui
    start_time = 0
    current_time = (0, 0)
    flags = 0

    # Conditions
    run = True

    holding_width_bar = False
    holding_height_bar = False
    holding_mines_bar = False

    game_is_going = False

    first_move = True

    win = False
    lose = False
    while run:
        # Refresh screen fill and grid background
        screen.fill('grey40')

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # These conditions are checked if the game has started
            if game_is_going:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not win and not lose:
                        flags = update_display(screen, display, cell_scale, flags, first_move)
                    # allows player to reset game if the first move has been made
                    if not first_move:
                        if reset_button_bounds[0][0] <= pygame.mouse.get_pos()[0] <= reset_button_bounds[0][1]:
                            if reset_button_bounds[1][0] <= pygame.mouse.get_pos()[1] <= reset_button_bounds[1][1]:
                                (start_time, current_time, flags) = reset_game()[0:3]
                                (game_is_going, first_move, win, lose) = reset_game()[3:]
                    if quit_bounds[0][0] <= pygame.mouse.get_pos()[0] <= quit_bounds[0][1]:
                        if quit_bounds[1][0] <= pygame.mouse.get_pos()[1] <= quit_bounds[1][1]:
                            run = False
                # generates a game board using the first move input to avoid mines
                if first_move:
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        board, first_move, start_time = generate_board(screen, board, mines, cell_scale)
            # Runs when player is selecting borad values
            else:
                # If user moves mouse off a selected bar, they can still adjust the value
                if pygame.mouse.get_pressed()[0]:
                    width = get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar)[0]
                    height = get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar)[1]
                    mines = get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar)[2]
                    holding_width_bar = get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar)[3]
                    holding_height_bar = get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar)[4]
                    holding_mines_bar = get_board_values(screen, width, height, mines, holding_width_bar, holding_height_bar, holding_mines_bar)[5]
                else:
                    holding_width_bar = False
                    holding_height_bar = False
                    holding_mines_bar = False
                # shows the board and defines certain values when done button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    (board, display, border_size, cell_scale, game_is_going) = clicked_done(screen, width, height, screen_res)
        
        if game_is_going: #runs if board values have been selected
            reset_button_bounds = [(screen.get_width() / 2 - screen.get_height() / 23, screen.get_width() / 2 + screen.get_height() / 23),
                                   (screen.get_height() * .01, screen.get_height() * .01 + screen.get_height() / 11.5)]
            
            # Draw board info
            draw_board(screen, display, border_size, cell_scale)
            reveal_adjacent(board, display)
            draw_mine_count(screen, board, display, cell_scale)
            
            if not win and not lose:
                (win, lose) = check_win_lose(board, display)

            # draws mine count, reset button, and tracks time
            current_time = draw_ui(screen, mines, start_time, current_time, flags, win, lose, first_move, game_is_going)
        
        else: #runs before board dimensions and mine number are chosen
            draw_board_value_prompt(screen, width, height, mines)
        
        if win or lose:
            show_mines(screen, board, display, cell_scale)


        # Update screen display
        pygame.display.flip()


if __name__ == '__main__':
    # Prompts the terminal for a method to play
    while True:
        print('Select play mode')
        print('    1) Terminal')
        print('    2) Pygame')
        play_type = input('Mode (1 or 2): ')
        print()
        
        if play_type in ['1', '2']:
            play_type = int(play_type)
            break
        else:
            print('Invalid input')
    
    if play_type == 1:
        terminal_play()
    elif play_type == 2:
        pygame_play()
    
    pygame.quit()