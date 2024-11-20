import matplotlib.pyplot as plt 
import numpy as np 
import wave

# shows the sound waves 
def visualize(path: str): 
    
    # reading the audio file 
    raw = wave.open(path) 
      
    # reads all the frames  
    # -1 indicates all or max frames 
    signal = raw.readframes(1700) 
    signal = np.frombuffer(signal, dtype ="int16") 
      
    # gets the frame rate 
    f_rate = raw.getframerate() 
  
    # to Plot the x-axis in seconds  
    # you need get the frame rate  
    # and divide by size of your signal 
    # to create a Time Vector  
    # spaced linearly with the size  
    # of the audio file 
    time = np.linspace( 
        0, # start 
        len(signal) / f_rate, 
        num = len(signal) 
    ) 

    plt.subplot(1,2,1)

    plt.plot(time, signal) 
      
    # title of the plot 
    plt.title("Sound Wave") 
      
    # label of x-axis 
    plt.xlabel("Time") 
    
    plt.subplot(1,2,2)
    # actual plotting 
    
    # title of the plot 
    plt.title("Sound Wave") 
      
    # label of x-axis 
    plt.xlabel("Time") 
    # shows the plot  
    # in new window 
    plt.show() 
  
  
if __name__ == "__main__": 
    
    # gets the command line Value 
    path = r"C:\Users\zanyi\Documents\GitHub\AIMV\chaseAtlantic.wav"
  
    visualize(path)
    
    