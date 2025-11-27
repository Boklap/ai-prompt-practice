# How to Play Terminal Snake Game

## Quick Start Guide

### Launching the Game
1. Open your terminal
2. Navigate to the game directory
3. Run: `python3 snake_game.py`
4. The main menu will appear

## Main Menu Navigation

### Menu Options
```
╔══════════════════════════════════════╗
║         🐍 TERMINAL SNAKE 🐍         ║
║                                      ║
║    $ ./snake --lunch-break-mode      ║
║                                      ║
║   ▶ [ PLAY ]                         ║
║     [ EXIT ]                         ║
║                                      ║
╚══════════════════════════════════════╝
```

### Controls
- **↑ Arrow Key**: Move selection up
- **↓ Arrow Key**: Move selection down  
- **ENTER Key**: Select highlighted option

## Game Controls

### Movement Keys
| Key | Direction | Visual Effect |
|-----|----------|---------------|
| **W** | UP | Snake moves upward |
| **A** | LEFT | Snake moves left |
| **S** | DOWN | Snake moves downward |
| **D** | RIGHT | Snake moves right |

### Special Keys
| Key | Function | When to Use |
|-----|----------|-------------|
| **SPACE** | Speed Boost (1.2x faster) | Hold for quick maneuvers |
| **ENTER** | Return to Menu | After game over or victory |

## Game Rules

### Objective
Guide your snake to eat food (@ symbols) and grow as long as possible without crashing.

### Scoring
- **Each food eaten**: +10 points
- **High score**: Automatically saved and displayed
- **Win condition**: Fill the entire game board

### Movement Rules
1. **Continuous movement**: Snake always moves in current direction
2. **No reversing**: Cannot go directly backward (e.g., can't go left if moving right)
3. **Wall collision**: Game ends if snake hits the border walls
4. **Self collision**: Game ends if snake hits its own body

### Food System
- **Maximum foods**: 3 food items on screen at once
- **Random placement**: Food appears in empty spaces only
- **Automatic respawn**: New food appears when one is eaten
- **Growth**: Snake grows longer each time food is eaten

## Visual Elements

### Game Symbols
- **● (Green)**: Snake head - shows your current direction
- **○ (Cyan)**: Snake body - follows behind the head
- **@ (Red)**: Food - collect these to grow and score
- **█ (White)**: Walls - avoid hitting these

### Score Display
```
Score: 120  High Score: 450
```
Located at the top of the game screen during play.

## Game States

### Playing
- Snake moves continuously in chosen direction
- Food items appear randomly
- Score increases as food is collected
- Speed boost available with spacebar

### Game Over
```
YOU LOSE
Press ENTER to return to main menu
```
Triggers when snake hits wall or itself.

### Victory
```
YOU WIN!
Final Score: 780
Press ENTER to return to main menu
```
Achieved when entire board is filled with snake.

## Strategy Tips

### Beginner Strategies
1. **Start slow**: Focus on control before speed
2. **Use walls**: Bounce off walls to change direction safely
3. **Plan ahead**: Look where you're going, not just at the snake
4. **Create patterns**: Develop consistent movement patterns

### Advanced Techniques
1. **Spiral patterns**: Efficient way to fill the board
2. **Speed boost timing**: Use for tight turns or escaping
3. **Board control**: Divide the board into sections
4. **Food management**: Plan routes between multiple foods

### Common Mistakes to Avoid
- **Panic movements**: Stay calm and plan your route
- **Ignoring the tail**: Always know where your body is
- **Corner trapping**: Avoid getting stuck in corners
- **Speed overuse**: Don't hold spacebar continuously

## Winning the Game

### Victory Condition
Fill the entire game board with your snake. This requires:
- Precise movement planning
- Efficient space utilization
- Avoiding all collisions
- Strategic food collection

### Winning Strategy
1. **Start in corners**: Work from outside inward
2. **Create spirals**: Systematic board filling
3. **Leave escape routes**: Always have a way out
4. **Use speed boost**: For final tight spaces

## Keyboard Reference

### During Game
```
W     - Move Up
A     - Move Left  
S     - Move Down
D     - Move Right
SPACE - Speed Boost (hold)
```

### During Menu
```
↑     - Move Up
↓     - Move Down
ENTER - Select Option
```

### After Game
```
ENTER - Return to Main Menu
```

## Troubleshooting

### Controls Not Working
- Ensure terminal window is active
- Check if caps lock is on
- Try restarting the game

### Display Issues
- Make sure terminal supports colors
- Try resizing terminal window
- Check terminal compatibility

### Performance Issues
- Close other applications
- Ensure terminal is not overloaded
- Check system resources

## Pro Tips

### Speed Boost Usage
- **Short bursts**: Use for quick direction changes
- **Tight spaces**: Navigate through narrow passages
- **Food racing**: Beat the snake to food
- **Emergency escapes**: Get out of dangerous situations

### Pattern Recognition
- **Learn common shapes**: Recognize safe movement patterns
- **Memory game**: Remember your tail position
- **Spatial awareness**: Keep track of empty spaces

### Mental Preparation
- **Stay relaxed**: It's a lunch break game!
- **Focus**: Concentrate on movement, not score
- **Practice**: Skills improve with repeated play

---

**Enjoy your lunch break gaming session! 🐍**