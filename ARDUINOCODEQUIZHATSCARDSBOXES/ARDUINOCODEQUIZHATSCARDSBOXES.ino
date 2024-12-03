const int thresholdA0 = 110; // Threshold for A0 True
const int thresholdA1 = 110; // Threshold for A1 False
const int generalThreshold = 250; // General threshold for other pins

const int numSensors = 10;
const int sensorPins[numSensors] = {A0, A1, A2, A3, A8, A9, A6, A5, A4, A7 };
int lastSensorValue[numSensors] = {0};
unsigned long lastSensorTime[numSensors] = {0};
const unsigned long debounceTime = 500; // Debounce time in milliseconds
const int relayPin = 2;

const unsigned long relayOnTime = 4 * 60 * 1000;  // 4 minutes
const unsigned long relayOffTime = 8 * 60 * 1000; // 8 minutes
unsigned long programStartTime;

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT); // set the relayPin to OUTPUT
  programStartTime = millis(); // save the time the program started
}

void loop() {
  for (int i = 0; i < numSensors; i++) {
    int sensorValue = analogRead(sensorPins[i]);
    int threshold;

    // Set threshold based on the pin
    if (sensorPins[i] == A0) {
      threshold = thresholdA0;
    } else if (sensorPins[i] == A1) {
      threshold = thresholdA1;
    } else {
      threshold = generalThreshold;
    }

    // Check if sensorValue is above threshold and if debounce time has passed
    if (sensorValue > threshold && millis() - lastSensorTime[i] > debounceTime) {
      Serial.println(i + 1);
      lastSensorTime[i] = millis();
    }
  }

  unsigned long elapsed = millis() - programStartTime;
  if (elapsed > relayOffTime) {
    digitalWrite(relayPin, HIGH); // turn the relay OFF after 8 minutes
  } else if (elapsed > relayOnTime) {
    digitalWrite(relayPin, LOW); // turn the relay ON after 4 minutes
  }
}
