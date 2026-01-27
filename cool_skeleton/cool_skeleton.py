"""
Cool Skeleton
A detailed ASCII skeleton smoking a cigar.
Press Q to quit.
"""

import os
import time
import random
import msvcrt

WIDTH = 70
HEIGHT = 30


class Smoke:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.age = 0
        self.max_age = random.randint(12, 20)
        self.drift = random.uniform(-0.5, 0.5)

    def update(self):
        self.age += 1
        self.y -= 0.8
        self.x += self.drift
        if random.random() < 0.2:
            self.drift = random.uniform(-0.5, 0.5)

    def get_char(self):
        progress = self.age / self.max_age
        if progress < 0.2:
            return '█'
        elif progress < 0.4:
            return '▓'
        elif progress < 0.6:
            return '▒'
        elif progress < 0.8:
            return '░'
        else:
            return '.'

    def is_dead(self):
        return self.age >= self.max_age or self.y < 0


class Animation:
    def __init__(self):
        self.frame = 0
        self.smoke_particles = []
        self.cigar_glow = 0
        self.blink_timer = 0
        self.is_blinking = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_skeleton(self):
        glow = ['*', 'o', '*', 'O'][self.cigar_glow % 4]

        eye_l = "O" if not self.is_blinking else "-"
        eye_r = "O" if not self.is_blinking else "-"

        skeleton = f"""
                         ___________
                      .-'           '-.
                    .'    .-------.    '.
                   /     /  .--.   \\     \\
                  |     |  ( {eye_l}  )   |     |
                  |     |   '--'    |     |
                  |     |  ( {eye_r}  )   |     |
                  |     |   '--'    |     |
                   \\     \\         /     /
                    '.    '-------'    .'
                      '.   .-----.   .'
                        '-|       |-'
                          | ===== |
                          |  ~~~  |====={glow}
                          '.___.-'
                             | |
                        .----' '----.
                       /             \\
                      |   .--. .--.   |
                      |  ( o )( o )   |
                      |   `--' `--'   |
                      |    |    |     |
                     /|    |    |     |\\
                    | |    |    |     | |
                    | |    |    |     | |
                    |  \\   |    |    /  |
                    |   \\  |    |   /   |
                    |====\\ |    | /=====|
                    |     \\|    |/      |
                   /|      |    |       |\\
                  | |      |    |       | |
                  | |      |    |       | |
                   \\|      |    |       |/
                    |     /|    |\\      |
                    |    | |    | |     |
                    |   _| |    | |_    |
                   /   (___|    |___)   \\
                  (                      )
                   \\    /\\      /\\     /
                    |  /  \\    /  \\   |
                    | |    |  |    |  |
                    |_|    |__|    |__|"""

        return skeleton

    def draw(self):
        self.clear_screen()

        print("+" + "=" * WIDTH + "+")
        print("|" + " COOL SKELETON ".center(WIDTH) + "|")
        print("+" + "=" * WIDTH + "+")

        skeleton = self.get_skeleton()
        lines = skeleton.split('\n')

        # Pad lines and add smoke
        output_lines = []
        for i, line in enumerate(lines):
            padded = line.ljust(WIDTH)[:WIDTH]
            output_lines.append(list(padded))

        # Draw smoke on top of skeleton
        for smoke in self.smoke_particles:
            sx = int(smoke.x)
            sy = int(smoke.y)
            if 0 <= sy < len(output_lines) and 0 <= sx < WIDTH:
                char = smoke.get_char()
                output_lines[sy][sx] = char

        for line in output_lines:
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
        quote = quotes[(self.frame // 40) % len(quotes)]
        print("|" + f'"{quote}"'.center(WIDTH) + "|")
        print("+" + "=" * WIDTH + "+")
        print("  [Q] Quit")

    def update(self):
        self.frame += 1

        # Cigar glow
        if self.frame % 6 == 0:
            self.cigar_glow += 1

        # Blinking
        self.blink_timer += 1
        if self.blink_timer > 50 and not self.is_blinking:
            if random.random() < 0.1:
                self.is_blinking = True
                self.blink_timer = 0
        if self.is_blinking and self.blink_timer > 3:
            self.is_blinking = False
            self.blink_timer = 0

        # Spawn smoke from cigar tip
        if self.frame % 4 == 0:
            self.smoke_particles.append(Smoke(47, 14))

        # Update smoke
        for smoke in self.smoke_particles:
            smoke.update()

        # Remove dead smoke - limit max particles to prevent issues
        self.smoke_particles = [s for s in self.smoke_particles if not s.is_dead()]
        if len(self.smoke_particles) > 50:
            self.smoke_particles = self.smoke_particles[-50:]

    def run(self):
        # Clear input buffer
        while msvcrt.kbhit():
            msvcrt.getch()

        try:
            while True:
                self.draw()
                self.update()

                # Input check with timing
                start = time.time()
                while time.time() - start < 0.12:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        try:
                            if key.decode().lower() == 'q':
                                return
                        except:
                            pass
                    time.sleep(0.02)
        except KeyboardInterrupt:
            pass


def main():
    anim = Animation()
    anim.run()
    print("\n  Stay cool, skeleton!")


if __name__ == "__main__":
    main()
