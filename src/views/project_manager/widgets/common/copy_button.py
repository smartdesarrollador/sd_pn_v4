"""
Botón de copiar con feedback visual

Botón que copia contenido al portapapeles y muestra feedback
visual al usuario.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from ...styles.full_view_styles import FullViewStyles
from ...styles.color_palette import FullViewColorPalette


class CopyButton(QPushButton):
    """
    Botón de copiar con feedback visual

    Muestra un icono de copiar que cambia a check cuando
    se hace click, con feedback visual temporal.

    Señales:
        copy_clicked: Emitida cuando se hace click en el botón
    """

    # Señal
    copy_clicked = pyqtSignal()

    def __init__(self, parent=None):
        """
        Inicializar botón de copiar

        Args:
            parent: Widget padre
        """
        super().__init__(parent)

        self.original_text = "📋"
        self.copied_text = "✓"
        self.feedback_duration = 1000  # ms

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Inicializar interfaz de usuario"""
        self.setText(self.original_text)
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Copiar al portapapeles")

        # Conectar señal de click
        self.clicked.connect(self.on_clicked)

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_copy_button_style())

    def on_clicked(self):
        """Manejar evento de click"""
        self.show_feedback()
        self.copy_clicked.emit()

    def show_feedback(self):
        """
        Mostrar feedback visual de copiado

        Cambia el icono a check y el color a verde,
        luego restaura el estado original después de 1 segundo.
        """
        # Cambiar a estado "copiado"
        self.setText(self.copied_text)
        self.setToolTip("¡Copiado!")

        # Aplicar estilo de éxito
        self.setStyleSheet(f"""
            CopyButton {{
                background-color: {FullViewColorPalette.SUCCESS};
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
        """)

        # Restaurar después de feedback_duration
        QTimer.singleShot(self.feedback_duration, self.reset_state)

    def reset_state(self):
        """Restaurar estado original del botón"""
        self.setText(self.original_text)
        self.setToolTip("Copiar al portapapeles")
        self.apply_styles()

    def set_feedback_duration(self, duration_ms: int):
        """
        Establecer duración del feedback visual

        Args:
            duration_ms: Duración en milisegundos
        """
        self.feedback_duration = duration_ms
