# ImagePlotter

We want to make a 2 and a half degree of freedom robot capable of drawing any image on a piece of paper and is capable of using computer vision. When a user walks up into the robots view , the robot will recognise the user and will begin to draw. This project will be interactive and be able to capture memories with friends.

The device will use a rotating base with 2 motors mounted on top. 1 motor will spin a a wheel to create rotational motion another motor will create linear motion that will move the pen alongside the shaft. This will allow the pen to mark up the entire page. We will be using a solenoid actuator connected to the pen in order to lift and lower the pen. This will be controlled by a signal from the microcontroller. Our motors will be requiring a larger current supply than our microcontroller can support, so we will be using MOSFET's in order to be able to properly supply sufficient voltage to the motors. 

![Scaled Sketch](https://user-images.githubusercontent.com/97563760/154204014-fe9ef3ca-9391-4aec-83e9-0e81f0d38162.png)

__Figure 3:__ 2.5 DOF Image Plotter Schematic.

## BOM 
| Qty. | Part                  | Source                | Est. Cost | 
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors     | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe          | ME405 Tub             |     -     |
|  2   | Black & Red Sharpie&trade | Pre-Owned     |   -   |
|  2   | 5A Power MOSFETs          | [Digi-Key]  ( https://www.digikey.com/en/products/detail/taiwan-semiconductor-corporation/TSM900N06CH-X0G/7360597?s=N4IgjCBcoLQBxVAYygMwIYBsDOBTANCAPZQDa4cADBALoC%2BdhATGSACoDKAsgJyWUA5SgDYAwgAkABAA1KAcRD0gA)        |   $3.80   |
|  1   | .?” Guide Rails 10” Length | McMaster | ? |
|  1   | .?” Threaded Rod 10” Length       | McMaster | ? |
|  1   | .?” Lead Screw        | McMaster | ? |
|  1   | 3” Rubber Wheel       | [McMaster](https://www.mcmaster.com/wheels/wheels-4/rubber-wheels-7/) | $1.98 |
|  1   | Solenoid Actuator        | [Digikey](https://www.digikey.com/en/products/detail/sparkfun-electronics/ROB-11015/6163694) | $4.95 |
|  1   | Rotating Base       | McMaster | ? |


## Classes

## Documentation

## Website Link
