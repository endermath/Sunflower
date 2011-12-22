import pygame, sys, random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Sandy's Sunflowers")

iconsSurfaceObj = pygame.image.load('icons.png')
                           

iconSize=32

# Create subsurfaces for the 16x16 icons from icons.png. Double them in size to get 32x32 surfaces.
def getSurfaceFromIcons(x,y):
    return pygame.transform.scale2x(iconsSurfaceObj.subsurface(Rect(x*16,y*16,16,16)))

wateringCanSurfaceObj = getSurfaceFromIcons(0,0)
waterSplashSurfaceObj = getSurfaceFromIcons(1,0)
flowerSurfaceObj = getSurfaceFromIcons(2,0)
flowerstalkSurfaceObj = getSurfaceFromIcons(2,1)
pelletSurfaceObj = getSurfaceFromIcons(3,0)
skullSurfaceObj = getSurfaceFromIcons(4,0)
tapSurfaceObj = getSurfaceFromIcons(5,0)
tapSplashSurfaceObj = getSurfaceFromIcons(5,1)

sandySurfaceObj = getSurfaceFromIcons(0,1)
dirtSurfaceObj = getSurfaceFromIcons(0,2)
brickSurfaceObj = getSurfaceFromIcons(0,3)

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

def drawIcon(surf,x,y):
    windowSurfaceObj.blit(surf,(x*iconSize,y*iconSize))

class Player:
    xpos = 5  #x position within 32x32 grid
    ypos = screenSize-2  #y position within 32x32 grid
    dir = 1  #1=facing right, -1=facing left
    water = 2000

class Flower:
    height = 1
    water = 3000
    xpos = 1
    def __init__(self,xpos):
        self.xpos = xpos
        self.height = random.randint(1,4)
        self.water = random.randint(2000,4000)

outside = False  # True if outside

player = Player()
flowers = []
flowers.append(Flower(random.randint(1,screenSize-2)))
flowers.append(Flower(random.randint(1,screenSize-2)))
flowers.append(Flower(random.randint(1,screenSize-2)))

watering = False
wateringTime = 30
wateringCounter = wateringTime

while True:
    
    # fill background
    windowSurfaceObj.fill(pygame.Color(38,94,179))
    
    # draw scene
    for y in range(0,screenSize-1):
        if (y<screenSize-3 or not outside):
            windowSurfaceObj.blit(brickSurfaceObj, (0,y*iconSize))
        if (y<screenSize-3 or outside):
            windowSurfaceObj.blit(brickSurfaceObj, ((screenSize-1)*iconSize,y*iconSize))
    for x in range(0,screenSize):
        windowSurfaceObj.blit(dirtSurfaceObj, (x*iconSize, (screenSize-1)*iconSize))
    

    if outside:
        drawIcon(tapSurfaceObj, screenSize-2,screenSize-3)
    else:
        for f in flowers:
            for s in range(1,f.height+1):
                drawIcon(flowerstalkSurfaceObj,f.xpos,screenSize-1-s)    #draw the stalk
            drawIcon(flowerSurfaceObj,f.xpos,screenSize-1-(f.height+1))  #draw the flower on top
            watermeter = fontObj.render(str(f.water/20),False,pygame.Color(20,20,180))
            waterRect=watermeter.get_rect()
            waterRect.centerx=f.xpos*iconSize+iconSize/2
            waterRect.centery=((screenSize-1)*iconSize)+iconSize/2
            windowSurfaceObj.blit(watermeter,waterRect)

    # update flower data
    for f in flowers:
        f.water = max (f.water-1, 0)
        if f.water<=0:
            flowers.remove(f)                   #the flower died of dehydration! :(
            

    
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
            player.water-=5
            if (outside and player.xpos==screenSize-3):
                if wateringCounter%10>5:
                    drawIcon(tapSplashSurfaceObj, screenSize-2,screenSize-2)
                    player.water+=50
            else:    
                windowSurfaceObj.blit(pygame.transform.flip(waterSplashSurfaceObj,(player.dir==-1),False),((2*player.dir+player.xpos)*iconSize,player.ypos*iconSize))
                for f in flowers:
                    if f.xpos == 2*player.dir+player.xpos:
                        f.water+=5
        else:
            watering=False
        
    
    # show some text
    msgSurfaceObj = pygame.transform.scale2x(fontObj.render("Sandy's Sunflowers",False,pygame.Color(0,0,0)))
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.centerx = windowSurfaceObj.get_rect().centerx
    msgRectObj.centery = 20
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)

    msgSurfaceObj = pygame.transform.scale2x(fontObj.render("Water: "+str(player.water/20),False,pygame.Color(0,0,0)))
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.centerx = windowSurfaceObj.get_rect().centerx
    msgRectObj.centery = 50
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
                    player.dir = -1
                    player.xpos -= 1
                    if outside and player.xpos<0:
                        outside=False
                        player.xpos=screenSize-1
                    if not outside and player.xpos<1:
                        player.xpos=1

            if event.key == K_RIGHT:
                    player.dir = 1
                    player.xpos+=1
                    if outside and player.xpos>=screenSize-2:
                        player.xpos = screenSize-3
                    if not outside and player.xpos>=screenSize:
                        outside=True
                        player.xpos=0
            

            if event.key==K_SPACE:
                soundRefillWater.play()
                wateringCounter=wateringTime
                watering=True
        
    pygame.display.update()
    fpsClock.tick(30)
    

