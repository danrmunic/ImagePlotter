'''!
    @file closedloop.py
    @brief Closed loop controller containing methods to control an arbitraries motor duty cycle
    @details Controller uses the difference of reference and current values to create an error variable. the time 
             difference, and magnitude of error are then used in the update method to return a duty for the motor to be run.
    @author John Bennett
    @author Daniel Munic
    @author Rodolfo Diaz
    @date   January 25, 2022
'''

import utime
import array

class ClosedLoop:
    '''!@brief                  Interface with closed loop controller
        @details                Contains all methods that will be used in task_hardware to set the duty cycle based on closed
                                loop control.
    '''
        
    def __init__ (self, Kp, setpoint = 0, Ki = 0, Kd = 0, satLim = [-100,100]):
        '''!@brief Constructs a closed loop controller
            @details Sets up a PID controler, a set point and the saturation limits for a given controller.
            @param Kp is the proportional gain in the PID controller.
            @param setpoint is the goal set point of the controller. If none is specified setpoint = 0.
            @param Ki is the integral gain in the PID controller. If none is spesified Ki = 0.
            @param Kd is the derivative gain in the PID controller. If none is spesified Kd = 0.
            @param satLim is a list containing the upper and lower bounds of the saturation limit. If none is spesified satLim is between -100 and 100. 
        '''
        ## Kp is the proportional gain
        self.Kp = Kp
        ## Kd is the derivitive gain
        self.Kd = Kd
        ## Kd is the integral gain
        self.Ki = Ki
        ## Setpoint is the goal point, the point which the motors attempts to reach
        self.setpoint = setpoint
        ## Instantiates duty saturation upper and lower limits
        self.satLim = satLim
        ## Sum of error over a difference in time
        self.esum = 0
        ## Previous error
        self.laste = 0
        ## A counter using ms
        self.Time = utime.ticks_ms
        ## A value that keeps the current time
        self.to = self.Time()
        ## A list that keeps track of the times
        self.times = array.array('l',[])
        ## A list that keep tracks of the poisitons
        self.positions = array.array('l',[])
        ## A flag that determines whether or not the function is recording, set to false or not recording
        self.recording = False

    def update (self, read, tdif):
        '''!@brief Constructs a closed loop controller and Facilitates recording time and postion to the motor
            @details Uses the set point and the input parameter read to create an error signal. This error signal
                     is converted into an output signal with PID controller. While recording is true a loop is used to record the
                     position and time. Once it has finished recording, it prints the values of all 100 positons and times.
            @param read is the motor reading the new values from the encoder.
            @param tdif is the difference of time between recordings.
            @return Sends back actuation signal value using sat method.
        '''
        # Error signal which is the difference between the expected setpoint and the measured value [read].
        e = self.setpoint - read
        #Updates sum of error (area under curve)
        self.esum += (self.laste+e)*tdif/2
        #  Delta error calculated by taking difference in error values over a time difference
        dele = (e - self.laste)/tdif
        # Updates last error
        self.laste = e
        # Actuation signal (in duty cycle) calculation using gains and error values
        actuation_signal = self.Kp*(e) + self.Ki*(self.esum) + self.Kd*(dele)
        
        if(utime.ticks_diff(self.Time(),self.to) < 2000 and self.recording):
            self.times.append(utime.ticks_diff(self.Time(),self.to))
            self.positions.append(read)
        elif (self.recording):
            print("#START#")
            self.print_values()
            self.recording = False
            print("#STOP#")
            
        return self.sat(actuation_signal)
                
    def sat(self,duty):
        '''!@brief Saturation functionallity
            @details Controls if a duty is too large from what is calculated in update method.
            @param duty is the value sent by what is calculated in update method.
            @return Sends back either the saturated limit if duty is too high or original duty based on bounds.
        '''
        if duty<self.satLim[0]:
            return self.satLim[0]
        elif duty>self.satLim[1]:
            return self.satLim[1]
        return duty

    def set_setpoint(self, point):
        '''!@brief Function that resets the setpoint and begins to record the current time.
            @details Also resets the lists for positions and times.
            @param point is the new setpoint
        '''   
        self.setpoint = point
        self.to = self.Time()
        self.record()

    def set_control_gain(self, gain):
        '''!@brief Function that sets the controller gains.
            @param gain is the new proportional gain.
        ''' 
        self.Kp = gain
        
    def record(self):
        '''!@brief Function that rests the the values in the lists for positions and times.
            @details Also changes the recording flag to true so that it allows the computer to begin recording values.
        '''
        self.times = array.array('l',[])
        self.positions = array.array('f',[])
        self.recording = True
        
    def print_values(self):
        '''!@brief Function that prints the values in the lists for positions and times
        '''         
        for i in range(len(self.times)):
            print(str(self.times[i]) + "," + str(self.positions[i]))
