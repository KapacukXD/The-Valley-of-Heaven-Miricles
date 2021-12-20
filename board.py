import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[1][1] = 1
        self.left = 70
        self.top = 250
        self.cell_size = 30
        self.l = self.cell_size * (5 ** 0.5)
        self.xrc, self.yrc = self.left + 2 * self.cell_size, self.top

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cx = self.left + 2 * self.cell_size * (x + y)
                cy = self.top + self.cell_size * (x - y)
                pygame.draw.circle(screen, (0, 0, 0), (cx, cy), 3, 0)
                pygame.draw.line(screen, (0, 0, 0), (cx - 2 * self.cell_size, cy), (cx, cy - self.cell_size))
                pygame.draw.line(screen, (0, 0, 0), (cx, cy + self.cell_size), (cx + 2 * self.cell_size, cy))
                pygame.draw.line(screen, (0, 0, 0), (cx - 2 * self.cell_size, cy), (cx, cy + self.cell_size))
                pygame.draw.line(screen, (0, 0, 0), (cx, cy - self.cell_size), (cx + 2 * self.cell_size, cy))
        for y in range(self.height):
            for x in range(self.width):
                cx = self.left + 2 * self.cell_size * (x + y)
                cy = self.top + self.cell_size * (x - y)
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), (cx - 15, cy - 50, 30, 60))

    def on_board(self, mouse_pos):
        if (0 < mouse_pos[0] - self.left < self.width * self.cell_size
                and 0 < mouse_pos[1] - self.top < self.height * self.cell_size):
            return True
        return False

    def get_cell(self, mouse_pos):
        x1, y1 = mouse_pos
        x2 = y1 - ((-0.5) * x1 + self.top)
        print(x2)
        y2 = 0.5 * x2 + self.top
        rox = ((x2 - self.left) ** 2 + (y2 - self.top) ** 2) ** 0.5
        xr = rox / self.l

        x2 = self.top - (y1 - (0.5 * x1 + self.top) + self.top)
        y2 = (-0.5) * x2 + self.top

        roy = ((x2 - self.left) ** 2 + (y2 - self.top) ** 2) ** 0.5
        yr = roy / self.l

        xrcm = self.xrc + 2 * self.cell_size * (xr + yr)
        yrcm = self.yrc + self.cell_size * (xr - yr)

        lrm = xrcm - 2 * self.cell_size + 1
        trm = yrcm - self.cell_size + 1
        return int(xr), int(yr)

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)


if __name__ == '__main__':
    pygame.init()
    width, height = 800, 500
    size = width, height
    pygame.display.set_caption('Координаты клетки')
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    board = Board(5, 7)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(board.get_click(event.pos))
        screen.fill((255, 255, 255))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()