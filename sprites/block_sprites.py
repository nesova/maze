from data import *


class Poison(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(poison_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(f'images/poison.png'), tile_size)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group, all_sprites)
        self.frames = []
        self.door_im = pygame.transform.scale(pygame.image.load(f'images/door.png'), (tile_width * 4, tile_height))
        self.cut_sheet(self.door_im, 4, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.open = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Web(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(web_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(f'images/web.png'), tile_size)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
