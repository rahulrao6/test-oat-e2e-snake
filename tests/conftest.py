"""Shared fixtures for test suite."""

import pytest
from src.game import Game, GameConfig


@pytest.fixture
def game_factory():
    """Factory fixture for creating games with deterministic config."""
    def _create_game(seed=42, grid_width=20, grid_height=10, tick_rate=200):
        config = GameConfig(
            seed=seed,
            grid_width=grid_width,
            grid_height=grid_height,
            tick_rate=tick_rate
        )
        return Game(config)
    return _create_game


@pytest.fixture
def game(game_factory):
    """Default game instance with seed=42, 20x10 grid."""
    return game_factory()
