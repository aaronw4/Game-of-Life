import sys, pygame
import pygame.draw
import random
import pygame.time

size = width, height = 500, 500
dead_color = 0, 0, 0
alive_color = 255, 255, 255

screen = pygame.display.set_mode(size)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.clear_screen()
        pygame.display.flip()

        self.last_update = 0

        self.grid_active = 0
        self.grids = []
        self.init_grids()
        self.set_grid()

    def init_grids(self):
        columns = 25
        rows = 25

        def create_grid():
            grid = []
            for col in range(25):
                row = [0] * 25
                grid.append(row)
            return grid

        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None):
        for columns in range(25):
            for rows in range(25):
                if value is None:
                    cells = random.choice([0, 0, 0, 0, 1])
                else:
                    cells = value
                self.grids[self.grid_active][columns][rows] = cells

    def draw(self):
        color = dead_color
        for columns in range(25):
            for rows in range(25):
                if self.grids[self.grid_active][columns][rows] == 1:
                    color = alive_color
                elif self.grids[self.grid_active][columns][rows] == 0:
                    color = dead_color
                pygame.draw.rect(self.screen, color, (columns * 20, rows * 20, 20, 20))
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(dead_color)
    
    def check_neighboors(self, col, row):
        # self.grids[self.grid_active][columns][rows]
        def get_value(col, row):
            try:
                value = self.grids[self.grid_active][col][row]
            except:
                value = 0
            return value

        alive_neighboors = get_value(col-1, row) + get_value(col+1, row) + get_value(col, row-1)\
        + get_value(col, row+1) + get_value(col-1, row-1) + get_value(col+1, row-1)\
        + get_value(col-1, row+1) + get_value(col+1, row+1)
        
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

    def update(self):
        for columns in range(25):
            for rows in range(25):
                next_grid = self.check_neighboors(columns, rows)
                self.grids[(self.grid_active + 1) % 2][columns][rows] = next_grid
        self.grid_active = (self.grid_active + 1) % 2

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.frame_rate()

    def frame_rate(self):
        now = pygame.time.get_ticks()
        time_passed = now - self.last_update
        time_remaining = int(500 - time_passed)
        if time_remaining > 0:
            pygame.time.delay(int(time_remaining))
        self.last_update = now

if __name__ == '__main__':
    game = Game()
    game.run()