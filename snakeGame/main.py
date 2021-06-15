import random

import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SNAKE_SPEED = 3

WIDTH, HEIGHT = 400, 400

BLOCKSIZE = 20

STARTPOSX = 10 * BLOCKSIZE
STARTPOSY = 10 * BLOCKSIZE

FOOD_EVENT = pygame.USEREVENT + 1

FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_grid(snake, food, snakelist):
    SCREEN.fill(BLACK)
    for x in range(0, WIDTH, BLOCKSIZE):
        for y in range(0, HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

    pygame.draw.rect(SCREEN, RED, food)
    pygame.draw.rect(SCREEN, GREEN, snake)

    current = snakelist.head
    while current is not None:
        pygame.draw.rect(SCREEN, GREEN, current.data)
        current = current.next

    pygame.display.update()


def move_snake(snake, direction, snakelist):
    previous = snakelist.head
    current = snakelist.head.next
    while current is not None:
        old = Node(pygame.Rect(current.data.x,
                               current.data.y, BLOCKSIZE, BLOCKSIZE))
        current.data.x = previous.data.x
        current.data.y = previous.data.y
        previous = old
        current = current.next

    if direction == 0:
        snake.x += BLOCKSIZE  # right
    elif direction == 1:
        snake.y += BLOCKSIZE  # down
    elif direction == 2:
        snake.x -= BLOCKSIZE  # left
    elif direction == 3:
        snake.y -= BLOCKSIZE  # up


def generate_food():
    food_x = random.randint(0, 20) * BLOCKSIZE
    food_y = random.randint(0, 20) * BLOCKSIZE
    return pygame.Rect(food_x, food_y, BLOCKSIZE, BLOCKSIZE)


def handle_food_eat(snake, food):
    if snake.colliderect(food):
        pygame.event.post(pygame.event.Event(FOOD_EVENT))


def main():
    snake = pygame.Rect(STARTPOSX, STARTPOSY, BLOCKSIZE, BLOCKSIZE)

    snakeList = LinkedList()
    snakeList.add_list(snake)

    clock = pygame.time.Clock()
    run = True
    time_elapsed = 0

    direction = 0  # direction 0 = right, 1 = down, 2 = left, 3 = up

    food = generate_food()

    while run:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and direction != 2:
                    direction = 0
                if event.key == pygame.K_DOWN and direction != 3:
                    direction = 1
                if event.key == pygame.K_LEFT and direction != 0:
                    direction = 2
                if event.key == pygame.K_UP and direction != 1:
                    direction = 3

            if event.type == FOOD_EVENT:

                food = generate_food()
                if direction == 0:
                    snake_body = pygame.Rect(snakeList.tail.data.x - BLOCKSIZE,
                                             snakeList.tail.data.y, BLOCKSIZE, BLOCKSIZE)
                elif direction == 1:
                    snake_body = pygame.Rect(snakeList.tail.data.x,
                                             snakeList.tail.data.y - BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
                elif direction == 2:
                    snake_body = pygame.Rect(snakeList.tail.data.x + BLOCKSIZE,
                                             snakeList.tail.data.y, BLOCKSIZE, BLOCKSIZE)
                else:
                    snake_body = pygame.Rect(snakeList.tail.data.x,
                                             snakeList.tail.data.y + BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
                snakeList.add_list(snake_body)
                snakeList.print_list()

        handle_food_eat(snake, food)

        time_elapsed += dt

        if time_elapsed > 250:
            move_snake(snake, direction, snakeList)
            time_elapsed = 0

        draw_grid(snake, food, snakeList)

    pygame.quit()


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_list(self, item):
        """add an item at the end of the list"""

        if not isinstance(item, Node):
            item = Node(item)

        if self.head is None:
            self.head = item
        else:
            self.tail.next = item

        self.tail = item

        return

    def print_list(self):
        current = self.head
        count = 0
        while current is not None:
            print("node met coorinaten x: " + str(current.data.x) + " y:" + str(current.data.y))
            current = current.next
            count += 1
        print("length of the list = " + str(count))
        print("tail: " + str(self.tail))
        return


if __name__ == "__main__":
    main()
