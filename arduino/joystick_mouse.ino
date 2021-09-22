int VRx = A0;
int VRy = A1;
int SW = A2;


void setup() {
  
  Serial.begin(38400);
}


int x, y, btn;
char inc = 0;

void loop() {
  x = analogRead(VRx);
  y = analogRead(VRy);
  btn = digitalRead(SW);
  
  // send joystick values to serial port
  Serial.print((int)inc);
  Serial.print(": ");
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(btn);
  inc++;
}
