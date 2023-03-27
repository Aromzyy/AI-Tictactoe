#importing the required modules
import pygame
import sys
from copy import deepcopy
import numpy as np


#the colors we will use for the game interface
background_shade= (255,255,0)
line_shade = (0,0,255)
x_shade= (0, 255, 0)
o_shade = (0, 0, 0)

#these are the dimensions of our board
board_width = 720
board_height = 720

#defining number of rows and columns in the game
columns = 3
rows = 3

#the size of the board
board_size = board_width // columns

#this is how large the xs, os and lines will be
x_size = 20
line_size= 15
circle_size = 15
radius = board_size // 4

#space between the ending of the cross line and the column line
spacing = 50

#initializing pygame module
pygame.init()

#creating the screen that our user will see
interface = pygame.display.set_mode( (720, 720) )

#we put the color for our interface's background
interface.fill(background_shade)

# the label that will be displayed on the game interface
pygame.display.set_caption('HUMAN vs AI')



class Board:
    #constructor for the board class
    def __init__(self):
        
        #we are using zeros to represent empty squares on the console board
        self.boxes = np.zeros( (rows, columns) )
        
        # a list of empty squares to initialize the board 
        self.unmarked_boxes = self.boxes 
        
        #initializing the number of marked squares to 0 since the game hasn't started
        self.marked_boxes = 0

    #checks the final state to see whether we have a win and returns 1 or 2 depending on who won  or no win returns 0
    def end_state(self, visible=False):
        #visible is set to false at first since we don't want to draw a line when there's no win
        

        # drawing a line for when a player fills a column
       
        for col in range(columns):
            #checking that these marks are the same and that the squares are not empty  
            if self.boxes[0][col] == self.boxes[1][col] == self.boxes[2][col] != 0:
                
                #the color of the line will depend on who won between playesr 1 and 2
                if visible:
                    #start position of the line
                    start = (col * board_size + board_size // 2, 20)
                    #end position of the line
                    stop = (col * board_size + board_size // 2, board_height - 20)
                    
                    #selecting the color of the line based on the winner
                    if self.boxes[0][col] == 2 :
                        color = x_shade
                    else:
                        color = o_shade
                    
                    #draw the line using the start and stop positions
                    pygame.draw.line(interface, color, start, stop, line_size)
                return self.boxes[0][col]

        # drawing a line for when a player fills an ascending diagonal

        #checking that these marks are the same and that the squares are not empty
        if self.boxes[2][0] == self.boxes[1][1] == self.boxes[0][2] != 0:
        
            
            #the color of the line will depend on who won between playesr 1 and 2
            if visible:
                
                #where the line starts
                start = (20, board_height - 20)
                #where the line ends
                stop = (board_width - 20, 20)
                
                #selecting the color of the line based on the winner
                if self.boxes[1][1] == 2:
                        color = x_shade
                else:
                        color = o_shade
                
                pygame.draw.line(interface, color, start, stop, x_size)
            
            return self.boxes[1][1]

        
        # drawing a line for when a player fills a row
        for row in range(rows):
            #checking that these marks are the same and that the squares are not empty
            
            if self.boxes[row][0] == self.boxes[row][1] == self.boxes[row][2] != 0:
            

                #the color of the line will depend on who won between players 1 and 2
                if visible:
                    start = (20, row * board_size + board_size // 2)
                    stop = (board_width - 20, row * board_size + board_size // 2)
                    
                    #selecting the color of the line based on the winner
                    if self.boxes[0][col] == 2 :
                        color = x_shade
                    else:
                        color = o_shade
                    pygame.draw.line(interface, color, start, stop, line_size)
                return self.boxes[row][0]

        
        # drawing a line for when a player fills a descending diagonal
        
        if self.boxes[0][0] == self.boxes[1][1] == self.boxes[2][2] != 0:
            if visible:
                start = (20, 20)
                stop = (board_width- 20, board_height - 20)
                
                #selecting the color of the line based on the winner
                if self.boxes[0][col] == 2 :
                        color = x_shade
                else:
                        color = o_shade
                pygame.draw.line(interface, color, start, stop, x_size)
            return self.boxes[1][1]

        # we return 0 if no one has won
        return 0

    #this method marks the squares based on the player that has placed their symbol on it
    def put_symbol(self, row, col, player):
        
        #we change the 0 on the board to the number assigned to the player that marked it
        self.boxes[row][col] = player
        
        #we add 1 to the count of the number of marked squares
        self.marked_boxes += 1

    
    def find_unmarked(self):
        #checks for the squares that have no mark on them and returns a list of their coordinates
        unmarked_boxes = []
        for row in range(rows):
            for col in range(columns):
                #checks if the square is empty
                if self.boxes[row][col] == 0:
                    #adds those coordinates to the list
                    unmarked_boxes.append( (row, col) )
        
        return unmarked_boxes

    def check_unmarked(self, row, col):
        #checks and returns the positions of empty squares i.e the value there is a 0
        return self.boxes[row][col] == 0

    #checks to see if no square has been marked, meaning that no move has been made yet
    def board_untouched(self):
        return self.marked_boxes == 0

    #checks if all squares have been marked, meaning that the game is over
    def board_fully_marked(self):
        return self.marked_boxes == 9

    

class Bot:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player


    def minimax(self, board, minimizing):
        
        # this is the base case e.g win or draw
        state = board.end_state()

        # if no one wins i.e they draw, we return 0, with no optimal move since we are already at the base case
        if board.board_fully_marked():
            return 0, None

        # if player 1 wins, we return 1, with no optimal move since we are already at the base case
        if state == 1:
            return 1, None 

        # if player 2 (bot) wins, we return -1 since the ai is using the minimizing approach, also no optimal move since we are already at a base case
        elif state == 2:
            return -1, None

        

        if minimizing:
            
            #the minimum value that the minimizing player gets from the board, we will keep updating in case the layer gets a smaller value
            lowest_value = 5
            
            #look for the unmarked squares
            unmarked_boxes = board.find_unmarked()

            #loop through the empty squares
            for (row, col) in unmarked_boxes:
                
                #create a copy of the board so that we don't alter the main board when testing
                new_board = deepcopy(board)
                
                #mark the temporary / copied square with the symbol of the minimizing player
                new_board.put_symbol(row, col, self.player)
                
                #recursively call the minimax function
                value = self.minimax(new_board, True)[0]
                
                #if the minimizing player gets a value less than their current one, they replace t with the new lower value
                if value < lowest_value:
                    lowest_value = value
                    
                    #this is the row and column that led us to that minimum evaluation value
                    optimal_choice = (row, col)
            
            #we get our lowest evaluation value and the move that led us to it.
            return lowest_value, optimal_choice

        
        else:
            #the maximum evaluation value that the maximizing player gets, we keep updating when we find a larger evaluation value
            highest_value = -5
            
            #we check for the unmarked squares on the board
            unmarked_boxes = board.find_unmarked()

            #looping through the unmarked squares
            for (row, col) in unmarked_boxes:
                #making a temporary copy of the board to avoid altering the main one
                new_board = deepcopy(board)
                
                #mark the tenporary / copied square with the symbol of the maximizing  player 
                new_board.put_symbol(row, col, 1)
                
                #recursively call minimax function
                value = self.minimax(new_board, False)[0]

                #if we get an evaluation value greater than what we have, the higher value becomes our new value
                if value > highest_value:
                    highest_value = value
                    
                    #the move that got us to the maximum evaluation value
                    optimal_choice = (row, col)
            
            #we return the highest evaluation value and the move that got us there
            return highest_value,optimal_choice

    
    #this is our key evaluation function
    def compute_value(self, main_board):
        
        #gives us the position where the AI has marked and the value obtained after taking that position by applying minimax algorithm
        value,choice= self.minimax(main_board, True)
        
        print(f'the bot has marked the square at {choice}')
        
        #gives us the coordinates of the box that the ai marked after using minimax algorithm
        return choice 

class Tictactoe:
    #constructor for the game object
    def __init__(self):
        
        self.bot = Bot()

        #the human always plays first
        self.player = 1   
        
        #a console board to enable us apply the game logic
        self.board = Board() 

        #for creating the lines, defined below
        self.draw_lines()
        
        #if the game is not over yet, we still run it
        self.in_progress = True

        self.boxes = np.zeros( (rows, columns) )
        self.marked_boxes = 0
    
    #we use this to draw the lines for the game
    def draw_lines(self):
        
        interface.fill( background_shade )

        # we draw the horizontal lines for the game interface
        pygame.draw.line(interface, line_shade, (0, board_size), (board_width, board_size), line_size)
        pygame.draw.line(interface, line_shade, (0, board_height - board_size), (board_width, board_height - board_size), line_size)
        
        # we draw the vertical lines for the game interface
        pygame.draw.line(interface, line_shade, (board_size, 0), (board_size, board_height), line_size)
        pygame.draw.line(interface, line_shade, (board_width - board_size, 0), (board_width - board_size, board_height), line_size)
        

    def choose_box(self, row, col):
        #assigning that box to that player
        self.board.put_symbol(row, col, self.player)
    

        if self.player == 1:
            # player 1 draws circles to make a move
            midpoint = (col * board_size + board_size // 2, row * board_size + board_size // 2)
            pygame.draw.circle(interface, o_shade, midpoint, radius, circle_size)
            
        
        elif self.player == 2:

            #player 2 draws crosses to make a move

            #the descending line of the cross
            start1 = (col * board_size + spacing, row * board_size + spacing)
            stop1 = (col * board_size + board_size - spacing, row * board_size + board_size - spacing)
            pygame.draw.line(interface, x_shade, start1, stop1, x_size)
            
            # the ascending line of the cross
            start2= (col * board_size + spacing, row * board_size + board_size - spacing)
            stop2 = (col * board_size + board_size - spacing, row * board_size + spacing)
            pygame.draw.line(interface, x_shade, start2, stop2, x_size)

        #we change the player to be the opponent
        # we use this since 0%2 + 1 =2 and 2%2 + 1 = 1
        self.player = self.player % 2 + 1
    
    def game_over(self):
        #if all boxes are marked
        return self.board.board_fully_marked() or self.board.end_state(visible=True) != 0 


def main():

    
    #creating the game object using the class Game
    game = Tictactoe()
    #we use it to access the board for the game
    board = game.board
    bot = game.bot


    while True:

        if game.in_progress and game.player == bot.player:

            # update the screen
            pygame.display.update()

            # the coordinates that led us to the minimum evaluation value
            row, col = bot.compute_value(board)
            
            #make a move in that direction since it gives the bot the best result
            game.choose_box(row, col)
            
            #if all boxes are marked, we stop running the game
            if game.game_over():
                game.in_progress = False
            
        
        # we are looking through all possible game events i.e actions taken by the user
        for event in pygame.event.get():

            # if a user clicks onto the interface
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #these are the coordinates for where the user clicked on the screen
                coord = event.pos
                
                #we then convert these coordinates from pixels to (row, column) format
                row = coord[1] // board_size
                col = coord[0] // board_size
                
                # if there is an empty square and the game is still on, we make a move
                if board.check_unmarked(row, col) and game.in_progress:
                    game.choose_box(row, col)

                    #if the game is over i. e all boxes are marked, we stop running it
                    if game.game_over():
                        game.in_progress = False

            # if the user selects to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        #updates portions of the screen
        pygame.display.update()
        
main()