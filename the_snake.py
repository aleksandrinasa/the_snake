from random import choice, randint

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_0 = 0
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTRAL_POSITION = (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2 - 1)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

STONE_COLOR = (255, 255, 0)

WHITE_COLOR = (255, 255, 255)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов"""

    def __init__(self, body_color=WHITE_COLOR, position=CENTRAL_POSITION):
        """
        Инициализация игрового объекта.
        Параметры:
        - body_color (цвет тела объекта, по умолчанию белый)
        - position (позиция объекта, по умолчанию центральная)
        """
        self.body_color = body_color
        self.position = position

    def draw(self):
        """
        Метод отрисовки объекта.
        Должен быть определен в подклассе.
        """
        raise NotImplementedError(
            f"This method is not defined in class {self.__class__}")

    def clear(self):
        """Метод очистки позиций объектов с экрана."""
        for position in self.positions:
            rect = (pg.Rect((position[0] * GRID_SIZE,
                            position[1] * GRID_SIZE),
                            (GRID_SIZE, GRID_SIZE))
                    )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.positions = []


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def randomize_position(self, occupied_positions):
        """
        Метод для случайного определения позиции яблока на игровом экране.
        Параметры:
        - occupied_positions (координаты, занятые змейкой)
        Возвращает:
        - позиция (tuple) - Случайная координата в пределах игрового поля при
        условии, что оно не занято другими объектами.
        """
        while True:
            supposed_position = randint(
                GRID_0, GRID_WIDTH - 1), randint(GRID_0, GRID_HEIGHT - 1)
            if supposed_position not in occupied_positions:
                self.position = supposed_position
                break

    def draw(self):
        """Метод отрисовки яблока."""
        rect = (pg.Rect((self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stones(GameObject):
    """Класс, представляющий группу камней в игре."""

    def __init__(self, body_color=STONE_COLOR):
        super().__init__(body_color)
        self.positions = []

    def randomize_position(self, occupied_positions):
        """
        Метод для случайного определения позиций камней на игровом экране.
        Параметры:
        - occupied_positions (координаты, занятые змейкой)
        Возвращает:
        - позиция (tuple) - Случайная координата в пределах игрового поля при
        условии, что оно не занято другими объектами.
        """
        while True:
            supposed_position = randint(
                GRID_0, GRID_WIDTH - 1), randint(GRID_0, GRID_HEIGHT - 1)
            if supposed_position not in occupied_positions + self.positions:
                self.positions.append(supposed_position)
                break

    def draw(self):
        """Метод отрисовки камней."""
        for position in self.positions:
            rect = (pg.Rect((position[0] * GRID_SIZE,
                    position[1] * GRID_SIZE),
                    (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змею в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def update_direction(self):
        """Метод для обновления направления движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод отрисовки змеи на экране с помощью pg."""
        rect = (pg.Rect((self.get_head_position[0] * GRID_SIZE,
                        self.get_head_position[1] * GRID_SIZE),
                        (GRID_SIZE, GRID_SIZE))
                )
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = (pg.Rect((self.last[0] * GRID_SIZE,
                                 self.last[1] * GRID_SIZE),
                                 (GRID_SIZE, GRID_SIZE))
                         )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self):
        """
        Метод получения текущей позиции головы змеи.
        Возвращает:
        - позиция (tuple) - Текущая координата головы змеи
        """
        return self.positions[0]

    @property
    def get_new_head_position(self):
        """
        Метод получения новой позиции головы змеи после движения.
        Возвращает:
        - позиция (tuple) - Новая координата головы змеи
        """
        return (
            (self.get_head_position[0] + self.next_direction[0]) % GRID_WIDTH,
            (self.get_head_position[1] + self.next_direction[1]) % GRID_HEIGHT
        )

    def move(self):
        """Метод перемещения змеи."""
        self.positions.insert(0, self.get_new_head_position)
        self.update_direction()

    def reset(self):
        """Метод сброса состояния змеи в начальное состояние."""
        self.positions = [CENTRAL_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """
    Обрабатывает события клавиш и обновляет направление движения объекта.
    Параметры:
    - game_object: Объект игры, у которого есть атрибут 'direction'
    и метод 'move()'.
    Возвращает:
    - True, если направление движения изменилось, иначе False.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            else:
                return False
            game_object.move()
            return True


def main():
    """
    Основная функция игры. Инициализирует pg, создает объекты змеи,
    яблока, камней и запускает основной игровой цикл.
    """
    pg.init()
    snake = Snake()
    stones = Stones()
    apple = Apple(APPLE_COLOR)
    apple.randomize_position(snake.positions)
    while True:
        snake.draw()
        apple.draw()
        stones.draw()
        clock.tick(SPEED)
        if handle_keys(snake):
            if snake.get_head_position == apple.position:
                apple.randomize_position(
                    snake.positions + stones.positions)
                snake.length += 1
                if snake.length % 3 == 0:
                    stones.randomize_position(
                        snake.positions + [apple.position])
            elif (snake.get_head_position in stones.positions
                    + snake.positions[3:]):
                snake.clear()
                snake.reset()
                stones.clear()
            else:
                snake.last = snake.positions.pop()
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
