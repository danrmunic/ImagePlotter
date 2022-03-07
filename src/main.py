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



def polar_to_motor(point):
    #input is in the format (r, theta)
    #motor 2 goes from -10 to 10, which is 90 degrees
    #motor 1 goes from 0 to 1000, which is 8.75 inches
    #theta goes from -pi/4 to pi/4
    #r goes from 0 to sqrt(1000^2+ 500^2) ~~1118
    
    r = point[0]
    theta = point[1]
    
    #map the values from 0 to 1118 into -900 to 100
    r = (r * 1000/math.sqrt(1000**2 + 500**2)) - 900
    
    #map the values from -pi/4 to pi/4 into -10 to 10
    theta = (theta * 10) / (math.pi/4)
    
    return (r,theta)


def rectangular_to_polar(point):
    #input is in the format (x, y)
    #the image size should be (727, 1000)
    x = point[0]
    y = point[1]
    
    #cartesian coordinates before transforming the image (x,y):
    #                        o
    #(0,1000)________________(0,0)
    #        |               |
    #        |               |
    #        |               |
    #        |               |
    #        |_______________|
    #(1000,1000)             (1000, 0)
    #o is the robot aka the reference we will be taking the angle from
    
    #cartesian coordinates after transforming the image (newx,newy):
    #(0,-500)________________(0,-500)
    #        |               |
    #        |               |
    #     o  |               |
    #        |               |
    #        |_______________|
    #(0, 500)                 (1000, 500)
    
    #polar coordinates (r, theta)
    #(500,-pi/4)________________ (1118,arctan(-500,1000))
    #            |               |
    #            |               |
    #         o  |               | (1000, 0)
    #            |               |
    #            |_______________|
    #(500, pi/4)                  (1118, arctan(500/1000))
    
    #rotate the point 90 degrees using rotation matrix
    #newx = cos(pi/2) x + sin(pi/2) y
    #newy = -sin(pi/2) x + cos(pi/2) y
    newx = y
    newy = -x
    
    #transform the image to our 'angle reference point' is in the middle
    newy = newy - (newy/2)
    
    #calculate r and theta of the new image
    theta = math.atan(newy/newx)
    r = math.sqrt(newx ** 2 + newy ** 2)
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
    
    control1 = closedLoop.ClosedLoop(50)
    
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
    
    #currpos are the positions the motors are currently moving towards (not where they actually are)
    currpos1 = 0
    currpos2 = 0
    finishedmove = 1
    tolerance = 0.1
    while True:
        
        if finishedmove == 1:
            encoder1.updatePosition()
            motor1.set_duty(control1.update(encoder1.read(),10))
            currpos1 = motor1_set.get()
            control1.set_setpoint(currpos1)
            
            encoder2.updatePosition()        
            motor2.set_duty(control2.update(encoder2.read(),10))
            currpos2 = motor2_set.get()
            control2.set_setpoint(currpos2)
            
            finishedmove = 0
            print((currpos1, currpos2))
            
        #check the encoder  if we're done moving with +- tolerance
        if currpos1 < encoder1.read() + tolerance and currpos1 > encoder1.read() - tolerance  and currpos2 < encoder2.read() + tolerance and currpos2 > encoder2.read() - tolerance:
            finishedmove = 1
            
        yield (0)
  
def task_logic ():
    #take input as contours[] from task_user
    contour_index = 0
    point_index = 0
    while True:
        #check if you've finished the list of contours
        if contour_index < len(contours):
            contour = contours[contour_index]
            #check if you've finished the current contour
            if point_index < len(contour):
                #Find what the next point is
                next_point = contour[point_index]
                
                #do the math to find what need to be sent to the motors
                next_point = rectangular_to_polar(next_point)
                next_point = polar_to_motor(next_point)
                
                print(next_point[0], next_point[1])
                #send these values to the motors
                motor1_set.put(next_point[0])
                motor2_set.put(next_point[1])
                
                #go to the next point
                point_index = point_index + 1
                
                #Make sure the marker is down while drawing.
                #This should only transition from Lifted to Dropped when transitioning between contours
                drop_marker = True
            else:
                #if the current contour is finished, lift the marker, reset the index
                point_index = 0
                drop_marker = False
                
                #go to the next contour
                contour_index = contour_index + 1
        else:
            contour_index = 0
            #read_file.put(1)
        yield(0)    

def task_user ():
    #Reads a file, makes the list of contours out of that
    
    while True:
        if read_file.get():
            try:
                f = open("strokes.txt", 'r')
            except FileNotFoundError:
                print("waiting for file strokes.txt...")
            
            Lines = f.readlines()
 
            #print("testing")
            contour = []
            #go through all the lines to fill the contours list
            for line in Lines:
                #create an empty contour
                
                #check if the contour is finished. If it is, add it to contours list and then start a new contour
                if '}' in line:
                    contours.append(contour)
                    #print(contours)
                    contour=[]
                elif '{' in line:
                    continue
                else:
                    #use eval to convert string to tuple, then add that point to the contour
                    point = eval(line)
                    intpoint = (int(point[0]), int(point[1]))
                    #print(intpoint)
                    contour.append(intpoint[:])
                
            read_file.put(0)
            yield (0)
            
        
def task_solenoid ():
    #Control the lifting of the marker
    #I know this doesn't need to be its own task,
    #    but I think its more readable this way than putting it inside the logic task
    pinB3 = pyb.Pin(pyb.Pin.cpu.B3, pyb.Pin.OUT_PP)
    while True:
        if drop_marker:
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
            
            encoder_position = task_share.Share ('h', thread_protect = False, name = "encoder")
            position = task_share.Share ('h', thread_protect = False, name = "position")
            #motor1_set = task_share.Queue ('h', 20, thread_protect = False, name = "motor1_set")
            #motor2_set = task_share.Queue ('h', 20, thread_protect = False, name = "motor2_set")
            
            motor1_set = task_share.Share ('f', thread_protect = False, name = "motor1_set")
            motor2_set = task_share.Share ('f', thread_protect = False, name = "motor2_set")
            #booleans
            drop_marker = task_share.Share ('b', thread_protect = False, name = "drop_marker")
            read_file = task_share.Share ('b', thread_protect = False, name = "read_file")
            read_file.put(1)
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
