import processing.serial.*;
Serial myPort;


int numReadings = 10000; 
String sensorValue[] = new String[numReadings];
int readingCounter = 0; 
int file_num = 0;

String val;

void setup()
{
  String portName = Serial.list()[0]; 
  myPort = new Serial(this, portName, 57600); //aumentar los bauds.
}


void serialEvent(Serial myPort) {
  val = myPort.readStringUntil('\n');  
  if (val != null) { //cuando lleguen valores desde el serial.

    //val tiene caracteres "sucios" y hay que limpiarlos, pero si llamar a la funcion trim ralentiza el codigo, quitarla y ya filtraremos con Matlab.
    sensorValue[readingCounter] = trim(val);

    readingCounter++;
 
    if (readingCounter == numReadings)
    {
      saveStrings("file" + file_num + ".csv", sensorValue); //mirar si la funcion saveStrings sobreescribe el archivo o no.
      println("Actualizado."); //Para saber cuando se han volcado los datos.
      readingCounter = 0;
      file_num += 1;
    }
  } 
  
}


void draw()
{
}