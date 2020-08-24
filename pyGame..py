import sys, pygame
import pygame.draw
import random

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
        self.init_grids()

    def init_grids(self):
        columns = 25
        rows = 25
        print('Columns: %d\nRows: %d' % (columns, rows))

        self.grids = []
        grid = []
        for col in range(25):
            row = [0] * 25
            grid.append(row)
        self.grids.append(grid)

        self.grid_active = 0
        self.set_grid()
        print(self.grids[0])

    def set_grid(self, value=None):
        for columns in range(25):
            for rows in range(25):
                if value is None:
                    cells = random.choice([0, 0, 0, 0, 1])
                else:
                    cells = value
                self.grids[self.grid_active][columns][rows] = cells

    def draw(self):
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

    def update(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()

    


if __name__ == '__main__':
    game = Game()
    game.run()