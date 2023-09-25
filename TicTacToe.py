import os

class TicTacToe:
    def __init__(self) -> None:
        self.board = [i for i in range(1,10)]
        
    def display_board(self):
        os.system('clear')
        print("-------------------")
        for i in range(3):
            print("|     |     |     |")
            print(f"|  {self.board[i*3]}  |  {self.board[i*3 + 1]}  |  {self.board[i*3 + 2]}  |")
            print("|     |     |     |")
            print("-------------------")
    
    def define_palyer(self):
        player1 = input("Do you want to be X or O?").upper()
        if player1 == "X":
            player2 = "O"
        else:
            player2 = "X"
        return player1, player2
    
    def who_play(self):
        count_x = 0
        count_o = 0
        for i in self.board:
            if i == "X":
                count_x += 1
            elif i == "O":
                count_o += 1
        if count_x == count_o:
            return "X"
        else:
            return "O"
        
    def h_position_check(self, player):
        while True:
            position = input(f"{player}, choose your next position: (1-9) ")
            if position.isdigit() and int(position) in range(1, 10):
                position = int(position) - 1
                if self.board[position] == "X" or self.board[position] == "O":
                    print("This position is already taken!")
                else:
                    break
            else:
                print("Invalid input!")
        return position
    
    def multiple_player(self, player1, player2):
        current_cursor = self.who_play()
        if current_cursor == player1:
            player = "Player 1"
        else:
            player = "Player 2"
        position = self.h_position_check(player)
        self.board[position] = current_cursor

    def check_win(self):
        for i in range(3):
            if self.board[i*3] == self.board[1+i*3] == self.board[2+i*3]:
                return True
            elif self.board[i] == self.board[3+i] == self.board[6+i]:
                return True
        if self.board[0] == self.board[4] == self.board[8]:
            return True
        elif self.board[2] == self.board[4] == self.board[6]:
            return True
        else:
            return False
        
    def check_tie(self):
        count = 0
        for i in self.board:
            if i == "X" or i == "O":
                count += 1
        if count == 9:
            return True
        return False
        
    def play_again(self):
        again = input("Do you want to play again? (Y/N)").upper()
        if again == "Y":
            return True
        return False
    
    def play(self):
        while True:
            player1, player2 = self.define_palyer()
            while True:
                self.display_board()
                self.multiple_player(player1, player2)
                if self.check_win():
                    self.display_board()
                    print("You win!")
                    break
                if self.check_tie():
                    self.display_board()
                    print("It's a tie!")
                    break
            if not self.play_again():
                break