# Gui with classes and buffer.
import tkinter as tk
import numpy as np
import matplotlib as mpl
import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import pillow

arrayFigure = Figure(figsize = (6,6), dpi = 100)
arrayAxes = arrayFigure.add_subplot(111)

import CellularAutomata

class CellButton(tk.Button):

    def __init__(self, master = None, cell = None):
        super().__init__(master)
        self.cell = cell
        self.address = self.cell.address
        self.config(bg = 'black', borderwidth = 0.3, command = self.clicked)
        self.grid(sticky = 'NSEW')
    
    def clicked(self):
        if self.cell.state == 1:
            self.cell.setState(0)
        elif self.cell.state == 0:
            self.cell.setState(1)
        self.master.automata.assignLiveNeighboors()
        self.linkCell()    
        
    def linkCell(self):
        if self.cell.state == 1:
            self.config(bg = 'white')
        elif self.cell.state == 0:
            self.config(bg = 'black')



class CellButtonArray(tk.Frame):
    
    def __init__(self, master = None, automata = None, rows = None, cols = None):
        super().__init__(master)  
        self.automata = automata     
        self.rows = rows
        self.cols = cols
        #self.stateImage = pillow.Image.fromarray(self.stateArray)
        self.cellButtons = {}
        for row in range(self.rows):
            tk.Grid.rowconfigure(self, row, weight = 1)
            self.cellButtons[row] = {}
            for col in range(self.cols):
                tk.Grid.columnconfigure(self, col, weight = 1)
                cell = self.automata.cells[row][col]
                self.cellButtons[row][col] = CellButton(self, cell = cell)
                self.cellButtons[row][col].grid(row = row, column = col, sticky = 'NSEW')
                self.cellButtons[row][col].address = row, col
                self.cellButtons[row][col].linkCell()
        
        


class caMainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        import CellularAutomata
        self.automata = CellularAutomata.Automata(rows= 340, cols = 340)
        self.rows = self.automata.rows
        self.cols = self.automata.cols


        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        self.geometry('470x500')

        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill = 'both', expand = True)

        self.ControlFrame = tk.Frame(self.mainFrame)
        title = tk.Label(self.ControlFrame, text = 'Cellular Automata')
        title.pack(side = 'top')
        self.ControlFrame.pack(side = 'top')

        self.arrayHolderFrame = tk.Frame(self.mainFrame)
        self.arrayHolderFrame.pack(side = 'bottom', fill = 'both', expand = True)

        # self.CellButtonArrayFrame = CellButtonArray(self.arrayHolderFrame, automata = self.automata, rows = self.rows, cols = self.cols)
        # self.CellButtonArrayFrame.place(x = 0, y = 0, relheight = 1., relwidth = 1.)

        self.imageFrame = tk.Frame(self.arrayHolderFrame)
        self.imageFrame.place(x = 0, y = 0, relheight = 1., relwidth = 1.)

        self.canvas = FigureCanvasTkAgg(arrayFigure, self.imageFrame)
        arrayAxes.imshow(self.automata.cellStates, aspect = 'auto', extent = (0, self.rows, 0, self.cols))
        arrayAxes.set_axis_off()
        arrayFigure.tight_layout()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = 'both', anchor = 'center', expand = True)

        #self.CellButtonArrayFrame.lift()

        self.nextButton = tk.Button(self.ControlFrame, text = 'next', command = self.update)
        self.nextButton.pack(side = 'right')

        self.playButton = tk.Button(self.ControlFrame, text = 'play', command = self.play)
        self.playButton.pack(side = 'left')

        self.stopButton = tk.Button(self.ControlFrame, text = 'stop', command = self.stop)
        self.stopButton.pack(side = 'left')

    def update(self):
        self.automata.nextGen()
        arrayAxes.clear()
        arrayAxes.imshow(self.automata.cellStates, aspect = 'auto', extent = (0, self.rows, 0, self.cols))
        arrayAxes.set_axis_off()
        arrayFigure.tight_layout()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = 'both', anchor = 'center', expand = True)
        # for row in self.automata.cells:
        #     for cell in row:
        #         self.CellButtonArrayFrame.cellButtons[cell.address[0]][cell.address[1]].linkCell()

    def play(self):
        global running
        self.update()
        running = self.after(100, self.play)
    
    def stop(self):
        global running
        try:
            self.after_cancel(running)
        except:
            pass
        
        
def runApp():
    app = caMainApp()
    app.mainloop()

if __name__ == '__main__':
    runApp()