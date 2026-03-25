#!/usr/bin/env python3
"""
Simple Snake Game using curses for terminal-based gameplay.
Controls: Arrow keys to move, 'q' to quit
"""
import curses
import random
from collections import deque
from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.height -= 1  # Reserve space for score
        
        # Initialize snake in the middle
        start_y, start_x = self.height // 2, self.width // 2
        self.snake = deque([(start_y, start_x)])
        self.direction = Direction.RIGHT
        
        # Place first food
        self.food = self.place_food()
        self.score = 0
        self.game_over = False
        
        # Setup curses
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(100)  # Game speed (ms)
        
    def place_food(self):
        """Place food at random location not occupied by snake."""
        while True:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if (y, x) not in self.snake:
                return (y, x)
    
    def draw(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        # Draw snake
        for i, (y, x) in enumerate(self.snake):
            if 0 <= y < self.height and 0 <= x < self.width:
                char = 'O' if i == 0 else 'o'  # Head vs body
                self.stdscr.addch(y, x, char)
        
        # Draw food
        if 0 <= self.food[0] < self.height and 0 <= self.food[1] < self.width:
            self.stdscr.addch(self.food[0], self.food[1], '*')
        
        # Draw score
        score_text = f"Score: {self.score} | Press 'q' to quit"
        self.stdscr.addstr(self.height, 0, score_text[:self.width - 1])
        
        self.stdscr.refresh()
    
    def handle_input(self):
        """Handle keyboard input."""
        try:
            key = self.stdscr.getch()
        except:
            return
        
        if key == ord('q'):
            self.game_over = True
        elif key == curses.KEY_UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif key == curses.KEY_DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        elif key == curses.KEY_LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif key == curses.KEY_RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
    
    def update(self):
        """Update game state."""
        # Calculate new head position
        head_y, head_x = self.snake[0]
        dy, dx = self.direction.value
        new_head = (head_y + dy, head_x + dx)
        
        # Check collision with walls
        if (new_head[0] < 0 or new_head[0] >= self.height or
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.place_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def run(self):
        """Main game loop."""
        while not self.game_over:
            self.draw()
            self.handle_input()
            self.update()
        
        # Game over screen
        self.stdscr.clear()
        game_over_text = f"Game Over! Final Score: {self.score}"
        restart_text = "Press any key to exit..."
        self.stdscr.addstr(self.height // 2, (self.width - len(game_over_text)) // 2, game_over_text)
        self.stdscr.addstr(self.height // 2 + 1, (self.width - len(restart_text)) // 2, restart_text)
        self.stdscr.nodelay(0)  # Blocking input
        self.stdscr.getch()


def main(stdscr):
    game = SnakeGame(stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)
