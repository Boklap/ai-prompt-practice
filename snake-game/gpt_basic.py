#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Snake Terminal Edition - Minimalist Tech Style (Final Polished Version)
Author: Generated Concept 1
Environment: Linux Alpine Terminal
Python: 3.15.0a2
Libraries: Only standard Python libraries
"""

import os
import sys
import termios
import tty
import time
import json
import random

# -------------------------
# Terminal color codes (ANSI)
# -------------------------
class Colors:
    SNAKE = '\033[92m'  # Green
    FOOD = '\033[91m'   # Red
    WALL = '\033[97m'   # White
    RESET = '\033[0m'

# -------------------------
# Directions mapping
# -------------------------
DIRECTIONS = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

# -------------------------
# Symbols
# -------------------------
SNAKE_CHAR = '█'
FOOD_CHAR = '●'
WALL_CHAR = '#'
EMPTY_CHAR = ' '

# -------------------------
# High score file path
# -------------------------
SCORE_FILE = os.path.expanduser('~/score/score.json')

# -------------------------
# Load high score
# -------------------------
def load_highscore():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f).get('highscore', 0)
        except:
            return 0
    return 0

# -------------------------
# Save high score
# -------------------------
def save_highscore(score):
    os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
    with open(SCORE_FILE, 'w') as f:
        json.dump({'highscore': score}, f)

# -------------------------
# Get single key press
# -------------------------
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# -------------------------
# Clear terminal screen
# -------------------------
def clear():
    os.system('clear')

# -------------------------
# Draw main menu
# -------------------------
def draw_menu(selected=0):
    clear()
    print("  ______             _        _______                  _ _ ")
    print(" / ____/___  ____ _ (_)___   / ____(_)________  ____ _(_) |")
    print("/ /   / __ \/ __ `/ / / __ \ / /   / / ___/ _ \/ __ `/ / |")
    print("/ /___/ /_/ / /_/ / / / / / // /___/ / /  /  __/ /_/ / / |")
    print("\____/\____/\__, /_/_/_/ /_/ \____/_/_/   \___/\__, /_/|_|")
    print("           /____/                               /____/      \n")
    print("      {}{}{}       {}{}{}       {}{}{}".format(
        SNAKE_CHAR, Colors.SNAKE, Colors.RESET,
        FOOD_CHAR, Colors.FOOD, Colors.RESET,
        SNAKE_CHAR, Colors.SNAKE, Colors.RESET))
    menu_items = ['Play', 'Exit']
    for i, item in enumerate(menu_items):
        prefix = '➤ ' if i == selected else '  '
        print(f"{prefix}{item}")

# -------------------------
# Draw game board
# -------------------------
def draw_board(snake, foods, score, width, height):
    clear()
    print(f"Score: {score}  Highscore: {load_highscore()}")
    for y in range(height):
        line = ''
        for x in range(width):
            if (y, x) in snake:
                line += f"{Colors.SNAKE}{SNAKE_CHAR}{Colors.RESET}"
            elif (y, x) in foods:
                line += f"{Colors.FOOD}{FOOD_CHAR}{Colors.RESET}"
            elif y == 0 or y == height-1 or x == 0 or x == width-1:
                line += f"{Colors.WALL}{WALL_CHAR}{Colors.RESET}"
            else:
                line += EMPTY_CHAR
        print(line)

# -------------------------
# Main game loop
# -------------------------
def game_loop():
    width, height = 30, 15
    snake = [(height // 2, width // 2)]
    direction = 'd'
    score = 0
    foods = []

    # Spawn initial foods
    while len(foods) < 3:
        pos = (random.randint(1, height-2), random.randint(1, width-2))
        if pos not in snake and pos not in foods:
            foods.append(pos)

    while True:
        draw_board(snake, foods, score, width, height)

        start = time.time()
        key = getch()
        speed = 0.05  # default frame
        if key in DIRECTIONS:
            direction = key
        elif key == ' ':
            speed = 0.03  # speed up

        dy, dx = DIRECTIONS[direction]
        new_head = (snake[0][0] + dy, snake[0][1] + dx)

        # Collision detection
        if (new_head in snake) or new_head[0] == 0 or new_head[0] == height-1 or new_head[1] == 0 or new_head[1] == width-1:
            print("You lose! Press Enter to return to main menu.")
            input()
            return

        snake.insert(0, new_head)

        # Eat food
        if new_head in foods:
            foods.remove(new_head)
            score += 10
            while len(foods) < 3:
                pos = (random.randint(1, height-2), random.randint(1, width-2))
                if pos not in snake and pos not in foods:
                    foods.append(pos)
        else:
            snake.pop()

        # Win condition
        if len(snake) >= (width-2)*(height-2):
            print("You win! Press Enter to return to main menu.")
            save_highscore(score)
            input()
            return

        # Maintain 60 FPS
        elapsed = time.time() - start
        time.sleep(max(speed - elapsed, 0))

# -------------------------
# Main menu loop
# -------------------------
def main():
    selected = 0
    while True:
        draw_menu(selected)
        key = getch()
        if key == 'w':
            selected = (selected -1) % 2
        elif key == 's':
            selected = (selected +1) % 2
        elif key == '\r':
            if selected == 0:
                game_loop()
            else:
                clear()
                sys.exit()

if __name__ == "__main__":
    main()
