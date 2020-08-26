from enum import Enum
from random import randrange
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Snake:
    def __init__(self, x_position, y_position) -> None:
        self.size = 10
        self.length = 1
        self.body = [[x_position, y_position]]
        self.x_position = x_position
        self.y_position = y_position

    def draw(self, game_display):
        pygame.draw.rect(game_display, RED,
                         (self.x_position, self.y_position,
                          self.size, self.size))

        for part in self.body[:-1]:
            pygame.draw.rect(game_display, BLUE,(part[0], part[1], self.size, self.size))

    def move(self, direction):
        if direction == Direction.LEFT:
            self.x_position -= 10
        if direction == Direction.RIGHT:
            self.x_position += 10
        if direction == Direction.UP:
            self.y_position -= 10
        if direction == Direction.DOWN:
            self.y_position += 10

    def get_head(self):
        return [self.x_position, self.y_position]

    def get_rect(self, game_display):
        return pygame.Rect(game_display, (self.x_position, self.y_position))


class Food:
    def __init__(self, width, height) -> None:
        self.size = 10
        self.x_position = 0
        self.y_position = 0
        self.randomize(width, height)
    
    def randomize(self, width, height):
        self.x_position = round(randrange(0, width - self.size) / 10.0) * 10
        self.y_position = round(randrange(0, height - self.size) / 10.0) * 10

    def draw(self, game_display, color=WHITE):
        pygame.draw.rect(game_display, color, (self.x_position, self.y_position, self.size, self.size))
        
    def get_position(self):
        return [self.x_position, self.y_position]

    def get_rect(self, game_display):
        return pygame.Rect(game_display, (self.x_position, self.y_position))


class Display:
    direction: Direction
    pygame.init()

    def __init__(self, width, height, snake: Snake):
        self.width = width
        self.height = height
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.snake = snake
        
        self.food = Food(self.width, self.height)
        self.direction: Direction = Direction.RIGHT
        pygame.display.set_caption('Snake')

    def draw_score(self):
        text = pygame.font.SysFont(None, 24)
        text_render = text.render(f"Score: {self.snake.length - 1}", True, WHITE)
        self.gameDisplay.blit(text_render, (20, 20))

    def clear_display(self):
        self.gameDisplay.fill((0, 0, 0))

    def movement(self, key):
        if (key == pygame.K_LEFT or key == pygame.K_a) and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if (key == pygame.K_RIGHT or key == pygame.K_d) and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        if (key == pygame.K_UP or key == pygame.K_w) and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if (key == pygame.K_DOWN or key == pygame.K_s) and self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def food_snake_collision(self):
        """
        Adds to the snake body and pops if the snake is not colliding with the food
        """
        self.snake.body.insert(0, [self.snake.x_position, self.snake.y_position])
        if self.food.get_position() == self.snake.get_head():
            self.snake.length += 1
            self.food.randomize(self.width, self.height)
        else:
            self.snake.body.pop()

    def game_over(self) -> bool:
        if [self.snake.x_position, self.snake.y_position] in self.snake.body[1:]:
            return True
        return False

    def boundaries_transform(self):
        x, y = self.snake.get_head()[0], self.snake.get_head()[1]
        if x < 0:
            self.snake.x_position = self.width
        if x > self.width:
            self.snake.x_position = 0 - self.snake.size
        if y < 0:
            self.snake.y_position = self.height
        if y > self.height - 10:
            self.snake.y_position = 0 - self.snake.size

    def render(self):
        self.snake.move(self.direction)
        self.snake.draw(self.gameDisplay)
        self.food.draw(self.gameDisplay)

        self.boundaries_transform()
        self.food_snake_collision()
        self.draw_score()
        pygame.display.update()

    def update(self):
        fps = 20
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    self.movement(event.key)

            self.render()
            self.clear_display()

            if self.game_over():
                break

            clock.tick(fps)


if __name__ == "__main__":
    s_width = 600
    s_height = 600

    game_snake = Snake(s_width // 2, s_height // 2)
    display = Display(s_width, s_height, game_snake)
    display.update()


