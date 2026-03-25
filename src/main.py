"""Main entry point for Snake game."""

import sys
import time
from typing import Optional

from src.game import Game, GameConfig, GameStatus, TICK_RATE_MS
from src.input import InputHandler
from src.renderer import render


def main() -> None:
    """
    Run the Snake game.
    
    Entry point that:
    1. Initializes Game with default config
    2. Sets up terminal for raw/non-blocking input
    3. Runs game loop at TICK_RATE_MS intervals
    4. Handles game over and restart
    5. Restores terminal on exit
    """
    # Initialize input handler
    input_handler = InputHandler()
    
    try:
        # Enable raw terminal mode
        input_handler.enable()
        
        # Clear screen initially
        print('\033[2J\033[H', end='', flush=True)
        
        # Game loop (supports restart)
        running = True
        while running:
            # Initialize game
            game = Game(GameConfig())
            
            # Main game loop
            game_running = True
            while game_running:
                # Get start time for consistent tick rate
                tick_start = time.time()
                
                # Read input (non-blocking)
                key = input_handler.read_key()
                
                # Check for quit command
                if key == 'q':
                    running = False
                    game_running = False
                    break
                
                # Get current game status
                status = game.get_status()
                
                if status == GameStatus.RUNNING:
                    # Update game state
                    game.tick(key)
                    
                    # Render frame
                    frame = render(game.get_state())
                    print(frame, end='', flush=True)
                    
                elif status in (GameStatus.GAME_OVER, GameStatus.WIN):
                    # Game over - render final state
                    frame = render(game.get_state())
                    print(frame, end='', flush=True)
                    
                    # Wait for quit or restart
                    restart_key = None
                    while restart_key not in ('q', 'r'):
                        restart_key = input_handler.read_key()
                        time.sleep(0.01)  # Small sleep to avoid busy waiting
                    
                    if restart_key == 'q':
                        running = False
                        game_running = False
                    elif restart_key == 'r':
                        # Clear screen for restart
                        print('\033[2J\033[H', end='', flush=True)
                        game_running = False  # Exit inner loop to restart
                
                # Sleep to maintain consistent tick rate
                elapsed = time.time() - tick_start
                sleep_time = (TICK_RATE_MS / 1000.0) - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
    
    finally:
        # Restore terminal settings
        input_handler.disable()
        # Move cursor to bottom and print newline for clean exit
        print('\n', flush=True)


if __name__ == '__main__':
    main()
