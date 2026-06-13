import pygame
import random

pygame.init()

# Pantalla
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atrapa la vocal")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (220, 235, 255)
RED = (255, 100, 100)

# Fonts
font = pygame.font.SysFont("arial", 100)
small_font = pygame.font.SysFont("arial", 40)

# Imatges
letters = ["a", "e", "i", "o", "u"]

images = {
    "a": pygame.transform.scale(
        pygame.image.load("A.png").convert_alpha(), (120, 120)
    ),
    "e": pygame.transform.scale(
        pygame.image.load("E.png").convert_alpha(), (120, 120)
    ),
    "i": pygame.transform.scale(
        pygame.image.load("I.png").convert_alpha(), (120, 120)
    ),
    "o": pygame.transform.scale(
        pygame.image.load("O.png").convert_alpha(), (120, 120)
    ),
    "u": pygame.transform.scale(
        pygame.image.load("U.png").convert_alpha(), (120, 120)
    )
}

# Posicions de les imatges
image_rects = {}

spacing = 160
start_x = 100

for i, letter in enumerate(letters):

    rect = pygame.Rect(
        start_x + i * spacing,
        HEIGHT - 150,
        120,
        120
    )

    image_rects[letter] = rect

# Lletra que cau
current_letter = random.choice(letters)
letter_x = random.randint(100, WIDTH - 100)
letter_y = -100

fall_speed = 2

score = 0
lives = 3

clock = pygame.time.Clock()

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            for letter, rect in image_rects.items():

                if rect.collidepoint(pos):

                    if letter == current_letter:

                        score += 1

                    else:

                        lives -= 1

                    # Nova lletra
                    current_letter = random.choice(letters)
                    letter_x = random.randint(100, WIDTH - 100)
                    letter_y = -100

    # Mou la lletra
    letter_y += fall_speed

    # Ha arribat a baix?
    if letter_y > HEIGHT - 200:

        lives -= 1

        current_letter = random.choice(letters)
        letter_x = random.randint(100, WIDTH - 100)
        letter_y = -100

    screen.fill(BLUE)

    # Dibuixar lletra
    text = font.render(current_letter.upper(), True, BLACK)
    screen.blit(text, (letter_x, letter_y))

    # Dibuixar imatges
    for letter, rect in image_rects.items():

        pygame.draw.rect(screen, WHITE, rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

        screen.blit(images[letter], rect)

    # Puntuació
    score_text = small_font.render(
        f"Punts: {score}",
        True,
        BLACK
    )
    screen.blit(score_text, (20, 20))

    # Vides
    lives_text = small_font.render(
        f"Vides: {lives}",
        True,
        RED
    )
    screen.blit(lives_text, (20, 70))

    if lives <= 0:

        game_over = font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over,
            (250, 250)
        )

        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()