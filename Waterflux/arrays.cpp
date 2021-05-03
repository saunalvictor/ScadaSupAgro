/*
 *  Arrays library
 * 
 *  Functions for arrays
 * 
 *  Alexi Husson
 *  18/04/2019
 */

#include <Arduino.h>


void decal(float a,float* tab, int sizeTab){
  for (int i = sizeTab-1; i > 0; i--){
    tab[i] = tab[i-1];
  }
  tab[0] = a;
}

float mean(float* tab, int sizeTab){
  float count = 0;
  for(int i=0; i<sizeTab; i++){
    count+=tab[i];
  }
  return count/sizeTab;
}

void printTab(float* tab, int sizeTab){
    for(int i=0; i<sizeTab; i++){
        Serial.println("Tab["+String(i)+"] = "+String(tab[i]));
    }
}
