import sys
import pygame
import random
import time
import pygame.draw
import hyperlink
import pyGameRules

url = hyperlink.parse(u"https://en.wikipedia.org/wiki/Conway's_Game_of_Life#Rules")
size = width, height = 500, 600
#Cell is 20x20 giving a 25x25 grid
dead_color = 0, 0, 0 #black
alive_color = 255, 255, 255 #white
dark_gray = 50, 50, 50
gray = 127, 127, 127
blue = 0, 0, 255
navy_blue = 0, 0, 100

class Game:
    def __init__(self):
        self.count = 0
        self.pause = False
        self.start = False
        self.speed = 0.5
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

    def clear_grid(self):
        self.clear_screen()
        for columns in range(25):
            for rows in range(25):
                self.grids[self.grid_active][columns][rows] = 0
                self.grids[(self.grid_active + 1) % 2][columns][rows] = 0
        self.count = 0
        #sets everything back to zero

    def random_grid(self, value=None):
        for columns in range(25):
            for rows in range(25):
                if value is None:
                    cells = random.choice([0, 0, 0, 0, 1])
                    #0 = dead, 1 = alive
                    #randomly picks from array. 20% chance of cell being alive
                self.grids[self.grid_active][columns][rows] = cells
        self.start = True

    def x_grid(self):
        for num in range(25):
            self.grids[self.grid_active][num][num] = 1
            self.grids[self.grid_active][num][24 - num] = 1
        self.start = True

    def plus_grid(self):
        for num in range(25):
            self.grids[self.grid_active][num][12] = 1
            self.grids[self.grid_active][12][num] = 1
        self.start = True

    def rules(self):
        pyGameRules.run()

    def button(self, message, x, y, button_width, button_height, inactive_color, active_color, action=None):
        #function to create all buttons. X and Y are coordinates on grid
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
        #Inserts and centers text in button

    def start_game(self):
        self.start = True

    def speed_up(self):
        if self.speed == 0:
            pass
        else:
            self.speed -= 0.1
    
    def speed_down(self):
        if self.speed == 1:
            pass
        else:
            self.speed += 0.1

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

        new_font = pygame.font.SysFont('arial', 20)
        output = new_font.render('Speed', True, alive_color, dead_color)
        self.screen.blit(output, (360, 550))
        self.button(u"\u25B2", 420, 550, 20, 20, gray, dark_gray, self.speed_up)
        self.button(u"\u25BC", 450, 550, 20, 20, gray, dark_gray, self.speed_down)


        self.button('Start', 10, 510, 70, 30, gray, dark_gray, self.start_game)
        self.button('Pause', 10, 560, 70, 30, gray, dark_gray)
        self.button('Clear', 90, 510, 70, 30, gray, dark_gray)
        self.button('Rules', 90, 560, 70, 30, gray, dark_gray, self.rules)

        self.button('Big X', 170, 510, 70, 30, blue, navy_blue, self.x_grid)
        self.button('Big +', 170, 560, 70, 30, blue, navy_blue, self.plus_grid)
        self.button('Random', 250, 510, 70, 30, blue, navy_blue, self.random_grid)

        pygame.display.flip()
        #Turns grid of numbers into colors alive_cole is white, dead_color is black

    def paused_screen(self):
        #created a new screen to show when paused
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

        new_font = pygame.font.SysFont('arial', 20)
        output = new_font.render('Speed', True, alive_color, dead_color)
        self.screen.blit(output, (360, 550))
        self.button(u"\u25B2", 420, 550, 20, 20, gray, dark_gray)
        self.button(u"\u25BC", 450, 550, 20, 20, gray, dark_gray)


        self.button('Start', 10, 510, 70, 30, gray, dark_gray)
        self.button('Continue', 10, 560, 70, 30, gray, dark_gray)
        self.button('Clear', 90, 510, 70, 30, gray, dark_gray)
        self.button('Rules', 90, 560, 70, 30, gray, dark_gray, self.rules)

        self.button('Big X', 170, 510, 70, 30, blue, navy_blue)
        self.button('Big +', 170, 560, 70, 30, blue, navy_blue)
        self.button('Random', 250, 510, 70, 30, blue, navy_blue)
        
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
        #Above code treats cells outside of boarder as dead and does not count them

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
            #location of pause button
                if click[0] == 1:
                    if self.pause is False:
                        self.pause = True
                        self.paused_screen()
                    else:
                        self.pause = False
                        self.draw()
            if 160 > mouse[0] > 90 and 540 > mouse[1] > 510:
            #location of clear button
                if click[0] == 1:
                    self.start = False
                    self.clear_grid()
                    self.run()
            if self.start is False:
                if click[0] == 1:
                    mousepos_x, mousepos_y = event.pos
                    col, row = (int((mousepos_x) // 20), int((mousepos_y) // 20))
                    print(col, row)
                    if col < 25 and row < 25:
                        if self.grids[self.grid_active][col][row] == 1:
                            self.grids[self.grid_active][col][row] = 0
                        else:
                            self.grids[self.grid_active][col][row] = 1
                #if game is not running, cells can be turned off and on by clicking space with mouse
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while self.start is False:
            self.events()
            self.draw()
        while self.start is True:
            self.events()
            if self.pause:
                continue
            self.draw()
            time.sleep(self.speed)
            self.update()
            self.count += 1
        #A loop that pauses after each self.draw according to self.speed

if __name__ == '__main__':
    game = Game()
    game.run()