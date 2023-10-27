import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import QDateTime
from interfaceProgram import Ui_MainWindow
import serial
import threading

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.OnButt.setText("Запуск")
        self.is_running = False
        self.can_add_to_list = False
        self.serial_port = None

        self.ui.OnButt.clicked.connect(self.toggle_reading)

    def toggle_reading(self):
        self.is_running = not self.is_running

        if self.is_running:
            self.ui.OnButt.setText("Остановить")
            self.ui.listWidget.clear()  # Очищаем список перед добавлением новых строк
            self.can_add_to_list = True  # Разрешаем добавление новых строк
            self.start_reading()
        else:
            self.ui.OnButt.setText("Запуск")
            self.stop_reading()

    def start_reading(self):
        try:
            self.serial_port = serial.Serial('COM4', 9600, timeout=1)
            threading.Thread(target=self.read_from_serial, daemon=True).start()
        except serial.SerialException:
            self.ui.listWidget.addItem("Не удалось подключиться к порту COM4")

    def stop_reading(self):
        self.can_add_to_list = False  # Запрещаем добавление новых строк
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def read_from_serial(self):
        while self.is_running and self.serial_port and self.serial_port.is_open:
            line = self.serial_port.readline().decode().strip()
            if line and self.can_add_to_list:
                self.add_to_list(line)

    def add_to_list(self, data):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        label_info = f"Событие: {data}, Время: {current_time}"
        list_item = QListWidgetItem(label_info)
        self.ui.listWidget.addItem(list_item)
        self.ui.listWidget.addItem("")  # Пустая строка для разделения

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
