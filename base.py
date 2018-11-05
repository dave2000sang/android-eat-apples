import pygame
import time
import random
pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

jet_width = 208

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('fuckblyat')
clock = pygame.time.Clock()

jetImg = pygame.image.load('fighterjet.png')

def jet(x, y):
    gameDisplay.blit(jetImg, (x, y))

def apples(apple_x, apple_y, apple_r, apple_w, color):
    pygame.draw.circle(gameDisplay, color, (apple_x, apple_y), apple_r, apple_w)
def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center =  ((display_width /2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display('blyat')

def game_loop():
    x = (display_width * 0.4)
    y = (display_height * 0.5)

    x_change = 0

    apple_startx = random.randrange(0, display_width)
    apple_starty = -600
    apple_speed = 7
    apple_radius = 20
    apple_width = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)
        apples(apple_startx, apple_starty, apple_radius, apple_width, red)
        apple_starty += apple_speed

        jet(x, y)

        if x > display_width - jet_width or x < 0:
            crash()

        if apple_starty > display_height:
            apple_starty = 0 - apple_starty
            apple_startx = random.randrange(0, display_width)

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
