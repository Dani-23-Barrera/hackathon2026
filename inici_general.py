import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aprèn les vocals japoneses")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (210,220,235)
GRAY = (230,230,230)

font = pygame.font.SysFont("arial", 60)
small_font = pygame.font.SysFont("arial", 35)

# ESTATS
MENU = 0
TEORIA = 1
JOC = 2

pantalla = MENU

# BOTONS
boto_teoria = pygame.Rect(450, 280, 300, 80)
boto_jugar = pygame.Rect(450, 400, 300, 80)
boto_tornar = pygame.Rect(30, 30, 180, 60)

clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # MENÚ
            if pantalla == MENU:

                if boto_teoria.collidepoint(event.pos):
                    pantalla = TEORIA

                if boto_jugar.collidepoint(event.pos):
                    pantalla = JOC

            # TEORIA
            elif pantalla == TEORIA:

                if boto_tornar.collidepoint(event.pos):
                    pantalla = MENU

    # ---------------- MENU ----------------

    if pantalla == MENU:

        screen.fill(BLUE)

        titol = font.render(
            "VOCALS JAPONESES",
            True,
            BLACK
        )

        screen.blit(
            titol,
            titol.get_rect(center=(WIDTH//2,150))
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

    # ---------------- TEORIA ----------------

    elif pantalla == TEORIA:

        screen.fill(WHITE)

        titol = font.render(
            "TEORIA",
            True,
            BLACK
        )

        screen.blit(titol, (500, 50))

        linies = [
            "Les vocals japoneses són:",
            "",
            "あ = A",
            "い = I",
            "う = U",
            "え = E",
            "お = O",
            "",
            "Memoritza-les abans de jugar."
        ]

        y = 180

        for linea in linies:
            txt = small_font.render(linea, True, BLACK)
            screen.blit(txt, (150, y))
            y += 50

        pygame.draw.rect(screen, GRAY, boto_tornar)
        pygame.draw.rect(screen, BLACK, boto_tornar, 2)

        txt = small_font.render("TORNAR", True, BLACK)
        screen.blit(
            txt,
            txt.get_rect(center=boto_tornar.center)
        )

    # ---------------- JOC ----------------

    elif pantalla == JOC:

        # AQUÍ HAS D'ENGANXAR TOT EL TEU CODI DEL JOC
        # (des de pairs = {...} fins al final)

        screen.fill((210,220,235))

        txt = font.render(
            "POSA AQUÍ EL TEU JOC",
            True,
            BLACK
        )

        screen.blit(
            txt,
            txt.get_rect(center=(WIDTH//2, HEIGHT//2))
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()