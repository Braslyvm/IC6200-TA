import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ruta relativa hacia la carpeta donde están minimax.py y utils.py
ruta_actual = os.path.dirname(__file__)
ruta_modulos = os.path.join(ruta_actual, "tic-tac-toe")
sys.path.append(ruta_modulos)

from minimax import ai_play
from utils import terminal, utility, result, players, PLAYER_X, PLAYER_O


class TicTacToeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gato - Minimax Retro")
        self.root.geometry("680x760")
        self.root.resizable(False, False)
        self.root.configure(bg="#111111")

        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        self.human_mark = PLAYER_X
        self.game_over = False
        self.ia_vs_ia = False
        self.ai_loop_running = False

        self.status_var = tk.StringVar(value="Turno de X")
        self.detail_var = tk.StringVar(value="Selecciona una opción para empezar.")
        self.mode_var = tk.StringVar(value="Modo: Jugador vs IA")

        self.build_ui()
        self.update_turn_labels()

    def build_ui(self):
        # =========================
        # ENCABEZADO
        # =========================
        header = tk.Frame(self.root, bg="#111111")
        header.pack(fill="x", padx=18, pady=(18, 10))

        title = tk.Label(
            header,
            text="TIC TAC TOE",
            font=("Courier New", 28, "bold"),
            bg="#111111",
            fg="#00ff66"
        )
        title.pack(anchor="center")

        subtitle = tk.Label(
            header,
            text="MINIMAX ARCADE",
            font=("Courier New", 12, "bold"),
            bg="#111111",
            fg="#00ccff"
        )
        subtitle.pack(anchor="center", pady=(4, 0))

        # =========================
        # PANEL SUPERIOR
        # =========================
        top_panel = tk.Frame(
            self.root,
            bg="#1b1b1b",
            highlightthickness=2,
            highlightbackground="#00ff66"
        )
        top_panel.pack(fill="x", padx=18, pady=(8, 12))

        # Fila 1: ficha + botones
        row1 = tk.Frame(top_panel, bg="#1b1b1b")
        row1.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(
            row1,
            text="Ficha:",
            font=("Courier New", 12, "bold"),
            bg="#1b1b1b",
            fg="#ffffff"
        ).pack(side="left")

        self.mark_var = tk.StringVar(value=PLAYER_X)

        tk.Radiobutton(
            row1,
            text="X",
            value=PLAYER_X,
            variable=self.mark_var,
            command=self.change_player_mark,
            font=("Courier New", 12, "bold"),
            bg="#1b1b1b",
            fg="#00ff66",
            selectcolor="#222222",
            activebackground="#1b1b1b",
            activeforeground="#00ff66"
        ).pack(side="left", padx=(10, 6))

        tk.Radiobutton(
            row1,
            text="O",
            value=PLAYER_O,
            variable=self.mark_var,
            command=self.change_player_mark,
            font=("Courier New", 12, "bold"),
            bg="#1b1b1b",
            fg="#00ccff",
            selectcolor="#222222",
            activebackground="#1b1b1b",
            activeforeground="#00ccff"
        ).pack(side="left", padx=(0, 20))

        # Frame para botones iguales
        buttons_frame = tk.Frame(row1, bg="#1b1b1b")
        buttons_frame.pack(side="left", fill="x", expand=True)

        buttons_frame.grid_columnconfigure(0, weight=1, uniform="btn")
        buttons_frame.grid_columnconfigure(1, weight=1, uniform="btn")
        buttons_frame.grid_columnconfigure(2, weight=1, uniform="btn")

        tk.Button(
            buttons_frame,
            text="REINICIAR",
            command=self.reset_game,
            font=("Courier New", 11, "bold"),
            bg="#ffcc00",
            fg="#111111",
            activebackground="#ffd633",
            activeforeground="#111111",
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2"
        ).grid(row=0, column=0, padx=5, sticky="ew")

        tk.Button(
            buttons_frame,
            text="IA vs IA",
            command=self.start_ai_vs_ai,
            font=("Courier New", 11, "bold"),
            bg="#ff3366",
            fg="white",
            activebackground="#ff4d79",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2"
        ).grid(row=0, column=1, padx=5, sticky="ew")

        tk.Button(
            buttons_frame,
            text="DETENER IA",
            command=self.stop_ai_vs_ai,
            font=("Courier New", 11, "bold"),
            bg="#666666",
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2"
        ).grid(row=0, column=2, padx=5, sticky="ew")

        # Fila 2: estado
        row2 = tk.Frame(top_panel, bg="#1b1b1b")
        row2.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            row2,
            textvariable=self.status_var,
            font=("Courier New", 15, "bold"),
            bg="#1b1b1b",
            fg="#ffffff"
        ).pack(anchor="w")

        tk.Label(
            row2,
            textvariable=self.detail_var,
            font=("Courier New", 10),
            bg="#1b1b1b",
            fg="#bbbbbb"
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            row2,
            textvariable=self.mode_var,
            font=("Courier New", 10, "bold"),
            bg="#1b1b1b",
            fg="#00ccff"
        ).pack(anchor="w", pady=(4, 0))

        # =========================
        # TABLERO
        # =========================
        board_frame = tk.Frame(
            self.root,
            bg="#111111",
            highlightthickness=2,
            highlightbackground="#00ccff"
        )
        board_frame.pack(padx=18, pady=10)

        self.buttons = []
        grid = tk.Frame(board_frame, bg="#111111")
        grid.pack(padx=18, pady=18)

        for y in range(3):
            row = []
            for x in range(3):
                btn = tk.Button(
                    grid,
                    text="",
                    font=("Courier New", 30, "bold"),
                    width=4,
                    height=2,
                    bg="#1f1f1f",
                    fg="#ffffff",
                    activebackground="#2a2a2a",
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    highlightthickness=2,
                    highlightbackground="#444444",
                    command=lambda px=x, py=y: self.on_click(px, py),
                    cursor="hand2"
                )
                btn.grid(row=y, column=x, padx=6, pady=6)
                row.append(btn)
            self.buttons.append(row)

        # =========================
        # PANEL INFERIOR
        # =========================
        bottom_panel = tk.Frame(
            self.root,
            bg="#1b1b1b",
            highlightthickness=2,
            highlightbackground="#ffcc00"
        )
        bottom_panel.pack(fill="x", padx=18, pady=(14, 0))

        tk.Button(
            bottom_panel,
            text="JUGADA IA",
            command=self.play_ai_turn,
            font=("Courier New", 12, "bold"),
            bg="#00ccff",
            fg="#111111",
            activebackground="#33d6ff",
            activeforeground="#111111",
            relief="flat",
            bd=0,
            padx=14,
            pady=10,
            cursor="hand2"
        ).pack(pady=14)

    def change_player_mark(self):
        self.human_mark = self.mark_var.get()
        self.stop_ai_vs_ai(silent=True)
        self.reset_game()

        if self.human_mark == PLAYER_O:
            self.detail_var.set("La IA inicia porque X siempre juega primero.")
            self.root.after(400, self.play_ai_turn)

    def reset_game(self):
        self.stop_ai_vs_ai(silent=True)

        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.game_over = False
        self.detail_var.set("Haz clic en una casilla para jugar.")
        self.mode_var.set("Modo: Jugador vs IA")

        for y in range(3):
            for x in range(3):
                self.buttons[y][x].config(
                    text="",
                    state="normal",
                    bg="#1f1f1f",
                    fg="#ffffff",
                    highlightbackground="#444444"
                )

        self.update_turn_labels()

    def start_ai_vs_ai(self):
        self.reset_game()
        self.ia_vs_ia = True
        self.ai_loop_running = True
        self.mode_var.set("Modo: IA vs IA")
        self.detail_var.set("Las dos IAs están jugando.")
        self.root.after(500, self.run_ai_vs_ai)

    def stop_ai_vs_ai(self, silent=False):
        self.ia_vs_ia = False
        self.ai_loop_running = False
        if not silent and not self.game_over:
            self.mode_var.set("Modo: Jugador vs IA")
            self.detail_var.set("Modo IA vs IA detenido.")

    def run_ai_vs_ai(self):
        if not self.ai_loop_running or self.game_over:
            return

        if terminal(self.board):
            self.check_game_end()
            return

        move = ai_play(self.board)
        if move is None:
            self.check_game_end()
            return

        self.board = result(self.board, move)
        self.refresh_board()

        if self.check_game_end():
            return

        self.root.after(650, self.run_ai_vs_ai)

    def on_click(self, x, y):
        if self.game_over:
            return

        if self.ia_vs_ia:
            self.detail_var.set("Desactiva IA vs IA para jugar manualmente.")
            return

        if players(self.board) != self.human_mark:
            self.detail_var.set("Espera el turno de la IA.")
            return

        if self.board[y][x] is not None:
            self.detail_var.set("Esa casilla ya está ocupada.")
            return

        self.board = result(self.board, (x, y))
        self.refresh_board()

        if self.check_game_end():
            return

        self.root.after(300, self.play_ai_turn)

    def play_ai_turn(self):
        if self.game_over:
            return

        if terminal(self.board):
            self.check_game_end()
            return

        if not self.ia_vs_ia and players(self.board) == self.human_mark:
            return

        move = ai_play(self.board)

        if move is None:
            self.check_game_end()
            return

        self.board = result(self.board, move)
        self.refresh_board()
        self.check_game_end()

    def refresh_board(self):
        for y in range(3):
            for x in range(3):
                value = self.board[y][x]

                color = "#ffffff"
                if value == PLAYER_X:
                    color = "#00ff66"
                elif value == PLAYER_O:
                    color = "#00ccff"

                self.buttons[y][x].config(
                    text="" if value is None else value,
                    fg=color
                )

        self.update_turn_labels()

    def update_turn_labels(self):
        if self.game_over:
            return

        current = players(self.board)
        self.status_var.set(f"Turno de {current}")

        if self.ia_vs_ia:
            self.detail_var.set("La IA está calculando la siguiente jugada...")
            return

        if current == self.human_mark:
            self.detail_var.set("Te toca jugar.")
        else:
            self.detail_var.set("La IA está calculando la mejor jugada.")

    def get_winning_cells(self):
        lines = []

        # Filas
        for y in range(3):
            lines.append([(0, y), (1, y), (2, y)])

        # Columnas
        for x in range(3):
            lines.append([(x, 0), (x, 1), (x, 2)])

        # Diagonales
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(2, 0), (1, 1), (0, 2)])

        for line in lines:
            values = [self.board[y][x] for x, y in line]
            if values[0] is not None and values[0] == values[1] == values[2]:
                return line, values[0]

        return None, None

    def highlight_winning_line(self, winning_cells):
        for x, y in winning_cells:
            self.buttons[y][x].config(
                bg="#2d5a27",
                highlightbackground="#00ff66"
            )

    def show_end_message(self, title, message):
        messagebox.showinfo(title, message)

    def check_game_end(self):
        if not terminal(self.board):
            self.update_turn_labels()
            return False

        self.game_over = True
        self.ai_loop_running = False

        winning_cells, winner = self.get_winning_cells()

        for y in range(3):
            for x in range(3):
                self.buttons[y][x].config(state="disabled")

        if winning_cells:
            self.highlight_winning_line(winning_cells)

        score = utility(self.board)

        if score == 1:
            self.status_var.set("¡¡ GANÓ X !!")
            self.detail_var.set("La partida terminó con victoria para X.")
            self.show_end_message("Fin de la partida", "¡Ganó X!\n\nSe marcó la línea ganadora.")
        elif score == -1:
            self.status_var.set("¡¡ GANÓ O !!")
            self.detail_var.set("La partida terminó con victoria para O.")
            self.show_end_message("Fin de la partida", "¡Ganó O!\n\nSe marcó la línea ganadora.")
        else:
            self.status_var.set("== EMPATE ==")
            self.detail_var.set("No quedan jugadas disponibles.")
            self.show_end_message("Fin de la partida", "La partida terminó en empate.")

        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()