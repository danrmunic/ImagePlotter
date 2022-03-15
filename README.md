# ImagePlotter
__Authors: John Bennett, Daniel Munic, Rudi Diaz__<br />
__Date Modified: March 15, 2022__

This README.md introduces the ImagePlotter project, a ME 405 project. It includes and overviews of the implemented hardware and softwear. And a disscussion of the results and what we have learned.

## Introduction
We created an imageplotter capable of moving a pen with 2.5 degrees of freedom The robot plots in polar (r,theta) coordinates and is able to turn its operation on and off, by lifting or dropping a pen. We rotate a threaded rod for radial tranlations and use direct drive to move our wheel around a fixed orgin to create the theta angle. A solinoid was used for lifting a pen. We communicate drawing instruction through the serial port from our PC. 

The project is intended to be operated by its creators: John Bennett, Daniel Munic, and Rudi Diaz since we have a deeper understanding of the code. But the device is intended for anyone that wants to use our image plotter. We have a file that converts an image into a printable textfile that is able to be interpreted by our code. So if anyone has an image we can print it!

The goal of this project was to create any desired image by generating a series of contors and sending individual commands to the robot until the master piece is done. We were able demonstrate that we accomplished this goal by drawing squares, circles and writing the word image.

## Hardware Design Overview
The image plotter hardware that is structuarl consists of a support bearing, a wooden bearings, a wooden frame, a wooden leg for bearing, and a rod at the orgin. The image plotter hardware that is non-structuarl consists of two Pittperson DC motors, a threaded rods, a direct drive shaft connected to a wheel, a sharpee, a breadboard, a 5A mosfet, a solenoid, a nucleo with a shoe, a 2 H-bridge motor driver, a limit switch, and a solenoid and pen carrage. For a full list of our hardware see the BOM below

### BOM 
| Qty. | Part                  | Source                | Est. Cost | 
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors     | ME405 Tub             | - |
|  1   | Nucleo with Shoe          | ME405 Tub             | - |
|  2   | Black & Red Sharpie&trade | Pre-Owned             | - |
|  1   | Motor Driver 2 H-bridges  | ME405 Tub             | - |
|  1   | 5A Power MOSFETs          | [DigiiKey](https://www.digikey.com/en/products/detail/stmicroelectronics/STN3NF06L/654517?s=N4IgjCBcoLQBxVAYygMwIYBsDOBTANCAPZQDaIALAJwDsIAugL6OEBMZIAygCoByAzLwBiABgBsAGQaMgA)        |   $3.80   |
|  1   | Diode                     | ME405 Tub             | - |
|  1   | Solenoid Actuator         | [Digikey](https://www.digikey.com/en/products/detail/sparkfun-electronics/ROB-11015/6163694) | $4.95 |
|  1   | Limit Switch              | Gift                  | - |
|  1   | 1/4” Guide Rod 12” Long   | ME405 Bin             | - |
|  1   | 1/4” Threaded Rod 12” Long| ME405 Bin             | - |
|  1   | 3” Rubber Wheel           | ME405 Bin             | - |
|  2   | 3/8 to 1/4 Shaft Coupler  | [amazon](https://www.amazon.com/Stainless-Steel-Screw-Shaft-Coupler/dp/B00KVNA50G/ref=sr_1_3?crid=39PDB30GPBVOX&keywords=3%2F8+inch+to+3%2F8+inch+Stainless+Steel+Set+Screw+Shaft+Coupler&qid=1645675919&s=industrial&sprefix=3%2F8+inch+to+3%2F8+inch+stainless+steel+set+screw+shaft+coupler%2Cindustrial%2C110&sr=1-3) | $9.98 |
|  1   | Bearing Wheel             | Clayton               | - |
|  1   | Wooden Bearings           | Scrap Wood Bin        | - |
|  1   | Wooden Frame              | Scrap Wood Bin        | - |
|  1   | Wooden Wheel Leg          | Scrap Wood Bin        | - |
|  1   | Rotating Rod at Orgin     | ME405 Bin             | - |
|  1   | Solenoid and pen platform Carrage | 3D Print      | - |

The motors are in charge of moving the solenoid and pen carrage, which contains the sharpee and solenoid. One motor controls the radial distance by rotating the threaded shaft this pushes the solenoid and pen carrage along the shaft at about motor 1000 radians per about 8 inches of radial movement. The solenoid and pen carrage uses the direct drive shaft and wooden bearings to keep movement stable. The second motor controls the angular coordinate by using direct drive to move the wheel around a fixed rod at the orgin to create the theta angle, 20 radians on the motor is a 90 degree turn. We are also able to control when we lift and drop the pen using a solinoid. This allows the device to be able to draw on all areas of the paper. The solinoid is controlled by a mosfet when it is triggered the mosfet will allow current to flow from 5V to ground. We have a diode in parralel with the solinoid to protect our hardwear. The breadboard is used to provide a surface to connect electrical components. We have a limit switch which is mounted close to our motors. the limit switch allows up to locate the orgin when the solenoid and pen carrage crash into it. The wooden frame is what everything is mounted to and it provides support for the entire system. The support bearing adds another contact point to prevent the wooden frame from tilting. See figure 1 and 2 for hardware models. 

![Hardwear]()

__Figure 1:__ Image Plotter Hardware.

![Top View Hardwear](Images/OtherSideView.png)

__Figure 2:__ Top View of Image Plotter Hardware.

Figure 3 shows a close up view of our nucleo and breadboard and shows our wiring layout.

![Nucleo and Breadboard Layout](Images/OtherSideView.png)

__Figure 2:__ Top View of Image Plotter Hardware.






## Software Design Overview
The software is designed using a number of generators which operate as tasks scheduled in [main.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/main.py). The motor task sends the desired position to the motors using a [motor_driver](https://github.com/danrmunic/ImagePlotter/blob/main/src/motor_driver.py) object and [ClosedLoop](https://github.com/danrmunic/ImagePlotter/blob/main/src/closedloop.py) object, as well as receiving the motor position using an [Encoder](https://github.com/danrmunic/ImagePlotter/blob/main/src/Encoder.py) object to check if a movement is finished. The user task recieves points from the serial port which are sent from the computer in [PC.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/PC.py) (and generated in [sobel.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/sobel.py)). The logic task does the math to convert those points from rectangular coordinates to values which can be sent to the motors in the polar coordinate system. Finally, the Solenoid task moves the pen up and down while drawing based on input from the computer.  

Variables are shared between tasks using Shares and Queues in [task_share.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/task_share.py)


## Results Overview
The system was tested by sending a few pictures of squares as images. We noticed that when the image had short strokes, the machine was able to make precise movements and replicate it onto the paper. However, when there were large, signluar strokes, the machine would have difficulty recreating this image. This might be becaause the machine is working in radial and angular coordinates, so it struglles to be able to make straight lines.

## Expanding on the Process
In this project, we learned how useful it is to have a greater understanding of various components. The solenoid was extremely helpful in being able to move the sharpie up and down. It was difficult to integrate the entire system into one machine since there are multiple devices to connect with one another. However, when combined, they make a far more efficient machine than previously imagined. The best advice to give to someone who might expand on our current setup, would be to familiarize themselves with each component in order to create the best possible machine.



## Microcontroller Classes

* [main.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/main.py)
* [encoder.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/Encoder.py)
* [motor_driver.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/motor_driver.py)
* [closedloop.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/closedloop.py)
* [task_share.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/task_share.py)

## PC Classes
* [PC.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/PC.py)
* [sobel.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/sobel.py)

## Documentation

* [Image Plotter Documentation](https://github.com/danrmunic/ImagePlotter)

## Website Link

* [Image Plotter Website](https://danrmunic.github.io/ImagePlotter/index.html)

## Images used for testing

* [TestImages](https://github.com/danrmunic/ImagePlotter/tree/main/TestImages)



We created a two and a half degree of freedom robot capable of drawing any image on a piece of paper from an uploaded image on our PC. The code turns an image into a series of points that our system draws. The system will be using a radial and angular coordinate system. The device is intended as a fun activity for casual users.

The device uses a rotating base with two motors mounted on top. One motor spins a wheel to create rotational motion. Another motor creates linear motion that moves the pen linearly alongside a threaded shaft. The shafts are parallel to each other and are be connected with bearings and the pen mount. This setup allows the pen to mark up the entire page. We use a solenoid actuator and MOSFET to connect to the pen, and the solenoid lifts and lowers the pen. Our complete setup utilizes a signal microcontroller taking commands from a PC. Our Patterson Gearmotors require a larger voltage supply than our microcontroller can support, so we use the motor drivers with two H-bridges to control our motors in the project.
