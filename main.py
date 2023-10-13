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



  pygame.display.update()

# quits pygame
pygame.quit()
