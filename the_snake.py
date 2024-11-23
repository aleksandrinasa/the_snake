"""Импортируем модули для визуализации игры, нахождения случайного значения."""
import pygame
from random import choice, randint


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Варианты движения
STEPS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

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


class Rock(GameObject):
    """Дочерний класс для объекта игры."""

    def __init__(self):
        """Определение атрибутов дочернего класса."""
        self.body_color = (78, 87, 84)
        self.positions = []

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
    
    def randomize_position(self):
        """Метод генерирующий случайные координаты на игровом поле."""
        return ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))


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
        return ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))

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
        self.positions = [((GRID_WIDTH // 2 - 1) * GRID_SIZE,
                           (GRID_HEIGHT // 2 - 1) * GRID_SIZE)]
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
        print(self.next_direction)
        """Метод способствующий передвежению объекта по игровому полю."""
        if self.next_direction == RIGHT:
            if self.positions[0][0] + GRID_SIZE > SCREEN_WIDTH - GRID_SIZE:
                result = (abs(self.positions[0][0] + GRID_SIZE
                              - SCREEN_WIDTH), self.positions[0][1])
            else:
                result = (self.positions[0][0] + GRID_SIZE,
                          self.positions[0][1])
        elif self.next_direction == LEFT:
            if self.positions[0][0] - GRID_SIZE == -GRID_SIZE:
                result = (abs(self.positions[0][0] - GRID_SIZE
                          + SCREEN_WIDTH), self.positions[0][1])
            else:
                result = (self.positions[0][0] - GRID_SIZE,
                          self.positions[0][1])
        elif self.next_direction == UP:
            if self.positions[0][1] - GRID_SIZE == -GRID_SIZE:
                result = (self.positions[0][0],
                          abs(self.positions[0][1]
                              - GRID_SIZE + SCREEN_HEIGHT))
            else:
                result = (self.positions[0][0], self.positions[0][1]
                          - GRID_SIZE)
        elif self.next_direction == DOWN:
            if self.positions[0][1] + GRID_SIZE > SCREEN_HEIGHT - GRID_SIZE:
                result = (self.positions[0][0], abs(self.positions[0][1]
                          + GRID_SIZE - SCREEN_HEIGHT))
            else:
                result = (self.positions[0][0],
                          self.positions[0][1] + GRID_SIZE)
        self.positions.insert(0, result)
        self.positions.pop()

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

    @property
    def get_head_position(self):
        """Метод возвращающий голову объекта."""
        head = self.positions[0]
        return head

    def reset(self):
        """Метод возвращающий объект в исходное состояние."""
        self.clear()
        self.length = 1
        self.positions = [((GRID_WIDTH // 2 - 1) * GRID_SIZE,
                           (GRID_HEIGHT // 2 - 1) * GRID_SIZE)]
        self.direction = choice(STEPS)
        self.next_direction = RIGHT

    def clear(self):
        """Метод очищающий поле во время столкновение объекта с самим собой."""
        for i in range(len(self.positions)):
            rect = pygame.Rect(self.positions[i], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        for i in range(len(Rock().positions)):
            rect = pygame.Rect(Rock().positions[i], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


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
            game_object.last = game_object.positions[-1]
            game_object.move()
            game_object.update_direction()
            screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    rock = Rock()
    running = True
    while running:

        try:
            handle_keys(snake)
        except SystemExit:
            running = False
        if apple.position in snake.positions:
            apple.randomize_position()
        count = 0
        for i in range(len(snake.positions)):
            if snake.positions[i] == snake.get_head_position:
                count += 1
        if count == 2:
            print(True)
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            rock.positions = []
        if snake.positions[0] == apple.position:
            if (len(snake.positions) + 1) % 4 == 0:
                rock.positions.append(rock.randomize_position())
            snake.length += 1
            snake.positions.append(snake.last)
            snake.last = None
            apple.__init__()
        snake.next_direction = snake.direction
        snake.last = snake.positions[-1]
        if snake.positions[0] in rock.positions:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            rock.positions = []
        snake.move()
        snake.draw()
        apple.draw()
        rock.draw()
        clock.tick(SPEED)
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
