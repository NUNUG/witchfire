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
        She also keeps track of where she is on the screen."""
    def __init__(self, target_size, initial_position, list_of_image_files):
        MovingSprite.__init__(self, initial_position)
        # Set up multiple images for animation and use the first one for now.
        self._images = self.load_images(target_size, list_of_image_files)
        self._image_count = len(self._images)
        self._image_index = 0
        self._animate_marker = pygame.time.get_ticks()
        self.image = self._images[self._image_index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = initial_position
    def load_images(self, target_size, list_of_image_files):
        result = []
        for filename in list_of_image_files:
            loaded_image = pygame.transform.scale(pygame.image.load(filename), target_size)
            result.append(loaded_image)
        return result
    def animate(self):
        """Switches between images to create animation."""
        # Check to see if we've used this image long enough.
        frames_per_second = 10
        milliseconds_per_frame = 1000.0 / frames_per_second
        milliseconds_since_last_animation = pygame.time.get_ticks() - self._animate_marker
        if milliseconds_since_last_animation > milliseconds_per_frame:
            # Move to the other image and reset the timer.
            self._animate_marker = pygame.time.get_ticks()
            self._image_index = (self._image_index + 1) % self._image_count
            self.image = self._images[self._image_index]

class Hero(AnimatedSprite):
    """This is our witch.  She has two images so we can animate her.
        She also keeps track of where she is on the screen."""
    def __init__(self):
        #AnimatedSprite.__init__(self, (150, 30), (0, 200), ['assets\\images\\hero1.png', 'assets\\images\\hero2.png'])
        AnimatedSprite.__init__(self, (150, 117), (0, 200), [
            'assets\\images\\witch-1.png',
            'assets\\images\\witch-2.png',
            'assets\\images\\witch-3.png',
            'assets\\images\\witch-4.png'
        ])

    
class Fireball(AnimatedSprite):
    """This is the "bullet" fired by our hero."""
    def __init__(self, xpos, ypos):
        AnimatedSprite.__init__(self, (35, 20), (xpos, ypos), ['assets\\images\\fireball1.png', 'assets\\images\\fireball2.png'])

class Monster(AnimatedSprite):
    """This is a monster which knows how to move in evasive ways."""
    def __init__(self, initial_position, x_movement_path, y_movement_path):
        AnimatedSprite.__init__(self, (100, 75), initial_position, [
            'assets\\images\\jackolantern-0.png',
            'assets\\images\\jackolantern-1.png',
            'assets\\images\\jackolantern-2.png',
            'assets\\images\\jackolantern-3.png'
        ])
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
        posx = xdistance + xoffset
        posy = ydistance + yoffset
        MovingSprite.move(self, posx, posy)

        # Advance to the next path offset. Wrap around if we hit the end of xpath or ypath.
        self.x_path_index = (self.x_path_index + 1) % self.x_path_len
        self.y_path_index = (self.y_path_index + 1) % self.y_path_len

class PumpkinBitImages:
    def __init__(self):
        self._target_size = (50, 50)
        self.images = [
            pygame.transform.scale(pygame.image.load("assets\\images\\pumpkin-bits-0.png"), (self._target_size[0] * 2, self._target_size[1] * 2)),
            pygame.transform.scale(pygame.image.load("assets\\images\\pumpkin-bits-1.png"), self._target_size),
            pygame.transform.scale(pygame.image.load("assets\\images\\pumpkin-bits-2.png"), self._target_size),
            pygame.transform.scale(pygame.image.load("assets\\images\\pumpkin-bits-3.png"), self._target_size),
            pygame.transform.scale(pygame.image.load("assets\\images\\pumpkin-bits-4.png"), self._target_size),
            pygame.transform.scale(pygame.image.load("assets\\images\\pumpkin-bits-5.png"), self._target_size)
        ]

class PumpkinBit(pygame.sprite.Sprite):
    """This is a piece of a pumpkin which has been blown up.  It will fly in a random direction, 
    but then be influenced backward by its impact with the fireball and ascend downward according to gravity."""
    def __init__(self, initial_position, rando, image):
        self.position = initial_position
        self.default_speed = 1.0
        self.gravity = 0.098
        self.explosion_x_velocity = 1.0 * rando.randint(-1000, 1000) * 0.001 * self.default_speed * 1.0
        self.explosion_y_velocity = 1.0 * rando.randint(-1000, 1000) * 0.001 * self.default_speed * 1.0
        self.explosion_velocity = (self.explosion_x_velocity, self.explosion_y_velocity)
        self.impact_inertia = 2.75
        self.velocity = (self.explosion_velocity[0] + self.impact_inertia, self.explosion_velocity[1] * 1.0)
        self.angle = rando.randint(0, 359)
        self.angular_velocity = rando.randint(-1000, 1000) * 0.001 * 5.0
        self.image = image
        self.scale = 0.75
        self.rect = image.get_rect()
    def _rotate(self):
        self.angle = self.angle + self.angular_velocity
    def _apply_physics(self):
        self.velocity = (self.velocity[0] * 1.0, self.velocity[1] +  self.gravity)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
    def move(self):
        self._rotate()
        self._apply_physics()

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