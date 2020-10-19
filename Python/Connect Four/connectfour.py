import sys, pygame
import numpy

# COLOURS
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()


class ConnectFour:
    def __init__(self):
        self.colCount = 7
        self.rowCount = 6
        self.squareSize = 100
        self.radius = int(self.squareSize / 2 - 5)
        self.screenWidth = self.colCount * self.squareSize
        self.screenHeight = (self.rowCount + 1) * self.squareSize
        self.screenSize = (self.screenWidth, self.screenHeight)
        self.screen = pygame.display.set_mode(self.screenSize)

        self.board = numpy.zeros((self.rowCount, self.colCount))        # initialises board
        self.turn = 1

        self.gameFont = pygame.font.SysFont('Arial', 75)
        self.gameOver = False

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_position(self, col):
        """
        Checks whether top row at specified col contains a zero.
        If so, position is valid (empty). If not, then that col is full.
        :param col: column
        :return: True / False
        """
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        """
        Obtains the row number that is valid for the given col value (starts from the bottom).
        :param col: column
        :return: row number
        """
        for row in range(self.rowCount - 1, -1, -1):
            if self.board[row][col] == 0:
                return row

    def check_connect_four(self, piece):
        """
        Function is intended to check for winning moves horizontally, vertically and diagonally (scanning the whole board)
        :param piece:
        :return:
        """
        # Check horizontally
        for i in range(self.rowCount):
            for j in range(self.colCount - 3):
                if self.board[i][j] == piece and self.board[i][j + 1] == piece and self.board[i][j + 2] == piece and self.board[i][j + 3] == piece:
                    return True

        # Check vertically
        for j in range(self.colCount):
            for i in range(self.rowCount - 3):
                if self.board[i][j] == piece and self.board[i + 1][j] == piece and self.board[i + 2][j] == piece and self.board[i + 3][j] == piece:
                    return True

        # Check diagonally right
        for i in range(self.rowCount - 3):
            for j in range(self.colCount - 3):
                if self.board[i][j] == piece and self.board[i + 1][j + 1] == piece and self.board[i + 2][j + 2] == piece and self.board[i + 3][j + 3] == piece:
                    return True

        # Check diagonally left
        for i in range(self.rowCount - 3):
            for j in range(self.colCount - 1, -1, -1):
                if self.board[i][j] == piece and self.board[i + 1][j - 1] == piece and self.board[i + 2][j - 2] == piece and self.board[i + 3][j - 3] == piece:
                    return True

    # rect takes tuple of (x, y, height of rect, width of rect) in last argument
    def draw_board(self):
        pygame.draw.rect(self.screen, BLUE, (0, self.squareSize, self.squareSize * self.colCount, self.squareSize * self.rowCount))

        for row in range(self.rowCount):
            for col in range(self.colCount):
                if self.board[row][col] == 0:
                    pygame.draw.circle(self.screen, BLACK, (col * self.squareSize + int(self.squareSize / 2), row * self.squareSize + self.squareSize + int(self.squareSize / 2)),self.radius)
                elif self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, RED, (col * self.squareSize + int(self.squareSize / 2), row * self.squareSize + self.squareSize + int(self.squareSize / 2)), self.radius)
                elif self.board[row][col] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (col * self.squareSize + int(self.squareSize / 2), row * self.squareSize + self.squareSize + int(self.squareSize / 2)), self.radius)

    def main(self):
        self.draw_board()
        pygame.display.update()
        while not self.gameOver:
            valid_choice = False
            while not valid_choice:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()  # exit without annoying dialogue box

                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.screen, BLACK, (0, 0, self.screenWidth, self.squareSize))
                        posx = event.pos[0]

                        if self.turn % 2 == 1:
                            pygame.draw.circle(self.screen, RED, (posx, int(self.squareSize / 2)), self.radius)

                        if self.turn % 2 == 0:
                            pygame.draw.circle(self.screen, YELLOW, (posx, int(self.squareSize / 2)), self.radius)

                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(self.screen, BLACK, (0, 0, self.screenWidth, self.squareSize))
                        # If turn is odd, player one's turn
                        if self.turn % 2 == 1:
                            posx = event.pos[0]
                            col = int(posx // self.squareSize)

                            if self.is_valid_position(col):
                                row = self.get_next_open_row(col)
                                self.drop_piece(row, col, 1)
                                valid_choice = True

                                if self.check_connect_four(1):
                                    label = self.gameFont.render('PLAYER 1 WINS!', 1, RED)
                                    self.screen.blit(label, (40, 10))
                                    pygame.display.update()
                                    self.gameOver = True

                            else:
                                print('Column is full! Please select another one.')

                        # If turn is even, player two's turn
                        elif self.turn % 2 == 0:
                            posx = event.pos[0]
                            col = int(posx // self.squareSize)

                            if self.is_valid_position(col):
                                row = self.get_next_open_row(col)
                                self.drop_piece(row, col, 2)
                                valid_choice = True

                                if self.check_connect_four(2):
                                    label = self.gameFont.render('PLAYER 2 WINS!', 1, YELLOW)
                                    self.screen.blit(label, (40, 10))
                                    pygame.display.update()
                                    self.gameOver = True

                            else:
                                print('Column is full! Please select another one.')

                if valid_choice:
                    self.draw_board()
                    pygame.display.update()
                    print(self.board)
                    self.turn += 1

        if self.gameOver:
            pygame.time.wait(1500)


if __name__ == '__main__':
    game = ConnectFour()
    game.main()
