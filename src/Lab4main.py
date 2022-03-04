"""!
    @file main.py
    @brief Runs main logic and loops through running ADC stuff.
    @details This lab uses an RC circut that connects Pin C1 and C0 and records the voltage responce.
    @author Rodi Diaz
    @author Daniel Munic
    @author John Bennett
    @date Febuary 12, 2022   
"""
import pyb
import utime
import task_share

def isr_fun(dum):
    '''!@brief functun ran on Interrupt service routine.
        @details Everytime the service routine is called, it appends the current ADC
                value into a queue.
        @param dum is an unused callback variable.
    '''    
    myQueue.put(myadc.read())

if __name__ == "__main__":
    '''! @brief ADC Step Response recording.
         @details Sets a pin on the board into an output with a frequency of 1000
                  Set the output to high in order to see th esetp response.
                  Record the ADC value and put them into the queue for 1000 interations.
                  Once all the values have been recorded, print the value as well as the percent.
    '''
    ## Pin C1 is an output voltage pin
    pinC1 = pyb.Pin(pyb.Pin.cpu.C1, mode=pyb.Pin.OUT_PP)
    ## Pin C0 is will be used as our ADC object
    pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
    ## timer 1 will be ran every 1 ms
    tim1 = pyb.Timer(1, freq = 1000)
    
    ## myQueue stores up to 1000 ADC readings
    myQueue = task_share.Queue("h", 1000, name="Jonathan")
    
    ## myadc is an adc object that reads voltage outputs
    myadc = pyb.ADC(pinC0)
    
    while True:
        input("ready to start hit anything:")
        pinC1.high()
        
        tim1.callback(isr_fun)
        utime.sleep(1)
        tim1.callback(None)
        
        pinC1.low()
        
        print("#START#")
        for i in range(999):
            print(str(myQueue.get()) + "," + str(i * 0.001))
        myQueue.clear()
        print("#STOP#")
        