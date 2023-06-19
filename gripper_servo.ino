#include <Servo.h>
Servo gripper;
char message;
void setup() {
  Serial.begin(9600);
  gripper.attach(9);
  gripper.write(0);
}

void loop() {
  if (Serial.available()) {
    message = Serial.read();
  }
  if (message == 'P'){
    gripper.write(95);
  }
  else if (message == 'R'){
    gripper.write(60);
  }
  else if (message == 'B')
    gripper.write(80);
  else if (message == 'K')
    gripper.write(70); //60
  else if (message == 'Q')
    gripper.write(60); //70
  else if (message == 'H')
    gripper.write(110);
  else if (message == 'L'){
    gripper.write(0);
  }
}
