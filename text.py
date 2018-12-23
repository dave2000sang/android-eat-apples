import pygame
import base
import leaderboard
import colours
import time

pygame.init()

#Display
display_width = 800
display_height = 600

#Text Fonts
smallText = pygame.font.Font("freesansbold.ttf", 20)

gameDisplay = pygame.display.set_mode((display_width, display_height))

def center_box(box_width, box_height, display_width, display_height):
    box_x = (display_width - box_width) / 2
    box_y = (display_height - box_height) / 2

    return box_x, box_y

def button(msg, x, y, w, h, color, active_color, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    border = 3 #Change Border Thickness

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h), 0)
        if click[0] == 1 and action != None:

            if action == "leaderboard":
                leaderboard.display_leaderboard(gameDisplay, 'highscores.txt')
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, color, (x, y , w, h), 0)

    pygame.draw.rect(gameDisplay, colours.black, (x, y, w, h), border)
    textSurf, textRect = text_objects(msg, smallText, colours.black)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(textSurf, textRect)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text):
    TextSurf, TextRect = text_objects(text, smallText, colours.black)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(3)
