from data import *
import random


class Particle(pygame.sprite.Sprite):
    fire = [pygame.image.load(f'images/star.png')]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(key_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(f'images/key.png'), tile_size)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Coins(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coins_group, all_sprites)
        self.frames = []
        self.move_im = pygame.transform.scale(pygame.image.load(f'images/coins move.png'),
                                              (tile_width * 7, tile_height))
        self.cut_sheet(self.move_im, 7, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame += 0.2
        self.image = self.frames[int(self.cur_frame % 7)]
