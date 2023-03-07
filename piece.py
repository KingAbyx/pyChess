class Piece:
    def __init__(self, pos_x, pos_y, figure, colour):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.figure = figure
        self.colour = colour
        self.moved = False
        self.threatened_squares = set()

    def to_dict(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'figure': self.figure,
            'moved': self.moved
        }

    @classmethod
    def from_dict(cls, d, colour):
        piece = cls(d['pos_x'], d['pos_y'], d['figure'], colour)
        piece.moved = d['moved']
        return piece

    def get_threatened_squares(self, board):
        direct = 0
        if self.colour == 'W':
            direct = -1
        elif self.colour == 'B':
            direct = 1
        match self.figure:
            case 'P':
                if 0 <= self.pos_x+1 < 8 and 0 <= self.pos_y+direct < 8:
                    self.threatened_squares.add((self.pos_x+1, self.pos_y+direct))
                if 0 <= self.pos_x - 1 < 8 and 0 <= self.pos_y + direct < 8:
                    self.threatened_squares.add((self.pos_x-1, self.pos_y+direct))
            case 'R':
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    self.get_threats_in_direction(board, dx, dy)
            case 'N':
                for dx, dy in [(2, 1), (1, 2), (-2, 1), (1, -2), (2, -1), (-1, 2), (-2, -1), (-1, -2)]:
                    if 0 <= self.pos_x + dx < 8 and 0 <= self.pos_y + dy < 8:
                        self.threatened_squares.add((self.pos_x+dx, self.pos_y+dy))
            case 'B':
                for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    self.get_threats_in_direction(board, dx, dy)
            case 'Q':
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    self.get_threats_in_direction(board, dx, dy)
            case 'K':
                for dx, dy in [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]:
                    if 0 <= self.pos_x + dx < 8 and 0 <= self.pos_y + dy < 8:
                        self.threatened_squares.add((self.pos_x+dx, self.pos_y+dy))

    def get_threats_in_direction(self, board, dx, dy):
        x, y = self.pos_x + dx, self.pos_y + dy
        while 0 <= x < 8 and 0 <= y < 8:
            if not board.board[x][y] is None:
                self.threatened_squares.add((x, y))
                break
            self.threatened_squares.add((x, y))
            x += dx
            y += dy

    def get_moves(self, board):
        direct = 0
        moves = set()
        if self.colour == 'W':
            direct = -1
        elif self.colour == 'B':
            direct = 1
        match self.figure:
            case 'P':
                if 0 <= self.pos_y+direct < 8:
                    if board.board[self.pos_x][self.pos_y+direct] is None:
                        moves.add((self.pos_x, self.pos_y+direct))
                        if 0 <= self.pos_y+direct+direct < 8:
                            if self.pos_y == 6 or self.pos_y == 1:
                                if board.board[self.pos_x][self.pos_y+direct+direct] is None:
                                    moves.add((self.pos_x, self.pos_y+direct+direct))

                # taking
                if 0 <= self.pos_x+1 < 8 and 0 <= self.pos_y+direct < 8:
                    if not board.board[self.pos_x+1][self.pos_y+direct] is None:
                        if not board.board[self.pos_x+1][self.pos_y+direct].colour == self.colour:
                            moves.add((self.pos_x+1, self.pos_y+direct))
                if 0 <= self.pos_x - 1 < 8 and 0 <= self.pos_y + direct < 8:
                    if not board.board[self.pos_x-1][self.pos_y+direct] is None:
                        if not board.board[self.pos_x-1][self.pos_y+direct].colour == self.colour:
                            moves.add((self.pos_x-1, self.pos_y+direct))
            case 'R':
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    moves.update(self.get_moves_in_direction(board, dx, dy))
            case 'N':
                for dx, dy in [(2, 1), (1, 2), (-2, 1), (1, -2), (2, -1), (-1, 2), (-2, -1), (-1, -2)]:
                    if 0 <= self.pos_x + dx < 8 and 0 <= self.pos_y + dy < 8:
                        if board.board[self.pos_x+dx][self.pos_y+dy] is None:
                            moves.add((self.pos_x+dx, self.pos_y+dy))
                        elif not board.board[self.pos_x+dx][self.pos_y+dy].colour == self.colour:
                            moves.add((self.pos_x+dx, self.pos_y+dy))
            case 'B':
                for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    moves.update(self.get_moves_in_direction(board, dx, dy))
            case 'Q':
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    moves.update(self.get_moves_in_direction(board, dx, dy))
            case 'K':
                for dx, dy in [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]:
                    x, y = self.pos_x + dx, self.pos_y + dy
                    if 0 <= x < 8 and 0 <= y < 8:
                        if board.board[x][y] is None:
                            if not self.is_square_attacked_by_enemy(x, y, board):
                                moves.add((x, y))
                        else:
                            if board.board[x][y].colour != self.colour:
                                if not self.is_square_attacked_by_enemy(x, y, board):
                                    moves.add((x, y))

        return moves

    def get_moves_in_direction(self, board, dx, dy):
        moves = set()
        x, y = self.pos_x + dx, self.pos_y + dy
        while 0 <= x < 8 and 0 <= y < 8:
            if not board.board[x][y] is None:
                if not board.board[x][y].colour == self.colour:
                    moves.add((x, y))
                break
            moves.add((x, y))
            x += dx
            y += dy
        return moves

    def is_square_attacked_by_enemy(self, x, y, board):
        if self.colour == 'B':
            return (x, y) in board.threatened_squares_white
        else:
            return (x, y) in board.threatened_squares_black

    def __repr__(self):
        piece_emojis = {
            'R': {'W': '♖', 'B': '♜'},
            'N': {'W': '♘', 'B': '♞'},
            'B': {'W': '♗', 'B': '♝'},
            'K': {'W': '♔', 'B': '♚'},
            'Q': {'W': '♕', 'B': '♛'},
            'P': {'W': '♙', 'B': '♟'}
        }
        return piece_emojis[self.figure][self.colour]
