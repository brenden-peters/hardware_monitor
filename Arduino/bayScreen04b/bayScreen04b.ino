#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
String Str1;
String Str2;
const int buttonPin = 2;
int button = 0;
char screenLine[16];
int scrollDelay = 200;
int pageDelay = 2000;

char scratchPad[320]; // screen is 16x2 characters long/tall, so this is 10 screens of text
char junkPile[320]; // junk buffer

// TODO: make gather realtime updates over serial, have flag and incrementing int
//       to decide what stats to display -- allow realtime graph, too

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
}

void loop()
{
  // flush serial cache so we get up-to-date info?
  //lcd.clear();
  Serial.flush();
  Serial.readBytesUntil('Z', junkPile, 320);
  /*while(Serial.peek() != "~") //while serial isn't "~"
  {
    Serial.read();
    // do dee do dee do
  }*/
  getSerialAboutIt();
  //lcd.clear();
}

void getSerialAboutIt()
{
  int x = Serial.readBytesUntil('Z', scratchPad, 320);
  //Serial.print(x); Serial.print(": ");
  //Serial.print(scratchPad);
  //Serial.print("\n");
  
  char* line;
  char* line2;
  line = strtok(scratchPad, ",");
  while(line)
  {
    line2 = strtok(NULL, ",");
    writeToScreeny(line, line2);
    //Serial.println(line);
    line = '\0';
    line2 = '\0';
    line = strtok(NULL, ",");
    delay(pageDelay);
  }
  for (int i = 0; i < 320; i++)
    {
      scratchPad[i] = '\0';
    }
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
