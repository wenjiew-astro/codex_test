import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
GRAVITY = 0.05
FPS = 60


class Particle:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        self.vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.color = color
        self.lifetime = random.randint(40, 60)
        self.age = 0

    @property
    def alive(self):
        return self.age < self.lifetime

    def update(self):
        self.vel.y += GRAVITY
        self.pos += self.vel
        self.age += 1

    def draw(self, surface):
        if not self.alive:
            return
        alpha = max(255 * (1 - self.age / self.lifetime), 0)
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        surface.blit(s, self.pos)


class Firework:
    def __init__(self, x):
        self.pos = pygame.Vector2(x, HEIGHT)
        self.vel = pygame.Vector2(0, random.uniform(-8, -6))
        self.color = random.choice(
            [
                (255, 0, 0),
                (255, 165, 0),
                (255, 255, 255),
                (0, 128, 255),
                (0, 255, 127),
            ]
        )
        self.exploded = False
        self.particles = []

    @property
    def alive(self):
        return (not self.exploded) or len(self.particles) > 0

    def update(self):
        if not self.exploded:
            self.vel.y += GRAVITY
            self.pos += self.vel
            if self.vel.y >= 0:
                self.exploded = True
                for _ in range(random.randint(40, 60)):
                    self.particles.append(Particle(self.pos.x, self.pos.y, self.color))
        else:
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(
                surface, self.color, (int(self.pos.x), int(self.pos.y)), 3
            )
        else:
            for p in self.particles:
                p.draw(surface)


def create_firework(x=None):
    if x is None:
        x = random.randint(100, WIDTH - 100)
    return Firework(x)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fireworks")
    clock = pygame.time.Clock()

    fireworks = [create_firework()]
    spawn_timer = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                fireworks.append(create_firework())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                fireworks.append(create_firework(mx))

        screen.fill((0, 0, 0))

        for fw in fireworks:
            fw.update()
            fw.draw(screen)
        fireworks = [fw for fw in fireworks if fw.alive]

        spawn_timer += 1
        if spawn_timer > FPS * 2:
            spawn_timer = 0
            fireworks.append(create_firework())

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
