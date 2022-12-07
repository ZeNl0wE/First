import pygame


class Board:
    def __init__(self, width, height, seze):
        self.seze = seze
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = (self.seze[0] - self.left * 2) // self.width

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size,
                                      self.cell_size))

                pygame.draw.rect(screen, (255, 255, 255), (
                    j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x_cell = (x - self.left) // self.cell_size
        y_cell = (y - self.top) // self.cell_size
        if 0 <= x_cell < self.width and 0 <= y_cell < self.height:
            return x_cell, y_cell

    def on_click(self, cell_coords):
        x, y = cell_coords
        self.board[y][x] = not self.board[y][x]

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos):
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)

    def is_ex(self, pos):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def count_N(self, pos):
        x, y = pos
        summ = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.is_ex((i, j)):
                    summ += self.board[i][j]

        summ -= self.board[x][y]
        return summ

    def next_get(self):
        new_Board = []
        for i in range(len(self.board)):
            new_Board.append(self.board[i][:])
        new_Board = self.board.copy()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 1:
                    if self.count_N((i, j)) in (2, 3):
                        new_Board[i][j] = 1
                    else:
                        new_Board[i][j] = 0
                else:
                    if self.count_N((i, j)) in (2, 3):
                        new_Board[i][j] = 1
                    else:
                        new_Board[i][j] = 0

        self.board = new_Board[:]


class life(Board):
    def __init__(self):
        pass


if __name__ == '__main__':
    pygame.init()
    size = 700, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    is_rad = True
    running = True
    clock = pygame.time.Clock()
    board = Board(30, 30, size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP and is_rad:
                if event.button == 1:
                    board.get_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_rad = not is_rad
        if not is_rad:
            board.next_get()

        board.render(screen)
        clock.tick(30)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
