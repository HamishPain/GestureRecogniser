from random import random
from time import sleep
from math import cos, sin
import os
PI = 3.1415


class GameOverlord():
    def __init__(self, sizeOfBoard):
        self.size = sizeOfBoard
        self.gameBoard = self.makeArray(sizeOfBoard)
        self.deltaBoard = self.makeArray(sizeOfBoard)
        
    def makeArray(self, size):
        list = []
        for i in range(size):
            column = []
            for j in range(size):
                column.append(0)
            list.append(column)
            column = None
        return list[:]

    def getPoint(self, x, y):
        x = x % self.size
        y = y % self.size
        if x < 0: x = self.size-1
        if y < 0: y = self.size-1
        if x < self.size and x >= 0 and y < self.size and y >= 0:
            return self.gameBoard[x][y]
        else:
            return 0

    def countNeighbours(self, x, y):
        neighbourSum = self.getPoint(x+1, y) + self.getPoint(x, y+1) + self.getPoint(x-1, y) + self.getPoint(x, y-1) + self.getPoint(x+1, y+1) + self.getPoint(x+1, y-1) + self.getPoint(x-1, y+1) + self.getPoint(x-1, y-1)
        return neighbourSum

    def evaluateLife(self, currentlyAlive, neighbourCount):
        if neighbourCount > 3:
            return 0
        elif neighbourCount < 2:
            return 0
        elif neighbourCount == 3:
            return 1
        elif currentlyAlive and neighbourCount == 2:
            return 1
        else:
            return 0

    def evaluatePoint(self, x, y):
        ownState = self.getPoint(x,y)
        neighbourCount = self.countNeighbours(x,y)
        newPoint = self.evaluateLife(ownState, neighbourCount)
        return newPoint
        
    def updateBoard(self):
        self.gameBoard = self.deltaBoard[:]

    def updateStates(self):
        a = []
        for x in range(self.size):
            b = []
            for y in range(self.size):
                deltaState = self.evaluatePoint(x, y)
                b.append(deltaState)
                #self.setDeltaPoint(x, y, deltaState)
            a.append(b)
        
        return a[:]

    def randomise(self, chance):
        for x in range(self.size):
            for y in range(self.size):
                self.setDeltaPoint(x, y, random() < chance)
        self.updateBoard()

    def printBoard(self):
        boardString = ""
        for x in range(self.size):
            for y in range(self.size):
                pointState = self.getPoint(x, y)
                char = '.'
                if pointState:
                    char = '0'
                boardString += char + ' '
            boardString += '\n'
        print(boardString)

    def printNeighboursBoard(self):
        boardString = ""
        for x in range(self.size):
            for y in range(self.size):
                pointState = self.countNeighbours(x, y)
                boardString += str(pointState) + ' '
            boardString += '\n'
        print(boardString)

    def totalAlive(self):
        count = 0
        for x in range(self.size):
            for y in range(self.size):
                count += self.getPoint(x,y)
        return count

    def checkChanged(self, gameboard):
        for x in range(self.size):
            for y in range(self.size):
                if self.gameBoard[x][y] != gameboard[x][y]:
                    return 1
        print("No change")
        return 0


x = input("How large do you want the board to be?: ")
gameOverlord = GameOverlord(x)
gameOverlord.randomise(0.4)
history = []
while True:
    newBoard = gameOverlord.updateStates()
    gameOverlord.gameBoard = newBoard
    repeatFlag = 0
    for i in history:
        if not gameOverlord.checkChanged(i):
            repeatFlag = 1
    history.append(newBoard)
    if len(history) > 10:
        history = history[1:11]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(0.01)
    gameOverlord.printBoard()
    #gameOverlord.printNeighboursBoard()
    sleep(0.5)
    
    if repeatFlag:
        print("Reached stable state")
        sleep(5)
        print("Restarting")
        gameOverlord.randomise(0.4)
