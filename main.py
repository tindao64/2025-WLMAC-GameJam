# Example file showing a circle moving on screen
import pygame
from screen import Screen

# pygame setup
pygame.init()
screen = Screen(pygame.display.set_mode((300, 600)))

background = pygame.Surface(screen.screen.get_size())
background = background.convert()
background.fill("green")

player_pos = screen.screen.get_width() // 2
dt = 0.0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((143, 183, 247))
        self.rect = self.surf.get_rect(center = center)
    
    def up(self):
        self.rect = self.rect.move(0, dt * -200)

bullets = pygame.sprite.Group()

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.stop()
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_SPACE:
                    bullets.add(Bullet((player_pos, 550)))

    screen.screen.blit(background, (0, 0))

    pygame.draw.circle(screen.screen, "red", (player_pos, screen.screen.get_height() - 40), 40)

    for bullet in bullets:
        screen.screen.blit(bullet.surf, bullet.rect)
        bullet.up()
        if (bullet.rect.bottom < 0):
            bullet.kill()
    
    print(len(bullets))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos = max(40, player_pos - 300 * dt)
    if keys[pygame.K_d]:
        player_pos = min(260, player_pos + 300 * dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = screen.clock.tick(60) / 1000

pygame.quit()
