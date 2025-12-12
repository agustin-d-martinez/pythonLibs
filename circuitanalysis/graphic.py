import numpy as np												# Math utilities
import matplotlib.pyplot as plt                                 # For graph and plot of functions
from sympy import Poly											# For symbolic resolution of problems
from scipy import signal                                        # Signals utilities
from sympy import Expr

from .symbolic import symbolic

class graphic:
	@staticmethod
	def pole_zero_plot(H_tf):
		"""
		Grafica el diagrama de polos y ceros de una función de transferencia.

		Args:
			H_tf: Instancia de scipy.signal.TransferFunction.

		Returns:
			(zeros, poles): Numpy arrays con los ceros y polos.
		"""
		if isinstance(H_tf, Expr):
			num_coeffs, den_coeffs = symbolic.to_numeric_coeffs(H_tf)		# Convertir la función simbólica a coeficientes numéricos
			H_tf = signal.TransferFunction(num_coeffs, den_coeffs)		# Crear la función de transferencia para scipy
		elif not isinstance(H_tf, signal.TransferFunction):
			raise TypeError("H_tf debe ser una instancia de scipy.signal.TransferFunction")
		
		# Obtener polos y ceros
		zeros, poles, _ = signal.tf2zpk(H_tf.num, H_tf.den)
		
		# Crear el gráfico
		plt.figure()
		plt.axvline(0, color='k', lw=1)  # Eje vertical
		plt.axhline(0, color='k', lw=1)  # Eje horizontal
		
		plt.scatter(np.real(zeros), np.imag(zeros), color='b', marker='o', label='Ceros')  # Ceros en azul
		plt.scatter(np.real(poles), np.imag(poles), color='r', marker='x', label='Polos')  # Polos en rojo
		
		plt.title("Diagrama de Polos y Ceros")
		plt.xlabel("Re")
		plt.ylabel("Im")
		plt.grid(True)
		plt.legend()
		plt.axis('equal')  # Escala igual en ambos ejes
		plt.show()

		return zeros, poles

	@staticmethod
	def bodeMagnitude(H , w = None, plot_figure=True ):
		"""
		Genera el diagrama de Bode de Amplitud de una función de transferencia.

		Args:
			H: Función de transferencia.
			w: Vector de frecuencias. Si None, se calculará automáticamente.
			plot_figure: Mostrar o no la gráfica.

		Returns:
			mag, phase, w: Magnitud, fase y frecuencia.
		"""
		mag, phase, w = graphic.bode(H, w, False)

		if plot_figure:		# Graficar si se requiere
			plt.figure()
			plt.semilogx(w, mag)  # Eje x logarítmico
			plt.ylabel('Magnitud (dB)')
			plt.grid(True)
			plt.title('Diagrama de Bode')
			plt.show()

		return mag, w

	@staticmethod
	def bodePhase(H , w = None, plot_figure=True):
		"""
		Genera el diagrama de Bode de la fase de una función de transferencia.

		Args:
			H: Función de transferencia.
			w: Vector de frecuencias. Si None, se calculará automáticamente.
			plot_figure: Mostrar o no la gráfica.

		Returns:
			mag, phase, w: Magnitud, fase y frecuencia.
		"""
		mag, phase, w = graphic.bode(H, w, False)

		if plot_figure:		# Graficar si se requiere
			plt.figure()
			plt.title('Diagrama de Bode')
			plt.semilogx(w, phase)
			plt.ylabel('Fase (grados)')
			plt.xlabel('Frecuencia (rad/s)')
			plt.grid(True)
			plt.show()

		return phase, w

	def bode(H, w=None, plot_figure=True):
		"""
		Genera el diagrama de Bode de una función de transferencia.

		Args:
			H: Función de transferencia.
			w: Vector de frecuencias. Si None, se calculará automáticamente.
			plot_figure: Mostrar o no la gráfica.

		Returns:
			mag, phase, w: Magnitud, fase y frecuencia.
		"""
		if isinstance(H, Expr):  
			num_coeffs, den_coeffs = symbolic.to_numeric_coeffs(H)		# Convertir la función simbólica a coeficientes numéricos
			sys = signal.TransferFunction(num_coeffs, den_coeffs)		# Crear la función de transferencia para scipy
		elif isinstance(H, signal.TransferFunction):  
			sys = H  # Usar directamente la función de transferencia
		else:
			raise TypeError("La entrada debe ser una función simbólica (sympy.Expr) o una scipy TransferFunction")
		
		w, Hfreq = signal.freqresp(sys, w=w)	       # Calcular respuesta en frecuencia

		mag = 20 * np.log10(np.abs(Hfreq))		# Calcular magnitud y fase
		phase = np.angle(Hfreq, deg=True)

		if plot_figure:		# Graficar si se requiere
			plt.figure()
			plt.subplot(1, 2, 1)
			plt.semilogx(w, mag)  # Eje x logarítmico
			plt.ylabel('Magnitud (dB)')
			plt.grid(True)
			plt.title('Diagrama de Bode')
			plt.subplot(1, 2, 2)
			plt.semilogx(w, phase)
			plt.ylabel('Fase (grados)')
			plt.xlabel('Frecuencia (rad/s)')
			plt.grid(True)
			plt.show()

		return mag, phase, w

	@staticmethod
	def Zbode(H_z , w= None, plot_figure=True):
		if isinstance(H_z, Expr):  
			num_coeffs, den_coeffs = symbolic.to_numeric_coeffs(H_z)		# Convertir la función simbólica a coeficientes numéricos
		elif isinstance(H_z, signal.TransferFunction):  
			num_coeffs = H_z.num  # Usar directamente la función de transferencia
			den_coeffs = H_z.den
		else:
			raise TypeError("La entrada debe ser una función simbólica (sympy.Expr) o una scipy TransferFunction")
		
		w, Hfreq = signal.freqz(num_coeffs, den_coeffs)
		mag = 20 * np.log10(np.abs(Hfreq))		# Calcular magnitud y fase
		phase = np.angle(Hfreq, deg=True)

		if plot_figure:		# Graficar si se requiere
			plt.figure()
			plt.subplot(1, 2, 1)
			plt.semilogx(w, mag)  # Eje x logarítmico
			plt.ylabel('Magnitud (dB)')
			plt.grid(True)
			plt.title('Diagrama de Bode')
			plt.subplot(1, 2, 2)
			plt.semilogx(w, phase)
			plt.ylabel('Fase (grados)')
			plt.xlabel('Frecuencia (rad/s)')
			plt.grid(True)
			plt.show()

		return mag, phase, w
	@staticmethod
	def ZbodeMagnitude(H , w = None, plot_figure=True ):
		"""
		Genera el diagrama de Bode de Amplitud de una función de transferencia.

		Args:
			H: Función de transferencia.
			w: Vector de frecuencias. Si None, se calculará automáticamente.
			plot_figure: Mostrar o no la gráfica.

		Returns:
			mag, phase, w: Magnitud, fase y frecuencia.
		"""
		mag, phase, w = graphic.Zbode(H, w, False)

		if plot_figure:		# Graficar si se requiere
			plt.figure()
			plt.semilogx(w, mag)  # Eje x logarítmico
			plt.ylabel('Magnitud (dB)')
			plt.grid(True)
			plt.title('Diagrama de Bode')
			plt.show()

		return mag, w

	@staticmethod
	def ZbodePhase(H , w = None, plot_figure=True):
		"""
		Genera el diagrama de Bode de la fase de una función de transferencia.

		Args:
			H: Función de transferencia.
			w: Vector de frecuencias. Si None, se calculará automáticamente.
			plot_figure: Mostrar o no la gráfica.

		Returns:
			mag, phase, w: Magnitud, fase y frecuencia.
		"""
		mag, phase, w = graphic.Zbode(H, w, False)

		if plot_figure:		# Graficar si se requiere
			plt.figure()
			plt.title('Diagrama de Bode')
			plt.semilogx(w, phase)
			plt.ylabel('Fase (grados)')
			plt.xlabel('Frecuencia (rad/s)')
			plt.grid(True)
			plt.show()

		return phase, w
	@staticmethod
	def plot(x , Y , title=None , xlabel=None , ylabel=None, grid=False ):
		"""
		Grafica una función Y(x) utilizando MathPlotLib.

		Args:
			x: Vector de puntos eje X (horizontal).
			Y: Vector de puntos eje Y (vertical).
			title: Título del gráfico. Por defecto no tiene.
			xlabel: Título del eje X. Por defecto no tiene.
			ylabel: Título del eje Y. Por defecto no tiene.
			grid: Habilita la grilla. 
		"""
		plt.figure()
		plt.plot(x, Y)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.grid(grid)
		plt.title(title)
		plt.show()
		return None