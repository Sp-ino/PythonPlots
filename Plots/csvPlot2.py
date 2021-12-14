# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 12:27:55 2021

@author: spino
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fttp
from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"]
    })

#------------------------------Argument parsing-------------------------
p = ArgumentParser(description = 
                   "This script allows to plot .csv files having two columns, the first of which represents x data while the second contains y data")

p.add_argument("filename", 
               type = str, 
               help = "name of the .csv file")
p.add_argument("-f2", 
               "--filename2", 
               type = str, 
               help = "name of the second .csv file to be plotted on the same figure")
p.add_argument("-f3",
               "--filename3", 
               type = str, 
               help = "name of the third .csv file to be plotted in the same figure") 
p.add_argument("-x", 
               "--x_label",
               type = str, 
               help = "x label")
p.add_argument("-y", 
               "--y_label", 
               type = str, 
               help = "y label")
p.add_argument("-p", 
               "--userpath", 
               type = str, 
               help = "user specified path")
p.add_argument("-a", 
               "--start", 
               type = int, 
               help = "starting index from which to plot")
p.add_argument("-o", 
               "--stop", 
               type = int, 
               help = "index of the last element to be plotted")
p.add_argument("-s", 
               "--userxval", 
               type = str, 
               help = "This argument allows the user to specify the x values by passing it to the script as a .csv file. The x values should be n the second column of the .csv")
p.add_argument("-d", 
               "--diff", 
               type = bool, 
               help = "This option allows to plot argument1 minus argument2")
p.add_argument("-dft", 
               "--transf", 
               type = bool, 
               help = "This option allows to plot the DTFT of the input and to compute THD")
p.add_argument("-plty", 
               "--plottype", 
               type = str,
               default = None,
               choices = ["line", "stem"],
               help = "This option allows to choose the type of plot")
p.add_argument("-m",
               "--multicol",
               type = bool,
               help = "This option allows to import all columns from the .csv file. The first one is interpreted as the x-axis, while the remaining are seen as y data.")

args = p.parse_args() 
#-----------------------------------------------------------------------



#---------------------------Generate file paths-------------------------
#decide in which path to look for the files (default or user defined)
if args.userpath is None:
    filepath = "/home/spino/PhD/CSV/ADC_test/" #if userpath is not specified then a default path is used 
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
if args.multicol:
    try:
        data = np.genfromtxt(file, delimiter = ",") #if -m is true then data is imported as a numpy matrix
    except:
        print("Could not import " + args.filename)
        sys.exit(1)    
else:
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
        print("Could not import " + args.filename2)
        sys.exit(2)
        
if args.userxval is not None:
    try:
        userxdata = np.genfromtxt(xfile, delimiter = ",", names = ["uselesscol", "userx"])
    except:
        print("Could not import " + args.userxval)
        sys.exit(2)
#-----------------------------------------------------------------------

    

#---------------------Define which data to plot-------------------------
if args.multicol:
    row_len = data[0,:].size    #compute number of coluns (length of a row)
    col_len = data[:,0].size    #compute number of rows (length of a column)
    xdata = data[1:col_len+1,0] #extract xdata
    ydata = data[1:col_len+1,1:row_len+1]   #extract ydata (in general ydata is a matrix)
    ydata = ydata.transpose()   #transpose ydata to simplify the access to the single
                                #trace in this way traces can be iteratively plotted with
                                #for trace in ydata:
                                #   plot(trace)
else:    
    if args.userxval is None: 
        rawxdata = data["x"]
        xdata = rawxdata[1:rawxdata.size+1]
    else:
        xdata = userxdata["userx"]
    rawydata = data["y"]
    ydata = rawydata[1:rawydata.size]

if args.filename2 is not None:
    rawxdata2 = data2["x2"]
    xdata2 = rawxdata2[1:rawxdata2.size+1]

    rawydata2 = data2["y2"]
    ydata2 = rawydata2[1:rawydata2.size+1]
    
if args.filename3 is not None:
    rawxdata3 = data3["x3"]
    xdata3 = rawxdata3[1:rawxdata3.size+1]
    
    rawydata3 = data3["y3"]
    ydata3 = rawydata3[1:rawydata3.size+1]

#print data sizes   
print("x data size: ", xdata.size) #print x data size
print("y data size: ", ydata.size) #print y data size

if args.filename2 is not None:
    print("y2 size: ", ydata2.size) #print y2 data size, if present
    
if args.filename3 is not None:
    print("y3 size: ", ydata3.size) #print y3 data size, if present


#define which points to plot
if args.start is not None:  
    start_index = args.start
else:
    start_index = 0  
    
if args.stop is not None:
    stop_index = args.stop + 1
else:
    stop_index = xdata.size
#-----------------------------------------------------------------------


#--------optional section for plotting the DTFT of the input------------
if args.transf:
    Tsample = 0.000000052
    N = 32                                                          #N should be a power of 2
    startdft = 5
    
    if args.multicol:                                               #if -m is true, compute DFT and THD for each trace
        index = 0
        linydata = np.zeros((row_len-1, N//2))
        for curve in ydata:
            totransform = curve[startdft:N+startdft] - 1            #compute DFT
            plt.plot(totransform, "-o")
            transform = fttp.fft(totransform)
            linydata[index,:] += 2.0/N * np.abs(transform[:N//2])
            totsquared = 0                                          #compute THD
            for harm in linydata[index,2:linydata[0,:].size]:
                totsquared = totsquared + pow(harm,2)
            thdlin = np.sqrt(totsquared)/linydata[index,1]
            thd = 20*np.log10(thdlin)
            print("THD =", thd)
            index+=1
    else:
        totransform = ydata[startdft:N+startdft] - 1                #compute DFT
        plt.plot(totransform, "-o")
        transform = fttp.fft(totransform)
        linydata = 2.0/N * np.abs(transform[:N//2])
        
        totsquared = 0                                              #compute THD
        for harm in ydata[2:linydata.size-1]:
            totsquared = totsquared + pow(harm,2)   
        thdlin = np.sqrt(totsquared)/linydata[1]
        thd = 20*np.log10(thdlin)
        print("THD =", thd)
    
    ydata = 20*np.log10(linydata)               #compute DFT in dB
    
    xdata = np.linspace(0.0, 1.0/(Tsample*2*1000000), N//2+1) #compute x-axis for the DFT
    start_index = 0
    stop_index = N//2
#-----------------------------------------------------------------------


#---------------------Create the plot and show it-----------------------
#plot data by using a blue continuous line for the main plot, red continuous
# line for the additional plot (if present) and green continuous line for the third plot (if present)
fig, ax = plt.subplots(figsize=(7.5, 4.5))

if args.plottype is None or args.plottype == "line":                #plot by using continuous line
    if args.multicol:
        for curve in ydata:
            ax.plot(xdata[start_index:stop_index], curve[start_index:stop_index]) #if -m arg is true, plot all traces iteratively
    else:
        if args.diff == False or args.diff is None: #plot ydata
            ax.plot(xdata[start_index:stop_index], ydata[start_index:stop_index],"-",
                    label = "$V_P$")
        if (args.filename2 is None) and (args.diff == True): #return error message
            print("Error. 2 arguments must be specified to use the -d option")
            sys.exit(2)
        if (args.filename2 is not None) and (args.diff == True): #plot the difference between ydata and ydata2
            ydiff = ydata/ydata2
            ax.plot(xdata[start_index:stop_index], ydiff[start_index:stop_index], 
                    label = "1 ciclo")
        if (args.filename2 is not None) and (args.diff == False or args.diff is None): #plot also ydata2
            ax.plot(xdata[start_index:stop_index], ydata2[start_index:stop_index],
                    "r-.", label = "$V_Q$")
        if args.filename3 is not None: #plot also ydata3
           ax.plot(xdata[start_index:stop_index], ydata3[start_index:stop_index], 
                   "g-", label = "clock")
       
elif args.plottype == "stem":                                       #produce a stem plot
    bottomval = -95                                                 #decide which is the bottomline position
    if args.multicol:
        for curve in ydata:
            ax.stem(xdata[start_index:stop_index], curve[start_index:stop_index], bottom = bottomval) #if -m arg is true, plot all traces iteratively
    else:
        if args.diff == False or args.diff is None: #plot ydata
            ax.stem(xdata[start_index:stop_index], ydata[start_index:stop_index], label = "ADC", bottom = bottomval)
        if (args.filename2 is None) and (args.diff == True): #return error message
            print("Error. 2 arguments must be specified to use the -d option")
            sys.exit(2)
        if (args.filename2 is not None) and (args.diff == True): #plot the difference between ydata and ydata2
            ydiff = ydata - ydata2
            ax.plot(xdata2[start_index:stop_index], ydiff[start_index:stop_index], bottom = bottomval)
        if (args.filename2 is not None) and (args.diff == False or args.diff is None): #plot also ydata2
            markerline, stemlines, baseline = ax.stem(xdata[start_index:stop_index], ydata2[start_index:stop_index],
                                                      markerfmt = "C3o", label = "Ideale", bottom = bottomval)
            plt.setp(stemlines, 'color', plt.getp(markerline,'color'))
            plt.setp(stemlines, 'linestyle', 'dotted')
        if args.filename3 is not None: #plot also ydata3
           markerline, stemlines, baseline = ax.stem(xdata[start_index:stop_index], ydata3[start_index:stop_index],
                                                 markerfmt = "C4o", label = "Errore di kickback", bottom = bottomval)  

#add legend if necessary
if (args.filename2 is not None and (args.diff is None or args.diff == False)) or args.filename3 is not None:
    ax.legend(loc = "lower right")

#add labels to axes
if args.x_label is None: #decide which label to use for x axis (default or user defined)
    x_lab = "$V_{id}$ [s]" #"$f$ [MHz]" 
else:
    x_lab = args.x_label

if args.y_label is None: #decide which label to use for y axis (default or user defined)
    y_lab = "$C_{in}$ [F]"#"Tensione [V]" #"Ampiezza [dB20]" 
else:
    y_lab = args.y_label

ax.set_xlabel(x_lab) #add x label
ax.set_ylabel(y_lab) #add y label

#clean whitespace padding
fig.tight_layout()

#save and show the result
savepath = "/home/spino/PhD/Figures/ADC_test/"
figname = "a.png"
figurepath = savepath + figname
try:
    fig.savefig(figurepath, dpi = 600)
except:
    print("Couldn't save figure to specified path. Check savepath and make sure it exists.")
#-----------------------------------------------------------------------