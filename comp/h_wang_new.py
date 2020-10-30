import random

import time

import copy

import sys, os

os.system('cls')

horizontal = [0]

vertical = [0]

minenumber = [0]

def difficulty(a,b,c):
    difficult = input("Which difficulty would you like, beginner (10 mines), medium (40 mines), expert (16*30, 99 mines), or custom? ")
    while difficult != "beginner" and difficult != "medium" and difficult != "expert" and difficult != "custom":
        print ("\n")
        print ("That is not one of the options.")
        print ("\n")
        difficult = input("Which difficulty would you like, beginner (10 mines), medium (40 mines), expert (16*30, 99 mines), or custom? ")
    if difficult == "beginner":
        b[0] = random.randint(8,10)
        a[0] = b[0]
        c[0] = 10
    if difficult == "medium":
        b[0] = random.randint(13,16)
        a[0] = random.randint(15,16)
        c[0] = 40
    if difficult == "expert":
        b[0] = 30
        a[0] = 16
        c[0] = 99
    if difficult == "custom":
        customerow = input("Please input the number of rows you want (<31): ")
        while customrow > 30 or customrow != int:
            print ("That is not a valid answer.")
            customerow = input("Please input the number of rows you want (<31): ")
        a[0] = customrow
        customcolumn = input("Please input the number of columns you want (<27): ")
        while customcolumn > 26 or customcolumn != int:
            print ("That is not a valid answer.")
            customcolumn = input("Please input the number of columns you want (<27): ")
        b[0] = customcolumn
        custommine = input("Please input the number of mines you want : ")
        while custommine != int:
            print ("That is not a valid answer.")
            custommine = input("Please input the number of mines you want : ")
        if custommine >= a * b:
            c[0] = a[0] * b[0] - 1
        else:
            c[0] = custommine

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def game():

  start1 = [0]

  start2 = [0]

  os.system('cls')

  minefield = [[0 for i in range(0,horizontal[0])] for j in range (0,vertical[0])]

  playergrid = [["■" for i in range(0,horizontal[0])] for j in range (0,vertical[0])]

  def minecheck(x,y,z):
    row = z[x]
    y = row[y]
    return y

  timer = 0
  timer = time.time()

  def rowcount(a,b):
      flags = 0
      for i in range(0,b):
        row = a[i]
        flags += row.count("⚐")
      return flags

  def pretty(a,b,c):
    os.system('cls')
    print("time: ", timer, "                    ", "flags: ", rowcount(playergrid, vertical[0]))
    for i in range(0,b-1):
        print("   ", alphabet[i], end = "")
    print("   ", alphabet[b-1])
    print(" ", "-----" * b)
    for i in range(0,c):
      if i < 9:
          print("0"+str(i+1), end = "")
      else:
          print(i+1, end = "")
      for j in range(0,b-1):
          print("|", minecheck(i,j,a), " ", end = "")
      print("|", minecheck(i,b-1,a), "|")
      print(" ", "-----" * b)



  def allahs(a,b,c):
    x = random.randint(1,a)
    y = random.randint(1,b)
    bombsite = a[x]
    if x == start2[0] and y == start1[0]:
      return allahs(a,b,c)
    if not bombsite[y] == "☼":
      bombsite[y] = "☼"
    else:
      return allahs(a,b,c)

  def newvalue(x,y,z,a,b):
    if x in range(1,a):
        if y in range(1,b):
            for i in range (x-1,x+1):
                for j in range (x-1,x+1):
                    if minecheck (i,j,minefield) == "☼":
                        z = z + 1

    return z

  def change(a):
    letter = [alphabet[i] for i in range(0,vertical[0])]
    number = [i for i in range(0,horizontal[0])]
    for i in range(0,vertical):
      if letter[i] == a:
        a = number[i]
    return a

  def start(a,b,c,d,e):
    starting = input("Choose your first tile to start with by typing the coordinates of the tile, letter first.")
    number = [i for i in range(0,31)]
    if len(starting) == 2 or starting[0] in alphabet or starting[1] in number:
      d = int(change(starting[0]))
      e = int(starting[1])
    else:
      print ("That is not a valid square.")
      print ("\n")
      return start(horizontal[0], vertical[0], minenumber, start1[0], start2[0])
    startmine = minecheck(start2[0],start1[0],minefield)
    playergrid[start2[0]][start1[0]] = startmine
    for i in range(0,c):
      allahs(minefield)
    for c in range(1,a):
      for d in range(1,b):
        value = minecheck(c,d,minefield)
        if value == "☼":
          newvalue(c,d,minefield)
    zero(playergrid,minefield,start2[0],start1[0],horizontal[0],vertical[0])
    return (start1[0],start2[0])

  pretty(playergrid ,horizontal[0], vertical[0])

  start(horizontal[0], vertical[0], minenumber, start1[0], start2[0])

  def flag(y,x,b):
    row = b[y]
    if row[x] == "⚐":
      row[x] = "■"
    elif row[x] != "⚐" and row[x] != "■":
      return pretty(playergrid, horizontal[0], vertical[0])
    else:
      row[x] = "⚐"
    return pretty(playergrid, horizontal[0], vertical[0])

  def quit():
    os.system('cls')
    quitting = input("")
    return quit()

  def play(a,b,timer,c,d,e):
    x,y = choose(a,b,timer)
    mine = minecheck(y,x,a)
    if mine == "☼":
      pretty(minefield, horizontal[0], vertical[0])
      print ("You exploded like the children they used for minesweeping.")
      print ("Time: " + str(round(time.time() - timer)) + "s")
      again = input("Play again?")
      while again != "yes" and again != "no":
        print ("That is not a valid answer!")
        again = input("Play again?")
      if again == "yes":
        difficulty(horizontal, vertical, minenumber)
        game()
      else:
        quit()
    b[y][x] = mine
    pretty(playergrid, horizontal[0], vertical[0])
    blanksquare = 0
    for i in range(0,c):
      row = b[i]
      blanksquare += row.count("■")
      blanksquare += row.count("⚐")
    if blanksquare == e:
      pretty(minefield, horizontal[0], vertical[0])
      print("You swept those mines so hard.")
      print ("Time: " + str(round(time.time() - timer)) + "s")
      again = input("Play again?")
      while again != "yes" and again != "no":
        print ("That is not a valid answer!")
        again = input("Play again?")
      if again == "yes":
        difficulty(horizontal, vertical, minenumber)
        game()
      else:
        quit()
    return play(a,b,timer,horizonal[0],vertical[0],minenumber[0])

  def choose(a,b,timer):
    letter = [alphabet[i] for i in range(0,vertical[0])]
    number = [i for i in range(0,horizontal[0])]
    choice = input("To flag or unflag a tile, add \"f\" before the coordinates of the tile, letter first. To check a tile, type the coordinates of the tile, letter first. ").lower()
    if len(choice) == 3 and choice[0] == "f" and choice[1] in letter and choice[2] in number:
      x = int(change(choice[1]))
      y = int(choice[2])
      flag(y,x,b)
      return play(a,b,timer,horizonal[0],vertical[0],minenumber[0])
    if len(choice) == 2 and choice[0] in letter and choice[1] in number:
      newx = int(change(choice[0]))
      if minecheck(int(choice[1]),newx,a) == "⚐":
        sure = input("There is a flag here. Are you sure you want to check this tile?").lower()
        while sure != "yes" and sure != "no":
          print("That is not a valid answer!")
          sure = input("There is a flag here. Are you sure you want to check this tile?").lower()
        if sure == "no":
          return play(a,b,timer,horizona[0],vertical[0],minenumber[0])
        else:
          return(newx, int(choice[1]))
      return(newx, int(choice[1]))
    else:
      os.system('cls')
      print ("Incorrect.")
      print ("\n")
      pretty(playergrid, horizontal[0], vertical[0])
      return play(a,b,timer,horizonal[0],vertical[0],minenumber[0])

  play(minefield,playergrid,timer,horizonal[0],vertical[0],minenumber[0])

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
  difficulty(horizontal, vertical, minenumber)
  game()
