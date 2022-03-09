#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  8 22:58:26 2022

@author: spino
Copyright (c) 2022 Valerio Spinogatti
Licensed under GNU license
"""


import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
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


    #----------------------Save arguments into variables--------------------
    if args.start is not None:  
        start_index = args.start
    else:
        start_index = 0  
        
    if args.x_label is not None:
        xlab = args.x_label
    else:
        xlab = "frequeny [Hz]"

    if args.y_label is not None:
        ylab = args.y_label
    else:
        ylab = "magnitude [dB20]"
    #-----------------------------------------------------------------------


    #-----------------------------------------------------------------------
    Tsample = 0.000000052
    N = 32                                                          #N should be a power of 2
    sndr_list = []
    n_traces = ydata.shape[0]
    
    if args.multicol:                                               #if -m is true, compute DFT and THD for each trace
        index = 0
        linydata = np.zeros((n_traces, N//2))
        for curve in ydata:
            totransform = curve[start_index:N+start_index] - 1            #compute DFT
            plt.plot(totransform, "-o")
            transform = fft(totransform)
            linydata[index,:] += 2.0/N * np.abs(transform[:N//2])
            totsquared = 0                                          #compute THD
            for harm in linydata[index,2:linydata[0,:].size]:
                totsquared = totsquared + pow(harm,2)
            thdlin = np.sqrt(totsquared)/linydata[index,1]
            thd = 20*np.log10(thdlin)   
            sndr_list.append(-thd)
            print("THD =", thd)
            index+=1
    # else:
    #     totransform = ydata[start_index:N+start_index] - 1                #compute DFT
    #     plt.plot(totransform, "-o")
    #     transform = fttp.fft(totransform)
    #     linydata = 2.0/N * np.abs(transform[:N//2])
        
    #     totsquared = 0                                              #compute THD
    #     for harm in linydata[2:linydata.size-1]:
    #         totsquared = totsquared + pow(harm,2)   
    #     thdlin = np.sqrt(totsquared)/linydata[1]
    #     thd = 20*np.log10(thdlin)
    #     print("THD =", thd)
    # 
    ydata = 20*np.log10(linydata)               #compute DFT in dB
    
    xdata = np.linspace(0.0, 1.0/(Tsample*2*1000000), N//2+1) #compute x-axis for the DFT
    start_index = 0
    stop_index = N//2
    
    if len(sndr_list) >= 2 and args.savethd: 
        outname = "sndr_" + args.filename
        outfile = filepath + outname
        np.savetxt(outfile, sndr_list, delimiter = ",")
    #-----------------------------------------------------------------------
