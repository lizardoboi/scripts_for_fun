"""
Cool Skeleton
A detailed ASCII skeleton smoking a cigar.
Press Q to quit.
"""

import os
import time
import random
import msvcrt

WIDTH = 80
HEIGHT = 35


class Smoke:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.max_age = random.randint(15, 25)
        self.drift = random.choice([-1, 0, 0, 1])
        self.chars = ['░', '▒', '▓', '█', '▓', '▒', '░', '.', '\'', ' ']

    def update(self):
        self.age += 1
        self.y -= 1
        if random.random() < 0.3:
            self.x += self.drift
        if random.random() < 0.1:
            self.drift = random.choice([-1, 0, 1])

    def get_char(self):
        idx = min(int(self.age / self.max_age * len(self.chars)), len(self.chars) - 1)
        return self.chars[idx]

    def is_dead(self):
        return self.age >= self.max_age or self.y < 0


class Animation:
    def __init__(self):
        self.frame = 0
        self.smoke_particles = []
        self.cigar_glow = 0
        self.blink = False
        self.exhale = 0
        self.exhale_timer = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_skeleton_frame(self):
        # Cigar glow animation
        glow_chars = ['@', '*', 'O', '*']
        glow = glow_chars[self.cigar_glow % len(glow_chars)]

        # Eye animation (occasional blink)
        eye_l = "█" if not self.blink else "─"
        eye_r = "█" if not self.blink else "─"

        # Exhale animation - puff of smoke from mouth
        if self.exhale > 0:
            mouth = "═══○"
            exhale_smoke = "░▒▓" + "░" * (self.exhale // 2)
        else:
            mouth = "═══"
            exhale_smoke = ""

        skeleton = f"""
                                    ░░░░░░░░░░░░░
                                 ░░░▒▒▒▒▒▒▒▒▒▒▒░░░
                               ░░▒▒▓▓▓▓▓▓▓▓▓▓▓▒▒░░
                              ░▒▓██████████████▓▒░
                             ░▒▓████████████████▓▒░
                            ░▒▓██████████████████▓▒░
                            ░▒▓██████████████████▓▒░
                            ░▒▓████▓▓▓████▓▓▓████▓▒░
                            ░▒▓███▓{eye_l}▓▓██▓▓{eye_r}▓███▓▒░
                            ░▒▓████▓▓▓████▓▓▓████▓▒░
                            ░▒▓██████████████████▓▒░
                             ░▒▓████████████████▓▒░
                              ░▒▓██▓▓▓▓▓▓▓▓▓▓██▓▒░
                               ░▒▓██████████▓▓▒░     {exhale_smoke}
                                ░░▒▓▓{mouth}▓▓▒░░═══════{glow}
                                  ░░▒▒▒▒▒▒▒▒░░
                                   ░░░░░░░░░░
                                    ┌──┴──┐
                                    │     │
                               ╔════╧═════╧════╗
                               ║               ║
                               ║   ▄▄▄▄▄▄▄▄▄   ║
                              ╔╝  ░░░░░░░░░░░  ╚╗
                              ║  ░▒▒▒▒▒▒▒▒▒▒░  ║
                             ╔╝  ░▒▓▓▓▓▓▓▓▓▒░  ╚╗
                             ║   ░▒▓██████▓▒░   ║
                            ╔╝   ░▒▓██████▓▒░   ╚╗
                            ║    ░▒▓██████▓▒░    ║
                           ╔╝    ░▒▓▓▓▓▓▓▓▓▒░    ╚╗
                           ║     ░▒▒▒▒▒▒▒▒▒▒░     ║
                           ║      ░░░░░░░░░░      ║
                          ╔╝                      ╚╗
                          ║    ▄▄▄▄▄    ▄▄▄▄▄     ║
                         ╔╝   █░░░░█    █░░░░█    ╚╗
                         ║    █░▓▓░█    █░▓▓░█     ║
                         ║    █░░░░█    █░░░░█     ║
                         ║    ▀▀▀▀▀▀    ▀▀▀▀▀▀     ║
                         ╚═══╗              ╔═════╝
                             ║   ▄▄▄▄▄▄▄▄   ║
                             ║  █        █  ║
                             ╚══█   ██   █══╝
                                █   ██   █
                                █   ██   █
                                █  ████  █
                                █ ██  ██ █
                                ▀▀▀    ▀▀▀
"""
        return skeleton

    def get_alt_skeleton(self):
        """Alternative detailed view"""
        glow_chars = ['◉', '●', '◎', '●']
        glow = glow_chars[self.cigar_glow % len(glow_chars)]

        eye_l = "◉" if not self.blink else "─"
        eye_r = "◉" if not self.blink else "─"

        if self.exhale > 0:
            puff = "  " + "░" * min(self.exhale, 8) + "▒" * max(0, self.exhale - 8) // 2
        else:
            puff = ""

        skeleton = f"""

                              ██████████████████████
                           ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███
                         ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
                        █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
                       █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
                      █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
                      █▓▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓▓▓▓█
                      █▓▓▓▓▓░ {eye_l}    ░▓▓▓▓▓▓░    {eye_r} ░▓▓▓▓▓▓▓▓█
                      █▓▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓▓▓▓█
                       █▓▓▓▓▓▓▓▓▓▓▓███▓▓███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
                        █▓▓▓▓▓▓▓▓▓█   ▓▓▓   █▓▓▓▓▓▓▓▓▓▓▓▓█
                         █▓▓▓▓▓▓▓█   ▓▓▓▓▓   █▓▓▓▓▓▓▓▓▓▓█
                          ██▓▓▓▓█  ▓▓▓▓▓▓▓▓▓  █▓▓▓▓▓▓▓██{puff}
                            ██▓█ ═══════════ █▓██══════{glow}
                              ██  ▓▓▓▓▓▓▓▓▓  ██
                               █▓▓▓▓▓▓▓▓▓▓▓▓▓█
                                █▓▓▓▓▓▓▓▓▓▓▓█
                                 ██▓▓███▓▓██
                                   ██   ██
                            ████████     ████████
                           █▓▓▓▓▓▓▓█     █▓▓▓▓▓▓▓█
                          █▓░░░░░░░▓█   █▓░░░░░░░▓█
                          █▓░█████░▓█   █▓░█████░▓█
                          █▓░█   █░▓█   █▓░█   █░▓█
                          █▓░█████░▓█   █▓░█████░▓█
                          █▓░░░░░░░▓█   █▓░░░░░░░▓█
                          █▓▓▓▓▓▓▓▓▓█   █▓▓▓▓▓▓▓▓▓█
                           █████████     █████████
                              ║   ║         ║   ║
                              ║   ║         ║   ║
                            ▄▄╨▄▄▄╨▄▄     ▄▄╨▄▄▄╨▄▄
                           █ ░░░░░░░ █   █ ░░░░░░░ █
                           █░▓▓▓▓▓▓▓░█   █░▓▓▓▓▓▓▓░█
                            █████████     █████████
"""
        return skeleton

    def draw(self):
        self.clear_screen()

        print("╔" + "═" * 78 + "╗")
        print("║" + " COOL SKELETON ".center(78) + "║")
        print("╠" + "═" * 78 + "╣")

        # Get skeleton and add smoke
        skeleton_lines = self.get_alt_skeleton().split('\n')

        # Create screen buffer
        screen = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Draw skeleton to buffer
        for y, line in enumerate(skeleton_lines):
            if y < HEIGHT:
                for x, char in enumerate(line):
                    if x < WIDTH:
                        screen[y][x] = char

        # Draw smoke particles
        for smoke in self.smoke_particles:
            if 0 <= smoke.x < WIDTH and 0 <= smoke.y < HEIGHT:
                char = smoke.get_char()
                if char != ' ':
                    screen[smoke.y][smoke.x] = char

        # Render
        for row in screen:
            print("║" + "".join(row) + "║")

        print("╠" + "═" * 78 + "╣")

        # Cool quotes
        quotes = [
            "\"Death is just the beginning...\"",
            "\"I've got a bone to pick with you.\"",
            "\"Living my best afterlife.\"",
            "\"No body, no problem.\"",
            "\"Feeling bonely tonight.\"",
            "\"I find this humerus.\"",
            "\"Skull vibes only.\"",
            "\"Too cool for flesh.\"",
        ]
        quote = quotes[(self.frame // 50) % len(quotes)]
        print("║" + quote.center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        print("  Press [Q] to quit")

    def update(self):
        self.frame += 1

        # Cigar glow
        if self.frame % 8 == 0:
            self.cigar_glow += 1

        # Random blink
        if random.random() < 0.02:
            self.blink = True
        elif self.blink and random.random() < 0.3:
            self.blink = False

        # Exhale cycle
        self.exhale_timer += 1
        if self.exhale_timer > 80:
            if self.exhale == 0:
                self.exhale = 1
            elif self.exhale < 15:
                self.exhale += 1
            else:
                self.exhale = 0
                self.exhale_timer = 0

        # Spawn smoke from cigar (position adjusted for the skeleton)
        if self.frame % 3 == 0:
            # Cigar tip position
            smoke_x = 58 + random.randint(-1, 1)
            smoke_y = 13
            self.smoke_particles.append(Smoke(smoke_x, smoke_y))

        # Spawn exhale smoke
        if self.exhale > 5 and self.frame % 2 == 0:
            smoke_x = 55 + random.randint(0, self.exhale // 2)
            smoke_y = 12 + random.randint(-1, 1)
            self.smoke_particles.append(Smoke(smoke_x, smoke_y))

        # Update smoke
        for smoke in self.smoke_particles:
            smoke.update()

        # Remove dead smoke
        self.smoke_particles = [s for s in self.smoke_particles if not s.is_dead()]

    def run(self):
        while True:
            self.draw()

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

            self.update()


def main():
    anim = Animation()
    anim.run()
    print("\n  Stay cool, skeleton! 💀")


if __name__ == "__main__":
    main()
