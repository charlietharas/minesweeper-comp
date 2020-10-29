'''
Created on Oct 21, 2020

@author: Charlie Tharas
'''

import numpy as np
import random
import tkinter as tk

class Minesweeper:
    # declares game constants
    def __init__(self, difficulty):
        self.DIFF_SELECT = difficulty
        self.GRID_X = self.DIFF_SELECT[0][0]
        self.GRID_Y = self.DIFF_SELECT[0][1]
        self.NUM_MINES = self.DIFF_SELECT[1]
        self.num_flags = self.NUM_MINES
        self.score = 0 # flagged mines
        self.game_over = False
        print("Game settings at", self.DIFF_SELECT[2],"difficulty,", self.GRID_X, "by", self.GRID_Y, "grid with", self.NUM_MINES, "mines.")
    
        # starts everything
        self.guiInit()
    
    # setting up tkinter
    def guiInit(self):
        # gui initialization
        self.tk_root = tk.Tk()
        self.tk_root.title("Minesweeper by Charlie")
        self.tk_frame = tk.Frame(self.tk_root)
        self.tk_button_list = []
        self.grid_is_generated = False
        for i in range(self.GRID_X):
            for ii in range(self.GRID_Y):
                self.tk_button_list.append(tk.Button(self.tk_frame, activebackground='green', width=3, command=lambda i=i, ii=ii : self.doButtonCommand(i, ii)))
                self.tk_button_list[-1].bind("<Button-3>", self.flag) # works on win10
                self.tk_button_list[-1].bind("<Button-2>", self.unflag) # works on win10
                self.tk_button_list[-1].grid(row=i, column=ii)
                
        self.tk_text = tk.StringVar()
        text_to_set = "Flags", self.num_flags, "Total mines", self.NUM_MINES
        self.tk_text_label = tk.Button(self.tk_frame, text=text_to_set)
        self.tk_text_label.grid(row=ii+1, columnspan=self.GRID_X)
        self.tk_frame.pack(side="top", fill="both", expand=True)
        self.tk_root.mainloop()
        
    # managing events upon button presses
    def doButtonCommand(self, x, y):
        try:
            if self.grid_is_generated:
                self.reveal(x, y)
                self.doReveal()
            else:
                self.generateMines(x, y)
                self.doReveal()
                text_to_set = "Flags", self.num_flags, "Total mines", self.NUM_MINES
                self.tk_text_label.config(text=text_to_set)
        except IndexError:
            self.doButtonCommand(x, y)
    
    # starts the game
    def generateMines(self, start_x, start_y):
        # initialize starting tiles
        self.start_x = start_x
        self.start_y = start_y
        self.start_adjacent = []
        for i in [-1, 0, 1]:
            for ii in [-1, 0, 1]:
                self.start_adjacent.append([self.start_x+i, self.start_y+ii])
        
        # grid generation
        self.grid = np.zeros(shape=(self.GRID_X, self.GRID_Y))
        self.grid[self.start_x, self.start_y] = -2
        print("Successfully initialized start tile")
      
        # mine generation
        # sets coordinates for mines
        self.mines = []
        rand_x, rand_y = [0, 0]
        for i in range(self.NUM_MINES):
            rand_x = random.randint(0, self.GRID_X-1)
            rand_y = random.randint(0, self.GRID_Y-1)
            while [rand_x, rand_y] in self.mines or [rand_x, rand_y] in self.start_adjacent:
                rand_x = random.randint(0, self.GRID_X-1)
                rand_y = random.randint(0, self.GRID_Y-1)
            self.mines.append([rand_x, rand_y])
            
        print("Generated mines at coord list", self.mines)
        
        # places mines
        for i in self.mines:
            self.grid[i[0], i[1]] = -1
        
        # marks amount of mines near tiles
        for i in range(self.GRID_X):
            for ii in range(self.GRID_Y):
                if self.isUnusable(i, ii):
                    continue
                
                self.grid[i, ii] = self.getMines(i, ii)
                
        print("Grid generated.")
        print("GRID:")
        print(self.grid)
    
        # revealing overlay
        # shows which grid items are visible to the player
        self.revealed_overlay = np.zeros(shape=(self.GRID_X, self.GRID_Y))
        leftBorder, rightBorder, topBorder, bottomBorder = self.doBorderCheck(self.start_x, self.start_y)
        for i in range(self.start_x-leftBorder, self.start_x+(2*rightBorder)):
            for ii in range(self.start_y-topBorder, self.start_y+(2*bottomBorder)):
                print("DEBUG", i, ii)
                self.reveal(i, ii)
        self.doReveal()
                        
        # self.revealed_overlay[self.start_x-leftBorder:self.start_x+(2*rightBorder), self.start_y-topBorder:self.start_y+(2*bottomBorder)].fill(1)
    
        print("Designated revealed tiles.")
        print("REVEALED OVERLAY:")
        print(self.revealed_overlay)
        
        self.grid_is_generated = True
        
    # utility functions
    # get adjacent mine count
    # values for tiles (for debugging)
    # 0 is revealed (empty)
    # 1, 2, 3 are representations of mines nearby
    # -1 is mine
    # -2 is start
    def getMines(self, x, y):
        adj_mines = 0 
        if self.grid[x, y] == -1:
            return -1
        
        leftBorder, rightBorder, topBorder, bottomBorder = self.doBorderCheck(x, y)
        subsect = self.grid[x-leftBorder:x+(2*rightBorder), y-topBorder:y+(2*bottomBorder)].flatten()
        for i in subsect:
            if i == -1:
                adj_mines += 1
                
        return adj_mines
    
    # get if position is unsuitable to generate mine at/change/use
    def isUnusable(self, x, y):
        if self.grid[x, y] == -2 or self.grid[x, y] == -1:
            return True
        return False
    
    def doBorderCheck(self, x, y):
        leftBorder, rightBorder, topBorder, bottomBorder = [True, True, True, True] # reverse values necessary for operations
        if x-1 < 0:
            leftBorder = False
        elif x >= self.GRID_X:
            rightBorder = False
        if y - 1 <0:
            topBorder = False
        elif y >= self.GRID_Y:
            bottomBorder = False
        return [leftBorder, rightBorder, topBorder, bottomBorder]
    
    # updates grid for revealed tiles
    def doReveal(self):
        for i in self.tk_button_list:
            x = i.grid_info()['row']
            y = i.grid_info()['column']
            if self.revealed_overlay[x, y] == 1:
                i.config(text=self.grid[x, y], bg="white")
            if self.revealed_overlay[x, y] == 0:
                i.config(bg="gray")
            if self.revealed_overlay[x, y] == 2:
                i.config(bg="red")
    
    # player functions
    # player selects tile thinking it is not a mine. loses if it is a mine.
    def reveal(self, x, y):        
        if self.grid[x, y] == -1:
            self.lose() # pass x,y parameter to show user where they died?
            return "lost"
        
        if self.revealed_overlay[x, y] == 1:
            return "revealed"
        
        if self.revealed_overlay[x, y] == 2:
            self.unflag(x, y)
        
        if self.grid[x, y] == 0:
            self.revealed_overlay[x, y] = 1
            leftBorder, rightBorder, topBorder, bottomBorder = self.doBorderCheck(x, y)
            to_reveal_list=[]
            for i in [-leftBorder, 0, rightBorder]:
                for ii in [-topBorder, 0, bottomBorder]:
                    to_reveal_list.append([x+i, y+ii])
                    if self.grid[x+i, y+ii] == 0:
                        to_reveal=True
                        
            if to_reveal:
                for i in to_reveal_list:
                    self.reveal(i[0], i[1])
        
        self.revealed_overlay[x, y] = 1
        print("User made move at", x, y)
        print("GRID:")
        print(self.grid)
        print("REVEALED OVERLAY:")
        print(self.revealed_overlay)
               
    # player flags tile thinking it is a mine. tile is not revealed until player runs out of flags. if player places all flags and gets >0 wrong, loses. 
    def flag(self, event):
        x = event.widget.grid_info()['row']
        y = event.widget.grid_info()['column']
        if self.revealed_overlay[x, y] == 2 or self.revealed_overlay[x,y] == 1:
            return False
        else:
            self.num_flags -=1
            if self.num_flags == 0 and self.score == self.NUM_MINES:
                self.win()
            elif self.num_flags == 0 and self.score < self.NUM_MINES:
                self.lose()
            if self.grid[x, y] == -1:
                self.score += 1
            event.widget.config(bg='red')
            self.revealed_overlay[x, y] = 2
        text_to_set = "Flags", self.num_flags, "Total mines", self.NUM_MINES
        self.tk_text_label.config(text=text_to_set)
            
    # retract a suspected flag
    def unflag(self, event):        
        x = event.widget.grid_info()['row']
        y = event.widget.grid_info()['column']
        if self.revealed_overlay[x, y] != 2:
            return False
        else:
            self.num_flags += 1
            if self.grid[x, y] == -1:
                self.score -= 1
            event.widget.config(bg="gray")
            self.revealed_overlay[x, y] = 0
        text_to_set = "Flags", self.num_flags, "Total mines", self.NUM_MINES
        self.tk_text_label.config(text=text_to_set)
        
    def lose(self):
        if self.game_over:
            self.tk_root.destroy()
            exit()
        self.game_over=True
        text_to_set = "YOU LOSE"
        self.tk_text_label.config(text=text_to_set)
        print("Player lost.")
        self.revealed_overlay.fill(2)
        self.doReveal()
                    
    def win(self):
        if self.game_over:
            self.tk_root.destroy()
            exit()
        self.game_over=True
        text_to_set = "YOU WIN!!"
        self.tk_text_label.config(text=text_to_set)
        print("Player won.")
        self.revealed_overlay.fill(1)
        self.doReveal()

# todo gui: add flag counter
# difficulty presets / parameters
DIFF_EASY = [[8, 8], 10, "easy"]
DIFF_NORMAL = [[16, 16], 40, "normal"]
DIFF_EXPERT = [[16, 30], 99, "expert"]

game = Minesweeper(DIFF_NORMAL)

