import pygame
import sys

pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Joc inclusiu")

clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
fuente = pygame.font.SysFont(None, 50)

# Texto menú
texto = fuente.render("Benvingut al joc educatiu", True, NEGRO)

# Botón
boton = pygame.Rect(300, 250, 200, 80)
# Estado
mostrar_menu = True

while True:

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Click en botón
        if mostrar_menu and event.type == pygame.MOUSEBUTTONDOWN:
            if boton.collidepoint(event.pos):
                mostrar_menu = False

    # MENU
    if mostrar_menu:
        pantalla.fill(BLANCO)

        pygame.draw.rect(pantalla, NEGRO, boton)

        text = fuente.render("Jugar", True, BLANCO)

        pantalla.blit(texto, (170, 100))
        pantalla.blit(text, (350, 270))

    # JUEGO
    else:
        pantalla.fill(BLANCO)

    pygame.display.flip()
    clock.tick(60)