print("*" * 10, "Tic Tac Toe game", "*" * 10)

board = list(range(1, 10))


def draw_board(board):
    """
    Inside the program, the playing field is presented as a one-dimensional list with numbers from 1 to 9.
    """
    print("-" * 13)
    for i in range(3):
        print("|", board[0 + i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")
        print("-" * 13)


def take_input(player_token):
    """
    The objectives of this function:

    1. Accept user input.

    2. Process incorrect input, for example, you entered a wrong number. To convert a string to a number, use the int () function.

    3. Handle situations. when the cell is busy or when a number not from the range 1..9 is entered.
    """
    valid = False
    while not valid:
        player_answer = input("Where will we put " + player_token + "? ")
        try:
            player_answer = int(player_answer)
        except:
            print("Invalid input. Are you sure you entered the number?")
            continue
        if player_answer >= 1 and player_answer <= 9:
            if (str(board[player_answer - 1]) not in "XO"):
                board[player_answer - 1] = player_token
                valid = True
            else:
                print("This cage is already occupied!")
        else:
            print("Invalid entry. Please enter a number from 1 to 9.")


def check_win(board):
    """
    This function checks the playing field. We create a tuple with winning coordinates and loop through it in a for loop.

    If the symbols in all three given cells are equal, we return the winning symbol, otherwise, we return the False value.

    A non-empty string (winning character), when cast to a boolean type, will return True.
    """
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False


def main(board):
    """
    In this function, create a while loop. The cycle is performed until one of the players wins. In this loop we render the game board, accept user input, defining the token (x or zero) of the player.

    We wait for the counter variable to be greater than 4 to avoid the obviously unnecessary check_win function call.

    The tmp variable was created in order not to call the check_win function once again, we just “remember” its value and, if necessary, use it in the line “print (tmp,“ won! ”)”.
    """
    counter = 0
    win = False
    while not win:
        draw_board(board)
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1
        if counter > 4:
            tmp = check_win(board)
            if tmp:
                print(tmp, "winner!")
                win = True
                break
        if counter == 9:
            print("Draw!")
            break
    draw_board(board)


main(board)

input("Press Enter to exit!")
