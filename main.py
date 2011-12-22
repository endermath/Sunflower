import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((320,320))
pygame.display.set_caption("Sandy's Sunflowers")

iconsSurfaceObj = pygame.image.load('icons.png')
                           
iconSize=32
# Create subsurfaces for the 16x16 icons from icons.png. Double them in size to get 32x32 surfaces.
wateringCanSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(0,0,16,16)))
waterSplashSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(16,0,16,16)))
sandySurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(0,16,16,16)))
flowerSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(32,0,16,16)))
flowerstalkSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(32,16,16,16)))

# font
fontObj = pygame.font.Font('freesansbold.ttf', 16)

# Load sound effects
soundGrowth = pygame.mixer.Sound('Growth.wav')
soundMove = pygame.mixer.Sound('Move.wav')
soundRefillWater = pygame.mixer.Sound('RefillWater.wav')
soundPickup = pygame.mixer.Sound('Pickup.wav')


class Player:
    xpos = 5  #x position within 32x32 grid
    ypos = 5  #y position within 32x32 grid
    dir = 1  #1=facing right, -1=facing left
    screen = 0  # 0 = garden, 1 = outside

class Flower:
    def __init__(self):
        value = 0

player = Player()
flowers = []
flowers.append(Flower())
watering = False

while True:
    
    # fill background
    windowSurfaceObj.fill(pygame.Color(70,70,70))
    # draw Sandy and her watering can
    windowSurfaceObj.blit(sandySurfaceObj, (player.xpos*iconSize,player.ypos*iconSize))
    windowSurfaceObj.blit(wateringCanSurfaceObj, ((1+player.xpos)*iconSize,player.ypos*iconSize))
    
    #if watering
    if watering:
        windowSurfaceObj.blit(waterSplashSurfaceObj, ((2+player.xpos)*iconSize,player.ypos*iconSize))
    
    # show some text
    msgSurfaceObj = pygame.transform.scale2x(fontObj.render("Sandy's Sunflowers",False,pygame.Color(0,0,0)))
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.centerx = windowSurfaceObj.get_rect().centerx
    msgRectObj.centery = 20
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)
    
    # take care of events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            
            if event.key in (K_LEFT,K_RIGHT,K_DOWN,K_UP):
                soundMove.play()
                if event.key == K_DOWN:
                    player.ypos +=1
                if event.key == K_UP:
                    player.ypos -=1
                if event.key == K_LEFT:
                    player.xpos -=1
                if event.key == K_RIGHT:
                    player.xpos +=1

            if event.key==K_SPACE:
                soundRefillWater.play()
        
    pygame.display.update()
    fpsClock.tick(30)
    

