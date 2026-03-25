"""Test 180-degree turn guard (§14.3)."""

from src.game import Direction


def test_guard_right_to_left(game):
    """T-GUARD-01: Cannot turn 180° from RIGHT to LEFT."""
    assert game.get_direction() == Direction.RIGHT
    
    game.tick("a")  # Try to go LEFT
    state = game.get_state()
    
    # Direction should remain RIGHT
    assert state.direction == Direction.RIGHT


def test_guard_down_to_up(game):
    """T-GUARD-02: Cannot turn 180° from DOWN to UP."""
    # First move down
    game.tick("s")
    assert game.get_direction() == Direction.DOWN
    
    # Try to move up
    game.tick("w")
    state = game.get_state()
    
    # Direction should remain DOWN
    assert state.direction == Direction.DOWN


def test_guard_perpendicular_allowed(game):
    """T-GUARD-03: Perpendicular turns are allowed."""
    assert game.get_direction() == Direction.RIGHT
    
    game.tick("w")  # Turn UP (perpendicular)
    state = game.get_state()
    
    # Direction should change to UP
    assert state.direction == Direction.UP
