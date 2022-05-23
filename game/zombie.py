import pygame
import random
import sys
import time
from pygame.locals import *
from pygame import mixer
pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
FPS = 60

DEFAULT_MUSIC = "grasswalk.ogg"

MAX_GOTTEN_PASS = 10
ZOMBIE_SIZE = 70
ADD_NEW_ZOMBIE_RATE = 30
ADD_NEW_KIND_ZOMBIE = ADD_NEW_ZOMBIE_RATE

NORMAL_ZOMBIE_SPEED = 1
NEW_KIND_ZOMBIE_SPEED = NORMAL_ZOMBIE_SPEED / 1

CHEAT_ACTIVE = False

PLAYER_MOVE_RATE = 15
BULLET_SPEED = 10
ADD_NEW_BULLET_RATE = 15

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

Music = True
MUST_KILL = 100 # I created this variable solely for the convenience of showing this project. This means that you can change the number of zombies you need to kill at any time, thereby making it easier to present yourself (you won't have to score 100 points for a long time)


def terminate():
    print("Thanks for playing!")
    pygame.quit()
    sys.exit()


def waitForPlayerKeyPress():
    global Music
    global MUST_KILL
    global DEFAULT_MUSIC
    global CHEAT_ACTIVE
    while True:
        for event_ in pygame.event.get():
            if event_.type == QUIT:
                terminate()
            if event_.type == KEYDOWN:
                if event_.key == K_ESCAPE:
                    terminate()
                if event_.key == K_RETURN:
                    return
                if event_.key == K_h:
                    print('Welcome to Plants VS Zombies. This is the game Plants VS Zombies developed by Yanninay. Settings:\nP - how to play\nM - music off\nL - developer mode\nG - Github\nC - Cheats')
                if event_.key == K_m:
                    if not Music:
                        main_menu.play()
                        Music = True
                    else:
                        main_menu.stop()
                        fun_music.stop()
                        Music = False
                if event_.key == K_l:
                    MUST_KILL = int(input("Hi, Developer. Enter the number of zombies you need to kill "))
                    print("Okay, now you need to kill", MUST_KILL, "zombies to speed up the game. But keep in mind, I'll return the number of zombies you need to kill to the previous value, to make it easier for you to play.")
                if event_.key == K_g:
                    print("https://github.com/Yanninay/plants-vs-zombies")
                if event_.key == K_c:
                    print("You have activated the cheats. Now during the game by pressing the C key you can remove all zombies from the playing field")
                    CHEAT_ACTIVE = True
                if event_.key == K_p:
                    print("The essence of the game is very simple. You have to defeat all the zombies who are trying to eat you, and not let them go beyond the map. Move using the W and S buttons or the arrow keys. Press the space bar to shoot. ")

                    



def playerHasHitZombie(player_rect, zombies_list):
    for zombie in zombies_list:
        if player_rect.colliderect(zombie['rect']):
            return True
    return False


def bulletHasHitZombie(bullets_l):
    for bullet in bullets_l:
        if bullet['rect'].colliderect(z['rect']):
            bullets_l.remove(bullet)
            return True
    return False


def bulletHasHitCrawler(bullets_l):
    for bullet in bullets_l:
        if bullet['rect'].colliderect(c['rect']):
            bullets_l.remove(bullet)
            return True
    return False


def drawText(text, font_r, surface, x, y):
    text = font_r.render(text, 1, TEXTCOLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text, text_rect)



mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Zombie vs Plants by Yanninay')
pygame.mouse.set_visible(False)


font = pygame.font.SysFont(None, 48)


playerImage = pygame.image.load('SnowPea.gif')
playerRect = playerImage.get_rect()

bulletImage = pygame.image.load('SnowPeashooterBullet.gif')
bulletRect = bulletImage.get_rect()

zombieImage = pygame.image.load('tree.png')
newKindZombieImage = pygame.image.load('ConeheadZombieAttack.gif')

backgroundImage = pygame.image.load('background.png')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOW_WIDTH, WINDOW_HEIGHT))

main_menu = pygame.mixer.Sound("awesomeness.ogg")
fun_music = pygame.mixer.Sound("speedrun.ogg")
main = pygame.mixer.Sound(DEFAULT_MUSIC)
main_menu.play()



windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70))
drawText('Zombie VS Plants By Yanninay', font, windowSurface, (WINDOW_WIDTH / 4), (WINDOW_HEIGHT / 4))
drawText('Press Enter to start', font, windowSurface, (WINDOW_WIDTH / 3) - 10, (WINDOW_HEIGHT / 3) + 50)
drawText('Press H for settings', font, windowSurface, (WINDOW_WIDTH / 3) - 40, (WINDOW_HEIGHT / 3) + 90)
pygame.display.update()
waitForPlayerKeyPress()
while True:
    if Music:
        main_menu.stop()
        main.play()


    zombies = []
    newKindZombies = []
    bullets = []

    zombiesGottenPast = 0
    score = 0

    playerRect.topleft = (50, WINDOW_HEIGHT / 2)
    moveUp = moveDown = False
    shoot = False

    zombieAddCounter = 0
    newKindZombieAddCounter = 0
    bulletAddCounter = 40


    while True:  
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                elif event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                elif event.key == K_SPACE:
                    shoot = True
    

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                elif event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

                elif event.key == K_SPACE:
                    shoot = False
                elif event.key == K_m:
                    if Music:
                        fun_music.stop()
                        main.stop()
                        Music = False
                    else:
                        if score >= MUST_KILL:
                            fun_music.play()
                            Music = True
                        else:
                            main.play()
                            Music = True
                elif event.key == K_c:
                    if CHEAT_ACTIVE:
                        for z in zombies:
                            zombies.remove(z)
                        for c in newKindZombies:
                            newKindZombies.remove(c)

        zombieAddCounter += 1
        if zombieAddCounter == ADD_NEW_KIND_ZOMBIE:
            zombieAddCounter = 0
            zombieSize = ZOMBIE_SIZE
            newZombie = {
                'rect': pygame.Rect(WINDOW_WIDTH, random.randint(10, WINDOW_HEIGHT - zombieSize - 10), zombieSize,
                                    zombieSize),
                'surface': pygame.transform.scale(zombieImage, (zombieSize, zombieSize)),
            }
        
            zombies.append(newZombie)

        newKindZombieAddCounter += 1
        if newKindZombieAddCounter == ADD_NEW_ZOMBIE_RATE:
            newKindZombieAddCounter = 0
            newKind_Zombie_size = ZOMBIE_SIZE
            newCrawler = {
                'rect': pygame.Rect(WINDOW_WIDTH, random.randint(10, WINDOW_HEIGHT - newKind_Zombie_size - 10),
                                    newKind_Zombie_size, newKind_Zombie_size),
                'surface': pygame.transform.scale(newKindZombieImage, (newKind_Zombie_size, newKind_Zombie_size)),
            }
            newKindZombies.append(newCrawler)

    
        bulletAddCounter += 1
        if bulletAddCounter >= ADD_NEW_BULLET_RATE and shoot is True:
            bulletAddCounter = 0
            newBullet = {'rect': pygame.Rect(playerRect.centerx + 10, playerRect.centery - 25, bulletRect.width,
                                             bulletRect.height),
                         'surface': pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
                         }
            bullets.append(newBullet)


        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if moveDown and playerRect.bottom < WINDOW_HEIGHT - 10:
            playerRect.move_ip(0, PLAYER_MOVE_RATE)
  
        for z in zombies:
            z['rect'].move_ip(-1 * NORMAL_ZOMBIE_SPEED, 0)

        for c in newKindZombies:
            c['rect'].move_ip(-1 * NEW_KIND_ZOMBIE_SPEED, 0)


        for b in bullets:
            b['rect'].move_ip(1 * BULLET_SPEED, 0)

        for z in zombies[:]:
            if z['rect'].left < 0:
                zombies.remove(z)
                zombiesGottenPast += 1

        for c in newKindZombies[:]:
            if c['rect'].left < 0:
                newKindZombies.remove(c)
                zombiesGottenPast += 1

                for b in bullets[:]:
                    if b['rect'].right > WINDOW_WIDTH:
                        bullets.remove(b)

        for z in zombies:
            if bulletHasHitZombie(bullets):
                score += 1
                zombies.remove(z)

        for c in newKindZombies:
            if bulletHasHitCrawler(bullets):
                score += 1
                newKindZombies.remove(c)

        windowSurface.blit(rescaledBackground, (0, 0))

        windowSurface.blit(playerImage, playerRect)

        for z in zombies:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindZombies:
            windowSurface.blit(c['surface'], c['rect'])

       
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        
        drawText('Zombie gotten pass: %s' % zombiesGottenPast, font, windowSurface, 10, 20)
        drawText('Score: %s' % score, font, windowSurface, 10, 50)
        if score >= MUST_KILL:
            if Music:
                main.stop()
                fun_music.play()
            NORMAL_ZOMBIE_SPEED = 3
        elif score >= 200:
            NEW_KIND_ZOMBIE_SPEED = 3

        

        pygame.display.update()

        if playerHasHitZombie(playerRect, zombies):
            break
        if playerHasHitZombie(playerRect, newKindZombies):
            break

        if zombiesGottenPast >= MAX_GOTTEN_PASS:
            break

        mainClock.tick(FPS)

    time.sleep(1)
    if zombiesGottenPast >= MAX_GOTTEN_PASS:
        NORMAL_ZOMBIE_SPEED = 1
        NORMAL_ZOMBIE_SPEED / 1
        MUST_KILL = 100
        if Music:
            fun_music.stop()
            main.stop()
            main_menu.play()
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70))
        drawText('Score: %s' % score, font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
        drawText('ZOMBIE KILLED YOU', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 100)
        drawText('Press Enter to start the game again, or Escape to exit.', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 150)
        if CHEAT_ACTIVE:
            drawText('The cheats were disabled after your defeat', font, windowSurface, (WINDOW_WIDTH / 6) - 100,
                 (WINDOW_HEIGHT / 3) + 300)
            CHEAT_ACTIVE = False
        pygame.display.update()
        waitForPlayerKeyPress()
    if playerHasHitZombie(playerRect, zombies):
        NORMAL_ZOMBIE_SPEED = 1
        NORMAL_ZOMBIE_SPEED / 1
        MUST_KILL = 100
        if Music:
            fun_music.stop()
            main.stop()
            main_menu.play()
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70))
        drawText('Score: %s' % score, font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
        drawText('ZOMBIE KILLED YOU', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 100)
        drawText('Press Enter to start the game again, or Escape to exit.', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 150)
        if CHEAT_ACTIVE:
            drawText('The cheats were disabled after your defeat', font, windowSurface, (WINDOW_WIDTH / 6) - 100,
                 (WINDOW_HEIGHT / 3) + 300)
            CHEAT_ACTIVE = False
        pygame.display.update()
        waitForPlayerKeyPress()
