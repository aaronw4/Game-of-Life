import sys, pygame, random, time
import pygame.draw

size = width, height = 500, 600
#Cell is 20x20 giving a 25x25 grid
dead_color = 0, 0, 0
#black
alive_color = 255, 255, 255
#white

class Game:
    def __init__(self):
        self.count = 0
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.screen = pygame.display.set_mode(size)
        #opens window 500x500
        self.clear_screen()
        #function that turns all cells black
        pygame.display.flip()
        #updates the display

        self.grid_active = 0
        self.grids = []
        self.init_grids()
        self.set_grid()
        #Calls functions that creates two grids and displays one upon initiating

    def init_grids(self):
        def create_grid():
            grid = []
            for col in range(25):
                row = [0] * 25
                grid.append(row)
            return grid
            #creates grid with 25 rows([]) each with 25 columns(0's)

        self.grids.append(create_grid())
        self.grids.append(create_grid())
        #creates grids using create_grid fxn and appends them to grids[]

    def set_grid(self, value=None, grid=0):
        for columns in range(25):
            for rows in range(25):
                if value is None:
                    cells = random.choice([0, 0, 0, 0, 1])
                    #0 = dead, 1 = alive
                    #randomly picks from array. 20% chance of cell being alive
                else:
                    cells = value
                self.grids[grid][columns][rows] = cells

    def draw(self):
        for columns in range(25):
            for rows in range(25):
                if self.grids[self.grid_active][columns][rows] == 1:
                    color = alive_color
                elif self.grids[self.grid_active][columns][rows] == 0:
                    color = dead_color
                pygame.draw.rect(self.screen, color, (columns * 20, rows * 20, 20, 20)) #(Col pos, Row pos, cell width, cell height)

        font = pygame.font.SysFont('arial', 24)
        text = font.render("Generation: {}".format(self.count), True, alive_color, dead_color)
        self.screen.blit(text, (360, 510))
        
        pygame.display.flip()
        #Turns grid of numbers into colors alive_cole is white, dead_color is black

    def clear_screen(self):
        self.screen.fill(dead_color)
    
    def check_neighboors(self, col, row):
        def get_value(col, row):
            try:
                value = self.grids[self.grid_active][col][row]
            except:
                value = 0
            return value
        #Counts live neighboors. Ignores None from cells on boarder

        alive_neighboors = get_value(col-1, row) + get_value(col+1, row) + get_value(col, row-1)\
        + get_value(col, row+1) + get_value(col-1, row-1) + get_value(col+1, row-1)\
        + get_value(col-1, row+1) + get_value(col+1, row+1)
        #counts the number of live neighboors
        
        if self.grids[self.grid_active][col][row] == 1:
            if alive_neighboors < 2:
                return 0
            elif alive_neighboors > 3:
                return 0
            else:
                return 1
        else:
            if alive_neighboors == 3:
                return 1
            else:
                return 0
        #rules of life

    def update(self):
        self.set_grid(0, (self.grid_active + 1) % 2)
        #clears old grid, this treats off screen cells as dead
        for columns in range(25):
            for rows in range(25):
                next_grid = self.check_neighboors(columns, rows)
                self.grids[(self.grid_active + 1) % 2][columns][rows] = next_grid
        self.grid_active = (self.grid_active + 1) % 2
        #updates grid according to rules in check_neighboors fxn

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.events()
            self.update()
            self.count += 1
            self.draw()
            time.sleep(0.5)
        #Updates grid, displays grid, then waits 0.5 seconds and repeats

if __name__ == '__main__':
    game = Game()
    game.run()