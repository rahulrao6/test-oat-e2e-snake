"""Core game engine for Snake game."""

import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


# Game Constants (§2)
GRID_WIDTH = 20
GRID_HEIGHT = 10
INITIAL_SNAKE_LEN = 3
TICK_RATE_MS = 200


@dataclass(frozen=True)
class Position:
    """Position in the grid (§3, §4)."""
    x: int
    y: int
    
    def __add__(self, other: 'Position') -> 'Position':
        """Add two positions (for direction deltas)."""
        return Position(self.x + other.x, self.y + other.y)


class Direction(Enum):
    """Direction enum with delta vectors (§4)."""
    UP = Position(0, -1)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)
    
    def opposite(self) -> 'Direction':
        """Return the opposite direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]


class GameStatus(Enum):
    """Game status (§4)."""
    RUNNING = "running"
    GAME_OVER = "game_over"
    WIN = "win"


@dataclass
class GameState:
    """Complete game state (§4)."""
    snake: List[Position]
    direction: Direction
    food: Position
    score: int
    status: GameStatus


@dataclass
class GameConfig:
    """Game configuration (§12)."""
    seed: Optional[int] = None
    grid_width: int = GRID_WIDTH
    grid_height: int = GRID_HEIGHT
    tick_rate: int = TICK_RATE_MS


class Game:
    """Main game class (§5, §6, §13)."""
    
    def __init__(self, config: Optional[GameConfig] = None):
        """Initialize the game (§5)."""
        self.config = config or GameConfig()
        self._rng = random.Random(self.config.seed)
        self._state = self._initialize_state()
        self._pending_direction: Optional[Direction] = None
    
    def _initialize_state(self) -> GameState:
        """Initialize game state (§5)."""
        # Calculate vertical center
        vertical_center = self.config.grid_height // 2
        
        # Place snake horizontally at vertical center: head at (2, center), body at (1, center) and (0, center)
        snake = [
            Position(2, vertical_center),
            Position(1, vertical_center),
            Position(0, vertical_center),
        ]
        
        # Initial direction is RIGHT
        direction = Direction.RIGHT
        
        # Spawn initial food
        food = self._spawn_food(snake)
        
        return GameState(
            snake=snake,
            direction=direction,
            food=food,
            score=0,
            status=GameStatus.RUNNING
        )
    
    def _spawn_food(self, snake: List[Position]) -> Position:
        """Spawn food on a random unoccupied cell (§7)."""
        # Get all occupied positions
        occupied = set(snake)
        
        # Get all possible positions
        all_positions = [
            Position(x, y)
            for x in range(self.config.grid_width)
            for y in range(self.config.grid_height)
        ]
        
        # Filter out occupied positions
        available = [pos for pos in all_positions if pos not in occupied]
        
        # If no empty cells, return dummy position (WIN condition handled in tick)
        if not available:
            return Position(-1, -1)  # Dummy position
        
        # Pick random unoccupied cell
        return self._rng.choice(available)
    
    def tick(self, input_key: Optional[str] = None) -> None:
        """Execute one game tick (§6, §12)."""
        if self._state.status != GameStatus.RUNNING:
            return
        
        # Step 1: READ INPUT → update direction (with 180° guard)
        if input_key:
            new_direction = self._parse_input(input_key)
            if new_direction and new_direction != self._state.direction.opposite():
                self._pending_direction = new_direction
        
        # Apply pending direction change
        if self._pending_direction:
            self._state.direction = self._pending_direction
            self._pending_direction = None
        
        # Step 2: COMPUTE NEXT HEAD
        current_head = self._state.snake[0]
        new_head = current_head + self._state.direction.value
        
        # Step 3: CHECK WALL HIT
        if not self._is_in_bounds(new_head):
            self._state.status = GameStatus.GAME_OVER
            return
        
        # Step 4: CHECK SELF HIT (check against snake[0..n-2], excluding tail)
        if new_head in self._state.snake[:-1]:
            self._state.status = GameStatus.GAME_OVER
            return
        
        # Step 5: CHECK FOOD
        ate_food = (new_head == self._state.food)
        if ate_food:
            self._state.score += 1
            # Don't remove tail (snake grows)
        else:
            # Remove tail (snake moves)
            self._state.snake.pop()
        
        # Step 6: INSERT new_head at front
        self._state.snake.insert(0, new_head)
        
        # Respawn food if eaten
        if ate_food:
            new_food = self._spawn_food(self._state.snake)
            if new_food == Position(-1, -1):  # No empty cells
                self._state.status = GameStatus.WIN
            else:
                self._state.food = new_food
    
    def _parse_input(self, key: str) -> Optional[Direction]:
        """Parse input key to direction."""
        key_map = {
            'w': Direction.UP,
            's': Direction.DOWN,
            'a': Direction.LEFT,
            'd': Direction.RIGHT,
            'up': Direction.UP,
            'down': Direction.DOWN,
            'left': Direction.LEFT,
            'right': Direction.RIGHT,
        }
        return key_map.get(key.lower())
    
    def _is_in_bounds(self, pos: Position) -> bool:
        """Check if position is within grid bounds."""
        return (0 <= pos.x < self.config.grid_width and
                0 <= pos.y < self.config.grid_height)
    
    # Public API (§13)
    
    def get_state(self) -> GameState:
        """Get the complete game state."""
        return self._state
    
    def get_snake(self) -> List[Position]:
        """Get the snake positions (head-first)."""
        return self._state.snake.copy()
    
    def get_food(self) -> Position:
        """Get the food position."""
        return self._state.food
    
    def get_score(self) -> int:
        """Get the current score."""
        return self._state.score
    
    def get_status(self) -> GameStatus:
        """Get the game status."""
        return self._state.status
    
    def get_direction(self) -> Direction:
        """Get the current direction."""
        return self._state.direction
    
    def render(self) -> str:
        """Render the game (stub for now, renderer is separate ticket)."""
        return ""
