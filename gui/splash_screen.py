from PyQt5.QtWidgets import QSplashScreen, QLabel, QProgressBar, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QBrush
from locales.locale_manager import LocaleManager
import time

class SplashLoadingThread(QThread):
    """Потік для симуляції завантаження з оновленням прогресу"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.loading_steps = [
            ("splash_loading_locale", 200),
            ("splash_loading_components", 300),
            ("splash_loading_algorithms", 400),
            ("splash_loading_interface", 300),
            ("splash_loading_themes", 200),
            ("splash_loading_complete", 100)
        ]
    
    def run(self):
        """Виконання кроків завантаження"""
        total_time = sum(step[1] for step in self.loading_steps)
        current_progress = 0
        
        for i, (step_key, duration) in enumerate(self.loading_steps):
            # Отримуємо локалізований текст
            step_text = LocaleManager.get_locale("splash", step_key)
            if not step_text:  # Fallback якщо локалізація не знайдена
                step_text = f"Loading step {i+1}..."
            
            self.progress_updated.emit(int((i / len(self.loading_steps)) * 100), step_text)
            self.msleep(duration)  # Симуляція завантаження
        
        self.progress_updated.emit(100, LocaleManager.get_locale("splash", "splash_loading_complete"))
        self.msleep(200)
        self.finished.emit()

class SplashScreen(QSplashScreen):
    """Екран завантаження програми"""
    
    def __init__(self):
        # Створюємо pixmap для splash screen
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(45, 45, 45))  # Темний фон
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # Ініціалізуємо змінні для відображення
        self.current_progress = 0
        self.current_text = LocaleManager.get_locale("splash", "splash_initializing") or "Initializing..."
        
        self.init_loading_thread()
        
    def init_loading_thread(self):
        """Ініціалізація потоку завантаження"""
        self.loading_thread = SplashLoadingThread()
        self.loading_thread.progress_updated.connect(self.update_progress)
        self.loading_thread.finished.connect(self.loading_finished)
        
    def start_loading(self):
        """Запуск процесу завантаження"""
        self.loading_thread.start()
        
    def update_progress(self, value, text):
        """Оновлення прогресу завантаження"""
        self.current_progress = value
        self.current_text = text
        self.repaint()  # Перемальовуємо splash screen
        
    def loading_finished(self):
        """Завершення завантаження"""
        QTimer.singleShot(500, self.close)  # Затримка перед закриттям
        
    def paintEvent(self, event):
        """Кастомна відрисовка splash screen"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Заливаємо фон
        painter.fillRect(self.rect(), QColor(45, 45, 45))
        
        # Малюємо заголовок
        painter.setPen(QColor(255, 255, 255))
        title_font = QFont("Arial", 24, QFont.Bold)
        painter.setFont(title_font)
        title_rect = QRect(0, 80, self.width(), 40)
        painter.drawText(title_rect, Qt.AlignCenter, "Graph Analyzer")
        
        # Малюємо версію
        version_font = QFont("Arial", 12)
        painter.setFont(version_font)
        painter.setPen(QColor(204, 204, 204))
        version_rect = QRect(0, 120, self.width(), 20)
        painter.drawText(version_rect, Qt.AlignCenter, "v2.0")
        
        # Малюємо опис
        desc_font = QFont("Arial", 10)
        painter.setFont(desc_font)
        painter.setPen(QColor(170, 170, 170))
        desc_rect = QRect(0, 150, self.width(), 20)
        painter.drawText(desc_rect, Qt.AlignCenter, "Розширений аналізатор графів з візуалізацією")
        
        # Малюємо текст завантаження
        loading_font = QFont("Arial", 11)
        painter.setFont(loading_font)
        painter.setPen(QColor(170, 170, 170))
        text_rect = QRect(50, 250, self.width() - 100, 20)
        painter.drawText(text_rect, Qt.AlignLeft, self.current_text)
        
        # Малюємо прогрес бар
        progress_rect = QRect(50, 280, self.width() - 100, 20)
        
        # Фон прогрес бару
        painter.setBrush(QBrush(QColor(51, 51, 51)))
        painter.setPen(QColor(85, 85, 85))
        painter.drawRoundedRect(progress_rect, 5, 5)
        
        # Заповнена частина
        if self.current_progress > 0:
            fill_width = int((progress_rect.width() - 4) * (self.current_progress / 100))
            fill_rect = progress_rect.adjusted(2, 2, -2, -2)
            fill_rect.setWidth(fill_width)
            
            painter.setBrush(QBrush(QColor(0, 120, 212)))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(fill_rect, 3, 3)
            
        # Малюємо відсоток
        percent_font = QFont("Arial", 9, QFont.Bold)
        painter.setFont(percent_font)
        painter.setPen(QColor(255, 255, 255))
        percent_rect = QRect(0, 305, self.width(), 15)
        painter.drawText(percent_rect, Qt.AlignCenter, f"{self.current_progress}%")
