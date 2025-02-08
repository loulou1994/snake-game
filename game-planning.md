## MAIN COMPONENTS:
- [ ] Snake movement system
- [ ] Input handling
- [ ] Collision system
- [ ] Game mechanics (food, scoring)
- [ ] Game state management

## SNAKE MOVEMENT \(pseudocode):
### Initialize snake:
- Create head at starting position
- Create initial body segments
- Set starting direction

### Movement function:
- Save all current segment positions
- Move head in current direction
- For each body segment:
    - Move to previous position of segment ahead

### INPUT HANDLING:
- When key pressed:
    - If arrow key:
        - If new direction isn't opposite of current:
           - Update direction
    - If pause key:
        - - Toggle game pause

### COLLISION SYSTEM:
- Check wall collision:
    - If snake head position outside boundaries:
        - Return collision true

- Check self collision:
    - For each body segment:
        - If head overlaps segment:
            - Return collision true

- Check food collision:
    - If head overlaps food:
        - Grow snake
        - Spawn new food
        - Update score

### GAME MECHANICS:
- Spawn food:
    - Generate random position
    - While position overlaps snake:
        - Generate new position
    - Place food

- Grow snake:
    - Add new segment at tail position
    - Update score

### GAME STATE:
- Main game loop:
    - While game running:
        - Handle input
        - If not paused:
            - Move snake
            - Check collisions
            - If collision with wall or self:
                - Game over
            - If collision with food:
                - Grow snake
            - Update display
        - Update score display