import pygame
import random
import sys
import time
from pygame.locals import *
pygame.init()


WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
FPS = 60

MAX_GOTTEN_PASS = 10
ZOMBIE_SIZE = 70
ADD_NEW_ZOMBIE_RATE = 30
ADD_NEW_KIND_ZOMBIE = ADD_NEW_ZOMBIE_RATE

NORMAL_ZOMBIE_SPEED = 1
NEW_KIND_ZOMBIE_SPEED = NORMAL_ZOMBIE_SPEED / 1

PLAYER_MOVE_RATE = 15
BULLET_SPEED = 10
ADD_NEW_BULLET_RATE = 15

FUN = True

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)


def terminate():
    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event_ in pygame.event.get():
            if event_.type == QUIT:
                terminate()
            if event_.type == KEYDOWN:
                if event_.key == K_ESCAPE:
                    terminate()
                if event_.key == K_RETURN:
                    return


def player_has_hit_zombie(player_rect, zombies_list):
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

windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70))
drawText('Zombie VS Plants By Yanninay', font, windowSurface, (WINDOW_WIDTH / 4), (WINDOW_HEIGHT / 4))
drawText('Press Enter to start', font, windowSurface, (WINDOW_WIDTH / 3) - 10, (WINDOW_HEIGHT / 3) + 50)
pygame.display.update()
wait_for_player_to_press_key()
while True:

    zombies = []
    newKindZombies = []
    bullets = []

    zombiesGottenPast = 0
    score = 0

    playerRect.topleft = (50, WINDOW_HEIGHT / 2)
    moveLeft = moveRight = False
    moveUp = moveDown = False
    shoot = False

    zombieAddCounter = 0
    newKindZombieAddCounter = 0
    bulletAddCounter = 40


    while True:  
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

                if event.key == K_SPACE:
                    shoot = False

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
        if score >= 10 and score < 15:
            fun = pygame.image.load("fun.gif")
            windowSurface.blit(fun, (0,0))
            NORMAL_ZOMBIE_SPEED = 3
        elif score >= 20 and score < 23:
            fun2 = pygame.image.load("fun2.png")
            windowSurface.blit(fun2, (0,0))
            NEW_KIND_ZOMBIE_SPEED = 3

        

        pygame.display.update()

        if player_has_hit_zombie(playerRect, zombies):
            break
        if player_has_hit_zombie(playerRect, newKindZombies):
            break

        if zombiesGottenPast >= MAX_GOTTEN_PASS:
            break

        mainClock.tick(FPS)

    time.sleep(1)
    if zombiesGottenPast >= MAX_GOTTEN_PASS:
        NORMAL_ZOMBIE_SPEED = 1
        NORMAL_ZOMBIE_SPEED / 1
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70))
        drawText('Score: %s' % score, font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
        drawText('ZOMBIE KILLED YOU', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 100)
        drawText('Press Enter to start the game again, or Escape to exit.', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 150)
        pygame.display.update()
        wait_for_player_to_press_key()
    if player_has_hit_zombie(playerRect, zombies):
        NORMAL_ZOMBIE_SPEED = 1
        NORMAL_ZOMBIE_SPEED / 1
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70))
        drawText('Score: %s' % score, font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
        drawText('ZOMBIE KILLED YOU', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 100)
        drawText('Press Enter to start the game again, or Escape to exit.', font, windowSurface, (WINDOW_WIDTH / 4) - 80,
                 (WINDOW_HEIGHT / 3) + 150)
        pygame.display.update()
        wait_for_player_to_press_key()
