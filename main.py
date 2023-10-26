
import pygame
import constants
from character import Character
from weapon import Weapon

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

# helper function for image scaling
def scale_image(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))


# loads all weapons
pistol_img = pygame.image.load("assets/images/weapons/pistol.png").convert_alpha()
pistol_image = scale_image(pistol_img, constants.WEAPON_SCALE)

# loads ammo projectile
projectile_img = pygame.image.load("assets/images/weapons/blue_lightsaber.png").convert_alpha()
projectile_image = scale_image(projectile_img, constants.WEAPON_SCALE)

# loads all mob entities
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
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




# creates our hero!
player = Character(100, 100, mob_animations, 0)
# creates our hero's weapon
pistol = Weapon(pistol_image, projectile_image)
# creates sprite group for projectiles
projectile_group = pygame.sprite.Group()


# keeps window open till user closes it
run = True
while run:

  # sets frame rate
  clock.tick(constants.FPS)
  # sets screen background - find a way to make it a map
  screen.fill(constants.BACKGROUND)

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

  # updates player animated state
  player.update()
  projectile = pistol.update(player)
  if projectile:
    projectile_group.add(projectile)
  for projectile in projectile_group:
    projectile.update()

  # displays the player (Jason!) and weapon
  player.draw(screen)
  pistol.draw(screen)
  for projectile in projectile_group:
    projectile.draw(screen)

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
