/*
    This sketch sends a string to a TCP server, and prints a one-line response.
    You must run a TCP server in your local network.
    For example, on Linux you can use this command: nc -v -l 3000
*/

#include <string.h>
#include <Servo.h>

Servo servo;  // create servo object to control a servo

// pins
#define servo_pin 4

void setup() {
  Serial.begin(115200);

  servo.attach(servo_pin);
  servo.write(0);  
}

void loop() {
    String line = Serial.readStringUntil('\r');
    Serial.println(line);
    if (line.length()>0 && line.charAt(0)=='c' && line.charAt(1)=='m' && line.charAt(2)=='d' && line.charAt(3)=='=' && !(line == "None" || line == "none")){
      int cord = 90;
      String cmd = "";
      for(int i=4; i<line.length()+1; i++){
        if (char_is_digit(line.charAt(i))){
          cmd += line.charAt(i);
        }else{
           cord = cmd.toInt();
          cmd = "";
        }
      }
      Serial.println(String(cord));
      servo.write(cord);
    }
}

bool char_is_digit(char c){
  if (c > 47 && c < 58){ //ASCII codes
    return true;
  }else{
    return false;
  }
}
