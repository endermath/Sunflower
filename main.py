import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('Flower Game')

seedlingSurfaceObj = pygame.image.load('/Users/fistel/Developer/Sunflower/seedling.png')
flowerSurfaceObj = pygame.image.load('/Users/fistel/Developer/Sunflower/flower.png')
gardenerSurfaceObj = pygame.image.load('/Users/fistel/Developer/Sunflower/gardener.png')

mousex,mousey=0,0

fontObj = pygame.font.Font('freesansbold.ttf', 32)

soundBecomeFlower = pygame.mixer.Sound('/Users/fistel/Developer/Sunflower/becomeFlower.wav')

bigflower=False

while True:
    windowSurfaceObj.fill(pygame.Color(150,100,120))
    if bigflower:
        windowSurfaceObj.blit(flowerSurfaceObj, (150,150))
    else:
        windowSurfaceObj.blit(seedlingSurfaceObj, (150,150))

    windowSurfaceObj.blit(gardenerSurfaceObj, (250,250))
    
    msgSurfaceObj = fontObj.render('Water the flowers!',False,pygame.Color(0,0,0))
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,20)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key in (K_LEFT,K_RIGHT):
                msg = 'yay'
                soundBecomeFlower.play()
                bigflower=True
        
    pygame.display.update()
    fpsClock.tick(30)
    