import pygame
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from pawn import Pawn

# Notes:
# Rect class parameters: (abs. x_coor of top left corner, abs. y_coor of top left corner, width of rect, height of rect)
# pygame.draw.rect() parameters: (surface to draw on, color, object to draw)


# Intialize variables
light, dark = (237, 199, 190), (115, 88, 81)
width, height = 100, 100

class Square:
    """A class representing each square."""

    def __init__(self, x_coor, y_coor, screen):

        # Denotes coordinates of the square (0 - 7 in both dimentions)
        self.x_coor = x_coor
        self.y_coor = y_coor
        # Absolute positions of the top-left corner of the square
        self.x_abs = x_coor * width
        self.y_abs = y_coor * height
        # Define color
        self.color = light if (self.x_coor + self.y_coor) % 2 == 0 else dark
        # Screen to draw the square on
        self.screen = screen
        self.rect = pygame.Rect(self.x_abs, self.y_abs, width, height)
        self.occupying_piece = None
        self.is_selected = False

    # Method to draw individual square
    def draw(self):
        """Draws a square on the board and the potential piece occupying it."""

        # Draw the basic square
        pygame.draw.rect(self.screen, self.color, self.rect)

        # Draw the piece occupying the square, if there is one
        if self.occupying_piece:
            piece_rect = self.occupying_piece.image.get_rect(
                topleft = (self.x_abs, self.y_abs)
            )
            self.screen.blit(self.occupying_piece.image, piece_rect)



class Board:
    """A class representing the board as a whole."""

    def __init__(self, screen):

        # Initial state of the board's pieces; one list for each row
        self.init_state = [
            ['bR', 'bK', 'bB', 'bQ', 'bG', 'bB', 'bK', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wK', 'wB', 'wQ', 'wG', 'wB', 'wK', 'wR']
        ]

        self.squares = None
        self.build_square_objects(screen)
        # Store if a square is currently selected
        self.board_square_selected = False

    def build_square_objects(self, screen):
        """Assigns an attribute; a 2D list of all 64 square objects."""
        squares = []
        for y_coor in range(8):
            row = []
            for x_coor in range(8):
                row.append(Square(x_coor, y_coor, screen))
            squares.append(row)
        self.squares = squares
    
    def initial_setup(self):
        """Draws squares and places the pieces in their starting positions."""
        for y_coor, row in enumerate(self.init_state):
            for x_coor, piece in enumerate(row):
                
                if 'R' in piece:
                    color = 'w' if 'w' in piece else 'b'
                    self.squares[y_coor][x_coor].occupying_piece = Rook(
                        x_coor, y_coor, color
                    )

                if 'K' in piece:
                    color = 'w' if 'w' in piece else 'b'
                    self.squares[y_coor][x_coor].occupying_piece = Knight(
                        x_coor, y_coor, color
                    )

                if 'B' in piece:
                    color = 'w' if 'w' in piece else 'b'
                    self.squares[y_coor][x_coor].occupying_piece = Bishop(
                        x_coor, y_coor, color
                    )

                if 'Q' in piece:
                    color = 'w' if 'w' in piece else 'b'
                    self.squares[y_coor][x_coor].occupying_piece = Queen(
                        x_coor, y_coor, color
                    )

                if 'G' in piece:
                    color = 'w' if 'w' in piece else 'b'
                    self.squares[y_coor][x_coor].occupying_piece = King(
                        x_coor, y_coor, color
                    )

                if 'P' in piece:
                    color = 'w' if 'w' in piece else 'b'
                    self.squares[y_coor][x_coor].occupying_piece = Pawn(
                        x_coor, y_coor, color
                    )
            
        # All squares have corrected initial states, now display them
        for row in self.squares:
            for square in row:
                square.draw()

    def get_square_from_coor(self, x_abs, y_abs):
        """Take absolute x and y position, returns corresponding square 
        object."""

        # Determine which square was clicked
        x_coor = x_abs // 100
        y_coor = y_abs // 100
        square = self.squares[y_coor][x_coor]
        return square

    def select_square(self, square):
        """Takes in a square object. 'Deselects' previous square if there is 
        one, 'selects' square clicked on if a piece occupies it."""

        # Deselect previous square selected if there is one
        for row in self.squares:
            for prev_square in row:
                if prev_square.is_selected:
                    prev_square.is_selected = False
                    self.board_square_selected = False
    
        # Only select if there is a piece occupying the square
        if square.occupying_piece:
            square.is_selected = True
            self.board_square_selected = True

    def find_selected_square(self):
        """Returns the square object that is currently selected."""

        for row in self.squares:
            for square in row:
                if square.is_selected:
                    return square

    def click(self, x_abs, y_abs):
        """Handles any click event that is detected."""

        # Gather the clicked square object
        square = self.get_square_from_coor(x_abs, y_abs)

        # Situation 1: No square is currently selected
        # Select the clicked square
        if self.board_square_selected == False:
            self.select_square(square)

        # Situation 2: A square with a piece on it is already selected
        elif self.board_square_selected == True:

            # Find the square that is currently selected
            current_square = self.find_selected_square()

            # Move the current piece to the target square
            self.move_piece(current_square, square)

    def move_piece(self, current_square, target_square):
        """Takes in the current square and the target square objects, 
        displays the outcome of the move."""

        moving_piece = current_square.occupying_piece
        # Clear the previous square
        current_square.occupying_piece = None
        # Move the piece to the target square
        target_square.occupying_piece = moving_piece
        # Redraw both squares
        current_square.draw()
        target_square.draw()
        
        # Deselect the previous square
        current_square.is_selected = False
        self.board_square_selected = False
