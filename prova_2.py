import pygame
import random
import time

pygame.init()

# Configuració
WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matching Game")

font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 30)

WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
GREEN = (100, 220, 100)
RED = (220, 100, 100)
BLUE = (210, 220, 235)

# Dades
pairs = {
    "ア": "a",
    "イ": "i",
    "ウ": "u",
    "エ": "e",
    "オ": "o"
}

left_items = list(pairs.keys())
right_items = list(pairs.values())

random.shuffle(left_items)
random.shuffle(right_items)

selected_left = None
selected_right = None

wrong_pair = None
wrong_time = 0

matched = []

# Crear targetes
left_cards = []
right_cards = []

card_width = 450
card_height = 90

for i, item in enumerate(left_items):
    rect = pygame.Rect(
        50,
        50 + i * 120,
        card_width,
        card_height
    )
    left_cards.append((rect, item))

for i, item in enumerate(right_items):
    rect = pygame.Rect(
        700,
        50 + i * 120,
        card_width,
        card_height
    )
    right_cards.append((rect, item))


running = True

while running:

    screen.fill(BLUE)

    # Mostrar cartes esquerra
    for rect, value in left_cards:

        color = GRAY

        if value in matched:
            color = GREEN

        if wrong_pair and value in wrong_pair:
            color = RED

        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)

        text = font.render(value, True, BLACK)
        screen.blit(
            text,
            text.get_rect(center=rect.center)
        )

    # Mostrar cartes dreta
    for rect, value in right_cards:

        color = GRAY

        if value in matched:
            color = GREEN

        if wrong_pair and value in wrong_pair:
            color = RED

        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)

        text = small_font.render(value, True, BLACK)
        screen.blit(
            text,
            text.get_rect(center=rect.center)
        )

    # Eliminar vermell després de 0.7 segons
    if wrong_pair:
        if time.time() - wrong_time > 0.7:
            wrong_pair = None

    # Comprovar victòria
    if len(matched) == len(pairs) * 2:
        win_text = font.render("HAS GUANYAT!", True, (0, 150, 0))
        screen.blit(win_text, (450, 20))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            # Esquerra
            for rect, value in left_cards:
                if rect.collidepoint(pos):
                    if value not in matched:
                        selected_left = value

            # Dreta
            for rect, value in right_cards:
                if rect.collidepoint(pos):
                    if value not in matched:
                        selected_right = value

            # Comprovar parella
            if selected_left and selected_right:

                if pairs[selected_left] == selected_right:

                    matched.append(selected_left)
                    matched.append(selected_right)

                else:

                    wrong_pair = (
                        selected_left,
                        selected_right
                    )
                    wrong_time = time.time()

                selected_left = None
                selected_right = None

    pygame.display.flip()

pygame.quit()