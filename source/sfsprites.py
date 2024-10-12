import pygame
import math

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.position = initial_position
    def move(self, x_distance, y_distance):
        """Changes the location of the hero on the screen.
            Positive values move down and right, negative values move up and left."""
        (xval, yval) = self.position
        xval = xval + x_distance
        yval = yval + y_distance
        self.position = (xval, yval)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position
        

class AnimatedSprite(MovingSprite):
    """This is a sprite with two frames.
        He also keeps track of where he is on the screen."""
    def __init__(self, target_size, initial_position, imagefilename1, imagefilename2):
        MovingSprite.__init__(self, initial_position)
        # Set up 2 images for animation and use the first one for now.
        self._image1 = pygame.transform.scale(pygame.image.load(imagefilename1), target_size)
        self._image2 = pygame.transform.scale(pygame.image.load(imagefilename2), target_size)
        self._images = [self._image1, self._image2]
        self._image_index = 0
        self._animate_marker = pygame.time.get_ticks()
        self.image = self._images[self._image_index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = initial_position
    def animate(self):
        """Switches between images to create animation."""
        # Check to see if we've used this image long enough.
        frames_per_second = 10
        milliseconds_per_frame = 1000.0 / frames_per_second
        milliseconds_since_last_animation = pygame.time.get_ticks() - self._animate_marker
        if milliseconds_since_last_animation > milliseconds_per_frame:
            # Move to the other image and reset the timer.
            self._animate_marker = pygame.time.get_ticks()
            self._image_index = (self._image_index + 1) % 2
            self.image = self._images[self._image_index]
            #self.rect = self.image.get_rect()

class Hero(AnimatedSprite):
    """This is our hero.  He has two images so we can animate him.
        He also keeps track of where he is on the screen."""
    def __init__(self):
        AnimatedSprite.__init__(self, (150, 30), (0, 200), 'assets\\hero1.png', 'assets\\hero2.png')

    
class Fireball(AnimatedSprite):
    """This is the "bullet" fired by our hero."""
    def __init__(self, xpos, ypos):
        AnimatedSprite.__init__(self, (35, 20), (xpos, ypos), 'assets\\fireball1.png', 'assets\\fireball2.png')

class Monster(MovingSprite):
    """This is a monster which knows how to move in evasive ways."""
    def __init__(self, initial_position, x_movement_path, y_movement_path):
        MovingSprite.__init__(self, initial_position)
        self.image = pygame.transform.scale(pygame.image.load('assets\\monster1.png'), (100, 75))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (initial_position)
        self.x_path = x_movement_path
        self.y_path = y_movement_path
        self.x_path_len = len(self.x_path)
        self.y_path_len = len(self.y_path)
        self.x_path_index = 0
        self.y_path_index = 0
    def move(self, xdistance, ydistance):
        """Moves the sprite along its predisposed path but also offset by the
            specified distance like a normal sprite."""
        # Figure next value in the path
        xoffset = self.x_path[self.x_path_index]
        yoffset = self.y_path[self.y_path_index]
        ## Move
        #MovingSprite.move(self, xdistance + xoffset, ydistance + yoffset)

        # This part is working and necessary.
        #self.rect.left = self.rect.left + xdistance
        #self.rect.top = self.rect.top + ydistance
        #MovingSprite.move(self, xdistance + xoffset, ydistance + yoffset)
        #posx, posy = ()
        posx = xdistance + xoffset
        posy = ydistance + yoffset
        MovingSprite.move(self, posx, posy)

        # Advance to the next path offset. Wrap around if we hit the end of xpath or ypath.
        self.x_path_index = (self.x_path_index + 1) % self.x_path_len
        self.y_path_index = (self.y_path_index + 1) % self.y_path_len


def create_sinewave(increments):
    result = []
    for j in range(increments):
        result.append(math.sin(2 * math.pi * j / increments))
    return result

def create_sinewave_diff(increments, multiplier):
    sinewave = create_sinewave(increments)
    diffwave = []
    x = 0
    for f in sinewave:
        if x == 0:
            diffwave.append(sinewave[x])
        else:
            diffwave.append(sinewave[x] - sinewave[x-1])
        x = x + 1
    result = []
    for f in diffwave:
        result.append(f * multiplier)
    return result