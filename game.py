from random import randint

class Jewel():
    def __init__(self, pos) -> None:
        self.x, self.y = pos
        self.colour = randint(1, 6)
        self.reset_pairs()

    def reset_pairs(self):
        self.vertical_pair, self.horizontal_pair = [], []

class Engine():
    def __init__(self) -> None:
        self.game_board = [[Jewel((i, j)) for i in range(10)] for j in range(10)]

    def run(self):
        while True:
            self.print_board()
            print('')
            self.find_pairs()
            self.find_match_pairs()
            self.print_board()
            self.board_drop()
            pause = input()

    def board_drop(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                if jewel.colour == 0:
                    if i > 0:
                        for x in range(i):
                            self.game_board[i - x][j].colour = self.game_board[i - x - 1][j].colour
                    self.game_board[0][j] = Jewel((0, j))

    def find_pairs(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                self.game_board[i][j].reset_pairs()
                jewel.reset_pairs()
                if i > 0:
                    if jewel.colour == self.game_board[i - 1][j].colour:
                        jewel.vertical_pair.append((i - 1, j))
                if i < 9:
                    if jewel.colour == self.game_board[i + 1][j].colour:
                        jewel.vertical_pair.append((i + 1, j))
                if j > 0:
                    if jewel.colour == self.game_board[i][j - 1].colour:
                        jewel.horizontal_pair.append((i, j - 1))
                if j < 9:
                    if jewel.colour == self.game_board[i][j + 1].colour:
                        jewel.horizontal_pair.append((i, j + 1))

    def find_match_pairs(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                if len(jewel.horizontal_pair) > 1:
                    self.game_board[i][j].colour = 0
                    for pos in jewel.horizontal_pair:
                        x, y = pos
                        self.game_board[x][y].colour = 0
                if len(jewel.vertical_pair) > 1:
                    self.game_board[i][j].colour = 0
                    for pos in jewel.vertical_pair:
                        x, y = pos
                        self.game_board[x][y].colour = 0

    def print_board(self):
        for row in self.game_board:
            row_jewels = []
            for jewel in row:
                row_jewels.append(jewel.colour)
            print(row_jewels)

if __name__ == '__main__':
    my_game = Engine()
    my_game.run()