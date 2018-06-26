#include <LiquidCrystal.h>
#include <SoftwareSerial.h>


//SoftwareSerial mySerial(0, 1); // RX, TX
LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
String Str1;
String Str2;
const int buttonPin = 2;
int button = 0;
char scratchPad[140];
char screenLine[16];
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
  // flush serial cache so we get up-to-date info?
  lcd.clear();
  Serial.flush();
  getSerialAboutIt();
  //getSerialChunk();
  lcd.clear();
}

void getSerialChunk()
{
  while (Serial.readBytesUntil(',', scratchPad, 101))
  {
    writeLineToScreen(scratchPad);
    for (int i = 0; i < 140; i++)
    {
      scratchPad[i] = '\0';
    }
    //scratchPad[0] = "\0";
    delay(pageDelay);
  }
  //writeLineToScreen(scratchPad); // gets the last chunk?
}

void getSerialAboutIt()
{
  int ind = 0;
  //Serial.readBytesUntil('Z', scratchPad, 101);
  //Serial.readBytesUntil('Z', scratchPad, 140); // << don't do; buffer too small. 
                                                 //    Instead: parse on the fly


                                                 // 16 chars wide screen
                                                 // read until returns 0 if can't

  while(Serial.readBytesUntil(',', screenLine, 16))
  {
    writeToScreeny(screenLine, "");
    for (int i = 0; i < 16; i++)
    {
      screenLine[i] = '\0';
    }
    delay(pageDelay);
  }
                                                 
  /*while (Serial.available())
  {
    char inputChar = (char)Serial.read();
    scratchPad[ind++] = inputChar;
  }*/
  //lcd.print(ind);
  //delay(1000);
/*
  // while loop here to capture stats regardless of how many cores
  while (st1 = strtok(scratchPad, ","))
  {
    //st2 = strtok(NULL, ",");
    writeToScreeny(st1, ""); //st2);

    // clear buffers here so it's not re-printing garbage
    for (int i = 0; i < 140; i++)
    {
      scratchPad[i] = '\0';
    }
    st1 = '\0';
    st2 = '\0';
    delay(pageDelay);
    
  }
  
  //st1 = strtok(scratchPad, ",");
  //st2 = strtok(NULL, ",");
  //st3 = strtok(NULL, ",");
  //st4 = strtok(NULL, ",");
  //st5 = strtok(NULL, ",");
  //st6 = strtok(NULL, ",");
  
  //writeToScreeny(st3, st4);
  //delay(pageDelay);
  //writeToScreeny(st5, st6);
  //delay(pageDelay);

 
  */
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

void writeLineToScreen(String str1)
{
  lcd.clear();
  lcd.noAutoscroll();
  lcd.setCursor(0, 0);
  lcd.print(str1);
}



