# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:11:48 2016

@author: david.dorchies
"""

import logging
import threading
import time

class TES_JobScheduler():
    
    # Definition of jobs keys:LinuxTime, values:instruction    
    dJobs = {}
    # Answer of TES card
    sAns = ""    

    def __init__(self,dPrm):
        self.condAwake = threading.Condition()
        self.condAnswer = threading.Condition()
        self.dPrm = dPrm
        # Initialisation of Modbus communication
        if not "test" in self.dPrm or self.dPrm["test"]!="1":
            import minimalmodbus
            logging.info("Connecting to modbus hardware...")
            minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
            minimalmodbus.BAUDRATE = 9600
            minimalmodbus.PARITY = 'E'
            minimalmodbus.BYTESIZE = 8
            minimalmodbus.STOPBITS = 1
            #print minimalmodbus._getDiagnosticString()
            self.instr = minimalmodbus.Instrument('/'+dPrm['serial_port'], 1)
        else:
            logging.info("Testing without connection to modbus hardware")
    
    def RunNow(self,sInstruction):
        """
        Run an instaneous order
        @param sInstruction 
        """
        TimeStamp = time.time()
        return self.AddJob(TimeStamp,sInstruction)
    
    
    def AddJob(self,TimeStamp,sInstruction,bAsync=False):
        """ 
        Add a job to the queue
        @param TimeStamp Unix timestamp when the job should be run
        @param sInstruction the instruction
        @param bAsync Don't wait for an answer (asynchronous job)
        """
        self.dJobs[TimeStamp] = sInstruction
        logging.debug('dJobs[{}]={}'.format(TimeStamp,sInstruction))
        with self.condAwake:
            self.condAwake.notifyAll()
            if not bAsync:
                with self.condAnswer:
                    logging.debug("Waiting for answer")
                    self.condAnswer.wait()
                    return self.sAns


    def Start(self):
        """
        Daemon scheduler for interacting with TES card data acquisition
        @author David Dorchies
        @date 13/02/2016
        """
        logging.info('Starting TES_JobScheduler')
        while True:
            if not any(self.dJobs):
                # Nothing to do, waiting for the next job adding
                with self.condAwake:
                    logging.debug("Waiting for new job")
                    self.condAwake.wait(10)
                    logging.debug('Resource is available for new job')
            for TimeStamp, sInstruction in self.dJobs.items():
                if TimeStamp <= time.time():
                    self.sAns = self.RunJob(sInstruction)
                    if self.sAns != "":
                        self.condAnswer.notifyAll()
   
                 
    def RunJob(self,sInstruction):
        """ 
        Define which method beginning by "Order_" should be run for this job
        @param sInstruction String sent by the client to parse
        @return The value returned by the "Order_" method
        """
        sOrder,sArgs = sInstruction.split(" ")
        lArgs = sArgs.split(",")
        OrderMethodName = 'Order_' + sOrder
        OrderMethod = getattr(self, OrderMethodName, lambda: "nothing")
        return OrderMethod(lArgs)


    def Order_GET(self,lArgs):
        """
        Get data from a list of Registries
        @param lArgs List of Registry numbers
        @return If the data acquisition succeed: 
            a list of acquired raw data (String with space separator),
            a string beginning by "ERROR" else.
        """
        lD = []
        for Reg in lArgs:
            if not "test" in self.dPrm or self.dPrm["test"]!="1":
                try:
                    D=self.instr.read_register(int(Reg), 0)
                except IOError as e:
                    sErr="#{}: Reg #{} {}".format(Reg,e.errno, e.strerror)
                    logging.error("read_register "+sErr)
                    return "ERROR "+sErr
            else:
                time.sleep(0.1)
                import random
                D=random.random()*255
            lD.append(D)
        return " ".join(map(str,lD))


    def Order_SET(self,lArgs):
        """ 
        Define the value of a TOR output to ON during a specified time
        @param List containing:
            - Number of TOR Output to switch ON
            - Time in seconds of the switch ON
        @note Only one TOR output is switched ON at a time, if another TOR
            output is ON during this order, it will be switched OFF
        @return "OK" or a message beginning be "ERROR"
        """
        sReg,sTime = lArgs
        # Swich ON the TOR output
        if not "test" in self.dPrm or self.dPrm["test"]!="1":
            try:
                self.instr.read_register(int(sReg), 0)
            except IOError as e:
                sErr="#{}: Reg #{} {}".format(sReg,e.errno, e.strerror)
                logging.error("read_register "+sErr)
                return "ERROR "+sErr
        # Scheduling the Switch OFF
        TimeStamp = time.time()+float(sTime)
        self.AddJob(TimeStamp,"RESET "+sReg,True)
        return "OK"
        