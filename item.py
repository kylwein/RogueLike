import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_types):
        pygame.sprite.Sprite.__init__(self)
        self.animations = animation_types
        self.item = item_type
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, player):
        #if item has been collected
        if self.rect.colliderect(player.rect):
            if self.item == 0:
                player.money += 1
            elif self.item == 1:
                player.health += 10
                if player.health > 100:
                    player.health == 100
            self.kill()
        #animate the item
        animation_cd = 100
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)