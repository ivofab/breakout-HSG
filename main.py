# alles importieren

from ball import *
from brick import brick_start
from player import Platform
from settings import *
from button import Button


# initialisieren

def update_game_window():
    pygame.display.update()
    #Schwarzer Hintergrund
    display.fill([0, 0, 0])
    #Plattform wird gemalt
    player.draw(display)
    #Alle Bricks von die noch in der Bricklist sind zeichnen
    for brick in brick_list:
        brick.draw(display)
    #Alle Bälle von der Ballliste werden gezeichnet und bewegt
    for ball in ball_list:
        ball.ballmove(display)
        ball.draw(display)


def draw_game_over(win):
    pygame.display.update()
    display.fill([0, 0, 0])
    #zeichnet retry button
    retry.draw(display)
    #zeichnet quit button
    quit.draw(display)
    #wenn gewonnen wird Gewonnenbildschirm gezeigt
    if win:
        draw_text("YOU WON", pygame.font.SysFont('Constantia', 80), white, 400, 400)
    #Wenn nicht gewonnen kommt der GameOver bildschirm
    else:
        draw_text("GAME OVER", pygame.font.SysFont('Constantia', 80), white, 400, 400)



def draw_text(text, font, col, x, y):
    #render, macht aus schrift ein bild und display.blit zeigt dieses Bild auf dem Display an
    text = font.render(text, True, col)
    #wird als Bild zwischengespeichert, somit kann man nacher height und width ausgeben lassen und den Text centern
    h = text.get_height()
    w = text.get_width()
    # setzt mitte des textes an die vorgegebenen koordinaten
    display.blit(text, (x-w/2, y-h/2))

#braucht es für retry. setzt brick und balllist neu auf
def start_game():
    brick_list.clear()
    brick_start(brick_list)
    ball_list.clear()
    ball_list_update(ball_list, 400, 400)


# initialisieren
pygame.init()
display = pygame.display.set_mode((screen_width, screen_height))  # Fenster erstellen
pygame.display.set_caption('Breakout')  # Titel vom Fenster ändern
clock = pygame.time.Clock()  # damit das Game auf allen Geräten gleichschnell abläuft, egal wie leistungsfähig
mouse = pygame.mouse #damit mann später nicht immer pygame.mouse schreiben muss, sondern nur noch mouse

# Buttons erstellen
retry = Button(215, 600, 30, black, white, 'RETRY')
quit = Button(600, 600, 30, black, white, 'QUIT')


# Blöcke erstellen
brick_list = []
brick_start(brick_list)

# Erster Ball erstellen
ball_list = []
ball_list_update(ball_list, 400, 400)


# Player erstellen
player = Platform(400, 700, 100, 15, white)

# game window das erste mal updaten
update_game_window()

# Variabeln für Spiel Ende
run = True
game_over = False
win = False
start = False

# Main Loop
while run:
    #pygame hat Liste mit veschiedenen events, bei dieser Schlaufe, wird jeder dieser Events durchegangen
    for event in pygame.event.get():
        #wenn Fensterschliessbutton gedrückt wird, wird das spiel beendet
        if event.type == pygame.QUIT:
            run = False
        # wenn die Maus gedrückt wurde
        if event.type == pygame.MOUSEBUTTONDOWN:
            # dass es nur Ausgeführt wird wenn das Spiel vorüber ist
            if game_over:
                # wenn die Maus dabei auf dem Rect des retry button war
                if retry.rect.collidepoint(pygame.mouse.get_pos()):
                    # Spiel wird zurück gesetzt und neu gestartet
                    start_game()
                    game_over = False
                    start = False
                    win = False
                # wenn sie dabei auf dem quit knopf war
                elif quit.rect.collidepoint(pygame.mouse.get_pos()):
                    run = False
            # nur ausgeführt wenn das spiel noch nicht gestartet hat. startet das spiel und gibt dem ball seine geschwindigkeit
            elif not start:
                start = True

    # wenn das Spiel am Laufen ist
    if not game_over:
        # zeichnet den text und setzt ball auf die Platform vor Spielbeginn
        if not start:
            draw_text("PRESS MOUSE TO START", pygame.font.SysFont('Constantia', 30), white, 400, 400)
            ball_list[0].x = player.rect.x + player.rect.w / 2
            ball_list[0].y = player.rect.y - ball_list[0].r


        # testet ob noch bälle vorhanden sind und beeendet sonst das spiel
        if not ball_list:
            game_over = True
        # testet ob alle bricks weg sind und wenn ja beendet das spiel als gewonnen
        if not brick_list:
            win = True
            game_over = True

        # platform an Pos der Maus setzen
        # [0] damit nur die x position der maus ausgegeben wird
        #<2 und player.rect.x= 0 ist weil die maus gibt die postion der Mitte des paddlet an.
        # theoretisch würde es dann den Fall geben, dass die maus ganz am linken rand wäre und dann wäre die plattform
        # zur hälfte aus dem display. um dies zu verhindern wird die x koordinate des player auf null gesetzt, wenn die
        # maus weniger oder genau den abstand der hälfte der Breite von der Plattform zur Wand hat.
        if mouse.get_pos()[0] < player.rect.w / 2:
            player.rect.x = 0
        #das gleiche wie oben einfach mit der anderen Seite
        elif (mouse.get_pos()[0]) > screen_width - (player.rect.w / 2):
            player.rect.x = screen_width - player.rect.w  # Plattform von Rand begrenzt
        else:
            player.rect.x = mouse.get_pos()[0] - (
                    player.rect.w / 2)  # der hintere Teil, damit die Maus die Mitte der Plattform steuert und nicht den linken Rand
        # for schleife geht alle bälle durch
        for ball in ball_list:
            if ball.y > screen_height:
                ball_list.remove(ball)  # wenn ein ball aus dem bild ist wird er aus der liste gelöscht
            # Ball prallt an Plattform ab
            #nur colliderect reicht nicht, das and ist wichtig, damit es nur ausgeführt wird, wenn der Ball oberhalb der
            #Platform ist, sonst kommt es zu Problemen, wenn die platform bspw in den Ball hinein fährt würde er dann auch appralen
            if ball.rect.colliderect(player.rect) and ball.y < player.rect.y:
                #da man einwenig in den Ball reinfahren kann, wird der Ball vor dem apprallen zuerst auf die platformoberfläche
                #gesetzt, sonst würde er die ganze zeit hin und her abprallen, weil er dann dauernd mit der platform collided und abprallt
                ball.y = player.rect.y - ball.r
                #Ballbewegungsrichtung wird geändert (prallt ab)
                ball.y_speed *= -1
                #damit man die schräge des Balles verändern kann, machen wir nicht einfalls=Ausfallswinkel, sondern machen
                #die xgeschwindigkeit abhängig von wo der Ball die plattform trifft
                #durch 15, damit man auf eine vernünftige Geschwindigkeitsbreite kommt
                ball.x_speed = (ball.x - player.rect.centerx) / 15  # die x  geschwindigkeit ist abhängig von wo der ball die Plattform trifft
            # Ball prallt an Wand ab
            elif (ball.x - ball.r <= 0):
                ball.x = ball.r
                ball.x_speed *= -1
            elif (ball.x + ball.r >= screen_width):
                ball.x = screen_width - ball.r
                ball.x_speed *= -1
            #Ball prallt oben ab
            elif ball.y - ball.r <= 0:
                ball.y = ball.r
                ball.y_speed *= -1

            # Ball prallt an Bricks ab
            collideList = ball.rect.collidelistall(brick_list)  # füllt eine liste mit allen bricks die getroffen wurden
            # wenn collidelist inhalt hat
            if collideList:
                #ist ein Block in der collidelist, wird der yspeed umgekehrt, damit der ball abprallt
                ball.y_speed *= -1
                #in dieser forschleife werden alle Blöcke in der collidelist durchgegangen
                for index in collideList:
                    #man macht eine Clipline an der linken bzw rechten Seite des brick und testet, ob die eine Schnittfläche
                    # mit dem Ball bildet, falls ja wird der x speed geändert also die Schräge
                    if ball.rect.clipline(brick_list[index].rect.bottomleft,
                                          brick_list[index].rect.topleft) or ball.rect.clipline(
                        brick_list[index].rect.bottomright, brick_list[index].rect.topright):
                        ball.x_speed *= -1
                    brick_list[index].life -= 1  # setzt das leben der Bricks eines runter
                for brick in brick_list:
                    if brick.life <= 0:  # wenn sie kein leben haben werden sie gelöscht muss kleiner gleich sein im
                        # falle das zwei bälle zeitgleich treffen
                        if brick.ball:
                            ball_list_update(ball_list, brick.rect.centerx,
                                             brick.rect.centery)  # wenn der brick einen ball im innern hatte wird der neue ball generiert
                        #der Brick list mit dem collided wurde wird von der bricklist removed, damit er beim update game
                        #window nicht mehr gezeichnet wird
                        brick_list.remove(brick)

        update_game_window()
    # wenn das spiel zuende ist
    else:
        draw_game_over(win)
    # frame rate
    clock.tick(60)

pygame.quit()
