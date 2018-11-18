import pygame
import random
import blyat
import time
import math
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


#test

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('fuckblyat')
clock = pygame.time.Clock()

androidImg = pygame.image.load('fighterjet2.png')




def android(x, y):
    gameDisplay.blit(androidImg, (x, y))

def apples(apple_x, apple_y, apple_r, apple_w, color):
    pygame.draw.circle(gameDisplay, color, (apple_x, apple_y), apple_r, apple_w)

def print_blocks(b_x, b_y, width, height):
    pygame.draw.rect(gameDisplay, block_color, [b_x, b_y, width, height], 2)


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(3)

    game_loop()

def text_objects(text, font): #change later to add colour as parameter
    textSurface = font.render(text, True, blue,)
    return textSurface, textSurface.get_rect()


def game_over():
    message_display("Game Over")

def game_loop():
    androidX = (display_width * 0.4)
    androidY = (display_height * 0.8)

    velocity = 0
    count = 0

    #apple stuff
    apple_x = random.randrange(0, display_width)
    apple_y = -600
    apple_speed = 20
    apple_radius = 20
    apple_width = 0


    #floor blocks
    block_width = 1.5 * (2*apple_radius)
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
            #print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.q:
                    gameExit = True

        '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -android_speed
                if event.key == pygame.K_RIGHT:
                    x_change = android_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        '''

        coord, velocity = blyat.process_frame()
        if len(coord):
            androidX += velocity * 3
        if androidX < 0:
            androidX = 0
        if androidX > display_width - android_width:
            androidX = display_width - android_width

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
        apples(apple_x, apple_y, apple_radius, apple_width, red)
        apple_y += apple_speed

        #reset apple if falls out of screen
        if apple_y > display_height:
            apple_y = - apple_y
            apple_x = random.randrange(0, display_width)


        #check collision between apple and person
        if apple_y + apple_radius > androidY:
            if apple_x + apple_radius > androidX and apple_x - apple_radius < androidX + android_width:
                count = count + 1

                apple_y = - apple_y
                apple_x = random.randrange(0, display_width)


        # When missed apple
        if apple_y + apple_radius > androidY + android_height:

            hit_block = False
            # disappear block with x coordinate
            for i in range(len(blocks)):
                cur_block = blocks[i]

                if apple_x <= cur_block.x + cur_block.width and apple_x >= cur_block.x and cur_block.visible:
                    cur_block.disappear()
                    hit_block = True

                    # Reset apple y coordinate
                    apple_y = - apple_y
                    apple_x = random.randrange(0, display_width)
                    break


            # if pass through (no block disappear)
            if hit_block == False:
                game_over()


        pygame.display.update()
        clock.tick(60)

game_loop()
blyat.destroy()
pygame.quit()
quit()
