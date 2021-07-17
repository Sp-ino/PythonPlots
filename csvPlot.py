# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 12:27:55 2021

@author: spino
"""

import sys
import numpy
import matplotlib.pyplot as plt
from argparse import ArgumentParser

p = ArgumentParser(description = "This script allows to plot .csv files")

p.add_argument("filename", type = str, help = "name of the .csv file")
p.add_argument("-p", "--userpath", type = str, help = "user specified path. The path must end with a /")

args = p.parse_args() 

if args.userpath is None:
    filepath = "C:/Users/spino/Documents/UNIVERSITA/TesiLM/csvFiles/"
else:
    filepath = args.userpath

    
file = filepath + args.filename

try:
    data = numpy.genfromtxt(file, delimiter=",", names=["x", "y"])
except:
    print("Could not import specified file")
    sys.exit(-1)
    
plt.plot(data['x'], data['y'])
plt.xlabel("Time [ns]")
plt.ylabel("Voltage [V]")
plt.show()