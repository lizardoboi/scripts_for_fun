"""
Cool Skeleton
A simple ASCII skeleton smoking a cigar.
Press Q to quit.
"""

import os
import time
import random
import msvcrt

WIDTH = 50


class Smoke:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.age = 0
        self.max_age = random.randint(8, 14)
        self.drift = random.uniform(-0.3, 0.3)

    def update(self):
        self.age += 1
        self.y -= 1
        self.x += self.drift

    def get_char(self):
        if self.age < 3:
            return 'o'
        elif self.age < 6:
            return '.'
        else:
            return "'"

    def is_dead(self):
        return self.age >= self.max_age or self.y < 0


class Animation:
    def __init__(self):
        self.frame = 0
        self.smoke_particles = []
        self.cigar_glow = 0
        self.is_blinking = False
        self.blink_timer = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_skeleton(self):
        g = ['o', 'O', 'o', '*'][self.cigar_glow % 4]
        e = "O O" if not self.is_blinking else "- -"

        return [
            "                        ",
            "         _____          ",
            "        /     \\        ",
            f"       | {e} |        ",
            "       |   ^   |        ",
            f"        \\_===_/--====={g}",
            "           |            ",
            "       /---|---\\       ",
            "      /    |    \\      ",
            "     /   __|__   \\     ",
            "    |   /|   |\\   |    ",
            "        | | | |        ",
            "        | | | |        ",
            "        |_| |_|        ",
            "        /     \\       ",
            "       /       \\      ",
            "      |         |      ",
            "     _|         |_     ",
            "    |_|         |_|    ",
        ]

    def draw(self):
        self.clear_screen()

        print("+" + "=" * WIDTH + "+")
        print("|" + " COOL SKELETON ".center(WIDTH) + "|")
        print("+" + "=" * WIDTH + "+")

        lines = self.get_skeleton()
        output = []
        for line in lines:
            output.append(list(line.ljust(WIDTH)[:WIDTH]))

        # Draw smoke
        for smoke in self.smoke_particles:
            sx, sy = int(smoke.x), int(smoke.y)
            if 0 <= sy < len(output) and 0 <= sx < WIDTH:
                output[sy][sx] = smoke.get_char()

        for line in output:
            print("|" + "".join(line) + "|")

        print("+" + "=" * WIDTH + "+")

        quotes = [
            "Death is just the beginning...",
            "I've got a bone to pick with you.",
            "Living my best afterlife.",
            "No body, no problem.",
            "Feeling bonely tonight.",
            "I find this humerus.",
            "Skull vibes only.",
            "Too cool for flesh.",
        ]
        q = quotes[(self.frame // 40) % len(quotes)]
        print("|" + f'"{q}"'.center(WIDTH) + "|")
        print("+" + "=" * WIDTH + "+")
        print("  [Q] Quit")

    def update(self):
        self.frame += 1

        if self.frame % 5 == 0:
            self.cigar_glow += 1

        # Blink
        self.blink_timer += 1
        if not self.is_blinking and self.blink_timer > 40 and random.random() < 0.1:
            self.is_blinking = True
            self.blink_timer = 0
        if self.is_blinking and self.blink_timer > 2:
            self.is_blinking = False
            self.blink_timer = 0

        # Smoke from cigar
        if self.frame % 3 == 0:
            self.smoke_particles.append(Smoke(31, 5))

        for s in self.smoke_particles:
            s.update()

        self.smoke_particles = [s for s in self.smoke_particles if not s.is_dead()][:30]

    def run(self):
        while msvcrt.kbhit():
            msvcrt.getch()

        try:
            while True:
                self.draw()
                self.update()

                start = time.time()
                while time.time() - start < 0.15:
                    if msvcrt.kbhit():
                        if msvcrt.getch().decode().lower() == 'q':
                            return
                    time.sleep(0.02)
        except:
            pass


def main():
    Animation().run()
    print("\n  Stay cool!")


if __name__ == "__main__":
    main()
