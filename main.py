from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
