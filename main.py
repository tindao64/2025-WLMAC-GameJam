
import pygame
from pygame.sprite import Sprite, Group
import time
import math

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

PLAYER_SPEED = SCREEN_WIDTH // 8 # pixels per second
BULLET_SPEED = SCREEN_HEIGHT // 2

PLAYER_SHOOT_COOLDOWN = 1 # second

dt = 0.0

pygame.init()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

all_sprites = Group()
bullets = Group()

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert() # `convert` converts the image format to the display's format to avoid re-converting every time drawn
background.fill("green")

class Player(Sprite):
    def __init__(self):
        super().__init__()
        dimension = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 8
        self.background = pygame.Surface((dimension, dimension)).convert()
        self.background.fill("red")
        self.surf = pygame.Surface((dimension, dimension)).convert()
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 7 // 8))
        self.last_shot_time = 0
    
    def update(self):
        self.surf.blit(self.background, (0, 0))

        degrees = min((time.time() - self.last_shot_time) / PLAYER_SHOOT_COOLDOWN, 1) * 360 + 90
        pygame.draw.arc(self.surf, "yellow", self.surf.get_rect(), math.radians(90), math.radians(degrees), min(SCREEN_WIDTH, SCREEN_HEIGHT) // 32)

    def move_left(self):
        self.rect = self.rect.move(-PLAYER_SPEED * dt, 0)
        self.rect = self.rect.clamp((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def move_right(self):
        self.rect = self.rect.move(PLAYER_SPEED * dt, 0)
        self.rect = self.rect.clamp((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def shoot(self):
        now = time.time()
        if (now < self.last_shot_time + PLAYER_SHOOT_COOLDOWN):
            return
        self.last_shot_time = now
        bullet = Bullet((self.rect.centerx, SCREEN_HEIGHT * 7 // 8))
        bullets.add(bullet)
        all_sprites.add(bullet)

class Bullet(Sprite):
    def __init__(self, center):
        super().__init__()
        dimension = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 10
        self.surf = pygame.Surface((dimension, dimension)).convert()
        self.surf.fill("blue")
        self.rect = self.surf.get_rect(center = center)
    
    def update(self):
        self.rect = self.rect.move(0, -BULLET_SPEED * dt)
        if (self.rect.bottom < 0):
            self.kill()

player = Player()
all_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    display.blit(background, (0, 0))
    for sprite in all_sprites:
        sprite.update()
        display.blit(sprite.surf, sprite.rect)
    pygame.display.flip()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_left()
    if keys[pygame.K_d]:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.shoot()
 
    pygame.display.update()
    dt = clock.tick(60) / 1000
