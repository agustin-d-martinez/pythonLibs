from sympy import (Symbol, symbols, Expr,  
                   latex, cancel, simplify, Poly , summation , 
                   oo,
                   lambdify, 
                   Heaviside, DiracDelta,)
from sympy import sin as _sym_sin
from sympy import cos as _sym_cos

from sympy.integrals.transforms import laplace_transform as _laplace_transform
from sympy.integrals.transforms import inverse_laplace_transform as _inverse_laplace_transform

import scipy.signal as  sig
import numpy as np

from IPython.display import display, Math

### Symbols of variables ################################################
s : Symbol = symbols('s')		# symbol of laplace domain.
t : Symbol = symbols('t')		# symbol of temporal domain.

z : Symbol = symbols('z')		    # symbol of discrete-laplace domain (z-transform).
n : Symbol = symbols('n')		# symbol of discrete temporal domain.

def step(t: Expr | Symbol) -> Expr:
    return Heaviside(t)

def delta(t : Expr | Symbol) -> Expr:
    return DiracDelta(t)

def ramp(t : Expr | Symbol) -> Expr:
    return t * Heaviside(t) 

def sin(t: Expr | Symbol) -> Expr:
    return _sym_sin(t)

def cos(t: Expr | Symbol) -> Expr:
    return _sym_cos(t)


def Z_inductor(L : float = 1) -> Expr:
    """
    Expreción de impedancia de un inductor.

    Args:
        L: Valor del inductor

    Returns:
        Expresión del inductor.
    """
    return s*L

def Z_capacitor(C : float = 1) -> Expr:
    """
    Expreción de impedancia de un capacitor.

    Args:
        C: Valor del capacitor

    Returns:
        Expresión del capacitor.
    """
    return 1/(s*C)

def Y_inductor(L : float = 1) -> Expr:
    """
    Expreción de admitancia de un inductor.

    Args:
        L: Valor del inductor

    Returns:
        Expresión del inductor.
    """
    return 1/(s*L)

def Y_capacitor(C : float = 1) -> Expr:
    """
    Expreción de admitancia de un capacitor.

    Args:
        C: Valor del capacitor

    Returns:
        Expresión del capacitor.
    """
    return s*C

def z_transform(f_n : Expr) -> Expr:
    """
    Calcula la transformada Z de la función discreta f(n) por definicion. 

    Args:
        f_n: Funcion discreta simbolica en variable n.
    """
    return summation(f_n * z**(-n), (n, 0, oo))

def print_latex(expr : Expr , as_numden_poly = True) -> None:
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

def to_numeric_coeffs(H_s : Expr) -> tuple[float, float]:
    """
    Convierte una función de transferencia simbólica en coeficientes numéricos.

    Args:
        H_s: Función de transferencia simbólica (numerador/denominador).

    Returns:
        num_coeffs: Lista de coeficientes numéricos del numerador.
        den_coeffs: Lista de coeficientes numéricos del denominador.
    """
    if not isinstance(H_s, Expr):
        raise TypeError("H_s must be Expr.")

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

def to_signal_function(H : Expr, x: Symbol):
    f = lambdify(x, H)

def to_freq_response(H_s : Expr, f_axis : list | None = None) -> np.ndarray:
    if f_axis is None:
        f_axis = np.linspace(0, 10e3, 5000)
    
    f = lambdify(s, H_s)
    return f(1j* 2*np.pi * f_axis)


def to_time_response(h_t : Expr, t_axis : list | None = None) -> np.ndarray:
    if t_axis is None:
        t_axis = np.linspace(0, 10, 5000)
    
    f = lambdify(t, h_t)
    return f(t_axis)

def from_scipy_transferfunc(H_tf : sig.TransferFunction, symbol = None) -> Expr:
    """
    Convierte una TransferFunction numérica en una función de transferencia simbólica.

    Args:
        H_tf: Instancia de scipy.signal.TransferFunction.

    Returns:
        Función de transferencia simbólica.
    """
    if not isinstance(H_tf, sig.TransferFunction):
        raise TypeError("H_tf must be scipy.signal.TransferFunction")

    if symbol is None:
        symbol = s
    # Extraer coeficientes del numerador y denominador
    numerator_coeffs = H_tf.num
    denominator_coeffs = H_tf.den

    # Construir polinomios simbólicos
    numerator_poly = sum(c * symbol**i for i, c in enumerate(reversed(numerator_coeffs)))
    denominator_poly = sum(c * symbol**i for i, c in enumerate(reversed(denominator_coeffs)))

    return numerator_poly / denominator_poly

def laplace(H_t: Expr) -> Expr:
    """
    Devuelve la expresión Laplace de una función temporal.
    Args:
        H_t: Expresión en temporal (t) simbólica.
    
    Returns:
        Expresión en el el dominio de laplace (s) de la función.
    """
    return _laplace_transform(H_t , t , s)

def ilaplace(H_s : Expr) -> Expr:               #Cuidado con funciones muy complejas acá
    """
    Devuelve la expresión temporal de una función en Laplace.

    Args:
        H_s: Expresión en Laplace (s) de la función.
    
    Returns:
        Expresión en el tiempo (t) de la función.
    """
    return _inverse_laplace_transform(H_s, s, t)

