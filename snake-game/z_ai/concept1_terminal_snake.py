#!/usr/bin/env python3
"""
Terminal Snake Game - Concept 1
A terminal-themed snake game for developers' lunch breaks
"""

import os
import sys
import json
import time
import random
import threading
from pathlib import Path

class TerminalSnakeGame:
    """Main game class for Terminal Snake Game"""
    
    def __init__(self):
        # Game constants
        self.GAME_WIDTH = 40
        self.GAME_HEIGHT = 20
        self.FPS = 60
        self.FRAME_DELAY = 1.0 / self.FPS
        self.SPEED_BOOST_MULTIPLIER = 1.2
        
        # Game symbols
        self.SNAKE_HEAD = "●"
        self.SNAKE_BODY = "○"
        self.FOOD = "@"
        self.WALL = "█"
        self.EMPTY = " "
        
        # Colors (ANSI escape codes)
        self.GREEN = "\033[92m"
        self.RED = "\033[91m"
        self.YELLOW = "\033[93m"
        self.BLUE = "\033[94m"
        self.CYAN = "\033[96m"
        self.WHITE = "\033[97m"
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"
        
        # Game state
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
        
        # Initialize game
        self.setup_terminal()
        self.load_high_score()
        self.reset_game()
    
    def setup_terminal(self):
        """Setup terminal for game"""
        # Hide cursor and clear screen
        print("\033[?25l", end="")
        self.clear_screen()
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            score_path = Path.home() / "score" / "score.json"
            if score_path.exists():
                with open(score_path, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except:
            self.high_score = 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            score_dir = Path.home() / "score"
            score_dir.mkdir(exist_ok=True)
            score_path = score_dir / "score.json"
            
            with open(score_path, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def reset_game(self):
        """Reset game to initial state"""
        # Initialize snake in center
        center_x = self.GAME_WIDTH // 2
        center_y = self.GAME_HEIGHT // 2
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y)
        ]
        
        # Reset game state
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.speed_boost = False
        
        # Spawn initial foods
        self.foods = []
        self.spawn_foods()
    
    def spawn_foods(self):
        """Spawn foods up to maximum of 3"""
        max_foods = 3
        empty_spaces = self.get_empty_spaces()
        
        while len(self.foods) < max_foods and empty_spaces:
            pos = random.choice(empty_spaces)
            if pos not in self.foods:
                self.foods.append(pos)
            empty_spaces.remove(pos)
    
    def get_empty_spaces(self):
        """Get list of empty spaces on game board"""
        empty = []
        for x in range(1, self.GAME_WIDTH - 1):
            for y in range(1, self.GAME_HEIGHT - 1):
                if (x, y) not in self.snake and (x, y) not in self.foods:
                    empty.append((x, y))
        return empty
    
    def change_direction(self, new_direction):
        """Change snake direction if valid"""
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        
        if new_direction != opposites.get(self.direction):
            self.next_direction = new_direction
    
    def move_snake(self):
        """Move snake one step"""
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
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
        
        # Check collisions
        if self.check_collision(new_head):
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head in self.foods:
            self.foods.remove(new_head)
            self.score += 10
            self.spawn_foods()
            
            # Check win condition
            if not self.get_empty_spaces():
                self.game_won = True
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def check_collision(self, pos):
        """Check if position collides with walls or snake body"""
        x, y = pos
        
        # Check wall collision
        if x <= 0 or x >= self.GAME_WIDTH - 1 or y <= 0 or y >= self.GAME_HEIGHT - 1:
            return True
        
        # Check self collision
        if pos in self.snake[1:]:
            return True
        
        return False
    
    def draw_game(self):
        """Draw the game board"""
        self.clear_screen()
        
        # Create game board
        board = [[self.EMPTY for _ in range(self.GAME_WIDTH)] for _ in range(self.GAME_HEIGHT)]
        
        # Draw walls
        for x in range(self.GAME_WIDTH):
            board[0][x] = self.WALL
            board[self.GAME_HEIGHT - 1][x] = self.WALL
        
        for y in range(self.GAME_HEIGHT):
            board[y][0] = self.WALL
            board[y][self.GAME_WIDTH - 1] = self.WALL
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                board[y][x] = self.GREEN + self.SNAKE_HEAD + self.RESET
            else:
                board[y][x] = self.CYAN + self.SNAKE_BODY + self.RESET
        
        # Draw foods
        for x, y in self.foods:
            board[y][x] = self.RED + self.FOOD + self.RESET
        
        # Draw score
        score_text = f"Score: {self.score}  High Score: {self.high_score}"
        print(self.BOLD + self.WHITE + score_text + self.RESET)
        
        # Draw board
        for row in board:
            print("".join(row))
        
        # Draw game over or win message
        if self.game_over:
            self.draw_game_over()
        elif self.game_won:
            self.draw_game_won()
    
    def draw_game_over(self):
        """Draw game over message"""
        message = "YOU LOSE"
        hint = "Press ENTER to return to main menu"
        
        # Center the message
        start_x = (self.GAME_WIDTH - len(message)) // 2
        start_y = self.GAME_HEIGHT // 2
        
        print(f"\033[{start_y};{start_x}H" + self.RED + self.BOLD + message + self.RESET)
        print(f"\033[{start_y + 1};{(self.GAME_WIDTH - len(hint)) // 2}H" + self.WHITE + hint + self.RESET)
    
    def draw_game_won(self):
        """Draw win message"""
        message = "YOU WIN!"
        score_msg = f"Final Score: {self.score}"
        hint = "Press ENTER to return to main menu"
        
        # Center the message
        start_x = (self.GAME_WIDTH - len(message)) // 2
        start_y = self.GAME_HEIGHT // 2
        
        print(f"\033[{start_y};{start_x}H" + self.GREEN + self.BOLD + message + self.RESET)
        print(f"\033[{start_y + 1};{(self.GAME_WIDTH - len(score_msg)) // 2}H" + self.YELLOW + score_msg + self.RESET)
        print(f"\033[{start_y + 2};{(self.GAME_WIDTH - len(hint)) // 2}H" + self.WHITE + hint + self.RESET)
    
    def show_menu(self):
        """Show main menu"""
        self.clear_screen()
        
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
        
        print(self.GREEN + self.BOLD + menu_art + self.RESET)
        
        selected = 0
        while True:
            # Handle input
            try:
                import select
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    if key == '\033':  # Arrow key
                        sys.stdin.read(2)  # Read the rest of the sequence
                        key = sys.stdin.read(1)
                        if key == 'A' and selected > 0:  # Up
                            selected -= 1
                        elif key == 'B' and selected < 1:  # Down
                            selected += 1
                    elif key == '\n':  # Enter
                        if selected == 0:
                            return "play"
                        else:
                            return "exit"
            except:
                pass
            
            # Redraw menu with selection
            self.clear_screen()
            print(self.GREEN + self.BOLD + menu_art + self.RESET)
            
            play_selected = "▶" if selected == 0 else " "
            exit_selected = "▶" if selected == 1 else " "
            
            print(f"\033[8;4H{play_selected} [ PLAY ]")
            print(f"\033[9;4H{exit_selected} [ EXIT ]")
    
    def handle_input(self):
        """Handle keyboard input in separate thread"""
        while self.running:
            try:
                import select
                if select.select([sys.stdin], [], [], 0.01)[0]:
                    key = sys.stdin.read(1)
                    
                    if key == 'w':
                        self.change_direction("up")
                    elif key == 'a':
                        self.change_direction("left")
                    elif key == 's':
                        self.change_direction("down")
                    elif key == 'd':
                        self.change_direction("right")
                    elif key == ' ':
                        self.speed_boost = True
                    elif key == '\n' and (self.game_over or self.game_won):
                        # Update high score if needed
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                        return
            except:
                pass
    
    def run_game(self):
        """Main game loop"""
        clock = time.time()
        last_move = time.time()
        move_delay = 0.15  # Base movement delay
        
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        while not self.game_over and not self.game_won:
            current_time = time.time()
            
            # Calculate actual move delay with speed boost
            actual_delay = move_delay / (self.SPEED_BOOST_MULTIPLIER if self.speed_boost else 1.0)
            
            # Move snake at appropriate interval
            if current_time - last_move >= actual_delay:
                self.move_snake()
                last_move = current_time
            
            # Draw game
            self.draw_game()
            
            # Maintain FPS
            elapsed = time.time() - clock
            if elapsed < self.FRAME_DELAY:
                time.sleep(self.FRAME_DELAY - elapsed)
            clock = time.time()
        
        # Show final screen
        self.draw_game()
        
        # Wait for enter key
        while True:
            try:
                import select
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    if key == '\n':
                        break
            except:
                pass
    
    def run(self):
        """Main game runner"""
        try:
            while True:
                menu_choice = self.show_menu()
                
                if menu_choice == "play":
                    self.reset_game()
                    self.run_game()
                else:
                    break
        finally:
            # Restore terminal
            print("\033[?25h", end="")
            self.clear_screen()

if __name__ == "__main__":
    game = TerminalSnakeGame()
    game.run()