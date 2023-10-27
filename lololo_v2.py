import sys
import threading

import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QDialog, QComboBox
from PyQt5.QtCore import QDateTime
from interfaceProgram import Ui_MainWindow
from Setting import Ui_Setting
import configparser


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
        self.ui.Setting_Button.clicked.connect(self.open_settings_window)

        # Применить начальные настройки темы
        self.apply_theme()

    def open_settings_window(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def toggle_reading(self):
        self.is_running = not self.is_running

        if self.is_running:
            self.ui.OnButt.setText("Остановить")
            self.ui.listWidget.clear()
            self.can_add_to_list = True
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
        self.can_add_to_list = False
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
        self.ui.listWidget.addItem("")

    def apply_theme(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        index = config.get('Theme', 'index', fallback='0')
        background_color = config.get('Theme', 'background_color', fallback='#FFFFFF')
        text_color = config.get('Theme', 'text_color', fallback='#000000')
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.listWidget.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.OnButt.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.Setting_Button.setStyleSheet(f"background-color: {background_color}; color: {text_color};")


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_Setting()
        self.ui.setupUi(self)
        self.ui.theme_combobox.currentIndexChanged.connect(self.change_theme)
        config = configparser.ConfigParser()
        config.read('config.ini')
        theme_type = config.get('Theme', 'theme', fallback='0')  # Чтение типа темы (светлая или темная)
        background_color = config.get('Theme', 'Background_Color', fallback='#FFFFFF')  # Чтение цвета фона
        text_color = config.get('Theme', 'Text_Color', fallback='#000000')  # Чтение цвета текста
        self.ui.theme_combobox.setCurrentText("Светлая" if 'theme' == 0 else "Темная")
        self.apply_theme(theme_type, background_color, text_color)
        MyWindow.apply_theme(parent)

    def change_theme(self, index):
        theme = index if index == 0 else "1"
        background_color = "#A8D7E6" if index == theme else '#333333'
        text_color = '#000000' if index == theme else '#FFFFFF'
        self.apply_theme(theme, background_color, text_color)


    def apply_theme(self, theme, background_color, text_color):
        theme = theme
        background_color = background_color
        text_color = text_color
        # Применить цветовые настройки к окну настроек
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.theme_combobox.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.Language_Box.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        theme = "0" if theme == 0 else "1"

        # Сохранить настройки в файл config.ini
        config = configparser.ConfigParser()
        config['Theme'] = {
            'index': theme,
            'background_color': background_color,
            'text_color': text_color
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
