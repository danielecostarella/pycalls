void setup() {
  Serial.begin(9600);
  Serial.println("Starting...");
}

void loop() {
  delay(random(20000, 50000));  // Wait for a random amount of time before sending the next message

  if (random(2) == 0) {  // Send RING with 50% probability
    Serial.println("RING");
    delay(500);
  } else {  // Send TIME, DATE, and NMBR in order
    Serial.print("TIME = ");
    Serial.println(get_time());
    Serial.print("DATE = ");
    Serial.println(get_date());
    Serial.print("NMBR = ");
    Serial.println(get_number());
  }
}

String get_time() {
  String hour = String(random(0, 24));
  String minute = String(random(0, 60));
  String second = String(random(0, 60));
  return hour + ":" + minute + ":" + second;
}

String get_date() {
  String day = String(random(1, 32));
  String month = String(random(1, 13));
  String year = String(random(2020, 2030));
  return day + "/" + month + "/" + year;
}

String get_number() {
  String number = "";
  for (int i = 0; i < 10; i++) {
    number += String(random(0, 10));
  }
  return number;
}
