#creating a playable version of the popular game tetris
import pygame
import random

color = [
    (102, 153, 255),
    (204, 102, 255),
    (102, 255, 204),
    (255, 255, 153),
    (255, 102, 153),
    (0, 204, 153),
    (102, 0, 255),
    (204, 0, 102)
]

class Fig:
#creating an array of all possible filled shapes in a 4 x 4 matrix and their possible rotations

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]]
    ]
#randomly pick a type of tetris block and assign a random color
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.colors = random.randint(1, len(color) - 1)
        self.rotation = 0

#get the current rotation and also rotate
    def rotation(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    def image(self):
        return self.figures[self.type][self.rotation]

class Tetris:
    x = 100
    y = 60
    figure = None
    zoom = 20
    level = 2
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.score = 0
        self.state = "start"
        self.field = []
        for i in range(height):
            arr = []
            for j in range(width):
                arr.append(0)
            self.field.append(arr)
    
    def insert_figure(self):
        self.figure = Fig(3,0)
    
    def check_intersect(self):
        intersect = False
        for i in range(4):
             for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                                intersect = True
        return intersect
    
    def break_fig(self):
        line = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += line ** 2

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.colors
        self.break_fig()
        self.insert_figure()
        if self.check_intersect():
            self.state = "gameover"

    def gspace(self):
        while not self.check_intersect():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def down(self):
        self.figure.y += 1
        if self.check_intersect():
            self.figure.y -= 1
            self.freeze()

    def side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.check_intersect():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotation()
        if self.check_intersect():
            self.figure.rotation = old_rotation

pygame.init()

GREEN = (0, 51, 0)
NAVY = (0, 0, 102)
GREYBLUE = (102, 153, 153)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('BEST Tetris Game')

done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.insert_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.side(-1)
            if event.key == pygame.K_RIGHT:
                game.side(1)
            if event.key == pygame.K_SPACE:
                game.gspace()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(GREYBLUE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, NAVY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, color[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, color[game.figure.colors],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, GREEN)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()