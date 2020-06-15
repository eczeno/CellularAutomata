import tkinter as tk
import CellularAutomata

aut = CellularAutomata.Automata(rows = 40, cols = 40)
numRows = aut.rows
numCols = aut.cols


root = tk.Tk()
tk.Grid.rowconfigure(root, 0, weight = 1)
tk.Grid.columnconfigure(root, 0, weight = 1)
root.geometry('800x600')

window = tk.PanedWindow(root, orient = 'vertical')
window.grid(row = 0, column = 0, sticky = 'NSEW')



controlFrame = tk.Frame(window)
window.add(controlFrame)
title = tk.Label(controlFrame, text = 'Cellular Automata')
title.grid(sticky = 'NSEW')


gridFrame = tk.Frame(window)
window.add(gridFrame)


class cellButton(tk.Button):
    def __init__(self, master = None, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.address = (None, None)

        self.config(bg = 'black', borderwidth = 0.5, command = self.clicked)
        self.grid(sticky = 'NSEW')
    
    def clicked(self):
        row = self.address[0]
        col = self.address[1]    
        if aut.cells[row][col].state == 1:
            aut.cells[row][col].setState(0)            
        elif aut.cells[row][col].state == 0:
            aut.cells[row][col].setState(1)        
        aut.assignLiveNeighboors()
        self.linkCell(aut.cells[row][col])


    def linkCell(self, cell):
        assert(self.address == cell.address)
        if cell.state == 1:
            self.config(bg = 'white')
        elif cell.state == 0:
            self.config(bg = 'black')
        
        
cellButtons = {}
for row in range(numRows):
    tk.Grid.rowconfigure(gridFrame, row, weight = 1)
    cellButtons[row] = {}
    for column in range(numCols):
        tk.Grid.columnconfigure(gridFrame, column, weight = 1)
        cellButtons[row][column] = cellButton(gridFrame)
        cellButtons[row][column].grid(row = row, column = column, sticky = 'NSEW')
        cellButtons[row][column].address = (row, column)
        cellButtons[row][column].linkCell(aut.cells[row][column])


def update():
    aut.nextGen()
    for row in aut.cells:
        for cell in row:
            cellButtons[cell.address[0]][cell.address[1]].linkCell(cell)
            
def play():
    global running
    update()
    running = root.after(100, play)

def stop():
    global running
    root.after_cancel(running)


nextButton = tk.Button(controlFrame, text = 'next', command = update)
nextButton.grid()

playButton = tk.Button(controlFrame, text = 'play', command = play)
playButton.grid(row = 1, column = 2)

stopButton = tk.Button(controlFrame, text = 'stop', command = stop)
stopButton.grid(row = 1, column = 3)

root.mainloop()
