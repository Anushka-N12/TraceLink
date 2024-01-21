#include <WiFi.h>

#define LED_Y 4
#define LED_N 2

const int A1A = 18;//defining pin D18 for A1A
const int A1B = 5;//defining pin D5 for A1B
const int B1A = 21;//defining pin D21 for B1A
const int B1B = 19;//defining pin D19 for B1B

const char* ssid = "MDX welcomes you";
const char* password = "MdxL0vesyou";
//const char* ssid = "TP-Link_C036";
//const char* password = "30615526";

WiFiServer server(80);
void setup() {
  Serial.begin(115200);
  pinMode(LED_Y, OUTPUT);
  pinMode(LED_N, OUTPUT);
  digitalWrite(LED_Y, LOW);
  digitalWrite(LED_N, LOW);
  Serial.print("Connecting to the Network");
  WiFi.mode (WIFI_STA);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  server.begin();  // Starts the Server
  Serial.println("Server started");
  Serial.print("IP Address of network: ");
  Serial.println(WiFi.localIP());
  Serial.print("Copy and paste the following URL: http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");

  pinMode(B1A,OUTPUT);// defining pins as output
  pinMode(B1B,OUTPUT);
  
  pinMode(A1A,OUTPUT);
  pinMode(A1B,OUTPUT);    
  delay(3000);
}
void loop() {  
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  Serial.println("Waiting for new client");
  while (!client.available()) {
    delay(1);
  }
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
  if (request.indexOf("/LED=ON") == -1) {
    digitalWrite(LED_Y, HIGH);  // Turn ON LED
    delay(2000);
    digitalWrite(LED_Y, LOW); 
  }
  else if (request.indexOf("/LED=OFF") == -1) {
    digitalWrite(LED_N, HIGH); 
    delay(2000);
    digitalWrite(LED_N, LOW); 
  }
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
  motorA('L');// Turn motor A to LEFT
  motorB('R');// Turn motor B to RIGHT
  delay(500);
  motorA('S');// Turn motor A to RIGHT
  motorB('S');// Turn motor B to RIGHT
  delay(5000);
}

void motorA(char d)
{
  if(d =='R'){
    digitalWrite(A1A,LOW);
    digitalWrite(A1B,HIGH); 
  }else if (d =='L'){
    digitalWrite(A1A,HIGH);
    digitalWrite(A1B,LOW);    
  }else{
    //Robojax.com L9110 Motor Tutorial
    // Turn motor OFF
    digitalWrite(A1A,LOW);
    digitalWrite(A1B,LOW);    
  }
}// motorA end


/*
 * @motorB
 * activation rotation of motor B
 * d is the direction
 * R = Right
 * L = Left
 */
void motorB(char d)
{

    if(d =='R'){
      digitalWrite(B1A,LOW);
      digitalWrite(B1B,HIGH); 
    }else if(d =='L'){
      digitalWrite(B1A,HIGH);
      digitalWrite(B1B,LOW);    
    }else{
    //Robojax.com L9110 Motor Tutorial
    // Turn motor OFF      
      digitalWrite(B1A,LOW);
      digitalWrite(B1B,LOW);     
    }
}// motorB end 
