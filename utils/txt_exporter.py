from PyQt5.QtWidgets import QTextEdit
from utils.logger import Logger
from locales.locale_manager import LocaleManager

class TxtExporter:
    """
    Клас для експорту даних у текстовий файл (.txt) з QTextEdit.
    """
    @staticmethod
    def export(text_edit: QTextEdit, filepath: str):
        """
        Експортує дані з QTextEdit у файл .txt.

        :param text_edit: QTextEdit з даними для експорту
        :param filepath: Шлях до файлу для збереження
        """
        try:
            data = text_edit.toPlainText()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
            return True
        except Exception as e:
            Logger().error(LocaleManager.get_locale("txt_exporter", "export_error").format(error=str(e)))
            return False
