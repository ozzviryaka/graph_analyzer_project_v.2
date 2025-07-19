from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from gui.main_window import MainWindow
from gui.splash_screen import SplashScreen
from utils.logger import Logger
from locales.locale_manager import LocaleManager
import sys

if __name__ == "__main__":
    logger = Logger()
    
    # Створюємо додаток
    app = QApplication(sys.argv)
    
    # Завантажуємо локалізацію
    LocaleManager.load_locale()
    logger.info(LocaleManager.get_locale("main", "app_start"))
    
    # Створюємо та показуємо splash screen
    splash = SplashScreen()
    splash.show()
    
    # Запускаємо процес завантаження
    splash.start_loading()
    
    # Створюємо головне вікно в глобальній області
    window = None
    
    def show_main_window():
        """Показати головне вікно після завершення splash screen"""
        global window
        window = MainWindow()
        window.showMaximized()
    
    # Підключаємо показ головного вікна до завершення splash screen
    splash.loading_thread.finished.connect(show_main_window)
    
    # Запускаємо додаток
    exit_code = app.exec_()
    logger.info(LocaleManager.get_locale("main", "app_end"))
    sys.exit(exit_code)
