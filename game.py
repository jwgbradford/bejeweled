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
    
    def drop_rect(self, dy):
        jewel_center = (20 + (self.x * 40), 20 + ((self.y * 40) + dy))
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

    def column_drop(self, i):
        columns_to_drop = {}
        # test if any columns contain black jewels
        for j in range(self.board_width):
            if self.game_board[i][j].colour == 0:
                row_drop_count = 0
                if i == 0:
                    self.game_board[i][j].colour = randint(1, len(COLOURS) - 1) # make a new jewel
                    self.game_board[i][j].make_image()
                else:
                    for x in range(i):
                        if self.game_board[i - x][j].colour == 0: # if the jewel above ours is also black, we keep going
                            row_drop_count += 1
                        else:
                            break
                columns_to_drop[j] = row_drop_count
        return columns_to_drop

    def jewel_drop(self, i, columns_to_drop):
        for dy in range(40):
            for column in columns_to_drop:
                rows_to_drop = columns_to_drop[column]
                self.game_board[i - rows_to_drop][column].drop_rect(dy)
            self.draw_board()
            pygame.time.Clock().tick(20)

    def board_drop(self):
        # to drop the board, we want to start at the bottom row, and work up
        for i in range(self.board_height - 1, -1, -1):
            columns_to_drop = self.column_drop(i)
            #drop jewels by one row
            for _ in range(len(columns_to_drop)):
                print(columns_to_drop)
                self.jewel_drop(i, columns_to_drop)
                # and swap colours
                del_columns = {}
                for column in columns_to_drop:
                    rows_to_drop = columns_to_drop[column]
                    self.game_board[i - rows_to_drop + 1][column].colour = self.game_board[i - rows_to_drop][column].colour
                    self.game_board[i - rows_to_drop + 1][column].make_image()
                    self.game_board[i - rows_to_drop][column].colour = 0
                    self.game_board[i - rows_to_drop][column].make_image()
                    #columns_to_drop[column] -= 1
                    if columns_to_drop[column] == 0:
                        del_columns[column] = 0
                for column in del_columns:
                    columns_to_drop.pop(column)
                if len(columns_to_drop) == 0:
                    break

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
                    self.game_board[i][j].make_image()
                    for cell in jewel.horizontal_triple:
                        x, y = cell
                        self.game_board[x][y].colour = 0
                        self.game_board[x][y].make_image()
                if len(jewel.vertical_triple) > 0:
                    self.game_board[i][j].colour = 0
                    self.game_board[i][j].make_image()
                    for cell in jewel.vertical_triple:
                        x, y = cell
                        self.game_board[x][y].colour = 0
                        self.game_board[x][y].make_image()

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
