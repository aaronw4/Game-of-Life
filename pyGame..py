import sys, pygame, random, time
import pygame.draw

size = width, height = 500, 600
#Cell is 20x20 giving a 25x25 grid
dead_color = 0, 0, 0 #black
alive_color = 255, 255, 255 #white
dark_gray = 50, 50, 50
gray = 127, 127, 127

class Game:
    def __init__(self):
        self.count = 0
        self.pause = False
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

    def clear_screen(self):
        self.screen.fill(dead_color)

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

    def button(self, message, x, y, button_width, button_height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x + button_width) > mouse[0] > x and (y + button_height) > mouse[1] > y:
            pygame.draw.rect(self.screen, active_color, (x, y, button_width, button_height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, button_width, button_height))
        #if mouse is inside button and mouse button is clicked, run action fxn

        font = pygame.font.SysFont('arial', 20)
        text = font.render(message, True, alive_color)
        rect = text.get_rect()
        rect.center = (int(x + (button_width/2)), int(y + (button_height/2)))
        self.screen.blit(text, rect)

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

        self.button('Start', 10, 510, 70, 30, gray, dark_gray)
        self.button('Pause', 10, 560, 70, 30, gray, dark_gray)
        self.button('Random', 90, 510, 70, 30, gray, dark_gray)

        pygame.display.flip()
        #Turns grid of numbers into colors alive_cole is white, dead_color is black

    def paused_screen(self):
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

        self.button('Start', 10, 510, 70, 30, gray, dark_gray)
        self.button('Continue', 10, 560, 70, 30, gray, dark_gray)
        self.button('Random', 90, 510, 70, 30, gray, dark_gray)
        
        pygame.display.flip()
    
    def check_neighboors(self, col, row):
        neighboor_list = []
        #create a list to hold valid neighbooring cells

        for column in range(-1, 2):
            for rows in range(-1, 2):
                neighboor_row = row + rows
                neighboor_column = col + column
                #Iterates through all neighbooring cells

                valid_neighboor = True

                if (neighboor_row) == row and (neighboor_column) == col:
                    valid_neighboor = False
                #Does not count itself as a neighboor

                if (neighboor_row) < 0 or (neighboor_row) > 24:
                    valid_neighboor = False

                if (neighboor_column) < 0 or (neighboor_column) > 24:
                    valid_neighboor = False
                #Neighboor must fall in rows and columns 0 to 24 to be valid

                if valid_neighboor:
                    neighboor_list.append(self.grids[self.grid_active][neighboor_column][neighboor_row])
                #Adds neighboor cells that are valid to list

        alive_neighboors = sum(neighboor_list)
        #adds up the value of all neighbooring cells
        
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
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if 80 > mouse[0] > 10 and 590 > mouse[1] > 560:
                if click[0] == 1:
                    if self.pause is False:
                        self.pause = True
                        self.paused_screen()
                    else:
                        self.pause = False
                        self.draw()
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.events()
            if self.pause:
                continue
            self.update()
            self.count += True
            self.draw()
            time.sleep(0.5)
        #Updates grid, adds to count, displays grid, then waits 0.5 seconds and repeats

if __name__ == '__main__':
    game = Game()
    game.run()