# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 12:27:55 2021

@author: spino
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser


#------------------------------Argument parsing-------------------------
p = ArgumentParser(description = 
                   "This script allows to plot .csv files having two columns, the first of which represents x data while the second contains y data")

p.add_argument("filename", type = str, help = "name of the .csv file")
p.add_argument("-f", "--filename2", type = str, help = "name of the second .csv file to be plotted on the same figure") 
p.add_argument("-x", "--x_label", type = str, help = "x label")
p.add_argument("-y", "--y_label", type = str, help = "y label")
p.add_argument("-p", "--userpath", type = str, help = "user specified path")
p.add_argument("-a", "--start", type = int, help = "starting index from which to plot")
p.add_argument("-o", "--stop", type = int, help = "final index until which to plot")
p.add_argument("-s", "--userxval", type = str, help = "This argument allows the user to specify the x values by passing it to the script as a .csv file. The x values should be n the second column of the .csv")

args = p.parse_args() 
#-----------------------------------------------------------------------



#---------------------------Generate file paths-------------------------
#decide in which path to look for the files (default or user defined)
if args.userpath is None:
    filepath = "C:/Users/spino/Documents/UNIVERSITA/TesiLM/csvFiles/" #if userpath is not specified then a default path is used 
else:
    filepath = args.userpath

file = filepath + args.filename

if args.filename2 is not None:
    file2 = filepath + args.filename2
    
if args.userxval is not None:
    xfile = filepath + args.userxval
#-----------------------------------------------------------------------



#-------------------------Import the .csv files-------------------------
try:
    data = np.genfromtxt(file, delimiter = ",", names = ["x", "y"])
except:
    print("Could not import " + args.filename)
    sys.exit(1)
    
if args.filename2 is not None:
    try:
        data2 = np.genfromtxt(file2, delimiter = ",", names = ["x2", "y2"])
    except:
        print("Could not import " + args.filename2)
        sys.exit(2)
        
if args.userxval is not None:
    try:
        userxdata = np.genfromtxt(xfile, delimiter = ",", names = ["uselesscol", "userx"])
    except:
        print("Could not import " + args.userxval)
        sys.exit(2)
#-----------------------------------------------------------------------

    

#---------------------Create the plot and show it-----------------------
#define which data to plot
if args.userxval is None: 
    xdata = data["x"]
else:
    xdata = userxdata["userx"] 
        
ydata = data["y"] 

if args.filename2 is not None:
    xdata2 = data2["x2"]
    ydata2 = data2["y2"]
    
#print data sizes   
print("x data size: ", xdata.size) #print x data size
print("y data size: ", ydata.size) #print y data size

if args.filename2 is not None:
    print("y data 2 size: ", ydata2.size) #print y data 2 size, if present


#define which points to plot
if args.start is not None:  
    start_index = args.start
else:
    start_index = 1  
    
if args.stop is not None:
    stop_index = args.stop
else:
    stop_index = xdata.size


#plot data by using a blue continuous line for the main plot and red continuous
# line for the additional plot (if present)
plt.plot(xdata[start_index:stop_index], ydata[start_index:stop_index], "b-")
if args.filename2 is not None:
     plt.plot(xdata2[start_index:stop_index], ydata2[start_index:stop_index], "r-")   
     
    
#add labels
if args.x_label is None: #decide which label to use for x axis (default or user defined)
    x_lab = "Vid [V]"
else:
    x_lab = args.x_label

if args.y_label is None: #decide which label to use for y axis (default or user defined)
    y_lab = "Vod [V]"
else:
    y_lab = args.y_label
    
plt.xlabel(x_lab) #add x label
plt.ylabel(y_lab) #add y label
plt.show() #show the plot
#-----------------------------------------------------------------------