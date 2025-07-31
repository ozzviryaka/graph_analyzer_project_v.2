import datetime

class Logger:
    """
    Простий ефективний логгер для запису повідомлень у файл та консоль.
    """

    def __init__(self, filepath="app.log"):
        self.filepath = filepath

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

    def info(self, message):
        self.log(message, "INFO")

    def warning(self, message):
        self.log(message, "WARNING")

    def error(self, message):
        self.log(message, "ERROR")