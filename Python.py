from os import truncate
from cmath import cos, sin
from turtle import color
import serial
import numpy
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#Import all the libraries needed to create 3d plot

status = input("Enter R to restart scan or C to continue")                    #Ask the user if they would like to restart the scans
if(status == 'R'):
    f = open('data.txt','w')                                                    #Open the .txt file 
    truncate                                                                    #Erase all saved data
    f.close()                                                                   #Close the .txt file

s = serial.Serial('COM8', baudrate = 115200, timeout = 4)                       #Recieve data from uC at COM8 and a baud rate of 115200
print("Opening: " + s.name)


s.reset_input_buffer()
s.reset_output_buffer()

fig = plt.figure(figsize=(10,10))                                               #Define the axis for the 3d graph
ax = fig.add_subplot(111, projection='3d')                                      
ax.set_zlabel('x')                                                              #Label the x,y, z axis in 3d projection 
ax.set_ylabel('y')
ax.set_xlabel('z')

s.write('s'.encode())                                                           #Send a the flag 's' to start data collection
  
counter = 0                                                                     #Define variables 
x_line=0
y_line=0
z_line=0
z = 0

x = [0]*64                                                                      #Create array corresponding to 64 scans
f = open('data.txt','a')                                                        #Open a .txt file in append mode
try:
    while (counter != 64):                                                          #Collect 64 distance measurements
        x[counter] = float(s.readline().decode())                                   #Collect distance measurments and append to the array
        print(x[counter], counter + 1)                                              #Print each measurement and measurement number
        f.write(str(x[counter]))                                                    #Convert to string and append to .txt file
        f.write('\n')                                                               #Move to next line
        counter += 1                                                                #Increment counter by 1 each time 
    f.close()                                                                       #CLose the file
except ValueError:
    print("Closing: " + s.name )                            #Close the communcation line
    s.close()
    quit()                                                                                      #CLose the file

data = open("data.txt","r")                                                     #Open text file for user to view
dataStr = data.read()                                                           #Put the data into a string
dataList = dataStr.split("\n")                                                  #Seperate data at splaces
for i in range(0,len(dataList),1):                                              
    dataList[i] = str(dataList[i])                                              #Append the string to a list
data.close()                                                                    #Close the text file
dataList.pop(len(dataList)-1)                                                   #Remove the last "\n" 

Data = [float(i) for i in dataList]                                             #Convert the data into a float

plotdata = input("Enter P to plot data and C to continue")                   #Ask user if they would to plot the data
if(plotdata == 'P'):                                                          #Plot data if user inputs 'Yes'
    counter = 0
    while(counter != len(Data)):                                                 #If there is still data left to plot

        if(counter == 64):                                                      #Check the number of the scan and assign z value 
            z += 0.1
        elif(counter == 128):
            z += 0.1
        elif(counter == 192):
            z += 0.1
        elif(counter == 256):
            z += 0.1
        elif(counter == 320):
            z += 0.1
        elif(counter == 384):
            z += 0.1
        elif(counter == 448):
            z += 0.1
        elif(counter == 512):
            z += 0.1
        elif(counter == 576):
            z += 0.1
        elif(counter == 640):
            z += 0.1

        x_line = [(Data[counter-1])*cos((counter-1)*0.098),(Data[counter])*cos(counter*0.098)]    #Convert the distance into y and z
        y_line = [(Data[counter-1])*sin((counter-1)*0.098),(Data[counter])*sin(counter*0.098)]
        if(counter <  64):
            z_line = [0,0]
        else:
            z_line = [z,z] 
                                                                                
        ax.scatter( (Data[counter])*cos(counter*0.098) ,(Data[counter])*sin(counter*0.098),z, c = "red", s = 1) #Plot the points

        if(counter < 64):
            ax.plot(x_line ,y_line,0, color = 'red')                                                 #Check if the point is on the xy plane 
        else:
            ax.plot(x_line ,y_line,z_line, color = 'red')
        counter += 1

    count = 0
    lines = len(Data)                                                                                #Find the number of measurements taken
    
    while(count < lines-64):
        print(count)
        
        #While loop to create vertical lines
        if(count <64):                                                                               #Check which condition is met to determine scan number
            z = 0                                                                                    #Based on scan number, set z value appropriately 
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]    #Convert the distance into y and z and make the line between current and next points
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [0,0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')                                            #Plot the lines created 
        elif(64 <= count < 128):
            z = 0.1
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [0.1,0.2]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        elif(128 <= count < 192):
            z = 0.2
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [0.2,0.3]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(192 <= count < 256):
            z = 0.3
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(256 <= count < 320):
            z = 0.4
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(320 <= count < 384):
            z = 0.5
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(384 <= count < 448):
            z = 0.6
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(448 <= count < 512):
            z = 0.7
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(512 <= count < 576):
            z = 0.8
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        if(576 <= count < 640):
            z = 0.9
            x_line = [(Data[count])*cos((count)*0.098),(Data[count+64])*cos(count*0.098)]
            y_line = [(Data[count])*sin((count)*0.098),(Data[count+64])*sin(count*0.098)]
            z_line = [z,z+0.1]
            ax.plot(x_line ,y_line,z_line, color = 'red')
        count += 1                                    #Increment the count variable after each line segment
    plt.show()                                          #Plot the graph and show it

print("Closing: " + s.name )                            #Close the communcation line
s.close()
