from data import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.move_im = pygame.transform.scale(pygame.image.load(f'images/player.png'), (tile_width * 4, tile_height))
        self.cut_sheet(self.move_im, 4, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.count = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.is_web = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def counter(self):
        if self.count == 10:
            self.count = 0
            return True
        self.count += 1
        return False

    def update(self, keys):
        speed = 2
        if keys[pygame.K_LSHIFT]:
            speed = 4
        if self.is_web:
            speed = 1
        if True in keys:
            if keys[pygame.K_LEFT]:
                self.rect = self.rect.move(-speed, 0)
            if keys[pygame.K_RIGHT]:
                self.rect = self.rect.move(speed, 0)
            if keys[pygame.K_UP]:
                self.rect = self.rect.move(0, -speed)
            if keys[pygame.K_DOWN]:
                self.rect = self.rect.move(0, speed)
            if self.counter():
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
