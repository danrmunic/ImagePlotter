import cv2
import numpy as np
import imageio

#to do: handle high resolution images by downscaling

#CONSTANTS 
#   contour threshold changes minimum size of contours
#   high pass threshold changes minimum gradient value- should be higher for higher resolution images
#   scale factor is how much the image should be downscaled- UNIMPLEMENTED
CONTOUR_THRESHOLD = 30
HIGH_PASS_THRESHOLD = 220
SCALE_FACTOR = 1
IMAGE_NAME = "Obama.png"


#image
img = cv2.imread(IMAGE_NAME)

img = cv2.resize(img, (1000, 1400))
img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
#greyscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Guassian filter the image to blur it
blur = cv2.GaussianBlur(img, (3, 3), 0)

#find the gradient of the image
grad_x = cv2.Sobel(blur, cv2.CV_16S, 1, 0, ksize=3)
grad_y = cv2.Sobel(blur, cv2.CV_16S, 0, 1, ksize=3)
abs_grad_x = cv2.convertScaleAbs(grad_x)
abs_grad_y = cv2.convertScaleAbs(grad_y)
grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
cv2.imwrite("sobel.png", grad)

#for otsu filter !!!!
#ret,otsu = cv2.threshold(grad,60,255,cv2.THRESH_BINARY)

#for bw filter !!!!
#(thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#for canny edge !!!!
#edges_high = cv2.Canny(img, 60, 120)

#edges_high = cv2.bitwise_not(edges_high)
#otsu = cv2.bitwise_not(otsu)

#invert the image (swap blacks and whites)
grad = cv2.bitwise_not(grad)
cv2.imwrite("sobel_inverted.png", grad)

#apply threshold to the image for a high pass filter
threshold = grad.copy()
for x in range(grad.shape[0]):
    for y in range(grad.shape[1]):
        if grad[x][y] > HIGH_PASS_THRESHOLD:
            threshold[x][y]= 255
ret,threshold = cv2.threshold(threshold,254,255,cv2.THRESH_BINARY)

cv2.imwrite("sobel_binary.png", threshold)

#find contours of the image to know the "strokes" the plotter needs to make
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#convert the image back to rgb so the contour can be a seperate color
threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)

#make a list of strokes from the list of contours (this just changes how the data is arranged)
#Note: every point will be adjacent to (in 8 directions) the previous point. 
#also draw the contours on the image in red
strokes = []
for contour in contours:
    temp_list = []
    num_points = 0
    for q in contour:
        for point in q:
            num_points+=1
            temp_list.append(point)
            threshold[point[1], point[0]] = (0, 0, 255)
    if num_points > CONTOUR_THRESHOLD:
        strokes.append(temp_list)


m,n = img.shape
skip1 = 0
for stroke in strokes:
    #skip the border
    if skip1 == 0:
        skip1 = 1
        continue
    p1 = float(stroke[0][0])
    p2 = float(stroke[0][1])
    p1 = p1 * 1000
    p2 = p2 * 1000
    p1 = p1/n
    p2 = p2/m
    p1 = p1*8
    p1 = p1/11
    print("[" + str(p1-200) + "," + str(p2+800) + "]")
    print("{")
    print("{")
    for point in stroke:
	#print(str((point[0], point[1])) + str(m) + " " + str(n))
        p1 = float(point[0])
        p2 = float(point[1])
        p1 = p1 * 1000
        p2 = p2 * 1000
        p1 = p1/n
        p2 = p2/m
        p1 = p1*8
        p1 = p1/11
        print("[" + str(p1-200) + "," + str(p2+800) + "]")
	#print("[" + str(float(point[0])*float((1000/m))*float((8/11))) + "," + str(float(point[1])*(1000/m)) + "]")
    print("}")
    print("}")
    
#remove all black pixels from the image (i.e remove everything but contours)
height, width, _ = threshold.shape
for i in range(height):
    for j in range(width):
        if threshold[i,j].sum() == 0:
            threshold[i, j] = [255, 255, 255]

#convert all red pixels to black pixels (i.e make the remaining contours black)
threshold[np.all(threshold == (0, 0, 255), axis=-1)] = (0,0,0)

#Convert the strokes into a gif for visualizing how it will be drawn.
gif_images = []
prev_img = threshold.copy()
prev_img[prev_img<255]=255
for stroke in strokes:
    break
    temp_img = prev_img.copy()
    #print("NEW STROKE")
    for point in stroke:
        #print(point)
        temp_img[point[1], point[0]] = (0,0,0)
    gif_images.append(temp_img)
    prev_img = temp_img

with imageio.get_writer("stroke.gif", mode="I") as writer:
    for idx, frame in enumerate(gif_images):
        writer.append_data(frame)

#cv2.imwrite("im_bw.png", im_bw)
#cv2.imwrite("edges_high.png", edges_high)
cv2.imwrite("output.png", threshold)
#cv2.imwrite("otsu.png", otsu)
