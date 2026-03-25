"""Integration test scenarios (§14.8)."""

from src.game import GameStatus, Position


def test_scenario_short_game(game_factory):
    """T-SCENARIO-01: Full short game - move, eat, wall death."""
    # Use small grid for faster test
    game = game_factory(grid_width=5, grid_height=3)
    
    # Initial state
    assert game.get_status() == GameStatus.RUNNING
    initial_score = game.get_score()
    
    # Move a bit
    game.tick(None)  # Move right
    game.tick(None)  # Move right
    
    # Try to eat food if nearby
    food_pos = game.get_food()
    attempts = 0
    max_attempts = 10
    while game.get_snake()[0] != food_pos and attempts < max_attempts and game.get_status() == GameStatus.RUNNING:
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
            game.tick(None)
        attempts += 1
    
    # If we ate food, score should increase
    if game.get_score() > initial_score:
        assert game.get_score() == initial_score + 1
    
    # Force wall collision
    game.tick("d")  # Turn right
    while game.get_status() == GameStatus.RUNNING:
        game.tick(None)  # Keep moving right until wall hit
    
    # Should be game over
    assert game.get_status() == GameStatus.GAME_OVER


def test_scenario_u_turn(game):
    """T-SCENARIO-02: Navigate a U-turn with 3 direction changes."""
    # Initial: moving RIGHT at (2,5)
    # Execute: RIGHT -> UP -> LEFT -> DOWN (U-turn)
    
    initial_pos = game.get_snake()[0]
    
    # Move right
    game.tick(None)
    assert game.get_snake()[0] == Position(initial_pos.x + 1, initial_pos.y)
    
    # Turn up
    game.tick("w")
    assert game.get_snake()[0].y == initial_pos.y - 1
    
    # Turn left
    game.tick("a")
    assert game.get_snake()[0].x == initial_pos.x
    
    # Turn down
    game.tick("s")
    assert game.get_snake()[0].y == initial_pos.y
    
    # Should still be running
    assert game.get_status() == GameStatus.RUNNING


def test_scenario_consecutive_food(game_factory):
    """T-SCENARIO-03: Grow twice in a row with consecutive food eats."""
    game = game_factory(seed=50)  # Different seed for different food positions
    
    initial_length = len(game.get_snake())
    
    # Eat first food
    food_1 = game.get_food()
    max_moves = 50
    moves = 0
    while game.get_snake()[0] != food_1 and moves < max_moves and game.get_status() == GameStatus.RUNNING:
        head = game.get_snake()[0]
        if head.x < food_1.x:
            game.tick("d")
        elif head.x > food_1.x:
            game.tick("a")
        elif head.y < food_1.y:
            game.tick("s")
        elif head.y > food_1.y:
            game.tick("w")
        else:
            game.tick(None)
        moves += 1
    
    length_after_first = len(game.get_snake())
    assert length_after_first == initial_length + 1
    
    # Eat second food immediately
    food_2 = game.get_food()
    moves = 0
    while game.get_snake()[0] != food_2 and moves < max_moves and game.get_status() == GameStatus.RUNNING:
        head = game.get_snake()[0]
        if head.x < food_2.x:
            game.tick("d")
        elif head.x > food_2.x:
            game.tick("a")
        elif head.y < food_2.y:
            game.tick("s")
        elif head.y > food_2.y:
            game.tick("w")
        else:
            game.tick(None)
        moves += 1
    
    length_after_second = len(game.get_snake())
    assert length_after_second == initial_length + 2
    assert game.get_score() == 2
