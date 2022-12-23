import pygame

#Klasse um schneller dinge verändern zu können und damit es im programm einheitlich bleibt
class Platform(object):
    def __init__(self, x, y, w, h, color):
        #gleich wie bei den Bricks
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
    #Platform wird gemalt
    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)