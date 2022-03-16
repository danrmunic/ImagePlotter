## @file mainpage.py
#  @author Rodolfo Diaz
#  @author Daniel Munic
#  @author John Bennett
#  @date March 15, 2022   
#  @mainpage
#
#  @section Software Software Design
#  Here is our current plan for our code. First We have all our states and how they interact and share varables with each other.<br>
#  \image html TaskDiagrams.png "Figure 1: Image Plotter Task Diagram" <br>
#  Next sections show each States State Transition Diagram.
#  @subsection User User Task
#  \image html FSMUser.png "Figure 2: UserTask State Transition Diagram" <br>
#  This is the User Task which describes the task the microcontroller runs to take input from the computer through the serial bus.
#
#  Input is sent line by line in the form of points (rectangular coordinates) and brackets indicating
#  control of the solenoid ([ means drop the marker, ] means lift the marker). This can be seen in the text files in the TestImages folder on github. The series of points and brackets
#  to control the robot is generated in sobel.py. The files are sent in PC.py, which is run by the computer during runtime of the system.
#
#  On the microcontroller side, this task waits for input and interperets it (using the built in python function eval to convert strings to float tuples)to be used by other tasks. 
#  When the robot is ready for another input (when it finished the current function i.e move to a point or drop/raise solenoid) it replies "READY" to the computer. 
#  @subsection Motor Motors Task
#  \image html FSMMotors.png "Figure 3: Motor State Transition Diagram" <br>
#  This is the Motor task. The motors are first initialized, which involves creating two motor driver, two encoder, and two closed loop controller objects.
#  The rectangular coordinates are converted to polar and sent to the motor drivers.
#  Once the encoder reads that the motors have reached the positions they're supposed to be at, the task outputs that the move is finished so the User Task can read the next point. 
#  @subsection Solenoid Solenoid Task
#  \image html FSMSolenoid.png "Figure 4: Solenoid State Transition Diagram" <br>
#  This is the Solenoid task which moves the marker up and down using the solenoid. This simple task takes input from the User task as a boolean for turning on and off the solenoid. 
