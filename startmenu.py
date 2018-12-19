import pygame
import random
import blyat
import time
import basetest
import leaderboard
import colours

pygame.init()

display_width = 800
display_height = 600
largeText = pygame.font.Font('freesansbold.ttf', 115)
smallText = pygame.font.Font("freesansbold.ttf", 20)

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

startmenu_image = pygame.image.load("start_menu.jpeg").convert()

#Colours

def quitgame():
    pygame.quit()
    quit()

def button(msg, x, y, w, h, color, active_color, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                basetest.game_loop()
            if action == "leaderboard":
                leaderboard.leaderboard(gameDisplay, 'highscores.txt')
            if action == "quit":
                quitgame()
    else:
        pygame.draw.rect(gameDisplay, color, (x, y , w, h))

    textSurf, textRect = text_objects(msg, smallText, colours.black)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(textSurf, textRect)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text):
    TextSurf, TextRect = text_objects(text, largeText, colours.black)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(3)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #Title:
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = text_objects("Fuck", largeText, colours.black)
        textRect.center = (display_width/2, 50)
        gameDisplay.blit(textSurf, textRect)

        #Start Menu Background Image
        gameDisplay.blit(startmenu_image, [0, 0])

        #Start Menu Buttons
        button("Start",300, 100, 200, 100, colours.lightgray, colours.gray, "play")
        button("Leaderboard", 300, 250, 200, 100, colours.lightgray, colours.gray, "leaderboard")
        button("Quit", 300, 400, 200, 100, colours.lightgray, colours.gray, "quit")

        pygame.display.update()
        clock.tick(15)