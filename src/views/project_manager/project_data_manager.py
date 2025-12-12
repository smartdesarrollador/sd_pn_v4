"""
Gestor de datos para vista completa de proyecto

Obtiene y agrupa datos de proyectos desde la base de datos
para visualización en vista completa.

Autor: Widget Sidebar Team
Versión: 1.0
"""

from typing import Dict, List, Optional


class ProjectDataManager:
    """
    Gestor de datos para vista completa de proyecto

    Se encarga de:
    - Obtener datos del proyecto desde BD
    - Agrupar items por tags de proyecto
    - Agrupar items por categorías, listas y tags de items
    - Filtrar datos según criterios

    NOTA: Por ahora usa datos mock para testing.
    En futuras fases se integrará con DBManager real.
    """

    def __init__(self, db_manager=None):
        """
        Inicializar gestor de datos

        Args:
            db_manager: Instancia de DBManager (opcional por ahora)
        """
        self.db = db_manager

    def get_project_full_data(self, project_id: int) -> Optional[Dict]:
        """
        Obtener datos completos del proyecto agrupados por tags

        Args:
            project_id: ID del proyecto

        Returns:
            Diccionario con estructura:
            {
                'project_id': int,
                'project_name': str,
                'project_icon': str,
                'tags': [
                    {
                        'tag_name': str,
                        'tag_color': str,
                        'groups': [
                            {
                                'type': 'category' | 'list' | 'tag',
                                'name': str,
                                'items': [...]
                            }
                        ]
                    }
                ],
                'ungrouped_items': [...]
            }

        NOTA: Por ahora retorna datos mock para testing.
        """
        # TODO: En Fase 5, integrar con BD real
        # Por ahora, datos mock para testing
        return self._get_mock_project_data(project_id)

    def _get_mock_project_data(self, project_id: int) -> Dict:
        """
        Obtener datos mock para testing

        Args:
            project_id: ID del proyecto

        Returns:
            Datos mock del proyecto
        """
        return {
            'project_id': project_id,
            'project_name': 'proy_test_3',
            'project_icon': '📁',
            'tags': [
                {
                    'tag_name': 'git',
                    'tag_color': '#32CD32',
                    'groups': [
                        {
                            'type': 'category',
                            'name': 'CONFIG',
                            'items': [
                                {
                                    'id': 1,
                                    'label': 'Inicializar repositorio',
                                    'content': '$ git init\n$ git clone <url_del_repositorio>',
                                    'type': 'CODE',
                                    'description': 'Comandos para iniciar un nuevo repositorio'
                                },
                                {
                                    'id': 2,
                                    'label': 'Configurar usuario',
                                    'content': '$ git config --global user.name "Tu Nombre"\n$ git config --global user.email "tu@email.com"',
                                    'type': 'CODE',
                                    'description': 'Configuración de identidad'
                                }
                            ]
                        },
                        {
                            'type': 'category',
                            'name': 'COMMITS',
                            'items': [
                                {
                                    'id': 3,
                                    'label': 'Crear commit',
                                    'content': '$ git add .\n$ git commit -m "mensaje del commit"\n$ git push origin main',
                                    'type': 'CODE',
                                    'description': 'Flujo básico de commits'
                                }
                            ]
                        }
                    ]
                },
                {
                    'tag_name': 'backend',
                    'tag_color': '#FF6B6B',
                    'groups': [
                        {
                            'type': 'list',
                            'name': 'APIs REST',
                            'items': [
                                {
                                    'id': 4,
                                    'label': 'Documentación de FastAPI',
                                    'content': 'https://fastapi.tiangolo.com/',
                                    'type': 'URL',
                                    'description': 'Framework web moderno y rápido para Python'
                                },
                                {
                                    'id': 5,
                                    'label': 'Endpoint de autenticación',
                                    'content': 'Este endpoint maneja el login de usuarios mediante JWT tokens. Requiere email y password en el body de la petición POST. Retorna un token de acceso válido por 24 horas y un refresh token válido por 7 días.',
                                    'type': 'TEXT',
                                    'description': 'Descripción del endpoint /api/auth/login'
                                }
                            ]
                        },
                        {
                            'type': 'category',
                            'name': 'Database',
                            'items': [
                                {
                                    'id': 6,
                                    'label': 'Carpeta de migraciones',
                                    'content': 'C:\\Users\\ASUS\\Desktop\\proyectos_python\\widget_sidebar\\src\\database\\migrations',
                                    'type': 'PATH',
                                    'description': 'Directorio con migraciones de BD'
                                }
                            ]
                        }
                    ]
                },
                {
                    'tag_name': 'docs',
                    'tag_color': '#FFD700',
                    'groups': [
                        {
                            'type': 'tag',
                            'name': 'python',
                            'items': [
                                {
                                    'id': 7,
                                    'label': 'Guía de estilos PEP 8',
                                    'content': 'https://peps.python.org/pep-0008/',
                                    'type': 'URL',
                                    'description': 'Convenciones de código Python'
                                },
                                {
                                    'id': 8,
                                    'label': 'Introducción a Python',
                                    'content': '''Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Su filosofía de diseño enfatiza la legibilidad del código con el uso de indentación significativa. Python es dinámicamente tipado y cuenta con recolección de basura automática. Soporta múltiples paradigmas de programación, incluyendo programación estructurada, orientada a objetos y funcional.

Las características principales de Python incluyen:
- Sintaxis clara y legible
- Biblioteca estándar extensa
- Gran comunidad y ecosistema de paquetes
- Multiplataforma (Windows, macOS, Linux)
- Ideal para desarrollo web, ciencia de datos, automatización, IA y más

Python fue creado por Guido van Rossum y lanzado por primera vez en 1991. El nombre del lenguaje viene de Monty Python, no de la serpiente pitón como muchos creen.''',
                                    'type': 'TEXT',
                                    'description': 'Resumen sobre el lenguaje Python (texto extenso con >800 chars)'
                                }
                            ]
                        }
                    ]
                }
            ],
            'ungrouped_items': [
                {
                    'id': 9,
                    'label': 'Nota miscelánea',
                    'content': 'Este es un item que no pertenece a ningún tag de proyecto específico.',
                    'type': 'TEXT',
                    'description': 'Item sin tag de proyecto'
                }
            ]
        }

    def filter_by_project_tags(
        self,
        project_data: Dict,
        tag_filters: List[str],
        match_mode: str = 'OR'
    ) -> Dict:
        """
        Filtrar datos del proyecto por tags

        Args:
            project_data: Datos del proyecto completo
            tag_filters: Lista de nombres de tags para filtrar
            match_mode: 'AND' o 'OR' para coincidencia de tags

        Returns:
            Datos del proyecto filtrados
        """
        if not tag_filters:
            return project_data

        filtered_data = project_data.copy()
        filtered_data['tags'] = []

        # Filtrar tags
        for tag_data in project_data['tags']:
            if tag_data['tag_name'] in tag_filters:
                filtered_data['tags'].append(tag_data)

        # Si es modo AND, verificar que tenga todos los tags
        if match_mode == 'AND' and len(filtered_data['tags']) != len(tag_filters):
            filtered_data['tags'] = []

        return filtered_data

    def get_total_items_count(self, project_data: Dict) -> int:
        """
        Obtener cantidad total de items en el proyecto

        Args:
            project_data: Datos del proyecto

        Returns:
            Número total de items
        """
        total = 0

        # Contar items en tags
        for tag in project_data.get('tags', []):
            for group in tag.get('groups', []):
                total += len(group.get('items', []))

        # Contar items sin agrupar
        total += len(project_data.get('ungrouped_items', []))

        return total

    def get_tags_summary(self, project_data: Dict) -> List[Dict]:
        """
        Obtener resumen de tags con conteos

        Args:
            project_data: Datos del proyecto

        Returns:
            Lista de diccionarios con nombre, color y conteo de cada tag
        """
        summary = []

        for tag in project_data.get('tags', []):
            item_count = 0
            for group in tag.get('groups', []):
                item_count += len(group.get('items', []))

            summary.append({
                'name': tag['tag_name'],
                'color': tag['tag_color'],
                'count': item_count
            })

        return summary
