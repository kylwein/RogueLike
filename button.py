import pygame

class Button():
  def__init__(self,x,y,image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x,y)

def draw(self,surface):
  surface.blit(self.image, self.rect)

  
  
