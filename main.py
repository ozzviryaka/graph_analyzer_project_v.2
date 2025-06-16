from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.logger import Logger
from locales.locale_manager import LocaleManager
import sys

if __name__ == "__main__":
    logger = Logger()
    LocaleManager.load_locale()
    logger.info(LocaleManager.get_locale("main", "app_start"))
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    exit_code = app.exec_()
    logger.info(LocaleManager.get_locale("main", "app_end"))
    sys.exit(exit_code)
