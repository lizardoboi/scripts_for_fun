"""
Classic Snake Game
Use WASD or Arrow Keys to move.
Press Q to quit.
"""

import random
import time
import os
import msvcrt

# Game settings
WIDTH = 40
HEIGHT = 20
INITIAL_SPEED = 0.12


class Snake:
    def __init__(self):
        self.body = [(HEIGHT // 2, WIDTH // 2)]
        self.direction = (0, 1)  # Start moving right
        self.next_direction = (0, 1)
        self.grow = False

    def head(self):
        return self.body[0]

    def move(self):
        self.direction = self.next_direction
        head_y, head_x = self.head()
        dy, dx = self.direction
        new_head = (head_y + dy, head_x + dx)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def set_direction(self, direction):
        # Prevent reversing into self
        dy, dx = direction
        curr_dy, curr_dx = self.direction
        if (dy + curr_dy, dx + curr_dx) != (0, 0):
            self.next_direction = direction

    def check_collision(self):
        head = self.head()
        # Wall collision
        if head[0] <= 0 or head[0] >= HEIGHT - 1:
            return True
        if head[1] <= 0 or head[1] >= WIDTH - 1:
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = None
        self.score = 0
        self.game_over = False
        self.speed = INITIAL_SPEED
        self.spawn_food()

    def spawn_food(self):
        while True:
            y = random.randint(1, HEIGHT - 2)
            x = random.randint(1, WIDTH - 2)
            if (y, x) not in self.snake.body:
                self.food = (y, x)
                break

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self):
        self.clear_screen()

        print("+" + "-" * (WIDTH - 2) + "+")
        print("|" + "  SNAKE GAME  ".center(WIDTH - 2) + "|")
        print("+" + "-" * (WIDTH - 2) + "+")

        for y in range(HEIGHT):
            row = ""
            for x in range(WIDTH):
                if y == 0 or y == HEIGHT - 1:
                    row += "-"
                elif x == 0 or x == WIDTH - 1:
                    row += "|"
                elif (y, x) == self.snake.head():
                    row += "@"
                elif (y, x) in self.snake.body:
                    row += "o"
                elif (y, x) == self.food:
                    row += "*"
                else:
                    row += " "
            if y == 0 or y == HEIGHT - 1:
                print("+" + row[1:-1] + "+")
            else:
                print(row)

        print("+" + "-" * (WIDTH - 2) + "+")
        print(f"| SCORE: {self.score:<27} |")
        print("+" + "-" * (WIDTH - 2) + "+")
        print(" [WASD] Move  [Q] Quit")

    def draw_game_over(self):
        self.clear_screen()
        print(r"""
    +---------------------------------------+
    |                                       |
    |            GAME  OVER                 |
    |                                       |
    +---------------------------------------+""")
        print(f"    |         FINAL SCORE: {self.score:<5}           |")
        print(r"""    +---------------------------------------+
    |                                       |
    |    [ENTER] Play Again    [Q] Quit     |
    |                                       |
    +---------------------------------------+
    """)

    def process_input(self):
        while msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    self.snake.set_direction((-1, 0))
                elif key == b'P':
                    self.snake.set_direction((1, 0))
                elif key == b'K':
                    self.snake.set_direction((0, -1))
                elif key == b'M':
                    self.snake.set_direction((0, 1))
            else:
                try:
                    k = key.decode().lower()
                    if k == 'w':
                        self.snake.set_direction((-1, 0))
                    elif k == 's':
                        self.snake.set_direction((1, 0))
                    elif k == 'a':
                        self.snake.set_direction((0, -1))
                    elif k == 'd':
                        self.snake.set_direction((0, 1))
                    elif k == 'q':
                        self.game_over = True
                        return False
                except:
                    pass
        return True

    def update(self):
        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True
            return

        if self.snake.head() == self.food:
            self.snake.grow = True
            self.score += 10
            self.spawn_food()
            self.speed = max(0.05, self.speed - 0.005)

    def run(self):
        # Flush any pending input
        while msvcrt.kbhit():
            msvcrt.getch()

        last_move = time.time()

        while not self.game_over:
            self.draw()

            # Fast input polling loop
            while time.time() - last_move < self.speed:
                if not self.process_input():
                    return False
                time.sleep(0.01)

            last_move = time.time()
            self.update()

        self.draw_game_over()

        # Wait for restart or quit
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    k = key.decode().lower()
                    if k == 'q':
                        return False
                    elif k == '\r':
                        return True
                except:
                    if key == b'\r':
                        return True
            time.sleep(0.01)


def main():
    while True:
        game = Game()
        if not game.run():
            break
    print("\n  Thanks for playing!")


if __name__ == "__main__":
    main()
