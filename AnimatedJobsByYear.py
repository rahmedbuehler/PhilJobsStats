from math import pi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] = 'E:/Python/ffmpeg/bin/ffmpeg.exe'

jobs = [780,925,1039,1059,1273,1223,824,935,873,751,588,743,739,737,736,791,814]
year = []
for i in range(3,20):
	year.append(2000+i)
df = pd.DataFrame({'\nYear':year, 'Advertised Philosophy Jobs\n':jobs})

def augment(xold,yold,numsteps):
    xnew = []
    ynew = []
    for i in range(len(xold)-1):
        difX = xold[i+1]-xold[i]
        stepsX = difX/numsteps
        difY = yold[i+1]-yold[i]
        stepsY = difY/numsteps
        for s in range(numsteps):
            xnew = np.append(xnew,xold[i]+s*stepsX)
            ynew = np.append(ynew,yold[i]+s*stepsY)
    return xnew,ynew

augyear, augjobs = augment(year,jobs,20)
augdf = pd.DataFrame({'\nYear':augyear, 'Advertised Philosophy Jobs\n':augjobs})

# Initialize writer
writer = animation.FFMpegWriter(fps=45)
# Initialize Plt
#sns.set(style="darkgrid")
sns.set(style="whitegrid")
fig = plt.figure(figsize=(10,6))
plt.xlim(2003, 2020)
plt.ylim(0,1600)

def animate(i):
	data = augdf.iloc[:int(i+1)] #select data range
	p = sns.lineplot(x=data['\nYear'], y=data['Advertised Philosophy Jobs\n'], data=data, color="tab:blue")
	datascatter = df.iloc[:int(i/20)+1]
	if i>=319:
		datascatter = df
	sns.scatterplot(x=datascatter['\nYear'], y=datascatter['Advertised Philosophy Jobs\n'], data=datascatter, color="tab:blue")

ani = matplotlib.animation.FuncAnimation(fig, animate, frames=320, repeat=True)
#plt.show()
ani.save('C:/Users/rjBuehler/Desktop/JobsPerYear.mp4', writer=writer, dpi=400)