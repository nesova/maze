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


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.texture = pygame.image.load(f'images/player.png')
        self.step = CELL_SIDE
        self.direction = Direction.NONE

    def get_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.y -= self.step
        elif self.direction == 2:
            self.y += self.step
        elif self.direction == 3:
            self.x -= self.step
        elif self.direction == 4:
            self.x += self.step


class Exit:
    def __init__(self):
        self.open_key = 0
        self.pos = None
        self.door_textures = []
        self.state = "closed"
        for i in range(4):
            self.door_textures.append(pygame.image.load(f'images/image_door{i}.png'))

    def get_coord(self, x, y):
        self.pos = (x, y)

    def change_state(self):
        self.state = "opened"
        for i in range(1, 3):
            self.draw(i)

    def draw(self, texture_n):
        screen.blit(self.door_textures[texture_n], self.pos)


class Key:
    def __init__(self):
        self.keys = {}
        self.texture = pygame.image.load(f'images/key.png')

    def get_coord(self, x, y):
        self.keys[(x, y)] = "not taken"

    def update_to_is_taken(self, pos):
        self.keys[pos] = "is taken"

    def return_keys_coords(self):
        return list(self.keys.keys())

    def all_taken(self):
        if len(set(self.keys.values())) == 1:
            return True
        return False

    def draw(self):
        for key in self.keys:
            if self.keys[key] == "not taken":
                screen.blit(self.texture, key)


class Direction:
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Maze:
    def __init__(self):
        self.wall = Wall()
        self.player = Player()
        self.keys = Key()
        self.exit = Exit()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if MAP[i][j] == '#':
                    self.wall.get_coord(j * BLOCK_SIDE, i * BLOCK_SIDE)
                elif MAP[i][j] == "@":
                    self.player.get_pos(j * BLOCK_SIDE, i * BLOCK_SIDE)
                elif MAP[i][j] == 'X':
                    self.exit.get_coord(j * BLOCK_SIDE, i * BLOCK_SIDE)
                elif MAP[i][j] == 'K':
                    self.keys.get_coord(j * BLOCK_SIDE, i * BLOCK_SIDE)
        self.pos_walls = self.wall.pos
        self.pos_door = self.exit.pos

    def draw(self):
        self.wall.draw()
        self.player.draw()
        self.keys.draw()
        if self.exit.state == "closed":
            self.exit.draw(0)
        else:
            self.exit.draw(3)

    def win(self):
        if self.get_player_cell() == self.exit.pos and self.exit.state == "opened":
            return True

    def set_player_direction(self, direction):
        if self.player_can_move(direction):
            self.player.direction = direction
        else:
            self.player.direction = Direction.NONE

    def player_can_move(self, direction):
        pcx, pcy = self.get_player_cell()
        if direction == 1 and (pcx, pcy - CELL_SIDE) in self.pos_walls:
            return False
        if direction == 2:
            if (pcx, pcy + CELL_SIDE) in self.pos_walls:
                return False
            if (pcx, pcy + CELL_SIDE) == self.pos_door and self.exit.state == "closed":
                return False
        if direction == 3 and (pcx - CELL_SIDE, pcy) in self.pos_walls:
            return False
        if direction == 4 and (pcx + CELL_SIDE, pcy) in self.pos_walls:
            return False
        if direction == 0:
            return None
        return True

    def move_player(self):
        self.set_player_direction(self.player.direction)
        self.player.move()
        coord = self.get_player_cell()
        if coord in self.keys.return_keys_coords():
            self.keys.update_to_is_taken(coord)
            if self.keys.all_taken():
                self.exit.change_state()

    def get_player_cell(self):
        return (self.player.x, self.player.y)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    maze = Maze()
    font = pygame.font.SysFont('arial', 60)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    maze.set_player_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    maze.set_player_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    maze.set_player_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    maze.set_player_direction(Direction.RIGHT)
            elif event.type == pygame.KEYUP:
                maze.set_player_direction(Direction.NONE)
        maze.move_player()
        screen.fill((0, 0, 0))
        maze.draw()

        pygame.display.flip()
        pygame.time.wait(100)
pygame.quit()

