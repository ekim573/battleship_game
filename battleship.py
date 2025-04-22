import pygame
import sys
from enum import Enum, auto
import random

SHIP_IMAGE_PATH = {
    (1, 'h'): "/Users/erinkim/desktop/bcog200/images/ship1_horizontal.gif",
    (1, 'v'): "/Users/erinkim/desktop/bcog200/images/ship1_vertical.gif",
    (2, 'h'): "/Users/erinkim/desktop/bcog200/images/ship2_horizontal.gif",
    (2, 'v'): "/Users/erinkim/desktop/bcog200/images/ship2_vertical.gif",
    (3, 'h'): "/Users/erinkim/desktop/bcog200/images/ship3_horizontal.gif",
    (3, 'v'): "/Users/erinkim/desktop/bcog200/images/ship3_vertical.gif",
    (4, 'h'): "/Users/erinkim/desktop/bcog200/images/ship1_horizontal.gif",
    (4, 'v'): "/Users/erinkim/desktop/bcog200/images/ship1_vertical.gif"
}
#(size of ship, horizontal or vertical): image's path
#All ships that will be used 

class Grid:
    screen_size = (800, 900)
    grid_screen = (800, 800)
    score_screen = (800, 100)

    def __init__(self):
        self.grid = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Battleship")
        self.hit_positions = set() #track the position
        self.miss_positions = set()
        self.sunk = []
        self.miss_image = pygame.image.load("/Users/erinkim/desktop/bcog200/images/miss.gif")
    
    def set_grid(self, score, ammo, ships):        
        self.col = 10
        self.row_distance = self.grid_screen[0] // self.col
        self.col_height = self.grid_screen[1] // self.col

        grid_image_path = "/Users/erinkim/desktop/bcog200/images/sea.gif"
        grid_image = pygame.image.load(grid_image_path)
        grid_image = pygame.transform.scale(grid_image, self.grid_screen)
        self.grid.blit(grid_image, (0,0))

        score_image_path = "/Users/erinkim/desktop/bcog200/images/scoreboard.gif"
        score_image = pygame.image.load(score_image_path)
        score_image = pygame.transform.scale(score_image, self.score_screen)
        self.grid.blit(score_image, (0,800))

        font = pygame.font.SysFont("Arial", 30)
        board_text = font.render(f"Score:{score}  Ammo:{ammo}", True, (255, 255,255))
        self.grid.blit(board_text, (30,825))

        for x in range(0, self.grid_screen[0], self.row_distance):
            pygame.draw.line(self.grid, pygame.Color("white"), (x, 0), (x, self.grid_screen[1]))
        for y in range(0, self.grid_screen[1], self.col_height):
            pygame.draw.line(self.grid, pygame.Color("white"), (0,y), (self.grid_screen[0],y))

        for ship in ships: #get the ship image and fit it into the grids
            if ship.is_sunk():
                r, c = ship.ship_position[0]
                x = c * self.row_distance
                y = r * self.col_height
                
                if ship.direction == 'h':
                    width = ship.ship_size * self.row_distance
                    height = self.col_height
                else:
                    width = self.row_distance
                    height = ship.ship_size * self.col_height

                ship_image = pygame.transform.scale(ship.image, (width, height))
                self.grid.blit(ship_image, (x, y))

        missed_image = pygame.transform.scale(self.miss_image, (self.row_distance, self.col_height)) #make it correct size
        for (r,c) in self.miss_positions: #palce the missed areas
            x = c * self.row_distance
            y = r * self.col_height
            self.grid.blit(missed_image, (x,y))
              
        pygame.display.flip()
        """"   
        Create a grid screen (800, 800) 
        Background is a sea picture with white grid lines
        Create a board keeping track of the score and chances(ammo) left for the player
        Place the ships and if all the coordinates are hit, then show the image of the ship
        """


class Ship:
    grid_size = 10

    def __init__(self, ship_size):
        self.ship_size = ship_size
        self.ship_position = [] # row and column
        self.hit = set() # Need to Track hit positions
        self.direction = random.choice(['h', 'v']) # horizontal and vertical
        self.ship_image = None

    def is_sunk(self):
        return set(self.ship_position)== self.hit

    def placement(self, occupied): 
        while True:
            if self.direction == 'h':
                r = random.randint(0, self.grid_size -1)
                c = random.randint(0, self.grid_size - self.ship_size)
                position1 = [(r,c + i) for i in range(self.ship_size)]
                # choose a random r, and a c but (grid_size - self.ship_size) will limit so it does not go to the right edge
                # Might need to fix
            elif self.direction == 'v':
                r = random.randint(0, self.grid_size - self.ship_size)
                c = random.randint(0, self.grid_size - 1)
                position1 = [(r + i, c) for i in range(self.ship_size)]
                # choose a random c, and a r but limit so that it does not out of range 
                # Might need to fix

            if self.legal_position(position1, occupied):
                self.ship_position = position1 #check for overlap
                occupied.update(position1)
                self.load_image()
                break

    def load_image(self):
        image_path = SHIP_IMAGE_PATH.get ((self.ship_size, self.direction))
        if image_path:
            self.image = pygame.image.load(image_path)

    def is_sunk(self):
        return set(self.ship_position) == self.hit

    def legal_position(self, position1, occupied):

        for i in position1:
            r, c = i
            if not (0 <= r < self.grid_size and 0 <= c < self.grid_size):
                return False
            if i in occupied:
                return False
        
        return True
    """
    Place the ships randomly on the grid and check if the placement is occupied or not
    """


class Player:
    def __init__(self, miss, ammo):
        self.hit = 0
        self.miss = miss
        self.score = 0
        self.ammo = ammo
    """
    Track down score, hit, miss, and chances left for the player
    """

class GameState(Enum):
    RUNNING = auto() 
    GAME_OVER = auto()

class Game:
    def __init__(self):
        self.status = GameState.RUNNING
    
    def start(self):
        self.status = GameState.RUNNING

    def end(self):
        self.stauts = GameState.GAME_OVER

"""
Track the status of the game whether it should continue running or not
"""

def main():
    pygame.init()

    player = Player(miss = 0, ammo = 50)
    grid = Grid()
    game = Game()
    ships = []
    occupied = set()


    for size in [4,4,3,3,2,2,1,1]:
        ship = Ship(size)
        ship.placement(occupied)
        ships.append(ship)

    run = True
    while run:
        mouse_position = pygame.mouse.get_pos()
        grid.set_grid(player.score, player.ammo, ships)

        pygame.draw.circle(grid.grid, 'red', mouse_position, 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game.status == GameState.RUNNING:
                if player.ammo == 0 or mouse_position[1] >= 800: 
                    continue
                col = (mouse_position[0] // (Grid.grid_screen[0] // 10))
                row = (mouse_position[1] // (Grid.grid_screen[1] // 10))
                    
                if (row, col) in grid.hit_positions or (row, col) in grid.miss_positions:
                    continue
                    
                player.ammo -= 1
                hit = False
                    
                for ship in ships: #Needed to organize
                    if (row, col) in ship.ship_position:
                        hit = True
                        ship.hit.add((row, col))
                        grid.hit_positions.add((row, col))
                        player.hit += 1
                        player.score += 1
                        hit = True
                        break

                if not hit:
                    grid.miss_positions.add((row, col))
                    player.miss += 1
                           
        pygame.display.flip()             
    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()

