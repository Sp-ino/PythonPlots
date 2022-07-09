#!/bin/python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams['text.usetex'] = True 
rcParams['font.family'] = 'Times New Roman'

dircsv="/home/cristian/csv/sallen_key_10GHz/csv_files/"
filecsv="csv_THDvsfat200m.csv"
filecsv2="csv_THDvsfat410m.csv"
data=np.genfromtxt(dircsv+filecsv,delimiter=',',skip_header=1)
data2=np.genfromtxt(dircsv+filecsv2,delimiter=',',skip_header=1)

datax=data[:,0]/(10**9)
datay=data[:,1:]
datax2=data2[1:,0]/(10**9)
datay2=data2[1:,1:]






# fig, (mod, phs) = plt.subplots(2)
# fig.suptitle('Frequency response')
# mod.plot(datax, datay.transpose()[0])
# phs.plot(datax, datay.transpose()[1])
# mod.set(xlabel=r"\textit{frequency [GHz]}", ylabel=r"Amplitude [dB]", xscale='log')
# phs.set(xlabel=r"\textit{frequency [GHz]}", ylabel=r"Angle [deg]", xscale='log')


fig, (thd, snr, dr) = plt.subplots(3)
fig.suptitle(r"\textit{THD, SNR and DR VS frequency}")

thd.plot(datax, datay.transpose()[0], label=r"\textit{@$V_{In_{dm}}=200mV$}" )
thd.plot(datax2, datay2.transpose()[0], label=r"\textit{@$V_{In_{dm}}=400mV$}" )

snr.plot(datax, datay.transpose()[1], label=r"\textit{@$V_{In_{dm}}=200mV$}" )
snr.plot(datax2, datay2.transpose()[1], label=r"\textit{@$V_{In_{dm}}=400mV$}" )

dr.plot(datax, datay.transpose()[2], label=r"\textit{@$V_{In_{dm}}=200mV$}" )
dr.plot(datax2, datay2.transpose()[2], label=r"\textit{@$V_{In_{dm}}=400mV$}" )

thd.set(xticks=(np.linspace(0, 10, 11)), ylabel=r"THD [dB]")
snr.set( xticks=(np.linspace(0, 10, 11)), ylabel=r"SNR [dB]")
dr.set( xticks=(np.linspace(0, 10, 11)), xlabel=r"\textit{frequency [GHz]}", ylabel=r"DR [dB]")
plt.legend()
#plt.yticks(np.linspace(50,100,11))
#plt.xticks(np.logspace(1, 3, 7))
#plt.xscale('log')
# plt.xlabel(r"\textit{frequency [GHz]}",fontsize=16)

# plt.ylabel(r"\textit{[$\frac{V}{\sqrt{Hz}}$]}",fontsize=16)
# plt.title(r"\textit{Noise Spectrum}")
# # plt.legend()
fig.tight_layout()
plt.savefig("/home/cristian/csv/sallen_key_10GHz/pdf_files/"+filecsv[:-4]+".pdf")
plt.figure()
plt.show()

