//mysql 연결관련 헤더
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>

#include <ESP8266WiFi.h> //와이파이
#include <stdio.h>




//wifi 정보
const char* ssid = "aischool class03(5Ghz)";
const char* password = "gjaischool";

//sql 연결셋팅부
//IPAddress server_addr(192, 168, 100, 19); // I여기에 IP를 넣어주세요
char hostname[] = "project-db-stu3.smhrd.com"; // 도메인 주소가 있다면 넣어주세요  !! 둘중 하나만 사용해야합니다!
char user[] = "Insa4_IOTA_hacksim_1"; //계정정보 ID입니다
char password_[] = "aishcool1";        // DB password입니다

WiFiClient client;
MySQL_Connection conn(&client);
MySQL_Cursor* cursor;

char INSERT_SQL[] = "INSERT INTO test_arduino.hello_arduino (Sensor_ID,Temp_Values) VALUES ("S001",24)"; //실제 넣어줄 쿼리문입니다
char SensorId[] = "S0001";

void setup() {
  Serial.begin(115200); //전송속도

  Wifi_connect(); //와이파이 연결

  setupDateTime();//시간설정

  Serial.print("Connecting to SQL...  ");
  if (conn.connect(server_addr, 3307, user, password_)) {
    Serial.println("OK.");
  }
  else {
    Serial.println("FAILED.");
  }
  // create MySQL cursor object
  cursor = new MySQL_Cursor(&conn);
  
}


void loop() {
  
  if (WiFi.status() != WL_CONNECTED) { //와이파이 연결이 이상할시에 재접속 하는 코드
    Serial.println("try reconnect");
    Wifi_connect();
  }

  sprintf(INSERT_SQL,"INSERT INTO Insa4_IOTA_hacksim_1.temp (Sensor_ID,Temp_Value VALUES (SensorId,%d)", 24); //쿼리문 온습도
 
  if (conn.connected()) {
    cursor->execute(INSERT_SQL); //실제 excute되는 시점
  }

  delay(300000);

}




void Wifi_connect() {

  Serial.println("---------------------------------------");
  Serial.println(ssid);
  WiFi.begin(ssid, password); // 와이파이 이름과 비밀번호를 통해 WIFI연결을 시작 // WL_CONNECTED라는 값을 돌려준다
  while (WiFi.status() != WL_CONNECTED) {
    // 네트워크의 연결 상태, 8개의 리턴값
    // STATUS와 WL_CONNECTED 값이 같은지를 통해 제대로 연결이 되있는지를 확인할 수 있다
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wifi connected!");
  Serial.println("\nConnected to network");
  Serial.print("My IP address is: ");
  Serial.println(WiFi.localIP());
}
