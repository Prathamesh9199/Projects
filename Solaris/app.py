import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QPoint
from utility.chat_llm import ChatModel

class FloatingChatUI(QWidget):
    def __init__(self, chat_model):
        super().__init__()
        self.drag_pos = None
        self.init_ui()
        self.chat_model = chat_model

    def init_ui(self):
        self.setWindowTitle("AI Agent")
        self.setWindowOpacity(0.9)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setGeometry(1000, 100, 400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                color: white;
                font-family: Consolas;
                font-size: 14px;
            }
            QLineEdit {
                padding: 6px;
                border: none;
                border-top: 1px solid #555;
                background-color: #222;
                color: white;
            }
            QTextEdit {
                border: none;
                background-color: transparent;
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: #aaa;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: white;
            }
        """)

        layout = QVBoxLayout()

        # Title bar buttons
        button_layout = QHBoxLayout()
        self.minimize_btn = QPushButton("–")
        self.close_btn = QPushButton("×")

        self.minimize_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)

        button_layout.addStretch()
        button_layout.addWidget(self.minimize_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(self.handle_input)

        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_box)
        self.setLayout(layout)

    def handle_input(self):
        user_input = self.input_box.text().strip()
        if not user_input:
            return

        self.chat_display.append(f"You: {user_input}")
        self.input_box.clear()

        response = self.chat_model.get_response(user_input)
        self.chat_display.append(f"Agent: {response.message.content}\n")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        QApplication.quit()

    # Make the window draggable
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


if __name__ == "__main__":

    # initialize the chat model
    config_path = r"utility\\config.ini"
    chat_model = ChatModel(config_path)

    app = QApplication(sys.argv)
    chat_ui = FloatingChatUI(chat_model)
    chat_ui.show()
    sys.exit(app.exec())
