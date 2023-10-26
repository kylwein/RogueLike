import pygame
import math

class Weapon():
    def __init__(self, weapon_image, projectile_image):
        self.projectile_image = projectile_image
        self.original_image = weapon_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False

    def update(self, player):
        projectile = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # self.fired prevents player from spamming infinite bullets
        if pygame.mouse.get_pressed()[0] and self.fired == False: # 0 is left mouse button
            projectile = Projectile(self.projectile_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True

        # resets shooting cooldown
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

        return projectile

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))
