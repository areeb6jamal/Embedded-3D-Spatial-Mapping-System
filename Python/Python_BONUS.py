#Importing all required libraries
from cmath import cos, sin
from turtle import color
from os import truncate
import numpy
import math
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#---- Measurement Collection----
#Set variable to check if it is the first run
firstrun = True

#Inifite loop to keep running however many scans
while(1):
    #Get input on if scan is an additional scan or reset to the first
    status = input("Enter R to restart scan or C to continue")
    
    #If scan is restarting, erase all previously saved data - If not restarting, do not erase previous data and just append to it
    if(status == 'R'):
        datafile = open('data.txt','w')
        truncate
        datafile.close()

    #On the first run, open UART serial communication from uC at COM8 and specific baud rate of 115200
    #Every run beyond the first, not necessary
    if(firstrun == True):
        s = serial.Serial('COM8', baudrate = 115200, timeout = 4)
        print("Opening: " + s.name)
        #After first run, no longer needed to open
        #Do not enter if statement again
        firstrun = False

    #Given
    s.reset_input_buffer()
    s.reset_output_buffer()

    #Plot setup: Axis setup for 3D graph
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    #Axis labeling
    ax.set_xlabel('z')
    ax.set_ylabel('y')
    ax.set_zlabel('x')

    #Given
    #Send 's' flag 
    s.write('s'.encode())

    #Initialize Variables
    x_line=0
    y_line=0
    z_line=0
    z = 0
    count = 0
    array = [0]*64

    #Append mode file
    f = open('data.txt','a')
    #Try and except used for error received during bonus implementation. Once spun backwards, no valid measurement will be caught since kiel code resets as well.
    #Catch the ValueError and exit the program by closing communication line and killing program
    try:
        #Collect 64 measurements and add them to the array, show the array on the shell and then append to memory data file to be later used for plotting
        while (count != 64):
            array[count] = float(s.readline().decode())
            print(array[i_count], i_count + 1)
            f.write(str(array[i_count]))
            f.write('\n')
            #Increment count
            i_count += 1
        #Close file once finished
        f.close()
    except ValueError:
        print("Closing: " + s.name )
        s.close()
        quit()


#---- Plotting Measurement Setup ----
        
    #View file and store into a string
    Measurements = open("data.txt","r") 
    ListMeasurements = Measurements.read().split("\n")
    #Convert to string
    for i in range(0,len(ListMeasurements),1):                                              
        ListMeasurements[i] = str(ListMeasurements[i])
    #Close file and remove last new line and convert to float
    Measurements.close()
    ListMeasurements.pop(len(ListMeasurements)-1)
    plotdata = [float(i) for i in ListMeasurements]

    #If data is to be plotted, move to next scan or to finish without plotting
    action = input("Enter P to plot data and C to continue or E to exit")

    #Exit out of the while loop
    if(action == 'E'):
        print("Closing: " + s.name)
        s.close()
        break;

    #Plot data
    if(action == 'P'):                                                          
        count2 = 0
        #Assuming 10cm forward measurements and 10 total scans max
        while(count2 != len(plotdata)):
            if(count2 == 64):
                z += 0.1
            elif(count2 == 128):
                z += 0.1
            elif(count2 == 192):
                z += 0.1
            elif(count2 == 256):
                z += 0.1
            elif(count2 == 320):
                z += 0.1
            elif(count2 == 384):
                z += 0.1
            elif(count2 == 448):
                z += 0.1
            elif(count2 == 512):
                z += 0.1
            elif(count2 == 576):
                z += 0.1
            elif(count2 == 640):
                z += 0.1

            #Convert angle to radians (5.625*pi/180)
            #y and z of graph
            x_line = [(plotdata[count2-1])*cos((count2-1)*0.098),(plotdata[count2])*cos(count2*0.098)]
            y_line = [(plotdata[count2-1])*sin((count2-1)*0.098),(plotdata[count2])*sin(count2*0.098)]

            
            if(count2 <  64):
                z_line = [0,0]
            else:
                z_line = [z,z] 
                                                                                    
            ax.scatter( (plotdata[count2])*cos(count2*0.098) ,(plotdata[count2])*sin(count2*0.098),z, c = "red", s = 1)

            if(count2 < 64):
                #Check for x y plane point
                ax.plot(x_line ,y_line,0, color = 'red') 
            else:
                ax.plot(x_line ,y_line,z_line, color = 'red')
            count2 += 1

        count3 = 0
        #While loop used for vertical lines
        while(count3 < len(plotdata)-64):
            #Print iteration number to see how many data points are being plotted
            print(count)
            #Check for what scan number was present (10 max), indicating z value
            if(0 <= count3 < 64):
                z = 0
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [0,0.1]
                #Make a line between point and next point, add to plot
                ax.plot(x_line ,y_line,z_line, color = 'red')
            elif(64 <= count3 < 128):
                z = 0.1
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [0.1,0.2]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            elif(128 <= count3 < 192):
                z = 0.2
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [0.2,0.3]
                ax.plot(x_line ,y_line,z_line, color = 'red')
             if(192 <= count3 < 256):
                 z = 0.3
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            if(256 <= count3 < 320):
                z = 0.4
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            if(320 <= count3 < 384):
                z = 0.5
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            if(384 <= count3 < 448):
                z = 0.6
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            if(448 <= count3 < 512):
                z = 0.7
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            if(512 <= count3 < 576):
                z = 0.8
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            if(576 <= count3 < 640):
                z = 0.9
                x_line = [(plotdata[count3])*cos((count3)*0.098),(plotdata[count3+64])*cos(count3*0.098)]
                y_line = [(plotdata[count3])*sin((count3)*0.098),(plotdata[count3+64])*sin(count3*0.098)]
                z_line = [z,z+0.1]
                ax.plot(x_line ,y_line,z_line, color = 'red')
            #After each line segment, increase count
            count3 += 1
        #Plot final graph
        plt.show()

#If exited out of the while loop ('E' inputted), close port communication
print("Closing: " + s.name)
s.close()
