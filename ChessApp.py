import chess
import tkinter as tk
from PIL import Image, ImageTk
import os

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.box_size = 50
        self.root.geometry(f"730x500")
        self.root.title("Chess app")
        self.root.bind("<Escape>", lambda event: self.root.quit())

        self.board = chess.Board()
        self.selected_square = None
        self.game_on = False

        self.load_piece_images()
        self.initialize_window()

    def load_piece_images(self):
        self.piece_images = {}
        image_folder = "images"

        for piece in ["p", "n", "b", "r", "q", "k"]:
            for color in ["w", "b"]:
                file_name = f"{piece}{color}.png"
                file_path = os.path.join(image_folder, file_name)
                if os.path.exists(file_path):
                    image = Image.open(file_path)
                    image = image.resize((50, 50), Image.Resampling.LANCZOS)
                    self.piece_images[f"{piece}{color}"] = ImageTk.PhotoImage(image)

    def initialize_window(self):
        # Main frame for layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(padx=10, pady=10)

        # Status label
        self.status_label = tk.Label(self.main_frame, text="Start game", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Chessboard
        self.canvas = tk.Canvas(self.main_frame, width=self.box_size * 8, height=self.box_size * 8, bg="white")
        self.canvas.grid(row=1, column=0, rowspan=2, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_left_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.draw_board()

        # Frame for buttons and logs
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=1, column=1, padx=10, sticky="n")

        # Buttons
        self.start_button = tk.Button(self.right_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.right_frame, text="Stop Game", command=self.stop_game)
        self.stop_button.pack(pady=5)

        # Logs
        self.log_field = tk.Text(self.main_frame, height=20, width=30, state="disabled")
        self.log_field.grid(row=2, column=1, padx=10, pady=10, sticky="n")

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#7a9db2", "#d7e2e7"]
        selected_color = "#6dbbd2"
        hint_circle_color = "#bac4c7"
        hint_cross_color = "red"
        hint_size = 10

        selected_col = -1
        selected_row = -1

        if self.selected_square is not None:
            selected_col = chess.square_file(self.selected_square)
            selected_row = row = 7 - chess.square_rank(self.selected_square)

        # Draw squares
        for row in range(8):
            for col in range(8):
                if (row == selected_row and col == selected_col):
                    color = selected_color
                else:
                    color = colors[(row + col) % 2]
                x1 = col * self.box_size
                y1 = row * self.box_size
                x2 = x1 + self.box_size
                y2 = y1 + self.box_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        
        # Draw pieces
        for square, piece in self.board.piece_map().items():
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            x = col * self.box_size
            y = row * self.box_size
            piece_symbol = piece.symbol()
            color = "w" if piece_symbol.isupper() else "b"
            piece_type = piece_symbol.lower()
            self.canvas.create_image(x + self.box_size / 2, y + self.box_size / 2, image=self.piece_images[f"{piece_type}{color}"])

        # Draw possible moves
        if self.selected_square is not None:
            for move in self.board.legal_moves:
                if move.from_square == self.selected_square:
                    col = chess.square_file(move.to_square)
                    row = 7 - chess.square_rank(move.to_square)
                    x = col * self.box_size + self.box_size / 2
                    y = row * self.box_size + self.box_size / 2
                    if self.board.is_capture(move):
                        offset = hint_size
                        self.canvas.create_line(x - offset, y - offset, x + offset, y + offset, fill=hint_cross_color, width=2)
                        self.canvas.create_line(x - offset, y + offset, x + offset, y - offset, fill=hint_cross_color, width=2)
                    else:
                        self.canvas.create_oval(x - hint_size, y - hint_size, x + hint_size, y + hint_size, fill=hint_circle_color)
        
    def on_canvas_left_click(self, event):
        if self.game_on == False:
            return

        col = event.x // self.box_size
        row = event.y // self.box_size
        square =  chess.square(col, 7 - row)

        if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
            self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None

                if self.board.is_game_over():
                    self.stop_game()
                else:
                    self.update_status()
            else:
                self.selected_square = None

        self.draw_board()

    def on_canvas_right_click(self, event):
        if self.game_on == False:
            return
        self.selected_square = None
        self.draw_board()

    def update_status(self):
        text = ""
        if self.game_on == False and self.board.is_game_over():
            result = self.board.result()
            if result == "1-0":
                text = "White wins!"
            elif result == "0-1":
                text = "Black wins!"
            else:
                text = "It's a draw!"
        elif self.game_on == False:
            text = "Start game"
        elif self.board.turn:
            text = "White's turn"
        else:
            text = "Black's turn"

        self.status_label.config(text=text)

    def start_game(self):
        self.game_on = True
        self.selected_square = None
        self.board.reset()
        self.update_status()
        self.draw_board()

    def stop_game(self):
        self.game_on = False
        self.selected_square = None
        self.update_status()
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()