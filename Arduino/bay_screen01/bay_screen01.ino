#include <LiquidCrystal.h>
#include <SoftwareSerial.h>


//SoftwareSerial mySerial(0, 1); // RX, TX
LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
String Str1;
String Str2;

void setup()
{
  lcd.begin(16, 2);
  writeToScreen("LCD Bay: Initializing");
  delay(500);
  lcd.clear();
}

void loop()
{
  writeToScreen("System info here");
  delay(1000);
  writeToScreen("butts butts butt");
  delay(1000);
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
      delay(200);
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
}


