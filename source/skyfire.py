import pygame
from pygame.locals import *
import sys
import random
import math
from sfsprites import *



# Pygame Setup
pygame.mixer.pre_init(22050, -16, 2, 256)
pygame.mixer.init()
pygame.init()

# SkyFire setup
screen = pygame.display.set_mode([640, 480])
clock = pygame.time.Clock()
random.seed(pygame.time.get_ticks())

# Graphics setup
bg = pygame.transform.scale(pygame.image.load('assets\\slc-night.jpg'), (640, 480))
hero = Hero()
fireball = Fireball(hero.rect.left + hero.rect.width - 35, hero.rect.top + 5)
monsters = pygame.sprite.Group()
hudfont = pygame.font.Font(None, 50)


# Game metrics setup
hero_speed = 5.0
fired = False
fireball_speed = 15.0
monster_speed = 1.0
monsters_per_second = 1.5
monster_frequency = 1000.0 / monsters_per_second
last_monster_time = 0
score = 0
lives = 3
initial_monster_speed = monster_speed
initial_monsters_per_second = monsters_per_second
initial_monster_frequency = monster_frequency


# Sound setup
snd_fire = pygame.mixer.Sound('assets\\sounds\\fire.wav')
snd_1up = pygame.mixer.Sound('assets\\sounds\\1up.wav')
snd_hero_hit = pygame.mixer.Sound('assets\\sounds\\hero-hit.wav')
snd_hero_hit.set_volume(0.2)
snd_monster_hit = pygame.mixer.Sound('assets\\sounds\\monster-hit.wav')
snd_monster_hit.set_volume(0.2)
snd_background = pygame.mixer.Sound('assets\\sounds\\background.wav')
snd_background.set_volume(0.2)

snd_background.play(-1)


def show_hud(current_score, current_lives):
    scoretext = hudfont.render('Score: ' + str(current_score), 1, [255, 255, 255])
    livestext = hudfont.render('Lives: ' + str(current_lives), 1, [255, 255, 255])
    pygame.draw.rect(screen, [0, 0, 0], pygame.Rect(0, 449, 639, 479))
    screen.blit(livestext, pygame.Rect(0, 449, 320, 479))
    screen.blit(scoretext, pygame.Rect(320, 449, 639, 478))

def game_over():
        snd_background.stop()
        screen.fill([255, 0, 0])
        gameover_font = pygame.font.Font(None, 100)
        gameover_text = gameover_font.render('GAME OVER', True, [0, 0, 0])
        screen.blit(gameover_text, ((640 - gameover_text.get_rect().width)/ 2, (480 - gameover_text.get_rect().height) /2))
        show_hud(score, lives)
        pygame.display.update()

# Main game loop
while True:
    clock.tick(100)
    # Look for messages that the game sends to us
    for event in pygame.event.get():
        # User clicked the [X] to quit.  
        if event.type == pygame.QUIT:
            pygame.mixer.quit()
            sys.exit()


    # Game over
    if lives == 0:
        game_over()
        continue

    
    if pygame.key.get_focused():
        keystates = pygame.key.get_pressed()

        # Look for arrow keys
        btn_uparrow = (keystates[K_KP8] or keystates[K_UP])
        btn_downarrow = (keystates[K_KP2] or keystates[K_DOWN])
        
        # Look for FIRE button (spacebar)
        btn_space = keystates[K_SPACE]

    # Create new monsters if needed
    if (pygame.time.get_ticks() - last_monster_time > monster_frequency):
        amplitude = score + 1
        if (amplitude > 100): 
            amplitude = 100
        monsters.add(Monster( (640, random.randint(0, 300)), [0], create_sinewave_diff(math.trunc(640.0 / 8), amplitude)))
        last_monster_time = pygame.time.get_ticks()
        

    # Move objects around
    if btn_uparrow:
        # Move player up
        if hero.rect.top > 0 + hero_speed:
            hero.move(0, -hero_speed)

    if btn_downarrow:
        # Move player down
        if (hero.rect.bottom + hero_speed) < 479:
            hero.move(0, hero_speed)

    if btn_space and (not fired):
        # Launch a fireball.
        fireball.position = (hero.rect.left + hero.rect.width - 35.0, hero.rect.top + 5.0)
        snd_fire.play()
        fired = True

    if fired:
        # Move the fireball
        fireball.move(fireball_speed, 0)
        if fireball.rect.left > 640:
            # Fireball missed.  End it.
            fired = False


    # Move each monster
    for m in monsters:
        m.move(-monster_speed, 0)
    for m in monsters:
        if m.rect.left < -200:
            monsters.remove(m)
            


    # Look for collisions between the fireball and the monsters
    if (fired):
        collisions = pygame.sprite.spritecollide(fireball, monsters, True)
        if (len(collisions) > 0):
            fired = False
            score = score + 1
            if (score % 20) == 0:
                lives = lives + 1
                snd_1up.play()
            # Make it harder!
            monster_speed = initial_monster_speed + (score / 100.0)
            monsters_per_second = initial_monsters_per_second + (score / 100.0)
            monster_frequency = 1000.0 / monsters_per_second
            # TODO: Play a sound
            snd_monster_hit.play()
    
    # Look for collisions between the hero and the monsters
    collisions = pygame.sprite.spritecollide(hero, monsters, True)
    if (len(collisions) > 0):
        lives = lives - 1
        snd_hero_hit.play()

            
    # Draw the background
    screen.blit(bg, [0,0])
    
    # Draw the hero
    hero.animate()
    screen.blit(hero.image, hero.rect)

    # Draw the fireball
    if fired:
        fireball.animate()
        screen.blit(fireball.image, fireball.rect)

    # Draw the monsters
    for m in monsters:
        screen.blit(m.image, m.rect)

    # Draw the HUD
    show_hud(score, lives)

    # Draw the scene onto the monitor.
    pygame.display.update()