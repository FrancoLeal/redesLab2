import numpy as np
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write
from scipy import fft, arange, ifft
from scipy.fftpack import fftfreq, fftshift
from scipy import signal

import matplotlib.pyplot as plt

def abrirArchivo():
	rate,info = read("beacon.wav")
	print("El rate del archivo es: " + str(rate))
	#print(info)

	dimension = info[0].size
	#print(dimension)  

	if dimension == 1:
		data = info
		perfect = 1
	else:
		data = info[:,dimension-1]
		perfect = 0
	return data,rate

data,rate = abrirArchivo()
fs = rate
f, t, Sxx = signal.spectrogram(data,fs)
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()