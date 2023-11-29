import pygame
import math
import constants
import random


class Weapon():
    def __init__(self, weapon_image, projectile_image):
        self.projectile_image = projectile_image
        self.original_image = weapon_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = 300
        projectile = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # self.fired prevents player from spamming infinite bullets
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot >= shot_cooldown): # 0 is left mouse button
            projectile = Projectile(self.projectile_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

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
        # gets vertical and horizontal speed based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.PROJECTILE_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.PROJECTILE_SPEED)

    def update(self, enemy_list):
        #reset variables
        damage = 0
        damage_pos = None

        # makes projectile move in specific direction
        self.rect.x += self.dx
        self.rect.y += self.dy

        # deletes projectile if it goes off screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill() # deletes projectile

        #check collision between weapon and enemy !!!
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive: # see if weapon hits enemy
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break

        return damage, damage_pos






    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))
