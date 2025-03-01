import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 400
CELL_SIZE = 40
ROWS, COLS = 10, 20
FPS = 60

# Цвета
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Игровое поле
field = [[0 for _ in range(COLS)] for _ in range(ROWS)]


# Класс для игрока
class Player:
    def __init__(self):
        # Спавн в верхнем левом углу
        self.x, self.y = 0, 0
        self.trail = [(self.x, self.y)]  # След игрока

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Движение по границе
        if (0 <= new_x < COLS) and (0 <= new_y < ROWS):
            # Проверка на столкновение со следом
            if (new_x, new_y) in self.trail:
                self.trail.remove((new_x, new_y))  # Удаляем след
            self.x, self.y = new_x, new_y
            self.trail.append((self.x, self.y))

    def draw(self, surface):
        for pos in self.trail:
            pygame.draw.rect(surface, GREEN, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Класс для шарика
class Ball:
    def __init__(self):
        self.x = random.randint(1, COLS - 2)
        self.y = random.randint(1, ROWS - 2)
        self.dx = 1  # Новая скорость по X
        self.dy = 1  # Новая скорость по Y

    def move(self, player_trail):
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        # Проверка на столкновение с границами
        if new_x < 0 or new_x >= COLS:
            self.dx *= -1  # Отскок от правой и левой границы
        if new_y < 0 or new_y >= ROWS:
            self.dy *= -1  # Отскок от верхней и нижней границы

        # Проверка на столкновение со следом игрока
        if (new_x, new_y) in player_trail:
            self.dx *= -1  # Изменение направления движения по X
            self.dy *= -1  # Изменение направления движения по Y

        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 2)


# Основная функция игры
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ball and Player Game")
    clock = pygame.time.Clock()

    player = Player()
    ball = Ball()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)

        ball.move(player.trail)

        screen.fill(WHITE)
        player.draw(screen)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()