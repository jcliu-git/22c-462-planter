#include <EEPROM.h>

// serial states
#define S_WAIT 0
#define S_START 1
#define S_READ 2

// serial command message types
#define NULL_MSG 0
#define PLANTER_SET_MSG 1
#define HYDRO_SET_MSG 2
#define DRY_THRESHOLD_MSG 3
#define FLOW_TIME_MSG 4
#define MEASURE_MSG 5

// settings EEPROM locations
#define PLANTER_ENABLE 0
#define HYDRO_ENABLE 1
#define DRY_THRESHOLD 2
#define FLOW_TIME 4

// pumping settings variables
bool planter_enable = false;
bool hydro_enable = false;
short dry_threshold = 480;
long flow_time = 500;

// pump control state vars
bool pump_actives[] = {false, false, false, false};
unsigned long pump_starts[] = {0,0,0,0};

unsigned long start = 0;

void setup() {
  Serial1.begin(9600);
  Serial.begin(9600); // debug port
  digitalWrite(0, LOW); // disable RX pullup to avoid damaging PI
  EEPROM.get(0, planter_enable);
  EEPROM.get(1, hydro_enable);
  EEPROM.get(2, dry_threshold);
  EEPROM.get(4, flow_time);
  
  // debugging print
  Serial.print("P: ");
  Serial.print(planter_enable);
  Serial.print(" H: ");
  Serial.print(hydro_enable);
  Serial.print(" D: ");
  Serial.print(dry_threshold);  
  Serial.print(" F: ");
  Serial.println(flow_time);
  
  pinMode(2, OUTPUT);
  digitalWrite(2, hydro_enable ? HIGH : LOW); // set hydroponics pump

  // initialize planter pumps and set low
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  pinMode(5, OUTPUT);
  digitalWrite(5, LOW);
  pinMode(6, OUTPUT);
  digitalWrite(6, LOW);

  unsigned long start = millis();  
}

// serial state vars
byte current_state = S_WAIT;
byte current_type = NULL_MSG;
unsigned char* msg_buf = nullptr;
size_t msg_counter = 0;

void loop() { 
  // update hydroponics pump
  digitalWrite(2, hydro_enable ? HIGH : LOW);

  // update planter pumps
  updatePump(0, A0, 3);
  updatePump(1, A1, 4);
  updatePump(2, A2, 5);
  updatePump(3, A3, 6);  
  
  // serial handling state machine
  if (Serial1.available() > 0) {
    // read a byte
    byte rbyte[1];
    Serial1.readBytes(rbyte, 1);        
    
    // act on byte based on current serial state
    switch (current_state) {
      case S_WAIT:
      if(rbyte[0] == 255) {
        current_state = S_START;
      }      
      break;
      case S_START:
      if(rbyte[0] > 0 && rbyte[0] <= 5) {
        current_type = rbyte[0];
        msg_buf = new unsigned char[getContentSizeForType(current_type)];
        current_state = S_READ;
      }
      else {
        Serial1.println("Invalid type received");
        current_state = S_WAIT;
      }
      break;
      case S_READ:
      if(msg_counter < getContentSizeForType(current_type)) {
        msg_buf[msg_counter] = rbyte[0];
        msg_counter++;
      }
      else if(rbyte[0] == xorCksm(msg_buf, getContentSizeForType(current_type))) {
        if(current_type == PLANTER_SET_MSG) {
          bool value = (bool)msg_buf[0];
          planter_enable = value;
          EEPROM.put(PLANTER_ENABLE, value);
          unsigned char response[] = {255, current_type, msg_buf[0], rbyte[0]};
          Serial1.write(response, 4);
        }
        else if(current_type == HYDRO_SET_MSG) {
          bool value = (bool)msg_buf[0];
          hydro_enable = value;          
          EEPROM.put(HYDRO_ENABLE, value);
          unsigned char response[] = {255, current_type, msg_buf[0], rbyte[0]};
          Serial1.write(response, 4);                  
        }
        else if(current_type == DRY_THRESHOLD_MSG) {
          unsigned short value = bytesToShort(msg_buf);
          dry_threshold = value;                    
          EEPROM.put(DRY_THRESHOLD, value);
          unsigned char response[] = {255, current_type, msg_buf[0], msg_buf[1], rbyte[0]};
          Serial1.write(response, 5);                 
        }        
        else if(current_type == FLOW_TIME_MSG) {
          unsigned long value = bytesToLong(msg_buf);
          flow_time = value;          
          EEPROM.put(FLOW_TIME, value);
          unsigned char response[] = {255, current_type, msg_buf[0], msg_buf[1], msg_buf[2], msg_buf[3], rbyte[0]};
          Serial1.write(response, 7);             
        }
        else if(current_type == MEASURE_MSG) {
          unsigned short readings[] = {analogRead(A0), analogRead(A1), analogRead(A2), analogRead(A3),
                                       analogRead(A4), analogRead(A5), analogRead(A6), analogRead(A7)};
  
          // convert to array of bytes                                                                    
          unsigned char response[17];                                       
          for(size_t i = 0; i < 8; i++) {
            if(readings[i] < 255) {
              response[i*2] = 0;
              response[i*2 + 1] = readings[i];
            }
            else {                         
              response[i*2] = readings[i] / 256;
              response[i*2 + 1] = readings[i] % 256;              
            }            
          }
          response[16] = xorCksm(response, 16); // append checksum       
          Serial1.write(response, 17);
        }
             
        current_type = NULL_MSG;
        delete msg_buf;
        msg_buf = nullptr;
        msg_counter = 0;
        current_state = S_WAIT;
      }
      else {
        Serial1.println("Invalid message content");
        current_type = NULL_MSG;
        delete msg_buf;
        msg_buf = nullptr;
        msg_counter = 0;
        current_state = S_WAIT;
      }
      break;
    }
  }
}

size_t getContentSizeForType(byte tbyte) {
  switch(tbyte) {
    case PLANTER_SET_MSG:
    return 1;
    case HYDRO_SET_MSG:
    return 1;
    case DRY_THRESHOLD_MSG:
    return 2;
    case FLOW_TIME_MSG:
    return 4;
    case MEASURE_MSG:
    return 1;
  }
}

byte xorCksm(unsigned char* buf, size_t size) {
  byte rolling_xor = 0;
  for(int i = 0; i < size; i++) {
    rolling_xor ^= buf[i];
  }
  return rolling_xor;
}

unsigned short bytesToShort(unsigned char* buf) {
  return buf[0] * 0x100u + buf[1];
}

unsigned long bytesToLong(unsigned char* buf) {
  return buf[0] * 0x10000u + buf[1] * 0x1000u + buf[2] * 0x100u + buf[3];
}

void updatePump(size_t pump_no, byte sensor_pin_no, byte pump_pin_no) {
  // pump active state
  if(pump_actives[pump_no]) {
    if(!planter_enable) {
      digitalWrite(pump_pin_no, LOW);      
      pump_actives[pump_no] = false;            
    }
    else if(millis() - pump_starts[pump_no] > flow_time*2) {
      pump_actives[pump_no] = false;     
    }
    else if(millis() - pump_starts[pump_no] > flow_time) {
      digitalWrite(pump_pin_no, LOW);
    }    
  }
  
  // pump inactive state  
  else if(planter_enable && (analogRead(sensor_pin_no) > dry_threshold)) { 
    digitalWrite(pump_pin_no, HIGH);
    pump_starts[pump_no] = millis();
    pump_actives[pump_no] = true;    
  }
}
