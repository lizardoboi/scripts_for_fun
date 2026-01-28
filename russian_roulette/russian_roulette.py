import sys
import time
import random
import os

WHITE = "\033[97m"
RED = "\033[91m"
YELLOW = "\033[93m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def type_text(text, delay=0.03, color=WHITE):
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def dramatic_pause(seconds=1.5):
    for _ in range(int(seconds * 4)):
        sys.stdout.write(f"{DIM}.{RESET}")
        sys.stdout.flush()
        time.sleep(0.25)
    print()

REVOLVER = f"""{WHITE}
          _____
         |     |
    _____|     |_____
   /                 \\
  |    .-\"\"\"\"\"-.     |
  |   /  ({{}})   \\    |
  |  |   .---.   |   |
  |   \\       /  |   |
  |    '-...-'   |   |
   \\____     ___/   /
        |   |      /
        |   |     /
        |   |    /
        |   |   /
        |___|  /
        (___) /
         |_|/
{RESET}"""

CYLINDER = [
    f"""
    ╔═══════╗
    ║ {{0}} {{1}} {{2}} ║
    ║       ║
    ║ {{3}} {{4}} {{5}} ║
    ╚═══════╝
    """,
]

BANG = f"""{RED}{BOLD}
    ╔══════════════════════════════════════╗
    ║                                      ║
    ║    ██████╗  █████╗ ███╗   ██╗ ██████╗║
    ║    ██╔══██╗██╔══██╗████╗  ██║██╔════╝║
    ║    ██████╔╝███████║██╔██╗ ██║██║  ███║
    ║    ██╔══██╗██╔══██║██║╚██╗██║██║   ██║
    ║    ██████╔╝██║  ██║██║ ╚████║╚██████╔╝║
    ║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝║
    ║                                      ║
    ║           💀  ТЫ МЁРТВ  💀           ║
    ║                                      ║
    ╚══════════════════════════════════════╝
{RESET}"""

CLICK = f"""{GREEN}{BOLD}
    ╔══════════════════════════════════════╗
    ║                                      ║
    ║     ██████╗██╗     ██╗ ██████╗██╗  ██║
    ║    ██╔════╝██║     ██║██╔════╝██║ ██╔║
    ║    ██║     ██║     ██║██║     █████╔╝║
    ║    ██║     ██║     ██║██║     ██╔═██╗║
    ║    ╚██████╗███████╗██║╚██████╗██║  ██║
    ║     ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚║
    ║                                      ║
    ║          🍀  ПОВЕЗЛО  🍀             ║
    ║                                      ║
    ╚══════════════════════════════════════╝
{RESET}"""

SKULL = f"""{RED}
          ___
         /   \\
        | x x |
        |  ^  |
         \\___/
{RESET}"""

SURVIVED = f"""{GREEN}
          ___
         /   \\
        | ^ ^ |
        |  o  |
         \\___/
          |||
{RESET}"""

def draw_cylinder(chambers, bullet_pos, current, revealed=False):
    symbols = []
    for i in range(6):
        if revealed and i == bullet_pos:
            symbols.append(f"{RED}●{RESET}")
        elif i < current:
            symbols.append(f"{DIM}○{RESET}")
        elif i == current:
            symbols.append(f"{YELLOW}▶{RESET}")
        else:
            symbols.append(f"{WHITE}?{RESET}")

    print(f"""
    {DIM}╔═══════════╗{RESET}
    {DIM}║{RESET}  {symbols[0]}   {symbols[1]}   {symbols[2]}  {DIM}║{RESET}
    {DIM}║{RESET}           {DIM}║{RESET}
    {DIM}║{RESET}  {symbols[3]}   {symbols[4]}   {symbols[5]}  {DIM}║{RESET}
    {DIM}╚═══════════╝{RESET}
    """)

def spin_cylinder_animation():
    spin_frames = ["◐", "◓", "◑", "◒"]
    sys.stdout.write(f"\n  {YELLOW}Барабан крутится ")
    for i in range(random.randint(12, 20)):
        sys.stdout.write(f"\b{spin_frames[i % 4]}")
        sys.stdout.flush()
        time.sleep(0.1 + i * 0.02)
    print(f"\b●{RESET}")
    time.sleep(0.3)

def trigger_animation():
    sys.stdout.write(f"\n  {WHITE}Нажимаешь на курок")
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.7)
    print(RESET)
    time.sleep(0.5)

def boot_screen():
    clear()
    logo = f"""{RED}{BOLD}
    ██████╗ ██╗   ██╗███████╗███████╗██╗ █████╗ ███╗   ██╗
    ██╔══██╗██║   ██║██╔════╝██╔════╝██║██╔══██╗████╗  ██║
    ██████╔╝██║   ██║███████╗███████╗██║███████║██╔██╗ ██║
    ██╔══██╗██║   ██║╚════██║╚════██║██║██╔══██║██║╚██╗██║
    ██║  ██║╚██████╔╝███████║███████║██║██║  ██║██║ ╚████║
    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

    ██████╗  ██████╗ ██╗   ██╗██╗     ███████╗████████╗████████╗███████╗
    ██╔══██╗██╔═══██╗██║   ██║██║     ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝
    ██████╔╝██║   ██║██║   ██║██║     █████╗     ██║      ██║   █████╗
    ██╔══██╗██║   ██║██║   ██║██║     ██╔══╝     ██║      ██║   ██╔══╝
    ██║  ██║╚██████╔╝╚██████╔╝███████╗███████╗   ██║      ██║   ███████╗
    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚══════╝
{RESET}"""
    print(logo)
    print(REVOLVER)
    time.sleep(1)
    type_text("  6 камер. 1 пуля. Удачи.", delay=0.05, color=RED)
    print()

def play_round():
    bullet = random.randint(0, 5)
    survived = 0

    clear()
    print(f"\n  {YELLOW}{BOLD}═══ НОВАЯ ИГРА ═══{RESET}\n")
    type_text("  Заряжаем одну пулю в барабан...", color=DIM + WHITE)
    time.sleep(0.5)
    spin_cylinder_animation()
    type_text("  Барабан остановился.\n", color=DIM + WHITE)
    time.sleep(0.5)

    for chamber in range(6):
        print(f"  {WHITE}Камера {YELLOW}{chamber + 1}{WHITE} из {YELLOW}6{RESET}")
        draw_cylinder(6, bullet, chamber)

        print(f"  {CYAN}ENTER{WHITE} — нажать курок | {CYAN}quit{WHITE} — выйти{RESET}")
        try:
            user_input = input(f"  {RED}▸{RESET} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return False

        if user_input in ("quit", "exit", "q"):
            type_text("\n  Струсил? Ну ладно...", color=YELLOW)
            time.sleep(1)
            return True

        trigger_animation()

        if chamber == bullet:
            print(BANG)
            print(SKULL)
            draw_cylinder(6, bullet, chamber, revealed=True)
            print(f"  {RED}Пуля была в камере {bullet + 1}.{RESET}")
            print(f"  {DIM}Ты продержался {survived} раунд(ов).{RESET}\n")
            time.sleep(1)
            return True
        else:
            survived += 1
            print(CLICK)
            print(SURVIVED)
            print(f"  {GREEN}Выжил! Счёт: {survived}/6{RESET}\n")
            time.sleep(0.5)

    print(f"\n  {GREEN}{BOLD}{'=' * 40}")
    print(f"  🏆  ТЫ ПРОШЁЛ ВСЕ 6 КАМЕР!  🏆")
    print(f"  {'=' * 40}{RESET}\n")
    type_text("  Легенда. Абсолютный безумец.", color=GREEN)
    time.sleep(1)
    return True

def main():
    boot_screen()

    while True:
        print(f"\n  {CYAN}ENTER{WHITE} — начать игру | {CYAN}quit{WHITE} — выйти{RESET}")
        try:
            user_input = input(f"  {RED}▸{RESET} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input in ("quit", "exit", "q"):
            break

        if not play_round():
            break

    print()
    type_text("  До встречи... если доживёшь.", color=RED)
    time.sleep(0.5)
    clear()

if __name__ == "__main__":
    main()
