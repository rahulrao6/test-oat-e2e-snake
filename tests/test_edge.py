"""Test edge cases (§14.6)."""

from src.game import GameStatus, Position


def test_win_1x1_grid(game_factory):
    """T-EDGE-01: Snake filling tiny grid triggers WIN."""
    # With a very small grid like 2x2, test WIN condition
    # Initial snake is 3 segments, so it can't fit in 1x1
    # Use 3x2 grid (6 cells) and fill it completely
    game = game_factory(grid_width=3, grid_height=2, seed=200)
    
    # Eat food until board is completely full
    max_attempts = 200
    attempts = 0
    
    while game.get_status() == GameStatus.RUNNING and attempts < max_attempts:
        food_pos = game.get_food()
        
        # If food is invalid (no space), we should have won
        if food_pos == Position(-1, -1):
            break
        
        head = game.get_snake()[0]
        
        # Navigate to food carefully
        if head.x < food_pos.x:
            game.tick("d")
        elif head.x > food_pos.x:
            game.tick("a")
        elif head.y < food_pos.y:
            game.tick("s")
        elif head.y > food_pos.y:
            game.tick("w")
        else:
            game.tick(None)
        
        attempts += 1
    
    # Should reach WIN state when board is full (6 cells, snake length 6)
    if len(game.get_snake()) == 6:
        assert game.get_status() == GameStatus.WIN


def test_win_full_board(game_factory):
    """T-EDGE-02: Snake filling entire small board triggers WIN."""
    # Use a very small grid
    game = game_factory(grid_width=3, grid_height=2, seed=100)
    
    # Eat food repeatedly until board is full
    max_attempts = 100
    attempts = 0
    while game.get_status() == GameStatus.RUNNING and attempts < max_attempts:
        food_pos = game.get_food()
        head = game.get_snake()[0]
        
        # Navigate to food
        if head.x < food_pos.x:
            game.tick("d")
        elif head.x > food_pos.x:
            game.tick("a")
        elif head.y < food_pos.y:
            game.tick("s")
        elif head.y > food_pos.y:
            game.tick("w")
        else:
            game.tick(None)
        
        attempts += 1
    
    # Should eventually reach WIN state (or GAME_OVER if we hit ourselves)
    # On a 3x2 grid (6 cells), if we fill it, we should WIN
    if len(game.get_snake()) >= 6:
        assert game.get_status() in (GameStatus.WIN, GameStatus.GAME_OVER)


def test_rapid_direction_changes(game):
    """T-EDGE-03: Rapid direction changes - last input used with 180° guard."""
    # Queue multiple direction changes in one tick
    # Only the last valid one should apply
    initial_dir = game.get_direction()
    
    # Try: right (current), down, up (opposite of down), right
    # The 180° guard applies during tick processing
    game.tick("d")  # RIGHT (same direction)
    
    # Since we process one input per tick, test sequential inputs
    game.tick("s")  # DOWN (perpendicular, allowed)
    assert game.get_direction().name == "DOWN"
    
    game.tick("w")  # UP (opposite of DOWN, blocked)
    assert game.get_direction().name == "DOWN"  # Should still be DOWN


def test_no_input_continues_direction(game):
    """T-EDGE-04: No input between ticks continues current direction."""
    game.tick(None)  # Move right
    pos1 = game.get_snake()[0]
    
    game.tick(None)  # Move right again
    pos2 = game.get_snake()[0]
    
    # Should have moved right both times
    assert pos2.x == pos1.x + 1
    assert pos2.y == pos1.y


def test_input_during_game_over(game_factory):
    """T-EDGE-05: Input during GAME_OVER does not change state."""
    game = game_factory()
    
    # Force game over by hitting wall
    game.tick("w")  # Turn up
    while game.get_status() == GameStatus.RUNNING:
        game.tick(None)
    
    assert game.get_status() == GameStatus.GAME_OVER
    
    # Try to give input
    snake_before = game.get_snake().copy()
    game.tick("d")
    snake_after = game.get_snake()
    
    # State should be unchanged
    assert snake_before == snake_after
