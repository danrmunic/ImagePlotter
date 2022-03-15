
'''!
    @file Lab04_PC.py
    @brief Runs PC Code that Communicates with the micro Python Board through the serial board running Lab04 and plots responce.
    @author Rodolfo Diaz
    @author Daniel Munic
    @author John Bennett
    @date Febuary 7, 2022    
'''

import serial

def SendNextVal(s_port):
    '''!@brief
        @param 
    '''
    s_port.reset_input_buffer()
    a = str(NewLines.pop(0))
    print(a)
    s_port.write(a.encode("UTF-8") + b'\r\n')
    

def write_step(s_port):
    '''!@brief a generator that iterates through writting to the s_port.
        @param Current serial port
    '''
    readVal = "0"

    while True:
        yield readVal
        
        s_port.reset_output_buffer()
        readVal = s_port.readline().replace(b'\r\n', b'').decode()

        if not (readVal == "" or readVal == 'READY'):
            print(readVal)


if __name__ == '__main__':
    '''!@brief Communicates with the micro Python Board through the serial board
        @details Opens a spesified seiral port and iterates through writting new motor periods and step inputs.
                 Then plotting it.
    '''
    
    COM = 'COM3'
    Speed = 115200    
    
    try:
        f = open("obama.txt", 'r')
    except FileNotFoundError:
        print("waiting for file strokes.txt...")
            
    Lines = f.readlines()
    NewLines = []
    for line in Lines:
        NewLines.append(line.strip())

 
    
    
    readVal = b"hi"    
    
    with serial.Serial(COM, Speed,timeout=1) as s_port:
        commandCycle = write_step(s_port)
        s_port.reset_output_buffer()
        SendNextVal(s_port)
        while (True):
            try:
                if readVal == 'READY':
                    SendNextVal(s_port)
                    readVal = "hi again!"
                else:
                    readVal = next(commandCycle)

            except KeyboardInterrupt:      
                break
