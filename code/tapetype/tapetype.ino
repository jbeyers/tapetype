#include <Servo.h> 

// Create the servo objects
Servo servox;

bool ping = false; // Timing sensor latch
bool go = false; // Enable motor and printing
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
  digitalWrite(dir_out, HIGH);
} 

void loop() { 
    // Got this bit off the internet from a basic serial to servo tutorial.
    if (Serial.available()) {
        pos_byte = Serial.readStringUntil('\n'); // read data until newline
        pos = pos_byte.toInt();   // change datatype from string to integer        
        if (pos == 0) {
          go = false;
        } else if (pos > 180) {
          go = true;
        } else {
          servox.write(pos); // move servo
        }
    }
    // Create a debounced single trigger from the timing switch and send a
    // serial timing message.
    current = millis();
    if ( digitalRead(13)) {
        high = current;
        if (current - low > 50 && ping) {
            ping = false;
            Serial.println('p');
        }
    } else {
        low = current;
        if (current - high > 50 && !ping) {
            ping = true;
        }
    }
  // Control the stepper motor. Very rough, but good enough. The delays were
  // manually tuned together with the microstepping settings, using the TLAR
  // (That Looks About Right) method.
  if (go) {
      digitalWrite(disable_out, LOW);
      delay(3);
      digitalWrite(step_out, HIGH);
      delay(3);
      digitalWrite(step_out, LOW);
    } else {
      digitalWrite(disable_out, HIGH);
    }
}
