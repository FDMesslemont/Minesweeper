import os
import sys
import math
import random
import tkinter as tk
from functools import partial

os.chdir("C:/Users/GLA.Local/Documents/Minesweeper")
sys.setrecursionlimit(1000)

#_____TO DO_____
# - safe_cell func
# - Stopwatch
# - Flagging
# - Win condition
# - Dynamic sizing

#, text=cell_values[x][y] 

# Each game cell is a button
def game_cell(root , cell_values , x , y , cell_dict , cell_shown):
    #image of unchecked cells
    global brick
    brick = tk.PhotoImage(file="block.png") # 60x60
    #creates the game cell as a button
    cell = tk.Button(root , image=brick, command=partial(on_click ,x,y , cell_dict, cell_values , root , cell_shown),
                     bg="lightgray" , disabledforeground="lightgray" , overrelief="raised" , activebackground="pink" , activeforeground="white")
    cell.image = brick
    cell.bind("<ButtonRelease-3>", partial(handle_flag , x , y , cell_dict , cell_shown))
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
def set_values(root , rows, cols, cell_values , cell_dict , cell_shown):
    #Loop through grid
    for x in range(rows):
        for y in range(cols):

            #Next value reset
            value = 0

            #Create the cell for a mine, but it's value is already 'Mine'
            if cell_values[x][y] == 'M':
                cell_values[x][y] = 'M'
                cell_dict[(x,y)] = (game_cell(root , cell_values , x , y, cell_dict , cell_shown))
                cell_dict[(x,y)].grid(row=x , column=y)
                cell_shown[(x,y)] = False
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
            if (y < cols-1) and cell_values[x][y+1] == 'M':
                value += 1
            if (x > 0) and (y < cols-1) and cell_values[x-1][y+1] == 'M':
                value += 1
            if (x > 0) and cell_values[x-1][y]  == 'M':
                value += 1
            
            #Cell is assigned Value, indicating the amount of surronding mines
            cell_values[x][y] = value
            #The button representing the game cell is added to a dictionary and placed in it's grid position
            cell_dict[(x,y)] = game_cell(root , cell_values , x , y, cell_dict , cell_shown)
            cell_dict[(x,y)].grid(row=x , column=y)
            #Add to dict of exposed cells and set to false
            cell_shown[(x,y)] = False


# Handles click events, ends the game or calls a func to check adjacent tiles
def on_click(x , y , cell_dict, cell_values , root , cell_shown):
    if cell_values[x][y] == 'M':
        game_over(root)
    else:
        safe_cell(x , y , cell_values, cell_dict , cell_shown)

# Displays cell value, if 0 then all neighbouring cells must be displayed until a non-0 value is encountered
def safe_cell(x , y , cell_values, cell_dict , cell_shown):
   #Prevents us from checking already exposed cells
    if cell_shown[(x,y)] == False and ((x,y) not in flags):
        #Reveal the cell value by updating the image, add cell to our dict of exposed cells
        match cell_values[x][y]:
            case 1:
                cell_dict[(x,y)].config(image=score1)
                cell_shown[(x,y)] = True
            case 2:
                cell_dict[(x,y)].config(image=score2)
                cell_shown[(x,y)] = True
            case 3:
                cell_dict[(x,y)].config(image=score3) 
                cell_shown[(x,y)] = True
            case 4:
                cell_dict[(x,y)].config(image=score4)
                cell_shown[(x,y)] = True
            case 5:
                cell_dict[(x,y)].config(image=score5)
                cell_shown[(x,y)] = True
            case 6:
                cell_dict[(x,y)].config(image=score6)
                cell_shown[(x,y)] = True
            case 7:
                cell_dict[(x,y)].config(image=score7)
                cell_shown[(x,y)] = True
            case 8:
                cell_dict[(x,y)].config(image=score8)
                cell_shown[(x,y)] = True
            #When the cell is blank, we need to reveal all the neighbouring cells too
            case 0:
                cell_dict[(x,y)].config(image=score0)
                cell_shown[(x,y)] = True

                #Check neighbour cells, starting TL and going clockwise - can't call func if there is no neighbouring cell
                if (x > 0) and (y > 0):
                    safe_cell(x-1 , y-1 , cell_values , cell_dict , cell_shown)
                if (y > 0):
                    safe_cell(x , y-1 , cell_values , cell_dict , cell_shown)
                if (x < rows-1) and (y > 0) :
                    safe_cell(x+1 , y-1 , cell_values , cell_dict , cell_shown)
                if (x < rows-1) :
                    safe_cell(x+1 , y , cell_values , cell_dict , cell_shown)
                if (x < rows-1) and (y < cols-1):
                    safe_cell(x+1 , y+1 , cell_values , cell_dict , cell_shown)
                if (y < rows-1):
                    safe_cell(x , y+1 , cell_values , cell_dict , cell_shown)
                if (x > 0) and (y < cols-1):
                    safe_cell(x-1 , y+1 , cell_values , cell_dict , cell_shown)
                if (x > 0):
                    safe_cell(x-1 , y , cell_values , cell_dict , cell_shown)

def handle_flag(x , y , cell_dict , cell_shown , event):
    #Check if unexposed
    if cell_shown[(x,y)] == False:
        #If not flagged, flag
        if (x,y) not in flags:
            flags.append((x,y))
            cell_dict[(x,y)].config(image=flagged)
            cell_dict[(x,y)]['state'] = tk.DISABLED
        #if flagged, unflag
        else:
            flags.remove((x,y))
            cell_dict[(x,y)].config(image=brick)
            cell_dict[(x,y)]['state'] = tk.ACTIVE
    #Can't flag exposed cells
    else:
        pass

def game_over(root):
    for ele in root.winfo_children():
        ele.destroy()
    root.configure(background="black")
    gameOverText = tk.Button(root, text="GAME OVER. Press to reset" , command=restart, bg="darkgray" , fg="red"  , bd = 20, font=("Arial", 16, "bold"))
    gameOverText.pack()


def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    root = tk.Tk()
    root.title = "MINESWEEPER GAME"

    global flagged
    flagged = tk.PhotoImage(file="flag.png")
    global score0
    score0 = tk.PhotoImage(file="0.png")
    global score1
    score1 = tk.PhotoImage(file="1.png")
    global score2
    score2 = tk.PhotoImage(file="2.png")
    global score3
    score3 = tk.PhotoImage(file="3.png")
    global score4
    score4 = tk.PhotoImage(file="4.png")
    global score5
    score5 = tk.PhotoImage(file="5.png")
    global score6
    score6 = tk.PhotoImage(file="6.png")
    global score7
    score7 = tk.PhotoImage(file="7.png")
    global score8
    score8 = tk.PhotoImage(file="8.png")

    # Grid Parameters
    global rows
    rows = 15
    global cols
    cols = 12
    mine_count = 20
    # True values of the cells
    cell_values = [[0 for y in range(cols)] for x in range(rows)]
    # Dictionary of buttons shown to the player
    cell_dict = {}
    #Dictionary of bools, tells us if the cell at X,Y has been exposed
    cell_shown = {}
    # Position of flags placed by the player
    global flags
    flags = []

    set_mines(rows , cols , cell_values , mine_count)
    print("MINES SET")
    set_values(root , rows, cols, cell_values , cell_dict , cell_shown)
    print("VALUES SET")
    print(cell_dict)
    cwd = os.getcwd()
    print(cwd)

    root.mainloop()

main()