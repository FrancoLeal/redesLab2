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

def graficar(title,xlabel,ylabel,X,Y):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(X, Y)
    print("Mostrando grafico")
    plt.show()

def plotSpecgram(data,rate):
	NFFT = 1024
	Pxx, freqs, bins, im = plt.specgram(data,NFFT,Fs=rate)
	plt.show()


data,rate = abrirArchivo()
timp = len(data)/rate
t=linspace(0,timp,len(data))


Tdata,frq = fourier(data,rate)

graficar("sampletitle","samplex","sampley",t,data)


plotSpecgram(data,rate)
nyq_rate = rate / 2
cutoff_hz=1000
numtaps=1001

fircoef1_high = signal.firwin(numtaps,cutoff_hz/nyq_rate, pass_zero=False)

fircoef1_low = signal.firwin(numtaps,cutoff_hz/nyq_rate)

filtered_x = lfilter(fircoef1,1.0,data)

#plotSpecgram(filtered_x,rate)

#graficar("sampletitle","samplex","sampley",t,filtered_x)

write("salida.wav",rate,filtered_x)