"""
Fishing Screensaver
A peaceful ASCII art fishing animation.
Press Q to quit.
"""

import os
import time
import random
import msvcrt

WIDTH = 80
HEIGHT = 24

# Fish types swimming left
FISH_LEFT = [
    "><>",
    "><))'>",
    "><)))°>",
    "<><",
    "}(°><",
    "°<))))><",
    "><##'>",
]

# Fish types swimming right
FISH_RIGHT = [
    "<><",
    "<'((<>",
    "<°(((<>",
    "><>",
    "<>°{(",
    "<>((((°",
    "<'##><",
]

# Bubbles
BUBBLES = ["°", "o", "O", "0"]


class Fish:
    def __init__(self):
        self.going_left = random.choice([True, False])
        if self.going_left:
            self.shape = random.choice(FISH_LEFT)
            self.x = WIDTH + random.randint(0, 20)
        else:
            self.shape = random.choice(FISH_RIGHT)
            self.x = -len(self.shape) - random.randint(0, 20)
        self.y = random.randint(14, HEIGHT - 2)
        self.speed = random.uniform(0.3, 1.0)
        self.move_acc = 0

    def move(self, dt):
        self.move_acc += dt
        if self.move_acc >= self.speed:
            self.move_acc = 0
            if self.going_left:
                self.x -= 1
            else:
                self.x += 1

    def is_offscreen(self):
        if self.going_left:
            return self.x < -len(self.shape)
        else:
            return self.x > WIDTH


class Bubble:
    def __init__(self, x, y):
        self.x = x + random.randint(-1, 1)
        self.y = y
        self.char = random.choice(BUBBLES)
        self.speed = random.uniform(0.1, 0.3)
        self.move_acc = 0

    def move(self, dt):
        self.move_acc += dt
        if self.move_acc >= self.speed:
            self.move_acc = 0
            self.y -= 1
            self.x += random.randint(-1, 1)

    def is_offscreen(self):
        return self.y < 12  # Water surface


class Scene:
    def __init__(self):
        self.fishes = []
        self.bubbles = []
        self.frame = 0
        self.rod_frame = 0
        self.wave_offset = 0
        self.bird_x = -10
        self.bird_frame = 0
        self.catch_anim = 0
        self.spawn_initial_fish()

    def spawn_initial_fish(self):
        for _ in range(5):
            fish = Fish()
            fish.x = random.randint(0, WIDTH)
            self.fishes.append(fish)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_boat_and_fisher(self):
        # Fishing rod animation
        rod_positions = [
            [
                "       \\O/        ",
                "    ____I____     ",
                "   /  __|__  \\   ",
                "   \\_________/   ",
            ],
            [
                "       \\O_        ",
                "    ____I___\\_   ",
                "   /  __|__  \\   ",
                "   \\_________/   ",
            ],
            [
                "       \\O__       ",
                "    ____I____\\   ",
                "   /  __|__  \\   ",
                "   \\_________/   ",
            ],
        ]

        if self.catch_anim > 0:
            return [
                "       \\O/  !     ",
                "    ____I___/    ",
                "   /  __|__  \\   ",
                "   \\_________/   ",
            ]

        return rod_positions[self.rod_frame % 3]

    def get_fishing_line(self):
        lines = []
        if self.catch_anim > 0:
            line_art = [
                "                    |",
                "                    |",
                "                   <*>",
            ]
        else:
            line_patterns = [
                ["                     \\", "                      \\", "                       J"],
                ["                     |", "                      \\", "                       J"],
                ["                     |", "                     |", "                       J"],
            ]
            line_art = line_patterns[self.rod_frame % 3]
        return line_art

    def get_waves(self):
        wave1 = "~" * WIDTH
        wave2 = "~~~" + "≈~≈~" * ((WIDTH - 6) // 4) + "~~~"

        # Animate waves
        offset = self.wave_offset % 4
        wave1 = wave1[offset:] + wave1[:offset]
        wave2 = wave2[-offset:] + wave2[:-offset] if offset > 0 else wave2

        return [wave1, wave2]

    def get_bird(self):
        bird_frames = [
            ["  v  ", " \\   /", ""],
            ["     ", "  v  ", " / \\ "],
            ["     ", " < > ", ""],
        ]
        return bird_frames[self.bird_frame % 3]

    def draw(self):
        self.clear_screen()
        screen = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Sky gradient (top area)
        sky_chars = ['.', '*', '.', ' ', ' ']
        for y in range(5):
            if random.random() < 0.02:
                x = random.randint(0, WIDTH - 1)
                screen[y][x] = random.choice(['*', '.', '+'])

        # Draw bird
        bird = self.get_bird()
        bird_y = 2
        for i, line in enumerate(bird):
            for j, char in enumerate(line):
                bx = int(self.bird_x) + j
                by = bird_y + i
                if 0 <= bx < WIDTH and char != ' ':
                    screen[by][bx] = char

        # Draw sun
        sun = [
            "  \\ | /  ",
            " - ( ) - ",
            "  / | \\  ",
        ]
        sun_x = 5
        sun_y = 1
        for i, line in enumerate(sun):
            for j, char in enumerate(line):
                sx = sun_x + j
                sy = sun_y + i
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT and char != ' ':
                    screen[sy][sx] = char

        # Draw boat and fisher
        boat = self.get_boat_and_fisher()
        boat_x = 30
        boat_y = 7
        for i, line in enumerate(boat):
            for j, char in enumerate(line):
                bx = boat_x + j
                by = boat_y + i
                if 0 <= bx < WIDTH and char != ' ':
                    screen[by][bx] = char

        # Draw fishing line
        line = self.get_fishing_line()
        line_x = 45
        line_y = 10
        for i, row in enumerate(line):
            for j, char in enumerate(row):
                lx = line_x + j - 20
                ly = line_y + i
                if 0 <= lx < WIDTH and ly < HEIGHT and char != ' ':
                    screen[ly][lx] = char

        # Draw water surface (waves)
        waves = self.get_waves()
        water_start = 11
        for i, wave in enumerate(waves):
            for j, char in enumerate(wave[:WIDTH]):
                screen[water_start + i][j] = char

        # Draw underwater area (darker)
        for y in range(water_start + 2, HEIGHT):
            for x in range(WIDTH):
                if screen[y][x] == ' ':
                    if random.random() < 0.01:
                        screen[y][x] = '~'

        # Draw fish
        for fish in self.fishes:
            for i, char in enumerate(fish.shape):
                fx = fish.x + i
                if 0 <= fx < WIDTH and 0 <= fish.y < HEIGHT:
                    screen[fish.y][fx] = char

        # Draw bubbles
        for bubble in self.bubbles:
            if 0 <= bubble.x < WIDTH and 0 <= bubble.y < HEIGHT:
                screen[bubble.y][bubble.x] = bubble.char

        # Draw seabed
        seabed = "_.~._" * (WIDTH // 5 + 1)
        for i, char in enumerate(seabed[:WIDTH]):
            screen[HEIGHT - 1][i] = char

        # Seaweed
        seaweed_positions = [10, 25, 55, 70]
        seaweed_frames = [
            [")", "(", ")", "|"],
            ["(", ")", "(", "|"],
        ]
        sw_frame = seaweed_frames[self.frame % 2]
        for sx in seaweed_positions:
            for i, char in enumerate(sw_frame):
                sy = HEIGHT - 2 - i
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    screen[sy][sx] = char

        # Render
        print("+" + "-" * WIDTH + "+")
        for row in screen:
            print("|" + "".join(row) + "|")
        print("+" + "-" * WIDTH + "+")
        print("  Press [Q] to quit - Relax and watch the fish...")

    def update(self, dt):
        self.frame += 1

        # Update rod animation
        if self.frame % 15 == 0:
            self.rod_frame += 1

        # Update wave animation
        if self.frame % 5 == 0:
            self.wave_offset += 1

        # Update bird
        self.bird_x += 0.3
        if self.bird_x > WIDTH + 10:
            self.bird_x = -10
        if self.frame % 8 == 0:
            self.bird_frame += 1

        # Random catch animation
        if self.catch_anim > 0:
            self.catch_anim -= 1
        elif random.random() < 0.003:
            self.catch_anim = 20

        # Update fish
        for fish in self.fishes:
            fish.move(dt)

        # Remove offscreen fish
        self.fishes = [f for f in self.fishes if not f.is_offscreen()]

        # Spawn new fish
        if len(self.fishes) < 8 and random.random() < 0.05:
            self.fishes.append(Fish())

        # Update bubbles
        for bubble in self.bubbles:
            bubble.move(dt)

        # Remove offscreen bubbles
        self.bubbles = [b for b in self.bubbles if not b.is_offscreen()]

        # Spawn bubbles from fish
        if random.random() < 0.1 and self.fishes:
            fish = random.choice(self.fishes)
            if 0 <= fish.x < WIDTH:
                self.bubbles.append(Bubble(fish.x, fish.y - 1))

    def run(self):
        while True:
            self.draw()

            # Check for quit
            start = time.time()
            while time.time() - start < 0.1:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    try:
                        if key.decode().lower() == 'q':
                            return
                    except:
                        pass
                time.sleep(0.01)

            self.update(0.1)


def main():
    scene = Scene()
    scene.run()
    print("\n  Gone fishing... goodbye!")


if __name__ == "__main__":
    main()
