import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, row, col, size, total_rows, total_cols, groups):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.row = row
        self.col = col
        self.size = size
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.x = col * size
        self.y = row * size

        # cell state
        self.barrier = False
        self.neighbors = None
        self.walls = None
        self.maze_neighbors = None
        self.color = 'grey30'

        # sprite settings
        self.image = pygame.Surface((self.size-1,self.size-1))
        self.rect = self.image.get_rect(topleft = (self.x,self.y))

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = 'grey30'
        self.barrier = False

    def make_barrier(self):
        self.color = 'black'
        self.barrier = True

    def update_neighbors(self, grid):
        self.neighbors = {}
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier:
            self.neighbors['down'] = grid[self.row + 1][self.col]

        if self.col > 0 and not grid[self.row][self.col - 1].barrier:
            self.neighbors['left'] = grid[self.row][self.col - 1]

        if self.row > 0 and not grid[self.row - 1][self.col].barrier:
            self.neighbors['up'] = grid[self.row - 1][self.col]

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].barrier:
            self.neighbors['right'] = grid[self.row][self.col + 1]

    def update_walls(self, grid):
        self.walls = {}
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].barrier: 
            self.walls['down'] = grid[self.row + 1][self.col]

        if self.col > 0 and grid[self.row][self.col - 1].barrier:
            self.walls['left'] = grid[self.row][self.col - 1]

        if self.row > 0 and grid[self.row - 1][self.col].barrier:
            self.walls['up'] = grid[self.row - 1][self.col]

        if self.col < self.total_cols - 1 and grid[self.row][self.col + 1].barrier:
            self.walls['right'] = grid[self.row][self.col + 1]
        
    def update_neighbors_for_maze(self, grid):
        # for maze, neighbors considered to be second but next cell eg distance of 2
        self.maze_neighbors = {}
        if self.row < self.total_rows - 2 and not grid[self.row + 2][self.col].barrier:
            self.maze_neighbors['down'] = grid[self.row + 2][self.col]

        if self.col > 1 and not grid[self.row][self.col - 2].barrier:
            self.maze_neighbors['left'] = grid[self.row][self.col - 2]

        if self.row > 1 and not grid[self.row - 2][self.col].barrier:
            self.maze_neighbors['up'] = grid[self.row - 2][self.col]

        if self.col < self.total_cols - 2 and not grid[self.row][self.col + 2].barrier:
            self.maze_neighbors['right'] = grid[self.row][self.col + 2]



    def left_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
    def right_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[2]

    def update(self):
        if self.right_clicked():
            self.reset()

        elif self.left_clicked():
            self.make_barrier()
        
        self.image.fill(self.color)