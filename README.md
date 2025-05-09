# Battleship Game
Battleship is a simple classic strategy game, and this visual game was created using Python and Pygame. In this game, players are given limited number of ammo to find the ships and destroy them in randomly assigned hidden areas in the grid. This visual version has a sea background and a real-time update in the scoreboard of ammos, hits, and misses. Using this game, you can practice your strategies and logical skills.

## Functions and Parameters
### Grid
Create visual game display on screen
* Set screen_size = (800, 900)
* set_grid(score, ammo)
  * Set grid_screen = (800, 800)
  * Set score_screen = (800, 100)
  * Display background sea image
  * Draw 10x10 grid with white lines
  * Display score and ammo on scoreboard
  * Display sunk ships correctly rotated and scaled
  
### Ship
Set random placement and legality of the locations of ships and display
* placement(occupied)
  * Assign random areas on grid for ships
* is_sunk()
  * Check if all parts of the ship are hit
* legal_position(position1, occupied)
  * Check if there is an overlap or the ship is out-of-bound
* load_image()
  * Load the ship image from battlehsip_images

### Player
Tracks the player's game state and numbers
* hit
* miss
* score
* ammo

### GameState
Define status of the game
* RUNNING: Game is active
* GAME_OVER: Game ended

### Game
Control overall game status and play
* start_screen()
  * Display instructions
  * Display score instructions
  * Display example of game screen
  * Start button
    * When the button is clicked, move to the game screen
* run()
  * Start the game
  * Using the mouse, the player will choose certain grids on the screen
  * Track down which grids are chosen
  * If miss, add the miss_image with miss_sound
  * If hit, add the hit_image and hit_sound
  * When ammo=0, change game status to end
* end()
  * End the game by updating game state
  * When the ends, the screen will move to the game over sreen
  * Show the total score
  * The game will exit automatically

## Testing
* Install pygame
* Download battleship_images and sound file
* Start of the game, there should be a start screen with information about the game and a start button
* After pressing the start button, a screen with 10x10 grid with a sea background and a scoreboard will appear
* The ships will be randomly assigned correctly with no overlap or out-of-bounds
* The game will trackdown hits, misses, and ammo
* Miss: x image with a miss sound
* Hit: hit sound, and when all the area of the ship is hit, the ship will appear
* The score will increase with all hits and ammo will decrease with every choices made
* When ammo reaches 0, the game over screen will appear with the total score shown
* The game will end automatically from the game over screen
