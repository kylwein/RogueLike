
import pygame
import constants
from character import Character


# initializes pygame
pygame.init()

# sets screen dimensions
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Jason Journey")

# creates our hero!
player = Character(100, 100)


# keeps window open while True
run = True
while run:

  # displays the player (Jason!)
  player.draw(screen)


  # event handler
  for event in pygame.event.get():

    # finishes loop when you close the game window
    if event.type == pygame.QUIT:
      run = False

    if event.type == pygame.KEYDOWN:
      # moves right
      if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        print("right")

      # moves left
      if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        print("left")

      # moves up
      if event.key == pygame.K_w or event.key == pygame.K_UP:
        print("up")

      # moves down
      if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        print("down")


  pygame.display.update()

# quits pygame
pygame.quit()
