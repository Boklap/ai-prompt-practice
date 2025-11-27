#!/usr/bin/env python3
"""
Snake Game - Terminal-based implementation for office workers
A fun, refreshing game designed for lunch break entertainment

Author: Legendary Senior Game Developer
Version: 1.0.0
"""

import os
import json
import time
import random
import sys
import termios
import tty
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum

# Game Constants
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 18
FPS = 60
FRAME_DELAY = 1.0 / FPS
SPEED_MULTIPLIER = 1.2
SCORE_PER_FOOD = 10
MAX_FOODS = 3

# Color codes for terminal (ANSI)
class Colors:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# Game symbols
class Symbols:
    WALL_TOP_LEFT = '╭'
    WALL_TOP_RIGHT = '╮'
    WALL_BOTTOM_LEFT = '╰'
    WALL_BOTTOM_RIGHT = '╯'
    WALL_VERTICAL = '│'
    WALL_HORIZONTAL = '─'
    SNAKE_HEAD = '█'
    SNAKE_BODY = '█'
    APPLE = 'Ó'
    EMPTY = ' '

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    WIN = "win"

@dataclass
class Position:
    x: int
    y: int
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class HighScoreManager:
    """Manages high score persistence"""
    
    def __init__(self):
        self.score_dir = Path.home() / "score"
        self.score_file = self.score_dir / "score.json"
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Create score directory if it doesn't exist"""
        self.score_dir.mkdir(exist_ok=True)
    
    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            if self.score_file.exists():
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except (json.JSONDecodeError, IOError):
            pass
        return 0
    
    def save_high_score(self, score: int):
        """Save high score to file"""
        try:
            with open(self.score_file, 'w') as f:
                json.dump({'high_score': score}, f)
        except IOError:
            pass

class InputHandler:
    """Handles keyboard input without blocking"""
    
    def __init__(self):
        self.settings = None
    
    def get_key(self) -> Optional[str]:
        """Get a single key press without blocking"""
        if self.settings is None:
            self.settings = termios.tcgetattr(sys.stdin)
        
        try:
            tty.setraw(sys.stdin.fileno())
            import select
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                
                # Handle arrow keys (escape sequences)
                if key == '\x1b':  # ESC key start of escape sequence
                    # Check if it's an arrow key sequence
                    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                        key += sys.stdin.read(1)  # Read '['
                        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                            key += sys.stdin.read(1)  # Read final character
                            return key
                
                return key
        except:
            pass
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        
        return None
    
    def cleanup(self):
        """Restore terminal settings"""
        if self.settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

class Renderer:
    """Handles all rendering operations"""
    
    def __init__(self):
        self.clear_screen()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def render_menu(self, selected_option: int, high_score: int):
        """Render the main menu"""
        self.clear_screen()
        
        # Calculate center position
        menu_width = SCREEN_WIDTH
        menu_height = SCREEN_HEIGHT
        start_x = (80 - menu_width) // 2  # Assuming 80 column terminal
        start_y = (24 - menu_height) // 2  # Assuming 24 row terminal
        
        # Menu art - snake and apple theme
        menu_art = [
            f"{Colors.BRIGHT_GREEN}    ╔══════════════════════════════╗    {Colors.RESET}",
            f"{Colors.BRIGHT_GREEN}    ║  🐍  SNAKE BREAK TIME  🍎  ║    {Colors.RESET}",
            f"{Colors.BRIGHT_GREEN}    ╚══════════════════════════════╝    {Colors.RESET}",
            "",
            f"{Colors.BRIGHT_CYAN}           The Perfect Lunch Break Game           {Colors.RESET}",
            "",
            f"{Colors.BRIGHT_YELLOW}    ┌────────────────────────────────┐    {Colors.RESET}",
            f"{Colors.BRIGHT_YELLOW}    │                                 │    {Colors.RESET}",
            f"{Colors.BRIGHT_YELLOW}    │      🐍 🍎 🐍 🍎 🐍 🍎 🐍      │    {Colors.RESET}",
            f"{Colors.BRIGHT_YELLOW}    │                                 │    {Colors.RESET}",
            f"{Colors.BRIGHT_YELLOW}    └────────────────────────────────┘    {Colors.RESET}",
            "",
            "",
            f"{Colors.BRIGHT_WHITE}              High Score: {high_score:04d}              {Colors.RESET}",
            "",
            ""
        ]
        
        # Menu options
        menu_options = ["PLAY", "EXIT"]
        
        # Print menu art and options
        for i, line in enumerate(menu_art):
            print(f"{' ' * start_x}{line}")
        
        # Print menu options
        for i, option in enumerate(menu_options):
            color = Colors.BRIGHT_GREEN if i == selected_option else Colors.WHITE
            prefix = "▶ " if i == selected_option else "  "
            print(f"{' ' * (start_x + 12)}{color}{prefix}{option}{Colors.RESET}")
    
    def render_game(self, snake: List[Position], foods: List[Position], score: int, high_score: int):
        """Render the game screen"""
        self.clear_screen()
        
        # Create game board
        board = [[Symbols.EMPTY for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
        
        # Draw walls
        for x in range(SCREEN_WIDTH):
            board[0][x] = Symbols.WALL_HORIZONTAL
            board[SCREEN_HEIGHT - 1][x] = Symbols.WALL_HORIZONTAL
        
        for y in range(SCREEN_HEIGHT):
            board[y][0] = Symbols.WALL_VERTICAL
            board[y][SCREEN_WIDTH - 1] = Symbols.WALL_VERTICAL
        
        # Draw corners
        board[0][0] = Symbols.WALL_TOP_LEFT
        board[0][SCREEN_WIDTH - 1] = Symbols.WALL_TOP_RIGHT
        board[SCREEN_HEIGHT - 1][0] = Symbols.WALL_BOTTOM_LEFT
        board[SCREEN_HEIGHT - 1][SCREEN_WIDTH - 1] = Symbols.WALL_BOTTOM_RIGHT
        
        # Create separate color and content boards for proper alignment
        color_board = [[Colors.RESET for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
        
        # Draw snake
        for i, pos in enumerate(snake):
            if 0 <= pos.x < SCREEN_WIDTH and 0 <= pos.y < SCREEN_HEIGHT:
                if i == 0:  # Head
                    board[pos.y][pos.x] = Symbols.SNAKE_HEAD
                    color_board[pos.y][pos.x] = Colors.BRIGHT_GREEN
                else:  # Body
                    board[pos.y][pos.x] = Symbols.SNAKE_BODY
                    color_board[pos.y][pos.x] = Colors.GREEN
        
        # Draw foods
        for food in foods:
            if 0 <= food.x < SCREEN_WIDTH and 0 <= food.y < SCREEN_HEIGHT:
                board[food.y][food.x] = Symbols.APPLE
                color_board[food.y][food.x] = Colors.BRIGHT_RED
        
        # Calculate center position
        start_x = (80 - SCREEN_WIDTH) // 2
        start_y = (24 - SCREEN_HEIGHT) // 2
        
        # Print score info
        print(f"{' ' * start_x}{Colors.BRIGHT_YELLOW}Score: {score:04d}  High Score: {high_score:04d}{Colors.RESET}")
        print()
        
        # Print game board with proper color handling
        for y in range(SCREEN_HEIGHT):
            line_parts = []
            for x in range(SCREEN_WIDTH):
                color = color_board[y][x]
                char = board[y][x]
                line_parts.append(f"{color}{char}")
            line = ''.join(line_parts) + Colors.RESET
            print(f"{' ' * start_x}{line}")
    
    def render_game_over(self, message: str, score: int, high_score: int):
        """Render game over screen"""
        self.clear_screen()
        
        start_x = (80 - SCREEN_WIDTH) // 2
        start_y = (24 - SCREEN_HEIGHT) // 2
        
        # Print empty lines for centering
        for _ in range(start_y + 4):
            print()
        
        print(f"{' ' * (start_x + 8)}{Colors.BRIGHT_RED}{message}{Colors.RESET}")
        print()
        print(f"{' ' * (start_x + 6)}{Colors.BRIGHT_YELLOW}Final Score: {score:04d}{Colors.RESET}")
        if score > high_score:
            print(f"{' ' * (start_x + 4)}{Colors.BRIGHT_GREEN}NEW HIGH SCORE!{Colors.RESET}")
        print()
        print(f"{' ' * (start_x + 2)}{Colors.WHITE}Press ENTER to return to menu{Colors.RESET}")

class SnakeGame:
    """Main game logic and state management"""
    
    def __init__(self):
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.high_score_manager = HighScoreManager()
        
        # Game state
        self.state = GameState.MENU
        self.snake: List[Position] = []
        self.foods: List[Position] = []
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.high_score = self.high_score_manager.load_high_score()
        self.menu_selection = 0
        self.speed_boost = False
        self.last_move_time = 0
        self.move_delay = 0.15  # Base movement delay
        
        self._init_game()
    
    def _init_game(self):
        """Initialize game state"""
        self.snake = [Position(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.foods = []
        self._spawn_foods()
    
    def _spawn_foods(self):
        """Spawn food items on the board"""
        while len(self.foods) < MAX_FOODS:
            food = self._get_random_empty_position()
            if food and food not in self.foods:
                self.foods.append(food)
    
    def _get_random_empty_position(self) -> Optional[Position]:
        """Get a random empty position on the board"""
        empty_positions = []
        
        for y in range(1, SCREEN_HEIGHT - 1):
            for x in range(1, SCREEN_WIDTH - 1):
                pos = Position(x, y)
                if pos not in self.snake and pos not in self.foods:
                    empty_positions.append(pos)
        
        if empty_positions:
            return random.choice(empty_positions)
        return None
    
    def _move_snake(self):
        """Move the snake in the current direction"""
        head = self.snake[0]
        new_head = Position(head.x + self.direction.x, head.y + self.direction.y)
        
        # Check wall collision
        if (new_head.x <= 0 or new_head.x >= SCREEN_WIDTH - 1 or
            new_head.y <= 0 or new_head.y >= SCREEN_HEIGHT - 1):
            self.state = GameState.GAME_OVER
            return
        
        # Check self collision
        if new_head in self.snake:
            self.state = GameState.GAME_OVER
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        ate_food = False
        for food in self.foods[:]:
            if new_head == food:
                self.foods.remove(food)
                self.score += SCORE_PER_FOOD
                ate_food = True
                break
        
        if not ate_food:
            self.snake.pop()
        
        # Spawn new food if needed
        self._spawn_foods()
        
        # Check win condition
        if len(self.snake) >= (SCREEN_WIDTH - 2) * (SCREEN_HEIGHT - 2):
            self.state = GameState.WIN
    
    def _handle_input(self):
        """Handle keyboard input"""
        key = self.input_handler.get_key()
        
        if self.state == GameState.MENU:
            if key == 'w' or key == 'W' or key == '\x1b[A':  # Up arrow
                self.menu_selection = 0
            elif key == 's' or key == 'S' or key == '\x1b[B':  # Down arrow
                self.menu_selection = 1
            elif key == '\r' or key == '\n':  # Enter
                if self.menu_selection == 0:  # Play
                    self.state = GameState.PLAYING
                    self._init_game()
                else:  # Exit
                    return False
        
        elif self.state == GameState.PLAYING:
            # Movement keys
            if key == 'w' or key == 'W':
                if self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
            elif key == 's' or key == 'S':
                if self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
            elif key == 'a' or key == 'A':
                if self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
            elif key == 'd' or key == 'D':
                if self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
            
            # Speed boost
            self.speed_boost = (key == ' ')  # Spacebar
        
        elif self.state in [GameState.GAME_OVER, GameState.WIN]:
            if key == '\r' or key == '\n':  # Enter
                self.state = GameState.MENU
                self.menu_selection = 0
        
        return True
    
    def _update(self, current_time: float):
        """Update game state"""
        if self.state == GameState.PLAYING:
            # Update direction
            self.direction = self.next_direction
            
            # Calculate movement delay based on speed boost
            current_delay = self.move_delay / (SPEED_MULTIPLIER if self.speed_boost else 1.0)
            
            # Move snake if it's time
            if current_time - self.last_move_time >= current_delay:
                self._move_snake()
                self.last_move_time = current_time
    
    def _render(self):
        """Render current game state"""
        if self.state == GameState.MENU:
            self.renderer.render_menu(self.menu_selection, self.high_score)
        elif self.state == GameState.PLAYING:
            self.renderer.render_game(self.snake, self.foods, self.score, self.high_score)
        elif self.state == GameState.GAME_OVER:
            self.renderer.render_game_over("YOU LOSE", self.score, self.high_score)
        elif self.state == GameState.WIN:
            self.renderer.render_game_over("YOU WIN!", self.score, self.high_score)
    
    def run(self):
        """Main game loop"""
        try:
            while True:
                current_time = time.time()
                
                # Handle input
                if not self._handle_input():
                    break
                
                # Update game state
                self._update(current_time)
                
                # Render
                self._render()
                
                # Control frame rate
                time.sleep(FRAME_DELAY)
                
                # Update high score if game ended
                if self.state in [GameState.GAME_OVER, GameState.WIN]:
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.high_score_manager.save_high_score(self.high_score)
        
        except KeyboardInterrupt:
            pass
        finally:
            self.input_handler.cleanup()
            self.renderer.clear_screen()

def main():
    """Entry point of the game"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()