import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[1][1] = 1
        self.left = 100
        self.top = 400
        self.cell_size = 50
        self.l = self.cell_size * (5 ** 0.5)
        self.xrc, self.yrc = self.left + 2 * self.cell_size, self.top

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, tile, char, bg):
        rect = bg.get_rect()
        screen.blit(bg, rect)
        for y in range(self.height):
            for x in range(self.width):
                cx = self.left + 2 * self.cell_size * (x + y)
                cy = self.top + self.cell_size * (x - y)
                tile = pygame.transform.scale(tile, (200 + 5, 100 + 5))
                rect = tile.get_rect()
                w, h = rect[2], rect[3]
                screen.blit(tile, (cx - w / 2, cy - h / 2, w, h))
                # pygame.draw.circle(screen, (0, 0, 0), (cx, cy), 3, 0)
                # pygame.draw.line(screen, (0, 0, 0), (cx - 2 * self.cell_size, cy), (cx, cy - self.cell_size))
                # pygame.draw.line(screen, (0, 0, 0), (cx, cy + self.cell_size), (cx + 2 * self.cell_size, cy))
                # pygame.draw.line(screen, (0, 0, 0), (cx - 2 * self.cell_size, cy), (cx, cy + self.cell_size))
                # pygame.draw.line(screen, (0, 0, 0), (cx, cy - self.cell_size), (cx + 2 * self.cell_size, cy))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    char = pygame.transform.scale(char, (96, 112))
                    rect = char.get_rect()
                    w, h = rect[2], rect[3]
                    cx = self.left + 2 * self.cell_size * (x + y)
                    cy = self.top + self.cell_size * (x - y)
                    screen.blit(char, (cx - 1.2 * w / 2, cy - 1.6 * h / 2, w, h))
                    # pygame.draw.rect(screen, (0, 255, 0), (cx - 15, cy - 50, 30, 60))

    def on_board(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_cell(self, mouse_pos):
        x1, y1 = mouse_pos
        x_ots, y_ots = self.left - 2 * self.cell_size, self.top
        x2 = y1 - ((-0.5) * x1 + y_ots)

        y2 = 0.5 * x2 + y_ots
        rox = ((x2 - x_ots) ** 2 + (y2 - y_ots) ** 2) ** 0.5
        xr = rox / self.l

        x2 = y_ots - (y1 - (0.5 * x1 + y_ots) + y_ots)
        y2 = (-0.5) * x2 + y_ots

        roy = ((x2 - x_ots) ** 2 + (y2 - y_ots) ** 2) ** 0.5
        yr = roy / self.l

        xrcm = self.xrc + 2 * self.cell_size * (xr + yr)
        yrcm = self.yrc + self.cell_size * (xr - yr)

        lrm = xrcm - 2 * self.cell_size + 1
        trm = yrcm - self.cell_size + 1
        return int(xr), int(yr)

    def get_click(self, mouse_pos):
        self.on_click(*self.get_cell(mouse_pos))

    def on_click(self, x, y):
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
    board = Board(8, 8)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((255, 255, 255))
        board.render(screen, tile, char, bg)
        pygame.display.flip()
    pygame.quit()
