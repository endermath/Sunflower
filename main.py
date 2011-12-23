import pygame, sys, random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Sandy's Sunflowers")

scaleFactor=2


iconSize=16*scaleFactor

iconsSurfaceObj = pygame.image.load('icons2.png')
(iconsSizex,iconsSizey) = iconsSurfaceObj.get_size()
iconsSurfaceObj = pygame.transform.scale(iconsSurfaceObj,(scaleFactor*iconsSizex,scaleFactor*iconsSizey))

                                    
fontSurfaceObj = pygame.image.load('font.png')
(fontSizex,fontSizey) = fontSurfaceObj.get_size()
fontSurfaceObj = pygame.transform.scale(fontSurfaceObj,(scaleFactor*fontSizex,scaleFactor*fontSizey))
charSize = 8*scaleFactor

fontmap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ:1234567890' ="


def myRender(surf,pos,text):
    (posx,posy)=pos
    text=text.upper()
    for char in text:
        charSurf = fontSurfaceObj.subsurface(Rect(fontmap.index(char)*charSize,0,charSize,charSize))
        surf.blit(charSurf,(posx,posy))
        posx+=charSize
        

# Create subsurfaces for the icons
def getSurfaceFromIcons(x,y):
    return iconsSurfaceObj.subsurface(Rect(x*iconSize,y*iconSize,iconSize,iconSize))

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
screenSize = 16  #number of icons that fit in either direction
windowSurfaceObj = pygame.display.set_mode((screenSize*iconSize, screenSize*iconSize))

# Load sound effects
soundGrowth = pygame.mixer.Sound('Growth.wav')
soundMove = pygame.mixer.Sound('Move.wav')
soundRefillWater = pygame.mixer.Sound('RefillWater.wav')
soundPickup = pygame.mixer.Sound('Pickup.wav')
soundSkullPickup = pygame.mixer.Sound('SkullPickup.wav')

def drawIcon(surf,x,y):
    windowSurfaceObj.blit(surf,(x*iconSize,y*iconSize))

class Player:
    xpos = 5  #x position within 32x32 grid
    ypos = screenSize-2  #y position within 32x32 grid
    dir = 1  #1=facing right, -1=facing left
    water = 2000
    pellets = 0
    watering = False  #true when watering flowers
    refilling = False #true when refilling water
    maxWater = 8000
    score = 0
    isOutside = False  # True if outside
    
    def draw(self):
        # draw Sandy and her watering can
        if (self.dir==1):
            windowSurfaceObj.blit(sandySurfaceObj, (self.xpos*iconSize,self.ypos*iconSize))
            windowSurfaceObj.blit(wateringCanSurfaceObj, ((self.dir+self.xpos)*iconSize,self.ypos*iconSize))
        else:
            windowSurfaceObj.blit(pygame.transform.flip(sandySurfaceObj,True,False), (self.xpos*iconSize,self.ypos*iconSize))
            windowSurfaceObj.blit(pygame.transform.flip(wateringCanSurfaceObj,True,False), ((self.dir+self.xpos)*iconSize,self.ypos*iconSize))

    def moveLeft(self):
        if not self.watering:
            self.dir = -1
        self.xpos -= 1
        if self.isOutside and self.xpos<0:
            self.isOutside=False
            self.xpos=screenSize-1
        if not self.isOutside and self.xpos<1:
            self.xpos=1

    def moveRight(self):
        if not self.watering:
            self.dir = 1
        self.xpos+=1
        if self.isOutside and self.xpos>=screenSize-2:
            self.xpos = screenSize-3
        if not self.isOutside and self.xpos>=screenSize:
            self.isOutside=True
            self.xpos=0

class Flower:
    height = 1
    water = 3000
    xpos = 1
    def __init__(self,xpos):
        self.xpos = xpos
        self.height = random.randint(1,4)
        self.water = random.randint(2000,4000)

class FallingItem:
    xpos = 4
    ypos = 0
    surf = None
    fallTime = 15
    fallCounter = 15
    onFloorTime = 100
    onFloorCounter = 100

    def __init__(self,xpos):
        self.xpos=xpos
        self.fallCounter = self.fallTime
        self.onFloorCounter = self.onFloorTime

    def fallAndDecideIfTimeToRemove(self):
        self.fallCounter-=1
        if self.fallCounter<0:
            self.fallCounter=self.fallTime
            self.ypos=min(self.ypos+1,screenSize-2)
        if self.ypos == screenSize-2:
            self.onFloorCounter -=1
            if self.onFloorCounter<0:
                return False
        return True
    def draw(self):
        if self.ypos<screenSize-2 or self.onFloorCounter>30 or self.onFloorCounter%2>0:
            drawIcon(self.surf,self.xpos,self.ypos)

class Skull(FallingItem):
    surf = skullSurfaceObj
    def giveBonus(self,p):
        p.water = p.water/2
        soundSkullPickup.play()

class Pellet(FallingItem):
    surf = pelletSurfaceObj
    def giveBonus(self,p):
        p.pellets += 1
        soundPickup.play()




# Global variables common to both title screen and game loop
hiscore = 0
isPlayingTheGame = True
# Constants
fallSpawnTime = 60


# Show title screen and wait for player to press space.
def showTitleScreen():
    global isPlayingTheGame,hiscore

    # fill background black
    windowSurfaceObj.fill(pygame.Color(0,0,0))

    # print some text
    myRender(windowSurfaceObj,(20,20),"Sandy's Sunflowers")
    myRender(windowSurfaceObj,(20,40),"Press space to play")
    
#    msgSurfaceObj = fontObj.render("Sandy's Sunflowers",False,pygame.Color(20,200,20))
#    msgRectObj = msgSurfaceObj.get_rect()
#    msgRectObj.centerx = windowSurfaceObj.get_rect().centerx
#    msgRectObj.centery = 20
#    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)

#    msgSurfaceObj = fontObj.render("Press space to play",False,pygame.Color(20,200,20))
#    msgRectObj = msgSurfaceObj.get_rect()
#    msgRectObj.centerx = windowSurfaceObj.get_rect().centerx
#    msgRectObj.centery = 50
#    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key==K_SPACE:
                initGame()
                titleScreen = False


class Game():
    def __init__(self):        
        self.player = Player()
        self.flowers = []
        self.flowers.append(Flower(random.randint(1,screenSize-2)))
        self.flowers.append(Flower(random.randint(1,screenSize-2)))
        self.flowers.append(Flower(random.randint(1,screenSize-2)))

        self.fallingItems = []

        self.fallSpawnCounter = fallSpawnTime   #delay until next falling item is created
        self.wateringCounter = 0            #for animating the splashing of water when watering or refilling



    def updateObjects(self):
        # falling items
        for f in self.fallingItems:
            if not f.fallAndDecideIfTimeToRemove():
                self.fallingItems.remove(f)
        self.fallSpawnCounter -=1
        if self.fallSpawnCounter<0:
            self.fallSpawnCounter = fallSpawnTime+random.randint(10,50)
            pos=random.randint(1,screenSize-3)
            self.fallingItems.append(random.choice([Skull(pos),Pellet(pos)]))

        # flowers
        for f in self.flowers:
            f.water = max (f.water-1, 0)
            if f.water<=0:
                self.flowers.remove(f)                   #the flower died of dehydration! :(
            

    def drawScene(self,isOutside):
        # fill background
        windowSurfaceObj.fill(pygame.Color(38,94,179))
        
        # draw bricks and dirt
        for y in range(0,screenSize-1):
            if (y<screenSize-3 or not isOutside):
                windowSurfaceObj.blit(brickSurfaceObj, (0,y*iconSize))
            if (y<screenSize-3 or isOutside):
                windowSurfaceObj.blit(brickSurfaceObj, ((screenSize-1)*iconSize,y*iconSize))
        for x in range(0,screenSize):
            windowSurfaceObj.blit(dirtSurfaceObj, (x*iconSize, (screenSize-1)*iconSize))
        

        #if outside, draw tap and update falling items
        if isOutside:
            drawIcon(tapSurfaceObj, screenSize-2,screenSize-3)
            for f in self.fallingItems:
                f.draw()
                if (f.xpos,f.ypos) == (self.player.xpos,self.player.ypos):
                    f.giveBonus(self.player)
                    self.fallingItems.remove(f)

                    
        #if inside, draw flowers
        else:
            for f in self.flowers:
                for s in range(1,f.height+1):
                    drawIcon(flowerstalkSurfaceObj,f.xpos,screenSize-1-s)    #draw the stalk
                drawIcon(flowerSurfaceObj,f.xpos,screenSize-1-(f.height+1))  #draw the flower on top
                #watermeter = fontObj.render(str(f.water/20),False,pygame.Color(20,20,180))
                #waterRect=watermeter.get_rect()
                #waterRect.centerx=f.xpos*iconSize+iconSize/2
                #waterRect.centery=((screenSize-1)*iconSize)+iconSize/2
                #windowSurfaceObj.blit(watermeter,waterRect)

    def displayScore(self):
        #print score etc at top of screen
        windowSurfaceObj.fill(pygame.Color(0,0,0),Rect(0,0,screenSize*iconSize,2*iconSize))
        
        #print score
        scoreTextx = ((screenSize*iconSize/2)-5*charSize)/2
        scoreTexty = 0 
        myRender(windowSurfaceObj,(scoreTextx,scoreTexty),"SCORE")
        
        scoreWidth = charSize * len(str(self.player.score))
        scorex = ((screenSize*iconSize/2)-scoreWidth)/2
        scorey = scoreTexty+charSize
        myRender(windowSurfaceObj,(scorex,scorey),str(self.player.score))

        #print hiscore
        hiscoreTextx = screenSize*iconSize/2 + ((screenSize*iconSize/2)-7*charSize)/2
        hiscoreTexty =0
        myRender(windowSurfaceObj,(hiscoreTextx,hiscoreTexty),"HISCORE")
        
        hiscoreWidth = charSize * len(str(hiscore))
        hiscorex = screenSize*iconSize/2+((screenSize*iconSize/2)-hiscoreWidth)/2
        hiscorey = hiscoreTexty+charSize
        myRender(windowSurfaceObj,(hiscorex,hiscorey),str(hiscore))
        
        #draw water bar
        waterBarx = 0
        waterBary = charSize * 2
        waterBarLength = int(screenSize*iconSize*self.player.water/float(self.player.maxWater))
        windowSurfaceObj.fill(pygame.Color(20,20,240),Rect(waterBarx,waterBary, waterBarLength, charSize))
        
        #draw pellets
        pelletsPosx = 0
        pelletsPosy = charSize * 3
        windowSurfaceObj.blit(pelletSurfaceObj,(pelletsPosx,pelletsPosy-charSize))
        myRender(windowSurfaceObj,(pelletsPosx+iconSize,pelletsPosy),"="+str(self.player.pellets))

        
    def gameLoop(self):    
        global hiscore, isPlayingTheGame
        self.updateObjects()
        self.drawScene(self.player.isOutside)
        self.player.draw()

        # If player is watering, animate splashing and give water to flower
        if self.player.watering:
            self.wateringCounter = self.wateringCounter-1 % 10
            if self.player.water>0:
                self.player.water = max(self.player.water-15,0)
                for f in self.flowers:
                    if f.xpos == 2*self.player.dir+self.player.xpos:
                        f.water+=15
                if self.wateringCounter%2>0:
                    windowSurfaceObj.blit(pygame.transform.flip(waterSplashSurfaceObj,(self.player.dir==-1),False),((2*self.player.dir+self.player.xpos)*iconSize,self.player.ypos*iconSize))
            else:
                self.player.watering=False
                soundRefillWater.stop()

        # If refilling water at the tap, animate splashing and give player water
        if self.player.refilling:
            self.wateringCounter = self.wateringCounter-1 % 10
            #flash water splash below the tap
            if self.wateringCounter%2>0:
                drawIcon(tapSplashSurfaceObj, screenSize-2,screenSize-2)
            self.player.water = min(self.player.water+50,self.player.maxWater)

        
        self.displayScore()

        # take care of events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key in (K_LEFT,K_RIGHT):
#                    soundMove.play()
                    if event.key == K_LEFT:
                        self.player.moveLeft()
                    if event.key == K_RIGHT:
                        self.player.moveRight()
                if event.key==K_SPACE:
                    if (not self.player.watering) and (not self.player.refilling):
                        if (self.player.isOutside and self.player.xpos==screenSize-3):
                            self.player.refilling=True
                            soundRefillWater.play(loops=-1)  #plays water sound and loop it indefinitely
                        else:
                            if self.player.water>0:
                                self.player.watering=True
                                soundRefillWater.play(loops=-1)
            elif event.type==KEYUP:
                if event.key==K_SPACE:
                    self.player.watering = False
                    self.player.refilling = False
                    soundRefillWater.stop()         #stop playing water sound
                    
                

            
            
while True:
    showTitleScreen()
    game = Game()
    while (isPlayingTheGame):
        game.gameLoop()
        pygame.display.update()
        fpsClock.tick(30)
    

