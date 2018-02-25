int sensorPin = A0;
int sensorValue;
int counter = 0;
String text = "";
void setup(){
pinMode(sensorPin,INPUT);
Serial.begin(57600);  // 115200  57600
}

void loop(){
/*
  if (counter == 100){
    Serial.println(text);
    text = "";
    counter = 0;
  }
 */
  sensorValue = analogRead(sensorPin); 
  Serial.println(sensorValue); 
  /*
  text = text + " " + String(sensorValue) ;
  counter+= 1;
  */
  delayMicroseconds(690);

}
