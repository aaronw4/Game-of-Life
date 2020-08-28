import pygame

def run():
    pygame.init()
    white = 255, 255, 255
    black = 0, 0, 0
    dark_gray = 50, 50, 50
    gray = 127, 127, 127

    display_surface = pygame.display.set_mode((700, 300))
    pygame.display.set_caption("Game of Life Rules")

    font = pygame.font.SysFont('arial', 20)
    message1 = "1. Any live cell with fewer than two live neighbours dies, as if by underpopulation."
    message2 = "2. Any live cell with two or three live neighbours lives on to the next generation."
    message3 = "3. Any live cell with more than three live neighbours dies, as if by overpopulation."
    message4 = "4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."

    text1 = font.render(message1, True, white, black)
    text2 = font.render(message2, True, white, black)
    text3 = font.render(message3, True, white, black)
    text4 = font.render(message4, True, white, black)

    def button(message, x, y, button_width, button_height, inactive_color, active_color, action=None):
        #function to create all buttons. X and Y are coordinates on grid
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x + button_width) > mouse[0] > x and (y + button_height) > mouse[1] > y:
            pygame.draw.rect(display_surface, active_color, (x, y, button_width, button_height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(display_surface, inactive_color, (x, y, button_width, button_height))
        #if mouse is inside button and mouse button is clicked, run action fxn

        font = pygame.font.SysFont('arial', 20)
        text = font.render(message, True, white)
        rect = text.get_rect()
        rect.center = (int(x + (button_width/2)), int(y + (button_height/2)))
        display_surface.blit(text, rect)
        #Inserts and centers text in button

    def home():
        pass

    button('Return', 340, 250, 70, 30, gray, dark_gray)

    while True:
        display_surface.fill(black)
        display_surface.blit(text1, (20, 50))
        display_surface.blit(text2, (20, 100))
        display_surface.blit(text3, (20, 150))
        display_surface.blit(text4, (20, 200))
        button('Return', 300, 250, 70, 30, gray, dark_gray)

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                pygame.quit() 
                quit() 
            pygame.display.update()  