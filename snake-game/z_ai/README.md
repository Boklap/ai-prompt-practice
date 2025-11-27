# Terminal Snake Game

A terminal-themed Snake game designed specifically for software developers' lunch breaks.

## Overview

Terminal Snake Game is a modern implementation of the classic Snake game, featuring a terminal aesthetic that resonates with developers. Built with Python 3.15.0a2 and designed to run in Linux Alpine terminals without any external dependencies.

## Features

### Core Gameplay
- **60 FPS smooth gameplay** with no flickering
- **WASD movement controls** for intuitive play
- **Spacebar speed boost** (1.2x faster) for advanced players
- **Progressive difficulty** as snake grows longer
- **Win condition**: Fill the entire game board
- **Lose conditions**: Hit walls or snake body

### Visual Design
- **Terminal aesthetic** with green-on-black color scheme
- **Clean, minimalist symbols** for reduced eye strain
- **Real-time score display** with high score tracking
- **Smooth animations** at consistent 60 FPS

### Technical Features
- **No external dependencies** - uses only Python standard library
- **Persistent high score** storage in `~/score/score.json`
- **Threaded input handling** for responsive controls
- **Cross-platform compatibility** (Linux, macOS, Windows)

## Installation & Setup

### Prerequisites
- Python 3.15.0a2 or higher
- Linux Alpine terminal (recommended) or any standard terminal
- No additional packages required

### Quick Start

1. **Download the game file**
   ```bash
   # Save the snake_game.py file to your desired location
   ```

2. **Make the file executable**
   ```bash
   chmod +x snake_game.py
   ```

3. **Run the game**
   ```bash
   python3 snake_game.py
   # or
   ./snake_game.py
   ```

## How to Play

### Main Menu
- **Navigation**: Use ↑↓ arrow keys to navigate menu options
- **Selection**: Press ENTER to select highlighted option
- **Options**: 
  - `[ PLAY ]` - Start a new game
  - `[ EXIT ]` - Exit the game

### Game Controls

| Key | Action |
|-----|--------|
| **W** | Move snake UP |
| **A** | Move snake LEFT |
| **S** | Move snake DOWN |
| **D** | Move snake RIGHT |
| **SPACE** | Activate speed boost (hold) |
| **ENTER** | Return to menu (when game over) |

### Game Rules

1. **Objective**: Guide the snake to eat food (@ symbols) and grow as long as possible
2. **Scoring**: Each food eaten = 10 points
3. **Food Spawning**: Up to 3 food items appear randomly on empty spaces
4. **Movement**: Snake cannot reverse direction (can't go directly back)
5. **Collision**: Game ends if snake hits walls or its own body
6. **Victory**: Win by filling the entire game board with the snake
7. **Speed Boost**: Hold spacebar for 1.2x faster movement

### Strategy Tips

- **Plan ahead**: Look for food patterns and plan your route
- **Use walls wisely**: Use walls to turn around safely
- **Speed boost timing**: Use speed boost for tight maneuvers or to reach food faster
- **Board control**: Try to create patterns that leave escape routes
- **Winning strategy**: Start in spiral patterns to efficiently fill space

## Game Elements

### Visual Symbols
- **●** (Green): Snake head - shows current direction
- **○** (Cyan): Snake body - follows the head
- **@** (Red): Food items - collect to grow and score
- **█** (White): Walls - avoid collision

### Scoring System
- **Base points**: 10 points per food item
- **High score**: Automatically saved and persisted
- **Score location**: Top-left corner during gameplay

## Technical Details

### Performance
- **Frame Rate**: Locked at 60 FPS for smooth gameplay
- **Input Response**: Threaded input handling for immediate response
- **Memory Usage**: Minimal footprint suitable for any system
- **CPU Usage**: Optimized for low power consumption

### File Structure
```
snake_game.py              # Main game executable
~/score/score.json         # High score storage (auto-created)
```

### Code Architecture
- **Object-oriented design** with clean class structure
- **Modular functions** for maintainability
- **Comprehensive comments** for code clarity
- **Error handling** for robust operation

## Troubleshooting

### Common Issues

**Q: Game runs slowly or lags**
A: Check terminal performance and close other resource-intensive applications

**Q: Arrow keys don't work in menu**
A: Ensure your terminal properly supports ANSI escape sequences

**Q: High score not saving**
A: Check write permissions in home directory and ensure `~/score/` can be created

**Q: Colors not displaying correctly**
A: Verify terminal supports ANSI color codes (most modern terminals do)

**Q: Game crashes on startup**
A: Ensure you're using Python 3.15.0a2 or higher

### Compatibility Notes
- **Tested on**: Linux Alpine, Ubuntu, macOS, Windows 10/11
- **Terminal support**: Works with most modern terminal emulators
- **Python versions**: Requires Python 3.15.0a2 features

## Development Information

### Code Quality
- **Clean, modular architecture** for easy maintenance
- **Comprehensive documentation** for all functions
- **Performance optimized** for smooth 60 FPS gameplay
- **Error resilient** with graceful failure handling

### Extension Points
The game is designed for easy modification:
- **Game symbols**: Modify visual elements in `__init__`
- **Colors**: Adjust color scheme in terminal color definitions
- **Game mechanics**: Tweak difficulty parameters
- **Board size**: Modify `GAME_WIDTH` and `GAME_HEIGHT` constants

## License

This game is provided as open-source for educational and entertainment purposes.

## Support

For issues, suggestions, or contributions, please refer to the game documentation and code comments for guidance on modifications and improvements.

---

**Enjoy your lunch break gaming! 🐍**