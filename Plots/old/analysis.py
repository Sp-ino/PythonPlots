import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x=pd.read_csv("./MonteCarlo.0.csv",delimiter=',',index_col=0)
x=x[x.columns[3:]]
data=x.to_numpy()
data[data>0.5]=1
data[data<=0.5]=0
res=np.zeros(int(data.shape[0]*(data.shape[0]-1)/2))
cnt=0
for i in range(data.shape[0]-1):
    for j in range(i+1,data.shape[0]):
        res[cnt]=np.count_nonzero(data[i,:]==data[j,:])/data.shape[1]*100
        cnt=cnt+1
print("Media Inter-HD\t mu=%.4f \t std=%.4f"%(np.mean(res),np.std(res)))
plt.hist(res,bins=10)
print("Media Bias\t mu=%.4f \t std=%.4f"%(np.mean(np.mean(data,axis=1)*100),np.std(np.mean(data,axis=1)*100)))
