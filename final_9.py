import pygame
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

# =========================
# CONFIG
# =========================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Llenguatge de signes")

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
VICTORIA = 3

pantalla = MENU

# =========================
# BOTONES
# =========================
boto_teoria = pygame.Rect(450, 280, 300, 80)
boto_jugar = pygame.Rect(450, 400, 300, 80)
boto_tornar = pygame.Rect(30, 30, 180, 60)
boto_menu = pygame.Rect(30, 30, 220, 60)

# =========================
# TEORÍA
# =========================
teoria_img = pygame.image.load("teoria.jpeg")
teoria_img = pygame.transform.scale(teoria_img, (350, 350))

# =========================
# NIVELES
# =========================

nivel1 = {
    "A.png": "a",
    "I.png": "i",
    "U.jpeg": "u",
    "E.png": "e",
    "O.jpeg": "o"
}

nivel2 = {
    "no.jpeg": "no",
    "si.jpeg": "si",
    "hola.jpeg": "hola",
    "nombre.jpeg": "el meu nom és",
    "gracias.jpeg": "gràcies"
}

def cargar_imagenes(pairs):
    imgs = {}
    for k in pairs.keys():
        img = pygame.image.load(k).convert_alpha()
        img = pygame.transform.scale(img, (80, 80))
        imgs[k] = img
    return imgs

# =========================
# GAME STATE
# =========================
nivel_actual = 1

pairs = nivel1
images = cargar_imagenes(pairs)

left_items = list(pairs.keys())
right_items = list(pairs.values())

selected_left = None
selected_right = None
wrong_pair = None
wrong_time = 0
matched = []

partida_finalizada = False

# =========================
# CARTAS
# =========================
card_width = 450
card_height = 90

left_cards = []
right_cards = []

def crear_cartas():
    global left_cards, right_cards

    random.shuffle(left_items)
    random.shuffle(right_items)

    left_cards = []
    right_cards = []

    for i, item in enumerate(left_items):
        rect = pygame.Rect(50, 100 + i * 110, card_width, card_height)
        left_cards.append((rect, item))

    for i, item in enumerate(right_items):
        rect = pygame.Rect(700, 100 + i * 110, card_width, card_height)
        right_cards.append((rect, item))

crear_cartas()

# =========================
# LOOP
# =========================
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # ================= MENU =================
            if pantalla == MENU:

                if boto_teoria.collidepoint(event.pos):
                    pantalla = TEORIA

                if boto_jugar.collidepoint(event.pos):
                    pantalla = JOC

            # ================= TEORIA =================
            elif pantalla == TEORIA:

                if boto_tornar.collidepoint(event.pos):
                    pantalla = MENU

            # ================= JUEGO =================
            elif pantalla == JOC:

                if boto_menu.collidepoint(event.pos):
                    pantalla = MENU

                    matched = []
                    selected_left = None
                    selected_right = None
                    wrong_pair = None
                    nivel_actual = 1

                    pairs = nivel1
                    images = cargar_imagenes(pairs)
                    left_items = list(pairs.keys())
                    right_items = list(pairs.values())
                    crear_cartas()

                    continue

                if not partida_finalizada:

                    pos = pygame.mouse.get_pos()

                    for rect, value in left_cards:
                        if rect.collidepoint(pos):
                            if value not in matched:
                                selected_left = value

                    for rect, value in right_cards:
                        if rect.collidepoint(pos):
                            if value not in matched:
                                selected_right = value

                    if selected_left and selected_right:

                        if pairs[selected_left] == selected_right:
                            matched.append(selected_left)
                            matched.append(selected_right)
                        else:
                            wrong_pair = (selected_left, selected_right)
                            wrong_time = time.time()

                        selected_left = None
                        selected_right = None

                # ================= NIVEL CONTROL =================
                if len(matched) == len(pairs) * 2:

                    if nivel_actual == 1:
                        nivel_actual = 2

                        # PASAR NIVEL 2
                        pairs = nivel2
                        images = cargar_imagenes(pairs)
                        left_items = list(pairs.keys())
                        right_items = list(pairs.values())

                        matched = []
                        crear_cartas()

                    else:
                        pantalla = VICTORIA

                        if not partida_finalizada:
                            requests.post(
                                "https://fun.codelearn.cat/hackathon/game/finalize",
                                json={
                                    "game_id": game_id,
                                    "data": {"matched": matched},
                                    "score": 100
                                }
                            )
                            partida_finalizada = True

    # ================= MENU =================
    if pantalla == MENU:

        screen.fill(BLUE)

        titol = font.render("Llenguatge de signes (ASL)", True, BLACK)
        screen.blit(titol, titol.get_rect(center=(WIDTH//2, 150)))

        pygame.draw.rect(screen, GRAY, boto_teoria)
        pygame.draw.rect(screen, BLACK, boto_teoria, 2)

        pygame.draw.rect(screen, GRAY, boto_jugar)
        pygame.draw.rect(screen, BLACK, boto_jugar, 2)

        screen.blit(small_font.render("TEORIA", True, BLACK),
                    small_font.render("TEORIA", True, BLACK).get_rect(center=boto_teoria.center))

        screen.blit(small_font.render("JUGAR", True, BLACK),
                    small_font.render("JUGAR", True, BLACK).get_rect(center=boto_jugar.center))

    # ================= TEORIA =================
    elif pantalla == TEORIA:

        screen.fill(WHITE)

        titol = font.render("TEORIA", True, BLACK)
        screen.blit(titol, titol.get_rect(center=(WIDTH//2, 60)))

        screen.blit(teoria_img, (100, 180))

        lineas = [
            "Llengua de signes",
            "comunicació visual",
            "",
            "Aprendràs vocabulari bàsic"
        ]

        y = 180
        for l in lineas:
            screen.blit(small_font.render(l, True, BLACK), (550, y))
            y += 50

        pygame.draw.rect(screen, GRAY, boto_tornar)
        pygame.draw.rect(screen, BLACK, boto_tornar, 2)

        screen.blit(small_font.render("TORNAR", True, BLACK),
                    small_font.render("TORNAR", True, BLACK).get_rect(center=boto_tornar.center))

    # ================= JOC =================
    elif pantalla == JOC:

        screen.fill(BLUE)

        pygame.draw.rect(screen, GRAY, boto_menu)
        pygame.draw.rect(screen, BLACK, boto_menu, 2)

        screen.blit(small_font.render("MENÚ", True, BLACK),
                    small_font.render("MENÚ", True, BLACK).get_rect(center=boto_menu.center))

        for rect, value in left_cards:

            color = GRAY
            if value in matched:
                color = GREEN
            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(screen, SHADOW, rect.move(5, 5), border_radius=12)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, BLACK, rect, 2)

            img = images[value]
            screen.blit(img, img.get_rect(center=rect.center))

        for rect, value in right_cards:

            color = GRAY
            if value in matched:
                color = GREEN
            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(screen, SHADOW, rect.move(5, 5), border_radius=12)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, BLACK, rect, 2)

            txt = small_font.render(value.upper(), True, BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))

        if wrong_pair and time.time() - wrong_time > 0.7:
            wrong_pair = None

    # ================= VICTORIA =================
    elif pantalla == VICTORIA:

        screen.fill(BLUE)

        titol = font.render("HAS COMPLETAT TOTS ELS NIVELLS", True, GREEN)
        screen.blit(titol, titol.get_rect(center=(WIDTH//2, 300)))

        txt = small_font.render("Felicitats!", True, BLACK)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, 380)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()