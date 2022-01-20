import sqlite3
from random import choice, randrange
import pygame
from subprocess import call


class Cell:
    def __init__(self, num, type, x1, y1, can_go_to, x2, y2, act):
        self.num = num
        self.type = type
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.can_go_to = can_go_to.copy()
        self.act = act


class Board:
    def __init__(self):
        pass

    def render(self, screen):
        screen.blit(b, (0 + x, 0 + y))
        if curent_cell != 0:
            screen.blit(string, (curent_cell.x1, curent_cell.y1 + y - 50))


def update_allies():
    f = open('data/allies.txt', 'w')
    f.write(' '.join(allies))
    f.close()


def is_in_cell(xt, yt):
    for cell in cells:
        if cell.x1 < xt < cell.x2 and cell.y1 < yt < cell.y2:
            return cell.num
    return None


if __name__ == '__main__':
    f = open('data/is_lose.txt', 'w')
    f.write('')
    f.close()

    f = open('data/money.txt', 'w')
    f.write('0')
    f.close()
    pygame.init()
    pygame.display.set_caption('Координаты клетки')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    fps = 60
    clock = pygame.time.Clock()
    h, w = pygame.display.Info().current_h, pygame.display.Info().current_w
    font = pygame.font.Font(None, 22)

    b = pygame.image.load('data/mboard.png')
    bg = pygame.image.load('data/bg.png')
    string = pygame.image.load('data/string.png').convert_alpha()
    running = True
    board = Board()

    con = sqlite3.connect("data/game.db")
    cur = con.cursor()

    cells = []

    f = open('data/chars.txt')
    all_chars = f.read().split()
    f.close()

    allies = []
    for i in range(3):
        allies += [choice(all_chars)]
    f = open('data/allies.txt', 'w')
    f.write(' '.join(allies))
    f.close()

    for i in range(1, 16):
        num, type, x1, y1, can_go_to, x2, y2, act = cur.execute(f"""SELECT * FROM board
            WHERE cell_num = '{i}'""").fetchall()[0]
        cell = Cell(num, type, x1, y1, list(map(int, can_go_to.split())), x2, y2, act)
        cells += [cell]

    curent_cell = 0
    timer = 0
    f = open('data/fool.txt', 'w')
    f.write('')
    f.close()

    running = True
    moving = False
    last = (0, 0)
    m_x, m_y = 0, 0

    f = open('data/shop_chars.txt')
    shop_chars = f.read().split()
    f.close()
    x, y = 0, -490
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                act = event.button
                if act == 4:
                    if y < -20:
                        y += 20
                elif act == 5:
                    if y > -490:
                        y -= 20
                elif act == 1:
                    xt, yt = event.pos
                    yt -= y
                    print(xt, yt)
                    print(is_in_cell(xt, yt))
                    cur_cell = None
                    a = is_in_cell(xt, yt)
                    for i in cells:
                        if i.num == a:
                            cur_cell = i
                    if cur_cell:
                        if timer > 10:
                            if curent_cell == 0:
                                if cur_cell.num == 1:
                                    print(cur_cell.x2 - cur_cell.x1, cur_cell.y2 - cur_cell.y1)
                                    f = open('data/cell_type.txt', 'w')
                                    f.write(cur_cell.type)
                                    f.close()
                                    enemies = []
                                    for i in range(randrange(1, 5)):
                                        enemies += [choice(all_chars)]
                                    f = open('data/enemies.txt', 'w')
                                    f.write(' '.join(enemies))
                                    f.close()
                                    call(["python", "nice_board.py"])
                                    curent_cell = cur_cell
                            elif cur_cell.act == 'b' and cur_cell.num in curent_cell.can_go_to:
                                f = open('data/cell_type.txt', 'w')
                                f.write(cur_cell.type)
                                f.close()
                                curent_cell = cur_cell
                                enemies = []
                                for i in range(randrange(1, 5)):
                                    enemies += [choice(all_chars)]
                                f = open('data/enemies.txt', 'w')
                                f.write(' '.join(enemies))
                                f.close()
                                call(["python", "nice_board.py"])
                            elif cur_cell.act == 's' and cur_cell.num in curent_cell.can_go_to:
                                curent_cell = cur_cell
                                call(["python", "shop.py"])
                            elif cur_cell.act == 'r' and cur_cell.num in curent_cell.can_go_to:
                                curent_cell = cur_cell
                                f = open('data/allies.txt')
                                tallies = f.read().split()
                                f.close()

                                tallies += [choice(all_chars)]

                                f = open('data/allies.txt', 'w')
                                f.write(' '.join(tallies))
                                f.close()
                            elif cur_cell.act == 'w' and cur_cell.num in curent_cell.can_go_to:
                                f = open('data/is_lose.txt', 'w')
                                f.write('n')
                                f.close()
                                curent_cell = cur_cell
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        f = open('data/is_lose.txt')
        is_lose = f.read()
        f.close()

        if is_lose:
            running = False
            if timer > 10:
                call(["python", "end.py"])
                timer = 0

        screen.blit(bg, (0, 0))
        board.render(screen)
        timer += 1
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

