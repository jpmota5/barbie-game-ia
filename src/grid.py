import pygame

# Definindo cores conforme a legenda
COLOR_MAP = {
    1: (128, 128, 128),  # Asfalto (Cinza Escuro)
    3: (190, 132, 85),   # Terra (Marrom)
    5: (50, 205, 50),    # Grama (Verde)
    10: (211, 211, 211), # Paralelepípedo (Cinza Claro)
    0: (255, 184, 103)   # Edifícios (Laranja)
}

CELL_SIZE = 15  # Tamanho de cada célula
GRID_SIZE = 42  # Matriz 42x42

# Função para ler o arquivo .txt e carregar a matriz
def load_grid_from_file(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            # Cada linha do arquivo representa uma linha da matriz
            row = list(map(int, line.split()))
            grid.append(row)
    return grid

# Função para desenhar a matriz de acordo com as cores do arquivo
def draw_grid(screen, grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = COLOR_MAP.get(value, (0, 0, 0))  # Se o valor não estiver no map, usar preto
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
