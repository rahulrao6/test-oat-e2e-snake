"""Non-blocking keyboard input handler for Snake game."""

import sys
import termios
import tty
from typing import Optional


class InputHandler:
    """
    Non-blocking keyboard input handler (§8).
    
    Handles raw terminal input without requiring Enter key.
    Works on Unix-like systems (macOS, Linux).
    """
    
    def __init__(self):
        """Initialize the input handler."""
        self._old_settings = None
        self._enabled = False
    
    def enable(self) -> None:
        """
        Enable raw terminal mode for non-blocking input.
        
        Must be called before reading input.
        """
        if self._enabled:
            return
        
        # Save original terminal settings
        self._old_settings = termios.tcgetattr(sys.stdin)
        
        # Set raw mode (no echo, no buffering, no special char processing)
        tty.setraw(sys.stdin.fileno())
        
        self._enabled = True
    
    def disable(self) -> None:
        """
        Restore original terminal settings.
        
        Should be called when done reading input (e.g., on exit).
        """
        if not self._enabled or self._old_settings is None:
            return
        
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)
        self._enabled = False
    
    def read_key(self) -> Optional[str]:
        """
        Read a single key press in non-blocking mode (§8).
        
        Returns immediately if no key is pressed.
        
        Supported keys:
        - WASD (w/s/a/d)
        - Arrow keys (↑/↓/←/→)
        - q (quit)
        - r (restart, for game over)
        
        Returns:
            Key string ('w', 's', 'a', 'd', 'up', 'down', 'left', 'right', 'q', 'r'),
            or None if no key pressed
        """
        if not self._enabled:
            return None
        
        # Check if input is available (non-blocking)
        import select
        if not select.select([sys.stdin], [], [], 0)[0]:
            return None
        
        # Read first character
        ch = sys.stdin.read(1)
        
        # Handle escape sequences (arrow keys)
        if ch == '\x1b':
            # Read next two chars for escape sequence
            # Arrow keys are: ESC [ A/B/C/D
            next_chars = sys.stdin.read(2)
            if next_chars == '[A':
                return 'up'
            elif next_chars == '[B':
                return 'down'
            elif next_chars == '[C':
                return 'right'
            elif next_chars == '[D':
                return 'left'
            else:
                # Unknown escape sequence
                return None
        
        # Handle regular keys
        ch_lower = ch.lower()
        if ch_lower in ('w', 's', 'a', 'd', 'q', 'r'):
            return ch_lower
        
        # Unknown key
        return None
    
    def __enter__(self):
        """Context manager entry."""
        self.enable()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disable()
        return False
