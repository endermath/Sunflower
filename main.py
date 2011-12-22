import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Sandy's Sunflowers")

iconsSurfaceObj = pygame.image.load('icons.png')
                           

iconSize=32

# Create subsurfaces for the 16x16 icons from icons.png. Double them in size to get 32x32 surfaces.
wateringCanSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(0,0,16,16)))
waterSplashSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(16,0,16,16)))
flowerSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(32,0,16,16)))
flowerstalkSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(32,16,16,16)))
sandySurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(0,16,16,16)))
dirtSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(0,32,16,16)))
brickSurfaceObj = pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(0,48,16,16))) 

# Create a screen
screenSize = 16
windowSurfaceObj = pygame.display.set_mode((screenSize*iconSize, screenSize*iconSize))

# font
fontObj = pygame.font.Font('freesansbold.ttf', 16)

# Load sound effects
soundGrowth = pygame.mixer.Sound('Growth.wav')
soundMove = pygame.mixer.Sound('Move.wav')
soundRefillWater = pygame.mixer.Sound('RefillWater.wav')
soundPickup = pygame.mixer.Sound('Pickup.wav')


class Player:
    xpos = 5  #x position within 32x32 grid
    ypos = screenSize-2  #y position within 32x32 grid
    dir = 1  #1=facing right, -1=facing left
    screen = 0  # 0 = garden, 1 = outside

class Flower:
    def __init__(self):
        value = 0

player = Player()
flowers = []
flowers.append(Flower())
watering = False
wateringTime = 30
wateringCounter = wateringTime

while True:
    
    # fill background
    windowSurfaceObj.fill(pygame.Color(38,94,179))
    
    # draw scene
    for y in range(0,screenSize-1):
        windowSurfaceObj.blit(brickSurfaceObj, (0,y*iconSize))
        if (y<screenSize-3):
            windowSurfaceObj.blit(brickSurfaceObj, ((screenSize-1)*iconSize,y*iconSize))
    for x in range(0,screenSize):
        windowSurfaceObj.blit(dirtSurfaceObj, (x*iconSize, (screenSize-1)*iconSize))
    
    windowSurfaceObj.blit(flowerstalkSurfaceObj, (3*iconSize, (screenSize-2)*iconSize))
    windowSurfaceObj.blit(flowerSurfaceObj, (3*iconSize, (screenSize-3)*iconSize))

    
    # draw Sandy and her watering can
    if (player.dir==1):
        windowSurfaceObj.blit(sandySurfaceObj, (player.xpos*iconSize,player.ypos*iconSize))
        windowSurfaceObj.blit(wateringCanSurfaceObj, ((player.dir+player.xpos)*iconSize,player.ypos*iconSize))
    else:
        windowSurfaceObj.blit(pygame.transform.flip(sandySurfaceObj,True,False), (player.xpos*iconSize,player.ypos*iconSize))
        windowSurfaceObj.blit(pygame.transform.flip(wateringCanSurfaceObj,True,False), ((player.dir+player.xpos)*iconSize,player.ypos*iconSize))

    
    #if watering
    if watering:
        wateringCounter -= 1
        if (wateringCounter>0):            
            windowSurfaceObj.blit(pygame.transform.flip(waterSplashSurfaceObj,(player.dir==-1),False),((2*player.dir+player.xpos)*iconSize,player.ypos*iconSize))
        else:
            watering=False
        
    
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
            
            if event.key in (K_LEFT,K_RIGHT):
                soundMove.play()
                if event.key == K_LEFT:
                    player.xpos = max(player.xpos-1,1)
                    player.dir = -1
                if event.key == K_RIGHT:
                    player.xpos = min(player.xpos+1,screenSize-2)
                    player.dir = 1

            if event.key==K_SPACE:
                soundRefillWater.play()
                wateringCounter=wateringTime
                watering=True
        
    pygame.display.update()
    fpsClock.tick(30)
    

