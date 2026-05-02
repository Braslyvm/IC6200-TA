"""
gui.py — Qt5 interface for the Hospital Hill-Climbing Optimizer.
Single large board. Imports utils and hc directly.
"""

import sys
import copy

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QSpinBox, QGroupBox,
    QStatusBar, QScrollArea, QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "hill-climbing"))

sys.path.append(HC_DIR)

import utils
import hc


# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0f1117"
SURFACE   = "#1a1d27"
SURFACE2  = "#232638"
ACCENT    = "#4f7fff"
ACCENT2   = "#7c5cfc"
SUCCESS   = "#3ecf8e"
WARNING   = "#f5a623"
TEXT      = "#e8eaf6"
TEXT_DIM  = "#6b7280"
BORDER    = "#2e3150"

CELL_EMPTY    = "#1e2235"
CELL_HOUSE    = "#c47a00"
CELL_HOSPITAL = "#1e7a55"
CELL_BORDER   = "#2e3150"

CELL_SIZE     = 90
EMOJI_FONT_SZ = 34


# ── Cell ─────────────────────────────────────────────────────────────────────
class CellWidget(QLabel):
    def __init__(self, x, y, win):
        super().__init__()
        self.gx, self.gy, self.win = x, y, win
        self.setFixedSize(CELL_SIZE, CELL_SIZE)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Segoe UI Emoji", EMOJI_FONT_SZ))
        self.setCursor(Qt.PointingHandCursor)
        self.refresh()

    def refresh(self):
        val = self.win.board[self.gy][self.gx]
        if val == utils.OBJECT_HOSPITAL:
            bg, text = CELL_HOSPITAL, utils.OBJECT_HOSPITAL
        elif val == utils.OBJECT_HOUSE:
            bg, text = CELL_HOUSE, utils.OBJECT_HOUSE
        else:
            bg, text = CELL_EMPTY, ""
        self.setText(text)
        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                border: 2px solid {CELL_BORDER};
                border-radius: 10px;
            }}
            QLabel:hover {{
                border: 2px solid {ACCENT};
                background: {'#2a3a6a' if bg == CELL_EMPTY else bg};
            }}
        """)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.win.cycle_cell(self.gx, self.gy)
        elif e.button() == Qt.RightButton:
            self.win.clear_cell(self.gx, self.gy)
        super().mousePressEvent(e)


# ── Board ─────────────────────────────────────────────────────────────────────
class BoardWidget(QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.gl = QGridLayout()
        self.gl.setSpacing(5)
        self.gl.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.gl)
        self.cells = []
        self.rebuild()

    def rebuild(self):
        for row in self.cells:
            for c in row:
                self.gl.removeWidget(c)
                c.deleteLater()
        self.cells = []
        for y in range(len(self.win.board)):
            row = []
            for x in range(len(self.win.board[0])):
                c = CellWidget(x, y, self.win)
                self.gl.addWidget(c, y, x)
                row.append(c)
            self.cells.append(row)

    def refresh_all(self):
        for row in self.cells:
            for c in row:
                c.refresh()


# ── Main Window ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Optimizer  •  Hill Climbing")
        self.resize(2000, 780)
        self.board = self._default_board()
        self._apply_style()
        self._build_ui()
        self._refresh_stats()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background: {BG};
                color: {TEXT};
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 13px;
            }}
            QGroupBox {{
                border: 1.5px solid {BORDER};
                border-radius: 10px;
                margin-top: 12px;
                padding: 10px 8px 8px 8px;
                font-weight: 600;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
                color: {ACCENT};
                font-size: 12px;
            }}
            QSpinBox {{
                background: {SURFACE2};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 4px 8px;
                color: {TEXT};
                min-width: 60px;
            }}
            QScrollArea {{ border: none; background: {SURFACE}; }}
            QStatusBar {{
                background: {SURFACE};
                color: {TEXT_DIM};
                font-size: 11px;
                border-top: 1px solid {BORDER};
            }}
        """)

    def _default_board(self):
        H, h, N = utils.OBJECT_HOSPITAL, utils.OBJECT_HOUSE, None
        return [
            [N, N, N, N, H, N, N, N, h, N],
            [N, N, h, N, N, N, N, N, N, N],
            [N, N, N, N, N, N, N, N, N, N],
            [N, h, N, N, N, N, N, N, N, H],
            [N, N, N, N, N, N, h, N, N, N],
        ]

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        main_h = QHBoxLayout(root)
        main_h.setContentsMargins(14, 14, 14, 14)
        main_h.setSpacing(14)

        # ── Sidebar ───────────────────────────────────────────────────────
        sidebar = QVBoxLayout()
        sidebar.setSpacing(12)
        sidebar.setAlignment(Qt.AlignTop)

        # Size
        size_box = QGroupBox("Dimensiones")
        sf = QVBoxLayout(size_box)
        sf.setSpacing(6)
        sf.addWidget(self._dim_label("Filas"))
        self.spin_rows = self._spinbox(2, 15, len(self.board))
        sf.addWidget(self.spin_rows)
        sf.addWidget(self._dim_label("Columnas"))
        self.spin_cols = self._spinbox(2, 20, len(self.board[0]))
        sf.addWidget(self.spin_cols)
        sf.addSpacing(4)
        sf.addWidget(self._small_btn("Aplicar tamaño", self.resize_board))
        sidebar.addWidget(size_box)

        # Legend
        leg_box = QGroupBox("Celdas  (click izq. para ciclar)")
        lf = QVBoxLayout(leg_box)
        lf.setSpacing(6)
        for emoji, label, color in [
            ("⬜", "Vacío",   TEXT_DIM),
            (utils.OBJECT_HOUSE,    "Casa",    WARNING),
            (utils.OBJECT_HOSPITAL, "Hospital", SUCCESS),
        ]:
            rw = QWidget()
            rl = QHBoxLayout(rw)
            rl.setContentsMargins(0, 0, 0, 0)
            ic = QLabel(emoji)
            ic.setFont(QFont("Segoe UI Emoji", 18))
            lb = QLabel(label)
            lb.setStyleSheet(f"color:{color}; font-weight:600;")
            rl.addWidget(ic); rl.addWidget(lb); rl.addStretch()
            lf.addWidget(rw)
        note = QLabel("Click derecho → limpiar celda")
        note.setStyleSheet(f"color:{TEXT_DIM}; font-size:11px;")
        lf.addWidget(note)
        sidebar.addWidget(leg_box)

        # Stats
        stats_box = QGroupBox("Estadísticas")
        stf = QVBoxLayout(stats_box)
        stf.setSpacing(6)
        self.lbl_hospitals = self._stat_row(stf, "Hospitales")
        self.lbl_houses    = self._stat_row(stf, "Casas")
        self.lbl_cost_cur  = self._stat_row(stf, "Costo actual")
        self.lbl_cost_opt  = self._stat_row(stf, "Costo óptimo")
        self.lbl_improve   = self._stat_row(stf, "Mejora")
        sidebar.addWidget(stats_box)

        # Buttons
        sidebar.addSpacing(4)
        sidebar.addWidget(self._small_btn("🔄  Tablero por defecto", self.reset_board))
        sidebar.addWidget(self._small_btn("⬜  Limpiar tablero",     self.clear_board))
        sidebar.addSpacing(8)

        run_btn = QPushButton("🚀  Ejecutar Hill Climbing")
        run_btn.setFixedHeight(50)
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        run_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {ACCENT}, stop:1 {ACCENT2});
                color: white; border: none; border-radius: 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #6690ff, stop:1 #9a7dff);
            }}
            QPushButton:pressed {{ background: {ACCENT}; }}
        """)
        run_btn.clicked.connect(self.run_hc)
        sidebar.addWidget(run_btn)
        sidebar.addStretch()

        sw = QWidget()
        sw.setLayout(sidebar)
        sw.setFixedWidth(215)
        main_h.addWidget(sw)

        # ── Board (large, single) ─────────────────────────────────────────
        board_box = QGroupBox("Tablero")
        board_box.setStyleSheet(f"""
            QGroupBox {{
                border: 1.5px solid {BORDER};
                border-radius: 12px;
                margin-top: 12px;
                padding: 10px;
                font-weight: 700;
                font-size: 14px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 14px; padding: 0 6px;
                color: {ACCENT};
            }}
        """)
        bbl = QVBoxLayout(board_box)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignCenter)
        self.board_widget = BoardWidget(self)
        scroll.setWidget(self.board_widget)
        bbl.addWidget(scroll)
        main_h.addWidget(board_box, stretch=1)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(
            "Listo — click izquierdo: ciclar celda  |  click derecho: limpiar celda"
        )

    # ── Helper widgets ────────────────────────────────────────────────────
    def _dim_label(self, t):
        l = QLabel(t)
        l.setStyleSheet(f"color:{TEXT_DIM}; font-size:11px;")
        return l

    def _spinbox(self, lo, hi, val):
        s = QSpinBox(); s.setRange(lo, hi); s.setValue(val); return s

    def _small_btn(self, label, slot):
        btn = QPushButton(label)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(34)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {SURFACE2}; color: {TEXT};
                border: 1px solid {BORDER}; border-radius: 8px; padding: 0 8px;
            }}
            QPushButton:hover {{ border-color: {ACCENT}; color: {ACCENT}; }}
        """)
        btn.clicked.connect(slot)
        return btn

    def _stat_row(self, layout, key):
        rw = QWidget()
        rl = QHBoxLayout(rw); rl.setContentsMargins(0, 0, 0, 0)
        k = QLabel(key + ":"); k.setStyleSheet(f"color:{TEXT_DIM}; font-size:12px;")
        v = QLabel("—");       v.setStyleSheet(f"color:{TEXT}; font-weight:700;")
        rl.addWidget(k); rl.addStretch(); rl.addWidget(v)
        layout.addWidget(rw)
        rw._v = v
        return rw

    def _set_stat(self, rw, text, color=TEXT):
        rw._v.setText(text)
        rw._v.setStyleSheet(f"color:{color}; font-weight:700;")

    # ── Board actions ─────────────────────────────────────────────────────
    def cycle_cell(self, x, y):
        cur = self.board[y][x]
        self.board[y][x] = (
            utils.OBJECT_HOUSE    if cur is None else
            utils.OBJECT_HOSPITAL if cur == utils.OBJECT_HOUSE else
            None
        )
        self.board_widget.refresh_all()
        self._refresh_stats()

    def clear_cell(self, x, y):
        self.board[y][x] = None
        self.board_widget.refresh_all()
        self._refresh_stats()

    def clear_board(self):
        r, c = len(self.board), len(self.board[0])
        self.board = [[None]*c for _ in range(r)]
        self.board_widget.refresh_all()
        self._refresh_stats()
        self.status.showMessage("Tablero limpiado.")

    def reset_board(self):
        self.board = self._default_board()
        self.spin_rows.setValue(len(self.board))
        self.spin_cols.setValue(len(self.board[0]))
        self.board_widget.rebuild()
        self._refresh_stats()
        self.status.showMessage("Tablero restaurado al ejemplo por defecto.")

    def resize_board(self):
        nr, nc = self.spin_rows.value(), self.spin_cols.value()
        or_, oc = len(self.board), len(self.board[0])
        nb = [[None]*nc for _ in range(nr)]
        for y in range(min(or_, nr)):
            for x in range(min(oc, nc)):
                nb[y][x] = self.board[y][x]
        self.board = nb
        self.board_widget.rebuild()
        self._refresh_stats()
        self.status.showMessage(f"Tablero redimensionado a {nr}×{nc}.")

    # ── Algorithm ─────────────────────────────────────────────────────────
    def run_hc(self):
        if not utils.find_objects(self.board, utils.OBJECT_HOSPITAL):
            QMessageBox.warning(self, "Sin hospitales",
                "Coloca al menos un hospital 🏥 en el tablero.")
            return
        if not utils.find_objects(self.board, utils.OBJECT_HOUSE):
            QMessageBox.warning(self, "Sin casas",
                "Coloca al menos una casa 🏠 en el tablero.")
            return

        initial_cost = utils.cost(self.board)
        result_map   = hc.hill_climbing(copy.deepcopy(self.board))
        final_cost   = utils.cost(result_map)
        improvement  = initial_cost - final_cost

        # Apply optimized positions directly to the single board
        self.board = result_map
        self.board_widget.refresh_all()

        self._refresh_stats(skip_opt=True)
        self._set_stat(self.lbl_cost_opt, str(final_cost), SUCCESS)
        self._set_stat(self.lbl_improve,
            f"−{improvement}" if improvement > 0 else "sin mejora",
            SUCCESS if improvement > 0 else TEXT_DIM)

        self.status.showMessage(
            f"✅  Completado — Costo inicial: {initial_cost}  →  "
            f"Costo final: {final_cost}  (mejora: {improvement})"
        )

    # ── Stats ─────────────────────────────────────────────────────────────
    def _refresh_stats(self, skip_opt=False):
        h  = utils.find_objects(self.board, utils.OBJECT_HOSPITAL)
        ho = utils.find_objects(self.board, utils.OBJECT_HOUSE)
        cc = utils.cost(self.board)
        self._set_stat(self.lbl_hospitals, str(len(h)))
        self._set_stat(self.lbl_houses,    str(len(ho)))
        self._set_stat(self.lbl_cost_cur,  str(cc))
        if not skip_opt:
            self._set_stat(self.lbl_cost_opt, "—")
            self._set_stat(self.lbl_improve,  "—", TEXT_DIM)


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 12))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
