"""Test collision detection (§14.5)."""

from src.game import Position, GameStatus


def test_wall_right(game_factory):
    """T-WALL-01: Hitting right wall causes GAME_OVER."""
    game = game_factory()
    
    # Move snake to right edge (x=19)
    while game.get_snake()[0].x < 19:
        game.tick(None)  # Move right
    
    # Next move should hit wall
    game.tick(None)
    
    assert game.get_status() == GameStatus.GAME_OVER


def test_wall_left(game_factory):
    """T-WALL-02: Hitting left wall causes GAME_OVER."""
    game = game_factory()
    
    # Turn around and move to left edge
    game.tick("w")  # Turn up first
    game.tick(None)
    game.tick("a")  # Then turn left
    
    while game.get_snake()[0].x > 0:
        game.tick(None)  # Move left
    
    # Next move should hit wall
    game.tick(None)
    
    assert game.get_status() == GameStatus.GAME_OVER


def test_wall_top(game_factory):
    """T-WALL-03: Hitting top wall causes GAME_OVER."""
    game = game_factory()
    
    # Move to top edge (y=0)
    game.tick("w")  # Turn up
    
    while game.get_snake()[0].y > 0:
        game.tick(None)  # Move up
    
    # Next move should hit wall
    game.tick(None)
    
    assert game.get_status() == GameStatus.GAME_OVER


def test_wall_bottom(game_factory):
    """T-WALL-04: Hitting bottom wall causes GAME_OVER."""
    game = game_factory()
    
    # Move to bottom edge (y=9)
    game.tick("s")  # Turn down
    
    while game.get_snake()[0].y < 9:
        game.tick(None)  # Move down
    
    # Next move should hit wall
    game.tick(None)
    
    assert game.get_status() == GameStatus.GAME_OVER


def test_self_collision(game_factory):
    """T-SELF-01: Head moving into own body causes GAME_OVER."""
    game = game_factory(seed=42)
    
    # Grow the snake first to make self-collision possible
    # We need a longer snake to reliably hit ourselves
    food_eaten = 0
    max_attempts = 100
    attempts = 0
    
    # Eat food to grow snake to length 6+
    while food_eaten < 3 and attempts < max_attempts:
        food_pos = game.get_food()
        head = game.get_snake()[0]
        
        if head.x < food_pos.x:
            game.tick("d")
        elif head.x > food_pos.x:
            game.tick("a")
        elif head.y < food_pos.y:
            game.tick("s")
        elif head.y > food_pos.y:
            game.tick("w")
        else:
            # We're at food position, it should be eaten on this tick
            game.tick(None)
            food_eaten += 1
        
        attempts += 1
    
    # Now create a self-collision: move in a square to hit our body
    # Get current position and direction
    initial_len = len(game.get_snake())
    assert initial_len >= 6, "Snake should be long enough"
    
    # Make a tight square pattern to collide with ourselves
    game.tick("w")  # Turn up
    game.tick(None)
    game.tick("a")  # Turn left
    game.tick(None)
    game.tick("s")  # Turn down
    game.tick(None)
    game.tick("s")  # Keep going down
    game.tick(None)
    game.tick("d")  # Turn right - should hit body
    game.tick(None)
    game.tick("d")  # Continue right - should hit body
    
    assert game.get_status() == GameStatus.GAME_OVER


def test_tail_chase_safe(game_factory):
    """T-SELF-02: Tail is removed before collision check, so chasing tail is safe."""
    game = game_factory()
    
    # Initial: [(2,5), (1,5), (0,5)]
    # Move in a square pattern (should be safe)
    game.tick(None)  # Right to (3,5)
    game.tick("w")   # Up to (3,4)
    game.tick("a")   # Left to (2,4)
    game.tick("s")   # Down to (2,5) - where tail was initially
    
    # Should still be running
    assert game.get_status() == GameStatus.RUNNING
