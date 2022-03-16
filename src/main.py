"""!
    @file main.py
    @details Runs main logic and loops through tasks
    @details This file contains a program that runs 6 tasks
    @author Rodi Diaz
    @author Daniel Munic
    @author John Bennett
    @date March 7, 2022   
"""

import gc
import pyb
import cotask
import task_share
import motor_driver
import closedLoop
import Encoder
import math

#selected zero position of the motor
#i.e if you start the program by going to radius = 0, motor1 will move to the origin
#ORIGIN = -1000

class Switch:
    def __init__ (self, inpin):
        self.pinSwitch = pyb.Pin (inpin, pyb.Pin.IN, pyb.Pin.PULL_UP)
    def state(self):
        if self.pinSwitch.value()==1:
            return 1
        return 0

def polar_to_motor(point):
    '''!@brief function that converts our point into a value acceptable for the motors.
        @details This function takes our two points, which are in the (R,theta) axis and
        maps these values into a certain region. The conversion is done so that the motors
        don't overextend and cause the machine to push pass its limits.
        @param point is the position of the motors in an (R,theta) axis
    '''        
    
    #input is in the format (r, theta)
    #motor 2 goes from -10 to 10, which is 90 degrees
    #motor 1 goes from 0 to 1000, which is 8.75 inches
    #theta goes from -pi/4 to pi/4
    #r goes from 0 to sqrt(1000^2+ 500^2) ~~1118
    
    r = point[0]
    theta = point[1]
    
    #map the values from 0 to 1118 into -900 to 100
    th1 = (r * 1000/math.sqrt(1000**2 + 500**2)) + origin.get() -650
     
    #map the values from -pi/2 to pi/2 into -10 to 10
    th2 = ((theta) * 10) / (math.pi/4)
    
    return (th1,th2)


def rectangular_to_polar(point):
    '''!@brief function that converts our point int cylindrical system.
        @details This function takes our two points, which are in the XY axis and
        convert these position into a cyldrical coordinate system since our machine moves
        by theta or radial position. The conversion is by the equations, and then returns
        two values, a radius and theta
        @param point is the position of the motors in an (X,Y) axis
    '''       
    
    
    #input is in the format (x, y)
    #the image size should be (727, 1000)
    x = point[0]
    y = point[1]
    
    #cartesian coordinates before transforming the image (x,y):
    #                        o
    #(0,1000)________________(0,0)
    #        |               |
    #        |               |
    #        |               |  O
    #        |               |
    #        |_______________|
    #(1000,1000)             (1000, 0)
    #O is the robot aka the reference we will be taking the angle from
    #o is the reference the computer is taking for the points
    
    #cartesian coordinates after transforming the image (newx,newy):
    #(600,-500)________________(1600,-500)
    #        |               |
    #        |               |
    #(0,0)O  |               |
    #        |               |
    #        |_______________|
    #(600, 500)                 (1600, 500)
    
    #polar coordinates (r, theta)
    #(500,-pi/2)________________ (1118,arctan(-500,1000))
    #            |               |
    #            |               |
    #         O  |               | (1000, 0)
    #            |               |
    #            |_______________|
    #(500, pi/2)                  (1118, arctan(500/1000))
    
    #rotate the point 90 degrees using rotation matrix
    #newx = cos(pi/2) x + sin(pi/2) y
    #newy = -sin(pi/2) x + cos(pi/2) y
    #Add 600 to newx because of the distance between r=0 and the lever point
    newx = y
    newy = -x
    
    #transform the image so our 'angle reference point' is in the middle
    newy = newy + 500
    
    #print("transformed rectangular:" + str((newx, newy)))
    
    #calculate r and theta of the new image
    #handle divide by zero
    if newx == 0.0:
        newx = 0.00001
    theta = math.atan(newy/newx)
    r = math.sqrt(newx ** 2 + newy ** 2)
    
    rsatLim = [800,1950]
    if r<rsatLim[0]:
        r = rsatLim[0]
    elif r>rsatLim[1]:
        r = rsatLim[1]
    
    thsatLim = [-3.14159/2,3.14159/2]
    if theta<thsatLim[0]:
        theta = thsatLim[0]
    elif theta>thsatLim[1]:
        theta = thsatLim[1]
    
    return (r,theta)


def task_motor1 ():
    '''!@brief Initializes and creates a motor object in order to move motor 1. 
        @details Creates timer channels that will be used specific to each motor channel to control motor function.
                Creates varriables that will be the motors pins as well as the encoder's pins.
                Creates a closed loop controller with a Kp of 50
                Using the encoder, and closed loop controller, update the position of the
                motor in regular intervals of 10ms until it reaches its final position.
    '''
    ## motor 1 timer (3)
    tim3 = pyb.Timer(3, freq = 20000)
    ## motor 1 pin B4
    pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
    ## motor 1 pin B5
    pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
    ## motor 1 pin Enable Pin A10
    pinENA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 1 object
    motor1 = motor_driver.Motor_Driver(pinB4, pinB5, tim3, pinENA)
    
    # encoder 1
    ## encoder 1 pin B6
    pinB6 = pyb.Pin.cpu.B6
    ## encoder 1 pin B7
    pinB7 = pyb.Pin.cpu.B7
    ## motor 1 encoder object
    encoder1 = Encoder.Encoder(pinB6, pinB7, 4)
    control1 = closedLoop.ClosedLoop(90)
    
    # motor 2
    ## motor 2 timer (5)
    tim5 = pyb.Timer(5, freq = 20000)
    ## motor 2 pin A0
    pinA0 = pyb.Pin(pyb.Pin.cpu.A0)
    ## motor 2 pin A1
    pinA1 = pyb.Pin(pyb.Pin.cpu.A1)
    ## motor 2 pin Enable Pin C1
    pinENB = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 2 object
    motor2 = motor_driver.Motor_Driver(pinA0, pinA1, tim5, pinENB)
    
    # encoder 2
    ## motor 2 encoder pin C6
    pinC6 = pyb.Pin.cpu.C6
    ## motor 2 encoder pin C7
    pinC7 = pyb.Pin.cpu.C7
    ## motor 2 encoder object
    encoder2 = Encoder.Encoder(pinC6, pinC7, 8)
    control2 = closedLoop.ClosedLoop(200,satLim = [-60,60])
    
    switch = Switch(pyb.Pin.board.PC2)
    
    #currpos are the positions the motors are currently moving towards (not where they actually are)
    currpos1 = 0
    currpos2 = 0
    tolerance1 = 3.0
    tolerance2 = 1
    while True:
        
        motor1.set_duty(control1.update(encoder1.read(),10))
        motor2.set_duty(control2.update(encoder2.read(),10))
        encoder1.updatePosition()
        encoder2.updatePosition()
        
        #for calibration
        if switch.state() == 1 and calibrated.get() == 0:
            origin.put(encoder1.read())
            motor1_set.put(encoder1.read())
            motor2_set.put(encoder2.read())
            print("Calibrated. Origin: " + str((encoder1.read(), encoder2.read())))
            finishedmove.put(1)
            calibrated.put(1)

            
            
        if finishedmove.get() == 1:
            currpos1 = motor1_set.get()
            control1.set_setpoint(currpos1)   
            
            currpos2 = motor2_set.get()
            control2.set_setpoint(currpos2)
            
            finishedmove.put(0)
            #print("moving to point" + str((currpos1, currpos2)))
            
        
        #print("Encoder position: " + str((encoder1.read(), encoder2.read())) )
        #check the encoder if we're done moving with +- tolerance
        if finishedmove.get() == 0 and currpos1 < encoder1.read() + tolerance1 and currpos1 > encoder1.read() - tolerance1 and currpos2 < encoder2.read() + tolerance2 and currpos2 > encoder2.read() - tolerance2:
            finishedmove.put(1)
            
        yield (0)
  
def task_logic ():
    '''!@brief function that moves between the states.
        @details This function takes the location of the current position. It then converts
        this position from rectangular coordiantes into cylindrical. It then sends these values
        to the motors so that it can move the position of the pen.
    '''       
    while True:
        
        if finishedmove.get() == 0:
            pass
        else:
            
            ###
            next_point = (px.get(), py.get())
            ###
            #print("rectangular positions: " + str((next_point[0], next_point[1])))
                
            #do the math to find what need to be sent to the motors
            next_point = rectangular_to_polar(next_point)
            #print("polar positions: " + str((next_point[0], next_point[1])))

            next_point = polar_to_motor(next_point)
                
            #print("motor positions: " + str((next_point[0], next_point[1])))
            #send these values to the motors
            motor1_set.put(next_point[0])
            motor2_set.put(next_point[1])
        
        yield(0)    

def task_user ():
    '''!@brief Function that reads a picture
        @details Function that reads a file. If there is something in the file,
        the function produces a list of contours out of it. This lists is what
        is later used as points for the motors to move to.
    '''        
    
    #Reads a file, makes the list of contours out of that
    CommReader = pyb.USB_VCP()
    
    while True:
        if(finishedmove.get() == 1):

            if(CommReader.any()):
                #Reads Most recent Command
                #point format [float,float]
                ## Stores the most recent key pressed
                point = CommReader.readline().decode("UTF-8")
                CommReader.read()
                print("Inputting to serial: " + str(point))

                if '}' in point:
                    print("Lifting Marker")
                    drop_marker.put(0)
                elif '{' in point:
                    print("Dropping Marker")
                    drop_marker.put(1)
                else:
                    try:
                        floatpoint = eval(point)
                        intpoint = (int(floatpoint[0]), int(floatpoint[1]))
                        #this is hacky code below, change this once its all working
                        px.put(floatpoint[0])
                        py.put(floatpoint[1])
#                         ready_for_input(1)
                    except (NameError,SyntaxError) as e:
                        print("Wrong point format")
            else:     
#                 if ready_for_input.get():
                print("READY")
#                 ready_for_input.put(0)
        yield (0)
            
        
def task_solenoid ():
    '''!@brief functun that controls the solenoid.
        @details Everytime this function is clled, it eiher moves the solenoid back into
        its original posittion or shrinks it. This allows the machine to decide when to write
        on the paper and when not to.
    '''       
   
   
   #Control the lifting of the marker
    #I know this doesn't need to be its own task,
    #    but I think its more readable this way than putting it inside the logic task
    pinB3 = pyb.Pin(pyb.Pin.cpu.B3, pyb.Pin.OUT_PP)
#     timer = pyb.Timer(2,freq=50)
#     channel = timer.channel(2,pyb.Timer.PWM,pin=pinB3)
#     channel.pulse_width_percent(0)
    while True:
        if drop_marker.get() == 1:
            pinB3.low()
        else:
            pinB3.high()
        yield(0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    global contours
    
    contours = []
    
    while True:
        try:
            print ('\033[2J________Running________ \r\n')
            
            
            keyShare = task_share.Share ('h', thread_protect = False, name = "keyShare")

#             encoder_position = task_share.Share ('h', thread_protect = False, name = "encoder")
#             position = task_share.Share ('h', thread_protect = False, name = "position")
            #motor1_set = task_share.Queue ('h', 20, thread_protect = False, name = "motor1_set")
            #motor2_set = task_share.Queue ('h', 20, thread_protect = False, name = "motor2_set")
            
            px= task_share.Share ('f', thread_protect = False, name = "px")
            py= task_share.Share ('f', thread_protect = False, name = "py")
            px.put(500)
            py.put(800)
            
            origin = task_share.Share ('f', thread_protect = False, name = "origin")
            origin.put(-3000)
            
            motor1_set = task_share.Share ('f', thread_protect = False, name = "motor1_set")
            motor2_set = task_share.Share ('f', thread_protect = False, name = "motor2_set")
            #booleans
            drop_marker = task_share.Share ('b', thread_protect = False, name = "drop_marker")
            drop_marker.put(0)
            
            finishedmove = task_share.Share ('b', thread_protect = False, name = "finishedmoved")
            finishedmove.put(1)
            
            calibrated = task_share.Share ('b', thread_protect = False, name = "calibrated")
            calibrated.put(0)
            
            ready_for_input = task_share.Share ('b', thread_protect = False, name = "ready")
            ready_for_input.put(1)
            #num = check_user_input("Select a motor Period:")
            
            # Create the tasks. If trace is enabled for any task, memory will be
            # allocated for state transition tracing, and the application will run out
            # of memory after a while and quit. Therefore, use tracing only for 
            # debugging and set trace to False when it's not needed
            ## Creates motor1 task
            task_motor1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 1, 
                             period = 40, profile = True, trace = False)
            ## Creates user task
            task_user = cotask.Task (task_user, name = 'Task_User', priority = 1, 
                                 period = 100, profile = True, trace = False)
            ## Creates logic task
            task_logic = cotask.Task (task_logic, name = 'Task_Logic', priority = 1, 
                                 period = 100, profile = True, trace = False)
            ## Creates solenoid Task
            task_solenoid = cotask.Task (task_solenoid, name = 'Task_Solenoid', priority = 1, 
                                 period = 100, profile = True, trace = False)
            
            
            # Add all the above tasks to the task list
            cotask.task_list = cotask.TaskList()
            cotask.task_list.append (task_motor1)
            cotask.task_list.append (task_user)
            cotask.task_list.append (task_logic)
            cotask.task_list.append (task_solenoid)
            
            # Run the memory garbage collector to ensure memory is as defragmented as
            # possible before the real-time scheduler is started
            gc.collect ()
            
            # Run the scheduler with the chosen scheduling algorithm. Quit if any 
            # character is received through the serial port
            while keyShare.get() != -1:
                cotask.task_list.pri_sched ()
            
            keyShare.put(2318008)
            
            # Print a table of task data and a table of shared information data
            #print ('\n' + str (cotask.task_list))
            #print (task_share.show_all ())
            #print (task1.get_trace ())
            #print ('\r\n')
        except KeyboardInterrupt:
                break
            
    print('Program Terminating')
