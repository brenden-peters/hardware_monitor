#include <LiquidCrystal.h>
#include <SoftwareSerial.h>


//SoftwareSerial mySerial(0, 1); // RX, TX
LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
String Str1;
String Str2;
const int buttonPin = 2;
int button = 0;
char scratchPad[140];
int scrollDelay = 200;
int pageDelay = 2000;
char *st1, *st2, *st3, *st4, *st5, *st6;

void setup()
{
  pinMode(buttonPin, INPUT);
  lcd.begin(16, 2);
  writeToScreeny("System Monitor:", "Initializing");
  delay(1000);
  handshake();
}

void handshake()
{
  Serial.begin(115200);
  while (!Serial)
  {//wait for connection
  }
  while(Serial.available()<=0)
  {
    writeToScreeny("System Monitor:", "Connecting    "); delay(scrollDelay);
    writeToScreeny("System Monitor:", "Connecting.   "); delay(scrollDelay);
    writeToScreeny("System Monitor:", "Connecting..  "); delay(scrollDelay);
    writeToScreeny("System Monitor:", "Connecting... "); delay(scrollDelay);
    writeToScreeny("System Monitor:", "Connecting .. "); delay(scrollDelay);
    writeToScreeny("System Monitor:", "Connecting  . "); delay(scrollDelay);
  }
  lcd.clear();
  writeToScreeny("Connected!", "");
  lcd.clear();
}

void loop()
{
  lcd.clear();
  getSerialAboutIt();
  lcd.clear();
}

void getSerialAboutIt()
{
  int ind = 0;
  Serial.readBytesUntil('Z', scratchPad, 101);
  /*while (Serial.available())
  {
    char inputChar = (char)Serial.read();
    scratchPad[ind++] = inputChar;
  }*/
  //lcd.print(ind);
  //delay(1000);
  st1 = strtok(scratchPad, ",");
  st2 = strtok(NULL, ",");
  st3 = strtok(NULL, ",");
  st4 = strtok(NULL, ",");
  st5 = strtok(NULL, ",");
  st6 = strtok(NULL, ",");
  writeToScreeny(st1, st2);
  delay(pageDelay);
  writeToScreeny(st3, st4);
  delay(pageDelay);
  writeToScreeny(st5, st6);
  delay(pageDelay);
}

void writeToScreeny(String str1, String str2)
{
  lcd.clear();
  lcd.noAutoscroll();
  lcd.setCursor(0, 0);
  lcd.print(str1);
  lcd.setCursor(0,1);
  lcd.print(str2);
}



