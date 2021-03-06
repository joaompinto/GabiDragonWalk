import pygame
from pygame.draw import circle
from dragonwalk.gfx.sprites import AnimableSprite

RIGHT = 1
LEFT = 2

class Player(pygame.sprite.Sprite):

    def __init__(self, sprite, walk_step_points=50):
        super(Player, self).__init__()
        self.image = sprite.image
        self.hspeed = 0
        self.speed = 5
        self.rect = sprite.rect
        self.face_direction = RIGHT
        self.vspeed = 0
        self._level = None
        self.sprite = sprite
        self.walk_step = 0
        self.walk_step_points = walk_step_points
        self._is_shooting = False

    @property
    def is_shooting(self):
        return self._is_shooting

    @property
    def position(self):
        return self.sprite.rect.x, self.sprite.rect.y

    @position.setter
    def position(self, value):
        self.sprite.rect.x, self.sprite.rect.y = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    def update(self, collidable=pygame.sprite.Group(), event=None):
        self._is_shooting = False
        hitting_the_ground_boundary = False
        self.experience_gravity()

        self.rect.x += self.hspeed

        # Check horizontal collisions
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if self.hspeed > 0:
                self.rect.right = collided_object.rect.left
            if self.hspeed < 0:
                self.rect.left = collided_object.rect.right

        self.rect.y += self.vspeed

        # Check level boundaries
        if self.rect.bottom > self.level.size[1]:
            self.position = self.position[0], self.level.size[1] - self.rect.height
            #self.rect.bottom = self.level.size[1]
            if self.vspeed > 0:
                hitting_the_ground_boundary = True
                self.vspeed = 0

        # Check vertical collisions
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if self.vspeed > 0:
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            if self.vspeed < 0:
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.hspeed = -self.speed
                if event.key == pygame.K_RIGHT:
                    self.hspeed = self.speed
                if event.key in [pygame.K_UP, pygame.K_SPACE]:
                    if hitting_the_ground_boundary or len(collision_list) > 0:  # Only jump when hitting in the ground
                        self.vspeed = -self.speed*2
                    self._is_shooting = True

            if event.type == pygame.KEYUP:  # Reset current speed
                if event.key == pygame.K_LEFT:
                    if self.hspeed < 0:
                        self.hspeed = 0
                if event.key == pygame.K_RIGHT:
                    if self.hspeed > 0:
                        self.hspeed = 0

        if self.sprite.images_count > 1:
            if self.hspeed == 0:
                self.sprite.selected_image_pos = 0
            else:
                if self.position[0] % self.walk_step_points == 0:
                    self.walk_step += 1
                    self.walk_step %= self.sprite.images_count
                self.sprite.selected_image_pos = self.walk_step

        if self.face_direction == RIGHT and self.hspeed < 0:
            self.sprite.flip(True, False)
            self.face_direction = LEFT
        if self.face_direction == LEFT and self.hspeed > 0:
            self.sprite.flip(True, False)
            self.face_direction = RIGHT


    def experience_gravity(self, gravity=.35):
        if self.vspeed == 0:  # Keep applying gravity
            self.vspeed = 1
        else:
            self.vspeed += gravity

    def draw(self, surface):
        surface.blit(self.sprite.image, self.rect)
        offset = 20
        #if self.face_direction == RIGHT:
        #    offset = self.rect.width-20
        #circle(surface, (255, 0, 0), (self.rect.x+offset, self.rect.y+self.rect.height), 5, 5)
