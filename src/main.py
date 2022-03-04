"""!
    @file main.py
    @details Runs main logic and loops through tasks
    @details This file contains a program that runs 3 tasks (motor1, motor2 and a usertask), and
        inter-task shared variable containing commands. for weather to step or not. 
        This file is meant to help us choose an appropiate motor period.
        The user can exit program by pressing cntrl+c
    @author Rodi Diaz
    @author Daniel Munic
    @author John Bennett
    @date Febuary 7, 2022   
"""

import gc
import pyb
import cotask
import task_share
import motor_driver
import closedLoop
import Encoder

# a few globals


def check_user_input(prompt):
    '''!@brief Verifies that input is a valid int or float
        @param propmt The input from the user
    '''
    while True:
        try:
            # Convert it into float
            num = input(prompt)
            return float(num)
        except ValueError:
            print("No.. "+ num +" input is not a number. It's a string. Enter a Number")

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
    
    control1 = closedLoop.ClosedLoop(50)
    
    
    while True:
        encoder1.updatePosition()
        
        motor1.set_duty(control1.update(encoder1.read(),10))
        
        if keyShare.get() == 1:
            encoder1.zero()
            control1.set_setpoint(20)
            keyShare.put(0)
        elif keyShare.get() == 3:
            encoder1.zero()
            control1.set_setpoint(20)
        yield (0)
    
def task_motor2 ():
    '''!@brief Initializes and creates a motor object in order to move motor 2. 
        @details Creates timer channels that will be used specific to each motor channel to control motor function.
                Creates varriables that will be the motors pins as well as the encoder's pins.
                Creates a closed loop controller with a Kp of 50
                Using the encoder, and closed loop controller, update the position of the
                motor in regular intervals of 10ms until it reaches its final position.
    '''
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
    
    control2 = closedLoop.ClosedLoop(50)
    
    while True:
        
        encoder2.updatePosition()        
        motor2.set_duty(control2.update(encoder2.read(),10))
        if keyShare.get() == 2:
            encoder2.zero()
            control2.set_setpoint(20)
            keyShare.put(0)
        elif keyShare.get() == 3:
            encoder2.zero()
            control2.set_setpoint(20)
            keyShare.put(0)
        yield (0)

def task_logic ():
    #take input as contours[] from task_user
    contour_index = 0
    point_index = 0
    while True:
        if contour_index <= len(contours):
            contour = contours[contour_index]
            if point_index <= len(contours):
                next_point = contour[point_index]
                point_index = point_index + 1
            else:
                point_index = 0
            contour_index = contour_index + 1
        else:
            contour_index = 0
        yield(0)


def task_controller ():
    #convert rectangular to polar coordinants from a point to control the motors to go to that point
    #use the encoder position to figure out how far we need to move
    while True:
        #convert the point to polar here
        yield(0)
        
    
    

def task_user ():
    '''!@brief Reads data from USB comm port.
        @details Checks to see if there is any new inputs from the comm port.
                Will step motor 1 if 'a' is pressed.
                Will step motor 2 if 'b' is pressed.
                Will stop motors and show diagnostics if 'c' is pressed.
                Will step motor 1 and 2 if 'd' is pressed.
    '''
    vcp = pyb.USB_VCP ()
    
    while True:
        yield (0)
        if vcp.any():
            command = vcp.read(1)
            if command == b'a':
                keyShare.put(1)
            elif command == b'd':
                keyShare.put(3)
            elif command == b'b':
                keyShare.put(2)
            elif command == b'c':
                print("read")
                keyShare.put(-1)
                
            print(vcp.read())
        
def task_solenoid ():
    
    while True:
        yield(0)

'''
def task_encoder ():
    # encoder 1
    ## encoder 1 pin B6
    pinB6 = pyb.Pin.cpu.B6
    ## encoder 1 pin B7
    pinB7 = pyb.Pin.cpu.B7
    ## motor 1 encoder object
    encoder1 = Encoder.Encoder(pinB6, pinB7, 4)
    
    # encoder 2
    ## motor 2 encoder pin C6
    pinC6 = pyb.Pin.cpu.C6
    ## motor 2 encoder pin C7
    pinC7 = pyb.Pin.cpu.C7
    ## motor 2 encoder object
    encoder2 = Encoder.Encoder(pinC6, pinC7, 8)
    
    while True:
        encoder1.updatePosition()
        encoder2.updatePosition()
        point = (encoder1.read(), encoder2.read())
        encoder_position = polar_to_rectangular(point)
        yield(0)
'''

def polar_to_rectangular(point):
    return (0,0)

def rectangular_to_polar(point):
    return (0,0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    global motor1_duty
    global motor2_duty 
    global contours 
    global next_point 
    global marker_dropped 
    global encoder_position 
    global position
    
    contours = []
    
    while True:
        try:
            print ('\033[2J________Running__LAB03________ \r\n'
               'Press \"a\" or \"b\" to step motor 1 or 2. Or \"d\" for both'
               'Press \"c\" to stop and show diagnostics.')
        
            keyShare = task_share.Share ('h', thread_protect = False, name = "Share 0")
            
            num = check_user_input("Select a motor Period:")
            
            # Create the tasks. If trace is enabled for any task, memory will be
            # allocated for state transition tracing, and the application will run out
            # of memory after a while and quit. Therefore, use tracing only for 
            # debugging and set trace to False when it's not needed
            ## Creates motor1 task
            task_motor1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 1, 
                             period = num, profile = True, trace = False)
            ## Creates motor2 task
            task_motor2 = cotask.Task (task_motor2, name = 'Task_Motor2', priority = 1, 
                                 period = num, profile = True, trace = False)
            ## Creates user task
            task_user = cotask.Task (task_user, name = 'Task_User', priority = 1, 
                                 period = 100, profile = True, trace = False)
            
            task_logic = cotask.Task (task_logic, name = 'Task_Logic', priority = 1, 
                                 period = 100, profile = True, trace = False)
            
            task_controller = cotask.Task (task_controller, name = 'Task_Controller', priority = 1, 
                                 period = 100, profile = True, trace = False)
            
            task_solenoid = cotask.Task (task_solenoid, name = 'Task_Solenoid', priority = 1, 
                                 period = 100, profile = True, trace = False)
            
            cotask.task_list = cotask.TaskList()
            cotask.task_list.append (task_motor1)
            cotask.task_list.append (task_motor2)
            cotask.task_list.append (task_user)
            #cotask.task_list.append (task_logic)
            #cotask.task_list.append (task_controller)
            #cotask.task_list.append (task_solenoid)
            
            # Run the memory garbage collector to ensure memory is as defragmented as
            # possible before the real-time scheduler is started
            gc.collect ()
            
            # Run the scheduler with the chosen scheduling algorithm. Quit if any 
            # character is received through the serial port
            while keyShare.get() != -1:
                cotask.task_list.pri_sched ()
            
            keyShare.put(2318008)
            
            # Print a table of task data and a table of shared information data
            print ('\n' + str (cotask.task_list))
            print (task_share.show_all ())
            #print (task1.get_trace ())
            print ('\r\n')
        except KeyboardInterrupt:
                break
    
    print('Program Terminating')
