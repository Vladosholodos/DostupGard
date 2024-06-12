import configparser
import sys
import threading

import mysql.connector
import pymysql
import serial
import datetime
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QDialog, QTableWidgetItem, QTableWidget
from mysql.connector import Error

from Setting import Ui_Setting
from Stats import Ui_stats_window
from interfaceProgram import Ui_MainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Инициализация главного окна
        self.ui.OnButt.setText("Запустить")  # Текст дял кнопки
        self.is_running = False  # Флаг запуска чтения порта
        self.can_add_to_list = False  # Флаг возможности добавления записей в QListWidget
        self.serial_port = None  # Флаг открытия порта
        self.ui.OnButt.clicked.connect(self.toggle_reading)  # Функция при нажатии на кнопку "Запустить"
        self.ui.Setting_Button.clicked.connect(self.open_settings_window)  # Функция при нажатии на кнопку "..."
        self.ui.stats_button.clicked.connect(self.open_stats_window)  # Функция при нажатии на кнопку "Статистика"
        self.stats_window = None  # Флаг окна статистики

        # Применить начальные настройки темы
        self.apply_theme()

    def open_settings_window(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def open_stats_window(self):
        stats_window = StatsWindow(self)
        stats_window.show()

    def toggle_reading(self):
        self.is_running = not self.is_running

        if self.is_running:
            self.ui.OnButt.setText("Остановить")
            self.ui.listWidget.clear()
            self.can_add_to_list = True
            self.start_reading()
        else:
            self.ui.OnButt.setText("Запустить")
            self.stop_reading()

    def start_reading(self):
        try:
            self.serial_port = serial.Serial('COM5', 9600, timeout=1)
            threading.Thread(target=self.read_from_serial, daemon=True).start()
            self.ui.listWidget.addItem("Все работает в штатном режиме. Хорошего дня!")
        except serial.SerialException:
            self.ui.listWidget.addItem("Не удалось подключиться к порту COM5")

    def stop_reading(self):
        self.can_add_to_list = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def read_from_serial(self):
        while self.is_running and self.serial_port and self.serial_port.is_open:
            line = self.serial_port.readline().decode().strip()
            if line and self.can_add_to_list:
                if is_user_authorized(line):
                    self.add_to_list(line)
                    # Добавляем данные в базу данных при каждом событии
                    add_data_to_database(line)
                    print(line)
                else:
                    self.add_to_list(f"Неудачная попытка доступа: {line}")
                    add_data_to_database(f"Неудачная попытка доступа: {line}")

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


def is_user_authorized(data):
    connection = mysql.connector.connect(
        host='localhost',
        user='admin',
        password='123qwe!@#QWE',
        database='test'  # Название базы данных
    )
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM authorized_users WHERE uid = %s", (data,))
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return result > 0


def add_data_to_database(data):
    try:
        # Подключение к базе данных
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='123qwe!@#QWE',
            database='test'  # Название базы данных
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # SQL-запрос для вставки данных
            insert_query = "INSERT INTO work_information (Время, Код) VALUES (%s, %s)"
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            data_to_insert = (current_time, data)

            if is_user_authorized(data):

                # Выполнение запроса
                cursor.execute(insert_query, data_to_insert)
                connection.commit()
                print("Данные успешно добавлены в базу данных")

                # Получение текущего значения Внутри
                uid = data
                select_in_value_query = "SELECT Внутри FROM user_information WHERE uid = %s"
                cursor.execute(select_in_value_query, (uid,))
                current_in_value = cursor.fetchone()[0]
                # Вычисление нового значения "in"
                if current_in_value == 1:
                    new_in_value = 0
                if current_in_value == 0:
                    new_in_value = 1
                # Обновление значения "in"
                update_in_value_query = "UPDATE user_information SET Внутри = %s WHERE uid = %s"
                cursor.execute(update_in_value_query, (new_in_value, uid))
                connection.commit()
            else:
                insert_querys = "INSERT INTO work_information (Время, Код) VALUES (%s, %s)"
                current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
                cursor.execute(insert_querys, (current_time, data))

    except Error as e:
        print(f"Ошибка: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Подключение к базе данных закрыто")


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_Setting()
        self.ui.setupUi(self)  # Инициализация окна настроек
        self.ui.theme_combobox.currentIndexChanged.connect(self.change_theme)
        config = configparser.ConfigParser()
        config.read('config.ini')  # Функция чтения файла config.ini
        theme_type = config.get('Theme', 'theme', fallback='0')  # Получение переменных из файла config.ini
        background_color = config.get('Theme', 'Background_Color',
                                      fallback='#FFFFFF')  # Получение переменной из файла config.ini
        text_color = config.get('Theme', 'Text_Color', fallback='#000000')  # Получение переменной из файла config.ini
        self.ui.theme_combobox.setCurrentText(
            "Светлая" if theme_type == '0' else "Темная")  # Получение переменной из файла config.ini
        self.apply_theme(theme_type, background_color, text_color)  # Вызов функции, которая применяет настройки темы
        MyWindow.apply_theme(parent)  # Определение родительского окна "Главного окна"

    def change_theme(self, index):
        theme = '0' if index == 0 else '1'
        background_color = "#A8D7E6" if theme == '0' else '#333333'
        text_color = '#000000' if theme == '0' else '#FFFFFF'
        self.apply_theme(theme, background_color, text_color)

    def apply_theme(self, theme, background_color, text_color):
        theme = theme
        background_color = background_color
        text_color = text_color
        # Применить цветовые настройки к окну настроек
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.theme_combobox.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.Language_Box.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        theme = "0" if theme == '0' else "1"

        # Сохранить настройки в файл config.ini
        config = configparser.ConfigParser()
        config['Theme'] = {
            'theme': theme,
            'Background_Color': background_color,
            'Text_Color': text_color
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


# Статистика--------------------------------------------------
class StatsWindow(QMainWindow):

    def __init__(self, parent=None):
        super(StatsWindow, self).__init__(parent)
        self.ui = Ui_stats_window()
        self.ui.setupUi(self)
        self.load_data_to_combobox()
        self.ui.pushButton.clicked.connect(self.clickonstats)

        config = configparser.ConfigParser()
        config.read('config.ini')
        theme_type = config.get('Theme', 'theme', fallback='0')
        background_color = config.get('Theme', 'Background_Color', fallback='#FFFFFF')
        text_color = config.get('Theme', 'Text_Color', fallback='#000000')
        self.apply_theme(background_color, text_color)

    def apply_theme(self, background_color, text_color):
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.ui.statsTable.setStyleSheet(f"""
               QTableWidget {{
                   background-color: {background_color};
                   color: {text_color};
                   gridline-color: {text_color};
                   font-size: 14px;
               }}
               QHeaderView::section {{
                   background-color: {background_color};
                   color: {text_color};
                   padding: 4px;
                   font-size: 14px;
                   font-weight: bold;
               }}
               QTableWidget::item {{
                   padding: 4px;
                   background-color: {background_color};
                   color: {text_color};
               }}
           """)

    def clickonstats(self):
        connection = pymysql.connect(host='localhost', user='admin', password='123qwe!@#QWE',
                                     database='test')  # Подключение к базе
        selected_user = self.ui.comboBox.currentText()
        try:
            with connection.cursor() as cursor:
                if selected_user == "Все":  # Параметр фильтрации "Все"
                    query = "SELECT wi.Время, ui.FIM_user FROM work_information wi JOIN user_information ui ON wi.Код = ui.uid"
                    cursor.execute(query)

                if selected_user == "Внутри":  # Параметр фильтрации "Внутри"
                    query = "SELECT FIM_user FROM user_information where Внутри = 1"
                    cursor.execute(query)

                if selected_user != "Все" and selected_user != "Внутри":  # Параметр фильтрации "*Пользователь*"
                    query = ("SELECT Время, Код FROM work_information "
                             "WHERE Код = (SELECT uid FROM user_information WHERE FIM_user = %s)"
                             "ORDER BY Время desc")
                    cursor.execute(query, (selected_user,))

                result = cursor.fetchall()
                if selected_user == "Внутри":
                    self.ui.statsTable.setRowCount(len(result))  # Устанавливаем количество строк
                    self.ui.statsTable.setColumnCount(1)
                    self.ui.statsTable.setHorizontalHeaderLabels(['Сейчас в здании общежития'])
                    for row_index, row_data in enumerate(result):
                        self.ui.statsTable.setItem(row_index, 0, QTableWidgetItem(str(row_data[0])))
                else:
                    self.ui.statsTable.setRowCount(len(result))  # Устанавливаем количество строк
                    self.ui.statsTable.setColumnCount(2)  # Устанавливаем количество столбцов
                    self.ui.statsTable.setHorizontalHeaderLabels(
                        ['Время', 'Пользователь'])  # Устанавливаем заголовки столбцов
                    for row_index, row_data in enumerate(result):
                        formatted_time = datetime.datetime.strptime(str(row_data[0]), "%Y-%m-%d %H:%M:%S").strftime(
                            "%d-%m-%Y %H:%M:%S")
                        self.ui.statsTable.setItem(row_index, 0, QTableWidgetItem(formatted_time))
                        self.ui.statsTable.setItem(row_index, 1, QTableWidgetItem(str(row_data[1])))

                self.ui.statsTable.resizeColumnsToContents()
        finally:
            connection.close()

    def load_data_to_combobox(self):
        connection = pymysql.connect(host='localhost', user='admin', password='123qwe!@#QWE',
                                     database='test')

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT FIM_user FROM user_information")
                result = cursor.fetchall()

                self.ui.comboBox.clear()  # Очистка ComboBox перед добавлением новых элементов

                for row in result:
                    self.ui.comboBox.addItem(row[0])  # Добавление элементов из базы в combobox

        finally:
            connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
