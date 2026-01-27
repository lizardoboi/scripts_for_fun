"""
One-Armed Bandit Slot Machine
A fun console slot machine game.
Press Enter to spin, 'q' to quit.
"""

import random
import time
import os

# Slot symbols with their weights (lower = rarer) and payouts
SYMBOLS = {
    "7": {"weight": 1, "payout": 100},
    "$": {"weight": 2, "payout": 50},
    "@": {"weight": 3, "payout": 25},
    "#": {"weight": 5, "payout": 10},
    "+": {"weight": 7, "payout": 5},
    "*": {"weight": 10, "payout": 3},
    "-": {"weight": 15, "payout": 2},
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_weighted_symbol():
    symbols = list(SYMBOLS.keys())
    weights = [SYMBOLS[s]["weight"] for s in symbols]
    return random.choices(symbols, weights=weights)[0]


def spin_reels():
    return [get_weighted_symbol() for _ in range(3)]


def display_machine(reels, credits, bet, message="", spinning=False):
    clear_screen()

    if spinning:
        display = [random.choice(list(SYMBOLS.keys())) for _ in range(3)]
    else:
        display = reels

    print(r"""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║   ░█▀▀░█░░░█▀█░▀█▀░░░█▄█░█▀█░█▀▀░█░█░   ║
    ║   ░▀▀█░█░░░█░█░░█░░░░█░█░█▀█░█░░░█▀█░   ║
    ║   ░▀▀▀░▀▀▀░▀▀▀░░▀░░░░▀░▀░▀░▀░▀▀▀░▀░▀░   ║
    ║                                           ║
    ╠═══════════════════════════════════════════╣
    ║                                           ║""")
    print(f"    ║       ┌───────┬───────┬───────┐       ║")
    print(f"    ║       │       │       │       │       ║")
    print(f"    ║       │   {display[0]}   │   {display[1]}   │   {display[2]}   │       ║")
    print(f"    ║       │       │       │       │       ║")
    print(f"    ║       └───────┴───────┴───────┘       ║")
    print(r"""    ║                                           ║
    ╠═══════════════════════════════════════════╣""")
    print(f"    ║   CREDITS: {credits:<10}  BET: {bet:<10}  ║")
    print(r"    ╠═══════════════════════════════════════════╣")

    if message:
        print(f"    ║   {message:<38}║")
    else:
        print(f"    ║                                           ║")

    print(r"    ╚═══════════════════════════════════════════╝")
    print()
    print("    [ENTER] Spin  [+/-] Bet  [Q] Quit")
    print()
    print("    PAYOUTS (3 matching):")
    print("    7=$100  $=$50  @=$25  #=$10  +=$5  *=$3  -=$2")
    print("    2 matching = half payout")


def calculate_winnings(reels, bet):
    if reels[0] == reels[1] == reels[2]:
        # Three of a kind
        return bet * SYMBOLS[reels[0]]["payout"]
    elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
        # Two of a kind
        if reels[0] == reels[1]:
            symbol = reels[0]
        elif reels[1] == reels[2]:
            symbol = reels[1]
        else:
            symbol = reels[0]
        return bet * (SYMBOLS[symbol]["payout"] // 2)
    return 0


def animate_spin(credits, bet):
    for _ in range(10):
        display_machine([], credits, bet, "SPINNING...", spinning=True)
        time.sleep(0.1)


def main():
    credits = 100
    bet = 10
    message = "Good luck! Press ENTER to spin!"
    reels = ["-", "-", "-"]

    while True:
        display_machine(reels, credits, bet, message)

        if credits <= 0:
            print("    GAME OVER! You're out of credits!")
            print("    Press ENTER to restart or Q to quit.")
            choice = input("    > ").strip().lower()
            if choice == 'q':
                break
            credits = 100
            message = "Fresh start! Good luck!"
            continue

        choice = input("    > ").strip().lower()

        if choice == 'q':
            print(f"\n    Thanks for playing! You leave with {credits} credits.")
            break
        elif choice == '+':
            bet = min(bet + 5, credits)
            message = f"Bet increased to {bet}"
        elif choice == '-':
            bet = max(bet - 5, 5)
            message = f"Bet decreased to {bet}"
        elif choice == '':
            if bet > credits:
                bet = credits

            credits -= bet
            animate_spin(credits, bet)
            reels = spin_reels()
            winnings = calculate_winnings(reels, bet)
            credits += winnings

            if winnings > 0:
                if reels[0] == reels[1] == reels[2]:
                    message = f"JACKPOT! Three {reels[0]}'s! You win {winnings}!"
                else:
                    message = f"Nice! You win {winnings}!"
            else:
                message = "No luck this time... Spin again!"


if __name__ == "__main__":
    main()
