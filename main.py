import pygame
import sys
import random


FPS = 50
size = (width, height) = (500, 500)
tile_size = (tile_width, tile_height) = (100, 100)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

collected_coins = 0


all_sprites = pygame.sprite.Group()
poison_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
bat_group = pygame.sprite.Group()

GRAVITY = 0.2
screen_rect = (0, 0, width, height)


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


def create_particles(position):
    particle_count = 40
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Poison(x, y)
            elif level[y][x] == 'K':
                Key(x, y)
            elif level[y][x] == "X":
                Exit(x, y)
            elif level[y][x] == "C":
                Coins(x, y)
            elif level[y][x] == 'G':
                Ghost(x, y)
                Poison(x, y)
            elif level[y][x] == 'B':
                Bat(x, y)
                Poison(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


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
        self.move_im = pygame.transform.scale(pygame.image.load(f'images/coins move.png'), (tile_width * 7, tile_height))
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


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def text(message, size, move_x, move_y):
    font = pygame.font.Font("data/font.ttf", size)
    text = font.render(message, True, pygame.Color('white'))
    textRect = text.get_rect()
    textRect.center = (move_x, move_y)
    screen.blit(text, textRect)


def start_screen():
    background = pygame.transform.scale(pygame.image.load(f'images/background.png'), size)
    screen.blit(background, (0, 0))
    text(" MAZE", 80, width // 5, height // 7 * 2)
    text("Нажмите, чтобы начать", 30, width // 5 * 2, height // 7 * 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def final_window(message):
    screen.fill((0, 0, 0))
    text(message, 40, width // 2, height // 2)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()


def secret_lvl_window():
    screen.fill((0, 0, 0))
    text("Секретный уровень",  40, width // 2, height // 7 * 2)
    text(" Ты собрал все монеты, так что ", 25, width // 5 * 2, height // 8 * 3)
    text("впереди тебя ждет еще одно подземелье", 25, width // 6 * 3, height // 9 * 4)
    text("Вперед, герой!!!", 25, width // 6 * 3, height // 10 * 5)
    text("Нажмите, чтобы начать", 30, width // 2, height // 7 * 5)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def level():
    global collected_coins
    camera = Camera()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        ratio = pygame.sprite.collide_rect_ratio(0.7)
        if pygame.sprite.groupcollide(player_group, ghost_group, False, False, ratio) != {}:
            pygame.mixer.music.stop()
            loss.play()
            final_window("Вас настигла смерть...")

        if pygame.sprite.groupcollide(player_group, bat_group, False, False, ratio) != {}:
            pygame.mixer.music.stop()
            loss.play()
            final_window("Вас настигла смерть...")

        if pygame.sprite.groupcollide(player_group, key_group, False, True, ratio) != {}:
            create_particles((player.rect.x, player.rect.y))
            collect_k.play()
        if pygame.sprite.groupcollide(player_group, poison_group, False, False, ratio) == {}:
            keys = pygame.key.get_pressed()
            player.update(keys)
        else:
            pygame.mixer.music.stop()
            loss.play()
            final_window("Вас настигла смерть...")

        if pygame.sprite.groupcollide(player_group, coins_group, False, True, ratio) != {}:
            collected_coins += 1
            collect_c.play()

        if pygame.sprite.groupcollide(player_group, exit_group, False, False, ratio) != {}:
            if str(key_group) == "<Group(0 sprites)>":
                for _ in range(3):
                    exit_group.update()
                    exit_group.draw(screen)
                    pygame.display.flip()
                    pygame.time.wait(300)
                return

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        ghost_group.update()
        stars_group.update()
        coins_group.update()
        bat_group.update()
        screen.fill((0, 0, 0))
        exit_group.draw(screen)
        poison_group.draw(screen)
        key_group.draw(screen)
        player_group.draw(screen)
        coins_group.draw(screen)
        stars_group.draw(screen)
        ghost_group.draw(screen)
        bat_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("sounds/background.mp3")
    pygame.mixer.music.play(-1)
    collect_c = pygame.mixer.Sound('sounds/pickupCoin.wav')
    collect_k = pygame.mixer.Sound('sounds/pickupKey.wav')
    loss = pygame.mixer.Sound('sounds/loss.wav')
    start_screen()
    for i in range(1, 6):
        poison_group.empty()
        exit_group.empty()
        key_group.empty()
        player_group.empty()
        stars_group.empty()
        coins_group.empty()
        ghost_group.empty()
        bat_group.empty()
        if collected_coins == 12 and i == 5:
            i = 'secret'
        elif i == 5:
            final_window("Вы успешно выбрались!")
        level_map = load_level(f"map_{i}.txt")
        player, level_x, level_y = generate_level(load_level(f"map_{i}.txt"))
        level()
    final_window("Вы успешно выбрались!")
