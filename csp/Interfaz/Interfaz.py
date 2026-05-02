import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QGroupBox, QFrame,
    QComboBox, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QMessageBox, QSplitter,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import (
    QFont, QColor, QBrush, QPen, QPainter, QTextCursor,
)
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSP_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "cps_backtracking", "csp")
)

sys.path.append(CSP_PATH)


# ── Importar lógica CSP desde csp.py ──────────────────────────────────────────
from csp import (
    Course,
    initialize,
    backtracking,
    backtracking_with_inference,
    select_mrv,
    select_degree,
    select_mrv_degree,
    _select_first,
)

# ── Paleta ─────────────────────────────────────────────────────────────────────
BG_DARK      = "#0d0f14"
BG_CARD      = "#161a23"
BG_PANEL     = "#1c2130"
ACCENT_BLUE  = "#4fa3e0"
ACCENT_CYAN  = "#00d4aa"
ACCENT_ERR   = "#e05050"
ACCENT_OK    = "#4caf82"
TEXT_PRIMARY = "#e8edf5"
TEXT_MUTED   = "#6b7a99"
BORDER       = "#252d3d"


# ── Hilo del solver ────────────────────────────────────────────────────────────

class SolverThread(QThread):
    done_signal = pyqtSignal(bool, dict)   # (success, {name: value})

    def __init__(self, variables, domain, constraints, algorithm):
        super().__init__()
        self.variables   = variables
        self.domain      = domain
        self.constraints = constraints
        self.algorithm   = algorithm

    def run(self):
        courses  = initialize(self.variables, self.domain)
        assigned = []

        select_map = {
            "backtracking_inference_first":      _select_first,
            "backtracking_inference_mrv":        select_mrv,
            "backtracking_inference_degree":     select_degree,
            "backtracking_inference_mrv_degree": select_mrv_degree,
        }

        if self.algorithm == "backtracking":
            first     = courses[0]
            remaining = courses[1:]
            success   = backtracking(first, remaining, assigned, self.constraints)
        else:
            select_fn = select_map.get(self.algorithm, _select_first)
            success   = backtracking_with_inference(
                courses, assigned, self.constraints, select_fn
            )

        final = {c.name: c.value for c in courses} if success else {}
        self.done_signal.emit(success, final)


# ── Grafo ──────────────────────────────────────────────────────────────────────

class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet(
            f"background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 8px;"
        )
        self._node_items = {}
        self._val_labels = {}

    def build(self, variables, constraints):
        self.scene.clear()
        self._node_items.clear()
        self._val_labels.clear()

        if not variables:
            return

        n  = len(variables)
        cx, cy, r = 200, 185, 145
        positions = {}

        for i, var in enumerate(variables):
            angle = 2 * math.pi * i / n - math.pi / 2
            positions[var] = (
                cx + r * math.cos(angle),
                cy + r * math.sin(angle),
            )

        # Aristas
        drawn = set()
        for con in constraints:
            left, right = con.split("!=")
            key = tuple(sorted([left, right]))
            if key in drawn or left not in positions or right not in positions:
                continue
            drawn.add(key)
            x1, y1 = positions[left]
            x2, y2 = positions[right]
            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(QPen(QColor(BORDER), 1.5))
            self.scene.addItem(line)

        # Nodos
        nr = 24
        for var, (x, y) in positions.items():
            ellipse = QGraphicsEllipseItem(x - nr, y - nr, nr * 2, nr * 2)
            ellipse.setBrush(QBrush(QColor(BG_PANEL)))
            ellipse.setPen(QPen(QColor(ACCENT_BLUE), 2))
            self.scene.addItem(ellipse)
            self._node_items[var] = ellipse

            name_lbl = QGraphicsTextItem(var)
            name_lbl.setDefaultTextColor(QColor(TEXT_PRIMARY))
            name_lbl.setFont(QFont("Courier New", 11, QFont.Bold))
            name_lbl.setPos(x - 7, y - 10)
            self.scene.addItem(name_lbl)

            val_lbl = QGraphicsTextItem("")
            val_lbl.setDefaultTextColor(QColor(ACCENT_CYAN))
            val_lbl.setFont(QFont("Courier New", 8))
            val_lbl.setPos(x - nr, y + nr + 2)
            self.scene.addItem(val_lbl)
            self._val_labels[var] = val_lbl

        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def show_result(self, success, assignment):
        for name, ellipse in self._node_items.items():
            if success and assignment.get(name):
                ellipse.setBrush(QBrush(QColor("#1a3a2a")))
                ellipse.setPen(QPen(QColor(ACCENT_OK), 2.5))
                self._val_labels[name].setPlainText(assignment[name][:3])
            else:
                ellipse.setBrush(QBrush(QColor("#3a1a1a")))
                ellipse.setPen(QPen(QColor(ACCENT_ERR), 2.5))

    def reset(self):
        for ellipse in self._node_items.values():
            ellipse.setBrush(QBrush(QColor(BG_PANEL)))
            ellipse.setPen(QPen(QColor(ACCENT_BLUE), 2))
        for lbl in self._val_labels.values():
            lbl.setPlainText("")


# ── Ventana principal ──────────────────────────────────────────────────────────

class CSPSolverWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSP Solver")
        self.setMinimumSize(950, 620)
        self.solver_thread = None
        self._apply_theme()
        self._build_ui()

    def _apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {BG_DARK};
                color: {TEXT_PRIMARY};
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                font-size: 13px;
            }}
            QGroupBox {{
                border: 1px solid {BORDER};
                border-radius: 8px;
                margin-top: 12px;
                padding: 8px;
                font-size: 11px;
                font-weight: bold;
                color: {TEXT_MUTED};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px;
            }}
            QLineEdit, QTextEdit {{
                background: {BG_PANEL};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 6px 10px;
                color: {TEXT_PRIMARY};
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {ACCENT_BLUE};
            }}
            QPushButton {{
                background: {BG_PANEL};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 8px 18px;
                color: {TEXT_PRIMARY};
                font-weight: 600;
            }}
            QPushButton:hover {{ background: {BORDER}; border-color: {ACCENT_BLUE}; }}
            QPushButton#run_btn {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #1e6fbf, stop:1 #0ba87e);
                border: none;
                color: white;
                font-size: 13px;
                font-weight: 700;
                padding: 10px 24px;
                border-radius: 8px;
            }}
            QPushButton#run_btn:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #2480d6, stop:1 #0dc490);
            }}
            QPushButton#run_btn:disabled {{ background: {BORDER}; color: {TEXT_MUTED}; }}
            QComboBox {{
                background: {BG_PANEL};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 6px 10px;
                color: {TEXT_PRIMARY};
            }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background: {BG_CARD};
                border: 1px solid {BORDER};
                color: {TEXT_PRIMARY};
                selection-background-color: {ACCENT_BLUE};
            }}
            QScrollBar:vertical {{
                background: {BG_DARK}; width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER}; border-radius: 4px; min-height: 20px;
            }}
        """)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ── Panel izquierdo ────────────────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(290)
        left.setStyleSheet(f"background: {BG_CARD}; border-radius: 10px;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(14, 14, 14, 14)
        ll.setSpacing(10)

        title = QLabel("CSP Solver")
        title.setFont(QFont("Courier New", 17, QFont.Bold))
        title.setStyleSheet(f"color: {ACCENT_CYAN}; background: transparent;")
        ll.addWidget(title)

        sub = QLabel("Satisfacción de Restricciones")
        sub.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent; font-size: 11px;")
        ll.addWidget(sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {BORDER};")
        ll.addWidget(sep)

        g_vars = QGroupBox("VARIABLES  (separadas por coma)")
        QVBoxLayout(g_vars).addWidget(self._field("A, B, C, D, E, F, G", "vars_input"))
        ll.addWidget(g_vars)

        g_dom = QGroupBox("DOMINIO  (separados por coma)")
        QVBoxLayout(g_dom).addWidget(self._field("Monday, Tuesday, Wednesday", "dom_input"))
        ll.addWidget(g_dom)

        g_con = QGroupBox("RESTRICCIONES  (X!=Y, una por línea)")
        self.con_input = QTextEdit()
        self.con_input.setFixedHeight(155)
        self.con_input.setPlainText(
            "A!=B\nA!=C\nB!=C\nB!=D\nB!=E\nC!=E\nC!=F\nD!=E\nE!=F\nE!=G\nF!=G"
        )
        QVBoxLayout(g_con).addWidget(self.con_input)
        ll.addWidget(g_con)

        g_alg = QGroupBox("ALGORITMO")
        self.alg_combo = QComboBox()
        self.alg_combo.addItems([
            "Backtracking simple",
            "Backtracking + AC-3 (First)",
            "Backtracking + AC-3 (MRV)",
            "Backtracking + AC-3 (Degree)",
            "Backtracking + AC-3 (MRV+Degree)",
        ])
        QVBoxLayout(g_alg).addWidget(self.alg_combo)
        ll.addWidget(g_alg)

        ll.addStretch()

        self.run_btn = QPushButton("▶  Ejecutar")
        self.run_btn.setObjectName("run_btn")
        self.run_btn.clicked.connect(self._run)
        ll.addWidget(self.run_btn)

        clear_btn = QPushButton("↺  Limpiar")
        clear_btn.clicked.connect(self._clear)
        ll.addWidget(clear_btn)

        root.addWidget(left)

        # ── Panel derecho ──────────────────────────────────────────────────
        right = QSplitter(Qt.Vertical)

        g_graph = QGroupBox("  GRAFO DE RESTRICCIONES")
        g_graph.setStyleSheet(f"QGroupBox {{ background: {BG_CARD}; border-radius: 10px; }}")
        self.graph = GraphWidget()
        self.graph.setMinimumHeight(320)
        QVBoxLayout(g_graph).addWidget(self.graph)
        right.addWidget(g_graph)

        g_res = QGroupBox("  RESULTADO")
        g_res.setStyleSheet(f"QGroupBox {{ background: {BG_CARD}; border-radius: 10px; }}")
        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)
        self.result_view.setFont(QFont("Courier New", 13))
        self.result_view.setStyleSheet(
            f"background: {BG_DARK}; border: 1px solid {BORDER}; "
            f"border-radius: 6px; color: {TEXT_PRIMARY}; padding: 10px;"
        )
        QVBoxLayout(g_res).addWidget(self.result_view)
        right.addWidget(g_res)

        right.setSizes([420, 200])
        root.addWidget(right, stretch=1)

    def _field(self, default, attr):
        w = QLineEdit(default)
        setattr(self, attr, w)
        return w

    # ── Helpers ────────────────────────────────────────────────────────────

    def _parse(self):
        variables   = [v.strip() for v in self.vars_input.text().split(",") if v.strip()]
        domain      = [d.strip() for d in self.dom_input.text().split(",") if d.strip()]
        constraints = [
            l.strip() for l in self.con_input.toPlainText().splitlines()
            if l.strip() and "!=" in l
        ]
        return variables, domain, constraints

    def _alg_key(self):
        return {
            "Backtracking simple":                "backtracking",
            "Backtracking + AC-3 (First)":        "backtracking_inference_first",
            "Backtracking + AC-3 (MRV)":          "backtracking_inference_mrv",
            "Backtracking + AC-3 (Degree)":       "backtracking_inference_degree",
            "Backtracking + AC-3 (MRV+Degree)":   "backtracking_inference_mrv_degree",
        }[self.alg_combo.currentText()]

    def _log(self, msg, color=None):
        c = color or TEXT_PRIMARY
        self.result_view.append(f'<span style="color:{c};">{msg}</span>')
        self.result_view.moveCursor(QTextCursor.End)

    # ── Slots ──────────────────────────────────────────────────────────────

    def _run(self):
        variables, domain, constraints = self._parse()
        if not variables or not domain:
            QMessageBox.warning(self, "Faltan datos", "Ingresa variables y dominio.")
            return

        self._clear()
        self.graph.build(variables, constraints)
        self.run_btn.setEnabled(False)
        self._log(f"Ejecutando {self.alg_combo.currentText()}…", TEXT_MUTED)

        self.solver_thread = SolverThread(variables, domain, constraints, self._alg_key())
        self.solver_thread.done_signal.connect(self._on_done)
        self.solver_thread.start()

    def _on_done(self, success, final):
        self.run_btn.setEnabled(True)
        self.graph.show_result(success, final)

        if success:
            self._log("✅  SOLUCIÓN ENCONTRADA", ACCENT_OK)
            self._log("")
            for name, val in final.items():
                self._log(f"   {name}  →  {val}", ACCENT_CYAN)
        else:
            self._log("❌  Sin solución para este CSP.", ACCENT_ERR)

    def _clear(self):
        self.result_view.clear()
        self.graph.reset()


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CSP Solver")
    win = CSPSolverWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()