from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центральная точка экрана
CENTRAL_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
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

# Цвет для объектов по умолчанию
WHITE_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:

    def __init__(self, body_color=WHITE_COLOR, position=CENTRAL_POSITION):
        self.body_color = body_color
        self.position = position

    def draw(self):
        raise NotImplementedError('This method is not implemented')


class Apple(GameObject):

    def __init__(self, body_color=APPLE_COLOR):
        position = self.randomize_position()
        super().__init__(body_color, position)

    def randomize_position(self):
        return randint(0, 31), randint(0, 23)

    def draw(self):
        rect = (pygame.Rect((self.position[0] * GRID_SIZE,
                             self.position[1] * GRID_SIZE),
                            (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, body_color=SNAKE_COLOR, positions=[CENTRAL_POSITION]):
        super().__init__(body_color)
        self.positions = positions
        self.length = len(self.positions)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        rect = (pygame.Rect((self.get_head_position[0] * GRID_SIZE,
                            self.get_head_position[1] * GRID_SIZE),
                            (GRID_SIZE, GRID_SIZE))
                )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = (pygame.Rect((self.last[0] * GRID_SIZE,
                                      self.last[1] * GRID_SIZE),
                                     (GRID_SIZE, GRID_SIZE))
                         )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def clear(self):
        for position in self.positions:
            rect = (pygame.Rect((position[0] * GRID_SIZE,
                                 position[1] * GRID_SIZE),
                                (GRID_SIZE, GRID_SIZE))
                    )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    @property
    def get_head_position(self):
        return self.positions[0]

    @property
    def get_new_head_position(self):
        return (
            (self.get_head_position[0] + self.next_direction[0]) % GRID_WIDTH,
            (self.get_head_position[1] + self.next_direction[1]) % GRID_HEIGHT
        )

    def move(self):
        if self.get_new_head_position in self.positions:
            self.clear()
            self.reset()
        else:
            self.positions.insert(0, self.get_new_head_position)
            self.update_direction()

    def reset(self):
        self.positions = [CENTRAL_POSITION, None]
        self.direction = RIGHT


def handle_keys(game_object):
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
            else:
                return False
            game_object.move()
            return True


def main():
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        snake.draw()
        apple.draw()
        clock.tick(SPEED)
        if handle_keys(snake):
            if snake.get_head_position == apple.position:
                apple = Apple()
            else:
                snake.last = snake.positions.pop()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
