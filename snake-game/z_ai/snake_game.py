#!/usr/bin/env python3
"""
Terminal Snake Game - Fixed Version
A terminal-themed snake game designed for developers' lunch breaks.

Author: Legendary Senior Game Developer
Version: 1.1.0 (Fixed Input Handling)
Target: Python 3.15.0a2, Linux Alpine Terminal
"""

import os
import sys
import json
import time
import random
import threading
import termios
import tty
import signal
from pathlib import Path

class TerminalSnakeGame:
    """
    Main game class for Terminal Snake Game.
    Implements a complete snake game with terminal aesthetics.
    """
    
    def __init__(self):
        """Initialize the game with default settings and game state."""
        # Game configuration constants
        self.GAME_WIDTH = 40
        self.GAME_HEIGHT = 20
        self.FPS = 60
        self.FRAME_DELAY = 1.0 / self.FPS
        self.SPEED_BOOST_MULTIPLIER = 1.2
        self.MAX_FOODS = 3
        self.POINTS_PER_FOOD = 10
        self.BASE_MOVE_DELAY = 0.15
        
        # Visual game symbols
        self.SNAKE_HEAD = "●"
        self.SNAKE_BODY = "○"
        self.FOOD = "@"
        self.WALL = "█"
        self.EMPTY = " "
        
        # Terminal color scheme (ANSI escape codes)
        self.GREEN = "\033[92m"
        self.RED = "\033[91m"
        self.YELLOW = "\033[93m"
        self.BLUE = "\033[94m"
        self.CYAN = "\033[96m"
        self.WHITE = "\033[97m"
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"
        
        # Game state variables
        self.snake = []
        self.foods = []
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_won = False
        self.running = True
        self.speed_boost = False
        
        # Input handling
        self.old_settings = None
        self.input_lock = threading.Lock()
        
        # Initialize game systems
        self.setup_terminal()
        self.load_high_score()
        self.reset_game()
    
    def setup_terminal(self):
        """Configure terminal for optimal game display."""
        # Hide cursor for cleaner gameplay
        print("\033[?25l", end="")
        sys.stdout.flush()
        self.clear_screen()
        
        # Set terminal to raw mode for immediate input
        try:
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except Exception as e:
            # Fallback for systems without termios
            print(f"Warning: Could not set terminal mode: {e}")
            pass
        
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal for graceful exit."""
        self.running = False
        self.restore_terminal()
        print("\nGame interrupted. Exiting...")
        sys.exit(0)
    
    def restore_terminal(self):
        """Restore terminal to original state."""
        # Show cursor again
        print("\033[?25h", end="")
        sys.stdout.flush()
        
        # Restore terminal settings
        if self.old_settings:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            except:
                pass
    
    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")
        sys.stdout.flush()
    
    def load_high_score(self):
        """Load high score from persistent storage."""
        try:
            score_path = Path.home() / "score" / "score.json"
            if score_path.exists():
                with open(score_path, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except Exception:
            # If loading fails, start with zero high score
            self.high_score = 0
    
    def save_high_score(self):
        """Save current high score to persistent storage."""
        try:
            score_dir = Path.home() / "score"
            score_dir.mkdir(exist_ok=True)
            score_path = score_dir / "score.json"
            
            with open(score_path, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception:
            # Silently fail if saving doesn't work
            pass
    
    def reset_game(self):
        """Reset game to initial state for new game session."""
        # Position snake in center of game board
        center_x = self.GAME_WIDTH // 2
        center_y = self.GAME_HEIGHT // 2
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y)
        ]
        
        # Reset all game state variables
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.speed_boost = False
        
        # Initialize food items
        self.foods = []
        self.spawn_foods()
    
    def spawn_foods(self):
        """Spawn food items up to maximum limit on empty spaces."""
        empty_spaces = self.get_empty_spaces()
        
        while len(self.foods) < self.MAX_FOODS and empty_spaces:
            pos = random.choice(empty_spaces)
            if pos not in self.foods:
                self.foods.append(pos)
            empty_spaces.remove(pos)
    
    def get_empty_spaces(self):
        """Calculate all empty positions on the game board."""
        empty = []
        for x in range(1, self.GAME_WIDTH - 1):
            for y in range(1, self.GAME_HEIGHT - 1):
                if (x, y) not in self.snake and (x, y) not in self.foods:
                    empty.append((x, y))
        return empty
    
    def change_direction(self, new_direction):
        """
        Change snake movement direction if the move is valid.
        Prevents snake from moving directly into itself.
        """
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        
        if new_direction != opposites.get(self.direction):
            with self.input_lock:
                self.next_direction = new_direction
    
    def move_snake(self):
        """Execute one movement step for the snake."""
        # Update current direction from buffered input
        with self.input_lock:
            self.direction = self.next_direction
        
        # Calculate new head position based on current direction
        head_x, head_y = self.snake[0]
        new_head = (head_x, head_y)  # Default initialization
        
        if self.direction == "up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "right":
            new_head = (head_x + 1, head_y)
        
        # Check for collisions with walls or self
        if self.check_collision(new_head):
            self.game_over = True
            return
        
        # Add new head to snake body
        self.snake.insert(0, new_head)
        
        # Check if food was consumed
        if new_head in self.foods:
            self.foods.remove(new_head)
            self.score += self.POINTS_PER_FOOD
            self.spawn_foods()
            
            # Check win condition (board completely filled)
            if not self.get_empty_spaces():
                self.game_won = True
        else:
            # Remove tail if no food was eaten
            self.snake.pop()
    
    def check_collision(self, pos):
        """Check if a position results in collision."""
        x, y = pos
        
        # Wall collision detection
        if x <= 0 or x >= self.GAME_WIDTH - 1 or y <= 0 or y >= self.GAME_HEIGHT - 1:
            return True
        
        # Self-collision detection (skip head to avoid false positive)
        if pos in self.snake[1:]:
            return True
        
        return False
    
    def draw_game(self):
        """Render the complete game display."""
        self.clear_screen()
        
        # Initialize game board matrix
        board = [[self.EMPTY for _ in range(self.GAME_WIDTH)] for _ in range(self.GAME_HEIGHT)]
        
        # Draw boundary walls
        for x in range(self.GAME_WIDTH):
            board[0][x] = self.WALL
            board[self.GAME_HEIGHT - 1][x] = self.WALL
        
        for y in range(self.GAME_HEIGHT):
            board[y][0] = self.WALL
            board[y][self.GAME_WIDTH - 1] = self.WALL
        
        # Draw snake with distinct head and body
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                board[y][x] = self.GREEN + self.SNAKE_HEAD + self.RESET
            else:
                board[y][x] = self.CYAN + self.SNAKE_BODY + self.RESET
        
        # Draw food items
        for x, y in self.foods:
            board[y][x] = self.RED + self.FOOD + self.RESET
        
        # Display score information
        score_text = f"Score: {self.score}  High Score: {self.high_score}"
        print(self.BOLD + self.WHITE + score_text + self.RESET)
        
        # Render game board
        for row in board:
            print("".join(row))
        
        # Display game over or victory messages
        if self.game_over:
            self.draw_game_over()
        elif self.game_won:
            self.draw_game_won()
    
    def draw_game_over(self):
        """Display game over message centered on screen."""
        message = "YOU LOSE"
        hint = "Press ENTER to return to main menu"
        
        # Calculate centered position
        start_x = (self.GAME_WIDTH - len(message)) // 2
        start_y = self.GAME_HEIGHT // 2
        
        # Render messages using cursor positioning
        print(f"\033[{start_y};{start_x}H" + self.RED + self.BOLD + message + self.RESET)
        print(f"\033[{start_y + 1};{(self.GAME_WIDTH - len(hint)) // 2}H" + self.WHITE + hint + self.RESET)
    
    def draw_game_won(self):
        """Display victory message centered on screen."""
        message = "YOU WIN!"
        score_msg = f"Final Score: {self.score}"
        hint = "Press ENTER to return to main menu"
        
        # Calculate centered position
        start_x = (self.GAME_WIDTH - len(message)) // 2
        start_y = self.GAME_HEIGHT // 2
        
        # Render messages using cursor positioning
        print(f"\033[{start_y};{start_x}H" + self.GREEN + self.BOLD + message + self.RESET)
        print(f"\033[{start_y + 1};{(self.GAME_WIDTH - len(score_msg)) // 2}H" + self.YELLOW + score_msg + self.RESET)
        print(f"\033[{start_y + 2};{(self.GAME_WIDTH - len(hint)) // 2}H" + self.WHITE + hint + self.RESET)
    
    def get_key_input(self):
        """Get a single key press from the user."""
        try:
            # Use select to check if input is available (non-blocking)
            import select
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                
                # Handle escape sequences (arrow keys)
                if key == '\033':
                    # Read the next two characters with timeout
                    if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                        key += sys.stdin.read(2)
                
                return key
        except (ImportError, OSError, IOError):
            # Fallback for systems without select or on error
            try:
                key = sys.stdin.read(1)
                if key == '\033':
                    key += sys.stdin.read(2)
                return key
            except:
                pass
        except:
            pass
        return None
    
    def show_menu(self):
        """Display main menu with navigation."""
        selected = 0
        while True:
            self.clear_screen()
            
            # Menu artwork with terminal theme
            menu_art = """
 ╔══════════════════════════════════════╗
 ║         🐍 TERMINAL SNAKE 🐍         ║
 ║                                      ║
 ║    $ ./snake --lunch-break-mode      ║
 ║                                      ║
 ║   ▶ [ PLAY ]                         ║
 ║     [ EXIT ]                         ║
 ║                                      ║
 ╚══════════════════════════════════════╝
"""
            
            # Update menu selection indicators
            play_selected = "▶" if selected == 0 else " "
            exit_selected = "▶" if selected == 1 else " "
            
            # Replace the placeholder indicators with actual selection
            menu_lines = menu_art.strip('\n').split('\n')
            menu_lines[6] = f" ║   {play_selected} [ PLAY ]                         ║"
            menu_lines[7] = f" ║   {exit_selected} [ EXIT ]                         ║"
            
            print(self.GREEN + self.BOLD + '\n'.join(menu_lines) + self.RESET)
            
            # Handle keyboard input for menu navigation
            key = self.get_key_input()
            
            if key:
                if key == '\033[A':  # Up arrow
                    if selected > 0:
                        selected -= 1
                elif key == '\033[B':  # Down arrow
                    if selected < 1:
                        selected += 1
                elif key == '\n':  # Enter key
                    return "play" if selected == 0 else "exit"
                elif key in ['w', 'W']:  # W key as alternative to up
                    if selected > 0:
                        selected -= 1
                elif key in ['s', 'S']:  # S key as alternative to down
                    if selected < 1:
                        selected += 1
                elif key in ['q', 'Q']:  # Quit key
                    return "exit"
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.05)
    
    def handle_input(self):
        """Handle real-time keyboard input during gameplay."""
        while self.running:
            key = self.get_key_input()
            
            if key:
                # Movement controls (WASD)
                if key in ['w', 'W']:
                    self.change_direction("up")
                elif key in ['a', 'A']:
                    self.change_direction("left")
                elif key in ['s', 'S']:
                    self.change_direction("down")
                elif key in ['d', 'D']:
                    self.change_direction("right")
                elif key == ' ':  # Spacebar for speed boost
                    with self.input_lock:
                        self.speed_boost = True
                elif key == '\n':  # Enter key
                    if self.game_over or self.game_won:
                        # Update high score and return to menu
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                        return
                elif key in ['q', 'Q']:  # Quit key
                    self.running = False
                    return
            else:
                # Reset speed boost when spacebar is released
                with self.input_lock:
                    self.speed_boost = False
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.01)
    
    def run_game(self):
        """Main game loop with timing and input handling."""
        clock = time.time()
        last_move = time.time()
        
        # Start input handling thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        # Main gameplay loop
        while not self.game_over and not self.game_won and self.running:
            current_time = time.time()
            
            # Calculate movement timing with speed boost
            with self.input_lock:
                actual_delay = self.BASE_MOVE_DELAY / (self.SPEED_BOOST_MULTIPLIER if self.speed_boost else 1.0)
            
            # Execute snake movement at appropriate intervals
            if current_time - last_move >= actual_delay:
                self.move_snake()
                last_move = current_time
            
            # Render game display
            self.draw_game()
            
            # Maintain consistent frame rate
            elapsed = time.time() - clock
            if elapsed < self.FRAME_DELAY:
                time.sleep(self.FRAME_DELAY - elapsed)
            clock = time.time()
        
        # Display final game state
        self.draw_game()
        
        # Wait for player to press enter
        while self.running and (self.game_over or self.game_won):
            key = self.get_key_input()
            if key == '\n':
                break
            time.sleep(0.05)
        
        # Wait for input thread to finish
        input_thread.join(timeout=0.5)
    
    def run(self):
        """Main application entry point."""
        try:
            while self.running:
                menu_choice = self.show_menu()
                
                if menu_choice == "play":
                    self.reset_game()
                    self.run_game()
                else:
                    break
        finally:
            # Restore terminal state
            self.restore_terminal()
            self.clear_screen()

def main():
    """Application entry point."""
    game = TerminalSnakeGame()
    game.run()

if __name__ == "__main__":
    main()