import pygame
import random
import blyat
import time
import base
import leaderboard
import colours
import text

pygame.init()

def game_intro():

    #Startmenu Background
    background_image = pygame.image.load("startmenu_background.jpg").convert()
    background_x = 0
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                base.quitgame()
                break

        #Start Menu Background Image
        reset_x = background_x % background_image.get_rect().width

        base.gameDisplay.blit(background_image, (reset_x - background_image.get_rect().width, 0))

        if reset_x < base.display_width:
            base.gameDisplay.blit(background_image, (reset_x, 0))

        background_x -= 1

    #Start Menu Buttons
        text.button(base.gameDisplay, "Start",300, 100, 200, 100, colours.lightgray, colours.gray, base.game_loop)
        text.button(base.gameDisplay, "Leaderboard", 300, 250, 200, 100, colours.lightgray, colours.gray, "leaderboard")
        text.button(base.gameDisplay, "Quit", 300, 400, 200, 100, colours.lightgray, colours.gray, base.quitgame)

        pygame.display.update()
        base.clock.tick(45)
