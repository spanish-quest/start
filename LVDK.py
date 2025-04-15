import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Load assets
background = pygame.image.load("jungle_background.jpg")
donkey_kong = pygame.image.load("monkey_pixel.png")

# Scale assets
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
donkey_kong = pygame.transform.scale(donkey_kong, (150, 150))

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong: Boulder Mayhem")

# Player setup
player_size = 40
player = pygame.Rect(100, SCREEN_HEIGHT - player_size, player_size, player_size)

# Platform setup
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
    pygame.Rect(200, SCREEN_HEIGHT - 150, 400, 20),
    pygame.Rect(100, SCREEN_HEIGHT - 250, 300, 20)
]

# Vine (ladder) setup
vines = [
    pygame.Rect(250, SCREEN_HEIGHT - 150, 20, 100),
    pygame.Rect(150, SCREEN_HEIGHT - 250, 20, 100)
]

# Campfire setup
campfires = [
    pygame.Rect(500, SCREEN_HEIGHT - 80, 40, 40)
]

# Boulder setup
boulders = []
boulder_radius = 15

# Game loop
clock = pygame.time.Clock()
player_speed = 5
jump = False
jump_height = 12
jump_count = jump_height
gravity = 0.5

def throw_boulder():
    x = 400 + random.randint(-50, 50)
    y = 100
    boulders.append({"pos": [x, y], "velocity": [random.choice([-3, 3]), 0]})

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        
    # Jumping and climbing
    if keys[pygame.K_UP]:
        if any(player.colliderect(vine) for vine in vines):
            player.y -= player_speed
        elif not jump:
            jump = True

    # Apply gravity
    if not any(player.colliderect(platform) for platform in platforms):
        player.y += gravity * 5
    else:
        jump = False

    # Jump mechanics
    if jump:
        player.y -= jump_count
        jump_count -= 1
        if jump_count < -jump_height:
            jump = False
            jump_count = jump_height

    # Boulder physics
    if random.random() < 0.02:
        throw_boulder()
    
    for boulder in boulders:
        boulder["pos"][0] += boulder["velocity"][0]
        boulder["pos"][1] += boulder["velocity"][1]
        boulder["velocity"][1] += gravity
        
        # Platform collision
        for platform in platforms:
            if pygame.Rect(boulder["pos"][0], boulder["pos"][1], 
                          boulder_radius*2, boulder_radius*2).colliderect(platform):
                boulder["velocity"][1] = 0
                boulder["pos"][1] = platform.top - boulder_radius

    # Draw everything
    screen.blit(background, (0, 0))
    
    # Draw platforms (brown logs)
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)
    
    # Draw vines (green ladders)
    for vine in vines:
        pygame.draw.rect(screen, GREEN, vine)
    
    # Draw campfires
    for fire in campfires:
        pygame.draw.rect(screen, ORANGE, fire)
    
    # Draw boulders
    for boulder in boulders:
        pygame.draw.circle(screen, (100, 100, 100), 
                          (int(boulder["pos"][0]), int(boulder["pos"][1])), 
                          boulder_radius)
    
    # Draw characters
    screen.blit(donkey_kong, (400, 50))
    pygame.draw.rect(screen, RED, player)

    pygame.display.flip()
    clock.tick(30)
