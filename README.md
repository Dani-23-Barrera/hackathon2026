import requests
import pygame

resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
dades = resposta.json()

# Iniciar pygame
pygame.init()

# Crear ventana
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi primer juego")

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# Posición del cuadrado
x = 100
y = 100
velocidad = 5

# FPS
clock = pygame.time.Clock()

# Bucle principal
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

    # Dibujar fondo
    pantalla.fill(BLANCO)

    # Dibujar cuadrado
    pygame.draw.rect(pantalla, AZUL, (x, y, 50, 50))

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar FPS
    clock.tick(60)
