#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 11:20:35 2022

@author: spino
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fttp
from argparse import ArgumentParser

def main():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"]
        })
    
    #------------------------------Argument parsing--------------------------------
    p = ArgumentParser(description = 
                       "This script allows to make histogram plot starting from .csv with one column.")
    
    p.add_argument("filename", 
                   type = str, 
                   help = "name of the .csv file")
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
    
    args = p.parse_args()
    #------------------------------------------------------------------------------
    
    
    #---------------------------Generate file paths-------------------------
    #decide in which path to look for the files (default or user defined)
    if args.userpath is None:
        filepath = "/home/spino/PhD/Lavori/ADC_test/CSV/" #if userpath is not specified then a default path is used 
    else:
        filepath = args.userpath
        
    file = filepath + args.filename
    #------------------------------------------------------------------------------
    
    
    #--------------------------Import list from csv--------------------------------
    try:
        data = np.genfromtxt(file, delimiter = ",") 
    except:
        print("Could not import " + args.filename)
        sys.exit(1)
    #------------------------------------------------------------------------------
     
    
    #------------------------Compute mean and standard dev-------------------------
    datalen = len(data)
    mean = sum(data)/datalen
    squares = [pow((value - mean), 2) for value in data]
    stdev = np.sqrt(sum(squares)/datalen)
    #------------------------------------------------------------------------------
    
    
    #--------------------------Generate histogram and save figure------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    #textstr = f"$\mu={mean}$ \n$\sigma={stdev}$ \n $N_p={datalen}$"
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mean, ),
        r'$\sigma=%.2f$' % (stdev, ),
        r'$N_{points}=%d$' % (datalen, )))
    
    ax.hist(data)
    ax.text(0.05, 0.95, textstr, transform = ax.transAxes, fontsize = 14,
            verticalalignment = 'top', bbox = props)
    
    fig.show()
    
    savepath = "/home/spino/PhD/Lavori/ADC_test/Manoscritti/figures/"
    figname = "sndr_v9_mismatch.png"
    figurepath = savepath + figname
    
    try:
        fig.savefig(figurepath, dpi = 600)
    except:
        print("Couldn't save figure to specified path. Check savepath and make sure it exists.")
    #-----------------------------------------------------------------------
    

if __name__ == "__main__":
    main()