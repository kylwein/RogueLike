from item import Item
import constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.wall_tiles = []
        self.ladder_tile = None

    def process_data(self, data, tile_list):
        self.level_length = len(data)

        # creates y and x counter in function definition
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # 7 represents wall
                if tile == 7:
                    self.wall_tiles.append(tile_data)
                # 8 represents exit
                elif tile == 8:
                    self.ladder_tile = tile_data
                #elif tile == 9:
                    #coin = Item(image_x, image_y, 0, )
                # adds the single tile to the map tiles list
                # no negative images so must be positive value
                if tile >= 0:
                    self.map_tiles.append(tile_data)


    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            # first argument is which tile, second argument is where to be drawn
            surface.blit(tile[0], tile[1])