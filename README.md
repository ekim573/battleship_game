# Battleship Game
Battleship is a simple classic strategy game, and this visual game was created using Python and Pygame. In this game, players are given limited number of ammo to find the ships and destroy them in randomly assigned hidden areas in the grid. This visual version has a sea background and a real-time update in the scoreboard of ammos, hits, and misses. Using this game, you can practice your strategies and logical skills.

## Functions and Parameters
### Grid
Create visual display on screen
* set_grid(score, ammo)
  * Display background sea image
  * Draw 10x10 grid with white lines
  * Display score and ammo on scoreboard

### Ship
Set random placement and legality of the locations of ships and display
* placement(occupied)
  * Assign random areas on grid for ships
* legal_position(position1, occupied)
  * Check if there is an overlap or the ship is out-of-bound

### Player
Tracks the player's game state
* hit
* miss
* score
* ammo

### Game
Control game status of player
* start()
  * Start the game
* end()
  * End the game by updating game state

## Testing
* Install pygame
* In the output, there should be shown a screen with 10x10 grid with a sea background and a scoreboard
* The ships will be randomly assigned correctly with no overlap or out-of-bounds
* The game will trackdown hits, misses, and ammos
* The window will close when the game is over
