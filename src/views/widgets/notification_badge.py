"""
Notification Badge Widget
Badge that displays a number count with color coding
"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


class NotificationBadge(QLabel):
    """
    A circular badge that displays a number count
    Changes color based on count (red if > 0, yellow if 0)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.setup_ui()

    def setup_ui(self):
        """Setup badge appearance"""
        # Default size (can be changed externally)
        if self.size() == QSize(0, 0):
            self.setFixedSize(QSize(20, 20))

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Font - size adapts to badge size
        font = QFont()
        font.setBold(True)
        self.setFont(font)

        # Initial update
        self.update_badge(0)

    def update_badge(self, count):
        """
        Update badge count and color

        Args:
            count: Number to display
        """
        self.count = count
        self.setText(str(count))

        # Color based on count
        if count > 0:
            # Red background for active notifications
            background_color = "#ff5252"
            text_color = "#ffffff"
        else:
            # Yellow background for no notifications
            background_color = "#ffc107"
            text_color = "#000000"

        # Adapt styling based on size
        size = self.width()
        if size >= 45:
            # Large badge
            border_radius = size // 2
            font_size = "18pt"
            padding = "4px"
        elif size >= 30:
            # Medium badge
            border_radius = size // 2
            font_size = "12pt"
            padding = "3px"
        else:
            # Small badge
            border_radius = 10
            font_size = "9pt"
            padding = "2px"

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {background_color};
                color: {text_color};
                border-radius: {border_radius}px;
                font-weight: bold;
                font-size: {font_size};
                padding: {padding};
            }}
        """)

        # Show/hide based on preference (always show for this use case)
        self.setVisible(True)

    def get_count(self):
        """Get current count"""
        return self.count
