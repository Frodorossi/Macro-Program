import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

class MouseTrackingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mouse Tracking Example")
        self.setGeometry(100, 100, 400, 400)

        self.mouse_coordinates_label = QLabel(self)
        self.mouse_coordinates_label.setGeometry(10, 10, 150, 30)
        self.mouse_coordinates_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Track mouse movements in the main window
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.mouse_coordinates_label.setText(f"Mouse Coordinates: ({x}, {y})")

def main():
    app = QApplication(sys.argv)
    window = MouseTrackingApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()