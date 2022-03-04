'''!
    @file Encoder.py
    @brief Creates and recieves encoder data from the moter
    @details The encoders used in reading positions from motors 1 and 2
            can read position, update position and zero position
    @author Rodolfo Diaz
    @author Daniel Munic
    @author John Bennett
    @date January 11, 2022    
'''
import pyb
import math

## @brief Encoder_Period the value/ period of ticks before the encoder overflows
Encoder_Period = 2**16
Ticks_Per_Revolution = 16384

def to_radians(ticks):
        return (float(ticks) / Ticks_Per_Revolution) * 2 * math.pi 

class Encoder:
    '''!@brief An Encoder class implements a motor driver for an ME405 kit.
        @details Objects of this class can be used to read encoder data based
                on the position of a given DC motor.
    '''
    def __init__(self, pinCH1, pinCH2, timerNum):
        '''!@brief Initializes and creates a encoder object.
            @details Creates timer channels that will be used to track the motors position through the encoder.
            @param pinCH1 First pin for configuring encoder.
            @param pinCH2 Second pin for configuring encoder.
            @param timerNum Timer Assosiated with the pins.
        '''
        ## @brief timer object for counting encoder ticks
        self.timer = pyb.Timer(timerNum, prescaler=0, period=Encoder_Period-1)
        self.timer.channel(1, mode=pyb.Timer.ENC_AB, pin=pinCH1)
        self.timer.channel(2, mode=pyb.Timer.ENC_AB, pin=pinCH2)

        ## @brief unbounded position, corresponds to timer_counter unless there is overflow/underflow
        self.position = self.timer.counter()
        ## @brief bounded position, corresponds to timer_counter reseting to zero every Encoder Period
        self.Eposition = self.timer.counter()

    def zero(self):
        '''!@brief Zeros the position and the encoder position.
        '''
        self.timer.counter(0)
        self.Eposition = self.timer.counter()
        self.position = self.timer.counter()
        

    def read_ticks(self):
        '''!@brief This function is called when we want to read the current motor position.
            @return Current encoder position.
        '''
        return self.position

    def read(self):
        '''!@brief This function is called when we want to read the current motor position in radians.
            @return Current encoder position in radians.
        '''
        return to_radians(self.read_ticks())

    def updatePosition(self):
        '''!@brief This function updates the current position.
            @details It uses the current encoder position and the previous encoder position
                    the calculate the delta to add to the unbounded position value while keeping
                    track of over flows.
        '''
        delta = self.timer.counter() - self.Eposition
        self.Eposition = self.timer.counter()
        #Fix Overflow
        if delta > Encoder_Period / 2:
            delta = delta - Encoder_Period

        #Fix Underflow
        elif delta < -(Encoder_Period / 2):
            delta = delta + Encoder_Period

        self.position = self.position + delta

#testing
#import utime
#if __name__ == '__main__':
#    pinCH1 = pyb.Pin.cpu.B6
#    pinCH2 = pyb.Pin.cpu.B7
#
#    myEncoder = Encoder(pinCH1, pinCH2, 4)
#
#    while True:
#        utime.sleep(.5)
#        myEncoder.updatePosition()
#        print(myEncoder.read())
