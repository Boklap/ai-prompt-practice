# Game Documentation

## Overview

Snake Game is a terminal-based recreation of the classic Snake arcade game, specifically designed for software engineers and IT professionals looking for a quick mental break during lunch hours. The game combines nostalgic gameplay with modern design principles and smooth performance.

## Game Concept

### Target Audience
- **Primary**: Software engineers, web developers, mobile app developers
- **Setting**: Office lunch breaks (13:00-14:00 timeframe)
- **Experience**: Refreshing, engaging, but not time-consuming

### Design Philosophy
- **Quick Sessions**: Games typically last 2-10 minutes
- **Low Cognitive Load**: Easy to learn, difficult to master
- **Professional Aesthetic**: Clean, minimalist design appealing to tech mindset
- **Instant Replayability**: No long-term commitment or complex setup

## Gameplay Mechanics

### Core Objective
Navigate a snake to eat apples and grow as large as possible without hitting walls or the snake's own body. The ultimate goal is to fill the entire playable area.

### Movement System
- **Controls**: WASD keys for directional movement
- **Physics**: Snake moves continuously in chosen direction
- **Speed Boost**: Hold spacebar for 1.2x speed increase
- **Constraints**: Cannot reverse direction (180° turns prohibited)

### Scoring System
- **Points**: 10 points per apple eaten
- **High Score**: Persistent tracking across sessions
- **Victory Bonus**: Special recognition for completing the game

### Win/Lose Conditions

**Win Condition**:
- Snake fills entire playable area (30 × 16 = 480 cells)
- All empty space consumed by snake body

**Lose Conditions**:
- **Wall Collision**: Snake head hits boundary walls
- **Self Collision**: Snake head hits any body segment

## Game Elements

### Snake
- **Appearance**: Solid block character (█)
- **Head**: Bright green color for visibility
- **Body**: Standard green color
- **Growth**: Body extends by one segment per apple eaten
- **Movement**: Smooth, grid-based motion

### Apples (Food)
- **Appearance**: Special character (Ó) in bright red
- **Quantity**: Up to 3 apples simultaneously
- **Placement**: Random empty positions
- **Respawn**: New apple appears immediately when eaten
- **Scarcity**: Decreases as snake grows larger

### Game Board
- **Dimensions**: 32×18 playable cells
- **Boundaries**: Decorative wall characters (╭╮╰╯│─)
- **Positioning**: Centered in standard 80×24 terminal
- **Background**: Empty space for snake movement

## User Interface

### Main Menu
- **Design**: Vertical menu list with snake/apple themed artwork
- **Options**: 
  - PLAY (Start new game)
  - EXIT (Quit application)
- **Navigation**: W/S keys to move, Enter to select
- **Visual Feedback**: Highlighted current selection

### Game Screen
- **Layout**: 
  - Top: Score display (current + high score)
  - Center: Game board with walls and gameplay area
  - Bottom: Empty for clean appearance
- **Color Scheme**: 
  - Snake head: Bright green
  - Snake body: Standard green
  - Apples: Bright red
  - Walls: Default terminal color
  - Text: Yellow for scores, white for messages

### Game Over Screens
**Lose Screen**:
- Message: "YOU LOSE" in bright red
- Final score display
- High score notification (if applicable)
- Return instruction: "Press ENTER to return to menu"

**Win Screen**:
- Message: "YOU WIN!" in bright green
- Final score display
- High score celebration
- Return instruction: "Press ENTER to return to menu"

## Controls Reference

### Menu Navigation
- **W/Up Arrow**: Move selection up
- **S/Down Arrow**: Move selection down
- **Enter**: Select highlighted option

### Gameplay Controls
- **W**: Move snake up
- **A**: Move snake left
- **S**: Move snake down
- **D**: Move snake right
- **Spacebar (Hold)**: Speed boost (1.2x faster)
- **Enter**: Return to menu (after game ends)

## Difficulty Progression

### Early Game
- **Challenge**: Learning controls and basic movement
- **Strategy**: Focus on collecting apples safely
- **Risk**: Low - plenty of open space

### Mid Game
- **Challenge**: Avoiding self-collision as snake grows
- **Strategy**: Plan efficient paths and avoid trapping
- **Risk**: Moderate - limited space for maneuvering

### Late Game
- **Challenge**: Precise movement in confined spaces
- **Strategy**: Methodical space filling patterns
- **Risk**: High - single mistake ends game

## Strategy Guide

### Beginner Tips
1. **Start Slow**: Focus on control familiarity before speed
2. **Plan Ahead**: Look 2-3 moves ahead, not just immediate next move
3. **Use Edges**: Walls provide temporary safety boundaries
4. **Avoid Center**: Early game center movement increases collision risk

### Intermediate Strategies
1. **Spiral Patterns**: Create efficient space-filling spirals
2. **Corridor Creation**: Leave escape routes when filling areas
3. **Speed Management**: Use boost for quick escapes, not routine movement
4. **Food Priority**: Target apples that open up new areas

### Advanced Techniques
1. **Reverse Planning**: Work backwards from desired end position
2. **Body Management**: Use snake body as temporary walls
3. **Optimal Paths**: Calculate most efficient apple collection routes
4. **Risk Assessment**: Evaluate each move's collision probability

## Psychological Elements

### Flow State
- **Balance**: Challenge matches skill level
- **Clear Goals**: Immediate objectives (eat apple) and long-term (fill board)
- **Immediate Feedback**: Visual and score feedback for actions
- **Loss of Self-Awareness**: Engaging enough to distract from work stress

### Stress Relief
- **Predictable Rules**: Consistent physics and behavior
- **Control**: Player has complete agency over outcomes
- **Achievement**: Progressive skill improvement visible
- **Break Duration**: Natural game length matches lunch break timing

## Technical Features

### Performance
- **Frame Rate**: Smooth 60 FPS rendering
- **Input Latency**: < 16ms response time
- **No Lag**: Optimized rendering prevents flickering
- **Resource Usage**: Minimal CPU and memory footprint

### Accessibility
- **Color Blind Friendly**: High contrast between elements
- **Clear Symbols**: Distinct characters for all game elements
- **Simple Controls**: Single-hand operation possible
- **Visual Clarity**: Large, readable text and symbols

## Game Balance

### Difficulty Curve
- **Gentle Start**: Low initial difficulty allows learning
- **Gradual Increase**: Difficulty scales with snake length
- **Plateau Points**: Brief difficulty rests during food collection
- **End Game Challenge**: Maximum difficulty requires precision

### Risk/Reward
- **Speed Boost**: Faster movement but reduced reaction time
- **Multiple Foods**: More scoring opportunities but increased complexity
- **Edge Hugging**: Safer movement but limited growth potential
- **Center Control**: Higher risk but better board coverage

## Session Structure

### Typical Game Length
- **Beginner**: 2-5 minutes (early collision)
- **Intermediate**: 5-10 minutes (mid-game mistakes)
- **Expert**: 10-15 minutes (completion or late-game precision)

### Lunch Break Integration
- **Quick Start**: Immediate gameplay from menu
- **Natural Pauses**: Game over provides clean break points
- **Multiple Sessions**: 2-3 games possible within lunch hour
- **Progress Tracking**: High score provides continuity

## Cultural References

### Tech Industry Appeal
- **Terminal Aesthetic**: Familiar environment for developers
- **Minimalist Design**: Appreciation for clean, efficient interfaces
- **Performance Focus**: Optimized code appeals to engineering mindset
- **Retro Gaming**: Nostalgia for early computer games

### Office Culture Integration
- **Lunch Break Activity**: Socially acceptable break time activity
- **Stress Relief**: Mental reset between work sessions
- **Skill Development**: Pattern recognition and strategic thinking
- **Community**: High score competition among colleagues

---

This game documentation provides comprehensive understanding of the game design, mechanics, and player experience for both players and developers.