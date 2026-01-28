import time
import random
import sys

farts = ["пррррт", "бздынь", "пфффф", "бррррр", "пук", "ПРРРРРРТ", "бзззз", "пшшшш"]

frames = [
    r"""
    \O/
     |
    / \
    """,
    r"""
     O
    /|\
    / \
    """,
    r"""
     O/
    /|
    / \
    """,
    r"""
    \O
     |\
    / \
    """,
]

while True:
    for frame in frames:
        sys.stdout.write("\033[2J\033[H")
        print("=" * 30)
        print("     СЕМА ЛОХ!!!")
        print("=" * 30)
        print(frame)
        if random.random() < 0.5:
            fart = random.choice(farts)
            print(f"    💨 {fart}!")
        print("=" * 30)
        time.sleep(0.4)
