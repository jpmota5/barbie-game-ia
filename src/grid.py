import pygame

# Definindo a cor branca para as bordas
WHITE = (255, 255, 255)
CELL_SIZE = 15  # Tamanho de cada célula
GRID_SIZE = 42  # Matriz 42x42

# Função para desenhar a matriz
def draw_grid(screen):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Desenha as bordas das células
