import pygame
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, mob_type, boss_enemy, size):
        self.mob_type = mob_type
        self.boss_enemy = boss_enemy

        self.flip = False
        self.animation_list = mob_animations[mob_type]
        self.frame_index = 0 # index to change sprite states
        self.move_state = 0 # idle = 0, run = 1, ...
        self.update_time = pygame.time.get_ticks() # time since frame updated
        self.health = health
        self.alive = True
        self.money = 0

        # image stuff :)
        self.image = self.animation_list[self.move_state][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size) # hitbox
        self.rect.center = (x, y) # center of hitbox


    def move(self, dx, dy, wall_tiles):
        screen_scroll = [0, 0]

        # makes it so player does not move twice as fast in diagonal
        if dx != 0 and dy != 0:
            dx = dx * math.sqrt(2)/2
            dy = dy * math.sqrt(2)/2

        # faces the player where the cursor is
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx

        if x_dist > 0:
            self.flip = False
        if x_dist < 0:
            self.flip = True


        self.rect.x += dx
        # check if player is touching a wall
        for wall in wall_tiles:
            # verify wall and player collision
            if wall[1].colliderect(self.rect):
                # check which side collision occured
                if dx > 0:
                    self.rect.right = wall[1].left
                if dx < 0:
                    self.rect.left = wall[1].right


        self.rect.y += dy
        # check if player is touching a wall
        for wall in wall_tiles:
            # verify wall and player collision
            if wall[1].colliderect(self.rect):
                # check which side collision occured
                if dy > 0:
                    self.rect.bottom = wall[1].top
                elif dy < 0:
                    self.rect.top = wall[1].bottom



        # if player is moving, display running animation
        if dx == 0 and dy == 0:
            self.move_state = 0
        else:
            self.move_state = 1

        # screen only scrolls around player
        if self.mob_type == 0:
            # scrolls camera left/right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH

            # scrolls camera up/down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH

        return screen_scroll

    def ai(self, screen_scroll):
        # moves the enemies based on the screen scrolling
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def update(self):

        if self.health <= 0: #see if your dead
            self.health = 0
            self.alive = False


        # sets current character frame state -- idle version
        self.image = self.animation_list[self.move_state][self.frame_index]

        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # addresses out of bounds error
        if self.frame_index >= len(self.animation_list[self.move_state]):
            self.frame_index = 0

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)

        if self.mob_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.PLAYER_SCALE * constants.OFFSET))
        else:
            if self.alive:
                surface.blit(flipped_image, self.rect)
                pygame.draw.rect(surface, constants.RED, self.rect, 1)
