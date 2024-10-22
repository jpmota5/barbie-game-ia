import pygame
import sys
from src.grid import draw_grid
from src.player import Cell

# Inicializando o pygame
pygame.init()

# Definindo algumas cores
BLACK = (0, 0, 0)

# Dimensões da janela e da célula
WIDTH, HEIGHT = 630, 630  # Tamanho da janela
GRID_SIZE = 42            # Tamanho da matriz

# Criando a janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo da Matriz 42x42')

# Função principal do jogo
def main():
    running = True
    
    # Célula móvel (começa na posição 0,0)
    moving_cell = Cell(0, 0, (0, 0, 255))  # Azul
    
    # Células coloridas-alvo
    target_cells = [
        Cell(10, 10, (255, 0, 0)),  # Vermelho
        Cell(30, 20, (0, 255, 0)),  # Verde
        Cell(25, 35, (255, 0, 0))   # Vermelho
    ]
    
    while running:
        screen.fill(BLACK)  # Preenche a tela com preto

        draw_grid(screen)  # Desenha a matriz
        
        # Desenha célula móvel
        moving_cell.draw(screen)
        
        # Desenha as células coloridas-alvo
        for cell in target_cells:
            cell.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Movimenta a célula com as teclas de seta
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_cell.move(-1, 0, GRID_SIZE)
                elif event.key == pygame.K_RIGHT:
                    moving_cell.move(1, 0, GRID_SIZE)
                elif event.key == pygame.K_UP:
                    moving_cell.move(0, -1, GRID_SIZE)
                elif event.key == pygame.K_DOWN:
                    moving_cell.move(0, 1, GRID_SIZE)

        pygame.display.flip()  # Atualiza a tela

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()