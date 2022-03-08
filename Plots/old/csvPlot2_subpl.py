# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 12:27:55 2021

@author: spino
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"]
    })

#------------------------------Argument parsing-------------------------
p = ArgumentParser(description = 
                   "This script allows to plot .csv files having two columns, the first of which represents x data while the second contains y data")

p.add_argument("filename", type = str, help = "name of the .csv file")
p.add_argument("-f2", "--filename2", type = str, help = "name of the second .csv file to be plotted on the same figure")
p.add_argument("-f3", "--filename3", type = str, help = "name of the third .csv file to be plotted in the same figure") 
p.add_argument("-x", "--x_label", type = str, help = "x label")
p.add_argument("-y", "--y_label", type = str, help = "y label")
p.add_argument("-x2", "--x2_label", type = str, help = "x2 label")
p.add_argument("-y2", "--y2_label", type = str, help = "y2 label")
p.add_argument("-x3", "--x3_label", type = str, help = "x3 label")
p.add_argument("-y3", "--y3_label", type = str, help = "y3 label")
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
    
if args.filename3 is not None:
    file3 = filepath + args.filename3
    
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
        
if args.filename3 is not None:
    try:
        data3 = np.genfromtxt(file3, delimiter = ",", names = ["x3", "y3"])
    except:
        print("Could not import " + args.filename3)
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
        
ydata = data["y"]*1000000000000

if args.filename2 is not None:
    xdata2 = data2["x2"]
    ydata2 = data2["y2"]*1000000
    
if args.filename3 is not None:
    xdata3 = data3["x3"]
    ydata3 = data3["y3"]*1000

#print data sizes   
print("x data size: ", xdata.size) #print x data size
print("y data size: ", ydata.size) #print y data size

if args.filename2 is not None:
    print("y2 data size: ", ydata2.size) #print y2 data size, if present
    
if args.filename3 is not None:
    print("y3 data size: ", ydata3.size) #print y3 data size, if present


#define which points to plot
if args.start is not None:  
    start_index = args.start
else:
    start_index = 1  
    
if args.stop is not None:
    stop_index = args.stop
else:
    stop_index = xdata.size

#optional section for plotting the ratio between ydata and a custom vector
# idealDeltaV = []
# for i in range(0,9):
#     idealDeltaV.append(1/pow(2,i))
#     ydata[i] = ydata[i]/idealDeltaV[i]

#plot data by using a blue continuous line for the main plot, red continuous
#line for the additional plot (if present) and green continuous line for the 
#third plot (if present)
if (args.filename2 is None) and (args.filename3 is None):
    fig, ax = plt.subplots(figsize=(4,7))
if args.filename2 is not None:
    fig, (ax, ax2) = plt.subplots(nrows = 2, ncols=1, figsize=(5.5,5.5)) 
if (args.filename2 is not None) and (args.filename3 is not None):
    fig, (ax, ax2, ax3) = plt.subplots(nrows = 3, ncols=1, figsize=(5.5,8)) 
ax.plot(xdata[start_index:stop_index], ydata[start_index:stop_index], label = "Consumo di potenza")
if args.filename2 is not None:
   ax2.plot(xdata2[start_index:stop_index], ydata2[start_index:stop_index], "r-", label = "Delay")
if args.filename3 is not None:
   ax3.plot(xdata3[start_index:stop_index], ydata3[start_index:stop_index], "g-", label = "Errore di kickback")  

#add legend if necessary
# if args.filename2 is not None or args.filename3 is not None:
#     ax.legend()

#add labels to axes
if args.x_label is None: #decide which label to use for x axis (default or user defined)
    x_lab = "$W_{56}$ [$\mu$m]"
else:
    x_lab = args.x_label

if args.y_label is None: #decide which label to use for y axis (default or user defined)
    y_lab = "delay [ps]"
else:
    y_lab = args.y_label
    
if args.x2_label is None: #decide which label to use for x axis (default or user defined)
    x2_lab = "$W_{56}$ [$\mu$m]"
else:
    x2_lab = args.x2_label

if args.y2_label is None: #decide which label to use for y axis (default or user defined)
    y2_lab = "Consumo di potenza [$\mu$W]"
else:
    y2_lab = args.y2_label
    
if args.x3_label is None: #decide which label to use for x axis (default or user defined)
    x3_lab = "$W_{56}$ [$\mu$m]"
else:
    x3_lab = args.x3_label

if args.y3_label is None: #decide which label to use for y axis (default or user defined)
    y3_lab = "Errore di carica [mV]"
else:
    y3_lab = args.y3_label

ax.set_xlabel(x_lab) #add x label
ax.set_ylabel(y_lab) #add y label

if args.filename2 is not None:
    ax2.set_xlabel(x2_lab) #add x2 label
    ax2.set_ylabel(y2_lab) #add y2 label
    
if args.filename3 is not None:
    ax3.set_xlabel(x3_lab) #add x3 label
    ax3.set_ylabel(y3_lab) #add y3 label


fig.tight_layout()

#save and show the result
savepath = "C:/Users/spino/Documents/UNIVERSITA/TesiLM/Manoscritti/tesi/figures/"
figname = "a.png"
figurepath = savepath + figname
fig.savefig(figurepath, dpi = 600)
#-----------------------------------------------------------------------