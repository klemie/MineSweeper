import pygame
from colors import colours
import random


class Grid:

    def __init__(self, gameMode):
        # Gamemodes
        if gameMode == "Easy" or gameMode == "e":
            self.numBombs = 10
            self.numCols = 10
            self.numRows = 10
            self.cell_size = 50
            self.fonts = 30
            self.font_position = 10
        if gameMode == "test" or gameMode == "t":
            self.numBombs = 100
            self.numCols = 10
            self.numRows = 10
            self.cell_size = 50
            self.fonts = 30
            self.font_position = 10

        if gameMode == "Normal" or gameMode == "n":
            self.numBombs = 28
            self.numCols = 18
            self.numRows = 18
            self.cell_size = 40
            self.fonts = 30
            self.font_position = 5
        if gameMode == "Hard" or gameMode == "h":
            self.numBombs = 69
            self.numCols = 24
            self.numRows = 24
            self.cell_size = 30
            self.fonts = 25
            self.font_position = 2

        # 0 = not opened, 1 = opened, 2 = falgged
        # initialize states, numbers, and bombs
        self.states = self.create_Grid()
        self.cellvals = self.create_Grid()
        self.cellvals = self.plant_bombs(self.cellvals)
        if gameMode == "test" or gameMode == "t":
            self.cellvals[1][1] = 0

        self.cellvals = self.plant_numbers(self.cellvals)
        self.lose = False
        self.flags = self.numBombs

    def draw_grid(self, screen):
        for row in range(self.numRows):
            for col in range(self.numCols):
                cellval = self.cellvals[row][col]
                state = self.states[row][col]

                colorbois = {
                    -1: 'black',
                    0: 'white',
                    1: 'corn_flower_blue',
                    2: 'green',
                    3: 'red',
                    4: 'purple',
                    5: 'maroon',
                    6: 'turquoise',
                    7: 'dark_blue',
                    8: 'dark_gray',
                    9: 'dark_red'
                }
                colourboisbox = {
                    -1: 'black',
                    0: 'white',
                    1: 'white',
                    2: 'white',
                    3: 'white',
                    4: 'white',
                    5: 'maroon',
                    6: 'white',
                    7: 'white',
                    8: 'white',
                    9: 'dark_red'
                }

                # 0 = not opened, 1 = opened, 2 = falgged
                if state == 0:
                    if row % 2 + col % 2 == 1:
                        colour_rect = 'græy'
                        color_num = "dark_gray"
                    else:
                        colour_rect = 'dark_gray'
                        color_num = "dark_gray"
                elif state == 1:
                    colour_rect = colourboisbox[cellval]
                    color_num = colorbois[cellval]
                elif state == 2:
                    colour_rect = 'cyan'
                    color_num = 'cyan'
                colour_rect = colours[colour_rect]
                color_num = colours[color_num]

                pygame.draw.rect(screen, colour_rect,
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 0)
#
                if cellval != 0 and cellval != -1 and state == 1 and cellval != 9:
                    cellvalstr = str(self.cellvals[row][col])
                    font = pygame.font.SysFont('Papyrus', self.fonts)
                    text = font.render(cellvalstr, False, color_num)
                    screen.blit(
                        text, (self.cell_size * col + self.font_position, self.cell_size * row + self.font_position))

    def create_Grid(self):
        temp_grid = []
        for n in range(self.numRows):
            temp_row = []
            for i in range(self.numCols):
                temp_row.append(0)
            temp_grid.append(temp_row)
        return temp_grid

    def plant_bombs(self, grid):
        rem = self.numBombs
        total = self.numRows * self.numCols
        for n in range(self.numRows):
            for m in range(self.numCols):
                p = rem / total

                if random.random() < p:
                    grid[n][m] = -1
                    rem -= 1
                total -= 1

        return grid

    def plant_numbers(self, grid):

        for n in range(self.numRows):
            for i in range(self.numCols):
                self.check_aroundBombs(n, i)
        return grid

    def getClickedCell(self):
        x, y = pygame.mouse.get_pos()
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)
        #print(x, y)
        #print(row, col)

        # print(self.cellvals)

        return (row, col)

    def click(self):
        # Left click event handler
        clicked_cell = self.getClickedCell()
        row = clicked_cell[0]
        col = clicked_cell[1]
        self.states[row][col] = 1
        if self.cellvals[row][col] == -1:
            self.lose = True
            if self.lose == True:
                for n in range(self.numRows):
                    for i in range(self.numCols):
                        if self.states[n][i] == 2 and self.cellvals[n][i] != -1:
                            self.states[n][i] = 1
                            self.cellvals[n][i] = 9
                        if self.cellvals[n][i] == -1:
                            self.states[n][i] = 1

        elif self.cellvals[row][col] == 0:
            self.floodfill(row, col)

    def click_right(self):
        # Right click event handler
        clicked_cell = self.getClickedCell()
        print(clicked_cell)
        row = clicked_cell[0]
        col = clicked_cell[1]

        if self.states[row][col] == 0:
            self.states[row][col] = 2
            self.flags -= 1
        elif self.states[row][col] == 2:
            self.states[row][col] = 0
            self.flags += 1

    def check_aroundBombs(self, row, col):

        # Make sure cell is not a bomb
        if (self.cellvals[row][col] != -1):
            bombcount = 0

            for testRow in range((row-1), (row + 2)):
                for testCol in range((col-1), (col+2)):
                    # Check if test cell is legit
                    if testRow >= 0 and testRow < self.numRows and testCol >= 0 and testCol < self.numCols:
                        # Check test cell for a bomb
                        if self.cellvals[testRow][testCol] == -1:
                            bombcount += 1

            self.cellvals[row][col] = bombcount

    def floodfill(self, row, col):
        for r in range((row-1), (row + 2)):
            for c in range((col - 1), (col+2)):
                if r >= 0 and r < self.numRows and c >= 0 and c < self.numCols and self.states[r][c] == 0:
                    if self.cellvals[r][c] > 0:
                        self.states[r][c] = 1
                    elif self.cellvals[r][c] == 0:
                        self.states[r][c] = 1
                        self.floodfill(r, c)

    def win(self, screen):
        for r in range(self.numRows):
            for c in range(self.numCols):
                cell = self.cellvals[c][r]
                state = self.states[c][r]
                if cell == -1 and state == 2 and self.flags <= 0:
                    print("You Win")
                    font = pygame.font.SysFont('Papyrus', 30)
                    text = font.render("You win™", False, colours["black"])
                    screen.blit(text, (((self.cell_size * self.numCols) /
                                        2), ((self.cell_size*self.numRows)/2)))
                    return True
        return False
