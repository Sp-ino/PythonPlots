#!/bin/python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tabulate import tabulate

rcParams['text.usetex'] = True 
rcParams['font.family'] = 'Times New Roman'

dircsv="/home/cristian/csv/sallen_key_10GHz/csv_files/"
filecsv="csv_LPF_wideBandMC1000.csv"
# filecsv2="csv_THDvsfat410m.csv"
data=np.genfromtxt(dircsv+filecsv,delimiter=',',dtype='str')
headerc=data[0,:]
data=data[3:,[1,3,5,6,7]]

values=0
print(tabulate(data, headers=headerc))