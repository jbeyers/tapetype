#include <Servo.h> 

// Create the servo objects
Servo servox;

bool ping = false; // Timing sensor latch
String pos_byte;
int pos;
unsigned long low;
unsigned long high;
unsigned long current;

const int step_out = 3;
const int dir_out = 4;
const int disable_out = 5;
const int start_in = 2;

void setup() { 
  servox.attach(6);  // Attach the servo
  pinMode(13, INPUT_PULLUP); // Timing switch
  Serial.begin(9600);
  // Start toggle.
  pinMode(start_in, INPUT_PULLUP);
  // Stepper driver controls
  pinMode(step_out, OUTPUT);
  pinMode(dir_out, OUTPUT);
  pinMode(disable_out, OUTPUT);
  digitalWrite(disable_out, HIGH);
} 

void loop() { 
    // Got this bit off the internet from a basic serial to servo tutorial.
    if (Serial.available()) {
        pos_byte = Serial.readStringUntil('\n'); // read data until newline
        pos = pos_byte.toInt();   // change datatype from string to integer        
        servox.write(pos); // move servo
    }
    // Create a debounced single trigger from the timing switch and send a
    // serial timing message.
    current = millis();
    if ( digitalRead(13)) {
        high = current;
        if (current - low > 50 && ping) {
            ping = false;
        }
    } else {
        low = current;
        if (current - high > 50 && !ping) {
            ping = true;
            Serial.println('p');
        }
    }
  // Control the stepper motor. Very rough, but good enough. The delays were
  // manually tuned together with the microstepping settings, using the TLAR
  // (That Looks About Right) method.
  if (digitalRead(start_in) == LOW) {
      digitalWrite(disable_out, LOW);
      digitalWrite(dir_out, HIGH);
      delay(2);
      digitalWrite(step_out, HIGH);
      delay(2);
      digitalWrite(step_out, LOW);
    } else {
      digitalWrite(disable_out, HIGH);
    }
}
