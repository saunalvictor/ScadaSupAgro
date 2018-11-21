#include <Wire.h>
#include <UnoWiFiDevEd.h>


float ppt=400; //nombre de pas par tour
float ppb=8;
float avt=4;
float vit= 2.75; //vitesse de rotation en tr/s 
float delaylegnth=1000000/(ppt*vit); //delais entre chaque pas en micro 
float nbpt=ppt/avt/ppb; 
float nbb;
float h;
bool demi=0;
int pos=308;




void setup() {

 //establish motor direction toggle pins
  pinMode(12, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
  pinMode(13, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  
  //establish motor brake pins
  pinMode(9, OUTPUT); //brake (disable) CH A
  pinMode(8, OUTPUT); //brake (disable) CH B

  //initialisation wifi
 Wifi.begin();
 Wifi.println("Web Server is up");

 //butées, fin de course
  pinMode(5, INPUT);
  digitalWrite(5,HIGH); //permet de forcer le passage du pin à LOW avec un 0 "parfait"
  pinMode(6, INPUT);
  digitalWrite(6,HIGH);
 
}
void loop() {

 while(Wifi.available()){
 process(Wifi);  
 }
  
}

void process(WifiData client) {
 // read the command
 String command = client.readStringUntil('/');
 
 if (command == "digital") {
 motorCommand(client);
 }
}


void motorCommand(WifiData client) {

 // Read pin number
  h = client.parseFloat();

  pos=pos+h;
 
  if (h==1010){
    pos=308;
  }

  else if (pos>308){
    h=308-pos+h;
    pos=308;
    
  }

  else if (pos<0){
    h=-pos+h;
    pos=0; 
  }

  

 
  // Send feedback to client
 client.println("HTTP/1.1 200 OK");
 client.println("Content-Type: text/html");
 client.println();
 client.print(F("Ouverture: "));
 client.print(pos);
 client.print(F(" mm"));
 client.print(EOL); //char terminator

 nbb=h*nbpt;
  
//////////ouverture vanne////////////////

  if (nbb>0&&h!=1010){

/////////////////////////
  
    if(demi=0){ 
        
      for (int x=0;x<nbb;x++){
        
        if(digitalRead(6)==0){
          pas1();
          pas2();   
          pas3(); 
          pas4();
          pas5();
          pas6();
          pas7();
          pas8();  
          }  
                            
        }
       
      //si le nombre de boucle n'est pas entier faire 4 pas de plus (demi boucle)
      if ((int)(10*nbb)%10!=0&&digitalRead(6)==0){
        pas1();
        pas2();
        pas3();
        pas4();
        demi=!demi;
        }
        
      }
        
//////////////////////////////////////////

    else if (demi=1){
      
      for (int x=0;x<nbb;x++){
        
        if(digitalRead(6)==0){
          pas5();
          pas6();
          pas7();
          pas8();
          pas1();
          pas2();
          pas3();
          pas4();
          }

        }
  
      if ((int)(10*nbb)%10!=0&&digitalRead(6)==0){
        pas5();
        pas6();
        pas7();
        pas8(); 
        demi=!demi;
        }
               
      }

    }
    
////////////fermeture vanne/////////////////////

  if (nbb<0&&h!=1010){
    
////////////////////////////////
    
    if(demi=0){

      for (int x=0; x>nbb; x--){
          
        if(digitalRead(5)==0){
          pas7();  
          pas6();    
          pas5();    
          pas4();   
          pas3();
          pas2();
          pas1();
          pas8();
          } 
                          
        }
  
      //si le nombre de boucle n'est pas entier  (,5) faire 4 pas de plus (demi boucle)
      if (int(10*nbb)%10!=0&&digitalRead(5)==0){
        pas7();  
        pas6();    
        pas5();    
        pas4();
        demi=!demi;
        }
        
      }  

//////////////////////////////////////////

    else if(demi=1){
    
    for (int x=0; x>nbb; x--){
          
        if(digitalRead(5)==0){
          pas3();
          pas2();
          pas1();
          pas8();
          pas7();  
          pas6();    
          pas5();    
          pas4();
          }
    
       }
    
      if ((int)nbb%10!=0&&digitalRead(5)==0){
        pas3();
        pas2();
        pas1();
        pas8();
        demi=!demi;
        }
                 
    }

  }
  
////////////////////////////////////////////  

 else if (h==1010){

    //reinitialisation
    while(digitalRead(6)!=1){
      pas1();
      pas2();   
      pas3(); 
      pas4();
      pas5();
      pas6();
      pas7();
      pas8();
      }

    stopmotor();
    asm volatile ("  jmp 0"); 
    
  }

////////////////////////////////////////
  
  stopmotor();
    
}

/////////////////fonctions moteur///////////////

void pas1(){
  digitalWrite(9, LOW);  //ENABLE CH A
  digitalWrite(8, HIGH); //DISABLE CH B
  
  digitalWrite(12, HIGH);   //Sets direction of CH A
  analogWrite(3, 255);   //Moves CH A
  
  delayMicroseconds(delaylegnth);  
}

void pas2(){
  digitalWrite(9, LOW);  //ENABLE CH A
  digitalWrite(8, LOW); //ENABLE CH B
  
  digitalWrite(12, HIGH);   //Sets direction of CH A
  analogWrite(3, 255);   //Moves CH A
  digitalWrite(13, HIGH);   //Sets direction of CH B
  analogWrite(11, 255);   //Moves CH B
  
  delayMicroseconds(delaylegnth);
}

void pas3(){
  digitalWrite(9, HIGH);  //DISABLE CH A
  digitalWrite(8, LOW); //ENABLE CH B
  
  digitalWrite(13, HIGH);   //Sets direction of CH B
  analogWrite(11, 255);   //Moves CH B
  
  delayMicroseconds(delaylegnth);
}

void pas4(){
  digitalWrite(9, LOW);  //ENABLE CH A
  digitalWrite(8, LOW); //ENABLE CH B

  digitalWrite(12, LOW);   //Sets direction of CH A
  analogWrite(3, 255);   //Moves CH A
  digitalWrite(13, HIGH);   //Sets direction of CH B
  analogWrite(11, 255);   //Moves CH B

  delayMicroseconds(delaylegnth);  
}

void pas5(){
  digitalWrite(9, LOW);  //ENABLE CH A
  digitalWrite(8, HIGH); //DISABLE CH B
  
  digitalWrite(12, LOW);   //Sets direction of CH A
  analogWrite(3, 255);   //Moves CH A
  
  delayMicroseconds(delaylegnth);
}

void pas6(){
  digitalWrite(9, LOW);  //ENABLE CH A
  digitalWrite(8, LOW); //ENABLE CH B 

  digitalWrite(12, LOW);   //Sets direction of CH A
  analogWrite(3, 255);   //Moves CH A
  digitalWrite(13, LOW);   //Sets direction of CH B
  analogWrite(11, 255);   //Moves CH B

  delayMicroseconds(delaylegnth);
}

void pas7(){
  digitalWrite(9, HIGH);  //DISABLE CH A
  digitalWrite(8, LOW); //ENABLE CH B
  
  digitalWrite(13, LOW);   //Sets direction of CH B
  analogWrite(11, 255);   //Moves CH B
  
  delayMicroseconds(delaylegnth);  
}

void pas8(){
  digitalWrite(9, LOW);  //ENABLE CH A
  digitalWrite(8, LOW); //ENABLE CH B 

  digitalWrite(12, HIGH);   //Sets direction of CH A
  analogWrite(3, 255);   //Moves CH A
  digitalWrite(13, LOW);   //Sets direction of CH B
  analogWrite(11, 255);   //Moves CH B

  delayMicroseconds(delaylegnth);
}

void stopmotor (){
  analogWrite(11, 0); //coupe l'alim des broches  
  analogWrite(3, 0);  
  digitalWrite(9, HIGH); 
  digitalWrite(8, HIGH);  
}

