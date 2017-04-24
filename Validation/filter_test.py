import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv, sys

sys.path.append('../')

import recursive_filter


with open('output.csv','rb') as csvfile:
    unfiltered_data = np.genfromtxt(csvfile,delimiter=',')

unfiltered_data = unfiltered_data[:,:2]

Fs = 22000
Ts = 1./Fs
Fc = 500
filt_order = 4


time = unfiltered_data[:,:1]/Fs
unfiltered_data = unfiltered_data[:,1]



y_fitler = recursive_filter.recursive_filt(Fc,Fs,filt_order)
y_out = unfiltered_data[0]

for idx in np.arange(len(unfiltered_data)-1):
    y_out = np.append(y_out,y_fitler.iter(unfiltered_data[idx+1],(time[idx+1]-time[idx])))



f1, axarr1 = plt.subplots(2, sharex=True)
axarr1[0].plot(time,unfiltered_data)
axarr1[0].set_title('Unfiltered Chirp')
axarr1[1].plot(time,y_out)
axarr1[1].set_xlabel('Time (sec)')


n = len(unfiltered_data)
k = np.arange(n)
T = n/Fs
freq = k/T
freq = freq[range(n/2)]

Y_in_fft = abs(np.fft.fft(unfiltered_data, norm = "ortho")/float(n))
Y_in_fft = Y_in_fft/Y_in_fft.max()
Y_in_fft = 20*np.log10(Y_in_fft)
Y_in_fft = Y_in_fft[range(n/2)]

Y_out_fft = abs(np.fft.fft(y_out, norm = "ortho")/float(n))
Y_out_fft = Y_out_fft/Y_out_fft.max()
Y_out_fft = 20*np.log10(Y_out_fft)
Y_out_fft = Y_out_fft[range(n/2)]



f2, axarr2 = plt.subplots(2, sharex=True)
axarr2[0].set_xscale('log')
axarr2[0].plot(freq,Y_in_fft)
axarr2[0].set_title('Unfiltered Chirp')
axarr2[0].set_ylabel('|Y_in(freq)|')
axarr2[0].set_ylim((-80,0))
axarr2[1].set_xscale('log')
axarr2[1].plot(freq,Y_out_fft)
axarr2[1].set_xlabel('Freq (Hz)')
axarr2[1].set_ylabel('|Y_out(freq)|')
axarr2[1].set_ylim((-80,0))




plt.show()


