import math
import random
import pygame

WIDTH, HEIGHT = 800, 600
GRAVITY = 0.05

class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.life = random.randint(40, 80)
        self.radius = 3
        self.color = color

    def update(self):
        self.vel.y += GRAVITY
        self.pos += self.vel
        self.life -= 1
        if self.radius > 0:
            self.radius -= 0.03

    def draw(self, surface):
        if self.life > 0 and self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), max(1, int(self.radius)))

class Firework:
    COLORS = [(255,0,0), (255,165,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (255,0,255), (255,255,255)]

    def __init__(self):
        self.pos = pygame.math.Vector2(random.randint(100, WIDTH-100), HEIGHT)
        self.vel = pygame.math.Vector2(0, random.uniform(-8, -12))
        self.color = random.choice(self.COLORS)
        self.exploded = False
        self.particles = []

    def update(self):
        if not self.exploded:
            self.vel.y += GRAVITY
            self.pos += self.vel
            if self.vel.y >= 0:
                self.exploded = True
                for _ in range(50):
                    self.particles.append(Particle(self.pos.x, self.pos.y, self.color))
        else:
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.life > 0 and p.radius > 0]

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), 3)
        else:
            for p in self.particles:
                p.draw(surface)

    def is_dead(self):
        return self.exploded and not self.particles


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Fireworks')
    clock = pygame.time.Clock()

    fireworks = []
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if random.random() < 0.02:
            fireworks.append(Firework())

        screen.fill((0, 0, 0))
        for fw in fireworks:
            fw.update()
            fw.draw(screen)
        fireworks = [fw for fw in fireworks if not fw.is_dead()]

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
