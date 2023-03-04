import pygame

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
web_group = pygame.sprite.Group()

GRAVITY = 0.2
screen_rect = (0, 0, width, height)
