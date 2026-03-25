"""Test basic movement (§14.2)."""

from src.game import Position, Direction


def test_move_forward(game):
    """T-MOVE-01: Tick with no input moves head forward."""
    game.tick(None)
    state = game.get_state()
    
    assert state.snake[0] == Position(3, 5)
    assert len(state.snake) == 3


def test_move_up(game):
    """T-MOVE-02: Input 'w' changes direction to UP."""
    game.tick("w")
    state = game.get_state()
    
    assert state.direction == Direction.UP
    assert state.snake[0] == Position(2, 4)


def test_move_down(game):
    """T-MOVE-03: Input 's' changes direction to DOWN."""
    game.tick("s")
    state = game.get_state()
    
    assert state.direction == Direction.DOWN
    assert state.snake[0] == Position(2, 6)


def test_tail_follows(game):
    """T-MOVE-04: Tail follows head correctly."""
    game.tick(None)
    state = game.get_state()
    
    # Snake moved right, tail segment removed from back
    assert state.snake == [Position(3, 5), Position(2, 5), Position(1, 5)]
