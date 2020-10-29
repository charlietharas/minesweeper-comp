'''
Created on Oct 21, 2020

@author: Charlie Tharas
'''

import numpy as np
import random
import tkinter as tk

# difficulty presets / parameters
diff_easy = [[8, 8], 10, "easy"]
diff_normal = [[16, 16], 40, "normal"]
diff_expert = [[16, 30], 99, "expert"]
diff_select = diff_easy # change this for the difficulty

grid_x = diff_select[0][0]
grid_y = diff_select[0][1]
num_mines = diff_select[1]
num_flags = num_mines
score = 0 # flagged mines
print("Game settings at", diff_select[2],"difficulty,", grid_x, "by", grid_y, "grid with", num_mines, "mines.")

# values for tiles (for debugging)
# 0 is revealed (empty)
# 1, 2, 3 are representations of mines nearby
# -1 is mine
# -2 is start

# gui initialization
tk_root = tk.Tk()
tk_root.title("Minesweeper by Charlie")
tk_frame = tk.Frame(tk_root)
tk_button_list = []
for i in range(grid_x):
    for ii in range(grid_y):
        tk_button_list.append(tk.Button(tk_frame, activebackground='green'))
        tk_button_list[-1].grid(row=i, column=ii)
        
tk_frame.pack()

# grid generation
grid = np.zeros(shape=(grid_x, grid_y))
start = input("Insert a starter tile in form of x, y \n")
try:
    start_x = int(start.split(',')[1])-1
    start_y = int(start.split(',')[0])-1
except:
    print("There was an error with your start tile selection. The program has been terminated.")
    exit()
    
if start_x < 0 or start_y < 0 or start_x > grid_x-1 or start_y > grid_y-1:
    print("There was an error with your start tile selection. Your indicated tile is out of bounds.")
    exit()

grid[start_x, start_y] = -2
print("Successfully initialized start tile")

start_adjacent = []
for i in [-1, 0, 1]:
    for ii in [-1, 0, 1]:
        start_adjacent.append([start_x+i, start_y+ii])

# utility functions
# get adjacent mine count
def getMines(x, y):
    adj_mines = 0 
    if grid[x, y] == -1:
        return -1
    
    leftBorder, rightBorder, topBorder, bottomBorder = [True, True, True, True] # reverse values necessary for operations
    if x-1 < 0:
        leftBorder = False
    elif x+2 >= grid_x:
        rightBorder = False
    if y - 1 <0:
        topBorder = False
    elif y+2 >= grid_y:
        bottomBorder = False
        
    subsect = grid[x-leftBorder:x+(2*rightBorder), y-topBorder:y+(2*bottomBorder)].flatten()
    for i in subsect:
        if i == -1:
            adj_mines += 1
            
    return adj_mines

# get if position is unsuitable to generate mine at/change/use
def isUnusable(x, y):
    if grid[x, y] == -2 or grid[x, y] == -1:
        return True
    return False

# mine generation
# sets coordinates for mines
mines = []
rand_x, rand_y = [0, 0]
for i in range(num_mines):
    rand_x = random.randint(0, grid_x-1)
    rand_y = random.randint(0, grid_y-1)
    while [rand_x, rand_y] in mines or [rand_x, rand_y] in start_adjacent:
        rand_x = random.randint(0, grid_x-1)
        rand_y = random.randint(0, grid_y-1)
    mines.append([rand_x, rand_y])
    
print("Generated mines at coord list", mines)

# places mines
for i in mines:
    grid[i[0], i[1]] = -1

# marks amount of mines near tiles
for i in range(grid_x):
    for ii in range(grid_y):
        if isUnusable(i, ii):
            continue
        
        grid[i, ii] = getMines(i, ii)
        
print("Grid generated.")
print("GRID:")
print(grid)

# revealing overlay
# shows which grid items are visible to the player
revealed_overlay = np.zeros(shape=(grid_x, grid_y))
leftBorder, rightBorder, topBorder, bottomBorder = [True, True, True, True] # reverse values necessary for operations
if start_x-1 < 0:
        leftBorder = False
elif start_x >= grid_x:
    rightBorder = False
if start_y - 1 <0:
    topBorder = False
elif start_y >= grid_y:
    bottomBorder = False
        
# must fix revealed_overlay
revealed_overlay[start_x-leftBorder:start_x+(2*rightBorder), start_y-topBorder:start_y+(2*bottomBorder)].fill(1)

print("Designated revealed tiles.")
print("REVEALED OVERLAY:")
print(revealed_overlay)

# player functions
# player selects tile thinking it is not a mine. loses if it is a mine.
def reveal(x, y):
    if grid[x, y] == -1:
        lose() # pass x,y parameter to show user where they died?
    
    if revealed_overlay[x, y] == 0: # TODO recursively search nearby empty tiles to autoreveal them
        pass # todo
        
    revealed_overlay[x, y] = 1
   
# player flags tile thinking it is a mine. tile is not revealed until player runs out of flags. if player places all flags and gets >0 wrong, loses. 
def flag(x, y):
    if num_flags == 0 and score == num_mines:
        win()
    elif num_flags == 0 and score < num_mines:
        lose()
    num_flags -=1
    if grid[x, y] == -1:
        score += 1
        
# retract a suspected flag
def unflag(x, y):
    num_flags += 1
    if grid[x, y] == -1:
        score -= 1
    
# todo display loss message, add highlighted tile that player lost on, reveal all mines, etc
def lose():
    exit()

# todo display win message, reveal all mines
def win():
    print("You won!")
    
# todo plays game:
while score < num_mines:
    pass
    # todo add game

# todo game: recursive revealing
# todo gui: add start tile selection
# todo gui: add main game under gui
# then done!