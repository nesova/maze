import sys
import random
from data import *
from sprites.mob_sprites import Ghost, Bat
from sprites.block_sprites import Exit, Poison, Web
from sprites.player_sprite import Player
from sprites.collecting_sprites import Particle, Key, Coins


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
            elif level[y][x] == "W":
                Web(x, y)
            elif level[y][x] == 'G':
                Ghost(x, y)
                Poison(x, y)
            elif level[y][x] == 'B':
                Bat(x, y)
                Poison(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


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


def start_screen():  # начальное окно
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


def final_window(message):  # окно проигрыша или выигрыша
    screen.fill((0, 0, 0))
    text(message, 40, width // 2, height // 2)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()


def second_lvl(lvl_coins=0):  # окно между уровнями
    background = pygame.transform.scale(pygame.image.load(f'images/lvl up {lvl_coins} coins.png'), size)
    screen.blit(background, (0, 0))
    text("LEVEL UP", 80, width // 2, height // 7 * 2)
    text("  Нажмите, чтобы продолжить", 30, width // 5 * 2, height // 7 * 5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def secret_lvl_window():  # окно перед секретным уровнем
    screen.fill((0, 0, 0))
    text("Секретный уровень", 40, width // 2, height // 7 * 2)
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


def level():  # окно загрузки уровня
    global lvl_coins
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

        if pygame.sprite.groupcollide(player_group, web_group, False, False, ratio) != {}:
            player.is_web = True
        else:
            player.is_web = False

        if pygame.sprite.groupcollide(player_group, coins_group, False, True, ratio) != {}:
            lvl_coins += 1
            collect_c.play()

        if pygame.sprite.groupcollide(player_group, exit_group, False, False, ratio) != {}:
            if str(key_group) == "<Group(0 sprites)>":
                open_door.play()
                pygame.mixer.music.pause()
                for _ in range(3):
                    exit_group.update()
                    exit_group.draw(screen)
                    pygame.display.flip()
                    pygame.time.wait(300)
                pygame.mixer.music.unpause()
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
        web_group.draw(screen)
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
    open_door = pygame.mixer.Sound('sounds/open door.wav')
    start_screen()
    for i in range(1, 6):
        lvl_coins = 0
        poison_group.empty()
        exit_group.empty()
        key_group.empty()
        player_group.empty()
        stars_group.empty()
        coins_group.empty()
        ghost_group.empty()
        bat_group.empty()
        web_group.empty()
        if collected_coins == 12 and i == 5:
            i = 'secret'
            secret_lvl_window()
        elif i == 5:
            final_window("Вы успешно выбрались!")
        level_map = load_level(f"map_{i}.txt")
        player, level_x, level_y = generate_level(load_level(f"map_{i}.txt"))
        level()
        second_lvl(lvl_coins)
        collected_coins += lvl_coins
    final_window("Вы успешно выбрались!")
