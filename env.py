import numpy as np
import os

def intialize_board():
    global board
    board = [[i for i in range(1+j*3, 4+j*3)] for j in range(3)]
    return board

def display_board(board):
    os.system('clear')
    print("-------------------")
    for i in range(len(board)):
        print("|     |     |     |")
        print(f"|  {board[i][0]}  |  {board[i][1]}  |  {board[i][2]}  |")
        print("|     |     |     |")
        print("-------------------")

def define_palyer():
    player1 = input("Do you want to be X or O?").upper()
    if player1 == "X":
        player2 = "O"
    else:
        player2 = "X"
    n_turns = 0
    return player1, player2, n_turns

def position_check(player, type="human"):
    i,j = 0, 0
    while True:
        test = False
        if type == "human":
            position = input(f"{player}, choose your next position: (1-9) ")
            if position.isdigit() and int(position) in range(1, 10):
                position = int(position)
                test = True
            else:
                print("Invalid input!")
        else:
            position = np.random.randint(1, 10)
            test = True
        if test:
            i = (position-1) // 3
            j = position % 3 -1
            if board[i][j] == "X" or board[i][j] == "O":
                if type == "human":
                    print("This position is already taken!")
            else:
                break
    return i, j

def multiple_player(player1, player2):
    global n_turns
    if n_turns % 2 == 0:
        player = "Player 1"
        cursor = player1
    else:
        player = "Player 2"
        cursor = player2
    i,j = position_check(player)
    board[i][j] = cursor
    n_turns += 1

def computer_player(player1, player2):
    global n_turns
    if n_turns % 2 == 0:
        player = "Player 1"
        i,j = position_check(player)
        board[i][j] = player1
        n_turns += 1
    else:
        i,j = position_check(None, type="computer")
        board[i][j] = player2
        n_turns += 1

def check_win():
    global board
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return True
        elif board[0][i] == board[1][i] == board[2][i]:
            return True
    if board[0][0] == board[1][1] == board[2][2]:
        return True
    elif board[0][2] == board[1][1] == board[2][0]:
        return True
    else:
        return False

def play_again():
    play_again = input("Do you want to play again? (Y/N)").upper()
    if play_again == "Y":
        board = intialize_board()
        return True
    return False

if __name__ == "__main__":
    while True:
        intialize_board()
        player1, player2, n_turns = define_palyer()
        while True:
            display_board(board)
            multiple_player(player1, player2)
            if check_win():
                display_board(board)
                print("You win!")
                break
            if n_turns == 9:
                display_board(board)
                print("It's a tie!")
                break
        if not play_again():
            break