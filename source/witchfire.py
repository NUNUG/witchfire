import pygame
from pygame.locals import *
import sys
import random
import math
from wfsprites import *
from konami_kode import KonamiKode

# Pygame Setup
pygame.mixer.pre_init(22050, -16, 2, 256)
pygame.mixer.init()
pygame.init()

# SkyFire setup
screen_buffer_width = 640
screen_buffer_height = 480
screen_buffer_dimensions = [screen_buffer_width, screen_buffer_height]
screen_width = 1920
screen_height = 1080
screen_dimensions = [screen_width, screen_height]
screen_buffer = pygame.surface.Surface(screen_buffer_dimensions)
screen = pygame.display.set_mode(screen_dimensions)
clock = pygame.time.Clock()
random.seed(pygame.time.get_ticks())

# Graphics setup
#bg = pygame.transform.scale(pygame.image.load('assets\\slc-night.jpg'), (640, 480))
bg = pygame.transform.scale(pygame.image.load('assets\\images\\village 2.png'), (640, 480))
hero = Hero()
#fireball = Fireball(hero.rect.left + hero.rect.width - 35, hero.rect.top + 5)
fireball = Fireball(hero.rect.left + hero.rect.width - 35, hero.rect.top + 53)
monsters = pygame.sprite.Group()
fodder = pygame.sprite.Group()
font_hud = pygame.font.Font(None, 50)
font_gameover = pygame.font.Font("assets\\fonts\\Gingerbread House.ttf", 100)
pumpkin_bit_images = PumpkinBitImages().images
pumpkin_bits_list = []

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
snd_konami = pygame.mixer.Sound('assets\\sounds\\konami-logo-snes.wav')
snd_hero_hit = pygame.mixer.Sound('assets\\sounds\\melting.wav')
snd_hero_hit.set_volume(0.2)
snd_monster_hit = pygame.mixer.Sound('assets\\sounds\\splatter.wav')
snd_monster_hit.set_volume(0.2)
snd_game_over = pygame.mixer.Sound('assets\\sounds\\what a world.wav')
snd_splatter = pygame.mixer.Sound('assets\\sounds\\splatter.wav')
snd_startup = pygame.mixer.Sound('assets\\sounds\\these things must be done delicately.wav')

snd_background = pygame.mixer.Sound('assets\\sounds\\background.wav')
snd_background.set_volume(0.2)

snd_background.play(-1)

def show_hud(current_score, current_lives):
    scoretext = font_hud.render('Score: ' + str(current_score), 1, [255, 255, 255])
    livestext = font_hud.render('Lives: ' + str(current_lives), 1, [255, 255, 255])
    pygame.draw.rect(screen_buffer, [0, 0, 0], pygame.Rect(0, 449, 639, 479))
    screen_buffer.blit(livestext, pygame.Rect(0, 449, 320, 479))
    screen_buffer.blit(scoretext, pygame.Rect(320, 449, 639, 478))

def silence_all():
    snd_1up.stop()
    snd_fire.stop()
    snd_hero_hit.stop()
    snd_monster_hit.stop()
    snd_game_over.stop()

def game_over():
    snd_background.stop()
    screen_buffer.fill([255, 128, 0])
    gameover_text = font_gameover.render('GAME OVER', True, [0, 0, 0])
    screen_buffer.blit(gameover_text, ((640 - gameover_text.get_rect().width)/ 2, (480 - gameover_text.get_rect().height) /2))
    show_hud(score, lives)
    # Draw buffer to screen.
    screen.blit(pygame.transform.scale(screen_buffer, (screen_width, screen_height)), (0,0))
    pygame.display.update()

def explode_monsters(monsters, bits_list):
    # For each of these monsters, create the bits.
    # Add the bits to the bits list.
    for m in monsters:
        for n in range(5):
            pumpkin_bit = PumpkinBit(m.position, random, pumpkin_bit_images[n])
            bits_list.append(pumpkin_bit)
    pass

def konami_kode_func():
    global lives
    lives += 30
    snd_konami.play()

konami_kode = KonamiKode(konami_kode_func)

snd_startup.play()

# Main game loop
while True:

    clock.tick(100)
    # Look for messages that the game sends to us
    for event in pygame.event.get():
        # User clicked the [X] to quit.  
        if ( event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
            pygame.mixer.quit()
            sys.exit()


    # Game over
    if lives == 0:
        game_over()
        continue

    # Read keyboard
    if pygame.key.get_focused():
        keystates = pygame.key.get_pressed()

        # Look for arrow keys
        btn_uparrow = (keystates[K_KP8] or keystates[K_UP])
        btn_downarrow = (keystates[K_KP2] or keystates[K_DOWN])
        
        # Look for FIRE button (spacebar)
        btn_space = keystates[K_SPACE]

        # Look for Konami code.
        konami_kode.capture(keystates)

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
        fireball.position = (hero.rect.left + hero.rect.width - 35.0, hero.rect.top + 45.0)
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
            # Play a sound.
            snd_monster_hit.play()
        explode_monsters(collisions, pumpkin_bits_list)
    
    # Look for collisions between the hero and the monsters
    collisions = pygame.sprite.spritecollide(hero, monsters, True)
    if (len(collisions) > 0):
        lives = lives - 1
        snd_hero_hit.play()
        if (lives == 0):
            silence_all()
            snd_game_over.play()

            
    # Draw the background
    screen_buffer.blit(bg, [0,0])
    
    # Draw the hero
    hero.animate()
    screen_buffer.blit(hero.image, hero.rect)

    # Draw the fireball
    if fired:
        fireball.animate()
        screen_buffer.blit(fireball.image, fireball.rect)

    # Draw the monsters
    for m in monsters:
        m.animate()
        screen_buffer.blit(m.image, m.rect)

    # Draw the pumpkin bits
    for b in pumpkin_bits_list:
        b.move()
        if b.position[1] > 700:
            pumpkin_bits_list.remove(b)
        screen_buffer.blit(pygame.transform.scale(pygame.transform.rotate(b.image, b.angle), (b.rect.width * b.scale, b.rect.height * b.scale)), Rect(b.rect.left, b.rect.top, b.rect.width, b.rect.height))

    # Draw the HUD
    show_hud(score, lives)

    # Draw the buffer on to the screen.
    screen.blit(pygame.transform.scale(screen_buffer, (screen_width, screen_height)), (0,0))

    # Draw the screen on the monitor.
    pygame.display.update()