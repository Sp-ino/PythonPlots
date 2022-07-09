#!/bin/python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams['text.usetex'] = True 
rcParams['font.family'] = 'Times New Roman'

dircsv="/home/cristian/csv/sallen_key_10GHz/csv_files/"
filecsv="csv_THDvsfat400m100M4G.csv"
# filecsv2="csv_THDvsfat410m.csv"
data=np.genfromtxt(dircsv+filecsv,delimiter=',',skip_header=1)
# data2=np.genfromtxt(dircsv+filecsv2,delimiter=',',skip_header=1)

datax=data[:,0]
datay=data[:,1:]
# datax2=data2[:,0]
# datay2=data2[:,1:]









# for columns in datay.transpose():
#     plt.plot(datax/(10**9),columns,label=r"\textit{Noise Spectrum}")
# plt.plot(datax,datay.transpose()[0],label=r"\textit{$V_{O_{dm}}$ (ideal)}")
# plt.plot(datax,datay.transpose()[1],label=r"\textit{$V_{O_{cm}}$}")
# plt.plot(datax,datay.transpose()[2],label=r"\textit{$V_{O_{dm}}$}")


yp# plt.plot(datax,datay.transpose()[0],label=r"\textit{THD}")
# plt.plot(datax,datay.transpose()[1],label=r"\textit{SNR}")
# plt.plot(datax,datay.transpose()[2],label=r"\textit{DR}")


# plt.plot(datax,datay.transpose()[0],label=r"\textit{THD\@$200mV$}")
# plt.plot(datax,datay.transpose()[1],label=r"\textit{SNR}")
# plt.plot(datax,datay.transpose()[2],label=r"\textit{DR}")
# plt.plot(datax2,datay2.transpose()[0],label=r"\textit{THD}")
# plt.plot(datax2,datay2.transpose()[1],label=r"\textit{SNR}")
# plt.plot(datax2,datay2.transpose()[2],label=r"\textit{DR}")

plt.plot(datax,datay.transpose()[0],label=r"\textit{THD}")
plt.plot(datax,datay.transpose()[1],label=r"\textit{SNR}")
plt.plot(datax,datay.transpose()[2],label=r"\textit{DR}")



#plt.yticks(np.linspace(-3,3,7))
#plt.xticks(np.logspace(1, 3, 7))
#plt.xscale('log')
plt.xlabel(r"\textit{frequency [GHz]}",fontsize=16)

plt.ylabel(r"\textit{[dB]}",fontsize=16)
plt.title(r"\textit{THD, SNR and DR VS frequency }")
plt.legend()
plt.savefig("/home/cristian/csv/sallen_key_10GHz/pdf_files/"+filecsv[:-4]+".pdf")
plt.figure()
plt.show()

