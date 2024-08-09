import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QScrollArea, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QPoint
import pyperclip


class CustomTitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.title_label = QLabel("Dishapradarsan", self)
        self.title_label.setStyleSheet("color: #ffffff; padding: 5px; font-size: 16px;font-weight: bold;")
        layout.addWidget(self.title_label)

        # Minimize button
        minimize_button = QPushButton("–", self)
        minimize_button.setFixedSize(20, 20)
        minimize_button.setStyleSheet("color: #93a1a1; background-color: #073642;")
        minimize_button.clicked.connect(self.parent.showMinimized)
        layout.addWidget(minimize_button)

        # Close button
        close_button = QPushButton("×", self)
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("color: #93a1a1; background-color: #073642;")
        close_button.clicked.connect(self.parent.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #002b36;")

        self.old_pos = self.pos()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.old_pos = event.globalPos()


class DirectoryStructureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 600, 500)

        # Set custom icon
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'icons/folder.png')))

        # Apply Solarized Black Theme
        self.apply_solarized_black_theme()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Custom Title Bar
        self.title_bar = CustomTitleBar(self)
        layout.addWidget(self.title_bar)

        # Path Input Layout
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(self)
        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_directory)
        path_layout.addWidget(QLabel("Directory Path:"))
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)

        # Ignore Directories Input Layout
        ignore_layout = QHBoxLayout()
        self.ignore_input = QLineEdit(self)
        browse_ignore_button = QPushButton("Browse", self)
        browse_ignore_button.clicked.connect(self.browse_ignore_directory)
        ignore_layout.addWidget(QLabel("Ignore Directories:"))
        ignore_layout.addWidget(self.ignore_input)
        ignore_layout.addWidget(browse_ignore_button)

        # Get Structure Button
        get_structure_button = QPushButton("Get Structure", self)
        get_structure_button.clicked.connect(self.get_structure)

        # Output Area
        self.output_area = QTextEdit(self)
        self.output_area.setFont(QFont('Courier', 10))
        self.output_area.setReadOnly(True)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.output_area)

        # Copy Structure Button
        copy_button = QPushButton("Copy Structure", self)
        copy_button.clicked.connect(self.copy_structure)

        # Adding Widgets to Layout
        layout.addLayout(path_layout)
        layout.addLayout(ignore_layout)
        layout.addWidget(get_structure_button)
        layout.addWidget(scroll_area)
        layout.addWidget(copy_button)

        self.setLayout(layout)

    def apply_solarized_black_theme(self):
        """Apply Solarized Black Theme to the interface."""
        palette = QPalette()

        # Base colors
        base00 = QColor("#002b36")  # Background
        base01 = QColor("#073642")  # Background highlight
        base02 = QColor("#586e75")  # Comments/Secondary Text
        base03 = QColor("#657b83")  # Subtle Text
        base0 = QColor("#839496")   # Normal Text
        base1 = QColor("#93a1a1")   # Highlight Text
        base2 = QColor("#eee8d5")   # Light background
        base3 = QColor("#fdf6e3")   # Lightest background
        yellow = QColor("#b58900")
        orange = QColor("#cb4b16")
        red = QColor("#dc322f")
        magenta = QColor("#d33682")
        violet = QColor("#6c71c4")
        blue = QColor("#268bd2")
        cyan = QColor("#2aa198")
        green = QColor("#859900")

        # Set the palette colors
        palette.setColor(QPalette.Window, base00)
        palette.setColor(QPalette.WindowText, base0)
        palette.setColor(QPalette.Base, base00)
        palette.setColor(QPalette.AlternateBase, base01)
        palette.setColor(QPalette.ToolTipBase, base3)
        palette.setColor(QPalette.ToolTipText, base1)
        palette.setColor(QPalette.Text, base0)
        palette.setColor(QPalette.Button, base01)
        palette.setColor(QPalette.ButtonText, base1)
        palette.setColor(QPalette.BrightText, red)
        palette.setColor(QPalette.Highlight, blue)
        palette.setColor(QPalette.HighlightedText, base3)

        # Apply the palette
        self.setPalette(palette)

        # Apply custom styles for the buttons and title bar
        self.setStyleSheet("""
            QWidget {
                background-color: #002b36;
                color: #839496;
                font-family: Courier;
            }
            QLabel {
                color: #93a1a1;
            }
            QPushButton {
                background-color: #073642;
                color: #93a1a1;
                border: 1px solid #586e75;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #586e75;
            }
            QLineEdit, QTextEdit {
                background-color: #073642;
                color: #839496;
                border: 1px solid #586e75;
            }
            QScrollArea {
                border: 1px solid #586e75;
            }
        """)

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.path_input.setText(dir_path)

    def browse_ignore_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory to Ignore")
        if dir_path:
            current_text = self.ignore_input.text().strip()
            if current_text:
                self.ignore_input.setText(f"{current_text}, {os.path.basename(dir_path)}")
            else:
                self.ignore_input.setText(os.path.basename(dir_path))

    def get_structure(self):
        dir_path = self.path_input.text().strip()
        if not dir_path or not os.path.isdir(dir_path):
            QMessageBox.warning(self, "Invalid Path", "Please enter a valid directory path.")
            return

        ignore_dirs = [d.strip() for d in self.ignore_input.text().split(',') if d.strip()]
        structure = self.build_structure(dir_path, ignore_dirs)
        self.output_area.setText(structure)

    def build_structure(self, root_dir, ignore_dirs, prefix=""):
        structure = f"{os.path.basename(root_dir)}/\n"

        dirs, files = [], []
        for entry in os.listdir(root_dir):
            full_path = os.path.join(root_dir, entry)
            if os.path.isdir(full_path) and entry not in ignore_dirs and entry != '__pycache__':
                dirs.append(entry)
            elif os.path.isfile(full_path):
                files.append(entry)

        # Add files
        for i, file in enumerate(files):
            if i == len(files) - 1 and not dirs:
                structure += f"{prefix}└── {file}\n"
            else:
                structure += f"{prefix}├── {file}\n"

        # Add directories
        for i, dir in enumerate(dirs):
            dir_path = os.path.join(root_dir, dir)
            if i == len(dirs) - 1:
                structure += f"{prefix}└── {dir}/\n"
                structure += self.build_structure(dir_path, ignore_dirs, prefix + "    ")
            else:
                structure += f"{prefix}├── {dir}/\n"
                structure += self.build_structure(dir_path, ignore_dirs, prefix + "│   ")

        return structure

    def copy_structure(self):
        structure = self.output_area.toPlainText()
        pyperclip.copy(structure)
        QMessageBox.information(self, "Copied", "Directory structure copied to clipboard.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DirectoryStructureApp()
    ex.show()
    sys.exit(app.exec_())
