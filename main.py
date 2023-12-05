import pygame
from pygame import mixer
import csv
import constants
from character import Character
from weapon import Weapon
from item import Item
from world import World

import numpy as np

# *** ADDITIONAL TO DO LIST ***
# ( ) Fix enemy hitbox
# ( ) Make potion have 4 total frames, so it is animated
# ( ) Tweak Enemy Health and Hitbox arguments
# ( ) Find other Music/Sounds effects
# (X) Fix character field of view orientation (following mouse cursor)

# initializes pygame and music mixer
mixer.init()
pygame.init()

# sets screen dimensions
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Jason Journey")

# sets game frame rate
clock = pygame.time.Clock()

# movement trigger variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# defines which level to load from csv
level = 99
start_intro = True
screen_scroll = [0, 0]


# -- SOUNDS AND MUSIC --
# load music and sounds
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

# *** change this based on weapon held
projectile_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
projectile_fx.set_volume(0.5)

hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)

coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)

potion_fx = pygame.mixer.Sound("assets/audio/heal.wav")
potion_fx.set_volume(0.5)

# define font!!
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)


# helper function for image scaling
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


# ** LOADS ITEMS **
# loads heart
empty_heart = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
                          constants.ITEM_SCALE)
half_heart = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
full_heart = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# loads coin
coin_frames = []
for i in range(4):
    image = scale_image(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_frames.append(image)

# load consumables
pwr_up = []
for i in range(4):
    image = scale_image(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.ITEM_SCALE)
    pwr_up.append(image)

all_items = []
all_items.append(coin_frames)
all_items.append(pwr_up)

# loads weapons
pistol_img = pygame.image.load("assets/images/weapons/pistol.png").convert_alpha()
pistol_image = scale_image(pistol_img, constants.WEAPON_SCALE)
fireball_image = scale_image(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),
                             constants.FIREBALL_SCALE)

# loads ammo projectile
projectile_img = pygame.image.load("assets/images/weapons/blue_lightsaber.png").convert_alpha()
projectile_image = scale_image(projectile_img, constants.WEAPON_SCALE)

# creates our level tileset
tile_list = []
for x in range(constants.DIFF_TILES + 1):  # addresses out of bounds error
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# loads all mob entities
mob_animations = []
mob_types = ["jason", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon", "merchant"]
animation_types = ["idle", "run"]

for mob in mob_types:
    # clears animation list
    temp_mob_list = []

    for animation in animation_types:
        # clears temporary list
        temp_action_list = []

        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_image(img, constants.PLAYER_SCALE)
            temp_action_list.append(img)

        temp_mob_list.append(temp_action_list)

    mob_animations.append(temp_mob_list)


# draws text onto screen
def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


# displays game info
def game_info():
    # draw HUD
    pygame.draw.rect(screen, (constants.HUD_COLOR), (0, 0, constants.SCREEN_WIDTH, 50))

    # draw hearts
    has_half_heart = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(full_heart, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and has_half_heart == False:
            screen.blit(half_heart, (10 + i * 50, 0))
            has_half_heart = True
        else:
            screen.blit(empty_heart, (10 + i * 50, 0))

    # draws the level number
    if level != 99:
        draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
    else:
        draw_text("SHOP", font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)

    # draw wallet ***change how money is displayed
    draw_text(f"Gold: {player.money}", font, constants.RED, constants.SCREEN_WIDTH - 150, 15)
    draw_text(f"X {player.money}", font, constants.RED, constants.SCREEN_WIDTH - 75, 15)

#creates class for screenfading
class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
        
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: #entire screen fade up to open the game
            pygame.draw.rect(screen, self.color,(0 - self.fade_counter,0, contants.SCREEN_WIDTH //2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color,(contants.SCREEN_WIDTH //2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color,(0,0 - self.fade_counter, contants.SCREEN_WIDTH, constants.SCREEN_HEIGHT//2))
            pygame.draw.rect(screen, self.color,(0, constants.SCREEN_HEIGHT//2 + self.fade_counter,contants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2: #fades down like it's closing the game
            pygame.draw.rect(screen, self.color, (0,0,constants.SCREEN_WITDH, 0 + self.fade_counter))
            
        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True
            
        return fade_complete
                
# tileset creation for level
world_data = []

# dummy data to populate the list so it is not empty
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

# overwrites dummy data with actual level
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, all_items, mob_animations)


# this function can be deleted later on, it just shows the grid outlines
# make sure to also delete where it is being called down below
def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0),
                         (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE),
                         (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))


# damage class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # makes so that the damage display scrolls appropriately
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # moves damage text up
        self.rect.y -= 1
        # deletes the counter after time
        self.counter += 1
        if self.counter > 30:
            self.kill()


# creates our hero and his weapon!
player = world.player
pistol = Weapon(pistol_image, projectile_image)

# gets the enemy list from the world class
enemy_list = world.all_enemies

# gets the npc list from the world class
npc_list = world.all_npcs

# creates sprite group for projectiles
damage_text_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_frames, True)
item_group.add(score_coin)

# loads all items from the world class
for item in world.all_items:
    item_group.add(item)

#creates actual Screenfades
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade (2, constants.PINK, 4)

# keeps window open till user closes it
run = True  # GAME LOOP
while run:

    # sets frame rate and screen background color
    clock.tick(constants.FPS)
    screen.fill(constants.BACKGROUND)

    # can be deleted later
    draw_grid()
    
    # if statement will make sure player can't run around after he's dead
    if player.alive:
    # change in x and y
        dx = 0
        dy = 0
    
        if moving_right:
            dx = constants.PLAYER_SPEED
        if moving_left:
            dx = -constants.PLAYER_SPEED
        if moving_up:
            dy = -constants.PLAYER_SPEED
        if moving_down:
            dy = constants.PLAYER_SPEED
    
        # moves player and stores screen scroll returned value
        screen_scroll = player.move(dx, dy, world.wall_tiles)
    
        # ** UPDATE METHODS **
    
    
    
    
        # updates the level tileset
        world.update(screen_scroll)
    
        # updates enemy animated state
        for enemy in enemy_list:
            fireball = enemy.ai(player, world.wall_tiles, screen_scroll, fireball_image)
            if fireball:
                fireball_group.add(fireball)
            if enemy.alive:
                enemy.update()
    
        # updates the npcs
        for npc in npc_list:
            npc.ai(player, world.wall_tiles, screen_scroll, fireball_image)
            npc.update()
    
        # updates player animated state
        player.update()
        # updates projectile state
        projectile = pistol.update(player)
        if projectile:
            projectile_group.add(projectile)
            projectile_fx.play()
        # working collision of projectiles with enemies
        for projectile in projectile_group:
            damage, damage_pos = projectile.update(screen_scroll, world.wall_tiles, enemy_list + npc_list)
            if damage:
                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                damage_text_group.add(damage_text)
                hit_fx.play()
        damage_text_group.update()
        fireball_group.update(screen_scroll, player)
        # scrolls screen while keeping items where they belong
        item_group.update(screen_scroll, player, coin_fx, potion_fx)



    # ** DRAW METHODS **

    # creates the level tileset
    world.draw(screen)


    # displays the enemy
    for enemy in enemy_list:
        enemy.draw(screen)
    for npc in npc_list:
      npc.draw(screen)
    # displays the player (Jason!), weapon, and items
    player.draw(screen)
    pistol.draw(screen)
    item_group.draw(screen)
    # displays projectiles (weapon bullets, etc)
    for projectile in projectile_group:
        projectile.draw(screen)
    for fireball in fireball_group:
        fireball.draw(screen)
    damage_text_group.draw(screen)
    # draws top part of screen with hp, text, coin sprite
    game_info()
    score_coin.draw(screen)

#checks to see if level is complete
    if level_complete == True:
        start_intro = True
        level ==1
        
        #there's a bunch of code here having to do with levels

#show intro
    if start_intro == True:
        if intro_fade.fade():
            start_intro = False
            intro_fade.fade_counter = 0

#show death!
    if player.alive == False:
        if death_fade.fade():
            death_fade.fade_counter = 0
            start_intro = True
    #the bunch of level code needs to be copied down here
    # delete temp_hp = player.health and player.health = temp_hp
        
    # event handler
    for event in pygame.event.get():

        # finishes loop when you close the game window
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            # moves right
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            # moves left
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            # moves up
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = True
            # moves down
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = True

        # stops player movement if key is let go
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = False

    pygame.display.update()

# quits pygame
pygame.quit()
