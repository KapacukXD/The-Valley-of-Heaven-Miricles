#MODULE INFO BLOCK
MODULE_NAME = 'libboard'
MODULE_VERSION = '0.0.1_vhm'
#MODULE INFO BLOCK END

import pretty_out
import pygame
import os

logger = pretty_out.Log()


class Board:
    # создание поля
    def __init__(self, width: int, height: int, cell_class: type):
        self.width = width
        self.height = height
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.__cell_class__ = cell_class
        self.make_board()
        logger.start_message(MODULE_NAME, MODULE_VERSION)

    def make_board(self):
        self.board = [[
            self.__cell_class__(self.left + (i * self.cell_size),
                                self.top + (j * self.cell_size),
                                self.cell_size) for j in range(self.height)
        ] for i in range(self.width)]

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.make_board()

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen,
                         color=pygame.Color('white'),
                         rect=(self.left, self.top,
                               self.cell_size * self.width,
                               self.cell_size * self.height),
                         width=1)

        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j].render(screen)

    def get_cell_by_position(self, x_pos: int, y_pos: int):
        try:
            return self.board[(x_pos - self.left) //
                              self.cell_size][(y_pos - self.top) //
                                              self.cell_size]
        except:
            return None

    def on_click(self, x_pos: int, y_pos: int):
        self.get_cell_by_position(x_pos, y_pos).on_click()


class Cell:
    def __init__(self, x_pos: int, y_pos: int, size: int):
        self.elements = []
        self.rect = ((x_pos, y_pos), (size, size))

    def add_element(self, element, element_name: str):
        try:
            self.elements.append({element_name: element})
        except Exception as E:
            logger.error(MODULE_NAME, E)
            raise E

    def remove_element(self, element_name: str):
        try:
            self.elements.pop(self.elements[element_name])
        except KeyError as E:
            logger.error(MODULE_NAME, E)
            raise E

    def get_all_elements(self):
        return list(self.elements.keys())

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen,
                         color=pygame.Color('white'),
                         rect=self.rect,
                         width=1)
        try:
            self.elements[0].render()
        except IndexError:
            pass

    def on_click(self, *args, **kwargs):
        self.elements[0].on_click(args, kwargs)

    def __str__(self):
        return f'cell on {self.rect}'


class GameDisplay:
    def __init__(self,
                 image_name: str,
                 display_resolution: tuple[int, int],
                 window_name: str = 'Game Window') -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(display_resolution)
        self.bg = pygame.image.load(
            os.join(['data', 'images', 'backgrounds', image_name]))
        pygame.display.set_caption(window_name)
        self.screen.blit(self.bg, self.bg.get_rect())

    def get_screen(self) -> pygame.Surface:
        return self.screen

