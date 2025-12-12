"""
Panel de vista completa para gestor de proyectos

Este panel muestra todos los items de un proyecto en una vista de lectura
completa de una sola columna, organizado jerárquicamente por tags de proyecto,
listas, categorías y tags de items.

IMPORTANTE: Este es un panel interno de ProjectManagerWindow, NO una ventana separada.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from .styles.full_view_styles import FullViewStyles
from .widgets.headers import ProjectHeaderWidget, ProjectTagHeaderWidget
from .widgets.item_group_widget import ItemGroupWidget
from .project_data_manager import ProjectDataManager


class ProjectFullViewPanel(QWidget):
    """
    Panel de vista completa de proyecto

    Este widget se integra dentro de ProjectManagerWindow usando QStackedWidget
    para alternar entre vista normal y vista completa.

    Características:
    - Vista de una columna con scroll vertical
    - Jerarquía de 4 niveles: Proyecto → Tags → Grupos → Items
    - Solo modo oscuro con alto contraste
    - Contenido extenso (>800 chars) se muestra con scroll
    - Sincronizado con filtros de tags de proyecto
    """

    # Señales
    item_copied = pyqtSignal(dict)  # Emite cuando se copia un item
    item_clicked = pyqtSignal(dict)  # Emite cuando se hace click en item

    def __init__(self, db_manager=None, parent=None):
        """
        Inicializar panel de vista completa

        Args:
            db_manager: Instancia de DBManager (opcional, usa mock si no se provee)
            parent: Widget padre (típicamente ProjectManagerWindow)
        """
        super().__init__(parent)

        # Data manager
        self.data_manager = ProjectDataManager(db_manager)

        # Estado interno
        self.project_data = None
        self.current_filters = []
        self.current_project_id = None

        # Inicializar UI
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Inicializar interfaz de usuario"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Content Widget (contenedor del scroll)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Establecer content widget en scroll area
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)

        # Mostrar mensaje inicial
        self.show_empty_state()

    def apply_styles(self):
        """Aplicar estilos CSS al panel"""
        self.setStyleSheet(FullViewStyles.get_main_panel_style())

    def show_empty_state(self):
        """Mostrar estado vacío cuando no hay proyecto seleccionado"""
        self.clear_view()

        empty_label = QLabel("Selecciona un proyecto para ver su contenido")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet(f"""
            color: #808080;
            font-size: 14px;
            padding: 50px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.content_layout.addWidget(empty_label)

    def load_project(self, project_id: int):
        """
        Cargar proyecto en la vista

        Args:
            project_id: ID del proyecto a cargar
        """
        self.current_project_id = project_id

        # Obtener datos del proyecto
        self.project_data = self.data_manager.get_project_full_data(project_id)

        if not self.project_data:
            self.show_empty_state()
            return

        # Renderizar vista
        self.render_view()

    def render_view(self):
        """Renderizar vista completa con todos los componentes"""
        if not self.project_data:
            return

        self.clear_view()

        # Header del proyecto
        project_header = ProjectHeaderWidget()
        project_header.set_project_info(
            self.project_data['project_name'],
            self.project_data['project_icon']
        )
        self.content_layout.addWidget(project_header)

        # Secciones por tag de proyecto
        for tag_data in self.project_data['tags']:
            self._render_tag_section(tag_data)

        # Items sin tag de proyecto
        if self.project_data['ungrouped_items']:
            self._render_ungrouped_section(
                self.project_data['ungrouped_items']
            )

        # Spacer al final
        self.content_layout.addStretch()

    def _render_tag_section(self, tag_data: dict):
        """
        Renderizar sección de tag de proyecto

        Args:
            tag_data: Datos del tag de proyecto
        """
        # Contar items totales en este tag
        total_items = sum(
            len(group['items'])
            for group in tag_data['groups']
        )

        # Header del tag
        tag_header = ProjectTagHeaderWidget()
        tag_header.set_tag_info(
            tag_data['tag_name'],
            tag_data['tag_color'],
            total_items
        )
        self.content_layout.addWidget(tag_header)

        # Container para grupos (para poder colapsar)
        tag_container = QWidget()
        tag_container_layout = QVBoxLayout(tag_container)
        tag_container_layout.setContentsMargins(0, 0, 0, 0)
        tag_container_layout.setSpacing(8)

        # Grupos de items
        for group in tag_data['groups']:
            group_widget = ItemGroupWidget(
                group['name'],
                group['type']
            )

            # Agregar items al grupo
            for item_data in group['items']:
                group_widget.add_item(item_data)

            tag_container_layout.addWidget(group_widget)

        self.content_layout.addWidget(tag_container)

        # Conectar colapso/expansión
        tag_header.toggle_collapsed.connect(
            lambda collapsed: tag_container.setVisible(not collapsed)
        )

    def _render_ungrouped_section(self, items: list):
        """
        Renderizar sección de items sin tag de proyecto

        Args:
            items: Lista de items sin tag de proyecto
        """
        # Header
        tag_header = ProjectTagHeaderWidget()
        tag_header.set_tag_info("Otros Items", "#808080", len(items))
        self.content_layout.addWidget(tag_header)

        # Grupo de items
        group_widget = ItemGroupWidget("Sin clasificar", "other")
        for item_data in items:
            group_widget.add_item(item_data)

        self.content_layout.addWidget(group_widget)

    def apply_filters(self, tag_filters: list[str], match_mode: str = 'OR'):
        """
        Aplicar filtros de tags al proyecto actual

        Args:
            tag_filters: Lista de nombres de tags para filtrar
            match_mode: 'AND' o 'OR' para coincidencia de tags
        """
        self.current_filters = tag_filters

        if not self.project_data:
            return

        # Si no hay filtros, mostrar todo
        if not tag_filters:
            self.render_view()
            return

        # Filtrar datos del proyecto
        filtered_data = self.data_manager.filter_by_project_tags(
            self.project_data,
            tag_filters,
            match_mode
        )

        # Guardar datos originales temporalmente
        original_data = self.project_data

        # Renderizar con datos filtrados
        self.project_data = filtered_data
        self.render_view()

        # Restaurar datos originales
        self.project_data = original_data

        # Log de filtrado
        visible_tags = [tag['tag_name'] for tag in filtered_data['tags']]
        print(f"✓ Filtros aplicados ({match_mode}): {tag_filters}")
        print(f"  Tags visibles: {visible_tags}")

    def clear_filters(self):
        """
        Limpiar todos los filtros activos

        Restaura la vista completa sin filtros.
        """
        self.current_filters = []
        if self.project_data:
            self.render_view()
            print("✓ Filtros limpiados - Mostrando todos los tags")

    def refresh_view(self):
        """
        Refrescar vista completa

        Re-carga el proyecto actual desde la base de datos
        y actualiza la visualización.
        """
        if self.current_project_id:
            self.load_project(self.current_project_id)

    def clear_view(self):
        """
        Limpiar todo el contenido de la vista

        Elimina todos los widgets del layout de contenido.
        """
        # Eliminar todos los widgets del layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_current_project_id(self) -> int:
        """
        Obtener ID del proyecto actualmente cargado

        Returns:
            ID del proyecto o None si no hay proyecto cargado
        """
        return self.current_project_id

    def has_active_filters(self) -> bool:
        """
        Verificar si hay filtros activos

        Returns:
            True si hay filtros aplicados, False en caso contrario
        """
        return len(self.current_filters) > 0


# Test del panel (para desarrollo)
if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Crear panel
    panel = ProjectFullViewPanel()
    panel.setWindowTitle("Vista Completa de Proyecto - Test")
    panel.setMinimumSize(800, 600)
    panel.show()

    sys.exit(app.exec())
