import json
import tkinter as tk
import board
from board import Board
import piece

global board1
global schemes
global buttons
global select


def press(button, x, y):
    global select

    # if the pressed button corresponds to a piece belonging to the player whose turn it is, selects the piece
    if not board1.board[x][y] is None:
        if board1.board[x][y].colour == board1.turn:
            select = board1.board[x][y]
            colour_board()
            button.config(bg=schemes.get("select")["bg"])
            for sx in select.get_moves(board1):
                buttons[sx[0]][sx[1]].config(bg=schemes.get("target")["bg"])

    # if the pressed button corresponds to a possible move, make the move, and change turn
    if select is not None:
        if (x, y) in select.get_moves(board1):
            buttons[select.pos_x][select.pos_y]["text"] = ""
            board1.move_or_take(select, x, y)
            buttons[x][y]["text"] = select
            select = None
            colour_board()
            if board1.turn == 'B':
                board1.turn = 'W'
            else:
                board1.turn = 'B'
            # recalculates the threatened squares, after a move is made
            board1.get_threatened_squares('W')
            board1.get_threatened_squares('B')

    # when king is in check, highlighted. does not work
    pset = set()
    threats = set()
    if board1.turn == 'W':
        pset = board1.white_pieces
        threats = board1.threatened_squares_black
    elif board1.turn == 'B':
        pset = board1.black_pieces
        threats = board1.threatened_squares_white
    for p in pset:
        if p.figure == 'K':
            if (p.pos_x, p.pos_y) in threats:
                buttons[p.pos_x][p.pos_y].config(bg=schemes.get("threat")["bg"])


def colour_board():
    # recolours the board according to the scheme, with a checkered pattern
    colour_white = True
    for x in buttons:
        colour_white = not colour_white
        for y in x:
            if colour_white:
                y.config(bg=schemes.get("white")["bg"], fg=schemes.get("white")["fg"])
                colour_white = not colour_white
            else:
                y.config(bg=schemes.get("black")["bg"], fg=schemes.get("black")["fg"])
                colour_white = not colour_white


def threat(colour):
    # This method highlights threatened squares
    # First calling the board to calculate the threatened squares for both colours
    board1.get_threatened_squares('W')
    board1.get_threatened_squares('B')
    # Resetting the board to black and white
    colour_board()
    # takes the threatened squares of the given colour
    threats = set()
    if colour == 'W':
        threats = board1.threatened_squares_white
    elif colour == 'B':
        threats = board1.threatened_squares_black
    # colours the buttons using the set of threatened squares
    for i, x in enumerate(buttons):
        for j, y in enumerate(x):
            if (i, j) in threats:
                y.config(bg=schemes.get("threat")["bg"])


def populate():
    # resets the text on all buttons to correspond with the board
    # only needed for loading, because the buttons are never out of sync otherwise
    for x in range(8):
        for y in range(8):
            if board1.board[x][y] is not None:
                buttons[x][y].config(text=board1.board[x][y])
            else:
                buttons[x][y].config(text="")
    board1.get_threatened_squares('W')
    board1.get_threatened_squares('B')


def save():
    global board1
    # calls the save function from board1
    board1.save('board.json')


def load():
    global board1
    global select
    # calling the class function load to convert and giving it the JSON file
    board1 = Board.load('board.json')

    # resetting the board states and button texts
    board1.populate()
    populate()
    select = None


if __name__ == '__main__':
    # initialising the window
    gui = tk.Tk()
    gui.title('Chess')
    gui.geometry('250x250')

    # initialising a new board, will be replaced if a board is later loaded
    board1 = board.Board()
    # adding pawns
    for x in range(8):
        board1.add_piece(piece.Piece(x, 6, 'P', 'W'))
        board1.add_piece(piece.Piece(x, 1, 'P', 'B'))
    # adding specials
    for x, p in enumerate(['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']):
        board1.add_piece(piece.Piece(x, 7, p, 'W'))
        board1.add_piece(piece.Piece(x, 0, p, 'B'))
    board1.populate()

    select = None

    # colour schemes for all the different button states
    schemes = {
        "black": {"bg": "#ffffff", "fg": "#000000"},
        "white": {"bg": "#000000", "fg": "#ffffff"},
        "select": {"bg": "#0000ff"},
        "target": {"bg": "#00ff00"},
        "threat": {"bg": "#ff0000"}
    }

    # setting up a 2D List of buttons that each already get their corresponding piece written on them
    buttons = []
    for x in range(8):
        buttons.append([])
        for y in range(8):
            button = tk.Button(gui, text=board1.board[x][y], width=2, height=1,
                               command=lambda x=x, y=y: press(buttons[x][y], x, y))
            button.grid(row=y, column=x, padx=1, pady=1)

            buttons[x].append(button)

    # initialising and setting up all the extra buttons on the side
    save_button = tk.Button(gui, text='S', width=2, height=1, command=lambda: save())
    save_button.grid(row=0, column=8, padx=2, pady=1)
    load_button = tk.Button(gui, text='L', width=2, height=1, command=lambda: load())
    load_button.grid(row=1, column=8, padx=4, pady=1)
    threat_w_button = tk.Button(gui, text='TW', width=2, height=1, command=lambda: threat('W'))
    threat_w_button.grid(row=2, column=8, padx=4, pady=1)
    threat_b_button = tk.Button(gui, text='TB', width=2, height=1, command=lambda: threat('B'))
    threat_b_button.grid(row=3, column=8, padx=4, pady=1)
    colour_board()

    # running the window
    gui.mainloop()
