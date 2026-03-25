# Bug Fixes

## Critical Bug: Blocking Input on Arrow Keys

### Location
`src/input.py`, lines 79-93 (original)

### Problem
The `read_key()` method was performing a **blocking read** when handling escape sequences for arrow keys. After detecting the ESC character (`\x1b`), the code would call `sys.stdin.read(2)` which blocks until 2 characters are available.

This violated the non-blocking contract of the `InputHandler` class and caused the game to freeze when:
- Arrow keys were pressed
- Incomplete escape sequences were received
- Any ESC key was pressed without a complete arrow key sequence

### Impact
1. **Keyboard input not responding correctly**: Arrow keys would cause the game to hang
2. **Food eating logic appearing broken**: The frozen game loop prevented smooth gameplay, making it seem like the food eating logic wasn't working

### Solution
Modified the escape sequence handling to use non-blocking reads with `select.select()`:
- Check if input is available before reading each character
- Return `None` for incomplete escape sequences instead of blocking
- Maintains the real-time, non-blocking behavior required for smooth gameplay

### Code Changes
```python
# Before (blocking):
if ch == '\x1b':
    next_chars = sys.stdin.read(2)  # BLOCKS until 2 chars available
    if next_chars == '[A':
        return 'up'
    # ...

# After (non-blocking):
if ch == '\x1b':
    if select.select([sys.stdin], [], [], 0)[0]:
        next_char1 = sys.stdin.read(1)
        if next_char1 == '[' and select.select([sys.stdin], [], [], 0)[0]:
            next_char2 = sys.stdin.read(1)
            if next_char2 == 'A':
                return 'up'
            # ...
    return None  # Incomplete sequence, don't block
```

## Testing
All existing tests pass. The fix maintains backward compatibility while solving the blocking issue.
