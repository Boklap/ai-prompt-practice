# Code Documentation

## Overview

This document provides detailed technical documentation for the Snake Game implementation, explaining the architecture, design patterns, and code organization.

## Architecture

### High-Level Design

The game follows a **Model-View-Controller (MVC)** pattern with additional utility classes:

- **Model**: Game state, snake position, food locations, score
- **View**: Renderer class handling all visual output
- **Controller**: SnakeGame class managing game logic and input
- **Utilities**: InputHandler, HighScoreManager for specialized tasks

### Class Hierarchy

```
SnakeGame (Main Controller)
├── Renderer (View)
├── InputHandler (Input Management)
├── HighScoreManager (Persistence)
├── Position (Data Structure)
├── Direction (Enum with Vector Data)
├── GameState (Enum)
├── Colors (Constants)
└── Symbols (Constants)
```

## Core Classes

### SnakeGame

**Purpose**: Main game controller and state machine

**Key Responsibilities**:
- Game loop management
- State transitions
- Collision detection
- Score management
- Coordinate input handling

**Key Methods**:
- `__init__()`: Initialize all game components
- `run()`: Main game loop with 60 FPS timing
- `_handle_input()`: Process keyboard input based on current state
- `_update()`: Update game state (snake movement, collisions)
- `_render()`: Delegate rendering to Renderer class
- `_move_snake()`: Core snake movement logic
- `_spawn_foods()`: Food placement algorithm

**State Management**:
```python
class GameState(Enum):
    MENU = "menu"           # Main menu screen
    PLAYING = "playing"     # Active gameplay
    GAME_OVER = "game_over" # Player lost
    WIN = "win"            # Player won
```

### Renderer

**Purpose**: Handles all visual output and screen management

**Key Responsibilities**:
- Screen clearing and positioning
- Menu rendering with art and styling
- Game board rendering with colors
- Game over/win screen display
- Terminal centering calculations

**Rendering Pipeline**:
1. Clear screen using `os.system('clear')`
2. Calculate center position for 80x24 terminal
3. Render appropriate content based on game state
4. Apply ANSI color codes for visual enhancement

**Color System**:
```python
class Colors:
    # Standard ANSI colors with bright variants
    BRIGHT_GREEN = '\033[92m'  # Snake head
    GREEN = '\033[32m'         # Snake body
    BRIGHT_RED = '\033[91m'    # Apples
    # ... more colors
```

### InputHandler

**Purpose**: Non-blocking keyboard input processing

**Key Features**:
- Raw terminal mode for immediate key detection
- Non-blocking input using `select.select()`
- Automatic terminal restoration on cleanup
- Cross-platform compatibility (Linux/Unix)

**Implementation Details**:
```python
def get_key(self) -> Optional[str]:
    # Set raw mode for immediate input
    tty.setraw(sys.stdin.fileno())
    
    # Non-blocking check for available input
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    
    # Restore normal terminal mode
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
```

### HighScoreManager

**Purpose**: Persistent score storage and retrieval

**Features**:
- JSON-based storage in `~/score/score.json`
- Automatic directory creation
- Error handling for file operations
- Thread-safe operations

**File Structure**:
```json
{
    "high_score": 1250
}
```

## Data Structures

### Position

**Purpose**: 2D coordinate representation with hash support

```python
@dataclass
class Position:
    x: int
    y: int
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

**Usage**: Enables efficient collision detection and set operations.

### Direction

**Purpose**: Movement directions with vector data

```python
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    def __init__(self, x: int, y: int):
        self.x = x  # Horizontal movement
        self.y = y  # Vertical movement
```

**Benefits**: Type-safe direction handling with built-in vector math.

## Game Mechanics

### Movement System

**Base Movement**:
- Snake moves at fixed intervals (default: 0.15 seconds)
- Direction changes are queued to prevent invalid moves
- Snake cannot reverse direction directly

**Speed Boost**:
- Holding spacebar multiplies speed by 1.2x
- Implemented by reducing movement delay
- Smooth transition between normal and boosted speed

### Collision Detection

**Wall Collision**:
```python
if (new_head.x <= 0 or new_head.x >= SCREEN_WIDTH - 1 or
    new_head.y <= 0 or new_head.y >= SCREEN_HEIGHT - 1):
    self.state = GameState.GAME_OVER
```

**Self Collision**:
```python
if new_head in self.snake:
    self.state = GameState.GAME_OVER
```

**Food Collision**:
```python
for food in self.foods[:]:
    if new_head == food:
        self.foods.remove(food)
        self.score += SCORE_PER_FOOD
        ate_food = True
        break
```

### Food Spawning Algorithm

**Process**:
1. Generate list of all empty positions
2. Randomly select positions not occupied by snake or existing food
3. Spawn up to `MAX_FOODS` (3) items
4. Replenish food immediately when eaten

**Edge Cases**:
- Handles board nearly full scenario
- Prevents food spawning on snake body
- Maintains consistent food count

## Performance Optimizations

### Frame Rate Control

**Implementation**:
```python
FPS = 60
FRAME_DELAY = 1.0 / FPS

# In game loop:
time.sleep(FRAME_DELAY)
```

**Benefits**:
- Consistent 60 FPS gameplay
- Prevents CPU overuse
- Smooth visual experience

### Efficient Rendering

**Strategy**:
- Only redraw when state changes
- Use string concatenation for line building
- Minimize system calls

### Memory Management

**Techniques**:
- Reuse Position objects
- Avoid unnecessary list copies
- Efficient collision detection with sets

## Error Handling

### Input Validation

**Terminal Settings**:
- Automatic restoration of terminal settings
- Graceful handling of keyboard interrupts
- Cleanup on program exit

### File Operations

**Score Storage**:
- Safe JSON parsing with error handling
- Directory creation with permission checks
- Graceful degradation if file operations fail

## Constants and Configuration

### Game Constants

```python
SCREEN_WIDTH = 32      # Playable area width
SCREEN_HEIGHT = 18     # Playable area height
FPS = 60              # Target frame rate
SPEED_MULTIPLIER = 1.2 # Speed boost factor
SCORE_PER_FOOD = 10   # Points per apple
MAX_FOODS = 3         # Maximum simultaneous foods
```

### Visual Constants

```python
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
```

## Testing Considerations

### Unit Testing Strategy

**Testable Components**:
- Position class methods
- Direction enum values
- HighScoreManager file operations
- Collision detection logic

**Integration Testing**:
- Game state transitions
- Input handling scenarios
- Rendering output verification

### Performance Testing

**Metrics to Monitor**:
- Frame rate consistency
- Memory usage patterns
- Input latency
- CPU utilization

## Future Enhancements

### Potential Improvements

**Gameplay**:
- Power-ups and special items
- Multiple difficulty levels
- Obstacles and barriers
- Time-based challenges

**Technical**:
- Configuration file support
- Save/load game states
- Network multiplayer
- Sound effects support

**Visual**:
- Enhanced animations
- Particle effects
- Multiple themes
- Customizable colors

---

This documentation provides a comprehensive understanding of the codebase architecture and implementation details for future maintenance and enhancement.