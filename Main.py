import itertools
import random
# Minesweeper

def promptInt(name, lo, hi):
    while True:
        s = input(f'Enter {name} [{lo}..{hi}]: ')
        try:
            v = int(s)
        except ValueError:
            print('ERROR: Try again, number only')
            continue
        if not (lo <= v <= hi):
            print('ERROR: Allowed range %d..%d' % (lo, hi))
            continue
        return v

class Minesweeper:
    CLEAR = 0
    MINE = 9
    def __init__(self, width = 9, height = 10, mineCount = 12):
        self.revealedLocations = []
        default_size = input('Load save game? [Y/n]: ')
        if default_size.lower() == 'n':
            self.width = promptInt('width', 0, 99)
            self.height = promptInt('height', 0, 99)
            self.mineCount = promptInt('number of mines',
                                           0, self.width * self.height - 1)
        else:
            with open("savegame.txt", "r") as f:
                newWidth = int(f.readline(2))
                space = f.readline(1)
                newHeight = int(f.readline(2)) 
                space = f.readline(1)
                newMineCount = int(f.readline(2))   
                self.width = newWidth
                self.height = newHeight
                self.mineCount = newMineCount
                self.minefield = f.readline()
                
        self.minefield = [[Minesweeper.CLEAR] * self.width
                      for _ in range(self.height)]

    def readLocation(self):
        while True:
            done = input('Type Quit if you would like to save and Quit: ')
            if done == 'Quit':
                print('Thanks for Playing!')
                with open("savegame.txt", "w") as f:
                    if self.width < 10: 
                        f.write('0')
                    f.write(str(self.width))
                    f.write(' ')
                    if self.height < 10:
                        f.write('0')
                    f.write(str(self.height))
                    f.write(' ')
                    if self.mineCount < 10:
                       f.write('0') 
                    f.write(str(self.mineCount))
                    f.write(' ')
                    f.write(str(self.minefield))
                    exit()
            s = input('Enter {[column][row]} in 4 digits ex: 0105: ')
            if len(s) != 4:
                print('ERROR: Only 4 digits allowed')
                continue
            try:
                row = int(s[2:]) - 1
                column = int(s[:2]) - 1
            except ValueError:
                print('ERROR: Invalid Input, try again')
                continue
            if not (0 <= row < self.height):
                print('ERROR: Row out of range')
            elif not (0 <= column < self.width):
                print('ERROR: Column of range')
            elif (row, column) in self.revealedLocations:
                print('ERROR: Already revealed')
            else:
                break
        self.revealedLocations.append((row, column))

    def placeMines(self):
        locs = set(itertools.product(range(self.height), range(self.width)))
        locs -= {self.revealedLocations[-1]}
        locs = random.sample(locs, self.mineCount)
        for row, column in locs:
            self.minefield[row][column] = Minesweeper.MINE

    def placeMinesCounts(self):
        width, height, minefield = self.width, self.height, self.minefield
        for i in range(height):
            for j in range(width):
                if minefield[i][j] == Minesweeper.MINE:
                    continue
                minefield[i][j] = Minesweeper.CLEAR
                for i2 in range(max(0, i - 1), min(i + 2, height)):
                    for j2 in range(max(0, j -1), min(j + 2, width)):
                        if minefield[i2][j2] == Minesweeper.MINE:
                            minefield[i][j] += 1

    def revealSafeLocations(self, row, column):
        width, height, minefield = self.width, self.height, self.minefield
        if minefield[row][column] == Minesweeper.CLEAR:
            for i in range(max(0, row - 1), min(row + 2, height)):
                for j in range(max(0, column - 1), min(column + 2, width)):
                    if (i, j) not in self.revealedLocations:
                        self.revealedLocations.append((i, j))
                        if minefield[i][j] == Minesweeper.CLEAR:
                            self.revealSafeLocations(i, j)

    def runFirstTurn(self):
        self.readLocation()
        self.placeMines()
        self.placeMinesCounts()
        row, column = self.revealedLocations[-1]
        self.revealSafeLocations(row, column)
  
     
    def printMinefield(self):
        print('\n'*10)
        for row in range(self.height + 1):
            cell = '|'
            for column in range(self.width + 1):
                if row == 0 and column == 0:
                    cell += ' .|'
                elif row == 0:
                    cell += f'{column:2}|'
                elif column == 0:
                    cell += f'{row:2}|'
                elif (row - 1, column - 1) in self.revealedLocations:
                    cell += f'{self.minefield[row-1][column-1]:2}|'
                else:
                    cell += '{:>3}'.format('|')
            print(cell)

    def revealAllMines(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.minefield[i][j] == Minesweeper.MINE:
                    self.minefield[i][j] = 'XX'
                    if (i, j) not in self.revealedLocations:
                        self.minefield[i][j] = '**'
                        self.revealedLocations.append((i, j))

    def isGameOver(self):
        row, column = self.revealedLocations[-1]
        if self.minefield[row][column] == Minesweeper.MINE:
            self.revealAllMines()
            self.printMinefield()
            print('YOU LOSE!')
            return True
        unmined_locations_count = self.width * self.height - self.mineCount
        if len(self.revealedLocations) == unmined_locations_count:
            self.revealAllMines()
            self.printMinefield()
            print('YOU WIN!')
            return True
        return False

    def restartGame(self):
        restart = input('Restart? [y/N]: ')
        return restart.lower() == 'y'

def main():
    while True:
        ms = Minesweeper()
        ms.printMinefield()
        ms.runFirstTurn()
        while not ms.isGameOver():
            ms.printMinefield()
            ms.readLocation()
            row, column = ms.revealedLocations[-1]
            ms.revealSafeLocations(row, column)
        if not ms.restartGame():
            break

if __name__ == '__main__':
    main()