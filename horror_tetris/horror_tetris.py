"""
HORROR TETRIS
Classic Tetris with 90s Horror/Slasher Trivia
Clear lines to unlock trivia questions for bonus points!
"""

import random
import time
import os
import msvcrt
import copy

# Game settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
INITIAL_SPEED = 0.5

# Tetromino shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

# 90s Horror/Slasher Trivia
TRIVIA = [
    {
        "q": "In Scream (1996), what's the killer's mask based on?",
        "a": ["The Scream painting", "A ghost", "A skull", "A witch"],
        "correct": 0
    },
    {
        "q": "Who directed 'The Silence of the Lambs' (1991)?",
        "a": ["Wes Craven", "Jonathan Demme", "John Carpenter", "Tobe Hooper"],
        "correct": 1
    },
    {
        "q": "What's the name of the killer in 'I Know What You Did Last Summer'?",
        "a": ["The Fisherman", "The Hook Man", "Ben Willis", "The Slicker"],
        "correct": 2
    },
    {
        "q": "In 'Candyman' (1992), how many times must you say his name?",
        "a": ["3 times", "5 times", "7 times", "13 times"],
        "correct": 1
    },
    {
        "q": "What year was 'The Blair Witch Project' released?",
        "a": ["1996", "1997", "1998", "1999"],
        "correct": 3
    },
    {
        "q": "Who plays Ghostface's first victim in Scream?",
        "a": ["Neve Campbell", "Drew Barrymore", "Courteney Cox", "Rose McGowan"],
        "correct": 1
    },
    {
        "q": "What's Hannibal Lecter's profession in 'Silence of the Lambs'?",
        "a": ["Surgeon", "Psychiatrist", "Professor", "Lawyer"],
        "correct": 1
    },
    {
        "q": "In 'Urban Legend' (1998), where does the movie take place?",
        "a": ["Summer camp", "High school", "College campus", "Small town"],
        "correct": 2
    },
    {
        "q": "Who directed 'Se7en' (1995)?",
        "a": ["David Fincher", "Ridley Scott", "David Lynch", "Darren Aronofsky"],
        "correct": 0
    },
    {
        "q": "What weapon is iconic to 'Scream'?",
        "a": ["Machete", "Chainsaw", "Hunting knife", "Axe"],
        "correct": 2
    },
    {
        "q": "In 'The Craft' (1996), what do the girls practice?",
        "a": ["Voodoo", "Witchcraft", "Necromancy", "Alchemy"],
        "correct": 1
    },
    {
        "q": "What hotel is 'The Shining' set in? (1980, but iconic)",
        "a": ["Overlook Hotel", "Bates Motel", "Hotel & Resort", "Grand Hotel"],
        "correct": 0
    },
    {
        "q": "Who played Chucky's voice in 'Child's Play' series?",
        "a": ["Robert Englund", "Brad Dourif", "Tony Todd", "Doug Bradley"],
        "correct": 1
    },
    {
        "q": "In 'Final Destination' (2000), what do they cheat?",
        "a": ["The Devil", "Death", "A curse", "A demon"],
        "correct": 1
    },
    {
        "q": "What's the name of the camp in 'Friday the 13th'?",
        "a": ["Camp Blood", "Camp Crystal Lake", "Camp Redwood", "Camp Blackwood"],
        "correct": 1
    },
    {
        "q": "In 'Misery' (1990), what does Annie Wilkes do to Paul?",
        "a": ["Blinds him", "Hobbles him", "Deafens him", "Poisons him"],
        "correct": 1
    },
    {
        "q": "What town is 'Scream' set in?",
        "a": ["Haddonfield", "Springwood", "Woodsboro", "Crystal Lake"],
        "correct": 2
    },
    {
        "q": "Who survives in horror movies according to the 'rules'?",
        "a": ["The jock", "The virgin", "The funny one", "The smart one"],
        "correct": 1
    },
]


class Piece:
    def __init__(self):
        self.shape_name = random.choice(list(SHAPES.keys()))
        self.shape = copy.deepcopy(SHAPES[self.shape_name])
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Game:
    def __init__(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.speed = INITIAL_SPEED
        self.trivia_queue = []
        self.used_trivia = []
        self.message = "Welcome to HORROR TETRIS!"
        self.bonus_msg = ""

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def valid_move(self, piece, dx=0, dy=0, rotated=None):
        shape = rotated if rotated else piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + dx
                    new_y = piece.y + y + dy
                    if new_x < 0 or new_x >= BOARD_WIDTH:
                        return False
                    if new_y >= BOARD_HEIGHT:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.piece.y + y
                    board_x = self.piece.x + x
                    if board_y >= 0:
                        self.board[board_y][board_x] = 1

    def clear_lines(self):
        lines_cleared = 0
        new_board = []
        for row in self.board:
            if all(row):
                lines_cleared += 1
            else:
                new_board.append(row)

        for _ in range(lines_cleared):
            new_board.insert(0, [0] * BOARD_WIDTH)

        self.board = new_board

        if lines_cleared > 0:
            self.lines += lines_cleared
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(lines_cleared, 100) * self.level

            # Queue trivia for each line cleared
            for _ in range(lines_cleared):
                self.queue_trivia()

            self.level = 1 + self.lines // 10
            self.speed = max(0.1, INITIAL_SPEED - (self.level - 1) * 0.05)

        return lines_cleared

    def queue_trivia(self):
        available = [t for t in TRIVIA if t not in self.used_trivia]
        if not available:
            self.used_trivia = []
            available = TRIVIA
        trivia = random.choice(available)
        self.used_trivia.append(trivia)
        self.trivia_queue.append(trivia)

    def spawn_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        if not self.valid_move(self.piece):
            self.game_over = True

    def draw(self):
        self.clear_screen()

        print("+" + "-" * 22 + "+" + "-" * 18 + "+")
        print("|    HORROR TETRIS     |" + "     NEXT:      |")
        print("+" + "-" * 22 + "+" + "-" * 18 + "+")

        for y in range(BOARD_HEIGHT):
            # Draw board
            row_str = "|"
            for x in range(BOARD_WIDTH):
                if self.is_piece_at(x, y):
                    row_str += "[]"
                elif self.board[y][x]:
                    row_str += "##"
                else:
                    row_str += " ."
            row_str += " |"

            # Draw next piece preview (rows 0-3)
            if y < 4:
                row_str += " "
                for x in range(4):
                    if y < len(self.next_piece.shape) and x < len(self.next_piece.shape[0]):
                        if self.next_piece.shape[y][x]:
                            row_str += "[]"
                        else:
                            row_str += "  "
                    else:
                        row_str += "  "
                row_str += "         |"
            elif y == 5:
                row_str += f" SCORE: {self.score:<9}|"
            elif y == 6:
                row_str += f" LINES: {self.lines:<9}|"
            elif y == 7:
                row_str += f" LEVEL: {self.level:<9}|"
            elif y == 9:
                row_str += "  CONTROLS:     |"
            elif y == 10:
                row_str += "  A/D - Move    |"
            elif y == 11:
                row_str += "  W   - Rotate  |"
            elif y == 12:
                row_str += "  S   - Drop    |"
            elif y == 13:
                row_str += "  Q   - Quit    |"
            else:
                row_str += "                  |"

            print(row_str)

        print("+" + "-" * 22 + "+" + "-" * 18 + "+")

        # Message area
        if self.bonus_msg:
            print(f"| {self.bonus_msg:<39} |")
            self.bonus_msg = ""
        else:
            print(f"| {self.message:<39} |")
        print("+" + "-" * 42 + "+")

    def is_piece_at(self, bx, by):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if self.piece.x + x == bx and self.piece.y + y == by:
                        return True
        return False

    def ask_trivia(self):
        if not self.trivia_queue:
            return

        trivia = self.trivia_queue.pop(0)
        self.clear_screen()

        print("+" + "-" * 50 + "+")
        print("|" + "  HORROR TRIVIA BONUS!  ".center(50) + "|")
        print("+" + "-" * 50 + "+")
        print("|" + " " * 50 + "|")

        # Word wrap question
        q = trivia["q"]
        while len(q) > 48:
            idx = q[:48].rfind(' ')
            print(f"| {q[:idx]:<48} |")
            q = q[idx+1:]
        print(f"| {q:<48} |")

        print("|" + " " * 50 + "|")
        print("+" + "-" * 50 + "+")

        for i, ans in enumerate(trivia["a"]):
            print(f"|  [{i+1}] {ans:<43} |")

        print("+" + "-" * 50 + "+")
        print("|  Answer 1-4 for +500 bonus points!              |")
        print("+" + "-" * 50 + "+")

        # Get answer with timeout
        start = time.time()
        answer = None
        while time.time() - start < 10:  # 10 second timeout
            if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    k = key.decode()
                    if k in '1234':
                        answer = int(k) - 1
                        break
                except:
                    pass
            time.sleep(0.05)

        if answer == trivia["correct"]:
            self.score += 500
            self.bonus_msg = "CORRECT! +500 BONUS POINTS!"
            self.message = "You know your horror!"
        elif answer is None:
            self.bonus_msg = "TIME'S UP!"
            self.message = f"Answer was: {trivia['a'][trivia['correct']]}"
        else:
            self.bonus_msg = "WRONG!"
            self.message = f"Answer was: {trivia['a'][trivia['correct']]}"

        time.sleep(1.5)

    def process_input(self):
        while msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'K':  # Left
                    if self.valid_move(self.piece, dx=-1):
                        self.piece.x -= 1
                elif key == b'M':  # Right
                    if self.valid_move(self.piece, dx=1):
                        self.piece.x += 1
                elif key == b'P':  # Down
                    return 'drop'
                elif key == b'H':  # Up
                    return 'rotate'
            else:
                try:
                    k = key.decode().lower()
                    if k == 'a':
                        if self.valid_move(self.piece, dx=-1):
                            self.piece.x -= 1
                    elif k == 'd':
                        if self.valid_move(self.piece, dx=1):
                            self.piece.x += 1
                    elif k == 's':
                        return 'drop'
                    elif k == 'w':
                        return 'rotate'
                    elif k == 'q':
                        return 'quit'
                except:
                    pass
        return None

    def run(self):
        while msvcrt.kbhit():
            msvcrt.getch()

        last_fall = time.time()

        while not self.game_over:
            self.draw()

            # Input loop
            while time.time() - last_fall < self.speed:
                action = self.process_input()
                if action == 'quit':
                    return False
                elif action == 'drop':
                    while self.valid_move(self.piece, dy=1):
                        self.piece.y += 1
                    break
                elif action == 'rotate':
                    rotated = [list(row) for row in zip(*self.piece.shape[::-1])]
                    if self.valid_move(self.piece, rotated=rotated):
                        self.piece.shape = rotated
                time.sleep(0.02)

            last_fall = time.time()

            # Move piece down
            if self.valid_move(self.piece, dy=1):
                self.piece.y += 1
            else:
                self.lock_piece()
                cleared = self.clear_lines()
                if cleared:
                    self.message = f"Cleared {cleared} line(s)!"
                self.spawn_piece()

                # Ask trivia after spawning (between pieces)
                if self.trivia_queue and not self.game_over:
                    self.ask_trivia()

        # Game over
        self.clear_screen()
        print(r"""
    +------------------------------------------+
    |                                          |
    |    +-+ +-+ +-+ +--     +-+ +-+ +-- +--   |
    |    |   |-| | | |-      | | | | |-  |-+   |
    |    +-+ | | | | +--     +-+ |/  +-- | |   |
    |                                          |
    +------------------------------------------+""")
        print(f"    |          FINAL SCORE: {self.score:<8}        |")
        print(f"    |          LINES CLEARED: {self.lines:<7}        |")
        print(f"    |          LEVEL REACHED: {self.level:<7}        |")
        print(r"""    +------------------------------------------+
    |                                          |
    |     [ENTER] Play Again    [Q] Quit       |
    |                                          |
    +------------------------------------------+
        """)

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
            time.sleep(0.02)


def main():
    while True:
        game = Game()
        if not game.run():
            break
    print("\n  Thanks for playing HORROR TETRIS!")


if __name__ == "__main__":
    main()
