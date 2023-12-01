
import pygame
import constants
from character import Character
from weapon import Weapon
from item import Item

# initializes pygame
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


#define font!!
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# helper function for image scaling
def scale_image(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))

# loads heart
empty_heart = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
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

# loads all weapons
pistol_img = pygame.image.load("assets/images/weapons/pistol.png").convert_alpha()
pistol_image = scale_image(pistol_img, constants.WEAPON_SCALE)

# loads ammo projectile
projectile_img = pygame.image.load("assets/images/weapons/blue_lightsaber.png").convert_alpha()
projectile_image = scale_image(projectile_img, constants.WEAPON_SCALE)

# loads all mob entities
mob_animations = []
mob_types = ["jason", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
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

#draw text onto screen
def draw_text(text, font, color, x, y):
  image = font.render(text, True, color)
  screen.blit(image, (x, y))

#display game info
def game_info():
  #draw HUD
  pygame.draw.rect(screen, (constants.HUD_COLOR), (0, 0, constants.SCREEN_WIDTH, 50))

  #draw hearts
  has_half_heart = False
  for i in range(5):
    if player.health >= ((i + 1) * 20):
      screen.blit(full_heart, (10 + i * 50, 0))
    elif (player.health % 20 > 0) and has_half_heart == False:
      screen.blit(half_heart, (10 + i * 50, 0))
      has_half_heart = True
    else:
      screen.blit(empty_heart, (10 + i * 50, 0))

  #draw wallet ***change how money is displayed
  draw_text(f"Gold: {player.money}", font, constants.RED, constants.SCREEN_WIDTH - 500, 15)


def draw_grid():
  for x in range(30):
    pygame.draw.line(screen, constants.WHITE, (x * 40, 0), (x * 40, constants.SCREEN_HEIGHT))
    pygame.draw.line(screen, constants.WHITE, (0, x * 40), (constants.SCREEN_WIDTH, x * 40))



#damage class
class DamageText(pygame.sprite.Sprite):
  def __init__(self, x, y, damage, color):
    pygame.sprite.Sprite.__init__(self)
    self.image = font.render(damage, True, color)
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.counter = 0

  def update(self):
    #move damage text up
    self.rect.y -= 1
    # delete the counter after time
    self.counter += 1
    if self.counter >30:
      self.kill()


# creates our hero!
player = Character(100, 100, 100, mob_animations, 0)

# create our first monster
enemy = Character(200, 300, 100, mob_animations, 1) # imp character

#monster list
enemy_list = []
enemy_list.append(enemy)

# creates our hero's weapon
pistol = Weapon(pistol_image, projectile_image)
# creates sprite group for projectiles

damage_text_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_frames)

potion = Item(200, 200, 1, pwr_up)
item_group.add(potion)

coin = Item(400, 400, 0, coin_frames)
item_group.add(coin)

# creates an enemy
#enemy = Character(100, 100, mob_animations, 1)

# keeps window open till user closes it
run = True # GAME LOOP
while run:

  # sets frame rate
  clock.tick(constants.FPS)
  # sets screen background - find a way to make it a map
  screen.fill(constants.BACKGROUND)

  draw_grid()

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


  # moves player
  player.move(dx, dy)


# updates enemy animated state
  for enemy in enemy_list:
    enemy.update()

  # updates player animated state
  player.update()
  projectile = pistol.update(player)
  if projectile:
    projectile_group.add(projectile)
  for projectile in projectile_group:
    damage, damage_pos = projectile.update(enemy_list)
    if damage:
      damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
      damage_text_group.add(damage_text)
  damage_text_group.update()

  item_group.update(player)

  print(projectile_group)

  # displays the enemy
  for enemy in enemy_list:
    enemy.draw(screen)

  # displays the player (Jason!), weapon, and items
  player.draw(screen)
  pistol.draw(screen)
  for projectile in projectile_group:
    projectile.draw(screen)
  damage_text_group.draw(screen)
  item_group.draw(screen)

  # draws top part of screen with hp, etc
  game_info()

  # draws little coin on top right
  score_coin.draw(screen)



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
