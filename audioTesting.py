import matplotlib.pyplot as plt 
from matplotlib import animation
import numpy as np
import wave

path = r"C:\Users\zanyi\Documents\GitHub\AIMV\chaseAtlantic.wav"

# reading the audio file 
raw = wave.open(path) 
signal = raw.readframes(-1) 
signal = np.frombuffer(signal, dtype ="int16") 
f_rate = raw.getframerate() 
time = np.linspace( 
        0, #start 
        len(signal) / f_rate, 
        num = len(signal) 
    ) 
fig, ax = plt.subplots()
# title of the plot 
plt.title("Sound Wave") 
plt.xlabel("Time") 
line2 = ax.plot(time[0], signal[1900])[0]
interval = 7000
a,b = min(signal), max(signal)
def update(frame):
    # for each frame, update the data stored on each artist.
    x=time[frame:frame+interval]
    y= signal[frame:frame+interval]
    print(y)
    ax.set(xlim=[min(x),max(x)], ylim=[min(y),max(y)], xlabel='Time [s]', ylabel='Z [m]')
    line2.set_xdata(x)
    line2.set_ydata(y)
    return (line2)

ani = animation.FuncAnimation(fig=fig, func=update, frames=f_rate, interval=0)
plt.show()

