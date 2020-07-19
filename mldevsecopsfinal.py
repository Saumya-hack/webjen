import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
data=pd.read_csv('server_logs.csv',delimiter=' ',header=None)
dataset=data
dataset=dataset.drop(columns=[1,2,5,8,9])
c=0
for i in dataset[4]:
    dataset[4][c]=float(i[1:-1])
    c+=1
c=0
for i in dataset[3]:
    dataset[3][c]=float(int(i[13:15])*3600+int(i[16:18])*60+int(i[19:21]))
    c+=1
c=0
for i in dataset.columns:
    c=0
    for j in dataset[i]:
        if j=='-':
            dataset[i][c]=0
        c+=1
c=0
for i in dataset[0]:
    s=i.split('.')
    dataset[0][c]=float(int(s[0])*2**24+int(s[1])*2**16+int(s[2])*2**8+int(s[3])*2**0)
    c+=1
sc=StandardScaler()
data_scaled=sc.fit_transform(dataset)
model = KMeans(n_clusters=2)
ci=0
cj=0
for i in data_scaled:
    ci+=1
    for j in i:
        cj+=1
        if j is None:
            data_scaled[i][j]=0
model.fit(data_scaled)
pred  = model.fit_predict(data_scaled)
di0={}
di1={}
c=0
for i in data[0]:
    if pred[c]==0:
        if i not in di0.keys():
            di0[i]=1
        else:
            di0[i]+=1
    else:
        if i not in di1.keys():
            di1[i]=1
        else:
            di1[i]+=1
    c+=1
di={}
for i in data[0]:
    if i not in di:
        di[i]=0
for i in di.keys():
    if i in di0.keys() and i in di1.keys():
        if di0[i]>di1[i]:
            di[i]=0
        elif di0[i]<di1[i]:
            di[i]=1
        else:
            di[i]=0
    elif i in di0.keys() and i not in di1.keys():
        di[i]=0
    elif i not in di0.keys() and i in di1.keys():
        di[i]=1
    else:
        di[i]=0
        
data['cluster name'] = pred
lis=[]
for i in di.keys():
    if di[i]==0:
        lis.append(i)
for i in lis:
    print(i)