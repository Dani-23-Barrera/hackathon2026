import pygame
import sys

pygame.init()

ANCHO = 800
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Joc inclusiu")

# Colores
BLANCO = (255, 255, 255)
A = personaje = pygame.image.load("A.jpeg")
A = personaje = pygame.transform.scale(personaje, (100, 100))
B = personaje_2 = pygame.image.load("B.jpeg")
B = personaje_2 = pygame.transform.scale(personaje_2, (100, 100))


# Posición del cuadrado
x = 100
y = 100
velocidad = 5

clock = pygame.time.Clock()

while True:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclas pulsadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_UP]:
        y -= velocidad
    if teclas[pygame.K_DOWN]:
        y += velocidad
    
    if x < 0:
        x = 0
    if x > ANCHO - 100:
        x = ANCHO - 100
    if y < 0:
        y = 0
    if y > ALTO - 100:
        y = ALTO - 100
    

    pantalla.fill((255, 255, 255))

    pantalla.blit(personaje, (x, y))
    pantalla.blit(personaje_2, (0, 0))

    

    # Actuali  pygame.display.flip()
    pygame.display.flip()
    # Limitar FPS
    clock.tick(60)