#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  8 19:35:25 2022

@author: spino
Copyright (c) 2022 Valerio Spinogatti
Licensed under GNU license
"""

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
                       "This script allows to plot traces imported from .csv files. The .csv file is \
                        expected to have traces stored as columns, with the first column being the x data. \
                        The program supports basic on-the-fly processing of the traces: for example, the \
                        user can choose whether to plot all the points in each trace or just part of them, \
                        or it can decide to treat the first column of the .csv file as either x data or y \
                        data.")
    
    p.add_argument("filename", 
                   type = str, 
                   help = "Name of the .csv file"
                   )
    p.add_argument("-p", 
                   "--userpath", 
                   type = str, 
                   help = "User specified path"
                   )
    p.add_argument("-x", 
                   "--x_label",
                   type = str, 
                   help = "x axis label")
    p.add_argument("-y", 
                   "--y_label", 
                   type = str, 
                   help = "y axis label"
                   )
    p.add_argument("-a", 
                   "--start", 
                   type = int, 
                   help = "Starting index from which to plot"
                   )
    p.add_argument("-o", 
                   "--stop", 
                   type = int, 
                   help = "Index of the last element to be plotted"
                   )
    p.add_argument("-m",
                   "--multipliers",
                   type = float,
                   nargs = "+",
                   default = None,
                   help = "y data is multiplied by the specified factors.\
                           Default value is 1 for all columns. The number \
                           of multipliers that are passed to the program \
                           must coincide with the number of y data columns \
                           in the .csv file."
                   )
    p.add_argument("-c",
                   "--columns",
                   type = int,
                   nargs = "+",
                   default = None,
                   help = "Indices of the columns to plot as y data from the .csv. \
                        The count should start from 1 if the first column of the .csv \
                        represents the x axis. If a 0 is passed as argument, the program \
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
        raise OSError(e)

    # Remove header
    _, data = data[0], data[1:]

    # Extract number of columns
    num_data_cols = data.shape[1]
    #-----------------------------------------------------------------------

    #----------------------Save arguments into variables--------------------
    if args.start is not None:  
        start_index = args.start
    else:
        start_index = 0  
        
    if args.stop is not None:
        stop_index = args.stop + 1
    else:
        stop_index = data.shape[0]

    if args.x_label is not None:
        xlab = args.x_label
    else:
        xlab = "x axis"

    if args.y_label is not None:
        ylab = args.y_label
    else:
        ylab = "y axis"

    num_y_cols = num_data_cols - 1
    if args.columns is None:    # if -c option is not specified, plot columns 1: against column 0
        col_list = list(range(1,num_y_cols+1))
    else:                       # otherwise plot only the specified ones
        col_list = args.columns
        if 0 in col_list:       # if 0 is in col_list then column 0 is interpreted as y data
            num_y_cols = num_data_cols
        
    if num_data_cols == 1 and 0 not in col_list:
        raise Warning("Option -c: the .csv file that has been imported has just one column of data. \
                    If you want to plot it rerun the script with the option --columns 0 \
                    or -c 0.")

    np_col_list = np.array(col_list)
    if np.any(np_col_list[np_col_list > num_y_cols]) or np.any(np_col_list[np_col_list < 0]):
        raise OSError("Option -c: one (or more) of the specified indices is invalid.")
    
    if args.multipliers is not None:
        if len(args.multipliers) != num_y_cols:
            raise OSError("Option -m: the number of multipliers that are specified must coincide with \
                           the number of y traces.")
        multipliers = args.multipliers
    else:
        multipliers = [1]*num_y_cols
    #-----------------------------------------------------------------------

    #-----------------------Extract vectors, plot and save------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    # Transpose data matrix to make things easier with for loops
    data_rows = data.transpose()

    if 0 in col_list:
        for ind, trace in enumerate(data_rows):
            if ind not in col_list:
                continue
            y = multipliers[ind]*trace[start_index:stop_index]
            ax.plot(y)
    else:
        x = data_rows[0, start_index:stop_index]
        for ind, trace in enumerate(data_rows[1:]):
            if ind+1 not in col_list:
                continue
            y = multipliers[ind]*trace[start_index:stop_index]
            ax.plot(x, y)

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