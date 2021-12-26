import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[1][1] = 1
        self.left = 435
        self.top = 400
        self.cell_size = 128
        self.l = self.cell_size * (5 ** 0.5)
        self.xrc, self.yrc = self.left + 2 * self.cell_size, self.top

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, char, bg):
        rect = bg.get_rect()
        screen.blit(bg, rect)
        for x in range(self.height):
            for y in range(self.width):
                tileImage = None
                if self.board[x][y] == 2:
                    #tileImage = wall
                    pass
                else:
                    tileImage = grass
                rect = tileImage.get_rect()
                s = self.cell_size / 2
                cx = (y * s) - (x * s) + self.left
                cy = (y * s * 0.5) + (x * s * 0.5) + self.top + 0.5 * rect[3]
                screen.blit(tileImage, (cx - 0.5 * rect[2], cy - rect[3]))
                pygame.draw.circle(screen, (0, 0, 0), (cx, cy), 3, 0)
                #pygame.draw.line(screen, (0, 0, 0), (cx - 2 * self.cell_size, cy), (cx, cy - self.cell_size))
                #pygame.draw.line(screen, (0, 0, 0), (cx, cy + self.cell_size), (cx + 2 * self.cell_size, cy))
                #pygame.draw.line(screen, (0, 0, 0), (cx - 2 * self.cell_size, cy), (cx, cy + self.cell_size))
                #pygame.draw.line(screen, (0, 0, 0), (cx, cy - self.cell_size), (cx + 2 * self.cell_size, cy))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    char = pygame.transform.scale(char, (48 * 1.5, 56 * 1.5))
                    rect = char.get_rect()
                    w, h = rect[2], rect[3]
                    s = self.cell_size / 2
                    cx = (y * s) - (x * s) + self.left
                    cy = (y * s * 0.5) + (x * s * 0.5) + self.top + 0.5 * rect[3]
                    screen.blit(char, (cx - 0.55 * w, cy - h))
                    # pygame.draw.rect(screen, (0, 255, 0), (cx - 15, cy - 50, 30, 60))

    def on_board(self, x, y):
        print(x, y)
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_cell(self, mouse_pos):
        x1, y1 = mouse_pos
        x = x1 - self.left
        y = y1 - self.top
        w, h = self.cell_size, self.cell_size * 0.5
        mouse_grid_x = (y / h) + (x / w)
        mouse_grid_y = (-x / w) + (y / h)
        print(int(mouse_grid_x), int(mouse_grid_y))
        return int(mouse_grid_y), int(mouse_grid_x)

    def get_click(self, mouse_pos):
        self.on_click(*self.get_cell(mouse_pos))

    def on_click(self, x, y):
        if self.on_board(x, y):
            if self.on_board(x, y - 1) and self.board[y - 1][x] == 1:
                self.board[y - 1][x] = 0
                self.board[y][x] = 1
            elif self.on_board(x, y + 1) and self.board[y + 1][x] == 1:
                self.board[y + 1][x] = 0
                self.board[y][x] = 1
            elif self.on_board(x - 1, y) and self.board[y][x - 1] == 1:
                self.board[y][x - 1] = 0
                self.board[y][x] = 1
            elif self.on_board(x + 1, y) and self.board[y][x + 1] == 1:
                self.board[y][x + 1] = 0
                self.board[y][x] = 1

    def set_pos(self, x, y):
        self.left = x
        self.top = y
        print(x, y)

if __name__ == '__main__':
    pygame.init()
    width, height = 1000, 800
    size = width, height
    pygame.display.set_caption('Координаты клетки')
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    char = pygame.image.load('char.png').convert_alpha()
    bg = pygame.image.load('blue_like_bg.png')
    # tile = pygame.image.load('tile50x25.png').convert_alpha()
    tile = pygame.image.load('green_tile50x25.png').convert_alpha()
    grass = pygame.image.load('grass.png').convert_alpha()
    grass = pygame.transform.scale(grass, (128, 128))
    board = Board(8, 8)
    running = True
    moving = False
    m_x, m_y = 0, 0
    x, y = 435, 400
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                act = event.button
                if act == 1:
                    board.get_click(event.pos)
                if act == 3:
                    moving = True
                    m_x, m_y = map(int, event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    m_x_ch, m_y_ch = m_x - int(event.pos[0]), m_y - int(event.pos[1])
                    x -= m_x_ch
                    y -= m_y_ch
                    board.set_pos(x, y)
                    m_x, m_y = map(int, event.pos)
        screen.fill((255, 255, 255))
        board.render(screen, char, bg)
        pygame.display.flip()
    pygame.quit()
