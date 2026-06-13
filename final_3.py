import pygame
import sys
import random
import time
import requests
import json

pygame.init()

# =========================
# REQUEST INICIAL
# =========================
respuesta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
datos = respuesta.json()

game_id = datos["game_id"]
seed = datos["seed"]

random.seed(seed)

print("Game ID:", game_id)
print("Seed:", seed)

# =========================
# CONFIG
# =========================
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
SHADOW = (180, 180, 180)

# FUENTES
font = pygame.font.SysFont("arial", 60)
small_font = pygame.font.SysFont("arial", 35)

# MENÚ
titulo = font.render("Benvingut al joc", True, BLACK)
boton = pygame.Rect(500, 350, 200, 80)

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

ultimo_guardado = time.time()
partida_finalizada = False

# CREAR CARTAS
left_cards = []
right_cards = []

card_width = 450
card_height = 90

for i, item in enumerate(left_items):
    rect = pygame.Rect(
        50,
        100 + i * 110,
        card_width,
        card_height
    )
    left_cards.append((rect, item))

for i, item in enumerate(right_items):
    rect = pygame.Rect(
        700,
        100 + i * 110,
        card_width,
        card_height
    )
    right_cards.append((rect, item))

# =========================
# BUCLE PRINCIPAL
# =========================
running = True

while running:

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # BOTÓN MENÚ
        if mostrar_menu and event.type == pygame.MOUSEBUTTONDOWN:
            if boton.collidepoint(event.pos):
                mostrar_menu = False

        # CLICK EN JUEGO
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

    # =========================
    # MENU
    # =========================
    if mostrar_menu:

        screen.fill(WHITE)

        screen.blit(
            titulo,
            titulo.get_rect(center=(WIDTH // 2, 180))
        )

        if boton.collidepoint(mouse):
            color_boton = (40, 40, 40)
        else:
            color_boton = BLACK

        pygame.draw.rect(
            screen,
            color_boton,
            boton,
            border_radius=20
        )

        text = small_font.render("JUGAR", True, WHITE)

        screen.blit(
            text,
            text.get_rect(center=boton.center)
        )

    # =========================
    # JUEGO
    # =========================
    else:

        screen.fill(BLUE)

        # GUARDAR PROGRESO CADA 5s
        if time.time() - ultimo_guardado > 5:

            progreso = {
                "matched": matched
            }

            requests.post(
                "https://fun.codelearn.cat/hackathon/game/store_progress",
                json={
                    "game_id": game_id,
                    "data": progreso
                }
            )

            print("Progreso guardado")

            ultimo_guardado = time.time()

        # IZQUIERDA
        for rect, value in left_cards:

            sombra = rect.move(5, 5)
            pygame.draw.rect(
                screen,
                SHADOW,
                sombra,
                border_radius=12
            )

            color = GRAY

            if value in matched:
                color = GREEN

            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                BLACK,
                rect,
                2,
                border_radius=12
            )

            img = images[value]
            img_rect = img.get_rect(center=rect.center)
            screen.blit(img, img_rect)

        # DERECHA
        for rect, value in right_cards:

            sombra = rect.move(5, 5)
            pygame.draw.rect(
                screen,
                SHADOW,
                sombra,
                border_radius=12
            )

            color = GRAY

            if value in matched:
                color = GREEN

            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                BLACK,
                rect,
                2,
                border_radius=12
            )

            text = small_font.render(
                value.upper(),
                True,
                BLACK
            )

            screen.blit(
                text,
                text.get_rect(center=rect.center)
            )

        # QUITAR ERROR ROJO
        if wrong_pair:
            if time.time() - wrong_time > 0.7:
                wrong_pair = None

        # GANAR
        if len(matched) == len(pairs) * 2:

            win_text = font.render(
                "HAS GUANYAT!",
                True,
                (0, 150, 0)
            )

            screen.blit(
                win_text,
                win_text.get_rect(center=(WIDTH // 2, 40))
            )

            # FINALIZAR SOLO UNA VEZ
            if not partida_finalizada:

                score = 100

                requests.post(
                    "https://fun.codelearn.cat/hackathon/game/finalize",
                    json={
                        "game_id": game_id,
                        "data": {
                            "matched": matched
                        },
                        "score": score
                    }
                )

                print("Partida finalizada")
                partida_finalizada = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()