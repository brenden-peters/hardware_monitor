#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
String Str1;
String Str2;
const int buttonPin = 2;
int button = 0;
char threads[2];
int logiCoreCount = 0;
char screenLine[16];
int scrollDelay = 200;
int pageDelay = 2000;

float cpu[];
float freeRam;
float usedRam


void setup()
{
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
  // get proc count
  Serial.readBytesUntil('Z', threads,  2);
  logiCoreCount = (10*(threads[0] - 48)) + (threads[1] - 48); // convert 2 digit chars to proper int
}

void loop() {
  // put your main code here, to run repeatedly:

}

void writeToScreeny(String str1, String str2)
{
  lcd.clear();
  lcd.noAutoscroll();
  lcd.setCursor(0, 0);
  lcd.print(str1);
  lcd.setCursor(0,1);
  lcd.print(str2);
  //Serial.println(str1);
  //Serial.println(str2);
  // "CP1: 10, CP2: 33, CP3: 5, CP4: 87, RAM: 50MB, Disk: 40, Other Text: 007Z"
}
