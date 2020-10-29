import random

import time

import copy

import sys, os


os.system('cls')

start1 = 0

start2 = 0

def game():

  os.system('cls')

  minefield = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

  playergrid = [["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],["■", "■", "■", "■", "■", "■", "■", "■", "■", "■"]]

  def minecheck(x,y,z):
    row = z[x]
    y = row[y]
    return y

  def pretty(a):
    os.system('cls')
    print("    A   B   C   D   E   F   G   H   I   J")
    print("  -----------------------------------------")
    for i in range(0,10):
      print(i, "|", minecheck(i,0,a), "|", minecheck(i,1,a), "|", minecheck(i,2,a), "|", minecheck(i,3,a), "|", minecheck(i,4,a), "|", minecheck(i,5,a), "|", minecheck(i,6,a), "|", minecheck(i,7,a), "|", minecheck(i,8,a), "|", minecheck(i,9,a), "|", )
      print("  -----------------------------------------")

  def open(y,x,b,a):
    if y - 1 > -1:
      row = b[y-1]
      if x - 1 > -1:
        row[x-1] = minecheck(y-1,x-1,a)
      row[x] = minecheck(y-1,x,a)
      if x + 1 < 10:
        row[x+1] = minecheck(y-1,x+1,a)

    row = b[y]
    if x - 1 > -1:
      row[x-1] = minecheck(y,x-1,a)
    if x + 1 < 10:
      row[x+1] = minecheck(y,x+1,a)

    if y + 1 < 10:
      row = b[y+1]
      if x - 1 > -1:
        row[x-1] = minecheck(y+1,x-1,a)
      row[x] = minecheck(y+1,x,a)
      if x + 1 < 10:
        row[x+1] = minecheck(y+1,x+1,a)

  def allahs(a):
    x = random.randint(0,9)
    y = random.randint(0,9)
    bombsite = a[x]
    if x == start2 and y == start1:
      return allahs(a)
    if start2 - 1 > -1:
      if start1 - 1 > -1:
        if x == start2 - 1 and y == start1 - 1:
          return allahs(a)
      if x == start2 - 1 and y == start1:
        return allahs(a)
      if start1 + 1 < 10:
        if x == start2 - 1 and y == start1 + 1:
          return allahs(a)
    if start1 - 1 > -1:
      if x == start2 and y == start1 - 1:
        return allahs(a)
    if start1 + 1 < 10:
      if x == start2 and y == start1 + 1:
        return allahs(a)
    if start2 + 1 < 10:
      if start1 - 1 > -1:
        if x == start2 + 1 and y == start1 - 1:
          return allahs(a)
      if x == start2 + 1 and y == start1:
        return allahs(a)
      if start1 + 1 < 10:
        if x == start2 + 1 and y == start1 + 1:
          return allahs(a)
    if not bombsite[y] == "☼":
      bombsite[y] = "☼"
    else:
      return allahs(a)

  def newvalue(x1,y,z):
    if x1 - 1 > -1:
      x = z[x1-1]
      if y - 1 > -1:
        if not x[y-1] == "☼":
          x[y-1] = x[y-1] + 1
      if not x[y] == "☼":
        x[y] = x[y] + 1
      if y + 1 < 10:
        if not x[y+1] == "☼":
          x[y+1] = x[y+1] + 1

    x = z[x1]
    if y - 1 > -1:
      if not x[y-1] == "☼":
        x[y-1] = x[y-1] + 1
    if y + 1 < 10:
      if not x[y+1] == "☼":
        x[y+1] = x[y+1] + 1


    if x1 + 1 < 10:
      x = z[x1+1]
      if y - 1 > -1:
        if not x[y-1] == "☼":
          x[y-1] = x[y-1] + 1
      if not x[y] == "☼":
        x[y] = x[y] + 1
      if y + 1 < 10:
        if not x[y+1] == "☼":
          x[y+1] = x[y+1] + 1

  def zero(b,a,y,x):
    grid = copy.deepcopy(b)
    open(y,x,b,a)
    if grid == b:
      return
    while True:
      grid = copy.deepcopy(b)
      for e in range(10):
        for f in range(10):
          if minecheck(e,f,b) == 0:
            open(e,f,b,a)
      if grid == b:
        return

  def start():
    global start1
    global start2
    starting = input("Choose your first tile to start with by typing the coordinates of the tile, letter first.")
    letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if len(starting) == 2 and starting[0] in letter and starting[1] in number:
      start1 = int(change(starting[0]))
      start2 = int(starting[1])
    else:
      print ("Incorrect.")
      print ("\n")
      return start()
    startmine = minecheck(start2,start1,minefield)
    playergrid[start2][start1] = startmine
    for i in range(0,15):
      allahs(minefield)
    for c in range(0,10):
      for d in range(0,10):
        value = minecheck(c,d,minefield)
        if value == "☼":
          newvalue(c,d,minefield)
    zero(playergrid,minefield,start2,start1)
    return (start1,start2)

  def change(a):
    letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(0,10):
      if letter[i] == a:
        a = number[i]
    return a

  pretty(playergrid)

  timer = time.time()

  start()

  pretty(playergrid)

  def flag(y,x,b):
    row = b[y]
    if row[x] == "⚐":
      row[x] = "■"
    elif row[x] != "⚐" and row[x] != "■":
      return pretty(b)
    else:
      row[x] = "⚐"
    return pretty(b)


  def quit():
    os.system('cls')
    quitting = input("")
    return quit()

  def play(a,b,timer):
    x,y = choose(a,b,timer)
    mine = minecheck(y,x,a)
    if mine == "☼":
      pretty(a)
      print ("Boom! Explosion! Death!")
      print ("Time: " + str(round(time.time() - timer)) + "s")
      again = input("Play again?")
      while again != "yes" and again != "no":
        print ("That is not a valid answer!")
        again = input("Play again?")
      if again == "yes":
        game()
      else:
        quit()
    b[y][x] = mine
    if mine == 0:
      zero(b,a,y,x)
    pretty(b)
    blanksquare = 0
    for i in range(0,10):
      row = b[i]
      blanksquare += row.count("■")
      blanksquare += row.count("⚐")
    if blanksquare == 15:
      pretty(a)
      print("No boom, explosion, or death. Congratulations!")
      print ("Time: " + str(round(time.time() - timer)) + "s")
      again = input("Play again?")
      while again != "yes" and again != "no":
        print ("That is not a valid answer!")
        again = input("Play again?")
      if again == "yes":
        game()
      else:
        quit()
    return play(a,b,timer)

  def choose(a,b,timer):
    letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    choice = input("To flag or unflag a tile, add \"f\" before the coordinates of the tile, letter first. To check a tile, type the coordinates of the tile, letter first. ").lower()
    if len(choice) == 3 and choice[0] == "f" and choice[1] in letter and choice[2] in number:
      x = int(change(choice[1]))
      y = int(choice[2])
      flag(y,x,b)
      return play(a,b,timer)
    if len(choice) == 2 and choice[0] in letter and choice[1] in number:
      newx = int(change(choice[0]))
      if minecheck(int(choice[1]),newx,a) == "⚐":
        sure = input("There is a flag here. Are you sure you want to check this tile?").lower()
        while sure != "yes" and sure != "no":
          print("That is not a valid answer!")
          sure = input("There is a flag here. Are you sure you want to check this tile?").lower()
        if sure == "no":
          return play(a,b,timer)
        else:
          return(newx, int(choice[1]))
      return(newx, int(choice[1]))
    else:
      os.system('cls')
      print ("Incorrect.")
      print ("\n")
      pretty(b)
      return play(a,b,timer)

  play(minefield,playergrid,timer)

print("Welcome to Minesweeper! \nType 'play' to start the game. \nType 'help' to learn how to play.")

pp = input().lower()
while pp != 'play':
  if pp == "help":
    print ("\n")
    print("Minesweeper is a game where the objective is to uncover all the tiles that are not mines. If you hit a mine, you lose. To identify which tiles are mines, there will be numbers next to the tiles representing how many mines are adjacent to the area in a 3 by 3 area. That means that if you see a '1' and there is only one uncleared tile adjacent to the '1,' then chances are, that tile is a mine. To keep track of which tiles are mine, type 'f' in front the the coordinate, which will mark that coordinate on the grid with a flag. In this version of Minesweeper, there are only 15 mines, so once all but 15 tiles are uncovered, you win.")
    print ("\n")
    print("Now type something else please.")
    pp = input().lower()
  else:
    print("That is not one of the options.")
    pp = input().lower()
if pp == 'play':
  game()
