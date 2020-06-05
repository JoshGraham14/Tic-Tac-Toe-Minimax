"""
A console-based Tic-Tic-Toe game that uses the MiniMax algorithm for a perfect AI.
It is impossible to win this game against the bot, best case scenario is a tie.

Author: Josh Graham
Date: 5/30/2020
"""

import random
import sys

class Player:
    """
    This class defines a player.

    Attributes:
        name (str): The name of the player.
        symbol (str): A single character to uniquely represent the player (usually 'X' or 'O').
    """

    def __init__(self, name, symbol):
        """
        The constructor for the Player class.
        
        Parameters:
            name (str): The name of the player.
            symbol (str): A single character to uniquely represent the player (usually 'X' or 'O'). 
        """

        self.name = name
        self.symbol = symbol

class Board:
    """
    This class defines the board to be used for the game.

    Attributes:
        x (int): An x coordinate for the board
        y (int): A y coordinate for the board
    """

    def __init__(self):
        """
        The constructor for the Board class.

        Generates an empty game board.
        """

        self.board = [['-', '-', '-'],
                      ['-', '-', '-'],
                      ['-', '-', '-']]

    def show_board(self):
        """Displays the current game board to the user by printing it to the console."""

        for row in self.board:
            for col in row:
                print(col, end=" ")
            print("")

    def set_player(self, player, x, y):
        """
        Places the symbol of the player on to the board at a specified position.

        If the player is the bot, the ai function is called for choosing it's position.

        Parameters:
            player (obj): The current player object whose turn it is.
            x (int): The x coordinate of where the player is placing their symbol.
            y (int): The y coordinate of where the player is placing their symbol.
        """

        if(player.name == "Bot"):
            # Calls the ai function to get the best possible coordinates
            best_x, best_y = ai(self, player)
            self.board[best_x][best_y] = player.symbol
        else:
            self.board[x][y] = player.symbol

    def game_state(self):
        """
        Checks if the game has been won.

        Returns:
            bool: True if won, False if not.
            str: 'X', 'O', or None, depending on if there is a winner, and who it is.
        """

        # Checks horizontal and vertical columns
        for i in range(3):
            if(self.board[i][0] == 'X' and self.board[i][1] == 'X' and self.board[i][2] ==  'X'):
                return True, 'X'
            elif(self.board[i][0] == 'O' and self.board[i][1] == 'O' and self.board[i][2] ==  'O'):
                return True, 'O'
            elif(self.board[0][i] == 'X' and self.board[1][i] == 'X' and self.board[2][i] ==  'X'):
                return True, 'X'
            elif(self.board[0][i] == 'O' and self.board[1][i] == 'O' and self.board[2][i] ==  'O'):
                return True, 'O'
        # Checks the diagonals
        if(self.board[0][0] == 'X' and self.board[1][1] == 'X' and self.board[2][2] == 'X' or
                self.board[0][2] == 'X' and self.board[1][1] == 'X' and self.board[2][0] == 'X'):
            return True, 'X'
        elif(self.board[0][0] == 'O' and self.board[1][1] == 'O' and self.board[2][2] == 'O' or
                self.board[0][2] == 'O' and self.board[1][1] == 'O' and self.board[2][0] == 'O'):
            return True, 'O'

        return False, None # If no winner is found this is returned

    def check_pos(self, x, y):
        """
        Checks if a supplied position has already been taken or if its open.

        Parameters:
            x (int): The x coordinate of the position to be checked.
            y (int): The y coordinate of the position to be checked.

        Returns:
            bool: True if the position is open, False if the position is taken.
        """

        if(self.board[x][y] == '-'):
            return True
        return False

    def board_full(self):
        """
        Checks if every position on the board has been filled (therefore the game will end as a tie).

        Returns:
            bool: True if the board has every position filled, False if there are still spots available.
        """

        for row in self.board:
            for col in row:
                if(col == '-'):
                    return False
        return True

def make_play(board, player):
    """
    Allows the user to select which position they would like to place their symbol on the board.

    The position is verified to be valid before moving onto the set_player method. If the player
    is the bot, it goes straight to the set_player method, which goes to the ai function.

    Parameters:
        board (obj): The current board object.
        player (obj): the current player object.
    """

    board.show_board()
    # dictionary of all possible moves where the key is a numbered position and the value is the coordinates
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    if(player.name == "Bot"):
        board.set_player(player, 0, 0)
    else: 
        free_pos = False
        # This loop guarantees that the position the user chooses is not already taken
        while(free_pos == False):
            # This loop guarantees that the user chooses a position the is possible on the board (1-9)
            while(True):
                try:
                    move = int(input("Choose where you would like to make your play (1 - 9): "))
                    if(move < 10 and move > 0):
                        break
                    else:
                        print("Please try again, you must enter a number from 1-9")
                except ValueError:
                    print("Please try again, you must enter a number from 1-9")
            xy = moves[move]
            # Checks if the chosen move is available        
            free_pos = board.check_pos(xy[0], xy[1])
        # If the position is valid, the set_player method is called
        board.set_player(player, xy[0], xy[1])

def ai(state, player):
    """
    The best possible move is found for the bot to make. 
    
    This is done by looping through every free position on the board, and calling the minimax function 
    to "score" each position. Whichever position has the best score, becomes the move the bot uses.

    Parameters:
        state (obj): The current board object.
        player (obj): the current player object.

    Returns
        best_move[0] (int): the row coordinate of the best move.
        best_move[1] (int): the column coordinate of the best move.
    """
    best_score = -10000 # Sets the intial best score at an impossibly low value
    # Loops through every possible position in the current board
    for row in range(len(state.board)):
        for col in range(len(state.board[row])):
            # Checks if the current position is empty
            if(state.board[row][col] == "-"):
                state.board[row][col] = player.symbol
                # Minimax algorithm is applied to the board with the current position taken by the bot
                score = minimax(state, 0, False)                
                state.board[row][col] = "-" # Removes symbol from the board for the next loop
                if(score > best_score):
                    best_score = score
                    best_move = [row, col]
    return best_move[0], best_move[1]

def minimax(state, depth, max_or_min):
    """
    Recursively finds the best possible move to be made on the current game board.

    Scores are given to the maximizing and minimizing player based on their chances of winning the game 
    as each possible position is "played". Whatever position gives the end state with the best maximizing 
    score and worst minimizing score is the optimal position for the bot.

    Parameters:
        state (obj): this is the gameboard object. It could be the current board, or one simulated for 
                     the algorithm.
        depth (int): The current depth of the game/algorithm. Basically how many turns have been played.

    Returns:
        int: the score of the current play being made.
    """

    # Finds if the game has been won and for which player
    g_state, symb = state.game_state()
    # This is the terminal condition, if the game has been won or tied (board is full)
    if(state.board_full() or g_state):
        if(g_state == True and symb == 'X'):
            return -10
        elif(g_state == True and symb == 'O'):
            return 10
        elif(g_state == False):
            return 0

    if(max_or_min):
        # Impossibly low score set for the maximizing player, so that any move will replace it
        best_score = -10000
        # Loops through every possible position
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                # Loops through every possible position
                if(state.board[row][col] == "-"):
                    state.board[row][col] = "O"
                    # The function is recursively called, with the depth increased and its the minimizing player's turn
                    score = minimax(state, depth + 1, False)
                    state.board[row][col] = "-" # Removes symbol from the board for the next loop
                    if(score > best_score):
                        best_score = score                       
        return best_score
    else:
        # Impossibly high score set for the minimizing player, so that any move will replace it
        best_score = 10000
        # Loops through every possible position
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                # Loops through every possible position
                if(state.board[row][col] == "-"):
                    state.board[row][col] = "X"
                    # The function is recursively called, with the depth increased and its the maximizing player's turn
                    score = minimax(state, depth + 1, True)
                    state.board[row][col] = "-" # Removes symbol from the board for the next loop
                    if(score < best_score):
                        best_score = score                       
        return best_score

def main():
    """This is where the code will begin and also where the main game loop is."""

    game_board = Board()
    # Introduction to game
    print("\nWelcome to Tic Tac Toe! Please select what you would like to play.")
    game_type = input("1. Single player against AI.\n2. 2 player with another person.\n3. Quit.\n")

    if(game_type == "1"):
        name = input("What is your name? ")
        p1 = Player(name, 'X')
        p2 = Player("Bot", 'O')
    elif(game_type == "2"):
        name = input("What is the name of the first player? ")
        p1 = Player(name, 'X')
        name = input("What is the name of the second player? ")
        p2 = Player(name, 'O')
    else:
        sys.exit()
    print("\nPlayer 1: " + p1.name + "\t  Symbol: " + p1.symbol)
    print("Player 2: " + p2.name + "\t  Symbol: " + p2.symbol + "\n")
    # Generates a random number to determine who goes first
    rand = random.random()
    if(rand > .5):
        print(p1.name + " goes first!")
        turn = 1
    else:
        print(p2.name + " goes first!")
        turn = -1

    # MAIN GAME LOOP
    while(game_type == "1" or game_type == "2"):
        if(turn == 1):
            print( "\n" + p1.name + " it is your turn.")
            make_play(game_board, p1)
        else:
            print("\n" + p2.name + " it is your turn.")
            make_play(game_board, p2)
        # Checks if the game has been won and by whom
        g_state, symb = game_board.game_state()
        if(g_state):
            if(turn == 1):
                game_board.show_board()
                print(p1.name + " has won the game!")
            else:
                game_board.show_board()
                print(p2.name + " has won the game!")
            break

        if(game_board.board_full() == True):
            print("")
            game_board.show_board()
            print("The game has ended as a draw.")
            break

        turn *= -1 # this switches whose turn it is each round

main() # starts the game