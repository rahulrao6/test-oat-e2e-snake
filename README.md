# Snake Game

A classic Snake game implemented in Python with ASCII terminal rendering.

## Overview

This is a real-time Snake game that runs in your terminal. Control the snake to eat food, grow longer, and avoid hitting walls or yourself. The game features:

- Real-time keyboard input (no need to press Enter)
- Consistent 200ms tick rate for smooth gameplay
- ASCII rendering with ANSI escape codes
- Game over detection and restart functionality

## How to Run

Run the game with:

```bash
python src/main.py
```

Or using Python's module syntax:

```bash
python -m src.main
```

## Controls

- **WASD** or **Arrow Keys**: Control snake direction
  - `W` / `↑`: Move up
  - `S` / `↓`: Move down
  - `A` / `←`: Move left
  - `D` / `→`: Move right
- **Q**: Quit game
- **R**: Restart (available after game over)

## How to Run Tests

Run the test suite with:

```bash
python -m pytest tests/
```

Run tests with verbose output:

```bash
python -m pytest tests/ -v
```

## Architecture

The game is organized into modular components:

- **`src/game.py`**: Core game engine
  - Game state management
  - Snake movement and collision detection
  - Food spawning logic
  - Tick-based game loop

- **`src/renderer.py`**: ASCII rendering
  - Converts game state to ASCII frames
  - Uses ANSI escape codes for efficient terminal updates
  - Displays score, game status, and controls

- **`src/input.py`**: Non-blocking keyboard input
  - Raw terminal mode for real-time input
  - Supports WASD and arrow keys
  - Cross-platform (Unix/Linux/macOS)

- **`src/main.py`**: Main entry point
  - Coordinates game loop timing
  - Manages terminal setup and cleanup
  - Handles game over and restart logic

## Requirements

- Python 3.7+
- Unix-like terminal (Linux, macOS) or Windows Terminal
- pytest (for running tests)

## Game Rules

- The snake starts at length 3 and moves continuously
- Eating food (`*`) increases score and snake length
- Hitting walls (`#`) or yourself (`o`) ends the game
- Fill the entire grid to win!
