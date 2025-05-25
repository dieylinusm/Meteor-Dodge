import asyncio
import platform
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 400
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Meteor Dodge")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Player properties
player_size = 20
player_x = width // 2
player_y = height - 50
player_speed = 5

# Meteor and star properties
meteor_size = 20
star_size = 10
meteor_speed = 3
star_speed = 2
meteors = []
stars = []
spawn_rate = 0.02  # Probability of spawning per frame

# Game variables
score = 0
running = True

# Function to create a new meteor
def create_meteor():
    x = random.randint(0, width - meteor_size)
    return {'x': x, 'y': 0}

# Function to create a new star
def create_star():
    x = random.randint(0, width - star_size)
    return {'x': x, 'y': 0}

# Setup function for initialization
def setup():
    global player_x, player_y, meteors, stars, score, running
    player_x = width // 2
    player_y = height - 50
    meteors = []
    stars = []
    score = 0
    running = True
    window.fill(black)
    pygame.display.update()

# Update loop for game logic
async def update_loop():
    global player_x, player_y, meteors, stars, score, running

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed

    # Spawn meteors and stars randomly
    if random.random() < spawn_rate:
        meteors.append(create_meteor())
    if random.random() < spawn_rate / 2:
        stars.append(create_star())

    # Update meteor positions
    for meteor in meteors[:]:
        meteor['y'] += meteor_speed
        if meteor['y'] > height:
            meteors.remove(meteor)

    # Update star positions
    for star in stars[:]:
        star['y'] += star_speed
        if star['y'] > height:
            stars.remove(star)

    # Check for collisions
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for meteor in meteors[:]:
        meteor_rect = pygame.Rect(meteor['x'], meteor['y'], meteor_size, meteor_size)
        if player_rect.colliderect(meteor_rect):
            return False  # Game over on meteor collision

    for star in stars[:]:
        star_rect = pygame.Rect(star['x'], star['y'], star_size, star_size)
        if player_rect.colliderect(star_rect):
            score += 1
            stars.remove(star)

    # Draw the screen
    window.fill(black)
    pygame.draw.rect(window, white, (player_x, player_y, player_size, player_size))  # Player
    for meteor in meteors:
        pygame.draw.rect(window, red, (meteor['x'], meteor['y'], meteor_size, meteor_size))  # Meteors
    for star in stars:
        pygame.draw.circle(window, yellow, (star['x'] + star_size // 2, star['y'] + star_size // 2), star_size // 2)  # Stars
    pygame.display.set_caption(f"Meteor Dodge - Score: {score}")
    pygame.display.update()

    return True

# Main game loop
FPS = 60

async def main():
    setup()
    global running
    while running:
        running = await update_loop()
        await asyncio.sleep(1.0 / FPS)

    # Game over message
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over - Score: {score}", True, white)
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    await asyncio.sleep(2)  # Wait 2 seconds
    pygame.quit()

# Run the game based on platform
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
