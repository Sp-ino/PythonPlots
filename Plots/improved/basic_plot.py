#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  8 19:35:25 2022

@author: spino
Copyright (c) 2022 Valerio Spinogatti
Licensed under GNU license
"""

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
                   help = "name of the .csv file"
                   )
    p.add_argument("-p", 
                   "--userpath", 
                   type = str, 
                   help = "user specified path"
                   )
    p.add_argument("-x", 
                   "--x_label",
                   type = str, 
                   help = "x label")
    p.add_argument("-y", 
                   "--y_label", 
                   type = str, 
                   help = "y label"
                   )
    p.add_argument("-a", 
                   "--start", 
                   type = int, 
                   help = "starting index from which to plot"
                   )
    p.add_argument("-o", 
                   "--stop", 
                   type = int, 
                   help = "index of the last element to be plotted"
                   )
    p.add_argument("-m",
                   "--multiplier",
                   type = float,
                   default = 1,
                   help = "data is multiplied by the specified factor.\
                           Default value is 1"
                   )
    p.add_argument("-c",
                   "--columns",
                   type = int,
                   nargs = "+",
                   default = None,
                   help = "Indices of the columns to plot as y data from the .csv. \
                        The count should start from 1 if the first column of the .csv \
                        represents the x axis. If a 0 is specified as argument, the program \
                        will assume that column 0 of the .csv  also represents y data \
                        and the selected columns will be plotted against the number of \
                        samples."
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
        data = np.genfromtxt(file, delimiter = ",", dtype = np.double)
    except FileNotFoundError as e:
        print("Error: ", e)
        sys.exit(1) 

    if args.multiplier is not None:
        mul = args.multiplier
    else:
        mul = 1

    if data.shape[1] == 1:
        raise Warning("The .csv file that has been")
    data_rows = data.transpose()
    xdata = data_rows[0, 1:]
    ydata = mul * data_rows[1:, 1:]
    #-----------------------------------------------------------------------

    #----------------------Save arguments into variables--------------------
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

    num_y_cols = ydata.shape[0]
    if args.columns is None:
        col_list = list(range(1,num_y_cols+1))
    else:
        col_list = args.columns
        np_col_list = np.array(col_list)
        if np_col_list[np_col_list > num_y_cols].shape[0] != 0:
            raise OSError("One (or more) of the indices that have been specified exceeds the range \
                          of valid indices for the columns of the y data.")
        
        col_list = args.columns
    #-----------------------------------------------------------------------


    #-----------------------Extract vectors, plot and save------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    if 0 in col_list:
        for ind, trace in enumerate(data_rows):
            if ind not in col_list:
                continue
            ax.plot(trace[start_index:stop_index])
    else:
        for ind, trace in enumerate(ydata):
            if ind+1 not in col_list:
                continue
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