"""
The program creates and allows you to play Minesweeper
"""

import random

__author__ = 'Nicholas Lamon'


def create_grid(size_x, size_y, mines, difficulty):
    """
    Creates the grid that is used for all the other functions
    :param size_x: The X Size of the Grid
    :param size_y: The Y Size of the Grid
    :param mines: If Mines should be Allowed (True / False)
    :param difficulty: The chance of bombs being spawned (1-10)
    :return: returns the array that was created
    """
    array = []
    line = []
    for y in range(0, size_y):
        for x in range(0, size_x):
            if mines:
                ran_num = random.randrange(0, 11)
                if ran_num <= difficulty:
                    line.append('x')
                else:
                    line.append('O')
            elif not mines:
                line.append('x')
        array.append(line)
        line = []
    return array


def display_grid(grid_array):
    """
    Take an array for an input and displays it to the user
    :param grid_array: The array that is used to display
    """
    # Takes any grid make and displays it
    for y in grid_array:
        for x in y:
            # print(row_number, end=' ')
            print(x, end=' ')
            # row_number += 1
        print()


def check_bomb(grid_array, coord_x, coord_y):
    """
    Creates an Array to find spot on grid Takes the number inside the
    coordinate spot and Checks if it's a bomb and returns True or False
    :param grid_array: The input grid to be read
    :param coord_x: The X coordinate of the point to be selected
    :param coord_y: The Y coordinate of the point to be selected
    :return: Returns true if there is a bomb and false if not
    """

    # Tests Edge Cases of List, so it doesn't wrap to other side
    if not (coord_x < 0 or coord_y < 0 or coord_y >= len(grid_array) or
            coord_x >= len(grid_array[coord_y])):
        # Defines the line that the numbers is on
        line = grid_array[coord_y]
        # print('Coord X',line[coordX])
        # checks if specific coordinate is bomb
        # returns True if it's a bomb, False if not
        if line[coord_x] == 'O':
            return True
        else:
            return False


def scan_3x3_grid(grid_array, coord_x, coord_y):
    """
    The code is going to scan a 3x3 area around a selected coordinate
    and count up how many bombs there are to display a number
    :param grid_array: The grid that will be scanned
    :param coord_x: The X coordinate of the point to be selected
    :param coord_y: The Y coordinate of the point to be selected
    :return:
    """
    total_bombs = 0

    # TOP LEFT
    if check_bomb(grid_array, coord_x - 1, coord_y - 1):
        total_bombs += 1
    # TOP MIDDLE
    if check_bomb(grid_array, coord_x, coord_y - 1):
        total_bombs += 1
    # TOP RIGHT
    if check_bomb(grid_array, coord_x + 1, coord_y - 1):
        total_bombs += 1
    # MIDDLE LEFT
    if check_bomb(grid_array, coord_x - 1, coord_y):
        total_bombs += 1
    # MIDDLE RIGHT
    if check_bomb(grid_array, coord_x + 1, coord_y):
        total_bombs += 1
    # BOTTOM LEFT
    if check_bomb(grid_array, coord_x - 1, coord_y + 1):
        total_bombs += 1
    # BOTTOM MIDDLE
    if check_bomb(grid_array, coord_x, coord_y + 1):
        total_bombs += 1
    # BOTTOM RIGHT
    if check_bomb(grid_array, coord_x + 1, coord_y + 1):
        total_bombs += 1

    return total_bombs


def new_grace_period(hidden_grid, working_grid, coord_x, coord_y):
    """
    In a three by three grid it checks the amount of bombs for each spot
    This is to make the game easier earlier on
    :param hidden_grid: The grid that the player doesn't see and has the
    bombs on it
    :param working_grid: The grid that the player sees and has the numbers
    on it
    :param coord_x: The X coordinate of the point to be selected
    :param coord_y: The Y coordinate of the point to be selected
    """

    for y in range(-1, 2):
        for x in range(-1, 2):
            new_coord_x = coord_x + x
            new_coord_y = coord_y + y
            # (new_coord_x, new_coord_y)
            # print(0 > new_coord_y)
            if 0 <= new_coord_y <= len(hidden_grid) and 0 <= new_coord_x <= \
                    len(hidden_grid[new_coord_y]):
                hidden_grid[new_coord_y][new_coord_x] = 'x'
                # if not(coordX < 0 or coordY < 0 or coordY >= len(hiddenGrid)
                # or coordX >= len(hiddenGrid[coordY])):
                # print('ran')
                working_grid[new_coord_y][new_coord_x] \
                    = scan_3x3_grid(hidden_grid, new_coord_x, new_coord_y)


def click_point(hidden_grid, working_grid, coord_x, coord_y,
                grace_period_counter):
    """
    Used to select a point and check if it's a bomb or not
    :param hidden_grid: The grid that the player doesn't see and has the
    bombs on it
    :param working_grid: The grid that the player sees and has the numbers
    on it
    :param coord_x: The X coordinate of the point to be selected
    :param coord_y: The Y coordinate of the point to be selected
    :param grace_period_counter: Used to check if the player has a grace period
    """
    # Defines the Grid
    hidden_line = hidden_grid[coord_y]
    working_line = working_grid[coord_y]

    # Check if grace period is active
    # Makes sure you can't get out on first click
    if grace_period_counter > 0:
        # print('counter', grace_period_counter)
        hidden_line[coord_x] = 'x'
        new_grace_period(hidden_grid, working_grid, coord_x, coord_y)

    # Detects if the spot is a bomb, if so it ends the game
    # If not a bomb it scans the area and changes

    if hidden_line[coord_x] == 'O':
        end_game()
    elif hidden_line[coord_x] == 'x':
        # Sets the coordinate on the Visible grid to the total bombs
        working_line[coord_x] = scan_3x3_grid(hidden_grid, coord_x, coord_y)


def flag_point(grid_array, coord_x, coord_y):
    """
    Flags a point as a bomb
    :param grid_array: The grid that the user can see
    :param coord_x: The X coordinate to be marked as a flag
    :param coord_y: The Y coordinate to be marked as a flag
    """
    line = grid_array[coord_y]
    if line[coord_x] == 'x':
        line[coord_x] = 'F'
    elif line[coord_x] == 'F':
        line[coord_x] = 'x'


# Need To Write Help Screen
def help_screen():
    """
    The Help screen that is displayed to explain how to play the game
    """
    print('---------------------------------------')
    print('In Minesweeper the objective is to flag all the bombs  \n'
          ' that are found on the map. When a point is selected \n'
          ' it tells you the amount of bombs that \n'
          ' are in a 3 x 3 area around the spot. If you \n'
          ' hit a bomb you lose and if you flag all the \n'
          ' mines you win. The top left is the origin of \n'
          ' the grid and it goes X coord first and then Y coord. \n'
          ' For example to select the middle of a 10x10grid\n '
          'you would type s 5 5 and to flag it you type f 5 5.\n '
          'Once you flag a point you can un-flag the point at anytime.\n')
    print('---------------------------------------')
    main()


def gameplay_loop(hidden_grid, working_grid, grace_period_counter):
    """
    Basic Logic:
    Create hiddenGrid and Grid full of x's based off of settings
    Gameplay Loop:
    Ask for Command Ex. Check 1 1 or Flag 1 1
    Take command and translate it to grid spot
    Push through check spot or flag with the grid and coord arguments.
    End game if bomb, loop back if not.
    Check if all bombs have a flag
    :param hidden_grid: The grid that the player doesn't see and has the
    bombs on it
    :param working_grid: The grid that the player sees and has the numbers
    on it
    :param grace_period_counter: Used to check if the player has a grace period
    """
    display_grid(working_grid)
    error = True
    while error:
        answer = input("Type 'S' Select Point Or 'F' to Flag a Point "
                       "(Ex. S 1 1 or F 1 1)")
        command = answer.split(' ')
        try:
            # Makes sure the other options are numbers
            command[1] = int(command[1]) - 1
            command[2] = int(command[2]) - 1
        except TypeError:
            print('Enter A valid whole number for grid coordinates')
        except IndexError:
            print('Enter the correct amount of numbers')
        except ValueError:
            print("If your reading this you typed something so messed up I "
                  "couldn't tell you. Please type something that is correct.")
        else:
            # Detects whether to flag or select
            if command[0].lower() == 's':
                # Confirms that the number is in the range of the grid.
                if (len(working_grid[command[2]]) >= int(command[1]) >= 0
                        and len(working_grid) >= int(command[2]) >= 0):
                    # Runs The Select Command
                    click_point(hidden_grid, working_grid, command[1],
                                command[2], grace_period_counter)
                    error = False
                else:
                    print('Please enter a whole number in the range of the '
                          'grid.')
            elif command[0].lower() == 'f':
                if (len(working_grid[command[2]]) >= int(command[1]) >= 0
                        and len(working_grid) >= int(command[2]) >= 0):
                    # Runs the Flag Command
                    flag_point(working_grid, command[1], command[2])
                    error = False
                else:
                    print('Please enter a whole number in the range of the '
                          'grid.')
            else:
                print("Invalid Answer:")


def start_game():
    """
    Opens settings and puts information into a list
    takes the info and creates the grids based off it
    Runs the Win Loop
    """
    settings = []
    f = open('settings.txt', 'r')
    settings.append(int(f.readline().rstrip()))
    settings.append(int(f.readline().rstrip()))
    settings.append(int(f.readline().rstrip()))
    f.close()
    grace_period_count = 1
    hidden_grid = create_grid(settings[0], settings[1], True, settings[2])
    working_grid = create_grid(settings[0], settings[1], False, settings[2])
    win = False
    while not win:
        gameplay_loop(hidden_grid, working_grid, grace_period_count)
        grace_period_count -= 1
        check_win(hidden_grid, working_grid)


def change_settings():
    """
    The section that allows the user to change their settings
    """
    settings = []
    f = open('settings.txt', 'r')
    settings.append(f.readline().rstrip())
    settings.append(f.readline().rstrip())
    settings.append(f.readline().rstrip())
    # print(settings)
    f.close()
    print('Your Settings are currently set to:')
    print('Grid Size: ', settings[0], 'x', settings[1], sep='')
    print('Current Difficulty is:', settings[2])
    # Gets the X Grid size while making sure user enters correct response
    f = open('settings.txt', 'w')
    print('What do you want the X grid size to be? (5-100)')
    error = True
    while error:
        try:
            answer = int(input(':'))
        except TypeError:
            print('Please enter a number 5-100')
        else:
            if 100 >= answer >= 5:
                f.write(str(answer) + '\n')
                error = False
            else:
                print('Please enter a number 5-100')
    # Gets the Y grid size while making sure user enters correct response
    print('What do you want the Y grid size to be? (5-100)')
    error = True
    while error:
        try:
            answer = int(input(':'))
        except TypeError:
            print('Please enter a whole number 5-100.')
        else:
            if 100 >= answer >= 5:
                f.write(str(answer) + '\n')
                error = False
            else:
                print('Please enter a whole number 5-100')
    # Gets the Difficulty making the answer is correct
    print('What do you want the Difficulty to be?'
          '(1-10, 1 = Impossible, 10 = Instant Win)')
    error = True
    while error:
        try:
            answer = int(input(':'))
        except TypeError:
            print('Please enter a whole number 1-10')
        else:
            if 10 >= answer >= 1:
                f.write(str(answer) + '\n')
                error = False
            else:
                print('Please enter a whole number 1-10')
    f.close()
    main()


def calculator():
    """
    A calculator that I used to meet the requirements for wierd things I didn't
    use.
    """
    answer = input('Input a whole number')
    try:
        answer = int(answer)
    except TypeError:
        calculator()
    else:
        print(answer ** 2, 'is your number squared')
        print(answer * 2, 'is your number times 2')
        print(answer / 2, 'is your number divided by 2')
        print(answer // 2, 'is your number floor divided by 2')
        if answer % 2 == 0:
            print('your number is even')
        else:
            print('your number is odd')
        print(str(answer) * 10, 'is your number printed 10 times')
        main()


def startup():
    """
    The starting message and menu that allows you to pick the options of
    settings, help, quit, calculator, or play
    """
    print('Welcome To Minesweeper')
    print("If you don't know how to Play type 'Help' if you want to play"
          "type 'Play' if you want to change default settings"
          " type 'Settings', for the extra requirements type 'calculator'."
          "\n If you want to stop "
          "playing you can type 'Quit'")
    correct_answer = False
    while not correct_answer:
        answer = input(':')
        if answer.lower() == 'help':
            correct_answer = True
            help_screen()
        elif answer.lower() == 'play':
            correct_answer = True
            start_game()
        elif answer.lower() == 'settings':
            correct_answer = True
            change_settings()
        elif answer.lower() == 'quit':
            quit()
        elif answer.lower() == 'calculator':
            correct_answer = True
            calculator()
        else:
            print('Type a valid answer')


def main():
    """
    The main function of the program that handles retrieving settings on boot
    of the program.
    """
    try:
        # Looks if a settings file already exists
        f = open('settings.txt', 'x')
    except FileExistsError:
        # If it exists it will keep old settings
        print('Old settings detected, Keeping those')
        print('-----------------')
    else:
        # If not it will set the default settings
        f.close()
        f = open('settings.txt', 'w')
        # gridX
        f.write('10\n')
        # gridY
        f.write('10\n')
        # Difficulty
        f.write('7\n')
        f.close()
    startup()


def win_game():
    """
    If the player has won the game this function will run which lets the player
    play again or go back to the main menu.
    """
    print('----------------')
    print('YOU WON!')
    valid_answer = False
    while not valid_answer:
        answer = input("Type 'P' to play again with same settings"
                       " or type 'R' to go back to main menu.")
        if answer.lower() == 'p':
            valid_answer = True
            start_game()
        elif answer.lower() == 'r':
            valid_answer = True
            main()
        else:
            print('Invalid Answer')


def end_game():
    """
    If the player Loses the game they can choose to play again or go back to
    the main menu
    """
    print('----------------')
    print('You Lost!')
    valid_answer = False
    while not valid_answer:
        answer = input("Type 'P' to play again with same settings"
                       " or type 'R' to go back to main menu.")
        if answer.lower() == 'p':
            valid_answer = True
            start_game()
        elif answer.lower() == 'r':
            valid_answer = True
            main()
        else:
            print('Invalid Answer')


def check_win(hidden_grid, working_grid):
    """
    Checks the total amount of correct flags match the total amount of  bombs
    :param hidden_grid: The grid the player doesn't see. Used for matching
    bombs to flags
    :param working_grid: The grid the user sees. Used to get the position of
    the flags
    """
    correct_flags = 0
    total_bombs = 0
    for y in range(0, len(hidden_grid)):
        for x in range(0, len(hidden_grid)):
            if hidden_grid[y][x] == 'O' and working_grid[y][x] == 'F':
                correct_flags += 1
            if hidden_grid[y][x] == 'O':
                total_bombs += 1
    if correct_flags == total_bombs:
        win_game()


if __name__ == "__main__":
    main()
