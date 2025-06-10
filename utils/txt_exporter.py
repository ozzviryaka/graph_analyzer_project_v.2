from PyQt5.QtWidgets import QTextEdit

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
            print(f"Помилка при експорті у .txt: {e}")
            return False
