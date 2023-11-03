
void setup()
{
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(A0, INPUT);
  Serial.begin(9600);
  Serial.println("Rohit Luni");
  Serial.println("========================");

}

void loop()
{
  
  int moisture_value = analogRead(A0);
  
  Serial.println(moisture_value);
  
  if(moisture_value > 500) 
  {
     Serial.println("Motor is ON");
     digitalWrite(7, HIGH);
     digitalWrite(8, HIGH);
  }
  else 
  {
     Serial.println("Motor is OFF");
     digitalWrite(7, LOW);
     digitalWrite(8, LOW);
  }
  
  delay(1000);
}