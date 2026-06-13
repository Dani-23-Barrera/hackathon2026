import pygame
import sys
import random
import time
import requests

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
pygame.display.set_caption("Aprèn les vocals japoneses")

clock = pygame.time.Clock()

# =========================
# COLORES
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (210, 220, 235)
GRAY = (230, 230, 230)
GREEN = (100, 220, 100)
RED = (220, 100, 100)
SHADOW = (180, 180, 180)

# =========================
# FUENTES
# =========================
font = pygame.font.SysFont("arial", 60)
small_font = pygame.font.SysFont("arial", 35)

# =========================
# ESTADOS
# =========================
MENU = 0
TEORIA = 1
JOC = 2

pantalla = MENU

# =========================
# BOTONES
# =========================
boto_teoria = pygame.Rect(450, 280, 300, 80)
boto_jugar = pygame.Rect(450, 400, 300, 80)
boto_tornar = pygame.Rect(30, 30, 180, 60)

# =========================
# IMAGEN TEORÍA
# =========================
teoria_img = pygame.image.load("teoria.jpeg")
teoria_img = pygame.transform.scale(teoria_img, (350, 350))

# =========================
# JUEGO
# =========================
pairs = {
    "A.png": "a",
    "I.png": "i",
    "U.jpeg": "u",
    "E.png": "e",
    "O.jpeg": "o"
}

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

# =========================
# CREAR CARTAS
# =========================
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

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # MENU
            if pantalla == MENU:

                if boto_teoria.collidepoint(event.pos):
                    pantalla = TEORIA

                if boto_jugar.collidepoint(event.pos):
                    pantalla = JOC

            # TEORIA
            elif pantalla == TEORIA:

                if boto_tornar.collidepoint(event.pos):
                    pantalla = MENU

            # JUEGO
            elif pantalla == JOC:

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

    # ================= MENU =================
    if pantalla == MENU:

        screen.fill(BLUE)

        titol = font.render(
            "VOCALS JAPONESES",
            True,
            BLACK
        )

        screen.blit(
            titol,
            titol.get_rect(center=(WIDTH//2, 150))
        )

        pygame.draw.rect(screen, GRAY, boto_teoria)
        pygame.draw.rect(screen, BLACK, boto_teoria, 2)

        pygame.draw.rect(screen, GRAY, boto_jugar)
        pygame.draw.rect(screen, BLACK, boto_jugar, 2)

        txt = small_font.render("TEORIA", True, BLACK)
        screen.blit(
            txt,
            txt.get_rect(center=boto_teoria.center)
        )

        txt = small_font.render("JUGAR", True, BLACK)
        screen.blit(
            txt,
            txt.get_rect(center=boto_jugar.center)
        )

    # ================= TEORIA =================
    elif pantalla == TEORIA:

        screen.fill(WHITE)

        titol = font.render("TEORIA", True, BLACK)

        screen.blit(
            titol,
            titol.get_rect(center=(WIDTH//2, 60))
        )

        screen.blit(teoria_img, (100, 180))

        lineas = [
            "L'ASL (American Sign Language)",
            "és una llengua visual que utilitza",
            "gestos amb les mans per comunicar-se.",
            "",
            "En aquest joc aprendràs vocals",
            "mitjançant signes i imatges."
        ]

        y = 180

        for linea in lineas:
            txt = small_font.render(linea, True, BLACK)
            screen.blit(txt, (550, y))
            y += 50

        pygame.draw.rect(screen, GRAY, boto_tornar)
        pygame.draw.rect(screen, BLACK, boto_tornar, 2)

        txt = small_font.render("TORNAR", True, BLACK)

        screen.blit(
            txt,
            txt.get_rect(center=boto_tornar.center)
        )

    # ================= JUEGO =================
    elif pantalla == JOC:

        screen.fill(BLUE)

        # Guardar progreso cada 5 segundos
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
                2
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
                2
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

        # Quitar error rojo
        if wrong_pair:
            if time.time() - wrong_time > 0.7:
                wrong_pair = None

        # GANAR
        if len(matched) == len(pairs) * 2:

            win_text = font.render(
                "HAS GUANYAT!",
                True,
                GREEN
            )

            screen.blit(
                win_text,
                win_text.get_rect(center=(WIDTH//2, 40))
            )

            if not partida_finalizada:

                requests.post(
                    "https://fun.codelearn.cat/hackathon/game/finalize",
                    json={
                        "game_id": game_id,
                        "data": {
                            "matched": matched
                        },
                        "score": 100
                    }
                )

                print("Partida finalizada")
                partida_finalizada = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()