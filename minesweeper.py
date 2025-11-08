from functools import partial
import random
from tkinter import *
from tkinter import messagebox
from tkmacosx import Button


class Minesweeper:
    
    def __init__(self, width, height, numBombs):
        self.width = width
        self.height = height
        self.numBombs = numBombs
        self.numFlags = 0
        self.counter = 0
        self.start = True
        self.root = Tk()
        self.root.title('Minesweeper')
        #Uses two lists to assign the number of a square to its respective color
        self.colorList = ['white','blue','darkgreen','red','purple','maroon','cyan','black','dim gray','black']
        #Initializes all the lists to store the games information
        self.value = [[0 for j in range(height)] for i in range(width)]
        self.clicked = [[False for j in range(height)] for i in range(width)]
        self.flagged = [[False for j in range(height)] for i in range(width)]

        #Initializes the counter for number of flags to bombs remaining
        self.mines = self.griddy(Label(self.root, text=str(numBombs), font=('Arial', 18)), 0, height, width)
    
        self.frames = [[self.griddy(Frame(self.root, relief=RAISED, bd=3), i, j, 1) for j in range(height)] for i in range(width)]
        self.squares = [[self.packman(self.bound(Button(self.frames[i][j], bg='white', height=40, width=40, bd=0, command=partial(self.reveal, i, j)), partial(self.flag, i, j))) for j in range(height)] for i in range(width)]
    
        #Continuously runs the tkinter event loops
        self.root.mainloop()

    def bound(self, button, function):
        button.bind("<Button-2>", function)
        return button

    def griddy(self, frame, i, j, k):
        frame.grid(row=j, column=i, columnspan=k)
        return frame

    def packman(self, block):
        block.pack(padx=1, pady=1)
        return block

    def reveal(self, x, y):
        '''Reveals the squares when clicked'''
        
        if self.start:
            for (a, b) in random.sample([(i, j) for i in range(self.width) for j in range(self.height) if not (x-1<=i<=x+1 and y-1<=j<=y+1)], self.numBombs):
                self.value[a][b] = '*'
                for adjacent in range(-1, 2):
                    for tangent in range(-1, 2):
                        if 0<=a+adjacent<self.width and 0<=b+tangent<self.height and self.value[a+adjacent][b+tangent] != '*':
                            self.value[a+adjacent][b+tangent] += 1

            self.start = False
    
        #If player clicks on a mine
        if self.value[x][y] == '*':
            self.mines['text'] = 'You Lost!'
            self.gameOver = True
        
            #Reveals all mines
            for i in range(self.width):
                for j in range(self.height):
                    if self.value[i][j] == '*':
                        self.squares[i][j]['text'] = '*'
                        self.squares[i][j]['disabledbackground'] = 'red'
                        self.squares[i][j]['disabledforeground'] = 'black'
                    self.squares[i][j]['state'] = DISABLED
                    self.squares[i][j].unbind("<Button-2>")                        
                    
            #Shows error message
            messagebox.showerror(title='Minesweeper', message='KABOOM! You lose.')
    
        #Else, if the game already started    
        else:
            #Reveals square and updates the display/lists
            self.counter += 1
            self.squares[x][y]['disabledforeground'] = self.colorList[self.value[x][y]]
            self.squares[x][y]['disabledbackground'] = 'light gray'
            self.frames[x][y]['relief'] = SUNKEN
            self.clicked[x][y] = True
            self.squares[x][y]['state'] = DISABLED
            self.squares[x][y].unbind("<Button-2>")
        
            #Starts a loop that reveals subsequent squares if square has no adjacent mines
            if self.value[x][y] != 0:
                self.squares[x][y]['text'] = str(self.value[x][y])
                
            else:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0<=x+i<self.width and 0<=y+j<self.height and self.value[x+i][y+j] != '*' and not self.clicked[x+i][y+j]:
                            self.reveal(x+i, y+j)
        
            #If all possible squares are revealed by the player, then the game is won
            if self.counter == self.width*self.height-self.numBombs:
                self.mines['text'] = 'You Won!!!'
                for i in range(self.width):
                    for j in range(self.height):
                        self.squares[i][j]['state'] = DISABLED
                        self.squares[i][j].unbind("<Button-2>")
                    
                #Shows winning message
                messagebox.showinfo('Minesweeper','Congratulations -- you won!')
        
    def flag(self, x, y, bruh):
        if not self.flagged[x][y]:
            self.squares[x][y]['disabledforeground'] = 'black'
            self.squares[x][y]['disabledbackground'] = 'white'
            self.squares[x][y]['state'] = DISABLED
            self.squares[x][y]['text'] = '*'            
            self.numFlags += 1
        
        elif self.flagged[x][y]:
            self.squares[x][y]['activebackground'] = 'white'
            self.squares[x][y]['state'] = 'normal'
            self.squares[x][y]['text'] = ''
            self.numFlags -= 1
        self.flagged[x][y] = not self.flagged[x][y]
        self.mines['text'] = str(self.numBombs-self.numFlags)

if __name__ == "__main__":
    width, height, mines = 12, 10, 20
    Minesweeper(width, height, mines)
