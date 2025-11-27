#!/usr/bin/env python3
"""
snake_lunch_minimal.py
Minimalist Code-Editor themed Snake for terminal (Alpine Linux compatible).

Features:
- Terminal-based snake using Python curses (no external pip packages).
- 60 FPS render loop; snake movement tick independent of render.
- Controls: WASD or arrow keys. Space = 1.2x speed boost while held.
- Walls on edges; snake dies if hits walls or itself.
- Up to 3 foods on screen; each food = +10 points.
- Win when snake fills entire playable area.
- Main menu with Play and Exit. Enter to select. Enter to return from end screen.
- Uses 256-color pairs when available but falls back gracefully.

Run:
    python3 snake_lunch_minimal.py

Notes:
- Designed for Linux terminals. If colors look off, try a 256-color capable terminal.
- If resizing terminal while playing causes layout issues, restart the program.

Author: Generated & polished by ChatGPT as senior dev mentor.
"""

import curses
import time
import random
from dataclasses import dataclass
from collections import deque
from typing import Deque, Tuple, List

# -------------------------
# Configuration
# -------------------------
@dataclass
class Config:
    fps: int = 60                         # Render frames per second
    width: int = 42                       # Game area width (including walls)
    height: int = 22                      # Game area height (including walls)
    base_moves_per_sec: float = 5.0       # Base snake speed (moves/sec)
    speed_boost_factor: float = 1.2       # Speed multiplier when space is held
    max_food: int = 3                     # Max concurrent food pieces
    points_per_food: int = 10             # Points per food

# Movement directions as (dy, dx)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# -------------------------
# Game state dataclass
# -------------------------
@dataclass
class GameState:
    snake: Deque[Tuple[int,int]]          # deque of (y,x) positions; head at index 0
    direction: Tuple[int,int]             # current movement direction
    foods: List[Tuple[int,int]]           # list of food positions
    score: int                            # current score
    highscore: int                        # recorded highscore
    running: bool                         # True while gameplay active
    won: bool                             # True if player filled map
    lost: bool                            # True if player died

# -------------------------
# Utility functions
# -------------------------
def in_bounds(conf: Config, pos: Tuple[int,int]) -> bool:
    """Return True if pos is inside interior (not a wall)."""
    y, x = pos
    return 0 < y < conf.height - 1 and 0 < x < conf.width - 1

# -------------------------
# Food spawn logic
# -------------------------
def spawn_food(conf: Config, state: GameState) -> None:
    """
    Spawn food items in empty cells (not on the snake nor on existing food),
    until state.foods length equals conf.max_food or no empties available.
    """
    snake_set = set(state.snake)
    empties = []
    for y in range(1, conf.height - 1):
        for x in range(1, conf.width - 1):
            if (y, x) not in snake_set and (y, x) not in state.foods:
                empties.append((y, x))
    random.shuffle(empties)
    while len(state.foods) < conf.max_food and empties:
        state.foods.append(empties.pop())

# -------------------------
# Game update (single tick)
# -------------------------
def update_game(conf: Config, state: GameState) -> None:
    """
    Advance the snake by one tile in the current direction.
    Handles collisions (walls/self), eating food, score updates, and win condition.
    """
    head = state.snake[0]
    new_head = (head[0] + state.direction[0], head[1] + state.direction[1])

    # Wall collision -> lose
    if not in_bounds(conf, new_head):
        state.lost = True
        state.running = False
        return

    # Self collision -> lose
    if new_head in state.snake:
        state.lost = True
        state.running = False
        return

    # Move head
    state.snake.appendleft(new_head)

    # If new head is on food, eat and grow (do not remove tail)
    if new_head in state.foods:
        state.foods.remove(new_head)
        state.score += conf.points_per_food
        if state.score > state.highscore:
            state.highscore = state.score
    else:
        # Normal move: remove tail
        state.snake.pop()

    # Win condition: snake fills all interior cells
    interior_cells = (conf.width - 2) * (conf.height - 2)
    if len(state.snake) >= interior_cells:
        state.won = True
        state.running = False

# -------------------------
# Rendering
# -------------------------
def init_colors():
    """
    Initialize color pairs. Uses curses' extended colors when available.
    Pair indices:
      1 -> neutral text
      2 -> accent cyan (snake head)
      3 -> food yellow
      4 -> wall/box grey
    """

    if not curses.has_colors():
        return

    curses.start_color()
    try:
        curses.use_default_colors()
    except Exception:
        pass  # some terminals raise an error, ignore

    # Check if terminal supports 256 colors
    has_256 = False
    if curses.COLORS >= 256:
        has_256 = True

    if has_256:
        # Use 256-color indices (better visuals)
        curses.init_pair(1, 250, -1)  # neutral body (light grey)
        curses.init_pair(2, 81, -1)   # head cyan
        curses.init_pair(3, 226, -1)  # food yellow
        curses.init_pair(4, 239, -1)  # walls dark grey
    else:
        # fallback to standard 8-color palette
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_CYAN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)

    # curses.start_color()
    # # allow default background
    # try:
    #     curses.use_default_colors()
    # except Exception:
    #     pass
    # # safe init (some terminals may not support 256 indices; curses will clamp)
    # curses.init_pair(1, 250, -1)   # neutral
    # curses.init_pair(2, 81, -1)    # accent cyan
    # curses.init_pair(3, 226, -1)   # food yellow
    # curses.init_pair(4, 239, -1)   # walls
    
def draw_border(win, conf: Config):
    """Draw the window border using box-drawing characters safely."""
    h, w = win.getmaxyx()  # actual window size (may be smaller than conf)
    
    # Top and bottom
    for x in range(min(conf.width, w)):
        try:
            win.addch(0, x, '─', curses.color_pair(4))
            win.addch(min(conf.height - 1, h-1), x, '─', curses.color_pair(4))
        except curses.error:
            pass
    
    # Left and right
    for y in range(min(conf.height, h)):
        try:
            win.addch(y, 0, '│', curses.color_pair(4))
            win.addch(y, min(conf.width - 1, w-1), '│', curses.color_pair(4))
        except curses.error:
            pass

    # Corners
    try: win.addch(0, 0, '┌', curses.color_pair(4))
    except curses.error: pass
    try: win.addch(0, min(conf.width - 1, w-1), '┐', curses.color_pair(4))
    except curses.error: pass
    try: win.addch(min(conf.height - 1, h-1), 0, '└', curses.color_pair(4))
    except curses.error: pass
    try: win.addch(min(conf.height - 1, h-1), min(conf.width - 1, w-1), '┘', curses.color_pair(4))
    except curses.error: pass

# def draw_border(win, conf: Config):
#     """Draw the window border using box-drawing characters."""
#     # Top and bottom
#     for x in range(conf.width):
#         win.addch(0, x, '─', curses.color_pair(4))
#         win.addch(conf.height - 1, x, '─', curses.color_pair(4))
#     # Left and right
#     for y in range(conf.height):
#         win.addch(y, 0, '│', curses.color_pair(4))
#         win.addch(y, conf.width - 1, '│', curses.color_pair(4))
#     # Corners
#     win.addch(0, 0, '┌', curses.color_pair(4))
#     win.addch(0, conf.width - 1, '┐', curses.color_pair(4))
#     win.addch(conf.height - 1, 0, '└', curses.color_pair(4))
#     win.addch(conf.height - 1, conf.width - 1, '┘', curses.color_pair(4))

def render(stdscr, conf: Config, state: GameState) -> None:
    """
    Render the whole frame. This creates a centered subwindow of size conf.width x conf.height.
    Draw border, foods, snake, and HUD above the window.
    """
    stdscr.erase()
    maxy, maxx = stdscr.getmaxyx()
    # center the playfield
    starty = max((maxy - conf.height) // 2, 0)
    startx = max((maxx - conf.width) // 2, 0)
    win = stdscr.subwin(conf.height, conf.width, starty, startx)
    win.erase()

    # border
    draw_border(win, conf)

    # foods
    for (y, x) in state.foods:
        # Place '✦' as food (if unsupported, it shows as fallback char)
        win.addch(y, x, '✦', curses.color_pair(3) | curses.A_BOLD)

    # snake drawing: head and body
    for idx, (y, x) in enumerate(state.snake):
        if idx == 0:
            win.addch(y, x, '▣', curses.color_pair(2) | curses.A_BOLD)  # head
        else:
            win.addch(y, x, '·', curses.color_pair(1))  # body

    # HUD (title + scores) placed above the window
    hud = f"[ S N A K E ]   Score: {state.score}   High: {state.highscore}"
    hud_y = max(starty - 2, 0)
    hud_x = startx
    try:
        stdscr.addstr(hud_y, hud_x, hud, curses.color_pair(1))
    except curses.error:
        # in case terminal is very small, ignore
        pass

    # messages (win/lose) centered inside playfield
    if state.lost:
        msg = " YOU LOSE — press ENTER "
        stdscr.addstr(starty + conf.height // 2, startx + (conf.width - len(msg)) // 2, msg, curses.color_pair(3))
    elif state.won:
        msg = " YOU WIN! press ENTER "
        stdscr.addstr(starty + conf.height // 2, startx + (conf.width - len(msg)) // 2, msg, curses.color_pair(3))

    stdscr.refresh()

# -------------------------
# Main menu
# -------------------------
def show_main_menu(stdscr, conf: Config) -> str:
    """
    Displays a simple main menu with Play and Exit.
    Returns the selected option string.
    """
    stdscr.erase()
    maxy, maxx = stdscr.getmaxyx()
    title_lines = [
        " [  S N A K E  ] ",
        "  Minimal Editor Theme — Lunch Break"
    ]
    # center title block
    top = max(2, maxy // 6)
    for i, line in enumerate(title_lines):
        try:
            stdscr.addstr(top + i, (maxx - len(line)) // 2, line, curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass

    options = ["Play", "Exit"]
    selected = 0

    stdscr.nodelay(False)  # block for menu input
    while True:
        for i, opt in enumerate(options):
            y = top + len(title_lines) + 2 + i * 2
            x = (maxx // 2) - 6
            style = curses.A_REVERSE if i == selected else curses.A_NORMAL
            try:
                stdscr.addstr(y, x, f"  {opt}  ", style | curses.color_pair(1))
            except curses.error:
                pass
        stdscr.refresh()
        key = stdscr.getch()
        if key in (curses.KEY_UP, ord('w'), ord('W')):
            selected = (selected - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            selected = (selected + 1) % len(options)
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
            selected = (selected - 1) % len(options)
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
            selected = (selected + 1) % len(options)
        elif key in (10, 13):  # Enter
            stdscr.nodelay(True)
            return options[selected]
        # small sleep to avoid busy-waiting while blocking menu (fine UX)
        time.sleep(0.02)

# -------------------------
# Main loop / entrypoint
# -------------------------
def main(stdscr):
    """
    Main program entrypoint intended to be used with curses.wrapper(main).
    Sets up curses modes, runs the main menu and game loop, and handles cleanup.
    """
    # Initial curses setup
    curses.curs_set(0)       # hide cursor
    stdscr.nodelay(True)     # non-blocking input by default
    stdscr.keypad(True)      # enable special keys (arrows)
    init_colors()

    conf = Config()
    global_highscore = 0

    while True:
        # Show menu and get user choice
        choice = show_main_menu(stdscr, conf)
        if choice == "Exit":
            break

        # Initialize a fresh game state
        midy = conf.height // 2
        midx = conf.width // 2
        snake = deque()
        # initial snake length 3, horizontal pointing right
        snake.append((midy, midx))
        snake.append((midy, midx - 1))
        snake.append((midy, midx - 2))
        state = GameState(
            snake=snake,
            direction=RIGHT,
            foods=[],
            score=0,
            highscore=global_highscore,
            running=True,
            won=False,
            lost=False
        )

        spawn_food(conf, state)

        # Timing variables: movement uses move ticks; rendering locks at FPS
        last_move_time = time.perf_counter()
        frame_interval = 1.0 / conf.fps

        # Game loop
        while True:
            frame_start = time.perf_counter()

            # Input handling (non-blocking)
            key = stdscr.getch()
            boost_active = False
            if key != -1:
                if key in (ord('w'), ord('W'), curses.KEY_UP):
                    # prevent 180-degree reversal
                    if state.direction != DOWN:
                        state.direction = UP
                elif key in (ord('s'), ord('S'), curses.KEY_DOWN):
                    if state.direction != UP:
                        state.direction = DOWN
                elif key in (ord('a'), ord('A'), curses.KEY_LEFT):
                    if state.direction != RIGHT:
                        state.direction = LEFT
                elif key in (ord('d'), ord('D'), curses.KEY_RIGHT):
                    if state.direction != LEFT:
                        state.direction = RIGHT
                elif key == ord(' '):
                    boost_active = True
                elif key in (10, 13):  # ENTER
                    if not state.running:
                        # Return to menu
                        break
                elif key == ord('q'):
                    # Quick quit to menu (counts as lose)
                    state.running = False
                    state.lost = True
                    break

            # quick extra poll to better detect space hold (terminals don't always provide key-held events)
            ch2 = stdscr.getch()
            if ch2 == ord(' '):
                boost_active = True

            # Movement tick logic:
            # compute effective rate (moves/sec) based on boost status
            effective_rate = conf.base_moves_per_sec * (conf.speed_boost_factor if boost_active else 1.0)
            effective_interval = 1.0 / effective_rate
            now = time.perf_counter()
            if now - last_move_time >= effective_interval and state.running:
                update_game(conf, state)
                last_move_time = now
                # attempt to spawn food after each move (ensures up to max_food)
                spawn_food(conf, state)

            # Render current frame
            render(stdscr, conf, state)

            # update global highscore
            if state.highscore > global_highscore:
                global_highscore = state.highscore

            # If game ended, keep displaying overlay until user presses ENTER (handled above)
            if not state.running:
                render(stdscr, conf, state)

            # Maintain 60 FPS render cadence
            frame_end = time.perf_counter()
            elapsed = frame_end - frame_start
            time_to_sleep = frame_interval - elapsed
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

        # End of a game round, back to menu loop

    # Program exit
    curses.endwin()

if __name__ == "__main__":
    # Use curses.wrapper to ensure terminal state is restored on crash/exit
    curses.wrapper(main)
