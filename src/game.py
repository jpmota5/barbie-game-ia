import pygame
import sys
from src.grid import draw_grid, load_grid_from_file

# Inicializando o pygame
pygame.init()

# Definindo algumas cores
BLACK = (0, 0, 0)

# Dimensões da janela e da célula
WIDTH, HEIGHT = 630, 630  # Tamanho da janela
GRID_SIZE = 42            # Tamanho da matriz
CELL_SIZE = 15            # Tamanho de cada célula

# Criando a janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo da Matriz 42x42')

# Função para carregar as imagens dos personagens
def load_character_images():
    characters = {
        'barbie': pygame.image.load('assets/barbie.png'),
        'brandon': pygame.image.load('assets/brandon.png'),
        'mary': pygame.image.load('assets/mary.png'),
        'ken': pygame.image.load('assets/ken.png'),
        'suzy': pygame.image.load('assets/suzy.png'),
        'carly': pygame.image.load('assets/carly.png'),
        'polly': pygame.image.load('assets/polly.png')
    }
    for name, image in characters.items():
        characters[name] = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
    return characters

# Função principal do jogo
def main():
    running = True
    
    # Carrega a matriz do arquivo
    grid = load_grid_from_file('assets/matriz.txt')
    
    # Carregar as imagens dos personagens
    character_images = load_character_images()
    
    # Definir a posição dos personagens fixos
    characters = {
        'brandon': (9, 8),
        'mary': (4, 12),
        'ken': (5, 34),
        'suzy': (35, 14),
        'carly': (23, 37),
        'polly': (36, 36)
    }
    
    # Posição inicial da Barbie
    barbie_pos = [22, 18]  # Inicial na linha 23, coluna 19

    while running:
        screen.fill(BLACK)  # Preenche a tela com preto

        draw_grid(screen, grid)  # Desenha a matriz carregada do arquivo
        
        # Desenha os personagens fixos na matriz
        for name, (row, col) in characters.items():
            image = character_images[name]
            x, y = col * CELL_SIZE, row * CELL_SIZE
            screen.blit(image, (x, y))  # Desenha a imagem do personagem na posição fixa

        # Desenha a Barbie na posição atual dela
        barbie_x, barbie_y = barbie_pos[1] * CELL_SIZE, barbie_pos[0] * CELL_SIZE
        screen.blit(character_images['barbie'], (barbie_x, barbie_y))  # Desenha a imagem da Barbie

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Movimenta a Barbie com as teclas de seta
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and barbie_pos[1] > 0:
                    barbie_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and barbie_pos[1] < GRID_SIZE - 1:
                    barbie_pos[1] += 1
                elif event.key == pygame.K_UP and barbie_pos[0] > 0:
                    barbie_pos[0] -= 1
                elif event.key == pygame.K_DOWN and barbie_pos[0] < GRID_SIZE - 1:
                    barbie_pos[0] += 1

        pygame.display.flip()  # Atualiza a tela

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
