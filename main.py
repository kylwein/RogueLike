import pygame
import random
from pygame import mixer
import csv
import constants
from character import Character
from weapon import Weapon
from item import Item
from world import World
from button import Button
from wave import WaveFunctionCollapse

# *** ADDITIONAL TO DO LIST ***
# ( ) Fix enemy hitbox
# ( ) Make potion have 4 total frames, so it is animated
# ( ) Tweak Enemy Health and Hitbox arguments
# ( ) Find other Music/Sounds effects
# (X) Fix character field of view orientation (following mouse cursor)
# ( ) Fix Merchant Spawn position (spawning a tile too low)

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
level = 0
screen_scroll = [0, 0]

# game intro animation and whether player completed the level
start_intro = False
start_game = False
pause_game = False
level_complete = False

# ----------------------------------------------------
# |                 Sounds Effects                   |
# ----------------------------------------------------

# music
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

# projectile shot sound
projectile_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
projectile_fx.set_volume(0.5)

# enemy is hit
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)

# coin is collected
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)

# potion is collected
potion_fx = pygame.mixer.Sound("assets/audio/heal.wav")
potion_fx.set_volume(0.5)

# define font!!
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# helper function for image scaling
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# scales background images (game menu, game over screen, etc)
def background_scaler(image):
    # gets the original dimensions of the image
    original_width = image.get_width()
    original_height = image.get_height()

    # finds appropriate scale factor
    scale_factor_width = constants.SCREEN_WIDTH / original_width
    scale_factor_height = constants.SCREEN_HEIGHT / original_height

    # uses greater factor so image covers the entire screen
    scale_factor = min(scale_factor_width, scale_factor_height)

    # scales the image
    return scale_image(image, scale_factor)

# ----------------------------------------------------
# |                   Loads Items                    |
# ----------------------------------------------------

# game intro image
intro = pygame.image.load("assets/images/backgrounds/game_intro.png").convert_alpha()
intro_image = background_scaler(intro)

# game over image
gameover = pygame.image.load("assets/images/backgrounds/game_over.png").convert_alpha()
gameover_image = background_scaler(gameover)

# button images
start_image = scale_image(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(),
                          constants.BUTTON_SCALE)
exit_image = scale_image(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(),
                          constants.BUTTON_SCALE)
restart_image = scale_image(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(),
                          constants.BUTTON_SCALE)
resume_image = scale_image(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(),
                          constants.BUTTON_SCALE)

# hearts
empty_heart = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
                          constants.ITEM_SCALE)
half_heart = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),
                         constants.ITEM_SCALE)
full_heart = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),
                         constants.ITEM_SCALE)
# coin
coin_frames = []
for i in range(4):
    image = scale_image(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_frames.append(image)

# consumables (eg. potion)
pwr_up = []
for i in range(4):
    image = scale_image(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.ITEM_SCALE)
    pwr_up.append(image)

# creates list with the created items
all_items = [coin_frames, pwr_up]

# weapons
pistol_img = pygame.image.load("assets/images/weapons/pistol.png").convert_alpha()
pistol_image = scale_image(pistol_img, constants.WEAPON_SCALE)
fireball_image = scale_image(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),
                             constants.FIREBALL_SCALE)
# player projectiles
projectile_img = pygame.image.load("assets/images/weapons/blue_lightsaber.png").convert_alpha()
projectile_image = scale_image(projectile_img, constants.PROJECTILE_SCALE)

# mob entities
mob_animations = []
mob_types = ["jason", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon", "merchant"]
animation_types = ["idle", "run"]

# creates our level tile set
tile_list = []
for x in range(constants.DIFF_TILES + 1):  # addresses out of bounds error
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

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

def reset_level():
  damage_text_group.empty()
  projectile_group.empty()
  item_group.empty()
  fireball_group.empty()

  #create empty tile list
  data = []
  for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    data.append(r)

  return data

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

    # draws the level number -- the shop is numbered 99
    if level != 99:
        draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
    else:
        draw_text("SHOP", font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)

    # draws player wallet
    draw_text(f"x{player.money}", font, constants.WHITE, constants.SCREEN_WIDTH - 75, 15)


# class used for screen fading
class ScreenFade():
    def __init__(self, direction, color, speed, fade_image=None):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
        self.image = fade_image

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed

        if self.image:
            # if an image is provided, draw it at the center of the screen
            image_x = (constants.SCREEN_WIDTH - self.image.get_width()) // 2
            image_y = (constants.SCREEN_HEIGHT - self.image.get_height()) // 2
            screen.blit(self.image, (image_x, image_y))

        if self.direction == 1: # fades up to open the game
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0,
                                                  constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0,
                                                  constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter,
                                                  constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, constants.SCREEN_HEIGHT//2 + self.fade_counter,
                                                  constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2:  # fades down like it's closing the game
            pygame.draw.rect(screen, self.color, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete

# ----------------------------------------------------
# |                    World Gen                     |
# ----------------------------------------------------

level_width, level_height = 15, 15
def add_perimeter_walls(world_data, wall_tile_index):
    rows = level_width
    columns = level_height

    # Top and bottom rows
    for col in range(columns):
        world_data[0][col] = wall_tile_index
        world_data[rows - 1][col] = wall_tile_index

    # Left and right columns
    for row in range(1, rows - 1):
        world_data[row][0] = wall_tile_index
        world_data[row][columns - 1] = wall_tile_index

def place_exit(world_data, exit_tile_index):
    rows = level_width
    columns = level_height

    while True:
        x = random.randint(1, rows - 2)
        y = random.randint(1, columns - 2)

        # Ensure the chosen spot is not a wall
        if world_data[x][y] != 7:  # Assuming 7 is the wall tile index
            world_data[x][y] = exit_tile_index
            break

# tile set creation for level
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

# wave = WaveFunctionCollapse()
# random_level = wave.collapse(level_width, level_height)
#
# def is_wall(tile_name):
#     return "wall" in tile_name
#
# for x, row in enumerate(random_level):
#     for y, potential in enumerate(row):
#         tile_type = potential.state.name
#         if is_wall(tile_type):
#             world_data[x][y] = 7
#         elif tile_type == "floor":
#             world_data[x][y] = 0
#         else:
#             print(tile_type)
#             world_data[x][y] = -1




# add_perimeter_walls(world_data, 7)
# place_exit(world_data, 8)
# world_data[5][5] = 11


world = World()
world.process_data(world_data, tile_list, all_items, mob_animations)



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

score_coin = Item(constants.SCREEN_WIDTH - 90, 23, 0, coin_frames, True)
item_group.add(score_coin)

# loads all items from the world class
for item in world.all_items:
    item_group.add(item)

intro_fade = ScreenFade(1, constants.BLACK, 8)
death_fade = ScreenFade(2, constants.FADE_BLACK, 12)

# ----------------------------------------------------
# |                    Game Loop                     |
# ----------------------------------------------------

# creates buttons
start_button = Button(constants.SCREEN_WIDTH // 2 - 45, constants.SCREEN_HEIGHT // 2 + 50, start_image)
exit_button = Button(25, 475, exit_image)
restart_button = Button(constants.SCREEN_WIDTH // 2 - restart_image.get_width() // 2, 450, restart_image)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_image)

# keeps window open till user closes it
run = True
while run:
    # sets frame rate and screen background color
    clock.tick(constants.FPS)

    if not start_game:

        screen.blit(intro_image, (0, 0))
        #screen.fill(constants.MENU_BACKGROUND)
        #draw_text("JASON JOURNEY", font, constants.BLACK, 270, 100)

        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game:
            screen.fill(constants.MENU_BACKGROUND)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False

        else:
            screen.fill(constants.BACKGROUND)

            # player can't run around after he's dead
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
        
                # ----------------------------------------------------
                # |                 Update Methods                   |
                # ----------------------------------------------------
    
                # level tile set
                world.update(screen_scroll)
        
                # enemy animated state
                for enemy in enemy_list:
                    fireball = enemy.ai(player, world.wall_tiles, screen_scroll, fireball_image)
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive:
                        enemy.update()
    
                # non-playable characters (npcs) such as the Merchant
                for npc in npc_list:
                    npc.ai(player, world.wall_tiles, screen_scroll, fireball_image)
                    npc.update()
    
                # player animated state
                player.update()
        
                # projectile state
                projectile = pistol.update(player)
                if projectile:
                    projectile_group.add(projectile)
                    projectile_fx.play()
        
                # working collision of projectiles with enemies
                for projectile in projectile_group:
                    characters_list = enemy_list + npc_list
                    damage, damage_pos = projectile.update(screen_scroll, world.wall_tiles, characters_list)
                    if damage:
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                        damage_text_group.add(damage_text)
                        hit_fx.play()

                damage_text_group.update()
                fireball_group.update(screen_scroll, player)
        
                # scrolls screen while keeping items where they belong
                item_group.update(screen_scroll, player, coin_fx, potion_fx)

            # ----------------------------------------------------
            # |                  Draw Methods                    |
            # ----------------------------------------------------

            # level tile set
            world.draw(screen)
            
            # enemy
            for enemy in enemy_list:
                enemy.draw(screen)
            for npc in npc_list:
                npc.draw(screen)
            
            # main character, weapon, and items
            player.draw(screen)
            pistol.draw(screen)
            item_group.draw(screen)
            
            # projectiles
            for projectile in projectile_group:
                projectile.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            damage_text_group.draw(screen)
        
            # top part of screen with hp, text, coin sprite
            game_info()
            score_coin.draw(screen)

            # ----------------------------------------------------
            # |                Event Handler                     |
            # ----------------------------------------------------

            # checks to see if level is complete
            if not level_complete:
                varrect = player.get_rect()
                if varrect.colliderect(world.ladder_tile[1]):
                    level_complete = True

            if level_complete:
                start_intro = True
                level += 1

                # -----------------------------------------------
                # |             Recreates the World             |
                # -----------------------------------------------

                # tile set creation for level
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

                # resets player position to the position from the world class
                newpos = world.player.get_pos()
                player.set_pos(newpos)

                # gets the enemy list from the world class
                enemy_list = world.all_enemies

                # gets the npc list from the world class
                npc_list = world.all_npcs

                # creates sprite group for projectiles
                damage_text_group = pygame.sprite.Group()
                projectile_group = pygame.sprite.Group()
                item_group = pygame.sprite.Group()
                fireball_group = pygame.sprite.Group()

                score_coin = Item(constants.SCREEN_WIDTH - 90, 23, 0, coin_frames, True)
                item_group.add(score_coin)

                # loads all items from the world class
                for item in world.all_items:
                    item_group.add(item)

                level_complete = False
                # ** can add a probability of being taken to the shop

            # displays game intro
            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            # show death!
            if not player.alive:
                if death_fade.fade():

                    # displays game over screen
                    image_x = (constants.SCREEN_WIDTH - gameover_image.get_width()) // 2
                    image_y = (constants.SCREEN_HEIGHT - gameover_image.get_height()) // 2
                    screen.blit(gameover_image, (image_x, image_y))

                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        level = 1
                        world_data = reset_level()
                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        world.process_data(world_data, tile_list, all_items, mob_animations)
                        temp_score = player.money
                        player = world.player
                        player.money = temp_score
                        enemy_list = world.all_enemies
                        score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_frames, True)
                        item_group.add(score_coin)
                        # add the items from the level data
                        for item in world.all_items:
                            item_group.add(item)
    
                # delete temp_hp = player.health and player.health = temp_hp
    
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
            if event.key == pygame.K_ESCAPE:
                pause_game = True

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
