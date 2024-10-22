import pygame

CELL_SIZE = 15  # Tamanho de cada célula

# Classe para a célula
class Cell:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen):
        rect = pygame.Rect(self.col * CELL_SIZE, self.row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)

    def move(self, dx, dy, grid_size):
        """Movimenta a célula dentro dos limites da grade"""
        self.col = max(0, min(self.col + dx, grid_size - 1))
        self.row = max(0, min(self.row + dy, grid_size - 1))
