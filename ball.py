import pygame
import settings


class Ball(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.x_speed = 0
        self.y_speed = settings.y_base_speed
        #zuerst wird ein Kreis gezeichnet, da wird die Mitte ausgegeben, bei einem Rechteck geht es um die Ecken, deshalb
        #muss der radius subtrahiert werden
        self.rect = pygame.Rect(x - r, y - r, 2 * r, 2 * r)

    #der Ball wird gezeichnet
    def draw(self, display):
        pygame.draw.circle(display, self.color, [self.x, self.y], self.r)

    #x koordinate wird mit dem xspeed bzw yspeed adsiert, somit bewegt der Ball sich.
    def ballmove(self, display):
        self.x += self.x_speed
        self.y += self.y_speed
        #der ball wird upgedatet mit den neuen x und y koordinaten
        self.rect.update(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)


def ball_list_update(ballList, x, y):
    ballList.append(Ball(x, y, 15, settings.white))
