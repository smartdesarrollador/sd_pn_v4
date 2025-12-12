"""
Widget para items de tipo PATH

Muestra items de ruta de archivo/carpeta clickeable.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from .base_item_widget import BaseItemWidget
from ...styles.full_view_styles import FullViewStyles
import subprocess
import os


class PathItemWidget(BaseItemWidget):
    """
    Widget para items de tipo PATH

    Características:
    - Muestra ruta de archivo/carpeta en naranja
    - Click en path abre en explorador de archivos
    - Icono 📁 para carpetas, 📄 para archivos
    - Botón de copiar para copiar path al portapapeles
    """

    def __init__(self, item_data: dict, parent=None):
        """
        Inicializar widget de item de path

        Args:
            item_data: Diccionario con datos del item
            parent: Widget padre
        """
        super().__init__(item_data, parent)
        self.apply_styles()

    def render_content(self):
        """Renderizar contenido de PATH"""
        # Layout horizontal para icono + título
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        # Determinar icono según tipo de path
        path_content = self.get_item_content()
        icon = "📁" if os.path.isdir(path_content) else "📄"

        icon_label = QLabel(icon)
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

        # Path clickeable
        if path_content:
            path_label = QLabel(path_content)
            path_label.setObjectName("path_text")
            path_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            path_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            path_label.setWordWrap(True)
            path_label.mousePressEvent = lambda event: self.open_path(path_content)
            path_label.setToolTip("Click para abrir en explorador")
            self.content_layout.addWidget(path_label)

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

    def open_path(self, path: str):
        """
        Abrir path en explorador de archivos

        Args:
            path: Ruta a abrir
        """
        try:
            if os.path.exists(path):
                # Windows: abrir en explorador con selección
                subprocess.Popen(f'explorer /select,"{path}"')
                print(f"✓ Path abierto: {path}")
            else:
                print(f"✗ Path no existe: {path}")
        except Exception as e:
            print(f"✗ Error al abrir path: {e}")

    def apply_styles(self):
        """Aplicar estilos CSS"""
        self.setStyleSheet(FullViewStyles.get_path_item_style())
