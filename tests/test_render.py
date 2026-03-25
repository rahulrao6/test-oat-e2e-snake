"""Test rendering (§14.7)."""

from src.renderer import render, CURSOR_HOME
from src.game import GameStatus, Position


def test_render_initial_frame_structure(game):
    """T-RENDER-01: Initial frame has correct structure."""
    state = game.get_state()
    frame = render(state)
    
    # Remove ANSI cursor home escape
    if frame.startswith(CURSOR_HOME):
        frame = frame[len(CURSOR_HOME):]
    
    lines = frame.split('\n')
    
    # Check structure:
    # Line 0: blank
    # Line 1: "Score: 0"
    # Line 2: blank
    # Line 3: top wall (22 chars for 20-wide grid)
    # Lines 4-13: 10 interior lines
    # Line 14: bottom wall
    # Line 15+: controls
    
    assert lines[0] == ''
    assert lines[1] == 'Score: 0'
    assert lines[2] == ''
    assert len(lines[3]) == 22  # Top wall
    assert lines[3].startswith('#') and lines[3].endswith('#')
    
    # Check 10 interior lines (indices 4-13)
    for i in range(4, 14):
        assert len(lines[i]) == 22
        assert lines[i].startswith('#') and lines[i].endswith('#')
    
    # Bottom wall
    assert len(lines[14]) == 22


def test_render_snake_positions(game):
    """T-RENDER-02: Snake appears at correct positions."""
    state = game.get_state()
    frame = render(state)
    
    # Remove ANSI escape
    if frame.startswith(CURSOR_HOME):
        frame = frame[len(CURSOR_HOME):]
    
    lines = frame.split('\n')
    
    # Snake is at [(2,5), (1,5), (0,5)]
    # In rendered frame:
    # - Line index = y + 4 (skip blank, score, blank, top wall)
    # - Char index = x + 1 (skip left wall)
    
    # Head at (2, 5)
    assert lines[5 + 4][2 + 1] == '@'  # Head marker
    
    # Body at (1, 5) and (0, 5)
    assert lines[5 + 4][1 + 1] == 'o'  # Body marker
    assert lines[5 + 4][0 + 1] == 'o'  # Body marker


def test_render_food_position(game):
    """T-RENDER-03: Food appears at correct position."""
    state = game.get_state()
    food = state.food
    frame = render(state)
    
    # Remove ANSI escape
    if frame.startswith(CURSOR_HOME):
        frame = frame[len(CURSOR_HOME):]
    
    lines = frame.split('\n')
    
    # Food position in rendered frame
    food_line_index = food.y + 4
    food_char_index = food.x + 1
    
    assert lines[food_line_index][food_char_index] == '*'


def test_render_game_over(game_factory):
    """T-RENDER-04: Game over overlay contains correct text."""
    game = game_factory()
    
    # Force game over
    game.tick("w")
    while game.get_status() == GameStatus.RUNNING:
        game.tick(None)
    
    state = game.get_state()
    frame = render(state)
    
    # Check for game over text
    assert 'GAME OVER' in frame
    assert f'Final Score: {state.score}' in frame
    assert '[Q] Quit' in frame and '[R] Restart' in frame
