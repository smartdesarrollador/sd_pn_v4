"""
Widget para items de tipo TEXT

Muestra items de texto con formato de párrafo.
Para contenido extenso (>800 chars) usa QTextEdit con scroll.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import QLabel, QTextEdit
from PyQt6.QtCore import Qt
from .base_item_widget import BaseItemWidget
from ...styles.full_view_styles import FullViewStyles


class TextItemWidget(BaseItemWidget):
    """
    Widget para items de tipo TEXT

    Características:
    - Muestra texto en formato de párrafo
    - Para contenido corto (<800 chars): QLabel con word-wrap
    - Para contenido extenso (≥800 chars): QTextEdit con scroll vertical
    - Altura máxima con scroll: 200px
    """

    MAX_CONTENT_LENGTH = 800  # Límite para mostrar contenido sin scroll

    def __init__(self, item_data: dict, parent=None):
        """
        Inicializar widget de item de texto

        Args:
            item_data: Diccionario con datos del item
            parent: Widget padre
        """
        super().__init__(item_data, parent)
        self.apply_styles()

    def render_content(self):
        """Renderizar contenido de texto"""
        # Título (si existe)
        label = self.get_item_label()
        if label and label != 'Sin título':
            title_label = QLabel(f"• {label}")
            title_label.setStyleSheet("""
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                padding-bottom: 4px;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            self.content_layout.addWidget(title_label)

        # Contenido
        content = self.get_item_content()
        if content:
            # Si el contenido es extenso (>800 chars), usar QTextEdit con scroll
            if len(content) > self.MAX_CONTENT_LENGTH:
                content_text = QTextEdit()
                content_text.setObjectName("text_content")
                content_text.setPlainText(content)
                content_text.setReadOnly(True)
                content_text.setMaximumHeight(200)  # Altura máxima con scroll
                content_text.setVerticalScrollBarPolicy(
                    Qt.ScrollBarPolicy.ScrollBarAsNeeded
                )
                content_text.setHorizontalScrollBarPolicy(
                    Qt.ScrollBarPolicy.ScrollBarAlwaysOff
                )
                content_text.setStyleSheet("""
                    QTextEdit {
                        background-color: transparent;
                        border: none;
                        color: #E0E0E0;
                        font-size: 13px;
                        line-height: 1.6;
                        font-family: 'Segoe UI', Arial, sans-serif;
                    }
                    QScrollBar:vertical {
                        background-color: #2A2A2A;
                        width: 8px;
                        border-radius: 4px;
                    }
                    QScrollBar::handle:vertical {
                        background-color: #505050;
                        border-radius: 4px;
                        min-height: 20px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background-color: #606060;
                    }
                    QScrollBar::add-line:vertical,
                    QScrollBar::sub-line:vertical {
                        border: none;
                        background: none;
                    }
                """)
                self.content_layout.addWidget(content_text)
            else:
                # Contenido normal sin scroll
                content_label = QLabel(content)
                content_label.setObjectName("text_content")
                content_label.setWordWrap(True)
                content_label.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextSelectableByMouse
                )
                self.content_layout.addWidget(content_label)

        # Descripción (si existe)
        description = self.get_item_description()
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                color: #808080;
                font-size: 12px;
                font-style: italic;
                padding-top: 4px;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            desc_label.setWordWrap(True)
            self.content_layout.addWidget(desc_label)

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_text_item_style())
