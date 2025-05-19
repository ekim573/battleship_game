# Battleship Game
Battleship is a simple classic strategy game, and this visual game was created using Python and Pygame. In this game, players are given limited number of ammo to find the ships and destroy them in randomly assigned hidden areas in the grid. This visual version has a sea background and a real-time update in the scoreboard of ammos, hits, and misses. Using this game, you can practice your strategies and logical skills.
![External Image](https://github.com/ekim573/battleship_game/blob/main/battleship_images/example.gif)

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
  * Place ships horizontally or vertically (random)
* is_sunk()
  * Check if all parts of the ship are hit
* legal_position(new_position, occupied)
  * Check if there is an overlap or the ship is out-of-bound
* load_image()
  * Load the ship image from battlehsip_images

### Player
Tracks the player's game state and numbers
* hit: number of success hits, starts at 0
* miss: number of misses
* score: total points, starts at 0
* ammo: number of chances left, starts at 50

### GameState
Define status of the game
* RUNNING = auto()
  * Game is active
* GAME_OVER = auto()
  * Game ended

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
  * Miss: miss_image, miss_sound
  * Hit: hit_image, hit_sound, +1 points
  * If ship is sunk: ship image appears, +5 points
  * When ammo=0, change game status to end
* end()
  * End the game by updating game state
  * When the ends, the screen will display to game over screen
  * Show the total score
  * The game will quit automatically

## Testing
* Install pygame (pip install pygame)
* Download battleship_images and sound file
* Change file paths according to your file path of where battleship_images and sound file is located
* Start of the game, there should be a start screen with information about the game and a start button
* After pressing the start button, a screen with 10x10 grid with a sea background and a scoreboard will appear
* The ships will be randomly assigned correctly with no overlap or out-of-bounds
* The game will trackdown hits, misses, and ammo
* Miss: x image with a miss sound
* Hit: explosion image with hit sound, and when all places are hit, ship will appear
* The score will increase with all hits and ammo will decrease with every choices made
* When ammo reaches 0, the game over screen will appear with the total score shown
* The game will end automatically from the game over screen
