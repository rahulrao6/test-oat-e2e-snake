"""Test initial game state (§14.1)."""

from src.game import Position, Direction, GameStatus


def test_init_state(game):
    """T-INIT-01: Initial snake, direction, score, and status."""
    state = game.get_state()
    
    assert state.snake == [Position(2, 5), Position(1, 5), Position(0, 5)]
    assert state.direction == Direction.RIGHT
    assert state.score == 0
    assert state.status == GameStatus.RUNNING


def test_init_food_valid(game):
    """T-INIT-02: Food spawns off snake, within bounds."""
    state = game.get_state()
    food = state.food
    
    # Food not on snake
    assert food not in state.snake
    
    # Food within bounds
    assert 0 <= food.x < 20
    assert 0 <= food.y < 10


def test_init_custom_grid(game_factory):
    """T-INIT-03: Custom grid size validated."""
    game = game_factory(grid_width=5, grid_height=3)
    state = game.get_state()
    food = state.food
    
    # Verify food within custom bounds
    assert 0 <= food.x < 5
    assert 0 <= food.y < 3
    
    # Verify snake is positioned correctly within custom bounds
    for segment in state.snake:
        assert 0 <= segment.x < 5
        assert 0 <= segment.y < 3
