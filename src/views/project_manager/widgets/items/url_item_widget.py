"""
Widget para items de tipo URL

Muestra items de URL con formato de enlace clickeable.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from .base_item_widget import BaseItemWidget
from ...styles.full_view_styles import FullViewStyles
import webbrowser


class URLItemWidget(BaseItemWidget):
    """
    Widget para items de tipo URL

    Características:
    - Muestra URL como enlace azul claro
    - Click en URL abre en navegador predeterminado
    - Icono 🔗 para identificación visual
    - Botón de copiar para copiar URL al portapapeles
    """

    def __init__(self, item_data: dict, parent=None):
        """
        Inicializar widget de item de URL

        Args:
            item_data: Diccionario con datos del item
            parent: Widget padre
        """
        super().__init__(item_data, parent)
        self.apply_styles()

    def render_content(self):
        """Renderizar contenido de URL"""
        # Layout horizontal para icono + título
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        # Icono de enlace
        icon_label = QLabel("🔗")
        icon_label.setStyleSheet("font-size: 16px;")
        title_layout.addWidget(icon_label)

        # Título
        label = self.get_item_label()
        if label and label != 'Sin título':
            title_label = QLabel(label)
            title_label.setStyleSheet("""
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            title_layout.addWidget(title_label)

        title_layout.addStretch()
        self.content_layout.addLayout(title_layout)

        # URL clickeable
        content = self.get_item_content()
        if content:
            url_label = QLabel(content)
            url_label.setObjectName("url_text")
            url_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            url_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            url_label.setWordWrap(True)
            url_label.mousePressEvent = lambda event: self.open_url(content)
            url_label.setToolTip("Click para abrir en navegador")
            self.content_layout.addWidget(url_label)

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

    def open_url(self, url: str):
        """
        Abrir URL en navegador predeterminado

        Args:
            url: URL a abrir
        """
        try:
            webbrowser.open(url)
            print(f"✓ URL abierta: {url}")
        except Exception as e:
            print(f"✗ Error al abrir URL: {e}")

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_url_item_style())
