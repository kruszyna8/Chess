import chess
import tkinter as tk
from PIL import Image, ImageTk
import os

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.box_size = 50
        self.root.geometry(f"400x400")
        self.root.title("Chess app")

        self.board = chess.Board()

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
        self.canvas = tk.Canvas(self.root, width=self.box_size*8, height=self.box_size*8)
        self.canvas.pack()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#7a9db2", "#d7e2e7"]
        
        # Draw squares
        for row in range(8):
            for col in range(8):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()