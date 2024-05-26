#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("RFID система готова к работе!");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  //UID метки
  String content = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();


  if (content.substring(1) == "33 D1 0C F8") {
    Serial.println("33 D1 0C F8");
    // Добавьте здесь код для разрешения доступа (например, открытие замка)
  } else {
    Serial.println("Доступ запрещен!");
  }
  delay(3000);  // Ждем 3 секунды перед следующей попыткой
}
