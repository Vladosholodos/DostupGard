#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600); // Инициализация последовательного порта
  SPI.begin();       // Инициализация SPI-интерфейса
  mfrc522.PCD_Init(); // Инициализация RFID-считывателя
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return; // Проверка наличия карты
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    return; // Считывание серийного номера карты
  }

  // Получение UID метки
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : " ");
    uid += String(mfrc522.uid.uidByte[i], HEX);

    // Добавление пробела после каждого символа
    if (i != mfrc522.uid.size - 1) {
      uid += " ";
    }
  }
  uid.toUpperCase(); // Преобразование UID в верхний регистр

  // Удаление лишних пробелов
  uid.replace("  ", " "); // Замена двух пробелов одним

  // Отправка UID в последовательный порт
  Serial.println(uid);

  delay(3000); // Задержка 3 секунды перед следующей попыткой
}
