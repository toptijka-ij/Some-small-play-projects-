import random

import pygame

WIDTH = 480
HEIGHT = 360
CELL_SIZE_CONSTANT = 10
ROWS, COLS = WIDTH // CELL_SIZE_CONSTANT, HEIGHT // CELL_SIZE_CONSTANT


def remove_ones_row_cols(arr):
    n = len(arr)
    m = len(arr[0])
    r = []
    c = ([0] * m)
    for i in range(n):
        if all(arr[i]):
            r.append(i)
        for j in range(m):
            if arr[i][j] == 1:
                c[j] += 1
    c = [x[0] for x in enumerate(c) if x[1] == n]
    for i in r[::-1]:
        del arr[i]
    for i in range(len(arr)):
        for j in c[::-1]:
            del arr[i][j]


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.schema = []

    def make_step(self, k, arr):
        for i in range(maze.rows):
            for j in range(maze.cols):
                if arr[i][j] == k:
                    if i > 0 and arr[i - 1][j] == 0 and self.schema[i - 1][j] == 1:
                        arr[i - 1][j] = k + 1
                    if j > 0 and arr[i][j - 1] == 0 and self.schema[i][j - 1] == 1:
                        arr[i][j - 1] = k + 1
                    if i < maze.rows - 1 and arr[i + 1][j] == 0 and self.schema[i + 1][j] == 1:
                        arr[i + 1][j] = k + 1
                    if j < maze.cols - 1 and arr[i][j + 1] == 0 and self.schema[i][j + 1] == 1:
                        arr[i][j + 1] = k + 1

    def nei(self, cell: Cell):
        res = {}
        if self.schema[cell.x + 2][cell.y] == -1:
            res['bottom'] = Cell(cell.x + 2, cell.y)
        if self.schema[cell.x - 2][cell.y] == -1:
            res['top'] = Cell(cell.x - 2, cell.y)
        if self.schema[cell.x][cell.y + 2] == -1:
            res['right'] = Cell(cell.x, cell.y + 2)
        if self.schema[cell.x][cell.y - 2] == -1:
            res['left'] = Cell(cell.x, cell.y - 2)
        return res

    @staticmethod
    def create_maze(rows, cols):
        maze = Maze(rows, cols)
        maze.schema = [([0] * maze.cols) for r in range(maze.rows)]
        for i in range(maze.rows):
            for j in range(maze.cols):
                if i != 0 and i != 1 and i != maze.rows - 1 and i != maze.rows - 2 \
                        and j != 0 and j != maze.cols - 1 and j != 1 and j != maze.cols - 2:
                    maze.schema[i][j] = -1
        start = (random.choice(range(2, maze.rows - 3)), random.choice(range(2, maze.cols - 3)))
        stack = [Cell(*start), ]
        while stack:
            cur_cell = stack.pop()
            nei_cells = maze.nei(cur_cell)
            if nei_cells:
                rand_cell = random.choice(list(nei_cells.keys()))
                if rand_cell == 'bottom':
                    maze.schema[cur_cell.x + 1][cur_cell.y] = 1
                    maze.schema[cur_cell.x + 2][cur_cell.y] = 1
                elif rand_cell == 'top':
                    maze.schema[cur_cell.x - 1][cur_cell.y] = 1
                    maze.schema[cur_cell.x - 2][cur_cell.y] = 1
                elif rand_cell == 'left':
                    maze.schema[cur_cell.x][cur_cell.y - 1] = 1
                    maze.schema[cur_cell.x][cur_cell.y - 2] = 1
                elif rand_cell == 'right':
                    maze.schema[cur_cell.x][cur_cell.y + 1] = 1
                    maze.schema[cur_cell.x][cur_cell.y + 2] = 1
                for k in nei_cells.keys():
                    if k != rand_cell:
                        stack.append(nei_cells[k])
                stack.append(nei_cells[rand_cell])
        for i in range(maze.rows):
            for j in range(maze.cols):
                maze.schema[i][j] = 1 if maze.schema[i][j] != 1 else 0
        remove_ones_row_cols(maze.schema)
        maze.rows, maze.cols = len(maze.schema), len(maze.schema[0])
        return maze

    def set_start_and_finish(self):
        self.start = random.choice(
            [Cell(x, y) for x in range(self.rows) for y in range(self.cols) if self.schema[x][y] == 1])
        self.finish = random.choice(
            [Cell(x, y) for x in range(self.rows) for y in range(self.cols) if self.schema[x][y] == 1])

    def find_path(self):
        arr = [([0] * self.cols) for r in range(self.rows)]
        arr[self.start.x][self.start.y] = 1
        k = 0
        while arr[self.finish.x][self.finish.y] == 0:
            k += 1
            self.make_step(k, arr)

        i, j = self.finish.x, self.finish.y
        k = arr[i][j]
        path = [Cell(i, j)]
        while k > 1:
            if i > 0 and arr[i - 1][j] == k - 1:
                i, j = i - 1, j
                path.append(Cell(i, j))
                k -= 1
            elif j > 0 and arr[i][j - 1] == k - 1:
                i, j = i, j - 1
                path.append(Cell(i, j))
                k -= 1
            elif i < self.rows - 1 and arr[i + 1][j] == k - 1:
                i, j = i + 1, j
                path.append(Cell(i, j))
                k -= 1
            elif j < self.cols - 1 and arr[i][j + 1] == k - 1:
                i, j = i, j + 1
                path.append(Cell(i, j))
                k -= 1
        pathes = []
        for i in range(self.rows):
            for j in range(self.cols):
                if arr[i][j]:
                    pathes.append(Cell(i, j))
        return path, pathes

    def draw_maze(self, place):
        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(place, pygame.Color('white') if self.schema[i][j] == 1 else pygame.Color('black'),
                                 [i * CELL_SIZE_CONSTANT, j * CELL_SIZE_CONSTANT, CELL_SIZE_CONSTANT,
                                  CELL_SIZE_CONSTANT])
                pygame.display.flip()
                pygame.time.delay(3)

    def draw_points(self, place, color, *cells):
        for cell in cells:
            pygame.draw.rect(place, pygame.Color(color),
                             [cell.x * CELL_SIZE_CONSTANT + CELL_SIZE_CONSTANT / 4,
                              cell.y * CELL_SIZE_CONSTANT + CELL_SIZE_CONSTANT / 4,
                              CELL_SIZE_CONSTANT / 2, CELL_SIZE_CONSTANT / 2])
            pygame.display.flip()
            pygame.time.delay(5)


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((WIDTH - 25, HEIGHT - 25))
    win.fill(pygame.Color('black'))
    maze = Maze.create_maze(ROWS, COLS)
    maze.draw_maze(win)
    maze.set_start_and_finish()
    maze.draw_points(win, 'MAGENTA', maze.start, maze.finish)
    path, pathes = maze.find_path()
    maze.draw_points(win, 'YELLOW', *pathes)
    maze.draw_points(win, 'BLUE', maze.start, maze.finish)
    maze.draw_points(win, 'MAGENTA', *path)
    maze.draw_points(win, 'BLUE', maze.start, maze.finish)
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
