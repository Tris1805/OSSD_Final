import pygame
import os
from tkinter import messagebox


current_dir = os.path.dirname(os.path.abspath(__file__))
image_path_X = os.path.join(current_dir, 'imgs', 'letterX.png')
image_path_O = os.path.join(current_dir, 'imgs', 'letterO.png')

try:
    pygame.init()  # Khởi tạo pygame
    letterX = pygame.image.load(image_path_X)
    letterO = pygame.image.load(image_path_O)
    new_width = 20 
    new_height = 20 
    letterX = pygame.transform.scale(letterX, (new_width, new_height))
    letterO = pygame.transform.scale(letterO, (new_width, new_height))
except pygame.error as e:
    print("Error loading image:", e)

class Grid:
    def __init__(self, rows, cols, width=800, height=800):
        self.rows = rows
        self.cols = cols
        self.cell_width = width // cols
        self.cell_height = height // rows

        self.grid = [[0 for x in range(self.rows)] for y in range(self.cols)]
        self.switch_player = True
        self.game_over = False

    def draw(self, surface):
        surface.fill((255, 255, 255))
        for i in range(1, self.rows):
            pygame.draw.line(surface, (200, 200, 200), (0, i * self.cell_height), (self.cols * self.cell_width, i * self.cell_height), 2)
        
        for i in range(1, self.cols):
            pygame.draw.line(surface, (200, 200, 200), (i * self.cell_width, 0), (i * self.cell_width, self.rows * self.cell_height), 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    pos_x = x * self.cell_width + (self.cell_width - letterX.get_width()) // 2
                    pos_y = y * self.cell_height + (self.cell_height - letterX.get_height()) // 2
                    surface.blit(letterX, (pos_x, pos_y))
                elif self.get_cell_value(x, y) == "O":
                    pos_x = x * self.cell_width + (self.cell_width - letterO.get_width()) // 2
                    pos_y = y * self.cell_height + (self.cell_height - letterO.get_height()) // 2
                    surface.blit(letterO, (pos_x, pos_y))

    def get_cell_value(self, x, y):
        return self.grid[y][x]
    
    def set_cell_value(self, x, y, value):
        if self.get_cell_value(y, x) == 0:   
                 self.grid[y][x] = value
    
    def get_mouse(self, x, y, player):
        if self.get_cell_value(y, x) == 0:  
            self.set_cell_value(y, x, player)
            if self.checkWin(x,y, player):
                self.game_over = True
        elif self.get_cell_value(y, x) == "X" or self.get_cell_value(y, x) == "O" :
            print("Same box")
            
    def is_box_empty(self, x, y):
        return self.grid[y][x] == 0
                
            

    def print_grid(self):
        for row in self.grid:
            print(row)

    def checkWin(self, x, y, XO):
        # Kiểm tra hàng ngang
        count = 0
        for j in range(20):
            if self.grid[x][j] == XO:
                count += 1
            else:
                count = 0
            if count == 5:
                return True

        # Kiểm tra hàng dọc
        count = 0
        for i in range(20):
            if self.grid[i][y] == XO:
                count += 1
            else:
                count = 0
            if count == 5:
                return True

        # Kiểm tra đường chéo chính (\)
        count = 0
        i, j = x, y
        while i > 0 and j > 0:
            i -= 1
            j -= 1
        while i < 20 and j < 20:
            if self.grid[i][j] == XO:
                count += 1
            else:
                count = 0
            if count == 5:
                return True
            i += 1
            j += 1

        # Kiểm tra đường chéo phụ (/)
        count = 0
        i, j = x, y
        while i < 19 and j > 0:
            i += 1
            j -= 1
        while i >= 0 and j < 20:
            if self.grid[i][j] == XO:
                count += 1
            else:
                count = 0
            if count == 5:
                return True
            i -= 1
            j += 1

        return False

    def reset_grid(self):
        self.grid = [[0 for x in range(self.rows)] for y in range(self.cols)]

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True
