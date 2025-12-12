import numpy as np												# Math utilities
from scipy import signal										# Signals utilities
from scipy.fft import fft as scipy_fft, fftfreq, next_fast_len	# FFT utilities

class fft_analisys:
	@staticmethod
	def validate_number_signal_list(x):
		if isinstance(x, (list, tuple)):
			x = np.array(x)  # Convertir a numpy array
		if not isinstance(x, np.ndarray):
			raise TypeError("El parámetro 'x' debe ser un numpy array, lista o tupla.")
		if not np.issubdtype(x.dtype, np.number):
			raise ValueError("El array 'x' debe contener valores numéricos.")
		if np.any(np.isnan(x)):
			raise ValueError("El array 'x' contiene valores NaN.")
		if np.any(np.isinf(x)):
			raise ValueError("El array 'x' contiene valores infinitos.")
		return x

	@staticmethod
	def FFT(x, fs, win=None, resolution=None):
		x = fft_analisys.validate_number_signal_list(x)
		if(fs <= 0):
			raise ValueError("La frecuencia de muestreo debe ser mayor a 0.")
		if(resolution is not None and resolution < 0):
			raise ValueError("La resolución no puede ser negativa.")

		# Ventaneo
		N = len(x)
		if win is None:
			w = np.ones(N)
		elif win == 'hann':         #Medir frecuencias
			w = signal.windows.hann(N)
		elif win == 'hamming':
			w = signal.windows.hamming(N)
		elif win == 'blackman':
			w = signal.windows.blackman(N)
		elif win == 'flattop':      #Medir amplitud
			w = signal.windows.flattop(N)
		else:
			raise ValueError(f"Ventana '{win}' no reconocida.")

		x = x * w
		errVentana = np.mean(w)

		#Largo final deseado (zero-padding)
		if resolution is not None:
			N = int(fs/resolution)

		N = next_fast_len(N)    #Mejora la velocidad del FFT

		#cálculo de FFT
		fftX = scipy_fft(x, N)
		freq = fftfreq(N, d=1/fs)

		return fftX, freq , errVentana

	@staticmethod
	def FFTabs(x, fs, win=None, full_spectrum=False, resolution=None):      # senal, freq = FFTabs(x, fs, 'flattop')
		"""
		Devuelve el FFT del módulo de una función.
		Args:
			x (Array-like): Señal a transformar.
			fs (Float): Frecuencia de muestreo.
			win (array-like, optional): Ventana a aplicar en la FFT.
			full_spectrum (bool, optional): Indica si se devuelve el espectro completo o solo frecuencias positivas.
			resolution (float, optional): Se indica la resolución mínima en frecuencia en caso de querer agregar muestras.

		returns:
			tuple:
				fftX (array): FFT del módulo de la señal.
				freq (array): Vector de frecuencias.
		"""
		fftX, freq, errVentana = fft_analisys.FFT(x,fs, win,resolution)
		fftX = np.abs(fftX) / (len(x)*errVentana)
		fftX [3:] *= 2                              # La continya no tiene el x2 (se agrega hasta 3 por distorcion de ventana)
		if not full_spectrum :
			fftX = fftX[:len(x)//2]
			freq = freq[:len(x)//2]
		return fftX, freq

	@staticmethod
	def FFTangle(x, fs, win=None, full_spectrum=False, resolution=None):
		fftX, freq, *_ = fft_analisys.FFT(x, fs, win, resolution)
		fftX = np.angle(fftX)
		if not full_spectrum :
			fftX = fftX[:len(x)//2]
			freq = freq[:len(x)//2]
		return fftX, freq

	@staticmethod
	def find_fundamental(freq, fftX, ignore_dc=True, threshold=None):
		"""
		Encuentra la frecuencia del armónico fundamental de una FFT. No realiza interpolación con una parábola.

		Args:
			freq (array): Eje de frecuencias.
			fftX (array): Magnitudes de la FFT.
			ignore_dc (bool): Si True, ignora el índice 0 (componente DC).
			threshold (float, optional): Valor mínimo de amplitud para considerar un pico.

		Returns:
			freq[idx_local] (float): Frecuencia del armónico fundamental.
			idx (int): Índice del armónico fundamental en fftX.
		"""
		# Ignorar la componente DC si es necesario
		start_idx = 3 if ignore_dc else 0                   #Considera DC a las primeras 3 frecuencias.

		# Aplicar umbral si se proporciona
		fftX_filtered = fftX[start_idx:]
		if threshold is not None:
			fftX_filtered[fftX_filtered < threshold] = 0

		# Índice del máximo
		idx_local = np.argmax(fftX_filtered) + start_idx

		return freq[idx_local], idx_local