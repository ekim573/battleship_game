import pygame
import sys
from enum import Enum, auto
import random

# the path to the saved image files
SHIP_IMAGE_PATH = {
    1: "../battleship_images/ship1.gif",
    2: "../battleship_images/ship2.gif",
    3: "../battleship_images/ship3.gif",
    4: "../battleship_images/ship4.gif",
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Text position
SCORE_TEXT_POSITION = (30, 825)


class Grid:
    """   
    Manages visual display of background picture, grid lines, and score board.
    Controls the placement of hit, miss, and ship images.
    """

    screen_size = (800, 900)
    grid_screen = (800, 800)
    score_screen = (800, 100)

    def __init__(self):
        self.grid = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Battleship")
        self.hit_positions = set() 
        self.miss_positions = set()
        self.sunk = []

        # the path to saved miss and hit images
        self.miss_image_path = pygame.image.load(
            "../battleship_images/miss.gif"
        )
        self.hit_image_path = pygame.image.load(
            "../battleship_images/hit.gif"
        )


    def set_grid(self, score, ammo, ships):
        """
        Draw the background, gridlines, scoreboard (score, ammo), and ships.
        """

        self.col = 10
        self.row_distance = self.grid_screen[0] // self.col
        self.col_height = self.grid_screen[1] // self.col

        # Background sea image
        grid_image_path = "../battleship_images/sea.gif"
        grid_image = pygame.image.load(grid_image_path)
        grid_image = pygame.transform.scale(grid_image, self.grid_screen)
        self.grid.blit(grid_image, (0, 0))

        # Score board image
        score_image_path = "../bcog200/battleship_images/scoreboard.gif"
        score_image = pygame.image.load(score_image_path)
        score_image = pygame.transform.scale(score_image, self.score_screen)
        self.grid.blit(score_image, (0, 800))

        # Score and ammo
        font = pygame.font.SysFont("Arial", 30)
        board_text = font.render(f"   Score:{score}     Ammo:{ammo}", True, WHITE)
        self.grid.blit(board_text, SCORE_TEXT_POSITION)

        # draw white grid lines
        for x in range(0, self.grid_screen[0], self.row_distance):
            pygame.draw.line(self.grid, pygame.Color("white"), (x, 0), (x, self.grid_screen[1]))
        for y in range(0, self.grid_screen[1], self.col_height):
            pygame.draw.line(self.grid, pygame.Color("white"), (0, y), (self.grid_screen[0], y))
        
        # Display completely sunk ships
        for ship in ships:  
            if ship.is_sunk():
                row, col = ship.ship_position[0]
                x = col * self.row_distance
                y = row * self.col_height

                if ship.direction == "h": # horizontal
                    width = ship.ship_size * self.row_distance
                    height = self.col_height
                    ship_image_scale = pygame.transform.scale(ship.image, (width, height))
                else: # vertical
                    width = self.row_distance
                    height = ship.ship_size * self.col_height
                    ship_image_scale = pygame.transform.scale(ship.image, (height,width))
                    ship_image_scale = pygame.transform.rotate(ship_image_scale, 90)

                self.grid.blit(ship_image_scale, (x, y))

        # display miss image in miss areas
        miss_image = pygame.transform.scale(self.miss_image_path, (self.row_distance, self.col_height))
        for (row, col) in self.miss_positions:
            x = col * self.row_distance
            y = row * self.col_height
            self.grid.blit(miss_image, (x, y))

        # display hit image in hit areas
        hit_image = pygame.transform.scale(self.hit_image_path, (self.row_distance, self.col_height))
        for (row, col) in self.hit_positions:
            x = col * self.row_distance
            y = row * self.col_height
            self.grid.blit(hit_image, (x, y))

        pygame.display.flip()


class Ship:
    """ Place the ships randomly on the grid and check if the placement is occupied or not."""
    grid_size = 10

    def __init__(self, ship_size):
        self.ship_size = ship_size
        self.ship_position = []  
        self.hit = set()  
        self.direction = random.choice(["h", "v"])  
        self.ship_image = None

    def is_sunk(self):
        """ Check if all parts of the ship is hit. """
        return set(self.ship_position) == self.hit

    def placement(self, occupied):
        """ Randomly place ships on the grid with no overlaps. """
        while True:
            # if horizontal position is chosen, place ship correctly
            if self.direction == "h":
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - self.ship_size)
                new_position = [(row, col + i) for i in range(self.ship_size)]

            # if vertical position is chosen, place ship correctly
            elif self.direction == "v":
                row = random.randint(0, self.grid_size - self.ship_size)
                col = random.randint(0, self.grid_size - 1)
                new_position = [(row + i, col) for i in range(self.ship_size)]

            # check if position is legal
            if self.legal_position(new_position, occupied):
                self.ship_position = new_position 
                occupied.update(new_position)
                self.load_image()
                break

    def load_image(self):
        """ Load ship image """
        image_path = SHIP_IMAGE_PATH.get(self.ship_size)
        if image_path:
            self.image = pygame.image.load(image_path)

    def is_sunk(self):
        """ Check if the ship is sunk """
        return set(self.ship_position) == self.hit

    def legal_position(self, new_position, occupied):
        """ Check if the ship position is not out of bound from the grid screen and is not occupied. """
        for i in new_position:
            row, col = i
            if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
                return False
            if i in occupied:
                return False
        return True


class Player:
    """ Track down score, hit, miss, and chances left for the player """
    def __init__(self, miss, ammo):
        self.hit = 0
        self.miss = miss
        self.score = 0
        self.ammo = ammo


class GameState(Enum):
    RUNNING = auto()
    GAME_OVER = auto()


class Game:
    """ Control and track game state, mouse input, sound, and screen transition. """

    def __init__(self):
        self.status = GameState.RUNNING
        self.player = Player(miss=0,ammo=50)
        self.grid = Grid()
        self.ships = []
        self.occupied = set()

        # the path to saved sound files
        self.hit_sound = pygame.mixer.Sound("../sound/hit.mp3")
        self.miss_sound = pygame.mixer.Sound("../sound/miss.mp3")

        # Create different sized ships
        for size in [4, 4, 3, 3, 2, 2, 1, 1]:
            ship = Ship(size)
            ship.placement(self.occupied)
            self.ships.append(ship)
    
    def start_screen(self):
        """
        Create a start screen consisting of instructions of the game and score, example of the game screen, and start button
        When the start button is pressed, the game starts and moves onto the game screen.
        """

        # the path to saved start screen
        start_screen_image = pygame.image.load("../battleship_images/start_screen.gif")
        start_screen_image = pygame.transform.scale(start_screen_image, (800,900))

        # the path to saved game example image
        example_image = pygame.image.load("../battleship_images/example.gif")
        example_image = pygame.transform.scale(example_image, (250,300))

        # instruction text
        font_instruction = pygame.font.SysFont("Arial", 20)
        instruction_text = [
            "Instructions for Battleship:",
            "1. Different size ships will be randomly assigned on the grid",
            "2. Guess the coordinates and try to sink all ships using the 50 ammos (chances)",
            "3. Practice strategies you can use to win the game",
            "",
            "Score:",
            "Hit part of ship: +1",
            "Ship is sunk: +5",
            "",
            "Example:"
        ]        

        # start button
        font = pygame.font.SysFont("Arial", 40)    
        start_text = font.render("Start", True, WHITE)
        start_button_rect = pygame.Rect(0,0,200,100)
        start_button_rect.center = (400,800)

        # Set start screen 
        while True:
            self.grid.grid.blit(start_screen_image, (0, 0))
            self.grid.grid.blit(example_image, (100,400))

            instruction_x = 50
            instruction_y = 100

            # display instruction text
            for instruction in instruction_text:
                text_surface = font_instruction.render(instruction, True, WHITE)
                self.grid.grid.blit(text_surface, (instruction_x, instruction_y))
                instruction_y += text_surface.get_height() + 5

            # display start button
            pygame.draw.rect(self.grid.grid, WHITE, start_button_rect)
            start_text = font.render("Start", True, BLACK)
            text = start_text.get_rect(center=start_button_rect.center)
            self.grid.grid.blit(start_text, text)
            pygame.display.flip()

            # check if start position is clicked to start game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):                      
                        return True
                    

    def run(self):
        """ Handle player input, check hits and misses, and end game when ammo is 0. """

        self.start_screen()

        run = True
        while run and self.status == GameState.RUNNING:

            # mouse position
            mouse_position = pygame.mouse.get_pos()
            self.grid.set_grid(self.player.score, self.player.ammo, self.ships)
            MOUSE_RADIUS = 5
            pygame.draw.circle(self.grid.grid, "red", mouse_position, MOUSE_RADIUS)

            # handle user event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.status == GameState.RUNNING:
                    if self.player.ammo == 0 or mouse_position[1] >= 800:
                        continue

                    col = mouse_position[0] // (Grid.grid_screen[0] // 10)
                    row = mouse_position[1] // (Grid.grid_screen[1] // 10)

                    if (row, col) in self.grid.hit_positions or (row, col) in self.grid.miss_positions:
                        continue

                    self.player.ammo -= 1
                    hit = False

                    # Check clicked area if it is a hit and give +1 point
                    for ship in self.ships:
                        if (row, col) in ship.ship_position:
                            hit = True
                            self.hit_sound.play()
                            ship.hit.add((row, col))
                            self.grid.hit_positions.add((row, col))
                            self.player.hit += 1
                            self.player.score += 1

                            # if ship is fully hit, give +5 points
                            if ship.is_sunk() and ship not in self.grid.sunk:
                                self.player.score += 5
                                self.grid.sunk.append(ship)
                            break
                    
                    # if not a hit
                    if not hit:
                        self.miss_sound.play()
                        self.grid.miss_positions.add((row, col))
                        self.player.miss += 1

                    # end game if ammo is 0
                    if self.player.ammo == 0:
                        self.end()
                        self.status = GameState.GAME_OVER

                pygame.display.flip()

    def end(self):
        """ When the game ends, display final score screen and exit game automatically. """
        self.status = GameState.GAME_OVER

        # the path to saved game over image and load the image
        game_over_image_path = "../battleship_images/game_over.gif"
        game_over_image = pygame.image.load(game_over_image_path)
        game_over_image = pygame.transform.scale(game_over_image, (800, 900))
        self.grid.grid.blit(game_over_image, (0, 0))

        # display final score
        font = pygame.font.SysFont("Times New Roman", 60)
        game_over_text = font.render(f"Final Score: {self.player.score}", "black", True, WHITE)
        text = game_over_text.get_rect(center=(400, 450))
        self.grid.grid.blit(game_over_text, text)

        pygame.display.flip()
        pygame.time.wait(5000)


def main():
    """ Set up pygame, run the game, and close window """
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
