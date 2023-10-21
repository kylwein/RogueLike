import pygame
import constants
import math

class Character():
    def __init__(self, x, y, animation_list):
        self.flip = False
        self.animation_list = animation_list
        self.frame_index = 0 # index to change sprite states
        self.update_time = pygame.time.get_ticks() # time since frame updated
        self.image = animation_list[0]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)


    def move(self, dx, dy):
        # makes it so player does not move twice as fast in diagonal
        if dx != 0 and dy != 0:
            dx = dx * math.sqrt(2)/2
            dy = dy * math.sqrt(2)/2

        # faces the player the correct way
        if dx > 0:
            self.flip = False
        if dx < 0:
            self.flip = True

        # updates player pos
        self.rect.x += dx
        self.rect.y += dy

    def update(self):

        # addresses out of bounds error
        if self.frame_index >= 3:
            self.frame_index = 0

        # sets current character frame state
        self.image = self.animation_list[self.frame_index]

        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)