import pygame
import sys
import random
import heapq
import time
from src.grid import draw_grid, load_grid_from_file

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)  # Cor rosa para o botão e fundo do overlay

WIDTH, HEIGHT = 630, 630
GRID_SIZE = 42
CELL_SIZE = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BARBIE WORLD')

font = pygame.font.Font(None, 30)  # Fonte para exibir o texto

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
    logo = pygame.image.load('assets/barbie-logo.png')  # Substitua pelo caminho da sua imagem
    logo = pygame.transform.scale(logo, (200, 100))  # Ajuste o tamanho conforme necessário
    return logo

def display_results_overlay(screen, total_time, total_cost, friends):
    overlay_width, overlay_height = 400, 200
    overlay_x, overlay_y = (WIDTH - overlay_width) // 2, (HEIGHT - overlay_height) // 2
    overlay_rect = pygame.Rect(overlay_x, overlay_y, overlay_width, overlay_height)
    
    # Desenha o fundo rosa
    pygame.draw.rect(screen, PINK, overlay_rect)
    pygame.draw.rect(screen, WHITE, overlay_rect, 2)

    results = [
        f"Tempo total: {total_time:.2f} segundos",
        f"Custo total: {total_cost}",
        "Amigos sorteados: " + ", ".join(friends)
    ]

    y_offset = overlay_y + 20
    for line in results:
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (overlay_x + 10, y_offset))
        y_offset += 40

    # Botão "Sair"
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

    # Loop para verificar o clique no botão "Sair"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def a_star_search(start, goal, grid):
    costs = {0: float('inf'), 1: 1, 3: 3, 5: 5, 10: 10}
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + costs[grid[neighbor[0]][neighbor[1]]]
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
            neighbors.append(neighbor)
    return neighbors

def main_game():
    running = True
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
    friends = random.sample(list(characters.keys()), 3)
    convinced_friends = []
    remaining_friends = friends.copy()
    total_cost = 0

    start_time = time.time()  # Início da contagem de tempo

    while running and len(convinced_friends) < 3:
        screen.fill(BLACK)
        draw_grid(screen, grid)
        
        for name, (row, col) in characters.items():
            image = character_images[name]
            x, y = col * CELL_SIZE, row * CELL_SIZE
            screen.blit(image, (x, y))
        
        barbie_x, barbie_y = barbie_pos[1] * CELL_SIZE, barbie_pos[0] * CELL_SIZE
        screen.blit(character_images['barbie'], (barbie_x, barbie_y))

        if not remaining_friends:
            break

        min_cost = float('inf')
        next_friend = None
        next_path = []
        
        random.shuffle(remaining_friends)
        for friend in remaining_friends:
            goal = characters[friend]
            path = a_star_search(tuple(barbie_pos), goal, grid)
            cost = sum(grid[pos[0]][pos[1]] for pos in path)

            if path and cost < min_cost:
                min_cost = cost
                next_friend = friend
                next_path = path

        if next_friend and next_path:
            path = next_path
            while path:
                barbie_pos = path.pop(0)
                barbie_x, barbie_y = barbie_pos[1] * CELL_SIZE, barbie_pos[0] * CELL_SIZE
                screen.blit(character_images['barbie'], (barbie_x, barbie_y))
                pygame.display.flip()
                time.sleep(0.1)
            
            convinced_friends.append(next_friend)
            remaining_friends.remove(next_friend)
            total_cost += min_cost

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    if len(convinced_friends) == 3:
        path = a_star_search(tuple(barbie_pos), tuple(initial_barbie_pos), grid)
        return_cost = sum(grid[pos[0]][pos[1]] for pos in path)
        total_cost += return_cost
        while path:
            barbie_pos = path.pop(0)
            barbie_x, barbie_y = barbie_pos[1] * CELL_SIZE, barbie_pos[0] * CELL_SIZE
            screen.blit(character_images['barbie'], (barbie_x, barbie_y))
            pygame.display.flip()
            time.sleep(0.1)

    end_time = time.time()
    total_time = end_time - start_time

    display_results_overlay(screen, total_time, total_cost, friends)

def main_menu():
    running = True
    logo_image = load_logo_image()  # Carrega a imagem do logo
    while running:
        screen.fill(WHITE)  # Altera o fundo para branco

        # Título do jogo
        title_text = font.render("BARBIE WORLD", True, (255, 105, 180))  # Cor rosa para o título
        start_text = font.render("Pressione ENTER para começar o jogo", True, (255, 105, 180))  # Texto de início

        # Calcular as posições centralizadas
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = HEIGHT // 2 - 60

        logo_x = WIDTH // 2 - logo_image.get_width() // 2
        logo_y = title_y + title_text.get_height() + 20  # 20 pixels abaixo do título

        start_x = WIDTH // 2 - start_text.get_width() // 2
        start_y = logo_y + logo_image.get_height() + 20  # 20 pixels abaixo do logo

        # Desenhar os elementos na tela
        screen.blit(title_text, (title_x, title_y))
        screen.blit(logo_image, (logo_x, logo_y))
        screen.blit(start_text, (start_x, start_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_game()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main_menu()