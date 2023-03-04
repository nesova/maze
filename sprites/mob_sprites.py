from data import *


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ghost_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(f'images/ghost.png'), tile_size)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.dx = 1
        self.affected_area = 500
        self.dist = self.affected_area

    def update(self):
        if self.dist < 0:
            self.dist = self.affected_area
            self.dx *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.rect.move(2 * self.dx, 0)
        self.dist -= 2


class Bat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bat_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(f'images/bat.png'), tile_size)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.dy = 1
        self.affected_area = 1000
        self.dist = self.affected_area

    def update(self):
        if self.dist < 0:
            self.dist = self.affected_area
            self.dy *= -1
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.rect.move(0, 4 * self.dy)
        self.dist -= 4
