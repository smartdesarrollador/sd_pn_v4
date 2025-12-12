"""
Paleta de colores para vista completa de proyectos

MODO OSCURO ÚNICAMENTE - Alto contraste para máxima legibilidad

Autor: Widget Sidebar Team
Versión: 1.0
"""


class FullViewColorPalette:
    """
    Paleta de colores para vista completa de proyectos

    IMPORTANTE: Esta paleta es SOLO para modo oscuro.
    NO implementar modo claro ni otros modos.
    """

    # ============================================
    # FONDOS
    # ============================================
    BG_MAIN = "#1A1A1A"              # Fondo principal
    BG_ITEM_TEXT = "#1E1E1E"         # Fondo para items de texto
    BG_ITEM_CODE = "#0D1117"         # Fondo para items de código
    BG_ITEM_URL = "#1A1A2E"          # Fondo para items de URL
    BG_ITEM_PATH = "#1E1E1E"         # Fondo para items de path
    BG_HOVER = "#2A2A2A"             # Fondo al hacer hover

    # ============================================
    # TEXTOS
    # ============================================
    TEXT_PRIMARY = "#E0E0E0"         # Texto principal
    TEXT_SECONDARY = "#B0B0B0"       # Texto secundario
    TEXT_CODE = "#7CFC00"            # Texto de código (verde neón)
    TEXT_URL = "#4A9EFF"             # Texto de URLs (azul claro)
    TEXT_PATH = "#FFA500"            # Texto de paths (naranja)

    # ============================================
    # JERARQUÍA (Títulos y encabezados)
    # ============================================
    TITLE_PROJECT = "#7CFC00"        # Verde lima - Título de proyecto
    TITLE_TAG = "#32CD32"            # Verde medio - Tags de proyecto
    TITLE_GROUP = "#FFD700"          # Amarillo dorado - Grupos de items

    # ============================================
    # BORDES
    # ============================================
    BORDER_DEFAULT = "#404040"       # Borde por defecto
    BORDER_CODE = "#2D4A2B"          # Borde para código
    BORDER_URL = "#2C3E73"           # Borde para URLs
    BORDER_PATH = "#8B4513"          # Borde para paths

    # ============================================
    # ESTADOS (Acentos y feedback)
    # ============================================
    ACCENT = "#00BFFF"               # Color de acento
    SUCCESS = "#00FF00"              # Verde éxito
    WARNING = "#FFD700"              # Amarillo advertencia
    ERROR = "#FF6B6B"                # Rojo error

    # ============================================
    # SCROLLBARS
    # ============================================
    SCROLLBAR_BG = "#2A2A2A"         # Fondo de scrollbar
    SCROLLBAR_HANDLE = "#505050"     # Handle de scrollbar
    SCROLLBAR_HANDLE_HOVER = "#606060"  # Handle hover

    @classmethod
    def get_contrast_ratio(cls, color1: str, color2: str) -> float:
        """
        Calcular ratio de contraste entre dos colores

        Args:
            color1: Color en formato hex (#RRGGBB)
            color2: Color en formato hex (#RRGGBB)

        Returns:
            Ratio de contraste (debe ser >= 7.0 para WCAG AAA)
        """
        def hex_to_rgb(hex_color: str) -> tuple:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def relative_luminance(rgb: tuple) -> float:
            r, g, b = [x / 255.0 for x in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)

        lum1 = relative_luminance(rgb1)
        lum2 = relative_luminance(rgb2)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        return (lighter + 0.05) / (darker + 0.05)

    @classmethod
    def validate_accessibility(cls) -> dict:
        """
        Validar que todos los contrastes cumplan WCAG AAA (7:1)

        Returns:
            Dict con validaciones de contraste
        """
        validations = {
            'TEXT_PRIMARY vs BG_MAIN': cls.get_contrast_ratio(
                cls.TEXT_PRIMARY, cls.BG_MAIN
            ),
            'TEXT_CODE vs BG_ITEM_CODE': cls.get_contrast_ratio(
                cls.TEXT_CODE, cls.BG_ITEM_CODE
            ),
            'TEXT_URL vs BG_ITEM_URL': cls.get_contrast_ratio(
                cls.TEXT_URL, cls.BG_ITEM_URL
            ),
            'TEXT_PATH vs BG_ITEM_PATH': cls.get_contrast_ratio(
                cls.TEXT_PATH, cls.BG_ITEM_PATH
            ),
            'TITLE_PROJECT vs BG_MAIN': cls.get_contrast_ratio(
                cls.TITLE_PROJECT, cls.BG_MAIN
            ),
        }

        return validations


# Validación en tiempo de importación (opcional, para desarrollo)
if __name__ == '__main__':
    print("Validación de Accesibilidad WCAG AAA (ratio mínimo: 7.0)")
    print("=" * 60)

    validations = FullViewColorPalette.validate_accessibility()

    for pair, ratio in validations.items():
        status = "✓ PASS" if ratio >= 7.0 else "✗ FAIL"
        print(f"{status} {pair}: {ratio:.2f}:1")

    print("=" * 60)
