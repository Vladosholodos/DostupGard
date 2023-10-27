import serial
import pymysql


class DatabaseHandler:
    def __init__(self, db_host, db_user, db_password, db_name, arduino_port):
        self.connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        self.serial_port = serial.Serial(arduino_port, 9600)

    def check_access(self, uid):
        with self.connection.cursor() as cursor:
            sql = f"SELECT * FROM authorized_users WHERE uid='{uid}'"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False

    def send_to_arduino(self, message):
        self.serial_port.write(message.encode())

    def close_connection(self):
        self.connection.close()
        self.serial_port.close()
