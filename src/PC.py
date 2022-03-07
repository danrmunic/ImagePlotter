'''!
    @file Lab04_PC.py
    @brief Runs PC Code that Communicates with the micro Python Board through the serial board running Lab04 and plots responce.
    @author Rodolfo Diaz
    @author Daniel Munic
    @author John Bennett
    @date Febuary 7, 2022    
'''

import serial
import time

def write_step(s_port):
    '''!@brief a generator that iterates through writting to the s_port.
        @param Current serial port
    '''
    readVal = "0"

    while True:
        yield readVal
        
        s_port.reset_output_buffer()
        readVal = s_port.readline().replace(b'\r\n', b'').decode()
        if ":" in readVal:
            s_port.reset_input_buffer()
            s_port.write(input(readVal).encode("UTF-8") + b'\r\n')
            time.sleep(.1)     
        elif not (readVal == "" or readVal == '#START#'):
            print(readVal)

if __name__ == '__main__':
    '''!@brief Communicates with the micro Python Board through the serial board
        @details Opens a spesified seiral port and iterates through writting new motor periods and step inputs.
                 Then plotting it.
    '''
    COM = 'COM12'
    Speed = 115200
    
    contours = []
    
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
    
    readVal = b"hi"    
    
    with serial.Serial(COM, Speed,timeout=1) as s_port:
        commandCycle = write_step(s_port)
        s_port.reset_output_buffer()
        while (True):
            try:
                if readVal == '#START#':
                    plotCOMData(s_port)
                    readVal = "hi again!"
                else:
                    readVal = next(commandCycle)

            except KeyboardInterrupt:      
                break

    