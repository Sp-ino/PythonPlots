#!/bin/python
import numpy as np
import matplotlib.pyplot as plt

x=np.genfromtxt("../CSV_files/PICO_PUF/cdsB9MW/130nmMMePROC200x12814072021.csv",delimiter=',',skip_header=1)
res=x[:,4::]
res[res<0.6]=0
res[res>0.6]=1
niter=200
bias=np.zeros(niter)
devstd=np.zeros(niter)
for i in range(niter):
    bias[i]=(np.mean(res[i,:]))*100
    devstd[i]=(np.std(res[i,:]))

print("la media totale è: ",np.mean(bias),"\n")

for i in range(niter):
    bias[abs(bias-i)<1]=i
    devstd[abs(devstd-i)<1]=i*100
    
print("la deviazione standard sulle medie è: ",np.std(bias),"\n")   

plt.hist(bias,bins=20)
plt.title("bias")
plt.figure()
plt.show()
HD_inter=np.zeros((niter//2)*(niter-1));
res= np.array(res, dtype=int)
m=0
for i in range(niter):
    for j in range (i+1,niter):
        dist=np.count_nonzero(np.bitwise_xor(res[i,:],res[j,:]))
        HD_inter[m]=(dist/128)*100
        m=m+1        
        
plt.hist(HD_inter,bins=40)
plt.title("HD_inter")
plt.figure()
plt.show()

print("la media sull'HD_inter è: ",np.mean(HD_inter),"\n")

np.savez_compressed("PUF28",mediatotale=np.mean(bias),devstdsumedie=np.std(bias),mediaHD_inter=np.mean(HD_inter))
