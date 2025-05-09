import pygame
import sys
from enum import Enum, auto
import random

SHIP_IMAGE_PATH = {
    1: "/Users/erinkim/desktop/bcog200/battleship_images/ship1.gif",
    2: "/Users/erinkim/desktop/bcog200/battleship_images/ship2.gif",
    3: "/Users/erinkim/desktop/bcog200/battleship_images/ship3.gif",
    4: "/Users/erinkim/desktop/bcog200/battleship_images/ship4.gif",
}


class Grid:
    """   
    screen_size = (800, 900)
    Create a grid screen (800, 800), score_screen (800, 100)
    Background is a sea picture with white grid lines
    Create a score board at the bottom of the screen including the score and ammo (chances)
    Place the ships
    """

    screen_size = (800, 900)
    grid_screen = (800, 800)
    score_screen = (800, 100)

    def __init__(self):
        self.grid = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Battleship")
        self.hit_positions = set()  # track the position
        self.miss_positions = set()
        self.sunk = []
        self.miss_image_path = pygame.image.load(
            "/Users/erinkim/desktop/bcog200/battleship_images/miss.gif"
        )
        self.hit_image_path = pygame.image.load(
            "/Users/erinkim/desktop/bcog200/battleship_images/hit.gif"
        )

    def set_grid(self, score, ammo, ships):
        self.col = 10
        self.row_distance = self.grid_screen[0] // self.col
        self.col_height = self.grid_screen[1] // self.col

        grid_image_path = "/Users/erinkim/desktop/bcog200/battleship_images/sea.gif"
        grid_image = pygame.image.load(grid_image_path)
        grid_image = pygame.transform.scale(grid_image, self.grid_screen)
        self.grid.blit(grid_image, (0, 0))

        score_image_path = "/Users/erinkim/desktop/bcog200/battleship_images/scoreboard.gif"
        score_image = pygame.image.load(score_image_path)
        score_image = pygame.transform.scale(score_image, self.score_screen)
        self.grid.blit(score_image, (0, 800))

        font = pygame.font.SysFont("Arial", 30)
        board_text = font.render(
            f"   Score:{score}       Ammo:{ammo}", True, (255, 255, 255)
        )
        self.grid.blit(board_text, (30, 825))

        for x in range(0, self.grid_screen[0], self.row_distance):
            pygame.draw.line(
                self.grid, pygame.Color("white"), (x, 0), (x, self.grid_screen[1])
            )
        for y in range(0, self.grid_screen[1], self.col_height):
            pygame.draw.line(
                self.grid, pygame.Color("white"), (0, y), (self.grid_screen[0], y)
            )

        for ship in ships:  # Get the ship image and transform the size to fit it into the grids
            if ship.is_sunk():
                r, c = ship.ship_position[0]
                x = c * self.row_distance
                y = r * self.col_height

                if ship.direction == "h": # horizontal
                    width = ship.ship_size * self.row_distance
                    height = self.col_height
                    ship_image_scale = pygame.transform.scale(ship.image, (width, height))
                else: # vertial
                    width = self.row_distance
                    height = ship.ship_size * self.col_height
                    ship_image_scale = pygame.transform.scale(ship.image, (height,width))
                    ship_image_scale = pygame.transform.rotate(ship_image_scale, 90)

                self.grid.blit(ship_image_scale, (x, y))

        miss_image = pygame.transform.scale(
            self.miss_image_path, (self.row_distance, self.col_height)
        )  # make it correct size
        for (r, c) in self.miss_positions:  # place the missed areas
            x = c * self.row_distance
            y = r * self.col_height
            self.grid.blit(miss_image, (x, y))

        hit_image = pygame.transform.scale(
            self.hit_image_path, (self.row_distance, self.col_height)
        )
        for (r, c) in self.hit_positions:
            x = c * self.row_distance
            y = r * self.col_height
            self.grid.blit(hit_image, (x, y))

        pygame.display.flip()


class Ship:
    """
    Place the ships randomly on the grid and check if the placement is occupied or not
    """

    grid_size = 10

    def __init__(self, ship_size):
        self.ship_size = ship_size
        self.ship_position = []  # row and column
        self.hit = set()  # Track hit positions
        self.direction = random.choice(["h", "v"])  # horizontal or vertical
        self.ship_image = None

    def is_sunk(self):
        return set(self.ship_position) == self.hit

    def placement(self, occupied):
        while True:
            if self.direction == "h":
                r = random.randint(0, self.grid_size - 1)
                c = random.randint(0, self.grid_size - self.ship_size)
                position1 = [(r, c + i) for i in range(self.ship_size)]
                # choose a random r, and a c but (grid_size - self.ship_size) will limit so it does not go to the right edge

            elif self.direction == "v":
                r = random.randint(0, self.grid_size - self.ship_size)
                c = random.randint(0, self.grid_size - 1)
                position1 = [(r + i, c) for i in range(self.ship_size)]
                # choose a random c, and a r but limit so that it does not out of range

            if self.legal_position(position1, occupied):
                self.ship_position = position1  # check for overlap
                occupied.update(position1)
                self.load_image()
                break

    def load_image(self):
        image_path = SHIP_IMAGE_PATH.get(self.ship_size)
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
        self.player = Player(miss=0, ammo=50)
        self.grid = Grid()
        self.ships = []
        self.occupied = set()
        self.hit_sound = pygame.mixer.Sound(
            "/Users/erinkim/desktop/bcog200/sound/hit.mp3"
        )
        self.miss_sound = pygame.mixer.Sound(
            "/Users/erinkim/desktop/bcog200/sound/miss.mp3"
        )

        for size in [4, 4, 3, 3, 2, 2, 1, 1]:
            ship = Ship(size)
            ship.placement(self.occupied)
            self.ships.append(ship)
    
    def start_screen(self):
        """
        Create a start screen consisting of instructions of the game and score, example of the game screen, and start button
        When the start button is pressed, the game starts and moves onto the game screen
        """

        start_screen_image = pygame.image.load("/Users/erinkim/desktop/bcog200/battleship_images/start_screen.gif")
        start_screen_image = pygame.transform.scale(start_screen_image, (800,900))

        example_image = pygame.image.load("/Users/erinkim/desktop/bcog200/battleship_images/example.gif")
        example_image = pygame.transform.scale(example_image, (250,300))

        font_instruction = pygame.font.SysFont("Arial", 20)
        instruction_text = [
            "Instructions for Battleship:",
            "1. The computer will randomly assign different size ships on the grid",
            "2. Guess the coordinates and try to sink all ships using the 50 ammos (chances)",
            "3. Practice strategies you can use to win the game",
            "",
            "Score:",
            "Hit part of ship: +1",
            "Whole ship is sunk: +5",
            "",
            "Example:"
        ]        

        font = pygame.font.SysFont("Arial", 40)    
        start_text = font.render("Start", True, (255, 255, 255))

        start_button_rect = pygame.Rect(0,0,200,100)
        start_button_rect.center = (400,800)


        while True:
            self.grid.grid.blit(start_screen_image, (0, 0))
            self.grid.grid.blit(example_image, (100,400))

            instruction_x = 50
            instruction_y = 100
            for instruction in instruction_text:
                text_surface = font_instruction.render(instruction, True, (255,255,255))
                self.grid.grid.blit(text_surface, (instruction_x, instruction_y))
                instruction_y += text_surface.get_height() + 5


            pygame.draw.rect(self.grid.grid, (255, 255, 255), start_button_rect)

            start_text = font.render("Start", True, (0, 0, 0))
            text = start_text.get_rect(center=start_button_rect.center)
            self.grid.grid.blit(start_text, text)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):                      
                        return True
                    

    def run(self):
        """
        Using the mouse, the player will choose certian grids on the screen
        Trackdown which areas were chosen
        If it is a miss, add the miss iamge with miss sound
        If it is a hit, add the hit image with hit sound
        When ammo = 0, then end the game
        """

        self.start_screen()

        run = True
        while run and self.status == GameState.RUNNING:
            mouse_position = pygame.mouse.get_pos()
            self.grid.set_grid(self.player.score, self.player.ammo, self.ships)
            pygame.draw.circle(self.grid.grid, "red", mouse_position, 5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and self.status == GameState.RUNNING
                ):
                    if self.player.ammo == 0 or mouse_position[1] >= 800:
                        continue

                    col = mouse_position[0] // (Grid.grid_screen[0] // 10)
                    row = mouse_position[1] // (Grid.grid_screen[1] // 10)

                    if (row, col) in self.grid.hit_positions or (
                        row,
                        col,
                    ) in self.grid.miss_positions:
                        continue

                    self.player.ammo -= 1
                    hit = False

                    for ship in self.ships:
                        if (row, col) in ship.ship_position:
                            hit = True
                            self.hit_sound.play()
                            ship.hit.add((row, col))
                            self.grid.hit_positions.add((row, col))
                            self.player.hit += 1
                            self.player.score += 1

                            if ship.is_sunk() and ship not in self.grid.sunk:
                                self.player.score += 5
                                self.grid.sunk.append(ship)
                            
                            break

                    if not hit:
                        self.miss_sound.play()
                        self.grid.miss_positions.add((row, col))
                        self.player.miss += 1

                    if self.player.ammo == 0:
                        self.end()
                        self.status = GameState.GAME_OVER

                pygame.display.flip()

    def end(self):
        """
        When the game ends, move screen to the game over screen
        Show the total score
        Exit game automatically
        """
        self.status = GameState.GAME_OVER

        game_over_image_path = "/Users/erinkim/desktop/bcog200/battleship_images/game_over.gif"
        game_over_image = pygame.image.load(game_over_image_path)
        game_over_image = pygame.transform.scale(game_over_image, (800, 900))
        self.grid.grid.blit(game_over_image, (0, 0))

        font = pygame.font.SysFont("Times New Roman", 60)
        game_over_text = font.render(
            f"Final Score: {self.player.score}", "black", True, (255, 255, 255)
        )
        text = game_over_text.get_rect(center=(400, 450))
        self.grid.grid.blit(game_over_text, text)

        pygame.display.flip()
        pygame.time.wait(5000)


def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
