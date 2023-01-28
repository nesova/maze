import pygame
import sys

FPS = 50
size = (width, height) = (500, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

tile_size = (tile_width, tile_height) = (100, 100)
player_image = pygame.transform.scale(pygame.image.load(f'images/player.png'), tile_size)
tile_images = {
    'wall': pygame.transform.scale(pygame.image.load(f'images/wall.png'), tile_size),
    'empty': pygame.transform.scale(pygame.image.load(f'images/ground.png'), tile_size)
}
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move_up(self):
        self.rect = self.rect.move(0, -tile_height)

    def move_down(self):
        self.rect = self.rect.move(0, +tile_height)

    def move_right(self):
        self.rect = self.rect.move(+tile_width, 0)

    def move_left(self):
        self.rect = self.rect.move(-tile_width, 0)


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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_LEFT:
                    player.move_left()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    start_screen()
    player, level_x, level_y = generate_level(load_level('map_1.txt'))
    level_1()
