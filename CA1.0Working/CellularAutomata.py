# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 19:39:52 2019

@author: zeno
"""


class Cell:    
    
    def __init__(self, chanceOfLife=0.5):
        import random
        self.state = 0
        self.prevState = 0
        self.lived = 0
        self.liveNeighboors = 0
        self.address = (None, None)
        if random.random() <= chanceOfLife:
            self.state = 1
            self.prevState = 1
            self.lived +=1
    
    def getState(self):
        return self.state
    
    
    def setState(self,state):
        self.state = state
        if state == 1:
            self.lived += 1
        
        
    def copyState(self):
        self.prevState = self.state
    
    def getPrevState(self):
        return self.prevState
    
    
    def getNumLived(self):
        return self.lived
    
    
    def getLiveNeighboors(self):
        return self.liveNeighboors


class Automata:
    def __init__(self, rows = 100, cols = 100, chanceOfLife = 0.5, start = []):
        self.rows = rows
        self.cols = cols
        self.numCells = rows*cols
        
        self.cells = []
        self.cellStates = []
        for r in range(rows):
            row = []
            cellStateRow = []
            for c in range(cols):
                cell = self.makeCell(chanceOfLife)
                cell.address = (r, c)
                row.append(cell)
                cellStateRow.append(cell.state)
            self.cells.append(row)
            self.cellStates.append(cellStateRow)
        
        self.assignLiveNeighboors()
        #self.assignAddresses()
       
    # def assignAddresses(self):
    #     for row in self.cells:
    #         for cell in row:
    #             cell.address = self.cells.index(row), self.cells[self.cells.index(row)].index(cell)

    def makeCell(self, chanceOfLife):
        return Cell(chanceOfLife)
    

    def nextGen(self):
        # for r in range(len(self.cells)):
        #     for c in range(len(self.cells[r])):
        #        self.cells[r][c].copyState()
               
        self.applyRules()
        self.assignLiveNeighboors()
        
        
    def applyRules(self):
        for row in self.cells:
            for cell in row:
                cell.copyState()
                if cell.prevState == 0:
                    if cell.liveNeighboors == 3:
                        cell.state = 1
                    else:
                        cell.state = 0
                if cell.prevState == 1:
                    if cell.liveNeighboors == 2 or cell.liveNeighboors == 3:
                        cell.state = 1
                    else:
                        cell.state = 0
    
            
    def assignLiveNeighboors(self):               
        for i in range(self.rows):
            for j in range(self.cols):
                
                iprev = (i - 1) % self.rows
                inext = (i + 1) % self.rows
                jprev = (j - 1) % self.cols
                jnext = (j + 1) % self.cols
                
                numLive = 0
                numLive += self.cells[iprev][jprev].state
                numLive += self.cells[iprev][j].state
                numLive += self.cells[iprev][jnext].state
                numLive += self.cells[i][jprev].state
                numLive += self.cells[i][jnext].state
                numLive += self.cells[inext][jprev].state
                numLive += self.cells[inext][j].state
                numLive += self.cells[inext][jnext].state
                
                self.cells[i][j].liveNeighboors = numLive    
                
    
    def getCells(self):
        return self.cells
        
        
def main():
    aut = Automata()
    cell = aut.cells[2][2]
    print(cell.state, cell.prevState, cell.liveNeighboors, cell.address)
    aut.nextGen()
    print(cell.state, cell.prevState, cell.liveNeighboors, cell.address)
    aut.nextGen()
    print(cell.state, cell.prevState, cell.liveNeighboors, cell.address)
    aut.nextGen()
    print(cell.state, cell.prevState, cell.liveNeighboors, cell.address)
    aut.nextGen()
    print(cell.state, cell.prevState, cell.liveNeighboors, cell.address)
    aut.nextGen()
    print(cell.state, cell.prevState, cell.liveNeighboors, cell.address)
    
    print(aut.cellStates[1][1:4])
    print(aut.cellStates[2][1:4])
    print(aut.cellStates[3][1:4])

if __name__ == '__main__':
    main()

