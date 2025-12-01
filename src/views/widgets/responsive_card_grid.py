"""
Responsive Card Grid - Grid layout responsive para cards

Sistema de grid que ajusta automáticamente el número de columnas
según el ancho disponible de la ventana:
- < 600px: 1 columna
- 600-900px: 2 columnas
- 900-1200px: 3 columnas
- >= 1200px: 4 columnas
"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
import logging

logger = logging.getLogger(__name__)


class ResponsiveCardGrid(QWidget):
    """Grid responsive que ajusta columnas según ancho de ventana"""

    # Señal cuando cambia el número de columnas
    columns_changed = pyqtSignal(int)

    # Breakpoints para responsive
    BREAKPOINTS = {
        'xs': 600,   # Extra small: 1 columna
        'sm': 900,   # Small: 2 columnas
        'md': 1200,  # Medium: 3 columnas
        'lg': 9999   # Large: 4 columnas
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cards = []  # Lista de cards agregadas
        self.current_columns = 0

        self.init_ui()

        # Timer para debounce del resize
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._recalculate_layout)

    def init_ui(self):
        """Inicializa la interfaz"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll area para el grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00ff88;
            }
        """)

        # Contenedor del grid
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(20)  # Espacio entre cards
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(self.grid_container)
        main_layout.addWidget(scroll_area)

    def add_card(self, card_widget: QWidget):
        """Agrega una card al grid"""
        self.cards.append(card_widget)

        # Si es la primera card, inicializar columnas
        if self.current_columns == 0:
            self.current_columns = self._calculate_columns(self.width())
            if self.current_columns == 0:
                self.current_columns = 3  # Default a 3 columnas

        # Agregar card al layout inmediatamente
        index = len(self.cards) - 1
        row = index // self.current_columns
        col = index % self.current_columns
        self.grid_layout.addWidget(card_widget, row, col)

    def clear_cards(self):
        """Limpia todas las cards del grid"""
        # Eliminar todos los widgets del layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.cards.clear()
        # No resetear current_columns para mantener el layout actual

    def _calculate_columns(self, width: int) -> int:
        """Calcula el número de columnas según el ancho"""
        if width < self.BREAKPOINTS['xs']:
            return 1
        elif width < self.BREAKPOINTS['sm']:
            return 2
        elif width < self.BREAKPOINTS['md']:
            return 3
        else:
            return 4

    def _recalculate_layout(self):
        """Recalcula el layout del grid según el ancho actual"""
        width = self.width()
        columns = self._calculate_columns(width)

        # Solo reorganizar si cambió el número de columnas
        if columns != self.current_columns:
            logger.info(f"Grid columns changed: {self.current_columns} -> {columns}")
            self.current_columns = columns
            self.columns_changed.emit(columns)
            self._relayout_cards()

    def _relayout_cards(self):
        """Reorganiza las cards en el grid según el número de columnas"""
        # Limpiar layout sin eliminar widgets
        while self.grid_layout.count():
            self.grid_layout.takeAt(0)

        # Colocar cards en grid
        for index, card in enumerate(self.cards):
            row = index // self.current_columns
            col = index % self.current_columns
            self.grid_layout.addWidget(card, row, col)

        logger.info(f"Relayout completed: {len(self.cards)} cards in {self.current_columns} columns")

    def resizeEvent(self, event):
        """Al redimensionar el widget, recalcular layout con debounce"""
        super().resizeEvent(event)

        # Reiniciar timer para debounce (evitar recalcular múltiples veces)
        self.resize_timer.stop()
        self.resize_timer.start(150)  # 150ms debounce

    def get_card_count(self) -> int:
        """Retorna el número total de cards"""
        return len(self.cards)

    def get_current_columns(self) -> int:
        """Retorna el número actual de columnas"""
        return self.current_columns
