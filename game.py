from random import randint
import pygame

COLOURS = [ (0, 0, 0),
    (255, 0, 0), (255, 64, 0), (255, 128, 0), (255, 191, 0), 
    (255, 255, 0), (191, 255, 0), (128, 255, 0), (64, 255, 0), 
    (0, 255, 0), (0, 255, 64), (0, 255, 128), (0, 255, 191),
    (0, 255, 255), (0, 191, 255), (0, 128, 255), (0, 64, 255), (0, 0, 255)
    ]

class Jewel():
    def __init__(self, pos) -> None:
        self.x, self.y = pos
        self.colour = randint(1, len(COLOURS) - 1)
        self.update_jewel()
        self.reset_triples()

    def update_jewel (self):
        self.make_image()
        self.get_rect()

    def reset_triples(self):
        self.vertical_triple, self.horizontal_triple = [], []
        
    def make_image(self):
        image = pygame.Surface((40, 40))
        image.set_colorkey(COLOURS[0])  # Black colors will not be blit.
        pygame.draw.circle(image, COLOURS[self.colour], (20, 20), 20)
        self.my_image =  image
    
    def get_rect(self):
        jewel_center = (20 + (self.x * 40), 20 + (self.y * 40))
        jewel_rect = self.my_image.get_rect(center = jewel_center)
        self.my_rect =  jewel_rect

class Engine():
    def __init__(self) -> None:
        self.board_width = 10
        self.board_height = 10
        pygame.init()
        self.game_window = pygame.display.set_mode((self.board_width * 40, self.board_height * 40))
        pygame.display.set_caption("DigiJewels")
        self.game_board = [[Jewel((i, j)) for i in range(self.board_width)] for j in range(self.board_height)]

    def run(self):
        while True:
            self.print_board()
            print('')
            self.find_triples()
            self.print_board()
            self.draw_board()
            self.board_drop()
            pause = input()

    def board_drop(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                if jewel.colour == 0:
                    if i > 0:
                        for x in range(i):
                            self.game_board[i - x][j].colour = self.game_board[i - x - 1][j].colour
                            self.game_board[i - x][j].update_jewel()
                    self.game_board[0][j].colour = randint(1, len(COLOURS) - 1)
                    self.game_board[0][j].update_jewel()

    def find_triples(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                self.game_board[i][j].reset_triples()
                if i > 0 and i < self.board_width - 1:
                    if (
                        jewel.colour == self.game_board[i - 1][j].colour and 
                        jewel.colour == self.game_board[i + 1][j].colour
                        ):
                        jewel.vertical_triple.append((i - 1, j))
                        jewel.vertical_triple.append((i + 1, j))
                if j > 0 and j < self.board_height - 1:
                    if (
                        jewel.colour == self.game_board[i][j - 1].colour and
                        jewel.colour == self.game_board[i][j + 1].colour
                        ):
                        jewel.horizontal_triple.append((i, j - 1))
                        jewel.horizontal_triple.append((i, j + 1))
        self.clear_matched()

    def clear_matched(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                if len(jewel.horizontal_triple) > 0:
                    self.game_board[i][j].colour = 0
                    for cell in jewel.horizontal_triple:
                        x, y = cell
                        self.game_board[x][y].colour = 0
                if len(jewel.vertical_triple) > 0:
                    self.game_board[i][j].colour = 0
                    for cell in jewel.vertical_triple:
                        x, y = cell
                        self.game_board[x][y].colour = 0

    def draw_board(self):
        self.game_window.fill(COLOURS[0])
        for row in self.game_board:
            for jewel in row:
                self.game_window.blit(jewel.my_image, jewel.my_rect)
        pygame.display.update()

    def print_board(self):
        for row in self.game_board:
            row_jewels = []
            for jewel in row:
                row_jewels.append(jewel.colour)
            print(row_jewels)

if __name__ == '__main__':
    my_game = Engine()
    my_game.run()
