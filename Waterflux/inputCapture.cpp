/*
 *  InputCapture
 * 
 *  Functions for mesure of PWM
 *  Needs interruptions enabled
 * 
 *  Alexi Husson
 *  18/04/2019
 */


#include <Arduino.h>
#include "inputCapture.h"

int pin;
volatile unsigned long prev_time;
volatile double period;

void captureInit(int p){
  pin = p;
  attachInterrupt(pin, rising, RISING);
}

double getFreq(){

  return 1/(period/1000000);
}

void rising() {  
  attachInterrupt(pin, rising2, RISING);
  prev_time = micros();
}

void rising2() {
  attachInterrupt(pin, rising, RISING);
  period = micros()-prev_time;
}
