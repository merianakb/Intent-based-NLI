from math import sqrt

tab=[]
i=0
N=100
n=16
avg= 0.9772

while i<84:
    tab.append(1)
    i=i+1

tab.append(0.85)
tab.append(0.85)
tab.append(0.79)
tab.append(0.85)
tab.append(0.79)
tab.append(0.79)
tab.append(0.79)
tab.append(0.75)
tab.append(0.85)
tab.append(0.75)
tab.append(0.75)
tab.append(0.8)
tab.append(0.8)
tab.append(0.8)
tab.append(0.66)
tab.append(0.85)

sum=0
i=0

while i<100:
    sum=sum+((tab[i]-avg)**2)
    i=i+1

print(sqrt(sum/100))

