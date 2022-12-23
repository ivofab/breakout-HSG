import pygame


class Button(object):
    def __init__(self, x, y, h, color_button, color_Text, inhalt):
        self.color_button = color_button
        self.color_Text = color_Text
        self.inhalt = inhalt
        self.x = x
        self.y = y
        #Schriftart und Grösse wird definiert
        self.font = pygame.font.SysFont('Constantia', h)
        #Schrift wrid zu Bild gerendert damit wir es besser positioniern können
        self.text = self.font.render(self.inhalt, True, self.color_Text)
        #Buttonbreite wird gleichgesetzt mit schriftrect breite
        self.w = self.text.get_width()
        # Buttonhöhe wird gleichgesetzt mit schriftrect höhe
        self.h = self.text.get_height()
        #das minus self.w/2 ist damit neu das x bzw y vom rect die Mitte ist und nicht mehr den Ecken
        self.rect = pygame.Rect(self.x-self.w/2, self.y-self.h/2, self.w, self.h)
    #buttons werden gemalt
    def draw(self, display):
        pygame.draw.rect(display, self.color_button, self.rect)
        display.blit(self.text, (self.x-self.w/2, self.y-self.h/2))
