list_of_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
board = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
def board_displaying(board):
    print("       |       |        ")
    print("   " + board[0] + "   |   " + board[1] + "   |   " + board[2] + "   ")
    print("       |       |        ")
    print("-------------------------")
    print("       |       |        ")
    print("   " + board[3] + "   |   " + board[4] + "   |   " + board[5] + "   ")
    print("       |       |        ")
    print("-------------------------")
    print("       |       |        ")
    print("   " + board[6] + "   |   " + board[7] + "   |   " + board[8] + "   ")
    print("       |       |        ")

def player1_choise():
    flag = True

    while flag:

        chosen_position = input(f"Player1, please enter the number in {list_of_values}: ")
        true_or_false = chosen_position.isdigit()

        if true_or_false == True:

            if int(chosen_position) not in list_of_values:
                flag = True
            else:
                flag = False
        else:
            flag = True

    result = int(chosen_position)
    return result

def player2_choise():
    flag = True

    while flag:

        chosen_position = input(f"Player2, please enter the number in {list_of_values}: ")
        true_or_false = chosen_position.isdigit()

        if true_or_false == True:

            if int(chosen_position) not in list_of_values:
                flag = True
            else:
                flag = False
        else:
            flag = True

    result = int(chosen_position)
    return result

def free_cells(tpl: tuple):
    board[tpl[0]] = tpl[1]
    list_of_values.remove(tpl[0])

    board_displaying(board)

    def x_or_o():

        flag = True
        diction = {0: "X", 1: "O"}
        lst = [0, 1]
        while flag:

            answer = input("Player1, enter 0 - for 'X', and 1 - for 'O'")
            boolean = answer.isdigit()

            if boolean:

                if int(answer) in lst:
                    flag = False
                    break
                else:
                    flag = True
            else:
                flag = True

        player1 = diction[int(answer)]
        player2 = diction[abs(int(answer) - 1)]

        print(f"First player is {player1}")
        print(f"Second player is {player2}")

        return player1, player2

def X_or_O():
    flag = True
    lst = ['X', 'O']
    while flag:

        answer = input("Player1, enter X or O: ").upper()

        if answer in lst:
            flag = False
            break
        else:
            flag = True

    player1 = answer
    lst.remove(answer)
    player2 = lst[0]

    print(f"First player is {player1}")
    print(f"Second player is {player2}")

    return player1, player2

def check_winner():
    if (board[0] == board[1] == board[2] or board[3] == board[4] == board[5] or
            board[6] == board[7] == board[8] or board[0] == board[4] == board[8] or
            board[2] == board[4] == board[6] or board[0] == board[3] == board[6] or
            board[1] == board[4] == board[7] or board[2] == board[5] == board[8]):
        print('CONGRETULATIONs')
        return False
    else:
        return True

board_displaying(board)

tpl = X_or_O()
_st = tpl[0]
_nd = tpl[1]

while check_winner():
    _ = player1_choise()
    choise = (_, _st)
    free_cells(choise)

    if check_winner():
        _2 = player2_choise()
        choise2 = (_2, _nd)
        free_cells(choise2)
    else:
        break


