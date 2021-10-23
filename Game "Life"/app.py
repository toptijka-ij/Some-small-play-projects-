import random

import pygame

WIDTH = 480
HEIGHT = 360
CELL_SIZE_CONSTANT = 10
ROWS, COLS = WIDTH // CELL_SIZE_CONSTANT, HEIGHT // CELL_SIZE_CONSTANT


def draw_cells(place, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            pygame.draw.rect(place, (0, 255 * matrix[i][j] % 256, 0),
                             [i * CELL_SIZE_CONSTANT, j * CELL_SIZE_CONSTANT, CELL_SIZE_CONSTANT, CELL_SIZE_CONSTANT])


def neighbours(current, x, y):
    count = -1
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if current[i][j]:
                count += 1
    if count in (2, 3):
        return True
    return False


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((HEIGHT, WIDTH))
    current = [[random.choice([0, 1]) for j in range(ROWS)] for i in range(COLS)]
    while 1:
        win.fill(pygame.Color('black'))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
        draw_cells(win, current)
        pygame.display.flip()
        pygame.time.delay(500)
        next = [([0] * ROWS) for i in range(COLS)]
        for i in range(1, COLS - 1):
            for j in range(1, ROWS - 1):
                next[i][j] = neighbours(current, i, j)
        current = next[:]
