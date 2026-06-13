import pygame
import sys
import random
import time
import requests

pygame.init()

# CONFIG
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc inclusiu")

clock = pygame.time.Clock()

# COLORES
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
GREEN = (100, 220, 100)
RED = (220, 100, 100)
BLUE = (210, 220, 235)

# FUENTES
font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 30)

# MENU
texto = font.render("Benvingut al joc educatiu", True, BLACK)
boton = pygame.Rect(500, 300, 200, 80)

mostrar_menu = True

# PAREJAS
pairs = {
    "A.png": "a",
    "I.png": "i",
    "U.jpeg": "u",
    "E.png": "e",
    "O.jpeg": "o"
}

# CARGAR IMÁGENES
images = {}

for filename in pairs.keys():
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    images[filename] = img

left_items = list(pairs.keys())
right_items = list(pairs.values())

random.shuffle(left_items)
random.shuffle(right_items)

selected_left = None
selected_right = None
wrong_pair = None
wrong_time = 0
matched = []

# CREAR CARTAS
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

# BUCLE PRINCIPAL
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # CLICK BOTÓN MENÚ
        if mostrar_menu and event.type == pygame.MOUSEBUTTONDOWN:
            if boton.collidepoint(event.pos):
                mostrar_menu = False

        # CLICK JUEGO
        elif not mostrar_menu and event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            # Selección izquierda
            for rect, value in left_cards:
                if rect.collidepoint(pos):
                    if value not in matched:
                        selected_left = value

            # Selección derecha
            for rect, value in right_cards:
                if rect.collidepoint(pos):
                    if value not in matched:
                        selected_right = value

            # Comprobar pareja
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

    # MENÚ
    if mostrar_menu:

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLACK, boton)

        text = font.render("Jugar", True, WHITE)

        screen.blit(texto, (350, 150))
        screen.blit(text, (550, 320))

    # JUEGO
    else:

        screen.fill(BLUE)

        # Mostrar izquierda (imágenes)
        for rect, value in left_cards:

            color = GRAY

            if value in matched:
                color = GREEN

            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)

            img = images[value]
            img_rect = img.get_rect(center=rect.center)
            screen.blit(img, img_rect)

        # Mostrar derecha (texto)
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

        # Quitar rojo después de 0.7s
        if wrong_pair:
            if time.time() - wrong_time > 0.7:
                wrong_pair = None

        # Victoria
        if len(matched) == len(pairs) * 2:
            win_text = font.render("HAS GUANYAT!", True, (0, 150, 0))
            screen.blit(win_text, (430, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()