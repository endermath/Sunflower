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
    waterMax = 10000.0
    xpos = 1
    def __init__(self,xpos):
        self.xpos = xpos
        self.height = random.randint(1,4)
        self.water = random.randint(1000,3000)
        self.growCounter = 0
        self.isFinished = False
        
    def grow(self):
        if not self.isFinished:
            self.water = self.water-self.height/3
            if self.water<0:
                self.isFinished = True
            else:
                self.growCounter += self.water/2500.0
                if self.growCounter > 200:
                    self.growCounter = 0
                    self.height += 1
                    if self.height > screenSize-5:
                        self.isFinished = True
            

    def draw(self):
        for s in range(1,self.height+1):
            drawIcon(flowerstalkSurfaceObj,self.xpos,screenSize-1-s)    #draw the stalk
        drawIcon(flowerSurfaceObj,self.xpos,screenSize-1-(self.height+1))  #draw the flower on top
        meterRect = Rect(self.xpos*iconSize, (screenSize-1)*iconSize + iconSize/4, int(round(iconSize*self.water/self.waterMax)), iconSize/4)
        windowSurfaceObj.fill(pygame.Color(20,20,220), meterRect)
        

class FallingItem:
    surf = None

    def __init__(self,xpos,ypos):
        self.xpos=xpos*iconSize
        self.ypos=ypos*iconSize
        self.xspeed = random.gauss(0,10)
        self.yspeed = random.gauss(0,3)
        self.onFloorCounter = 70
        self.isFalling = True
        
    def fallAndDecideIfTimeToRemove(self):
        if self.isFalling:
            self.xpos=self.xpos+self.xspeed
            if self.xpos > (screenSize-2)*iconSize or self.xpos < iconSize :
                self.xspeed = -self.xspeed
            
            self.yspeed = self.yspeed + 0.2
            self.ypos=self.ypos+self.yspeed
            if self.ypos > (screenSize-2)*iconSize:
                self.ypos =(screenSize-2)*iconSize 
                self.yspeed = -0.5*self.yspeed
                if int(round(self.yspeed))==0:
                    self.ypos = (screenSize-2)*iconSize
                    self.isFalling = False

        else:
            self.onFloorCounter -=1 
            if self.onFloorCounter<0:
                return False
        return True

    def draw(self):
        if self.ypos<(screenSize-2)*iconSize or self.onFloorCounter>30 or self.onFloorCounter%2>0:
            windowSurfaceObj.blit(self.surf,(int(round(self.xpos)),int(round(self.ypos))))

class Skull(FallingItem):
    surf = skullSurfaceObj
    def giveBonus(self,p):
        p.water = p.water/2
        soundSkullPickup.play()

class Pellet(FallingItem):
    surf = pelletSurfaceObj
    def giveBonus(self,p):
        p.score += 5
        p.pellets += 1
        soundPickup.play()

class FlowerItem(FallingItem):
    surf = flowerSurfaceObj
    def giveBonus(self,p):
        p.score+= 100
        soundPickup.play()

class FlowerStalkItem(FallingItem):
    surf = flowerstalkSurfaceObj
    def giveBonus(self,p):
        p.score+= 50
        soundPickup.play()

# Global variables common to both title screen and game loop
hiscore = 0
isPlayingTheGame = True
# Constants
fallSpawnTime = 40


# Show title screen and wait for player to press space.
def showTitleScreen():
    global isPlayingTheGame,hiscore

    # fill background black
    windowSurfaceObj.fill(pygame.Color(0,0,0))

    # print some text
    myRender(windowSurfaceObj,(20,20),"Sandy's Sunflowers")
    myRender(windowSurfaceObj,(20,40),"Keys: Left Right Space Return")
    myRender(windowSurfaceObj,(20,60),"Press space to play")
    
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

    isWaiting = True
    while isWaiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_SPACE:
                    isWaiting = False
        pygame.display.update()
        fpsClock.tick(30)




class Game():
    def __init__(self):        
        self.player = Player()
        self.flowers = []
        self.flowers.append(Flower(random.randint(1,screenSize-2)))
        self.flowers.append(Flower(random.randint(1,screenSize-2)))
        self.flowers.append(Flower(random.randint(1,screenSize-2)))

        self.fallingItems = []
        self.fallingFlowers = []

        self.fallSpawnCounter = fallSpawnTime   #delay until next falling item is created
        self.wateringCounter = 0            #for animating the splashing of water when watering or refilling



    def updateObjects(self):
        # falling items
        for f in self.fallingItems:
            if not f.fallAndDecideIfTimeToRemove():
                self.fallingItems.remove(f)
        for f in self.fallingFlowers:
            if not f.fallAndDecideIfTimeToRemove():
                self.fallingFlowers.remove(f)
                
        self.fallSpawnCounter -=1
        if self.fallSpawnCounter<0:
            self.fallSpawnCounter = fallSpawnTime+random.randint(10,50)
            pos=random.randint(1,screenSize-3)
            self.fallingItems.append(random.choice([Skull(pos,0),Pellet(pos,0)]))

        # flowers
        for f in self.flowers:
            f.grow()
            if f.isFinished:
                self.fallingFlowers.append(FlowerItem(f.xpos, screenSize-2-f.height))
                for s in range(0,f.height):
                    self.fallingFlowers.append(FlowerStalkItem(f.xpos, screenSize-2-s))
                self.flowers.remove(f)                   #turn flower into falling pieces!
                
            

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
                itemRect = Rect(int(round(f.xpos)),int(round(f.ypos)),iconSize,iconSize)
                playerRect = Rect(self.player.xpos*iconSize,self.player.ypos*iconSize,iconSize,iconSize)
                if itemRect.colliderect(playerRect):
                    f.giveBonus(self.player)
                    self.fallingItems.remove(f)

                    
        #if inside, draw flowers
        else:
            for f in self.flowers:
                f.draw()
            for f in self.fallingFlowers:
                f.draw()
                flowerRect = Rect(int(round(f.xpos)),int(round(f.ypos)),iconSize,iconSize)
                playerRect = Rect(self.player.xpos*iconSize,self.player.ypos*iconSize,iconSize,iconSize)
                if flowerRect.colliderect(playerRect):
                    f.giveBonus(self.player)
                    self.fallingFlowers.remove(f)
                

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
        pelletsPosx = (screenSize*iconSize-6*charSize)/2
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

        
        hiscore = max(hiscore, self.player.score)

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
                if event.key==K_RETURN:
                    if (not self.player.watering) and (not self.player.refilling) and (not self.player.isOutside):
                        target = self.player.dir+self.player.xpos
                        if (target in range(1,screenSize-2)) and (not target in [f.xpos for f in self.flowers]) and self.player.pellets>0:
                            self.flowers.append(Flower(target))
                            self.player.pellets-=1
                            
                            
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
    

