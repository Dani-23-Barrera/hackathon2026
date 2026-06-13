import pygame
import sys

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()

fuente = pygame.font.SysFont(None, 50)

# Botón
boton = pygame.Rect(300, 250, 200, 80)

mostrar_menu = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton.collidepoint(event.pos):
                mostrar_menu = False

    if mostrar_menu:
        pantalla.fill((0, 0, 0))

        # Dibujar botón
        pygame.draw.rect(pantalla, (0, 0, 255), boton)

        # Texto del botón
        texto = fuente.render("JUGAR", True, (255, 255, 255))
        pantalla.blit(texto, (340, 270))

    else:
        # Aquí empieza el juego
        pantalla.fill((255, 255, 255))

    pygame.display.flip()
    clock.tick(60)