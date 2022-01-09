import pygame
from collections import deque
from random import randrange
import sqlite3

f = open('data/field.txt')
rows = f.read().split()
f.close()
field = []
for row in rows:
    field += [list(row)]
all_sprites = pygame.sprite.Group()


def path(s, t):
    n = len(field)
    m = len(field[0])
    delta = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    inf = 1000000000000
    d = [[inf] * m for _ in range(n)]
    p = [[None] * m for _ in range(n)]
    used = [[False] * m for _ in range(n)]
    queue = deque()
    d[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    queue.append(s)
    while len(queue) != 0:
        fx, fy = queue.popleft()
        for dx, dy in delta:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < n and 0 <= ny < m and not used[nx][ny] and field[nx][ny] != '#' and field[nx][ny] != 'c':
                d[nx][ny] = d[fx][fy] + 1
                p[nx][ny] = (fx, fy)
                used[nx][ny] = True
                queue.append((nx, ny))
    cur = t
    short_path = []
    while cur is not None:
        short_path.append(list(reversed(cur)))
        cur = p[cur[0]][cur[1]]
    short_path.reverse()
    return short_path[1:]


def bfs_lite(s, t):
    n = len(field)
    m = len(field[0])
    delta = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    inf = 1000000000000
    d = [[inf] * m for _ in range(n)]
    p = [[None] * m for _ in range(n)]
    used = [[False] * m for _ in range(n)]
    queue = deque()
    d[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    queue.append(s)
    while len(queue) != 0:
        fx, fy = queue.popleft()
        for dx, dy in delta:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < n and 0 <= ny < m and not used[nx][ny] and field[nx][ny] != '#':
                d[nx][ny] = d[fx][fy] + 1
                p[nx][ny] = (fx, fy)
                used[nx][ny] = True
                queue.append((nx, ny))
    return d[t[0]][t[1]]


def bfs(s, t):
    n = len(field)
    m = len(field[0])
    delta = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    inf = 1000000000000
    d = [[inf] * m for _ in range(n)]
    p = [[None] * m for _ in range(n)]
    used = [[False] * m for _ in range(n)]
    queue = deque()
    d[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    queue.append(s)
    while len(queue) != 0:
        fx, fy = queue.popleft()
        for dx, dy in delta:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < n and 0 <= ny < m and not used[nx][ny] and field[nx][ny] != '#' and field[nx][ny] != 'c':
                d[nx][ny] = d[fx][fy] + 1
                p[nx][ny] = (fx, fy)
                used[nx][ny] = True
                queue.append((nx, ny))
    return d[t[0]][t[1]]


class Char:
    def __init__(self, image, is_ally, hp, attack, attack_range, step, speed, char_h):
        self.is_ally = is_ally
        if not is_ally:
            self.drop = randrange(1, 5)
        else:
            self.drop = 0
        self.image = image
        self.rect = image.get_rect()
        self.max_hp = hp
        self.cur_hp = hp
        self.attack = attack
        self.range = attack_range
        self.step = step
        self.speed = speed
        self.h = char_h
        self.x = None
        self.y = None

    def do_attack(self, another):
        another.cur_hp -= self.attack


class Cell:
    def __init__(self, cell_x, cell_y, what_object, cell_type):
        self.x = cell_x
        self.y = cell_y
        # self.tile_image = types[cell_type]
        # self.rect = self.tile_image.get_rect()
        self.object = what_object
        if what_object == '#':
            self.tile_image = bush
        else:
            self.tile_image = ground
        self.ground = ground
        self.rect = self.tile_image.get_rect()
        self.is_char_on = False
        self.char = None
        self.ghost_wall = False
        self.type = cell_type

    def place_char(self, character):
        self.is_char_on = True
        character.x = self.x
        character.y = self.y
        self.char = character
        field[self.y][self.x] = 'c'

    def replace_char(self):
        field[self.y][self.x] = '.'
        self.is_char_on = False
        self.char = None

    def die(self):
        self.replace_char()

    def render(self, board_screen, cell_size, left, top, who, can_move, queue):
        cur_char = queue[who]
        if can_move:
            mark_range = cur_char.step
        else:
            mark_range = cur_char.range
        s = cell_size / 2
        cx = (self.y * s) - (self.x * s) + left
        cy = (self.y * s * 0.5) + (self.x * s * 0.5) + top + 0.5 * self.rect[3]
        board_screen.blit(self.ground, (cx - 0.5 * self.rect[2], cy - self.rect[3]))
        board_screen.blit(self.tile_image, (cx - 0.5 * self.rect[2], cy - self.rect[3]))
        if bfs((cur_char.y, cur_char.x), (self.y, self.x)) <= mark_range and not self.is_char_on:
            board_screen.blit(ground_mark, (cx - 0.5 * self.rect[2], cy - self.rect[3]))
        if not can_move and self.is_char_on and self.char != cur_char and \
                bfs_lite((cur_char.y, cur_char.x), (self.y, self.x)) <= mark_range:
            board_screen.blit(ground_mark, (cx - 0.5 * self.rect[2], cy - self.rect[3]))
        if self.is_char_on:
            tw, th = self.char.rect[2], self.char.rect[3]
            h_new = self.char.h
            tw, th = tw * h_new / th, h_new
            char_in_scale = pygame.transform.scale(self.char.image, (tw, th))
            rect = char_in_scale.get_rect()
            tw, th = rect[2], rect[3]
            s = cell_size / 2
            cxc = (self.y * s) - (self.x * s) + left
            cyc = (self.y * s * 0.5) + (self.x * s * 0.5) + top + 0.5 * rect[3]
            screen.blit(char_in_scale, (cxc - 0.5 * tw, cyc - th))
        if self.ghost_wall:
            if self.is_char_on:
                if self.char.is_ally:
                    board_screen.blit(ally_char_show, (cx - 0.5 * self.rect[2], cy - self.rect[3]))
                else:
                    board_screen.blit(enemy_char_show, (cx - 0.5 * self.rect[2], cy - self.rect[3]))
            else:
                board_screen.blit(ghost_wall, (cx - 0.5 * self.rect[2], cy - self.rect[3]))

    def show_ghost_wall(self, board_screen, cell_size, left, top):
        s = cell_size / 2
        cx = (self.y * s) - (self.x * s) + left
        cy = (self.y * s * 0.5) + (self.x * s * 0.5) + top + 0.5 * self.rect[3]
        board_screen.blit(ghost_wall, (cx - 0.5 * self.rect[2], cy - self.rect[3]))


class Board:
    def __init__(self, cell_size, board_field, left, top, tile_type):
        self.can_move = True
        self.can_attack = False
        self.move_list = []
        self.is_last_move = False
        self.wait = 60
        self.who = 0
        self.queue = sorted(chars, key=lambda sx: sx.speed)
        self.width = len(board_field[0])
        self.height = len(board_field)
        self.board = [[Cell(cell_x, cell_y, board_field[cell_y][cell_x], tile_type)
                       for cell_x in range(self.width)] for cell_y in range(self.height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.chosen_char = None
        self.xrc, self.yrc = self.left + 2 * self.cell_size, self.top
        for t_char in self.queue:
            a, b = randrange(0, len(field)), randrange(0, len(field[0]))
            if t_char.is_ally:
                need_cell = 't'
            else:
                need_cell = 'e'
            while field[a][b] != need_cell:
                a, b = randrange(0, len(field)), randrange(0, len(field[0]))
            self.board[a][b].place_char(t_char)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, cur_screen, bg_image):
        self.wait += 1
        self.try_to_move()
        rect = bg_image.get_rect()
        screen.blit(bg_image, rect)
        for cell_x in range(self.height):
            for cell_y in range(self.width):
                self.board[cell_x][cell_y].render(cur_screen, self.cell_size,
                                                  self.left, self.top, self.who, self.can_move, self.queue)
        if self.chosen_char:
            cur_char = self.chosen_char
        else:
            cur_char = self.queue[self.who]
        h_new = cur_char.h
        hp = font.render(f'{cur_char.cur_hp}/{cur_char.max_hp}', True, (255, 100, 100))
        hp_len = cur_char.cur_hp / cur_char.max_hp
        tw, th = cur_char.rect[2], cur_char.rect[3]
        tw, th = tw * h_new / th, h_new
        pygame.draw.rect(cur_screen, (0, 0, 0), (106, 0, 233, 30), 0)
        pygame.draw.rect(cur_screen, (0, 0, 0), (90, 30, 249, 25), 0)
        pygame.draw.rect(cur_screen, (200, 0, 0), (106, 0, int(233 * hp_len), 30), 0)
        screen.blit(hp, (205, 10))
        pygame.draw.rect(cur_screen, (0, 0, 200), (90, 30, 249, 25), 0)
        menu_image = pygame.transform.scale(cur_char.image, (tw, th))
        cur_screen.blit(menu1, (0, 0))
        cur_screen.blit(menu_image, (1, 100 - th))

        cur_screen.blit(menu3, (0, 0))

    def on_board(self, cell_x, cell_y):
        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return True
        return False

    def get_cell(self, mouse_pos):
        x1, y1 = mouse_pos
        cell_x = x1 - self.left
        cell_y = y1 - self.top
        sw, sh = self.cell_size, self.cell_size * 0.5
        mouse_grid_x = (cell_y / sh) + (cell_x / sw)
        mouse_grid_y = (-cell_x / sw) + (cell_y / sh)
        return int(mouse_grid_y), int(mouse_grid_x)

    def get_click(self, mouse_pos):
        self.on_click(*self.get_cell(mouse_pos))

    def on_click(self, cell_x, cell_y):
        if self.can_move:
            if len(self.move_list) == 0 and not self.is_last_move:
                cur_char = self.queue[self.who]
                if self.on_board(cell_x, cell_y):
                    if bfs((cur_char.y, cur_char.x), (cell_y, cell_x)) == 0:
                        self.can_move = False
                        self.can_attack = True
                    elif not self.board[cell_y][cell_x].is_char_on:
                        if bfs((cur_char.y, cur_char.x), (cell_y, cell_x)) <= cur_char.step:
                            self.move_list = path((cur_char.y, cur_char.x), (cell_y, cell_x))
        elif self.can_attack:
            cur_char = self.queue[self.who]
            if self.on_board(cell_x, cell_y):
                if bfs((cur_char.y, cur_char.x), (cell_y, cell_x)) == 0:
                    self.can_move = True
                    self.can_attack = False
                    self.change_turn()
                elif bfs_lite((cur_char.y, cur_char.x), (cell_y, cell_x)) <= cur_char.range:
                    if self.board[cell_y][cell_x].is_char_on:
                        another = self.board[cell_y][cell_x].char
                        if cur_char.is_ally != another.is_ally:
                            cur_char.do_attack(another)
                            if another.cur_hp <= 0:
                                self.board[another.y][another.x].die()
                            self.can_move = True
                            self.can_attack = False
                            self.change_turn()
        win_ch = self.is_sm_win()
        if win_ch:
            if win_ch == 'a':
                stop('ally')
            else:
                stop('enemy')

    def try_to_move(self):
        if self.move_list:
            self.is_last_move = True
            if self.wait >= 60:
                next_x, next_y = self.move_list.pop(0)
                cur_char = self.queue[self.who]
                self.move_to(cur_char.x, cur_char.y, next_x, next_y)
        else:
            if self.is_last_move:
                self.is_last_move = False
                self.can_move = False
                self.can_attack = True

    def move_to(self, from_x, from_y, to_x, to_y):
        if self.board[to_y][to_x].object != '#':
            self.board[to_y][to_x].place_char(self.board[from_y][from_x].char)
            self.board[from_y][from_x].replace_char()

    def change_turn(self):
        self.who += 1
        self.who %= len(self.queue)
        while self.queue[self.who].cur_hp <= 0:
            self.who += 1
            self.who %= len(self.queue)
        if not self.queue[self.who].is_ally:
            self.enemy_turn()

    def enemy_turn(self):
        pass

    def get_focus(self):
        pass

    def is_sm_win(self):
        any_allies, any_enemies = False, False
        for char in self.queue:
            if char.cur_hp > 0:
                if char.is_ally:
                    any_allies = True
                else:
                    any_enemies = True
        if any_allies and any_enemies:
            return None
        elif any_allies:
            return 'a'
        return 'e'

    def show_mouse_pos(self, mouse_pos):
        global last
        cell_x, cell_y = self.get_cell(mouse_pos)
        old_x, old_y = last
        self.board[old_y][old_x].ghost_wall = False
        if self.on_board(cell_x, cell_y) and self.board[cell_y][cell_x].object != '#':
            self.board[cell_y][cell_x].ghost_wall = True
            self.chosen_char = self.board[cell_y][cell_x].char
            last = (cell_x, cell_y)

    def set_pos(self, cell_x, cell_y):
        self.left = cell_x
        self.top = cell_y


con = sqlite3.connect("data/game.db")
cur = con.cursor()

if __name__ == '__main__':
    pygame.init()
    width, height = 1000, 800
    size = width, height
    pygame.display.set_caption('Координаты клетки')
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    fps = 60
    clock = pygame.time.Clock()
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    ghost_wall = pygame.image.load('data/marks/yellow_ghost_wall.png').convert_alpha()
    ghost_wall = pygame.transform.scale(ghost_wall, (128, 128))

    h, w = pygame.display.Info().current_h, pygame.display.Info().current_w

    font = pygame.font.Font(None, 18)

    x, y = int(w / 2), int(h / 2) - 200

    f = open('data/cell_type.txt')
    cells_type = f.read()
    f.close()

    bg = pygame.image.load('data/bg.png')
    ground = pygame.transform.scale(pygame.image.load(f'data/{cells_type}/ground.png').convert_alpha(), (128, 128))
    bush = pygame.transform.scale(pygame.image.load(f'data/{cells_type}/objects/bush.png').convert_alpha(), (128, 128))
    enemy_char_show = pygame.transform.scale(pygame.image.load('data/marks/red_ghost_wall.png').convert_alpha(), (128, 128))
    ally_char_show = pygame.transform.scale(pygame.image.load('data/marks/blue_ghost_wall.png').convert_alpha(), (128, 128))
    ground_mark = pygame.transform.scale(pygame.image.load('data/marks/ground_mark.png').convert_alpha(), (128, 128))
    menu1 = pygame.transform.scale(pygame.image.load('data/menu/1.png').convert_alpha(), (105, 100))
    menu3 = pygame.transform.scale(pygame.image.load('data/menu/3.png').convert_alpha(), (342, 123))

    f = open('data/allies.txt')
    allies = f.read().split()
    f.close()
    f = open('data/enemies.txt')
    enemies = f.read().split()
    f.close()

    chars = []
    for name in allies:
        image = pygame.image.load(f'data/charters/{name}.png').convert_alpha()
        is_ally = True
        _, _, hp, attack, attack_range, step, speed, char_h = cur.execute(f"""SELECT * FROM charters
            WHERE name = '{name}'""").fetchall()[0]
        charter = Char(image, is_ally, hp, attack, attack_range, step, speed, char_h)
        chars += [charter]
    for name in enemies:
        image = pygame.image.load(f'data/charters/{name}.png').convert_alpha()
        is_ally = False
        _, _, hp, attack, attack_range, step, speed, char_h = cur.execute(f"""SELECT * FROM charters
            WHERE name = '{name}'""").fetchall()[0]
        charter = Char(image, is_ally, hp, attack, attack_range, step, speed, char_h)
        chars += [charter]
    board = Board(128, field, x, y, cells_type)
    running = True
    moving = False
    last = (0, 0)
    m_x, m_y = 0, 0

    def stop(who_wins):
        global running
        running = False
        print(who_wins)

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
                    x -= (m_x_ch * 0.6)
                    y -= (m_y_ch * 0.6)
                    board.set_pos(int(x), int(y))
                    m_x, m_y = map(int, event.pos)
                else:
                    board.show_mouse_pos(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        all_sprites.update()
        screen.fill((255, 255, 255))
        board.render(screen, bg)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
