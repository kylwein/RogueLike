import pygame
import weapon
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, mob_type, boss_enemy, size, static = False):
        self.mob_type = mob_type
        self.boss_enemy = boss_enemy

        self.flip = False
        self.animation_list = mob_animations[mob_type]
        self.frame_index = 0 # index to change sprite states
        self.move_state = 0 # idle = 0, run = 1, ...
        self.update_time = pygame.time.get_ticks() # time since frame updated
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.money = 0
        self.stunned = False

        # image stuff :)
        self.image = self.animation_list[self.move_state][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size) # hitbox
        self.rect.center = (x, y) # center of hitbox

        # used so the NPCs stay still
        self.static = static


    def move(self, dx, dy, wall_tiles):
        screen_scroll = [0, 0]

        # makes it so player does not move twice as fast in diagonal
        if dx != 0 and dy != 0:
            dx = dx * math.sqrt(2)/2
            dy = dy * math.sqrt(2)/2

        # faces the main player where the cursor is
        if self.mob_type == 0:
            pos = pygame.mouse.get_pos()
            x_dist = pos[0] - self.rect.centerx

            if x_dist > 0:
                self.flip = False
            if x_dist < 0:
                self.flip = True
        else:
            if dx > 0:
                self.flip = False
            if dx < 0:
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

    def ai(self, player, wall_tiles, screen_scroll, fireball_image):


        # npcs get mad if they take damage
        if self.static and self.health != 50:
            self.static = False

        clipped_line = ()
        stun_cooldown = 100
        ai_dx = 0
        ai_dy = 0
        fireball = None
        # moves the enemies based on the screen scrolling
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        for wall in wall_tiles:
            if wall[1].clipline(line_of_sight):
                clipped_line = wall[1].clipline(line_of_sight)

        # checks distance to player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx)** 2) + ((self.rect.centery - player.rect.centery)**2))
        if not clipped_line and dist > constants.RANGE:
            if self.rect.centerx > player.rect.centerx: # right hand side
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx: # left hand side
                ai_dx = constants.ENEMY_SPEED
            if self.rect.centery > player.rect.centery: # below
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery: # above
                ai_dy = constants.ENEMY_SPEED

        if self.alive and not self.static:

            if not self.stunned:
                self.move(ai_dx, ai_dy, wall_tiles)

                if dist < constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                # boss enemies shoot fireballs
                fireball_cooldown = 700
                if self.boss_enemy:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                            fireball = weapon.Fireball(fireball_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                            self.last_attack = pygame.time.get_ticks()

            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self. move_state = 0
              #  self.update_action(0)
            # idle animation not implemented yet

            if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False

        return fireball



    def update(self):

        if self.health <= 0: #see if your dead
            self.health = 0
            self.alive = False

    # timer to reset hit
        hit_cooldown = 500
        if self.mob_type == 0:
            if self.hit == True:
                if pygame.time.get_ticks() - self.last_hit > hit_cooldown:
                    self.hit = False

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
