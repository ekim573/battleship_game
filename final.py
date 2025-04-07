import pygame
import sys
from enum import Enum, auto
import random

class Grid:
    screen_size = (800, 900)
    grid_screen = (800, 800)
    score_screen = (800, 100)

    def __init__(self):
        self.grid = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Battleship")
    
    def set_grid(self, score, ammo):
        self.row = 10
        self.col = 10
        self.row_distance = self.grid_screen[0] // self.row
        self.col_height = self.grid_screen[1] // self.col

        grid_image_path = "/Users/erinkim/desktop/bcog200/sea.gif"
        grid_image = pygame.image.load(grid_image_path)
        grid_image = pygame.transform.scale(grid_image, self.grid_screen)
        self.grid.blit(grid_image, (0,0))

        score_image_path = "/Users/erinkim/desktop/bcog200/scoreboard.gif"
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
        
        pygame.display.flip()
        """"   
        Create a grid screen (800, 800) 
        Background is a sea picture with white grid lines
        Create a board keeping track of the score and chances(ammo) left for the player
        """


class Ship:
    grid_size = 10

    def __init__(self, ship_size):
        self.ship_size = ship_size
        self.ship_position = [] # row and column
        self.hit = set() # Need to Track hit positions
        self.position = random.choice(['h', 'v']) # horizontal and vertical

    def placement(self, occupied): 

        while True:
            if self.position == 'h':
                r = random.randint(0, self.grid_size -1)
                c = random.randint(0, self.grid_size - self.ship_size)
                position1 = [(r,c + i) for i in range(self.ship_size)]
                # choose a random r, and a c but (grid_size - self.ship_size) will limit so it does not go to the right edge
                # Might need to fix
            elif self.position == 'v':
                r = random.randint(0, self.grid_size - self.ship_size)
                c = random.randint(0, self.grid_size - 1)
                position1 = [(r + i, c) for i in range(self.ship_size)]
                # choose a random c, and a r but limit so that it does not out of range 
                # Might need to fix

            if self.legal_position(position1, occupied):
                self.ship_position = position1 #check for overlap
    
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
    RUNNING = auto() #import auto()
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
    grid.set_grid(score = player.score, ammo = player.ammo)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.flip()
                
    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()

