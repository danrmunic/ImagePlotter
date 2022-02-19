# ImagePlotter

We want to make a 2 and a half degree of freedom robot capable of drawing any image on a piece of paper and is capable of using computer vision or an uploaded image to create a masterpeice. When a user walks up into the robots view , the robot will recognise the user and will begin to draw. This project will be interactive and be able to capture memories with friends. The code will turn an image into a series of vectors that the robot will draw.

The device will use a rotating base with 2 motors mounted on top. 1 motor will spin a wheel to create rotational motion another motor will create linear motion that will move the pen alongside the shaft. This will allow the pen to mark up the entire page. We will be using a solenoid actuator connected to the pen in order to lift and lower the pen. This will be controlled by a signal from the microcontroller. Our motors will be requiring a larger current supply than our microcontroller can support, so we will be using MOSFET's in order to be able to properly supply sufficient voltage to the motors. 

![Scaled Sketch for Project](https://user-images.githubusercontent.com/97563760/154212086-1d5e8bd8-d7ae-4cbe-9947-79c46431a7ba.png)



__Figure 1:__ 2.5 DOF Image Plotter Schematic.

## BOM 
| Qty. | Part                  | Source                | Est. Cost | 
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors     | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe          | ME405 Tub             |     -     |
|  2   | Black & Red Sharpie&trade | Pre-Owned     |   -   |
|  2   | 5A Power MOSFETs          | [DigiiKey](https://www.digikey.com/en/products/detail/stmicroelectronics/STN3NF06L/654517?s=N4IgjCBcoLQBxVAYygMwIYBsDOBTANCAPZQDaIALAJwDsIAugL6OEBMZIAygCoByAzLwBiABgBsAGQaMgA)        |   $3.80   |
|  1   | 1/4” Guide Rod 12” Long | [servocity](https://www.servocity.com/0-375-3-8-x-12-00-stainless-steel-precision-shafting/) or ME405 Tub | $5.18 |
|  1   | 1/4” Threaded Rod 12” Long       | ME405 Tub | - |
|  1   | 3” Rubber Wheel       | [McMaster](https://www.mcmaster.com/wheels/wheels-4/rubber-wheels-7/) | $1.98 |
|  1   | 2.25” Chair Wheel       | [McMaster](https://www.mcmaster.com/24215T44/) | $2.30 |
|  1   | Solenoid Actuator        | [Digikey](https://www.digikey.com/en/products/detail/sparkfun-electronics/ROB-11015/6163694) | $4.95 |
|  1   | Rotating Base       | ME405 Tub | - |
|  2   | 3/8" Ball Bearing       | [servocity](https://www.servocity.com/3-8-bore-bottom-tapped-pillow-block/) | $12.74 |
|  2   | 3/8 to 3/8 Shaft Coupler       | [amazon](https://www.amazon.com/Stainless-Steel-Screw-Shaft-Coupler/dp/B00KVNACWC) | $9.98 |
|  1   | Solenoid and pen platform | 3D Print |- |


## Classes

## Documentation

## Website Link

