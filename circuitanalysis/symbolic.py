import numpy as np												# Math utilities
from sympy import symbols										# For symbolic resolution of problems
from sympy import cancel, simplify, Poly , summation , oo
from sympy import latex, inverse_laplace_transform , laplace_transform
from sympy import Expr											# For instance Verification
from scipy.signal import TransferFunction
from IPython.display import display, Math						# For prettier display of expresions

class symbolic:
	S = symbols('s')		# Símbolo para variable de Laplace.
	t = symbols('t')		# Símbolo para variable temporal.

	Z = symbols('Z')		# Símbolo para variable de Laplace discreto (transformada Z).
	n = symbols('n')		# Simbolo para variable discreta.

	def __init__(self):
		pass

	@staticmethod
	def Zinductor(L=1):
		"""
		Expreción de impedancia de un inductor.

		Args:
			L: Valor del inductor

		Returns:
			Expresión del inductor.
		"""
		return symbolic.S*L
	@staticmethod
	def Zcapacitor(C=1):
		"""
		Expreción de impedancia de un capacitor.

		Args:
			C: Valor del capacitor

		Returns:
			Expresión del capacitor.
		"""
		return 1/(symbolic.S*C)
	@staticmethod
	def Yinductor(L=1):
		"""
		Expreción de admitancia de un inductor.

		Args:
			L: Valor del inductor

		Returns:
			Expresión del inductor.
		"""
		return 1/(symbolic.S*L)
	@staticmethod
	def Ycapacitor(C=1):
		"""
		Expreción de admitancia de un capacitor.

		Args:
			C: Valor del capacitor

		Returns:
			Expresión del capacitor.
		"""
		return symbolic.S*C
	@staticmethod
	def laplace_transform(H_t):
		"""
		Devuelve la expresión Laplace de una función temporal.
		Args:
			H_t: Expresión en temporal (t) simbólica.
		
		Returns:
			Expresión en el el dominio de laplace (s) de la función.
		"""
		return laplace_transform(H_t , symbolic.t , symbolic.S)
	
	@staticmethod
	def inverse_laplace(H_s):               #Cuidado con funciones muy complejas acá
		"""
		Devuelve la expresión temporal de una función en Laplace.

		Args:
			H_s: Expresión en Laplace (s) de la función.
		
		Returns:
			Expresión en el tiempo (t) de la función.
		"""
		return inverse_laplace_transform(H_s, symbolic.S, symbolic.t)
	@staticmethod
	def z_transform(f_n):
		"""
		Calcula la transformada Z de la función discreta f(n) por definicion. 

		Args:
			f_n: Funcion discreta simbolica en variable n.
		"""
		return summation(f_n * symbolic.z**(-symbolic.n), (symbolic.n, 0, oo))

	@staticmethod
	def print_latex(expr , as_numden_poly = True):
		"""
		Escribe expresiones utilziando Latex.

		Args:
			expr: Expresión a escribir.
		"""
		expr = simplify(expr)
		if as_numden_poly : 
			num , den = expr.as_numer_denom()
			expr = cancel(num/den)    # Lo transforma en un cociente de polinomios. Eliminar en caso de no buscar eso.
		display(Math(latex(expr)))
		return None

	@staticmethod
	def eficaz(A):
		""" 
		Calcula el valor eficaz de A.
		
		Args:
			A: Función a calcular valor eficaz.
		"""
		return np.sqrt(np.mean(A**2))

	@staticmethod
	def paralelo(*Zargs):
		""" 
		Calcula el paralelo de los argumentos como inversa de suma de las inversas.
		
		Args:
			Zargs: Argumentos a realizar el paralelo.
		
		Returns:
			Valor del paralelo.
		"""
		if len(Zargs) == 0:
			raise ValueError("Se requiere al menos un impedancia para calcular el paralelo.")
		return 1/sum(1/arg for arg in Zargs)
	
	@staticmethod
	def SimbolicTransferFunction(numerator, denominator):
		"""
		Crea una función simbólica de transferencia en el dominio de Laplace.

		Args:
			numerator: Expresión simbólica del numerador.
			denominator: Expresión simbólica del denominador.

		Returns:
			Función de transferencia simplificada.
		"""
		return simplify(numerator / denominator)
	@staticmethod
	def NumericTransferFunction(numerator, denominator):
		"""
		Crea una función numérica scipy de transferencia en el dominio de Laplace.

		Args:
			numerator: Lista de Coeficientes del numerador.
			denominator: Lista de Coeficientes del denominador.

		Returns:
			Función de transferencia simplificada.
		"""
		return TransferFunction(numerator, denominator)

	@staticmethod
	def TransferFunction(numerator, denominator):
		"""
		Crea una función de transferencia.

		Args:
			numerator: Expresión simbólica o lista de coeficientes del numerador.
			denominator: Expresión simbólica o lista de coeficientes del denominador.

		Returns:
			Si los argumentos son simbólicos: Función de transferencia simbólica simplificada.
			Si los argumentos son numéricos: Objeto TransferFunction de scipy.signal.
		"""
		if isinstance(numerator, Expr) and isinstance(denominator, Expr):	# Verificar si los argumentos son simbólicos
			return simplify(numerator / denominator)
		elif isinstance(numerator, (list, tuple)) and isinstance(denominator, (list, tuple)):	# Verificar si los argumentos son numéricos (listas o arrays)
			return TransferFunction(numerator, denominator)
		else:
			raise TypeError("Los argumentos deben ser expresiones simbólicas o listas de coeficientes numéricos")


	def to_numeric_coeffs(H_s):
		"""
		Convierte una función de transferencia simbólica en coeficientes numéricos.

		Args:
			H_s: Función de transferencia simbólica (numerador/denominador).

		Returns:
			num_coeffs: Lista de coeficientes numéricos del numerador.
			den_coeffs: Lista de coeficientes numéricos del denominador.
		"""
		if not isinstance(H_s, Expr):
			print("H_s No es una expresion simbólica")
			return 

		H_s = simplify(H_s)	# Simplificar la función de transferencia

		num, den = H_s.as_numer_denom()		# Separar numerador y denominador
		
		free_vars = list(H_s.free_symbols)
		var = free_vars[0]					# Utiliza el primer simbolo que encuentre

		num_poly = Poly(num, var)	# Extraer coeficientes polinómicos
		den_poly = Poly(den, var)

		# Convertir coeficientes a números (float)
		num_coeffs = [float(c) for c in num_poly.all_coeffs()]
		den_coeffs = [float(c) for c in den_poly.all_coeffs()]

		return num_coeffs, den_coeffs

	def to_symbolic_transfer(H_tf, symbol = None):
		"""
		Convierte una TransferFunction numérica en una función de transferencia simbólica.

		Args:
			H_tf: Instancia de scipy.signal.TransferFunction.

		Returns:
			Función de transferencia simbólica.
		"""
		if not isinstance(H_tf, TransferFunction):
			raise TypeError("H_tf debe ser una instancia de scipy.signal.TransferFunction")

		if symbol is None:
			symbol = symbolic.S
		# Extraer coeficientes del numerador y denominador
		numerator_coeffs = H_tf.num
		denominator_coeffs = H_tf.den

		# Construir polinomios simbólicos
		numerator_poly = sum(c * symbol**i for i, c in enumerate(reversed(numerator_coeffs)))
		denominator_poly = sum(c * symbol**i for i, c in enumerate(reversed(denominator_coeffs)))

		return numerator_poly / denominator_poly
