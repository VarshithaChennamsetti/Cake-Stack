# -*- coding: utf-8 -*-
"""
Created on Sun May 17 13:11:37 2020

@author: Varshitha
"""
#importing libraries
import pygame
import time
import random
from pygame import mixer

#Initialising Pygame
pygame.mixer.pre_init(44100, 16, 2, 4096) 
pygame.init()
clock=pygame.time.Clock()

#Global variables
pause=False

#Colours
black=(0,0,0)
white=(255,255,255)
pink=(255,200,200)
purple=(224, 187, 228)
bright_pink=(255,182,193)
bright_purple=(149, 125, 173)
dark_red=(249,113,113)

#Sizes
display_width=800#main screen width
display_height=600#main screen height
cake_width=87#cake width
cake_height=50#cake height

#Characters
cake1=pygame.image.load(r'images\cake1.png')
cake2=pygame.image.load(r'images\cake2.png')
back=pygame.image.load(r'images\background.png')
cake_icon=pygame.image.load(r'images\cakeImg.png')

#Sounds
sc=mixer.Sound(r"audio\scored.wav")
back_music=mixer.Sound(r"audio\back_music.wav")

#Main window
gameDisplay=pygame.display.set_mode([display_width,display_height])
pygame.display.set_caption('Vinny\'s 1st Game: Cake Stack!')#Name of the window
pygame.display.set_icon(cake_icon)#Game Icon

#Messages
def small_text(msg,size,x,y):
    text_font=pygame.font.SysFont('comicsansms',size)
    TextSurf=text_font.render(msg,True,black)
    gameDisplay.blit(TextSurf,(x,y))
    
#Cake tier
class cakeTier:
    y=-600
    x=350 
    cake=cake1
    def __init__(self,x=350,y=-600,cake=cake1):#default values
        self.x=x
        self.y=y
        self.cake=cake
    def make_cake(self):#draw the cake
        gameDisplay.blit(self.cake,(self.x,self.y))

#Quit the game
def quitgame():
    pygame.quit()
    quit()


#To make the font
def text_objects(text,font,colour):
    textSurf=font.render(text,True,colour)
    return textSurf,textSurf.get_rect()

#Buttons
def button(msg,x,y,w,h,i_c,c,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay,c,(x,y,w,h))
        if click[0]==1 and action!=None:
            action()
    else:
        pygame.draw.rect(gameDisplay,i_c,(x,y,w,h))
    smallText=pygame.font.SysFont("comicsansms",20)
    TextSurf,TextRect=text_objects(msg,smallText,black)
    TextRect.center=(x+w/2,y+h/2)
    gameDisplay.blit(TextSurf,TextRect)

#Stroy Narration   
def narration():
    small_text("You are the Royal cook. You",30,390,165)
    small_text("have been ordered to make",30,390,195)
    small_text("the world's tallest cake for",30,390,225)
    small_text("the birthday of Princess Eve.",30,390,255)
    small_text("If you fail to stack a tier,",30,390,295)
    small_text("you have to start over again!",30,390,325)
    small_text("Press < or > to move cake!",30,390,440)
    small_text("Press space to pause game!",30,390,470)
    small_text("Game Developer: Vinny :D",15,500,550)
    
#Game Over
def gameOver(score):
    mixer.Sound.stop(back_music)
    over=True
    while(over):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        largeText=pygame.font.SysFont("comicsansms",75)
        TextSurf,TextRect=text_objects("Game Over!",largeText,black)
        TextRect.center=(display_width/2+180,display_height/2-180)
        small_text("Your Score: "+str(score),30,520,225)
        gameDisplay.blit(TextSurf,TextRect)
        button("Play again?",420,390,150,50,purple,bright_purple,gameLoop)
        button("Quit",620,390,100,50,pink,bright_pink,quitgame)
        pygame.display.update()
        clock.tick(15)
#unpause
def unpause():
    global pause
    pause=False
    mixer.Sound.play(back_music,-1)#Background music

#Paused
def paused():
    mixer.Sound.stop(back_music)
    global pause
    while(pause):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        largeText=pygame.font.SysFont("comicsansms",75)
        TextSurf,TextRect=text_objects("Paused",largeText,black)
        TextRect.center=(display_width/2+180,display_height/2+10)
        gameDisplay.blit(TextSurf,TextRect)
        button("Resume",420,390,150,50,purple,bright_purple,unpause)
        button("Quit",620,390,100,50,pink,bright_pink,quitgame)
        pygame.display.update()
        clock.tick(15)
    
#Menu
def game_intro():
    intro=True
    while(intro):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(back,(0,0))
        largeText=pygame.font.SysFont("comicsansms",75)
        TextSurf,TextRect=text_objects("Cake Stack!",largeText,dark_red)
        TextRect.center=(display_width/2+180,display_height/2-180)
        narration()
        gameDisplay.blit(TextSurf,TextRect)
        small_text("Background designed by brgfx / Freepik",7,1,580)
        button("Play",420,390,100,50,purple,bright_purple,gameLoop)
        button("Quit",620,390,100,50,pink,bright_pink,quitgame)
        pygame.display.update()
        clock.tick(15)

#Game loop
def gameLoop():
    mixer.Sound.play(back_music,-1)#Background music
    global pause
    stopped_cake=False#we have to check if the cake tier already stopped
    speed=7
    playGame=False#the game loop
    no_cakes=0#how many cakes printed so far
    cake_l=[]#to see if a cake has been already used
    cake_obj_list=[]#Object list for cake
    stacked_cakes=[]#no. of stacked cake objects
    move_5=[]#list to check if we moved the blocks once
    while(not playGame):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()    
            if len(cake_l)>1 and cake_l[-1]!=0:#to ensure we don't move the start cake tier
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:#when the player presses this... the cake tier that's falling will move left
                        cake_obj_list[-1].x=cake_obj_list[-1].x-50
                    elif event.key==pygame.K_RIGHT:#when the player presses this... the cake tier that's falling will move right
                        cake_obj_list[-1].x=cake_obj_list[-1].x+50
                    elif event.key == pygame.K_SPACE:#Pause using space bar
                        pause=True
                        paused()
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                        cake_obj_list[-1].x=cake_obj_list[-1].x
                cake_obj_list[-1].make_cake()
        gameDisplay.blit(back,(0,0))#as we want it to be our background image of 800*600
        if(len(stacked_cakes)>0):
            if(len(stacked_cakes) not in move_5 and len(stacked_cakes)>5 and stacked_cakes[-1].y<400):#to move only once after each score but the movement starts only after 5 cakes are stacked
                move_5.append(len(stacked_cakes))
                for i in stacked_cakes:
                    i.y+=50#move down by 50 pixels
            for i in stacked_cakes:
                i.make_cake()
        if(no_cakes not in cake_l):#We need to make a new cake tier
            if(no_cakes==0):
                c1=cakeTier(450,530,cake1)
                c1.make_cake()
                cake_l.append(no_cakes)
                cake_obj_list.append(c1)
                stacked_cakes.append(c1)
                no_cakes+=1
            elif(no_cakes>0):
                c=cakeTier()#temporary variable to store the cake object
                c.x=random.randrange(200,display_width-200)
                c.cake=random.choice([cake1,cake2])
                c.make_cake()
                stopped_cake=False
                cake_l.append(no_cakes)
                cake_obj_list.append(c)
        elif((no_cakes in cake_l) and no_cakes>0):#if its not the start cake and is alreaady created
            temp_x=cake_obj_list[-1].x
            temp_y=cake_obj_list[-1].y
            temp1_x=stacked_cakes[-1].x
            temp1_y=stacked_cakes[-1].y
            if temp1_y<temp_y+cake_height and temp_y+cake_height<temp1_y+20:#within the y limits of the cake tier top
                if temp1_x>temp_x and temp1_x<temp_x+cake_width and temp_x+cake_width>temp1_x-1+cake_width/2 or temp1_x+cake_width>temp_x and temp1_x+cake_width<temp_x+cake_width and temp_x<temp1_x+1+cake_width/2 :#within the x limits of the cake tier top
                    mixer.Sound.play(sc)
                    stacked_cakes.append(cake_obj_list[-1])
                    stopped_cake=True
                    no_cakes+=1
            if(stopped_cake==False):#if it didnt stop
                cake_obj_list[-1].y=cake_obj_list[-1].y+speed+(no_cakes*0.025)
                cake_obj_list[-1].make_cake()
            
        if(cake_obj_list[-1].y>display_height):#goes out of display height
            no_cakes+=1
        small_text("Background designed by brgfx / Freepik",7,1,580)
        small_text("Score: "+str(len(stacked_cakes)-1),30,0,0)
        if(len(cake_obj_list)>len(stacked_cakes)+1):#If the No. of created cakes are more than that of the stacked cakes, the game ends
            gameOver(len(stacked_cakes))
        pygame.display.update()
        clock.tick(60)
game_intro()
gameLoop()
pygame.quit()
