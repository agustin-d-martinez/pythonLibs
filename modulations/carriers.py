import numpy as np
from typing import Tuple

def carrier(I:np.ndarray, Q:np.ndarray, t:np.ndarray, fc:float, Tmax:float = None, fs:float = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Lleva I/Q de banda base a banda pasante real.

    Comportamiento:
    - Si no se pasa fs ni Tmax → usa t original sin remuestrear.
    - Si solo se pasa Tmax → recorta a Tmax.
    - Si se pasa fs → genera eje de 0→Tmax (o 0→t[-1] si Tmax=None).

    :param I: In-Phase array
    :type I: np.ndarray
    :param Q: Quadrature array
    :type Q: np.ndarray
    :param t: Vector de tiempo original
    :type t: np.ndarray
    :param fc: Frecuencia de portadora
    :type fc: float
    :param Tmax: Tiempo máximo de salida.
    :type Tmax: float, opcional
    :param fs: Frecuencia de muestreo deseada de salida
    :type fs: float, opcional

    :return: Time array and signal array.
    :rtype: Tuple[np.ndarray, np.ndarray]
    """
    I = np.asarray(I)
    Q = np.asarray(Q)
    t = np.asarray(t)

    if fs is None:
        Tmax = t if Tmax is None else t[t <= Tmax]
        I_res = np.interp(t_out, t, I)
        Q_res = np.interp(t_out, t, Q)

    else:
        if Tmax is None:
            Tmax = t[-1]

        dt = 1/fs
        t_out = np.arange(0, Tmax, dt)

        I_res = np.interp(t_out, t, I)
        Q_res = np.interp(t_out, t, Q)

    phase = 2 * np.pi * fc * t_out
    out = I_res * np.cos(phase) - Q_res * np.sin(phase)

    return t_out, out

