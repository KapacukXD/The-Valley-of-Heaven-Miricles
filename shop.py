import sqlite3
from random import randrange, choice
import pygame


class Char:
    def __init__(self, name, image, is_ally, hp, attack, attack_range, step, speed, char_h):
        self.cost = randrange(5, 15)
        self.name = name
        self.is_ally = is_ally
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
        self.is_bought = False


class Shop:
    def __init__(self):
        pass

    def render(self, screen):
        screen.blit(board, (0, 0))
        for i in range(3):
            if i == 0:
                fc, sc = 250, 310
                ft, st = 250, 430
            elif i == 1:
                fc, sc = 650, 400
                ft, st = 655, 525
            else:
                fc, sc = 1080, 310
                ft, st = 1090, 440
            ft += 20
            st += 10
            char = chars[i]
            if not char.is_bought:
                tw, th = char.rect[2], char.rect[3]
                h_new = 120 * char.h / 100
                tw, th = tw * h_new / th, h_new
                char_in_scale = pygame.transform.scale(char.image, (tw, th))
                rect = char_in_scale.get_rect()
                tw, th = rect[2], rect[3]
                screen.blit(char_in_scale, (fc + 92 - tw * 0.5, sc))

                hp = font.render(f'{char.max_hp}', True, (0, 0, 0))
                screen.blit(hp, (ft + 20, st))
                screen.blit(hart, (ft, st))

                attack = font.render(f'{char.attack}', True, (0, 0, 0))
                screen.blit(attack, (ft + 120, st))
                screen.blit(sword, (ft + 100, st))

                at_range = font.render(f'{char.range}', True, (0, 0, 0))
                screen.blit(at_range, (ft + 20, st + 20))
                screen.blit(bow, (ft, st + 20))

                at_speed = font.render(f'{char.speed}', True, (0, 0, 0))
                screen.blit(at_speed, (ft + 120, st + 20))
                screen.blit(speed_sword, (ft + 100, st + 20))

                step = font.render(f'{char.step}', True, (0, 0, 0))
                screen.blit(step, (ft + 20, st + 40))
                screen.blit(boot, (ft, st + 40))

                cost = font.render(f'{char.cost}', True, (0, 0, 0))
                screen.blit(cost, (ft + 120, st + 40))
                screen.blit(dollar, (ft + 100, st + 40))

    def which_char(self, pos):
        global allies
        if len(allies) < 5:
            x, y = pos
            if 497 > x > 192 and 553 > y > 206:
                if not chars[0].is_bought:
                    allies += [chars[0].name]
                    chars[0].is_bought = True
            if 893 > x > 594 and 648 > y > 305:
                if not chars[1].is_bought:
                    allies += [chars[1].name]
                    chars[1].is_bought = True
            if 1323 > x > 1017 and 559 > y > 222:
                if not chars[2].is_bought:
                    allies += [chars[2].name]
                    chars[2].is_bought = True
            update_allies()


def update_allies():
    f = open('data/allies.txt', 'w')
    f.write(' '.join(allies))
    f.close()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Координаты клетки')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    fps = 60
    clock = pygame.time.Clock()
    h, w = pygame.display.Info().current_h, pygame.display.Info().current_w
    font = pygame.font.Font(None, 22)

    board = pygame.image.load('data/callboard.png')
    bg = pygame.image.load('data/bg.png')

    running = True
    shop = Shop()

    f = open('data/allies.txt')
    allies = f.read().split()
    f.close()

    f = open('data/chars.txt')
    all_chars = f.read().split()
    f.close()

    shop_chars = []
    for i in range(3):
        shop_chars += [choice(all_chars)]

    hart = pygame.image.load('data/shop_icons/hart.png').convert_alpha()
    hart = pygame.transform.scale(hart, (12, 13))
    sword = pygame.image.load('data/shop_icons/swords.png').convert_alpha()
    sword = pygame.transform.scale(sword, (16, 13))
    speed_sword = pygame.image.load('data/shop_icons/speed_sword.png').convert_alpha()
    speed_sword = pygame.transform.scale(speed_sword, (12, 13))
    bow = pygame.image.load('data/shop_icons/bow.png').convert_alpha()
    boot = pygame.image.load('data/shop_icons/boot.png').convert_alpha()
    dollar = pygame.image.load('data/shop_icons/dollar.png').convert_alpha()
    dollar = pygame.transform.scale(dollar, (7, 14))
    print(h, w)
    con = sqlite3.connect("data/game.db")
    cur = con.cursor()
    chars = []
    for name in shop_chars:
        image = pygame.image.load(f'data/charters/{name}.png').convert_alpha()
        is_ally = True
        _, _, hp, attack, attack_range, step, speed, char_h = cur.execute(f"""SELECT * FROM charters
               WHERE name = '{name}'""").fetchall()[0]
        charter = Char(name, image, is_ally, hp, attack, attack_range, step, speed, char_h)
        chars += [charter]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                act = event.button
            if event.type == pygame.MOUSEBUTTONUP:
                print(shop.which_char(event.pos))
                print(event.pos)
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(bg, (0, 0))
        shop.render(screen)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()



'''
1: 251, 429
2: 654, 636
3: 1089, 440
'''