# Game Documentation

## Project Overview

Terminal Snake Game is a Python-based implementation of the classic Snake game, specifically designed for software developers to play during their lunch breaks. The game features a terminal aesthetic that resonates with developers while providing an engaging and relaxing gaming experience.

## Architecture

### Core Components

#### 1. TerminalSnakeGame Class
The main game controller that manages all game systems:
- **Game State Management**: Tracks snake position, food locations, score, and game status
- **Rendering System**: Handles all visual output to the terminal
- **Input System**: Processes keyboard input through threaded handling
- **Collision Detection**: Manages wall and self-collision logic
- **Score System**: Tracks current score and persistent high scores

#### 2. Game Loop System
```python
# Main game flow:
1. Initialize game state
2. Start input handling thread
3. Enter main game loop:
   - Process timed snake movement
   - Update game state
   - Render display
   - Maintain 60 FPS timing
4. Handle game over/victory conditions
5. Return to main menu
```

#### 3. Input Handling System
- **Threaded Architecture**: Separate thread for responsive input
- **Buffered Input**: Prevents input conflicts and missed commands
- **Multi-key Support**: Handles simultaneous movement and speed boost
- **Menu Navigation**: Arrow key navigation for menu system

## Code Structure

### Initialization (`__init__`)
- Sets up game constants and configuration
- Initializes visual symbols and color scheme
- Loads persistent high score data
- Configures terminal settings

### Game State Management
- **reset_game()**: Resets all game variables to initial state
- **spawn_foods()**: Manages food placement and respawning
- **get_empty_spaces()**: Calculates available positions for food

### Movement System
- **move_snake()**: Executes one movement step
- **change_direction()**: Validates and updates movement direction
- **check_collision()**: Detects wall and self-collision

### Rendering System
- **draw_game()**: Main rendering function
- **draw_game_over()**: Displays game over message
- **draw_game_won()**: Displays victory message
- **show_menu()**: Renders main menu interface

## Data Structures

### Snake Representation
```python
snake = [(head_x, head_y), (body_x1, body_y1), (body_x2, body_y2), ...]
# List of tuples representing snake segments
# Index 0 is always the head
```

### Food Management
```python
foods = [(food1_x, food1_y), (food2_x, food2_y), ...]
# List of tuples containing food positions
# Maximum of 3 foods at any time
```

### Game Board
```python
board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
# 2D matrix representing the game state
# Updated each frame for rendering
```

## Performance Optimizations

### Frame Rate Control
- **60 FPS Target**: Consistent frame timing using `time.sleep()`
- **Movement Timing**: Separate timing for snake movement vs rendering
- **Input Responsiveness**: Non-blocking input handling

### Memory Efficiency
- **Minimal Data Structures**: Efficient use of lists and tuples
- **No External Dependencies**: Pure Python standard library
- **Optimized Rendering**: Only redraw changed elements when possible

## Terminal Compatibility

### ANSI Escape Codes
The game uses standard ANSI escape sequences for:
- **Color Formatting**: `\033[9Xm` for different colors
- **Cursor Positioning**: `\033[Y;XH` for precise text placement
- **Text Attributes**: `\033[1m` for bold, `\033[2m` for dim

### Cross-Platform Support
- **Linux/Unix**: Native terminal support
- **macOS**: Terminal.app and iTerm2 compatible
- **Windows**: Windows Terminal and PowerShell support

## File I/O Operations

### High Score Persistence
```python
# Location: ~/score/score.json
# Format: {"high_score": numeric_value}
# Auto-creation of directory structure
# Graceful error handling for permission issues
```

## Error Handling

### Robustness Features
- **Input Validation**: Validates all keyboard inputs
- **File I/O Safety**: Handles file permission and access errors
- **Terminal State**: Ensures terminal is properly restored on exit
- **Exception Handling**: Try-catch blocks for all critical operations

## Extension Points

### Customization Options
1. **Visual Elements**: Modify symbols and colors in class constants
2. **Game Mechanics**: Adjust movement speed, board size, scoring
3. **Difficulty Levels**: Implement different difficulty presets
4. **Themes**: Create alternative visual themes

### Potential Enhancements
1. **Sound Effects**: Add terminal bell sounds for events
2. **Multiplayer**: Network-based multiplayer functionality
3. **Power-ups**: Special food items with unique effects
4. **Obstacles**: Static obstacles on the game board

## Testing Considerations

### Manual Testing Checklist
- [ ] Menu navigation works correctly
- [ ] All movement keys respond properly
- [ ] Speed boost functions as expected
- [ ] Collision detection works for walls and self
- [ ] Food spawning and collection works
- [ ] Score tracking and persistence functions
- [ ] Win/lose conditions trigger correctly
- [ ] Terminal state is properly restored

### Performance Testing
- [ ] Maintains 60 FPS on target systems
- [ ] Memory usage remains stable
- [ ] Input responsiveness under rapid key presses
- [ ] No screen flickering or artifacts

## Security Considerations

### Safe Practices
- **No File System Risks**: Only writes to user's home directory
- **No Network Access**: Completely offline operation
- **No System Calls**: Uses only standard Python libraries
- **Input Sanitization**: Validates all user inputs

## Deployment

### Distribution
- **Single File**: Complete game in one Python file
- **No Dependencies**: Runs on any system with Python 3.15.0a2+
- **Portable**: Can be run from any location
- **Self-Contained**: All functionality built-in

### Installation Steps
1. Ensure Python 3.15.0a2+ is installed
2. Download the snake_game.py file
3. Set executable permissions (optional)
4. Run with `python3 snake_game.py`

This documentation provides a comprehensive understanding of the game's internal workings for maintenance, modification, and educational purposes.