# Image Plotter
__Authors: John Bennett, Daniel Munic, Rudi Diaz__<br />
__Date Modified: March 15, 2022__

This README.md introduces the Image Plotter project, a ME 405 project. It includes and overviews of the implemented hardware and software. And a discussion of the results and what we have learned.

## Introduction
We created an image plotter capable of moving a pen with 2.5 degrees of freedom The robot plots in polar (r, theta) coordinates and can turn its operation on and off, by lifting or dropping a pen. We rotate a threaded rod for radial translations and use direct drive to move our wheel around a fixed origin to create the theta angle. A solenoid was used for lifting a pen. We communicate drawing instruction through the serial port from our PC. 

The project is intended to be operated by its creators: John Bennett, Daniel Munic, and Rudi Diaz since we have a deeper understanding of the code. But the device is intended for anyone that wants to use our image plotter. We have a file that converts an image into a printable text file that can be interpreted by our code. So, if anyone has an image, we can print it!

The goal of this project was to create any desired image by generating a series of contours and sending individual commands to the robot until the masterpiece is done. We were able demonstrate that we accomplished this goal by drawing squares, circles and writing the word image.

## Hardware Design Overview
The image plotter hardware that is structural consists of a support bearing, a wooden bearing, a wooden frame, a wooden leg for bearing, and a rod at the origin. The image plotter hardware that is non-structural consists of two Pitterson DC motors, a threaded rod, a direct drive shaft connected to a wheel, a sharpie, a breadboard, a 5A MOSFET, a solenoid, a Nucleo with a shoe, a 2 H-bridge motor driver, a limit switch, and a solenoid and pen carriage. For a full list of our hardware see the BOM below

### BOM 
| Qty. | Part                  | Source                | Est. Cost | 
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors     | ME405 Tub             | - |
|  1   | Nucleo with Shoe          | ME405 Tub             | - |
|  2   | Black Sharpie | Pre-Owned             | - |
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
|  1   | Rotating Rod at Origin     | ME405 Bin             | - |
|  1   | Solenoid and pen platform Carriage | 3D Print      | - |

The motors are in charge of moving the solenoid and pen carriage, which contains the sharpie and solenoid. One motor control the radial distance by rotating the threaded shaft this pushes the solenoid and pen carriage along the shaft at about motor 1000 radians per about 8 inches of radial movement. The solenoid and pen carriage uses the direct drive shaft and wooden bearings to keep movement stable. The second motor controls the angular coordinate by using direct drive to move the wheel around a fixed rod at the origin to create the theta angle, 20 radians on the motor are a 90 degree turn. We are also able to control when we lift and drop the pen using a solenoid. This allows the device to be able to draw on all areas of the paper. The solenoid is controlled by a MOSFET when it is triggered the MOSFET will allow current to flow from 5V to ground. We have a diode in parallel with the solenoid to protect our handwear. The breadboard is used to provide a surface to connect electrical components. We have a limit switch which is mounted close to our motors. the limit switch allows up to locate the origin when the solenoid and pen carriage crash into it. The wooden frame is what everything is mounted to, and it provides support for the entire system. The support bearing adds another contact point to prevent the wooden frame from tilting. See figure 1 and 2 for hardware models. 

![Handwear](Images/HardwareIso.jpg)

__Figure 1:__ Image Plotter Hardware.

![Top View Handwear](Images/HardwareTopView.jpg)

__Figure 2:__ Top View of Image Plotter Hardware.

Figure 3 shows a close-up view of our nucleo and breadboard and shows our wiring layout.

![Nucleo and Breadboard Layout](Images/NucleoAndBreadboard.jpg)

__Figure 3:__ Top View of Image Plotter Hardware.

## Software Design Overview
The software ran on the nucleo is designed using a number of generators which operate as tasks scheduled in [main.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/main.py). These tasks are the motor task, user task, logic task, and solenoid task. The code ran in [main.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/main.py) is meant to accept a singular rectangular coordinate from the user and convert them into motor angles. Then the motors will send the solenoid to that location. By using serial port communication, we can continue to send new rectangular coordinates until we have drawn a picture. Besides for accepting rectangular coordinates our code will also accept up "{" and down "}" commands to control the solenoid.

The motor task sends both motors to the desired position using a [motor_driver](https://github.com/danrmunic/ImagePlotter/blob/main/src/motor_driver.py) object and [ClosedLoop](https://github.com/danrmunic/ImagePlotter/blob/main/src/closedloop.py) object, as well as receiving the motor position using an [Encoder](https://github.com/danrmunic/ImagePlotter/blob/main/src/Encoder.py) object to check if a movement is finished. The user task receives points from the serial port which are sent from the computer in [PC.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/PC.py) (and generated in [sobel.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/sobel.py)). The logic task does the math to convert those points from rectangular coordinates to values which can be sent to the motors in the polar coordinate system. Finally, the Solenoid task moves the pen up and down while drawing based on input from the computer.  

Variables are shared between tasks using Shares and Queues in [task_share.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/task_share.py)

## Results Overview
Our system was able to draw a successful rectangle, circle, and the word image legibly. These images matched our jpg image. We will describe our testing process as well as the tests we preformed

We first started with calculations to predicted how to move from a rectangular coordinate to motor angles. We needed relationships between motor angles to theta and radius, we got these values experimentally by moving the motors. Next, we checked if the robot could accept polar coordinates. We wanted to determine if the robot could move to the desired polar coordinate. We had to further tune parameters to get the accuracy we wanted. Once we have achieved polar coordinates, we then started inputting rectangular coordinates. Once we were confident in our robot’s ability to move from one point to the next we moved to drawing images. 

The system was first tested by sending a picture of a square. While drawing we noticed that when the machine had to draw short strokes, the machine was able to make precise movements and replicate it onto the paper. However, when we inputted large change in position the machine would have difficulty accurately creating this line. This might be because the machine is working in radial and angular coordinates, so it struggles to be able to make straight lines, Since the movement in the theta direction is significantly larger than the radial movement. As we progressed with the project, we were able to change the step size to get the best results. 

We had the system draw three figures. The first was a simple rectangle picture the rectangle was drawn biased on the png image in figure 4. Figure 5 shows our machine’s output drawing. As you can see, the image is not a perfect copy of the image in figure 4, this is due to the fact that due to the machine's coordinate system being cylindrical and has large controller gains. This allowed for slight discrepancies as the machine did it's best to copy the image but was unable to make perfect lines. However, the results are still pretty amazing as the image is easily recognizable to the original image.

![Picture](https://user-images.githubusercontent.com/97563760/158492037-c5d4670c-e1ba-402b-9508-dbc4c1ef846e.png)

__Figure 4:__ Png Image of a Rectangle

![Rectangle](Images/Image.jpg)

__Figure 5:__ System's Drawing of a Rectangle. (Ignore the word image in the center)

We drew another simple shape of a circle. this drawing was also pretty good, but we did not have smooth curves. The scaling of the circle was obviously skewed. See figures 6 and 7. The image looked good and were extremely hay with these results.

![Circle Picture](TestImages/corcle.png)

__Figure 6:__ Png Image of a Circle.

![circle](Images/Circle.jpg)

__Figure 7:__ System's Drawing of a Circle.

The next image the machine drew was the word "IMAGE" as seen in figure 8. The drawing created by the robot can be seen in figure 9. Here we can see that the robot was able to replicate the drawing with a surprising amount of accuracy. One drawback was that machine took a large amount of time in order to complete this image as it could not move the pen at high speeds and the movements it made, while precise, were extremely small. We attempted to rectify this issue by having the machine draw every third point it received, but this led to errors, so we removed this feature. 

![IMAGE](https://user-images.githubusercontent.com/97563760/158493541-b9a949fc-e3b0-4a0a-b39e-d56c009b81c1.png)

__Figure 8:__ Png Image of the Word Image.

![Image](Images/Image.jpg)

__Figure 9:__ System's Drawing of the Word Image.

As for the last image, we had the image attempt to draw former US president Barack Obama. This was by far the most detailed image which unfortunately led to being the hardest one to complete. With all the details required, the image created unfortunately was not able to be an exact copy of the image we had. It also took a long time as the machine tried to capture every last detail. Our picture of Obama is unrecognisable.



__Figure 10:__ Png Image of Obama.

![Image](Images/Obama.jpg)

__Figure 11:__ System's Drawing of Obama.

## Expanding on the Process
In this project, we learned how useful it is to have a greater understanding of various components, we learned how to implement a limit switch, and a solenoid into our code. Also gaining experience and exploring different venders of mechatronic devices really opened our eyes to how to design. There were a couple of tough lessons that we learned during this project. The first was that when the robot rotated the motors moved at different speeds this made keeping a straight line difficult. To overcome this, we decreased the step size between movements. The next is that when purchasing an art make sure it can do what we want it to do. The purchased solenoid could not easily attach to the to the pen. There are solenoids that we could have bought with threads to mount stuff, but we failed to check for how it will mount. This error caused us a lot of stress since it took a long time for us to figure out how to hold the pen. Finally, our project was not the most well designed most of the arts were from the scrap bin, but by having good controls, good resolution and a well-tuned system helped to improve our systems performance in our project. 

For anyone who would like to build on our device, we have several recommendations could help. First improve the way the solenoid attached to the pen currently it is attached by a quick solder. This allows the pen to rotate while drawing which ruins the accuracy of our lines. If the connection were rigid the pen would be able to draw more accurately. Additional parameter tuning is required to optimize the system the Ki and Kd are currently zero and the motor period and Kp could need more tuning. This would allow the drawing to get to each point more accurately and may even allow a decreased tolerance. Decreasing the number of points in a contour would greatly improve the speed at which the machine prints.  

## Additional files
### Microcontroller Classes

* [main.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/main.py)
* [encoder.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/Encoder.py)
* [motor_driver.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/motor_driver.py)
* [closedloop.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/closedloop.py)
* [task_share.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/task_share.py)

### PC Classes
* [PC.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/PC.py)
* [sobel.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/sobel.py)

### Documentation

* [Image Plotter Documentation](https://github.com/danrmunic/ImagePlotter)

### Website Link

* [Image Plotter Website](https://danrmunic.github.io/ImagePlotter/index.html)

### Images Used for Testing

* [TestImages](https://github.com/danrmunic/ImagePlotter/tree/main/TestImages)
