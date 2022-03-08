#!usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser



def main():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"]
        })
    
    #------------------------------Argument parsing-------------------------
    p = ArgumentParser(description = 
                       "This script allows to plot curves exported from virtuoso as .csv files.")
    
    p.add_argument("filename", 
                   type = str, 
                   help = "name of the .csv file")
    p.add_argument("-p", 
                   "--userpath", 
                   type = str, 
                   help = "user specified path")
    p.add_argument("-x", 
                   "--x_label",
                   type = str, 
                   help = "x label")
    p.add_argument("-y", 
                   "--y_label", 
                   type = str, 
                   help = "y label")
    p.add_argument("-a", 
                   "--start", 
                   type = int, 
                   help = "starting index from which to plot")
    p.add_argument("-o", 
                   "--stop", 
                   type = int, 
                   help = "index of the last element to be plotted")
    p.add_argument("-m",
                   "--multiplier",
                   type = float,
                   default = 1,
                   help = "data is multiplied by the specified factor.\
                           Default value is 1"
                   )
    
    args = p.parse_args() 
    #-----------------------------------------------------------------------

    #----------------------Generate file paths and import-------------------
    #decide in which path to look for the files (default or user defined)
    if args.userpath is None:
        filepath = "/home/spino/PhD/Lavori/ADC_test/CSV/" #if userpath is not specified then a default path is used 
    else:
        filepath = args.userpath
    
    file = filepath + args.filename

    try:
        data = np.genfromtxt(file, delimiter = ",")
    except FileNotFoundError as e:
        print("Error: ", e)
        sys.exit(1) 

    if args.multiplier is not None:
        mul = args.multiplier
    else:
        mul = 1

    data_rows = data.transpose()
    xdata = data_rows[0, 1:]
    ydata = mul * data_rows[1:, 1:]
    #-----------------------------------------------------------------------

    #---------------------------Read arguments------------------------------
    if args.start is not None:  
        start_index = args.start
    else:
        start_index = 0  
        
    if args.stop is not None:
        stop_index = args.stop + 1
    else:
        stop_index = xdata.size

    if args.x_label is not None:
        xlab = args.x_label
    else:
        xlab = "x axis"

    if args.y_label is not None:
        ylab = args.y_label
    else:
        ylab = "y axis"
    #-----------------------------------------------------------------------


    #-----------------------Extract vectors, plot and save------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    for trace in ydata:
        ax.plot(xdata[start_index:stop_index], trace[start_index:stop_index])

    # #add legend if necessary
    # ax.legend(loc = "lower right")
    
    ax.set_xlabel(xlab) #add x label
    ax.set_ylabel(ylab) #add y label

    #clean whitespace padding
    fig.tight_layout()
    
    #save and show the result
    savepath = "/home/spino/PhD/Lavori/ADC_test/Manoscritti/figures/"
    figname = args.filename[0:-4] + ".png"
    figurepath = savepath + figname
    try:
        fig.savefig(figurepath, dpi = 600)
    except:
        print("Couldn't save figure to specified path. Check savepath and make sure it exists.")
    #-----------------------------------------------------------------------
    
    
if __name__ == "__main__":
    main()