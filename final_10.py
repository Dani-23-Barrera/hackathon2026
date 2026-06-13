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
WHITE = (245, 247, 250)
BLACK = (25, 25, 25)
BLUE = (210, 220, 235)
GRAY = (235, 235, 235)
GREEN = (90, 200, 120)
RED = (230, 90, 90)
SHADOW = (180, 180, 180)
DARK = (60, 60, 60)

# =========================
# FUENTES
# =========================
font = pygame.font.SysFont("arial", 64, bold=True)
small_font = pygame.font.SysFont("arial", 34)

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
def draw_button(rect, text, hover=False):
    color = (255, 255, 255) if hover else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=18)
    pygame.draw.rect(screen, DARK, rect, 2, border_radius=18)

    txt = small_font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))

boto_teoria = pygame.Rect(450, 280, 300, 80)
boto_jugar = pygame.Rect(450, 400, 300, 80)
boto_tornar = pygame.Rect(30, 30, 180, 60)
boto_menu = pygame.Rect(30, 30, 220, 60)

# =========================
# TEORÍA (imagen mejorada)
# =========================
teoria_img = pygame.image.load("teoria.jpeg").convert_alpha()
teoria_img = pygame.transform.smoothscale(teoria_img, (420, 320))

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
        img = pygame.transform.smoothscale(img, (90, 90))
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
card_height = 95

left_cards = []
right_cards = []

def crear_cartas():
    global left_cards, right_cards

    random.shuffle(left_items)
    random.shuffle(right_items)

    left_cards = []
    right_cards = []

    for i, item in enumerate(left_items):
        rect = pygame.Rect(60, 110 + i * 115, card_width, card_height)
        left_cards.append((rect, item))

    for i, item in enumerate(right_items):
        rect = pygame.Rect(690, 110 + i * 115, card_width, card_height)
        right_cards.append((rect, item))

crear_cartas()

# =========================
# LOOP
# =========================
running = True

while running:

    mouse = pygame.mouse.get_pos()

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

            # ================= JOC =================
            elif pantalla == JOC:

                if boto_menu.collidepoint(event.pos):
                    pantalla = MENU

                    matched.clear()
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

                    for rect, value in left_cards:
                        if rect.collidepoint(event.pos):
                            if value not in matched:
                                selected_left = value

                    for rect, value in right_cards:
                        if rect.collidepoint(event.pos):
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

                # ================= NIVEL =================
                if len(matched) == len(pairs) * 2:

                    if nivel_actual == 1:
                        nivel_actual = 2

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

        screen.fill(WHITE)

        title = font.render("LLENGUATGE DE SIGNES", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))

        draw_button(boto_teoria, "TEORIA", boto_teoria.collidepoint(mouse))
        draw_button(boto_jugar, "JUGAR", boto_jugar.collidepoint(mouse))

    # ================= TEORIA =================
    elif pantalla == TEORIA:

        screen.fill((240, 242, 245))

        panel = pygame.Rect(150, 120, 900, 450)
        pygame.draw.rect(screen, WHITE, panel, border_radius=25)
        pygame.draw.rect(screen, SHADOW, panel, 2, border_radius=25)

        title = font.render("TEORIA", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 160)))

        screen.blit(teoria_img, (220, 220))

        text = [
            "El llenguatge de signes és visual",
            "i permet comunicar-se amb gestos.",
            "",
            "Aprendràs vocabulari bàsic de forma divertida."
        ]

        y = 230
        for line in text:
            t = small_font.render(line, True, DARK)
            screen.blit(t, (650, y))
            y += 45

        draw_button(boto_tornar, "TORNAR", boto_tornar.collidepoint(mouse))

    # ================= JOC =================
    elif pantalla == JOC:

        screen.fill(BLUE)

        draw_button(boto_menu, "MENÚ", boto_menu.collidepoint(mouse))

        for rect, value in left_cards:

            color = GRAY
            if value in matched:
                color = GREEN
            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(screen, SHADOW, rect.move(5, 5), border_radius=15)
            pygame.draw.rect(screen, color, rect, border_radius=15)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)

            img = images[value]
            screen.blit(img, img.get_rect(center=rect.center))

        for rect, value in right_cards:

            color = GRAY
            if value in matched:
                color = GREEN
            if wrong_pair and value in wrong_pair:
                color = RED

            pygame.draw.rect(screen, SHADOW, rect.move(5, 5), border_radius=15)
            pygame.draw.rect(screen, color, rect, border_radius=15)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)

            txt = small_font.render(value.upper(), True, BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))

        if wrong_pair and time.time() - wrong_time > 0.7:
            wrong_pair = None

    # ================= VICTORIA =================
    elif pantalla == VICTORIA:

        screen.fill((235, 245, 255))

        panel = pygame.Rect(250, 180, 700, 340)
        pygame.draw.rect(screen, WHITE, panel, border_radius=25)
        pygame.draw.rect(screen, SHADOW, panel, 2, border_radius=25)

        title = font.render("FELICITATS!", True, GREEN)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 280)))

        text = small_font.render("Has completat tots els nivells", True, BLACK)
        screen.blit(text, text.get_rect(center=(WIDTH//2, 360)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()