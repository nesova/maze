import pygame

MAP = [
    '#######@###',
    '#         #',
    '# ### #####',
    '# # #     #',
    '# # # ### #',
    '#K# # #K# #',
    '### # # # #',
    '#   # #   #',
    '# # # # # #',
    '# #   # #K#',
    '#X#########',
]

BLOCK_SIDE = 50
CELL_SIDE = 50
WIDTH = len(MAP[0])
HEIGHT = len(MAP)
SCREEN_WIDTH = WIDTH * BLOCK_SIDE
SCREEN_HEIGHT = HEIGHT * BLOCK_SIDE


class Wall:
    def __init__(self):
        self.pos = []
        self.texture = pygame.image.load(f'images/wall.png')

    def get_coord(self, x, y):
        self.pos.append((x, y))

    def draw(self):
        for pos in self.pos:
            screen.blit(self.texture, pos)


class Maze:
    def __init__(self):
        self.wall = Wall()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if MAP[i][j] == '#':
                    self.wall.get_coord(j * BLOCK_SIDE, i * BLOCK_SIDE)

    def draw(self):
        self.wall.draw()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont('arial', 60)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        maze = Maze()
        maze.draw()
        pygame.display.flip()
    pygame.quit()