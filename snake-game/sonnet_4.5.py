#!/usr/bin/env python3
"""
Code Snake - A minimalist developer-themed terminal snake game
Perfect for software engineers' lunch break entertainment

Target Audience: Office workers in software/tech (web dev, mobile dev, etc.)
Play Time: Daily lunch breaks (13:00-14:00)
Theme: Clean, code-like aesthetics with syntax highlighting colors

Controls:
  W/A/S/D - Move snake
  SPACE (hold) - Speed boost (1.2x)
  ENTER - Select menu / Continue after game over
  
Mechanics:
  - Snake grows by eating food ($)
  - Each food = +10 points
  - Up to 3 foods spawn at once
  - Die by hitting walls or self
  - Win by filling entire area
  - 60 FPS, flicker-free rendering

High scores saved to ~/score/score.json
"""

import curses
import random
import time
import json
import os
from pathlib import Path
from collections import deque

# ============================================================================
# GAME CONSTANTS
# ============================================================================

# Game settings
FPS = 60  # Target framerate
BASE_SPEED = 8  # Frames between snake moves (lower = faster)
TURBO_SPEED = 5  # Speed when holding spacebar (~1.2x boost)
SCORE_PER_FOOD = 10  # Points per food eaten
MAX_FOODS = 3  # Maximum simultaneous food items

# Visual symbols - Minimalist code-like style
SNAKE_HEAD = '>'  # Default, changes based on direction
SNAKE_BODY = '='  # Body segments
FOOD = '$'  # Food items (like variables)
WALL_H = '-'  # Horizontal wall
WALL_V = '|'  # Vertical wall
WALL_CORNER = '+'  # Corner pieces
EMPTY = ' '  # Empty space

# Movement directions (dx, dy)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# ============================================================================
# HIGH SCORE MANAGEMENT
# ============================================================================

def get_score_path():
    """
    Get the full path to the score file.
    Creates ~/score/ directory if it doesn't exist.
    
    Returns:
        Path: Path object pointing to ~/score/score.json
    """
    home = Path.home()
    score_dir = home / "score"
    score_dir.mkdir(exist_ok=True)  # Create directory if needed
    return score_dir / "score.json"


def load_high_score():
    """
    Load the high score from the JSON file.
    
    Returns:
        int: High score value, or 0 if file doesn't exist or is invalid
    """
    try:
        score_path = get_score_path()
        if score_path.exists():
            with open(score_path, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, return 0
        pass
    return 0


def save_high_score(score):
    """
    Save the high score to the JSON file.
    
    Args:
        score (int): Score value to save
    """
    try:
        score_path = get_score_path()
        with open(score_path, 'w') as f:
            json.dump({'high_score': score}, f, indent=2)
    except IOError:
        # Silently fail if we can't write (disk full, permissions, etc.)
        pass


# ============================================================================
# GAME STATE
# ============================================================================

class GameState:
    """
    Manages all game state and logic.
    Handles snake movement, collision detection, food spawning, and scoring.
    """
    
    def __init__(self, width, height):
        """
        Initialize game state.
        
        Args:
            width (int): Playable area width (excluding walls)
            height (int): Playable area height (excluding walls)
        """
        self.width = width
        self.height = height
        self.reset()
    
    def reset(self):
        """
        Reset game to initial state.
        Snake starts in center, moving right, with empty food list.
        """
        # Start snake in the middle
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = deque([(start_x, start_y)])  # deque for efficient add/remove
        
        # Movement state
        self.direction = RIGHT
        self.next_direction = RIGHT  # Buffered input to prevent missed turns
        
        # Game objects
        self.foods = set()  # Using set for O(1) collision detection
        
        # Game state
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.speed_boost = False  # True when spacebar held
        
        # Spawn initial food
        self.spawn_foods()
    
    def spawn_foods(self):
        """
        Spawn food items in random empty positions.
        Spawns up to MAX_FOODS, avoiding snake body and existing food.
        """
        # Calculate available space
        total_cells = self.width * self.height
        occupied = len(self.snake) + len(self.foods)
        empty_cells = total_cells - occupied
        
        # Spawn foods up to maximum or until area is full
        while len(self.foods) < MAX_FOODS and len(self.foods) < empty_cells:
            # Generate random position
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = (x, y)
            
            # Only spawn if position is truly empty
            if pos not in self.snake and pos not in self.foods:
                self.foods.add(pos)
    
    def change_direction(self, new_direction):
        """
        Change snake's direction, preventing 180-degree reversals.
        
        Args:
            new_direction (tuple): New direction as (dx, dy)
        """
        # Get current and new direction vectors
        dx, dy = self.direction
        ndx, ndy = new_direction
        
        # Only allow turn if not opposite direction (prevents moving into self)
        if (dx, dy) != (-ndx, -ndy):
            self.next_direction = new_direction
    
    def update(self):
        """
        Update game state for one tick.
        Moves snake, checks collisions, handles food eating, and win/lose conditions.
        """
        # Don't update if game is over
        if self.game_over or self.game_won:
            return
        
        # Apply buffered direction change
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Move snake (add new head)
        self.snake.appendleft(new_head)
        
        # Check food collision
        if new_head in self.foods:
            # Ate food - remove it, add score, spawn new food
            self.foods.remove(new_head)
            self.score += SCORE_PER_FOOD
            self.spawn_foods()
            
            # Check win condition (filled entire area)
            if len(self.snake) == self.width * self.height:
                self.game_won = True
        else:
            # No food eaten - remove tail to maintain length
            self.snake.pop()


# ============================================================================
# RENDERING
# ============================================================================

def draw_menu(stdscr):
    """
    Draw the main menu with title and ASCII art.
    
    Args:
        stdscr: Curses screen object
        
    Returns:
        int: Y-coordinate where menu options should start
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Game title
    title = "// CODE SNAKE"
    
    # ASCII art representing code structure
    art = [
        "  function play() {",
        "    snake.eat($food);",
        "    while (alive) {",
        "      snake.move();",
        "    }",
        "  }",
    ]
    
    # Draw title centered
    if height > 2:
        title_x = max(0, width // 2 - len(title) // 2)
        stdscr.addstr(2, title_x, title, 
                     curses.color_pair(1) | curses.A_BOLD)
    
    # Draw ASCII art centered
    start_y = 4
    for i, line in enumerate(art):
        if start_y + i < height:
            line_x = max(0, width // 2 - len(line) // 2)
            stdscr.addstr(start_y + i, line_x, line, curses.color_pair(2))
    
    # Return Y position for menu options
    return start_y + len(art) + 2


def draw_game(stdscr, game_state, high_score):
    """
    Draw the game area with snake, food, walls, and score.
    
    Args:
        stdscr: Curses screen object
        game_state (GameState): Current game state
        high_score (int): Current high score
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Draw score at top
    score_text = f"score: {game_state.score} | high: {high_score}"
    if width > len(score_text):
        stdscr.addstr(0, 2, score_text, curses.color_pair(3))
    
    # Calculate game area dimensions (add 2 for walls)
    game_width = game_state.width + 2
    game_height = game_state.height + 2
    
    # Center the game area on screen
    offset_x = max(0, (width - game_width) // 2)
    offset_y = max(2, (height - game_height) // 2)
    
    # Draw top wall with corners
    if offset_y < height:
        for x in range(game_width):
            if offset_x + x < width:
                if x == 0:
                    # Top-left corner
                    stdscr.addstr(offset_y, offset_x + x, WALL_CORNER, 
                                curses.color_pair(1))
                elif x == game_width - 1:
                    # Top-right corner
                    stdscr.addstr(offset_y, offset_x + x, WALL_CORNER, 
                                curses.color_pair(1))
                else:
                    # Horizontal wall
                    stdscr.addstr(offset_y, offset_x + x, WALL_H, 
                                curses.color_pair(1))
    
    # Draw bottom wall with corners
    bottom_y = offset_y + game_height - 1
    if bottom_y < height:
        for x in range(game_width):
            if offset_x + x < width:
                if x == 0:
                    # Bottom-left corner
                    stdscr.addstr(bottom_y, offset_x + x, WALL_CORNER, 
                                curses.color_pair(1))
                elif x == game_width - 1:
                    # Bottom-right corner
                    stdscr.addstr(bottom_y, offset_x + x, WALL_CORNER, 
                                curses.color_pair(1))
                else:
                    # Horizontal wall
                    stdscr.addstr(bottom_y, offset_x + x, WALL_H, 
                                curses.color_pair(1))
    
    # Draw side walls (vertical)
    for y in range(1, game_height - 1):
        draw_y = offset_y + y
        if draw_y < height:
            # Left wall
            if offset_x < width:
                stdscr.addstr(draw_y, offset_x, WALL_V, 
                            curses.color_pair(1))
            # Right wall
            right_x = offset_x + game_width - 1
            if right_x < width:
                stdscr.addstr(draw_y, right_x, WALL_V, 
                            curses.color_pair(1))
    
    # Draw snake with directional head
    for i, (x, y) in enumerate(game_state.snake):
        draw_x = offset_x + x + 1  # +1 to account for wall
        draw_y = offset_y + y + 1
        
        if draw_y < height and draw_x < width:
            if i == 0:
                # Head - show direction with arrow
                dx, dy = game_state.direction
                if dx == 1:  # Moving right
                    head_char = '>'
                elif dx == -1:  # Moving left
                    head_char = '<'
                elif dy == 1:  # Moving down
                    head_char = 'v'
                else:  # Moving up
                    head_char = '^'
                stdscr.addstr(draw_y, draw_x, head_char, curses.color_pair(2))
            else:
                # Body segments
                stdscr.addstr(draw_y, draw_x, SNAKE_BODY, curses.color_pair(2))
    
    # Draw food items
    for x, y in game_state.foods:
        draw_x = offset_x + x + 1
        draw_y = offset_y + y + 1
        if draw_y < height and draw_x < width:
            stdscr.addstr(draw_y, draw_x, FOOD, curses.color_pair(3))


def draw_game_over(stdscr, game_state, message, high_score):
    """
    Draw game over screen with message and instructions.
    
    Args:
        stdscr: Curses screen object
        game_state (GameState): Current game state
        message (str): Game over message to display
        high_score (int): Current high score
    """
    # Draw the final game state
    draw_game(stdscr, game_state, high_score)
    
    height, width = stdscr.getmaxyx()
    y = height // 2
    
    # Draw main message
    if y < height:
        msg_x = max(0, width // 2 - len(message) // 2)
        stdscr.addstr(y, msg_x, message, 
                     curses.color_pair(3) | curses.A_BOLD)
    
    # Draw hint to continue
    hint = "[press ENTER to continue]"
    if y + 2 < height:
        hint_x = max(0, width // 2 - len(hint) // 2)
        stdscr.addstr(y + 2, hint_x, hint, curses.color_pair(1))
    
    # Show final score if player won
    if game_state.game_won and y + 1 < height:
        score_text = f"final_score = {game_state.score}"
        score_x = max(0, width // 2 - len(score_text) // 2)
        stdscr.addstr(y + 1, score_x, score_text, curses.color_pair(2))


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def run_game(stdscr):
    """
    Main game loop. Handles menu, game play, and game over states.
    
    Args:
        stdscr: Curses screen object (provided by curses.wrapper)
    """
    # Initialize color pairs (syntax highlighting theme)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Walls/UI
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Snake
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Food/Score
    
    # Configure curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input (don't wait for keypress)
    stdscr.timeout(1)   # 1ms timeout for getch()
    
    # Load saved high score
    high_score = load_high_score()
    
    # Menu state
    selected = 0  # Currently selected menu option
    menu_options = ["play()", "exit()"]  # Code-style menu items
    
    # Game state machine
    state = "MENU"  # States: MENU, GAME, GAME_OVER
    game_state = None
    frame_count = 0  # For speed control
    
    # Main loop
    while True:
        if state == "MENU":
            # === MENU STATE ===
            
            # Draw menu
            menu_y = draw_menu(stdscr)
            height, width = stdscr.getmaxyx()
            
            # Draw menu options
            for i, option in enumerate(menu_options):
                if menu_y + i < height:
                    # Add selection indicator
                    prefix = "→ " if i == selected else "  "
                    text = prefix + option
                    
                    # Highlight selected option
                    color = curses.color_pair(3) if i == selected else curses.color_pair(1)
                    
                    option_x = max(0, width // 2 - len(text) // 2)
                    stdscr.addstr(menu_y + i, option_x, text, color)
            
            stdscr.refresh()
            
            # Handle menu input
            key = stdscr.getch()
            if key == ord('w') or key == curses.KEY_UP:
                # Move selection up
                selected = (selected - 1) % len(menu_options)
            elif key == ord('s') or key == curses.KEY_DOWN:
                # Move selection down
                selected = (selected + 1) % len(menu_options)
            elif key == ord('\n'):  # Enter key
                if selected == 0:  # Play selected
                    # Initialize new game
                    height, width = stdscr.getmaxyx()
                    
                    # Calculate game area (leave room for UI and walls)
                    game_width = min(60, width - 4)
                    game_height = min(20, height - 6)
                    
                    game_state = GameState(game_width, game_height)
                    state = "GAME"
                    frame_count = 0
                else:  # Exit selected
                    return
            
            time.sleep(1/FPS)
        
        elif state == "GAME":
            # === GAME STATE ===
            
            # Handle input
            key = stdscr.getch()
            if key == ord('w'):
                game_state.change_direction(UP)
            elif key == ord('a'):
                game_state.change_direction(LEFT)
            elif key == ord('s'):
                game_state.change_direction(DOWN)
            elif key == ord('d'):
                game_state.change_direction(RIGHT)
            elif key == ord(' '):
                # Spacebar held - activate speed boost
                game_state.speed_boost = True
            else:
                # No spacebar - normal speed
                game_state.speed_boost = False
            
            # Update game at appropriate speed
            speed = TURBO_SPEED if game_state.speed_boost else BASE_SPEED
            if frame_count % speed == 0:
                game_state.update()
            
            # Draw game
            draw_game(stdscr, game_state, high_score)
            stdscr.refresh()
            
            # Check for game over conditions
            if game_state.game_over:
                state = "GAME_OVER"
                message = "// GAME OVER"
            elif game_state.game_won:
                state = "GAME_OVER"
                message = "// SUCCESS"
                
                # Update high score if beaten
                if game_state.score > high_score:
                    high_score = game_state.score
                    save_high_score(high_score)
            
            frame_count += 1
            time.sleep(1/FPS)
        
        elif state == "GAME_OVER":
            # === GAME OVER STATE ===
            
            # Draw game over screen
            draw_game_over(stdscr, game_state, message, high_score)
            stdscr.refresh()
            
            # Wait for Enter key to return to menu
            key = stdscr.getch()
            if key == ord('\n'):
                state = "MENU"
                selected = 0
            
            time.sleep(1/FPS)


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """
    Entry point for the game.
    Wraps the game loop with curses initialization/cleanup.
    """
    try:
        # curses.wrapper handles initialization and cleanup automatically
        curses.wrapper(run_game)
    except KeyboardInterrupt:
        # Clean exit on Ctrl+C
        pass


if __name__ == "__main__":
    main()