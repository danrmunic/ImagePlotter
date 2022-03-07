# ImagePlotter
We want to make a two and a half degree of freedom robot capable of drawing any image on a piece of paper from an uploaded image on our PC to create a masterpiece. The code will turn an image into a series of vectors that our system will draw the robot.

The device will use a rotating base with two motors mounted on top. One motor will spin a wheel to create rotational motion. Another motor will create linear motion that will move the pen linearly alongside a threaded shaft. The shaft will be parallel to each other and will be connected with bearings and the pen mount. This setup will allow the pen to mark up the entire page. We will be using a solenoid actuator and MOSFET to connect to the pen, and the solenoid will lift and lower the pen. Our complete setup will utilize a signal microcontroller taking commands from a PC. Our Patterson Gearmotors will require a larger voltage supply than our microcontroller can support, so we will be using the motor drivers with two H-bridges to control to control our motors in the project. 

![Solidworks Model](Images/SideView.png)

__Figure 1:__ Back view of Solidworks model of 2.5 DOF Image Plotter Schematic.


![Solidworks Model](Images/OtherSideView.png)

__Figure 2:__ Front view of Solidworks model.


![Scaled Sketch for Project](https://user-images.githubusercontent.com/97563760/154212086-1d5e8bd8-d7ae-4cbe-9947-79c46431a7ba.png)

__Figure 3:__ Version 1 of 2.5 DOF Image Plotter Schematic project.

## Introduction

We want to make a two and a half degree of freedom robot capable of drawing any image on a piece of paper from an uploaded image on our PC. The code will turn an image into a series of vectors that our system will draw. The system will be using a radial and angular coordinate system. The device will be intended as a fun activity for casual users. 


## Hardware Design Overview

The hardware of the project will be consisiting of two motors, two rods, a breadboard, a mosfet, a solenoid, a mount and a wooden frame in order to hold the robot. The motors will be in charge of moving the solenoid. One motor will control the the radial distance from the mount while the second motor will control the angular coordinate. This will allow the device to be able to go to all areas of the paper. The two rods will be used as guiding rods for the solenoid to be able to move up and down. The solenoid will be used as to control the pen, whether or not it marks the paper. This will be controlled by in input voltage into a mosfet that will either trigger the solenoid or not. The breadboard is used in otder to be able to provide a surface to connect electrical components. The wooden frame provides support for the entire system.

## Software Design Overview

## Results Overview
The system was tested by sending a few pictures of squares as images. We noticed that when the image had short strokes, the machine was able to make precise movements and replicate it onto the paper. However, when there were large, signluar strokes, the machine would have difficulty recreating this image. This might be becaause the machine is working in radial and angular coordinates, so it struglles to be able to make straight lines.

## Expanding on the Process
In this project, we learned how useful it is to have a greater understanding of various components. The solenoid was extremely helpful in being able to move the sharpie up and down. It was difficult to integrate the entire system into one machine since there are multiple devices to connect with one another. However, when combined, they make a far more efficient machine than previously imagined. The best advice to give to someone who might expand on our current setup, would be to familiarize themselves with each component in order to create the best possible machine.



## BOM 
| Qty. | Part                  | Source                | Est. Cost | 
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors     | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe          | ME405 Tub             |     -     |
|  2   | Black & Red Sharpie&trade | Pre-Owned     |   -   |
|  1   | Motor Driver 2 H-bridges| ME405 Tub | - |
|  1   | 5A Power MOSFETs          | [DigiiKey](https://www.digikey.com/en/products/detail/stmicroelectronics/STN3NF06L/654517?s=N4IgjCBcoLQBxVAYygMwIYBsDOBTANCAPZQDaIALAJwDsIAugL6OEBMZIAygCoByAzLwBiABgBsAGQaMgA)        |   $3.80   |
|  1   | Solenoid Actuator        | [Digikey](https://www.digikey.com/en/products/detail/sparkfun-electronics/ROB-11015/6163694) | $4.95 |
|  1   | 1/4” Guide Rod 12” Long | ME405 Bin | - |
|  1   | 1/4” Threaded Rod 12” Long       | ME405 Bin | - |
|  1   | Rotating Base       | ME405 Bin | - |
|  1   | 3” Rubber Wheel       | [McMaster](https://www.mcmaster.com/wheels/wheels-4/rubber-wheels-7/) | $1.98 |
|  1   | Bearing Wheel       | Clayton | - |
|  2   | 1/4" Ball Bearing       | [servocity](https://www.servocity.com/1-4-bore-bottom-tapped-pillow-block/) | $14 |
|  2   | 3/8 to 1/4 Shaft Coupler       | [amazon](https://www.amazon.com/Stainless-Steel-Screw-Shaft-Coupler/dp/B00KVNA50G/ref=sr_1_3?crid=39PDB30GPBVOX&keywords=3%2F8+inch+to+3%2F8+inch+Stainless+Steel+Set+Screw+Shaft+Coupler&qid=1645675919&s=industrial&sprefix=3%2F8+inch+to+3%2F8+inch+stainless+steel+set+screw+shaft+coupler%2Cindustrial%2C110&sr=1-3) | $9.98 |
|  1   | Solenoid and pen platform | 3D Print |- |


## Future Classes

* [encoder.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/encoder.py)
* [motor_driver.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/motor_driver.py)
* [main.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/main.py)
* [controller.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/controller.py)
* [user.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/user.py)
* [logic.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/logic.py)
* [solenoid.py](https://github.com/danrmunic/ImagePlotter/blob/main/src/solenoid.py)

## Documentation

* [Image Plotter Documentation](https://github.com/danrmunic/ImagePlotter)

## Website Link

* [Image Plotter Website](https://danrmunic.github.io/ImagePlotter/index.html)
