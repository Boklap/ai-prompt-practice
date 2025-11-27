# How to Play Snake Game

## Quick Start Guide

### Launching the Game
1. Open your terminal
2. Navigate to the game directory: `cd glm_4.6`
3. Run the game: `python3 snake_game.py`
4. The main menu will appear automatically

## Main Menu

### Menu Options
- **PLAY**: Start a new game
- **EXIT**: Quit the application

### Menu Controls
- **W/S or Arrow Keys**: Move selection up/down
- **Enter**: Select highlighted option

## Game Controls

### Movement
- **W**: Move snake UP ↑
- **A**: Move snake LEFT ←  
- **S**: Move snake DOWN ↓
- **D**: Move snake RIGHT →

### Special Actions
- **Spacebar (Hold)**: Speed boost - snake moves 1.2x faster
- **Enter**: Return to main menu (after game ends)

## Game Rules

### Objective
Eat red apples (Ó) to make your snake grow. Fill the entire playing area to win!

### How to Play
1. **Start Moving**: Your snake begins moving right automatically
2. **Eat Apples**: Guide your snake to eat red apples
3. **Grow Longer**: Your snake grows by one segment for each apple eaten
4. **Avoid Collisions**: Don't hit walls or your own body
5. **Fill the Board**: Win by covering all empty space with your snake

### Scoring
- **Each Apple**: 10 points
- **High Score**: Best score saved automatically
- **Win Bonus**: Special recognition for completing the game

## Game Elements

### Visual Guide
```
╭────────────────────────────────╮  ← Walls (boundaries)
│ █ÓÓ                           │  █ = Snake Head (bright green)
│ ██Ó                           │  █ = Snake Body (green)
│ ███Ó                          │  Ó = Apple (bright red)
│ ████Ó                         │  │ = Wall (vertical)
│ █████Ó                        │  ─ = Wall (horizontal)
│ ██████Ó                       │
│ ███████Ó                      │
│ ████████Ó                     │
│ █████████Ó                    │
│ ██████████Ó                   │
│ ███████████Ó                  │
│ ████████████Ó                 │
│ █████████████Ó                │
│ ██████████████Ó               │
│ ███████████████Ó              │
│ ████████████████Ó             │
╰────────────────────────────────╯
```

### Color Legend
- **Bright Green**: Snake head
- **Green**: Snake body  
- **Bright Red**: Apples
- **Default**: Walls and text

## Game States

### Playing
- Active gameplay with snake movement
- Score displayed in top-left corner
- Real-time high score tracking

### Game Over - YOU LOSE
Appears when:
- Snake hits a wall
- Snake hits its own body

**Display**: "YOU LOSE" message with final score

### Victory - YOU WIN!
Appears when:
- Snake fills entire playable area
- No empty spaces remain

**Display**: "YOU WIN!" message with final score

## Strategy Tips

### Beginner Strategies
1. **Stay Safe**: Keep away from walls initially
2. **Plan Ahead**: Think 2-3 moves before acting
3. **Use Edges**: Walls provide temporary safety
4. **Go Slow**: Don't use speed boost until comfortable

### Intermediate Tips
1. **Create Patterns**: Use spiral or snake-like patterns
2. **Leave Escape Routes**: Don't trap yourself in corners
3. **Smart Speed**: Use boost for quick direction changes
4. **Food Priority**: Target apples that open new areas

### Advanced Techniques
1. **Efficient Paths**: Plan routes to maximize space coverage
2. **Body Control**: Use your body as temporary walls
3. **Precision Movement**: Exact timing for tight spaces
4. **Risk Management**: Know when to play safe vs aggressive

## Common Mistakes to Avoid

### Movement Errors
- **Don't Reverse**: Can't go directly backward (W→S, A→D)
- **Watch Your Tail**: Remember where your body is going
- **Corner Traps**: Avoid getting stuck in corners
- **Speed Overuse**: Don't hold spacebar when precision is needed

### Strategic Errors
- **Ignoring the Future**: Plan your escape routes
- **Greedy Play**: Don't chase apples into dangerous areas
- **Panic Moves**: Stay calm when space gets tight
- **Forgetting Boundaries**: Remember wall positions

## Game Duration

### Typical Session Lengths
- **Quick Games**: 1-3 minutes (beginners, early collisions)
- **Average Games**: 3-8 minutes (intermediate players)
- **Long Games**: 8-15 minutes (experts, completion attempts)

### Perfect for Lunch Breaks
- **Multiple Sessions**: Play 2-3 games during lunch hour
- **Natural Breaks**: Game over provides clean stopping points
- **Quick Restart**: Immediate new game from menu

## Troubleshooting

### Control Issues
**Problem**: Keys not responding
**Solution**: Make sure terminal window is active (click on it)

**Problem**: Snake moves wrong direction
**Solution**: Remember you can't reverse directly - need to turn first

### Display Issues
**Problem**: Screen looks messy
**Solution**: Ensure your terminal supports colors and is at least 80x24

**Problem**: Game seems slow/fast
**Solution**: Game runs at 60 FPS - adjust terminal settings if needed

### Score Issues
**Problem**: High score not saving
**Solution**: Check permissions for home directory and ~/score/ folder

## Pro Tips

### Speed Boost Mastery
- **Quick Escapes**: Use boost to get out of tight spots
- **Apple Collection**: Faster apple gathering when path is clear
- **Don't Overuse**: Regular speed gives more control

### Pattern Recognition
- **Spiral Method**: Start from edges and work inward
- **Snake Pattern**: Create back-and-forth rows
- **Corner Method**: Fill corners first, then center

### Mental State
- **Stay Calm**: Panic leads to mistakes
- **Take Breaks**: Reset between games
- **Focus**: Concentrate on current move, not final score

## Keyboard Reference Card

```
MENU:
  W/S - Navigate up/down
  Enter - Select option

GAME:
  W - Move Up
  A - Move Left  
  S - Move Down
  D - Move Right
  Spacebar (Hold) - Speed Boost
  
AFTER GAME:
  Enter - Return to Menu
```

## Getting Better

### Practice Progression
1. **Week 1**: Learn controls, survive 2+ minutes
2. **Week 2**: Master basic patterns, score 100+ points
3. **Week 3**: Advanced strategies, score 300+ points
4. **Week 4**: Complete the game, achieve 500+ points

### Skill Development
- **Pattern Recognition**: Learn efficient space-filling patterns
- **Reaction Time**: Improve response to near-collisions
- **Strategic Planning**: Think multiple moves ahead
- **Risk Assessment**: Know when to play safe vs aggressive

---

Enjoy your lunch break gaming! 🐍🍎