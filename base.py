import pygame
import random
import blyat
import time
import math
import highscores
import colours
import text
from block import Block

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
block_color = (50, 7, 20)

android_width = 100  # for fighterandroid2.png
android_height = 100 # for fighterandroid2.png
android_speed = 10

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('fuckblyat')
clock = pygame.time.Clock()

androidImg = pygame.image.load('fighterjet2.png')

def quitgame():
    pygame.quit()
    quit()

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        gameDisplay.fill(colours.white)
        pausedSurf, pausedRect = text.text_objects("Paused", text.smallText, colours.black)
        pausedRect.center = (400, 200)
        gameDisplay.blit(pausedSurf, pausedRect)

        contSurf, contRect = text.text_objects("To continue, press ESCAPE again", text.smallText, colours.black)
        contRect.center = (400, 300)
        gameDisplay.blit(contSurf, contRect)
        pygame.display.update()
        clock.tick(5)


def android(x, y):
    gameDisplay.blit(androidImg, (x, y))

def print_apples(apple_x, apple_y, apple_r, apple_w, color):
    pygame.draw.circle(gameDisplay, color, (apple_x, apple_y), apple_r, apple_w)

class Apple:
    def __init__(self,x,y,r,w,speed,color):
        self.x = x
        self.y = y
        self.r = r
        self.w = w
        self.speed = speed
        self.color = color

class Reset_Apple (Apple):
    def __init__(self,x,y,r,w,speed,color):
        self.x = x
        self.y = y
        self.r = r
        self.w = w
        self.speed = speed
        self.color = color

def print_blocks(b_x, b_y, width, height):
    pygame.draw.rect(gameDisplay, block_color, [b_x, b_y, width, height], 2)

def game_over(count):
    text.message_display("Game Over")
    highscores.register_highscore(gameDisplay, count)

def game_loop():
    androidX = (display_width * 0.4)
    androidY = (display_height * 0.8)

    velocity = 0
    count = 0

    #Constants for apples
    APPLE_X = random.randrange(0, display_width)
    APPLE_Y = -600
    APPLE_SPEED = 15
    APPLE_RADIUS = 20
    APPLE_WIDTH = 0
    APPLE_COLOR = red
    RESET_APPLE_COLOR = green

    #apples list holds all apples
    apples = []
    apples.append(Apple(APPLE_X,APPLE_Y,APPLE_RADIUS,APPLE_WIDTH,APPLE_SPEED,APPLE_COLOR))

    #floor blocks
    block_width = 1.5 * (2*APPLE_RADIUS)
    block_height = 20
    num_blocks = int(math.ceil(display_width/block_width))
    blocks = []

    # Measure Time Elapsed
    start_time = time.time()

    # Flag to only insert one special apple at a time
    Insert_Reset_Already = False
    TIME_Reset_Apple = 15

    Insert_Apple = False
    #Time to release a new apple
    TIME_Apple = 20 + random.randrange(0, 10)

    #interval to change speed by speedChange every changeSpeedInterval
    initialInterval = 5
    changeSpeedInterval = initialInterval
    speedChange = 5

    for i in range(num_blocks):
        blocks.append(Block(block_width, block_height, i*block_width, androidY + android_height))

    gameExit = False


    # while game is running
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                gameExit = True
            #print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over(count)
                    gameExit = True

                elif event.key == pygame.K_ESCAPE:
                    pause()

        #for detecting face:
        coord, velocity = blyat.process_frame()

        #Move android from detecting face movement
        if len(coord):
            androidX += velocity * -3
        if androidX < 0:
            androidX = 0
        if androidX > display_width - android_width:
            androidX = display_width - android_width

        #Display camera live streaming
        bg = pygame.image.load("blyatface.jpg")
        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))

        #Update android
        android(androidX, androidY)

        #Update/draw floor:
        for i in range(num_blocks):
            cur_block = blocks[i]
            if cur_block.visible == True:
                print_blocks(cur_block.x, cur_block.y, cur_block.width, cur_block.height)

        #If TIME_Reset_Apple seconds have passed, add a new reset apple
        cur_time = time.time() - start_time
        #print "time: " + str(cur_time)

        # print len(apples)
        if cur_time % TIME_Reset_Apple >= 0 and cur_time % TIME_Reset_Apple <= 0.1 and (not Insert_Reset_Already):
            temp_x = random.randrange(0, display_width)
            apples.append(Reset_Apple (temp_x, APPLE_Y, APPLE_RADIUS, APPLE_WIDTH, APPLE_SPEED, RESET_APPLE_COLOR))
            Insert_Reset_Already = True

        #TIME_Apple = 10
        #Insert a new regular apple (every TIME_Apple seconds have passed)
        if cur_time % TIME_Apple >= 0 and cur_time % TIME_Apple <= 0.1 and (not Insert_Apple):
            temp_x = random.randrange(0, display_width)
            temp_y = - random.randrange(0, display_width)
            apples.append(Apple(temp_x,temp_y,APPLE_RADIUS, APPLE_WIDTH, APPLE_SPEED, APPLE_COLOR))
            Insert_Apple = True
            TIME_Apple = 20 + random.randrange(0, 10)   # Make a new random apple



        # Query through and update apple(s) falling
        for i in range(len(apples)):
            cur_apple = apples[i]

            print_apples(cur_apple.x, cur_apple.y, cur_apple.r, cur_apple.w, cur_apple.color)



            # Increase speed of Apple every time you catch a multiple of 5.


            if count == changeSpeedInterval:
                changeSpeedInterval += initialInterval
                APPLE_SPEED = APPLE_SPEED + speedChange

            print APPLE_SPEED
            cur_apple.y += APPLE_SPEED

            ##reset apple if falls out of screen
            #if cur_apple.y > display_height:
            #    cur_apple.y = - cur_apple.y
            #    cur_apple.x = random.randrange(0, display_width)


            #check collision between apple and android
            if cur_apple.y + cur_apple.r > androidY:
                if cur_apple.x + cur_apple.r > androidX and cur_apple.x - cur_apple.r < androidX + android_width:

                    count += 1

                    if isinstance(cur_apple, Reset_Apple):
                        # Reset blocks
                        for j in range(len(blocks)):
                            blocks[j].reappear()
                        del apples[i]                   # remove the Reset_Apple
                        Insert_Reset_Already = False    # can now add another Reset_Apple
                        break

                    cur_apple.y = - cur_apple.y - random.randrange(0, display_width)
                    cur_apple.x = random.randrange(0, display_width)
                    Insert_Apple = False

            # When missed apple (apple passed android)
            if cur_apple.y + cur_apple.r > androidY + android_height:
                hit_block = False
                # Make disappear block with x coordinate
                for k in range(len(blocks)):
                    cur_block = blocks[k]

                    if cur_apple.x <= cur_block.x + cur_block.width and cur_apple.x >= cur_block.x and cur_block.visible:
                        cur_block.disappear()
                        hit_block = True

                        # Reset apple y coordinate
                        cur_apple.y = - cur_apple.y - random.randrange(0, display_width)
                        cur_apple.x = random.randrange(0, display_width)
                        break

                # if pass through (no block disappear)
                if hit_block == False:
                    game_over(count)
                    gameExit = True

                #Check if current apple is a Reset_Apple, if it is, delete it.
                if isinstance(cur_apple, Reset_Apple):
                    del apples[i]
                    Insert_Reset_Already = False

                Insert_Apple = False


        pygame.display.update()
        clock.tick(30)

        #update_cnt = "count = " + str(count)
        #text.message_display(update_cnt)