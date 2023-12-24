import mysql
import serial
import pymysql


class DatabaseHandler:
    def __init__(self, db_host, db_user, db_password, db_name, arduino_port):
        self.connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        self.serial_port = serial.Serial(arduino_port, 9600)

        def check_access(self, uid):
            try:
                # Подключение к базе данных
                connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )

                if connection.is_connected():
                    cursor = connection.cursor()

                    # SQL-запрос для проверки доступа по UID метке
                    select_query = "SELECT COUNT(*) FROM authorized_users WHERE uid = %s"
                    cursor.execute(select_query, (uid,))

                    # Получаем результат запроса
                    count = cursor.fetchone()[0]

                    if count > 0:
                        print("Доступ разрешен")
                        return True
                    else:
                        print("Доступ запрещен")
                        return False

            except Error as e:
                print(f"Ошибка: {e}")
                return False

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Подключение к базе данных закрыто")
