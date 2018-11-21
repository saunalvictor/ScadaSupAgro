const int nb_pins = 12; // Number of pins to read

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available())
  {
    byte iRead = 0;
    iRead = Serial.read();
    if(iRead == 49)
    {
      String s = " ";
      for (int i = 0; i < nb_pins; i++)
      {
        s = s + analogRead(i) + " ";
      }
      s.trim();
      Serial.println(s);
    }
  }
}
