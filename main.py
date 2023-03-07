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
    board1.get_threatened_squares('W')
    board1.get_threatened_squares('B')

    # when king is in check, highlighted. does not work, because the board is recouloured after
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
                buttons[p.pos_x][p.pos_y].config(bg=schemes.get("target")["bg"])

    if not board1.board[x][y] is None:
        if board1.board[x][y].colour == board1.turn:
            select = board1.board[x][y]
            colour_board()
            button.config(bg=schemes.get("select")["bg"])
            for sx in select.get_moves(board1):
                buttons[sx[0]][sx[1]].config(bg=schemes.get("target")["bg"])
    if select is not None:
        if (x, y) in select.get_moves(board1):
            buttons[select.pos_x][select.pos_y]["text"] = ""
            board1.move_or_take_piece(select, x, y)
            buttons[x][y]["text"] = select
            select = None
            colour_board()
            if board1.turn == 'B':
                board1.turn = 'W'
            else:
                board1.turn = 'B'


def colour_board():
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
    board1.get_threatened_squares('W')
    board1.get_threatened_squares('B')
    colour_board()
    threats = set()
    if colour == 'W':
        threats = board1.threatened_squares_white
    elif colour == 'B':
        threats = board1.threatened_squares_black
    for i, x in enumerate(buttons):
        for j, y in enumerate(x):
            if (i, j) in threats:
                y.config(bg=schemes.get("threat")["bg"])


def save():
    global board1
    board1.save('board.json')


def load():
    global board1
    global select
    board1 = Board.load('board.json')
    board1.populate()
    select = None


if __name__ == '__main__':
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

    schemes = {
        "black": {"bg": "#ffffff", "fg": "#000000"},
        "white": {"bg": "#000000", "fg": "#ffffff"},
        "select": {"bg": "#0000ff"},
        "target": {"bg": "#00ff00"},
        "threat": {"bg": "#ff0000"}
    }

    buttons = []

    for x in range(8):
        buttons.append([])
        for y in range(8):
            button = tk.Button(gui, text=board1.board[x][y], width=2, height=1,
                               command=lambda x=x, y=y: press(buttons[x][y], x, y))
            button.grid(row=y, column=x, padx=1, pady=1)

            buttons[x].append(button)
    save_button = tk.Button(gui, text='S', width=2, height=1, command=lambda: save())
    save_button.grid(row=0, column=8, padx=2, pady=1)
    load_button = tk.Button(gui, text='L', width=2, height=1, command=lambda: load())
    load_button.grid(row=1, column=8, padx=4, pady=1)
    threat_w_button = tk.Button(gui, text='TW', width=2, height=1, command=lambda: threat('W'))
    threat_w_button.grid(row=2, column=8, padx=4, pady=1)
    threat_b_button = tk.Button(gui, text='TB', width=2, height=1, command=lambda: threat('B'))
    threat_b_button.grid(row=3, column=8, padx=4, pady=1)
    colour_board()

    gui.mainloop()
