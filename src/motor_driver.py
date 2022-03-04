'''!
    @file motor_driver.py
    @brief Creates and sends motors as dutys
    @details The motor driver L6206 is used for controling motors 1 and 2
            using functions to enable, disable, and set duty
    @author Rodolfo Diaz
    @author Daniel Munic
    @author John Bennett
    @date January 11, 2022    
'''
import pyb

class Motor_Driver:
    '''!@brief A motor class implements a motor driver for an ME405 kit.
        @details Objects of this class can be used to apply PWM to a given
                 DC motor.
    '''
    def __init__ (self,pinCH1,pinCH2,timX,pinEN):
        '''!@brief Initializes and creates a motor object.
            @details Creates timer channels that will be used specific to each motor channel to control motor function.
            @param motorChannel moter driver channel
            @param pinCH1 First pin for configuring motor
            @param pinCH2 Second pin for configuring motor
            @param timX Timer Assosiated with Pins
            @param pinEN the Enable Pin for the L6206
        '''
        ## @brief Timer channel to the first motor channel
        self.t2c1 = timX.channel(1, mode = pyb.Timer.PWM, pin=pinCH1)
        ## @brief Timer channel to the second motor channel
        self.t2c2 = timX.channel(2, mode = pyb.Timer.PWM, pin=pinCH2)
        ## @brief Enable pin
        self.pinEN = pinEN
        
        self.enable()
        
    def set_duty (self, duty):
        '''!@brief Set the PWM duty cycle for the motor channel.
            @details This method sets the duty cycle to the motor to the given level. Positive values
                    cause effort in one direction, negative values
                    in the opposite direction.
            @param Duty A signed number between -100 and 100 representing the duty
                      cycle of the PWM signal sent to the motor.
        '''
        #if duty is positive then set the first channel to specified duty and other to 0.
        if duty >= 0:
            if duty <= 100:
                self.t2c1.pulse_width_percent(100)
                self.t2c2.pulse_width_percent(100-duty)
            else:
                self.t2c1.pulse_width_percent(100)
                self.t2c2.pulse_width_percent(0)
        #if duty is negative then set the second channel to a specified duty (negative sign will make duty positive) and other to 0.
        elif duty < 0:
            if duty >= -100:
                self.t2c2.pulse_width_percent(100)
                self.t2c1.pulse_width_percent(100+duty)
            else:
                self.t2c2.pulse_width_percent(100)
                self.t2c1.pulse_width_percent(0)
    
    def enable(self):
        '''!@brief Initiates motor by switching the enable pin to high
        '''
        self.pinEN.high()
    
    def disable(self):
        '''!@brief Deinitiates motor by switching the enable pin to low and sets duty to zero 
        '''
        self.set_duty(0)
        self.pinEN.low()


import utime
if __name__ == '__main__':
    tim3 = pyb.Timer(3, freq = 20000)
    pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
    pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
    pinENA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    print('run')
    
    # motor 2
    tim5 = pyb.Timer(5, freq = 20000)
    pinA0 = pyb.Pin(pyb.Pin.cpu.A0)
    pinA1 = pyb.Pin(pyb.Pin.cpu.A1)
    pinENB = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 2 object
    
    
    motor1 = Motor_Driver(pinB4, pinB5, tim3, pinENA)
    motor1.set_duty(50)
    utime.sleep(2)
    motor1.set_duty(-100)
    utime.sleep(2)
    motor1.set_duty(0)
    
    motor2 = Motor_Driver(pinA0, pinA1, tim5, pinENB)
    motor2.set_duty(50)
    utime.sleep(2)
    motor2.set_duty(-100)
    utime.sleep(2)
    motor2.set_duty(0)
    