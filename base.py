import pygame
import random
import blyat
import time

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

jet_width = 100 #for fighterjet2.png
jet_height = 100 #for fighterjet2.png
jet_speed = 10


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('fuckblyat')
clock = pygame.time.Clock()

jetImg = pygame.image.load('fighterjet2.png')

def jet(x, y):
    gameDisplay.blit(jetImg, (x, y))

def apples(apple_x, apple_y, apple_r, apple_w, color):
    pygame.draw.circle(gameDisplay, color, (apple_x, apple_y), apple_r, apple_w)


def count_update(cnt):
    msg = '%s%d' %("Count = ", cnt)
    message_display(msg)


def message_display(text):
    myfont = pygame.font.SysFont('Comic Sans', 30)
    textsurface = textsurface = myfont.render(text, False, (0, 0, 0))
    gameDisplay.blit(textsurface, (0, 0))


def game_loop():
    x = (display_width * 0.4)
    y = (display_height * 0.8)

    x_change = 0
    count = 0

    #apple stuff
    apple_x = random.randrange(0, display_width)
    apple_y = -600
    apple_speed = 20
    apple_radius = 20
    apple_width = 0


    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            #print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True

        '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -jet_speed


                if event.key == pygame.K_RIGHT:
                    x_change = jet_speed



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        '''
        coord = blyat.process_frame()
        if len(coord):
            x = display_width - (coord[0][0] + coord[0][2] / 2)
        if x < 0:
            x = 0

        if x > display_width - jet_width:
            x = display_width - jet_width
        bg = pygame.image.load("blyatface.jpg")
        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))




        #Update jet
        jet(x, y)

        # update apple falling
        apples(apple_x, apple_y, apple_radius, apple_width, red)
        apple_y += apple_speed

        #reset apple if falls out of screen
        if apple_y > display_height:
            apple_y = - apple_y
            apple_x = random.randrange(0, display_width)



        if apple_y + apple_radius > y:
            if apple_x + apple_radius > x and apple_x - apple_radius < x + jet_width:
                count = count + 1

                apple_y = - apple_y
                apple_x = random.randrange(0, display_width)

        if apple_y + apple_radius > y + jet_height:
            #loseR!!!!
            gameExit = True


        count_update(count)

        pygame.display.update()
        clock.tick(60)


game_loop()
blyat.destroy()
pygame.quit()
quit()
