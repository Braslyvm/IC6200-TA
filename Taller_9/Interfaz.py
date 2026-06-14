import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy
)

from PyQt5.QtGui import QPixmap, QFont, QColor, QPainter, QPainterPath, QLinearGradient, QBrush, QPalette
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QSize

from Red_Neuronal import preparar_modelo, predecir_senal



COLOR_BG        = "#0D1117"   
COLOR_PANEL     = "#161B22"  
COLOR_BORDER    = "#30363D"   
COLOR_ACCENT    = "#E63946"   
COLOR_ACCENT2   = "#FFB703"   
COLOR_TEXT      = "#E6EDF3"  
COLOR_MUTED     = "#8B949E"   
COLOR_SUCCESS   = "#3FB950"  
COLOR_BTN_BG    = "#21262D"   




class PuntosCarga(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(20)
        self._paso = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(300)

    def _tick(self):
        self._paso = (self._paso + 1) % 4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        cx = w // 2
        r = 6
        gap = 18
        for i in range(3):
            x = cx + (i - 1) * gap
            alpha = 255 if i < self._paso else 60
            color = QColor(COLOR_ACCENT)
            color.setAlpha(alpha)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x - r // 2, 4, r, r)

    def detener(self):
        self._timer.stop()


class HiloPrepararModelo(QThread):
    terminado = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            preparar_modelo()
            self.terminado.emit()
        except Exception as e:
            self.error.emit(str(e))



class PantallaCarga(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cargando")
        self.setFixedSize(420, 260)
        self.setStyleSheet(f"background-color: {COLOR_BG};")

        # Ícono de señal estilizado
        icono = QLabel("🚦")
        icono.setAlignment(Qt.AlignCenter)
        icono.setFont(QFont("Segoe UI Emoji", 36))

        self.label_titulo = QLabel("Preparando red neuronal")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.label_titulo.setStyleSheet(f"color: {COLOR_TEXT};")

        self.label_sub = QLabel("Esto puede tomar unos segundos la primera vez")
        self.label_sub.setAlignment(Qt.AlignCenter)
        self.label_sub.setWordWrap(True)
        self.label_sub.setFont(QFont("Segoe UI", 10))
        self.label_sub.setStyleSheet(f"color: {COLOR_MUTED};")

        self.puntos = PuntosCarga()

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(14)
        layout.addWidget(icono)
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.label_sub)
        layout.addWidget(self.puntos)
        self.setLayout(layout)

        self.hilo = HiloPrepararModelo()
        self.hilo.terminado.connect(self.abrir_ventana_principal)
        self.hilo.error.connect(self.mostrar_error)
        self.hilo.start()

    def abrir_ventana_principal(self):
        self.puntos.detener()
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.show()
        self.close()

    def mostrar_error(self, mensaje):
        self.puntos.detener()
        self.label_titulo.setText("Error al cargar el modelo")
        self.label_titulo.setStyleSheet(f"color: {COLOR_ACCENT};")
        self.label_sub.setText(mensaje)


# ==============================
# Tarjeta de imagen con drop zone
# ==============================

class TarjetaImagen(QLabel):
    imagen_soltada = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(370, 310)
        self._vacia = True
        self._actualizar_estilo()

    def _actualizar_estilo(self):
        if self._vacia:
            self.setText("Arrastrá una imagen\no usá el botón")
            self.setFont(QFont("Segoe UI", 11))
            self.setStyleSheet(f"""
                QLabel {{
                    border: 2px dashed {COLOR_BORDER};
                    border-radius: 12px;
                    background-color: {COLOR_PANEL};
                    color: {COLOR_MUTED};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QLabel {{
                    border: 2px solid {COLOR_ACCENT};
                    border-radius: 12px;
                    background-color: {COLOR_PANEL};
                }}
            """)

    def cargar_imagen(self, ruta):
        pixmap = QPixmap(ruta)
        pixmap = pixmap.scaled(366, 306, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self._vacia = False
        self._actualizar_estilo()

    def limpiar(self):
        self.clear()
        self._vacia = True
        self._actualizar_estilo()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                QLabel {{
                    border: 2px dashed {COLOR_ACCENT};
                    border-radius: 12px;
                    background-color: #1C1F26;
                    color: {COLOR_ACCENT};
                }}
            """)

    def dragLeaveEvent(self, event):
        self._actualizar_estilo()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            ruta = urls[0].toLocalFile()
            if ruta.lower().endswith(('.png', '.jpg', '.jpeg', '.ppm')):
                self.cargar_imagen(ruta)
                self.imagen_soltada.emit(ruta)


# ==============================
# Panel de resultado
# ==============================

class PanelResultado(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(370, 310)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_PANEL};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
            }}
        """)

        self.label_estado = QLabel("En espera")
        self.label_estado.setAlignment(Qt.AlignCenter)
        self.label_estado.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.label_estado.setStyleSheet(f"""
            color: {COLOR_MUTED};
            background: transparent;
            border: none;
            letter-spacing: 2px;
        """)

        self.label_clase = QLabel("—")
        self.label_clase.setAlignment(Qt.AlignCenter)
        self.label_clase.setWordWrap(True)
        self.label_clase.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label_clase.setStyleSheet(f"""
            color: {COLOR_TEXT};
            background: transparent;
            border: none;
        """)

        # Barra de confianza
        self.label_conf_titulo = QLabel("CONFIANZA")
        self.label_conf_titulo.setAlignment(Qt.AlignCenter)
        self.label_conf_titulo.setFont(QFont("Segoe UI", 8))
        self.label_conf_titulo.setStyleSheet(f"color: {COLOR_MUTED}; background: transparent; border: none; letter-spacing: 2px;")

        self.label_conf_valor = QLabel("")
        self.label_conf_valor.setAlignment(Qt.AlignCenter)
        self.label_conf_valor.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.label_conf_valor.setStyleSheet(f"color: {COLOR_ACCENT}; background: transparent; border: none;")

        self.barra_fondo = QFrame()
        self.barra_fondo.setFixedSize(280, 8)
        self.barra_fondo.setStyleSheet(f"""
            background-color: {COLOR_BORDER};
            border-radius: 4px;
            border: none;
        """)

        self.barra_relleno = QFrame(self.barra_fondo)
        self.barra_relleno.setFixedHeight(8)
        self.barra_relleno.setFixedWidth(0)
        self.barra_relleno.setStyleSheet(f"""
            background-color: {COLOR_ACCENT};
            border-radius: 4px;
            border: none;
        """)

        barra_wrapper = QHBoxLayout()
        barra_wrapper.addStretch()
        barra_wrapper.addWidget(self.barra_fondo)
        barra_wrapper.addStretch()

        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet(f"color: {COLOR_BORDER}; background: transparent; border: none; border-top: 1px solid {COLOR_BORDER};")
        separador.setFixedHeight(1)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        layout.addStretch()
        layout.addWidget(self.label_estado)
        layout.addWidget(self.label_clase)
        layout.addWidget(separador)
        layout.addWidget(self.label_conf_titulo)
        layout.addWidget(self.label_conf_valor)
        layout.addLayout(barra_wrapper)
        layout.addStretch()
        self.setLayout(layout)

    def resetear(self):
        self.label_estado.setText("EN ESPERA")
        self.label_clase.setText("—")
        self.label_clase.setStyleSheet(f"color: {COLOR_TEXT}; background: transparent; border: none;")
        self.label_conf_valor.setText("")
        self.barra_relleno.setFixedWidth(0)

    def analizando(self):
        self.label_estado.setText("ANALIZANDO")
        self.label_clase.setText("...")
        self.label_conf_valor.setText("")
        self.barra_relleno.setFixedWidth(0)

    def mostrar_resultado(self, clase, confianza):
        self.label_estado.setText("RESULTADO")
        self.label_clase.setText(clase)

        # Color según confianza
        if confianza >= 80:
            color_conf = COLOR_SUCCESS
        elif confianza >= 50:
            color_conf = COLOR_ACCENT2
        else:
            color_conf = COLOR_ACCENT

        self.label_conf_valor.setText(f"{confianza:.1f}%")
        self.label_conf_valor.setStyleSheet(f"color: {color_conf}; background: transparent; border: none;")

        ancho = int(280 * confianza / 100)
        self.barra_relleno.setFixedWidth(ancho)
        self.barra_relleno.setStyleSheet(f"""
            background-color: {color_conf};
            border-radius: 4px;
            border: none;
        """)



def hacer_boton(texto, primario=False):
    btn = QPushButton(texto)
    btn.setFont(QFont("Segoe UI", 11))
    btn.setFixedHeight(44)
    btn.setCursor(Qt.PointingHandCursor)

    if primario:
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #FF4D5A;
            }}
            QPushButton:pressed {{
                background-color: #C1121F;
            }}
            QPushButton:disabled {{
                background-color: {COLOR_BORDER};
                color: {COLOR_MUTED};
            }}
        """)
    else:
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BTN_BG};
                color: {COLOR_TEXT};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #2D333B;
                border-color: {COLOR_MUTED};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_BG};
            }}
        """)
    return btn



class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reconocimiento de Señales de Tránsito")
        self.setFixedSize(860, 580)
        self.setStyleSheet(f"background-color: {COLOR_BG};")

        self.ruta_imagen = None

        self._construir_ui()

    def _construir_ui(self):
        # ---- Header ----
        badge = QLabel("CNN · GTSRB · 43 clases")
        badge.setFont(QFont("Segoe UI", 8))
        badge.setStyleSheet(f"""
            color: {COLOR_MUTED};
            background-color: {COLOR_BTN_BG};
            border: 1px solid {COLOR_BORDER};
            border-radius: 10px;
            padding: 2px 10px;
        """)
        badge.setFixedHeight(22)

        titulo = QLabel("Reconocimiento de Señales")
        titulo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        titulo.setStyleSheet(f"color: {COLOR_TEXT};")

        subtitulo = QLabel("Cargá una imagen de una señal de tránsito para identificarla")
        subtitulo.setFont(QFont("Segoe UI", 10))
        subtitulo.setStyleSheet(f"color: {COLOR_MUTED};")

        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        header_layout.addWidget(badge)
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)

        # ---- Contenido central ----
        self.tarjeta_img = TarjetaImagen()
        self.tarjeta_img.imagen_soltada.connect(self._imagen_desde_drop)

        self.panel_resultado = PanelResultado()

        contenido = QHBoxLayout()
        contenido.setSpacing(20)
        contenido.addWidget(self.tarjeta_img)
        contenido.addWidget(self.panel_resultado)

        # ---- Botones ----
        self.btn_agregar = hacer_boton("📂  Abrir imagen")
        self.btn_agregar.clicked.connect(self._abrir_imagen)

        self.btn_predecir = hacer_boton("Identificar señal", primario=True)
        self.btn_predecir.setEnabled(False)
        self.btn_predecir.clicked.connect(self._predecir)

        self.btn_limpiar = hacer_boton("Limpiar")
        self.btn_limpiar.setEnabled(False)
        self.btn_limpiar.clicked.connect(self._limpiar)

        fila_botones = QHBoxLayout()
        fila_botones.setSpacing(10)
        fila_botones.addWidget(self.btn_agregar)
        fila_botones.addWidget(self.btn_predecir)
        fila_botones.addWidget(self.btn_limpiar)

        # ---- Layout principal ----
        main = QVBoxLayout()
        main.setContentsMargins(30, 24, 30, 24)
        main.setSpacing(20)
        main.addLayout(header_layout)
        main.addLayout(contenido)
        main.addLayout(fila_botones)

        self.setLayout(main)

    def _abrir_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.ppm)"
        )
        if ruta:
            self._cargar_imagen(ruta)

    def _imagen_desde_drop(self, ruta):
        self._cargar_imagen(ruta)

    def _cargar_imagen(self, ruta):
        self.ruta_imagen = ruta
        self.tarjeta_img.cargar_imagen(ruta)
        self.panel_resultado.resetear()
        self.btn_predecir.setEnabled(True)
        self.btn_limpiar.setEnabled(True)

    def _predecir(self):
        if not self.ruta_imagen:
            return

        self.panel_resultado.analizando()
        self.btn_predecir.setEnabled(False)

        # Procesamos en el hilo de UI (modelo ya está cargado)
        QTimer.singleShot(50, self._ejecutar_prediccion)

    def _ejecutar_prediccion(self):
        resultado, confianza = predecir_senal(self.ruta_imagen)
        self.panel_resultado.mostrar_resultado(resultado, confianza)
        self.btn_predecir.setEnabled(True)

    def _limpiar(self):
        self.ruta_imagen = None
        self.tarjeta_img.limpiar()
        self.panel_resultado.resetear()
        self.btn_predecir.setEnabled(False)
        self.btn_limpiar.setEnabled(False)


# ==============================
# Ejecutar
# ==============================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    pantalla = PantallaCarga()
    pantalla.show()

    sys.exit(app.exec_())