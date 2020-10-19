import itertools

# SUGGESTIONS:
# use enumerate?
# next fix for errors
# next convert structure to classes
# create  graphical user interface for the game

def board_visual():
    global board
    board_output = 5 * '\t' + '   1  2  3'
    for i in range(len(board)):
        board_output += '\n' + 5 *'\t' + f'{i+1} ' + str(board[i]).replace(',', ' ')

    return board_output + '\n'

def winning_move():
    global board
    for i in range(len(board)):
        if (len(set(board[i])) == 1 and set(board[i]) == {1}) or (len(set(board[i])) == 1 and set(board[i]) == {2}):
            return True

        # checking for columns
        col_list = [board[0][i], board[1][i], board[2][i]]
        if (len(set(col_list)) == 1 and set(col_list) == {1}) or (len(set(col_list)) == 1 and set(col_list) == {2}):
            return True

        diag_list_1 = [board[0][0], board[1][1], board[2][2]]
        diag_list_2 = [board[0][2], board[1][1], board[2][0]]

        if (len(set(diag_list_1)) == 1 and set(diag_list_1) == {1}) or (len(set(diag_list_2)) == 1 and set(diag_list_2) == {1}):
            return True

        if (len(set(diag_list_1)) == 1 and set(diag_list_1) == {2}) or (len(set(diag_list_2)) == 1 and set(diag_list_2) == {2}):
            return True

def place_piece(player, row, col):
    global board
    if board[row][col] == 0:
        board[row][col] = player

    else:
        raise ValueError

def validate_format(position):
    try:
        x, z = position.split(":")
        x, z = int(x), int(z)

    except Exception:
        return False

    else:
        return True


game_running = True
game_won = False

while game_running:
    board = [[0, 0, 0] for i in range(3)]
    players = [1, 2]
    player_turn = itertools.cycle([1, 2])
    print(5*"\t" + "  NEW GAME" + "\n")
    print(board_visual())

    while game_won is False:
        player = next(player_turn)
        valid_move = False
        while valid_move is False:
            try:
                player_position = input(f'Player {player}, place your piece using the format ROW:COL\n')

                assert validate_format(player_position) is True

                player_position = player_position.split(':')
                row = int(player_position[0]) - 1
                col = int(player_position[1]) - 1
                place_piece(player, row, col)

                valid_move = True

            except ValueError:
                print("Position is already occupied, please enter a valid position.\n")

            except AssertionError:
                print("Position format is incorrect, please use the correct format ROW:COLUMN\n")

        print(board_visual())

        if winning_move() is True:
            print(f"Player {player} wins\n")
            game_won = True

    game_continue = None
    while game_continue not in ["y", "n"]:
        game_continue = input("Would you like to play another game? (y/n)\n")

        if game_continue == "y":
            game_won = False

        elif game_continue == "n":
            print("Thanks for playing!")
            game_running = False

        else:
            print("Please enter a valid option. (y/n)\n")


