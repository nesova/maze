import pygame
import sys

FPS = 50
size = (width, height) = (500, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

tile_size = (tile_width, tile_height) = (100, 100)
key_image = pygame.transform.scale(pygame.image.load(f'images/key.png'), tile_size)
tile_images = {
    'wall': pygame.transform.scale(pygame.image.load(f'images/wall.png'), tile_size),
    'empty': pygame.transform.scale(pygame.image.load(f'images/ground.png'), tile_size)
}

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'K':
                Key(x, y)
            elif level[y][x] == "X":
                Exit(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
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


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(key_group, all_sprites)
        self.image = key_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


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


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def start_screen():
    intro_text = ["MAZE", "",
                  "Нажмите на экран, чтобы начать"]

    background = pygame.transform.scale(pygame.image.load(f'images/background.png'), size)
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def level_1():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        ratio = pygame.sprite.collide_rect_ratio(0.5)
        pygame.sprite.groupcollide(player_group, key_group, False, True, ratio)
        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill((0, 0, 0))
        exit_group.draw(screen)
        tiles_group.draw(screen)
        key_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    start_screen()
    player, level_x, level_y = generate_level(load_level('map_1.txt'))
    level_1()
