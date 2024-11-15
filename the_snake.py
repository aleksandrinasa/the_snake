"""Импортируем модули для визуализации игры, нахождения случайного значения."""
import pygame
from random import choice, randint


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Варианты движения
STEPS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс игры."""

    def __init__(self):
        """Объявление атрибутов позции и цвета."""
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Пустой метод draw."""
        pass


class Apple(GameObject):
    """Дочерний класс для объекта игры."""

    body_color = (255, 0, 0)

    def __init__(self):
        """Переопределение атрибутов из родительского класса."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод генерирующий случайные координаты на игровом поле."""
        return ((randint(0, GRID_WIDTH) * GRID_SIZE),
                (randint(0, GRID_HEIGHT) * GRID_SIZE))

    def draw(self):
        """Метод отрисовывающий объект."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс для объекта игры."""

    def __init__(self):
        """Переропределение атрибутов родительского класса и создание новых."""
        super().__init__()
        self.positions = [(320, 240)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Метод обновления позициюи объекта."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # обновляет позицию змейки (координаты каждой секции)
    # добавляя новую голову в начало списка positions
    # и удаляя последний элемент, если длина змейки не увеличилась.
    def move(self):
        """Метод способствующий передвежению объекта по игровому полю."""
        for i in range(len(self.positions)):
            if self.next_direction == RIGHT:
                if self.positions[i][0] + GRID_SIZE > SCREEN_WIDTH:
                    result = (abs(self.positions[i][0] + GRID_SIZE
                                  - SCREEN_WIDTH), self.positions[i][1])
                else:
                    result = (self.positions[i][0] + GRID_SIZE,
                              self.positions[i][1])
            elif self.next_direction == LEFT:
                if self.positions[i][0] + GRID_SIZE < 0:
                    result = (abs(self.positions[i][0] - GRID_SIZE
                                  + SCREEN_WIDTH), self.positions[i][1])
                else:
                    result = (self.positions[i][0] - GRID_SIZE,
                              self.positions[i][1])
            elif self.next_direction == UP:
                if self.positions[i][1] - GRID_SIZE < 0:
                    result = (self.positions[i][0],
                              abs(self.positions[i][1]
                                  - GRID_SIZE + SCREEN_HEIGHT))
                else:
                    result = (self.positions[i][0], self.positions[i][1]
                              - GRID_SIZE)
            elif self.next_direction == DOWN:
                if self.positions[i][1] + GRID_SIZE > SCREEN_HEIGHT:
                    result = (self.positions[i][0], self.positions[i][1]
                              + GRID_SIZE - SCREEN_HEIGHT)
                else:
                    result = (self.positions[i][0],
                              self.positions[i][1] + GRID_SIZE)
            self.positions.insert(i, result)
            if self.positions[0] != Apple().position:
                self.positions.pop()
            print(self.positions)
    def draw(self):
        """Метод отрисовывающий объект."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

            # Затирание последнего сегмента
            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращающий голову объекта."""
        return (self.positions)[0]

    def reset(self):
        """Метод возвращающий объект в исходное состояние."""
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = choice(STEPS)


def handle_keys(game_object):
    """Функция обрабатывающая нажатие клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            if game_object.positions[0] != Apple().position:
                game_object.last = game_object.positions[-1]
            game_object.move()
            game_object.update_direction()


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    running = True
    while running:

        try:
            handle_keys(snake)
        except SystemExit:
            running = False
        if apple.position in snake.positions:
            apple.randomize_position()
        if len(snake.positions) > 1:
            count = 0
            for i in range(len(snake.positions)):
                if snake.positions[i] == snake.get_head_position:
                    count += 1
            if count == 2:
                snake.reset()
        if snake.positions[0] == apple.position:
            snake.length += 1
            snake.positions.append(apple.position)
            apple.__init__()
        snake.draw()
        apple.draw()
        clock.tick(SPEED)
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
