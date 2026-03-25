"""Test food mechanics (§14.4)."""

from src.game import Position


def test_food_eat_grows_snake(game):
    """T-FOOD-01: Eating food increases snake length and score."""
    initial_length = len(game.get_snake())
    initial_score = game.get_score()
    food_pos = game.get_food()
    
    # Move snake to food position
    while game.get_snake()[0] != food_pos:
        # Calculate direction to food
        head = game.get_snake()[0]
        if head.x < food_pos.x:
            game.tick("d")  # Move right
        elif head.x > food_pos.x:
            game.tick("a")  # Move left
        elif head.y < food_pos.y:
            game.tick("s")  # Move down
        elif head.y > food_pos.y:
            game.tick("w")  # Move up
    
    # Verify length increased by 1 and score increased
    assert len(game.get_snake()) == initial_length + 1
    assert game.get_score() == initial_score + 1


def test_food_respawns_after_eating(game):
    """T-FOOD-02: Food respawns after being eaten, not on snake."""
    food_pos_1 = game.get_food()
    
    # Move to and eat food
    while game.get_snake()[0] != food_pos_1:
        head = game.get_snake()[0]
        if head.x < food_pos_1.x:
            game.tick("d")
        elif head.x > food_pos_1.x:
            game.tick("a")
        elif head.y < food_pos_1.y:
            game.tick("s")
        elif head.y > food_pos_1.y:
            game.tick("w")
    
    # Get new food position
    food_pos_2 = game.get_food()
    
    # Food should have respawned
    assert food_pos_2 != food_pos_1
    # Food should not be on snake
    assert food_pos_2 not in game.get_snake()


def test_food_never_on_snake(game_factory):
    """T-FOOD-03: Food never spawns on snake (fuzz test)."""
    for seed in range(100):
        game = game_factory(seed=seed)
        state = game.get_state()
        
        # Verify food not on initial snake
        assert state.food not in state.snake


def test_multiple_food_eats(game):
    """T-FOOD-04: Eating 3 times increases score to 3."""
    for _ in range(3):
        food_pos = game.get_food()
        
        # Move to food
        max_moves = 50  # Prevent infinite loops
        moves = 0
        while game.get_snake()[0] != food_pos and moves < max_moves:
            head = game.get_snake()[0]
            if head.x < food_pos.x:
                game.tick("d")
            elif head.x > food_pos.x:
                game.tick("a")
            elif head.y < food_pos.y:
                game.tick("s")
            elif head.y > food_pos.y:
                game.tick("w")
            moves += 1
    
    assert game.get_score() == 3
