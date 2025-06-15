from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.logger import Logger
import sys

if __name__ == "__main__":
    logger = Logger()
    logger.info("Запуск програми Graph Analyzer")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    exit_code = app.exec_()
    logger.info("Завершення роботи програми Graph Analyzer")
    sys.exit(exit_code)
