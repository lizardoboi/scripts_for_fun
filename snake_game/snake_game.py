"""
Classic Snake Game
Use WASD or Arrow Keys to move.
Press Q to quit.
"""

import random
import time
import os
import msvcrt
import threading

# Game settings
WIDTH = 40
HEIGHT = 20
INITIAL_SPEED = 0.15


class Snake:
    def __init__(self):
        self.body = [(HEIGHT // 2, WIDTH // 2)]
        self.direction = (0, 1)  # Start moving right
        self.grow = False

    def head(self):
        return self.body[0]

    def move(self):
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
            self.direction = direction

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
        self.last_key = None
        self.running = True

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

        print("╔" + "═" * (WIDTH - 2) + "╗")
        print("║" + "        SNAKE GAME        ".center(WIDTH - 2) + "║")
        print("╠" + "═" * (WIDTH - 2) + "╣")

        for y in range(HEIGHT):
            row = ""
            for x in range(WIDTH):
                if y == 0 or y == HEIGHT - 1:
                    row += "═"
                elif x == 0 or x == WIDTH - 1:
                    row += "║"
                elif (y, x) == self.snake.head():
                    row += "O"
                elif (y, x) in self.snake.body:
                    row += "o"
                elif (y, x) == self.food:
                    row += "*"
                else:
                    row += " "
            if y == 0:
                print("╠" + row[1:-1] + "╣")
            elif y == HEIGHT - 1:
                print("╠" + row[1:-1] + "╣")
            else:
                print(row)

        print("╠" + "═" * (WIDTH - 2) + "╣")
        print(f"║  SCORE: {self.score:<8}  SPEED: {10 - int(self.speed * 50):<8}    ║")
        print("╚" + "═" * (WIDTH - 2) + "╝")
        print("\n  [WASD / Arrows] Move   [Q] Quit")

    def draw_game_over(self):
        self.clear_screen()
        print(r"""
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║      ___   __   __ __  ___           ║
    ║     / _ \ / /  |  V  || __|          ║
    ║    | (_| || /\ | \_/ || _|           ║
    ║     \__  ||__| |_| |_||___|          ║
    ║        |_|                           ║
    ║      __   _  _ ___  ___              ║
    ║     /__\ | || | __|| _ \             ║
    ║    | \/ || \/ | _| |   /             ║
    ║     \__/  \__/|___||_\_\             ║
    ║                                       ║
    ╠═══════════════════════════════════════╣""")
        print(f"    ║         FINAL SCORE: {self.score:<5}           ║")
        print(r"""    ╠═══════════════════════════════════════╣
    ║                                       ║
    ║    [ENTER] Play Again    [Q] Quit     ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    """)

    def input_thread(self):
        while self.running:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                # Handle arrow keys (they come as two bytes)
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H':
                        self.last_key = 'w'
                    elif key == b'P':
                        self.last_key = 's'
                    elif key == b'K':
                        self.last_key = 'a'
                    elif key == b'M':
                        self.last_key = 'd'
                else:
                    try:
                        self.last_key = key.decode().lower()
                    except:
                        pass
            time.sleep(0.01)

    def process_input(self):
        if self.last_key == 'w':
            self.snake.set_direction((-1, 0))
        elif self.last_key == 's':
            self.snake.set_direction((1, 0))
        elif self.last_key == 'a':
            self.snake.set_direction((0, -1))
        elif self.last_key == 'd':
            self.snake.set_direction((0, 1))
        elif self.last_key == 'q':
            self.game_over = True
            self.running = False

    def update(self):
        self.process_input()
        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True
            return

        if self.snake.head() == self.food:
            self.snake.grow = True
            self.score += 10
            self.spawn_food()
            # Speed up slightly
            self.speed = max(0.05, self.speed - 0.005)

    def run(self):
        input_thread = threading.Thread(target=self.input_thread, daemon=True)
        input_thread.start()

        while not self.game_over:
            self.draw()
            self.update()
            time.sleep(self.speed)

        self.draw_game_over()

        # Wait for restart or quit
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    k = key.decode().lower()
                    if k == 'q':
                        self.running = False
                        return False
                    elif k == '\r':  # Enter key
                        return True
                except:
                    if key == b'\r':
                        return True


def main():
    while True:
        game = Game()
        if not game.run():
            break
    print("\n  Thanks for playing!")


if __name__ == "__main__":
    main()
