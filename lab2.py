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

def plotSpecgram(data,rate,title):
	NFFT = 1024
	Pxx, freqs, bins, im = plt.specgram(data,NFFT,Fs=rate)
	plt.title(title)
	plt.ylabel("Frecuencia [hz]")
	plt.show()

def menu():
	try:
		data,rate = abrirArchivo()
	except:
		print("Error al leer el archivo")

	timp = len(data)/rate
	t=linspace(0,timp,len(data))

	nyq_rate = rate / 2
	cutoff_hz=1000
	cutoff_hz_sup=3000
	numtaps=1001

	opcion=1
	while opcion != 0:
		print("""Menú:
		1.- Mostrar audio original
		2.- Mostrar espectograma del audio original
		3.- Aplicar filtro paso bajo (mostrar espectrograma y guardar archivo)
		4.- Aplicar filtro paso banda (mostrar espectrograma y guardar archivo)
		5.- Aplicar filtro paso alto (mostrar espectrograma y guardar archivo)
		6.- Salir""")
		try:
			opcion = int(input("Ingrese una opción: "))
		except:
			opcion = 6
		if opcion==1:
			graficar("Audio","Tiempo [s]","Amplitud",t,data)
		elif opcion==2:
			print("--------------")
			plotSpecgram(data,rate,"Espectograma señal original")
			print("--------------")
		elif opcion==3:
			print("--------------")
			fircoef1_low = signal.firwin(numtaps,cutoff_hz/nyq_rate, window = "hamming")
			filtered_x = lfilter(fircoef1_low,1.0,data)
			write("salidaPasoBajo.wav",rate,filtered_x)
			print("Archivo de salida creado")
			plotSpecgram(filtered_x,rate,"sample")
			graficar("sampletitle","samplex","sampley",t,filtered_x)
			print("--------------")
		elif opcion==4:
			print("--------------")
			fircoef1_band = signal.firwin(numtaps,cutoff = [cutoff_hz/nyq_rate, cutoff_hz_sup/nyq_rate],window = "hamming", pass_zero=False)
			filtered_x = lfilter(fircoef1_band,1.0,data)
			write("salidaPasoBanda.wav",rate,filtered_x)
			print("Archivo de salida creado")
			plotSpecgram(filtered_x,rate,"sample")
			graficar("sampletitle","samplex","sampley",t,filtered_x)
			print("--------------")
		elif opcion==5:
			print("--------------")
			fircoef1_high = signal.firwin(numtaps,cutoff_hz/nyq_rate,window = "hamming", pass_zero=False)
			filtered_x = lfilter(fircoef1_high,1.0,data)
			write("salidaPasoAlto.wav",rate,filtered_x)
			print("Archivo de salida creado")
			plotSpecgram(filtered_x,rate,"sample")
			graficar("sampletitle","samplex","sampley",t,filtered_x)
			print("--------------")
		elif opcion > 6 or opcion < 1:
			print("Opcion no valida, intente otra vez")
		elif opcion == 6:
			opcion = 0
			print("Salir")

"""
data,rate = abrirArchivo()
timp = len(data)/rate
t=linspace(0,timp,len(data))


Tdata,frq = fourier(data,rate)

graficar("sampletitle","samplex","sampley",t,data)


plotSpecgram(data,rate)
nyq_rate = rate / 2
cutoff_hz=3000
cutoff_hz_sup=6000
numtaps=1001

fircoef1_high = signal.firwin(numtaps,cutoff_hz/nyq_rate, pass_zero=False)

fircoef1_low = signal.firwin(numtaps,cutoff_hz/nyq_rate)

fircoef1_band = signal.firwin(numtaps,cutoff = [cutoff_hz/nyq_rate, cutoff_hz_sup/nyq_rate])


filtered_x = lfilter(fircoef1_band,1.0,data)

plotSpecgram(filtered_x,rate)

graficar("sampletitle","samplex","sampley",t,filtered_x)

write("salida.wav",rate,filtered_x)
"""

menu()