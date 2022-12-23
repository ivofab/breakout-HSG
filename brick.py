import pygame
import settings
from random import *

#es ist ein konstrukt, welches ermöglicht einfach verschiedene Objekte zu machen, welche eigene Variabeln haben welche
# man sonst alle einzeln angeben müsste. man kann die parameter relativ einfach für die einzlenen bricks verändern
class Brick(object):
    # das self ist, damit man für alle einzelnen Bricks die parameter ändern kann. dann wird das self durch einen bestimmten
    #Brick verändert
    def __init__(self, x, y, w, h, life, ball):
        #wir weisen die parameter vom init den self dinger zu, um es wie gesagt einzeln veränder zu können
        self.life = life
        self.ball = ball
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, display):
        #gibt dem Brick die Farbe zum zugehörigen Leben
        color = settings.color_list[self.life-1]
        #zeichnet den Brick
        pygame.draw.rect(display, color, self.rect)

#ordnet bricks richtig an
def brick_start(brickList):
    for i in range(settings.col):
        for j in range(settings.row):
            #teilt den blöcken die Leben zu
            life = (settings.row-j+settings.life-1)//settings.life
            #fügt der Bricklist die Bricks mit den richtigen positionen zu (die pos wird verändert indem es mit i bzw j von
            #der for schleife multipliziert wird
            brickList.append(Brick((800/settings.col-1) * i + 10, 35 * j + 10, (800-80)/settings.col, 25, life, random() < .25))
