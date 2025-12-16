import os
import sys
import math
import random
import tkinter as tk
from functools import partial

os.chdir("/home/messlemont/Documents/Projects/Minesweeper")

#_____TO DO_____
# - safe_cell func
# - reset on gameover
# - Stopwatch
# - 


# Each game cell is a button
def game_cell(root , cell_values , x , y , cell_dict ):
    cell = tk.Button(root , text=cell_values[x][y] , command=partial(on_click ,x,y , cell_dict, cell_values , root),
                     bg="lightgray" , disabledforeground="lightgray" , overrelief="raised" , activebackground="pink" , activeforeground="white")
    #cell.image = tk.PhotoImage(file="brick.png")
    return cell

# Assigns which cells are mines
def set_mines(rows , cols , cell_values , mine_count):
    count = 0
    #loop until we have mine_count amount of mines
    while (count < mine_count):
        #Random coorsds, set as a mine if not already set
        x = random.randint(0 , rows - 1)
        y = random.randint(0 , cols - 1)
        print("X,Y: " + str(x) + "." + str(y))
        if cell_values[x][y] != 'M':
            cell_values[x][y] = 'M'
            count +=1
        print(count)

# Assigns values to non-mine cells based on number of surronding mines
def set_values(root , rows, cols, cell_values , cell_dict):
    #Loop through grid
    for x in range(rows):
        for y in range(cols):

            #Next value reset
            value = 0

            #Skip if it's a mine
            if cell_values[x][y] == 'M':
                cell_values[x][y] = 'M'
                cell_dict[(x,y)] = (game_cell(root , cell_values , x , y, cell_dict)).grid(row=x , column=y)
                continue

            #Check neighbour cells, starting TL and going clockwise
            if (x > 0) and (y > 0) and  cell_values[x-1][y-1] == 'M':
                value += 1
            if (y > 0) and cell_values[x][y-1] == 'M':
                value += 1
            if (x < rows-1) and (y > 0) and cell_values[x+1][y-1] == 'M':
                value += 1
            if (x < rows-1) and cell_values[x+1][y] == 'M':
                value +=1
            if (x < rows-1) and (y < cols-1) and cell_values[x+1][y+1] == 'M':
                value +=1
            if (y < rows-1) and cell_values[x][y+1] == 'M':
                value += 1
            if (x > 0) and (y < cols-1) and cell_values[x-1][y+1] == 'M':
                value += 1
            if (x > 0) and cell_values[x-1][y]  == 'M':
                value += 1
            
            #Cell is assigned Value, indicating the amount of surronding mines
            cell_values[x][y] = value
            cell_dict[(x,y)] = (game_cell(root , cell_values , x , y, cell_dict )).grid(row=x , column=y)

# Handles click events, ends the game or calls a func to check adjacent tiles
def on_click(x , y , cell_dict, cell_values , root):
    gameOver = False

    if cell_values[x][y] == 'M':
        gameOver = True
        for ele in root.winfo_children():
            ele.destroy()
        root.configure(background="black")
        gameOverText = tk.Label(root, text="GAME OVER. space to reset" , bg="black" , fg="red"  , bd = 20, font=("Arial", 16, "bold"))
        #gameOverText.bind("<space>", os.execl(sys.executable, sys.executable, *sys.argv))
        gameOverText.pack()
    else:
        safe_cell()

# Displays cell value, if 0 then all neighbouring cells must be displayed until a non-0 value is encountered
def safe_cell():
    pass



def main():
    root = tk.Tk()
    root.title = "MINESWEEPER GAME"

    score = 0

    # Grid Parameters
    rows = 10
    cols = 10
    mine_count = 25
    # True values of the cells
    cell_values = [[0 for y in range(cols)] for x in range(rows)]
    # Dictionary of buttons shown to the player
    cell_dict = {}
    # Position of flags placed by the player
    flags = []

    set_mines(rows , cols , cell_values , mine_count)
    print("MINES SET")
    set_values(root , rows, cols, cell_values , cell_dict)
    print("VALUES SET")
    cwd = os.getcwd()
    print(cwd)

    root.mainloop()

main()