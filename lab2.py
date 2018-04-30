import numpy as np
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write
from scipy import fft, arange, ifft
from scipy.fftpack import fftfreq, fftshift
from scipy import signal
from scipy.signal import convolve as sig_convolve, fftconvolve, lfilter, firwin
import time
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

def fourier(data,rate):
	timp=len(data)/rate
	Tdata = np.fft.fft(data)
	k = arange(-len(Tdata)/2,len(Tdata)/2)
	frq = k/timp
	frq=fftshift(frq)
	return Tdata,frq




NFFT = 1024
data,rate = abrirArchivo()
"""Pxx, freqs, bins, im = plt.specgram(data,NFFT,Fs=rate)
plt.show()"""
nyq_rate = rate / 2
cutoff_hz=1000
numtaps=1001
fircoef1 = signal.firwin(numtaps,cutoff_hz/nyq_rate)
Tdata = fourier(data,rate)
tstart = time.time()
conv_result = sig_convolve(Tdata, fircoef1[np.newaxis, :], mode='valid')
conv_time.append(time.time() - tstart)