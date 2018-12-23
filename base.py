import pygame
import random
import blyat
import time
import math
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

def android(x, y):
    gameDisplay.blit(androidImg, (x, y))

def print_apples(apple_x, apple_y, apple_r, apple_w, color):
    pygame.draw.circle(gameDisplay, color, (apple_x, apple_y), apple_r, apple_w)

class Apple:
    def __init__(self,x,y,r,w,speed,color):
        self.x = x
        self.y =y
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

def text_objects(text, font): #change later to add colour as parameter
    textSurface = font.render(text, True, blue,)
    return textSurface, textSurface.get_rect()

def game_over(count):
    import highscores
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
    APPLE_SPEED = 20
    APPLE_RADIUS = 20
    APPLE_WIDTH = 0
    APPLE_COLOR = red

    #apples list holds all apples
    apples = []
    apples.append(Apple(APPLE_X,APPLE_Y,APPLE_RADIUS,APPLE_WIDTH,APPLE_SPEED,APPLE_COLOR));

    #floor blocks
    block_width = 1.5 * (2*APPLE_RADIUS)
    block_height = 20
    num_blocks = int (math.ceil(display_width/block_width))
    blocks = []

    for i in range(num_blocks):
        blocks.append(Block(block_width, block_height, i*block_width, androidY + android_height))


    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                break
            #print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over(count)
                    gameExit = True
                    break

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

        # update apple falling
        for i in range(len(apples)):
            cur_apple = apples[i]

            print_apples(cur_apple.x, cur_apple.y, cur_apple.r, cur_apple.w, cur_apple.color)
            cur_apple.y += cur_apple.speed

            #reset apple if falls out of screen
            if cur_apple.y > display_height:
                cur_apple.y = - cur_apple.y
                cur_apple.x = random.randrange(0, display_width)


            #check collision between apple and person
            if cur_apple.y + cur_apple.r > androidY:
                if cur_apple.x + cur_apple.r > androidX and cur_apple.x - cur_apple.r < androidX + android_width:
                    count = count + 1

                    cur_apple.y = - cur_apple.y
                    cur_apple.x = random.randrange(0, display_width)


            # When missed apple
            if cur_apple.y + cur_apple.r > androidY + android_height:
                hit_block = False
                # Make disappear block with x coordinate
                for i in range(len(blocks)):
                    cur_block = blocks[i]

                    if cur_apple.x <= cur_block.x + cur_block.width and cur_apple.x >= cur_block.x and cur_block.visible:
                        cur_block.disappear()
                        hit_block = True

                        # Reset apple y coordinate
                        cur_apple.y = - cur_apple.y
                        cur_apple.x = random.randrange(0, display_width)
                        break


                # if pass through (no block disappear)
                if hit_block == False:
                    game_over(count)
                    gameExit = True
                    break

            #update_cnt = "count = " + str(count)
            #message_display(update_cnt);

            pygame.display.update()
            clock.tick(60)

