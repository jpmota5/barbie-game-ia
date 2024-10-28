import pygame
import sys
import random
import heapq
import time
import itertools  # Para gerar permutações
from src.grid import draw_grid, load_grid_from_file

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 20, 147)
ROSA_PATH = (255, 105, 180)

WIDTH, HEIGHT = 630, 630
GRID_SIZE = 42
CELL_SIZE = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BARBIE WORLD')

font = pygame.font.Font(None, 30)

def heuristica(pos_atual, destino):
    """Calcula a distância de Manhattan entre dois pontos."""
    return abs(pos_atual[0] - destino[0]) + abs(pos_atual[1] - destino[1])

def custo_movimento(mapa, pos1, pos2):
    """Define o custo de movimento entre dois pontos no mapa com base no tipo de terreno."""
    terreno_custo = {
        1: 1,   # asfalto
        3: 3,   # terra
        5: 5,   # grama
        10: 10  # paralelepípedo
    }
    
    tipo_terreno = mapa[pos2[0]][pos2[1]]  
    return terreno_custo.get(tipo_terreno, float('inf'))

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

def load_logo_image():
    logo = pygame.image.load('assets/barbie-logo.png')
    logo = pygame.transform.scale(logo, (200, 100))
    return logo

def display_results_overlay(screen, total_time, total_cost, friends):
    overlay_width, overlay_height = 400, 200
    overlay_x, overlay_y = (WIDTH - overlay_width) // 2, (HEIGHT - overlay_height) // 2
    overlay_rect = pygame.Rect(overlay_x, overlay_y, overlay_width, overlay_height)

    pygame.draw.rect(screen, ROSA_PATH, overlay_rect)
    pygame.draw.rect(screen, WHITE, overlay_rect, 2)

    results = [
        f"Tempo total: {total_time:.2f} segundos",
        f"Custo total: {total_cost}",
        "Convencidos: " + ", ".join(friends)
    ]

    y_offset = overlay_y + 20
    for line in results:
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (overlay_x + 10, y_offset))
        y_offset += 40

    exit_button_width = 100
    exit_button_height = 40
    exit_button = pygame.Rect(overlay_x + (overlay_width - exit_button_width) // 2,
                               overlay_y + overlay_height - 60,
                               exit_button_width, exit_button_height)

    pygame.draw.rect(screen, WHITE, exit_button)
    exit_text = font.render("Sair", True, PINK)
    screen.blit(exit_text, (exit_button.x + (exit_button_width - exit_text.get_width()) // 2,
                             exit_button.y + (exit_button_height - exit_text.get_height()) // 2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def a_star_search(mapa, inicio, destino):
    filas_prioridade = []
    heapq.heappush(filas_prioridade, (0, inicio))
    custo_acumulado = {inicio: 0}
    caminho = {inicio: None}
    visitados = set()

    while filas_prioridade:
        _, ponto_atual = heapq.heappop(filas_prioridade)

        if ponto_atual in visitados:
            continue
        visitados.add(ponto_atual)

        if ponto_atual == destino:
            caminho_final = []
            while ponto_atual:
                caminho_final.append(ponto_atual)
                ponto_atual = caminho[ponto_atual]
            return caminho_final[::-1]  

        for vizinho in get_neighbors(ponto_atual, mapa):
            custo_para_vizinho = custo_acumulado[ponto_atual] + custo_movimento(mapa, ponto_atual, vizinho)
            if custo_para_vizinho < custo_acumulado.get(vizinho, float('inf')):
                caminho[vizinho] = ponto_atual
                custo_acumulado[vizinho] = custo_para_vizinho
                prioridade = custo_para_vizinho + heuristica(vizinho, destino)
                heapq.heappush(filas_prioridade, (prioridade, vizinho))

    return []

def get_neighbors(pos, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
            neighbors.append(neighbor)
    return neighbors

def main_game():
    random.seed(time.time())  # Seed para garantir aleatoriedade entre execuções
    
    grid = load_grid_from_file('assets/matriz.txt')
    character_images = load_character_images()
    
    characters = {
        'brandon': (9, 8),
        'mary': (4, 12),
        'ken': (5, 34),
        'suzy': (35, 14),
        'carly': (23, 37),
        'polly': (36, 36)
    }
    
    barbie_pos = [22, 18]
    initial_barbie_pos = barbie_pos.copy()
    convinced_friends = []
    total_cost = 0
    path_history = []

    start_time = time.time()

    # Sorteia 3 amigos aleatórios a cada execução do jogo
    friends_list = list(characters.keys())
    selected_friends = random.sample(friends_list, 3)
    print(f"Sorteados: {selected_friends}")

    current_pos = barbie_pos.copy()
    remaining_friends = set(characters.keys())

    while len(convinced_friends) < 3:
        closest_friend = None
        min_cost = float('inf')
        closest_path = []

        for friend in remaining_friends:
            friend_pos = characters[friend]
            path = a_star_search(grid, tuple(current_pos), friend_pos)
            cost = sum(custo_movimento(grid, path[i], path[i + 1]) for i in range(len(path) - 1))
            
            if cost < min_cost:
                min_cost = cost
                closest_friend = friend
                closest_path = path

        if closest_path:
            while closest_path:
                path_history.append(tuple(current_pos))
                current_pos = closest_path.pop(0)

                barbie_x, barbie_y = current_pos[1] * CELL_SIZE, current_pos[0] * CELL_SIZE
                screen.fill(BLACK)
                draw_grid(screen, grid)

                for pos in path_history:
                    pygame.draw.circle(screen, ROSA_PATH, (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), 3)

                for name, (row, col) in characters.items():
                    image = character_images[name]
                    x, y = col * CELL_SIZE, row * CELL_SIZE
                    screen.blit(image, (x, y))

                screen.blit(character_images['barbie'], (barbie_x, barbie_y))
                pygame.display.flip()
                time.sleep(0.15)

            if closest_friend in selected_friends:
                convinced_friends.append(closest_friend)
            remaining_friends.remove(closest_friend)
            total_cost += min_cost
            path_history.append(tuple(current_pos))

    # Calcula o caminho de volta para a posição inicial
    return_path = a_star_search(grid, tuple(current_pos), tuple(initial_barbie_pos))
    return_cost = sum(custo_movimento(grid, return_path[i], return_path[i + 1]) for i in range(len(return_path) - 1))
    total_cost += return_cost

    # Exibe a volta da Barbie até a posição inicial
    while return_path:
        path_history.append(tuple(current_pos))
        current_pos = return_path.pop(0)

        barbie_x, barbie_y = current_pos[1] * CELL_SIZE, current_pos[0] * CELL_SIZE
        screen.fill(BLACK)
        draw_grid(screen, grid)

        for pos in path_history:
            pygame.draw.circle(screen, ROSA_PATH, (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), 3)

        for name, (row, col) in characters.items():
            image = character_images[name]
            x, y = col * CELL_SIZE, row * CELL_SIZE
            screen.blit(image, (x, y))

        screen.blit(character_images['barbie'], (barbie_x, barbie_y))
        pygame.display.flip()
        time.sleep(0.15)

    total_time = time.time() - start_time
    display_results_overlay(screen, total_time, total_cost, convinced_friends)

def main_menu():
    running = True
    logo_image = load_logo_image()
    title_font = pygame.font.Font(None, 50)
    start_font = pygame.font.Font(None, 30)

    while running:
        screen.fill(WHITE)
        
        # Centralizar título
        title_text = title_font.render("BARBIE WORLD", True, PINK)
        title_x = (WIDTH - title_text.get_width()) // 2
        title_y = (HEIGHT - title_text.get_height() - logo_image.get_height() - 50) // 2  # Ajustado para ficar abaixo da logo

        # Centralizar logo
        logo_x = (WIDTH - logo_image.get_width()) // 2
        logo_y = title_y + title_text.get_height() + 20  # Espaçamento entre o título e a logo

        # Centralizar texto de início
        start_text = start_font.render("Aperte ENTER para começar o jogo", True, PINK)
        start_x = (WIDTH - start_text.get_width()) // 2
        start_y = logo_y + logo_image.get_height() + 30  # Espaçamento entre a logo e o texto

        # Desenhar elementos na tela
        screen.blit(title_text, (title_x, title_y))
        screen.blit(logo_image, (logo_x, logo_y))
        screen.blit(start_text, (start_x, start_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_game()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()