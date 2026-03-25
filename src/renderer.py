"""ASCII renderer for Snake game."""

from typing import Set
from src.game import GameState, GameStatus, Position, GRID_WIDTH, GRID_HEIGHT


# Character constants (§9)
WALL_CHAR = '#'
SNAKE_HEAD_CHAR = '@'
SNAKE_BODY_CHAR = 'o'
FOOD_CHAR = '*'
EMPTY_CHAR = ' '

# ANSI escape codes (§15)
CURSOR_HOME = '\033[H'


def render(game_state: GameState) -> str:
    """
    Render the game state as an ASCII string (§9).
    
    Frame layout:
    - Score header (blank line + score line)
    - Grid with walls (GRID_HEIGHT + 2 rows, GRID_WIDTH + 2 cols)
    - Controls footer
    
    Args:
        game_state: Current game state
        
    Returns:
        Complete ASCII frame string with cursor-home escape
    """
    lines = []
    
    # Header: blank line + score
    lines.append('')
    lines.append(f'Score: {game_state.score}')
    lines.append('')
    
    # Build lookup sets for efficient rendering
    snake_positions: Set[Position] = set(game_state.snake)
    head_position: Position = game_state.snake[0] if game_state.snake else Position(-1, -1)
    food_position: Position = game_state.food
    
    # Top wall
    lines.append(WALL_CHAR * (GRID_WIDTH + 2))
    
    # Grid rows
    for y in range(GRID_HEIGHT):
        row = WALL_CHAR
        for x in range(GRID_WIDTH):
            pos = Position(x, y)
            # Render priority: Head > Body > Food > Empty
            if pos == head_position:
                row += SNAKE_HEAD_CHAR
            elif pos in snake_positions:
                row += SNAKE_BODY_CHAR
            elif pos == food_position:
                row += FOOD_CHAR
            else:
                row += EMPTY_CHAR
        row += WALL_CHAR
        lines.append(row)
    
    # Bottom wall
    lines.append(WALL_CHAR * (GRID_WIDTH + 2))
    
    # Footer
    if game_state.status == GameStatus.GAME_OVER:
        lines.append('')
        lines.append('GAME OVER')
        lines.append(f'Final Score: {game_state.score}')
        lines.append('[Q] Quit  [R] Restart')
    elif game_state.status == GameStatus.WIN:
        lines.append('')
        lines.append('YOU WIN!')
        lines.append(f'Final Score: {game_state.score}')
        lines.append('[Q] Quit  [R] Restart')
    else:
        lines.append('')
        lines.append('[WASD] Move  [Q] Quit')
    
    # Join all lines and prepend cursor home escape
    frame = '\n'.join(lines)
    return CURSOR_HOME + frame
