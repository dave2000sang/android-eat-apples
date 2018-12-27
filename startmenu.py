import pygame
import random
import blyat
import time
import base
import leaderboard
import colours
import text

pygame.init()

startmenu_image = pygame.image.load("startmenu_background.jpg").convert()


def game_intro():

    intro = True
    background_x = 0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                base.quitgame()
                break
        #Title:
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = text.text_objects("Fuck", largeText, colours.black)
        textRect.center = (text.display_width/2, 50)
        base.gameDisplay.blit(textSurf, textRect)

        #Start Menu Background Image
        base.gameDisplay.blit(startmenu_image, (background_x, 0))
        background_x -= 2

        #Start Menu Buttons
        text.button(base.gameDisplay, "Start",300, 100, 200, 100, colours.lightgray, colours.gray, base.game_loop)
        text.button(base.gameDisplay, "Leaderboard", 300, 250, 200, 100, colours.lightgray, colours.gray, "leaderboard")
        text.button(base.gameDisplay, "Quit", 300, 400, 200, 100, colours.lightgray, colours.gray, base.quitgame)

        pygame.display.update()
        base.clock.tick(15)
