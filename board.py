import json
from piece import Piece


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_pieces = set()
        self.black_pieces = set()
        self.threatened_squares_white = set()
        self.threatened_squares_black = set()
        self.turn = 'W'

    def to_dict(self):
        return {
            'white_pieces': [p.to_dict() for p in self.white_pieces],
            'black_pieces': [p.to_dict() for p in self.black_pieces],
            'turn': self.turn
        }

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def from_dict(cls, d):
        board = cls()
        board.white_pieces = set(Piece.from_dict(dd, 'W') for dd in d['white_pieces'])
        board.black_pieces = set(Piece.from_dict(dd, 'B') for dd in d['black_pieces'])
        board.turn = d['turn']
        return board

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            d = json.load(f)
            return cls.from_dict(d)

    def populate(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        for p in self.white_pieces:
            self.board[p.pos_x][p.pos_y] = p
        for p in self.black_pieces:
            self.board[p.pos_x][p.pos_y] = p

    def add_piece(self, piece):
        if piece.colour == 'W':
            self.white_pieces.add(piece)
        elif piece.colour == 'B':
            self.black_pieces.add(piece)

    def remove_piece(self, piece):
        if piece in self.white_pieces:
            self.white_pieces.remove(piece)
        elif piece in self.black_pieces:
            self.black_pieces.remove(piece)
        self.board[piece.pos_x][piece.pos_y] = None

    def move_or_take_piece(self, piece, x, y):
        self.board[piece.pos_x][piece.pos_y] = None
        # moves
        if self.board[x][y] is None:
            self.board[x][y] = piece
        # takes
        elif not self.board[x][y].colour == self.turn:
            if self.turn == 'W':
                self.black_pieces.discard(self.board[x][y])
            elif self.turn == 'B':
                self.black_pieces.discard(self.board[x][y])
            self.board[x][y] = piece
        piece.moved = True
        piece.pos_x = x
        piece.pos_y = y

    def get_threatened_squares(self, colour):
        threatened_squares = set()
        pieces = set()
        if colour == 'W':
            pieces = self.white_pieces
        elif colour == 'B':
            pieces = self.black_pieces

        for p in pieces:
            p.get_threatened_squares(self)
            threatened_squares.update(p.threatened_squares)
        if colour == 'W':
            self.threatened_squares_white = threatened_squares
        elif colour == 'B':
            self.threatened_squares_black = threatened_squares
