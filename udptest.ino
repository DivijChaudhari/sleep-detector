#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

int i;

boolean e_msg=false;

IPAddress ip(192,168,2,1);
IPAddress subnet(255,255,255,0);

WiFiUDP Udp;

void setup()
{
  Serial.begin(115200);
  
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(ip,ip,subnet);
  i=WiFi.softAP("divij","");
  
  //WiFi.mode(WIFI_STA);
  //WiFi.begin();
  Udp.begin(4210);
}

void loop()
{
  rmsg();
  if(Rec().equals("emergency"))
  {
    e_msg=true;
  }
}

void rmsg()
{
  i=Udp.parsePacket();
  if(i>0)
  {
    char rdata[i+1];
    Udp.read(rdata,i);
    rdata[i]='\0';
    Udp.beginPacket(Udp.remoteIP(),Udp.remotePort());
    if(e_msg)
    {
      Udp.write("emergency");
      e_msg=false;
    }
    else
    {
      Udp.write("no emergency");
    }
    Udp.endPacket();
  }
}

String Rec()
{
  String m="";
  char c='\0';
  while(Serial.available()>0)
  {
    delay(2);
    c=Serial.read();
    if(c=='\n'||c=='\r')
    {
      continue;
    }
    m+=c;
  }
  return m;
}
