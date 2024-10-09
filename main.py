import pygame
from segment import SegmentChain

SEGMENTS_AMOUNT = 3
SEGMENTS_LENGTH = 150

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

origin = (screen.get_size()[0] / 2, screen.get_size()[1] / 2)

chain = SegmentChain(
    SEGMENTS_AMOUNT,
    SEGMENTS_LENGTH,
)

chain.attach(origin) # Remove to make a free chain
    
def game_loop():
    chain.update(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    game_loop()

    pygame.display.update()

    clock.tick(60)
