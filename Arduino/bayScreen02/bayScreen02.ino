#include <LiquidCrystal.h>
#include <SoftwareSerial.h>


//SoftwareSerial mySerial(0, 1); // RX, TX
LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
String Str1;
String Str2;
String scratchPad;
int scrollDelay = 500;

void setup()
{
  lcd.begin(16, 2);
  writeToScreen("LCD Bay: Initializing");
  delay(500);
  handshake();
}

void handshake()
{
  Serial.begin(115200);
  //Serial.begin(9600);
  while (!Serial)
  {//wait for connection
  }
  while(Serial.available()<=0)
  {
    //Serial.print('z');
    //delay(300);
  }
  lcd.clear();
  writeToScreen("Connected!");
}

void loop()
{
  getSerialAboutIt();
  writeToScreen(scratchPad);
  //writeToScreen("Hello");
  delay(500);
  // delay(scrollDelay);
}

void getSerialAboutIt()
{
  scratchPad = "";
  while (Serial.available())
  {
    char inputChar = (char)Serial.read();
    scratchPad += inputChar;
    //if (inputChar == '\n') //scrub newline from stream
    //{
    //  // end of stream, mightn't need this
    //}
  }
  Serial.print(scratchPad);
  //writeToScreen(scratchPad);
}

void writeToScreen(String str)
{
  lcd.clear();
  lcd.noAutoscroll();
  lcd.setCursor(0, 0);
  int strSize = str.length();
  lcd.setCursor(16, 0);
  if(strSize > 24)
  {
    lcd.autoscroll();
    for (int i = 0; i < strSize; i++)
    {
      //lcd.print(i);
      lcd.print(str.charAt(i));
      delay(scrollDelay);
    }
  }
  else
  {
    Str1 = str.substring(0, 16);
    Str2 = str.substring(16, 32);
    lcd.setCursor(0, 0);
    lcd.print(Str1);
    lcd.setCursor(0, 1);
    lcd.print(Str2); 
  }
  lcd.noAutoscroll();
  Serial.println("Done writing to screen.");
}


