import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Координаты клетки')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    fps = 60
    clock = pygame.time.Clock()
    h, w = pygame.display.Info().current_h, pygame.display.Info().current_w
    font = pygame.font.Font(None, 22)
    running = True
    board = pygame.image.load('data/callboard.png')

    f = open('data/is_lose.txt')
    type = f.read()
    f.close()

    if type == 'y':
        bg = pygame.image.load('data/lose.png')
    else:
        bg = pygame.image.load('data/win.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(bg, (0, 0))

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
