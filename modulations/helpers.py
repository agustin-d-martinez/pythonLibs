import numpy as np
from typing import Tuple, List, Union

BitsInput = Union[str, List[int], Tuple[int, ...], np.ndarray]

def _check_array(bits: BitsInput, min_len:int =1)->np.ndarray:
    """
    Normaliza y valida el arreglo de bits de entrada.
    Acepta:
        - string de bits: "101011"
        - lista o tupla: [1,0,1,1]
        - numpy array: np.array([1,0,1])

    Reglas:
        - Todos los elementos deben ser 0 o 1.
        - Se devuelve siempre un np.ndarray(dtype=np.int8).
        - Si la cantidad de bits es menor a min_len → error.

    Parámetros
    ----------
    bits : str | list | tuple | np.ndarray
        Secuencia de bits a validar.
    min_len : int, optional
        Longitud mínima exigida.

    Returns
    -------
    np.ndarray
        Arreglo de bits validado y normalizado.
    """
    if isinstance(bits, str):                       # String
        if not all(c in "01" for c in bits):
            raise ValueError(f"Array debe contener solo '0' y '1'.")
        arr = np.fromiter((int(c) for c in bits), dtype=np.int8)

    elif isinstance(bits, (list, tuple)):           # List / tuple   
        try:
            arr = np.array(bits, dtype=np.int8)
        except Exception:
            raise ValueError(f"Array debe ser una secuencia de bits (0 y 1).")

    elif isinstance(bits, np.ndarray):
        arr = bits.astype(np.int8, copy=False)

    else:
        raise ValueError(f"Array debe ser string, lista, tupla o numpy array.")

    if arr.ndim != 1:
        raise ValueError(f"Array debe ser un arreglo unidimensional.")
    if not np.all((arr == 0) | (arr == 1)):
        raise ValueError(f"Array contiene valores no válidos. Solo se admiten 0 y 1.")
    if len(arr) < min_len:
        raise ValueError(f"Array debe tener al menos {min_len} bits.")

    return arr

def _alternate_x(arr: np.ndarray, value: int) -> np.ndarray:
    out = arr.copy().astype(float)
    polarity = 1
    for i, val in enumerate(arr):
        if val == value:
            out[i] = value * polarity
            polarity = -polarity
    return out

def _NRZ(bits: np.ndarray, Tb: float, Fs: float) -> Tuple[np.ndarray, np.ndarray]:
    N = int(Tb * Fs)                            # muestras por bit
    signal = np.repeat([b for b in bits], N)
    t = np.arange(len(signal)) / Fs
    return t, signal

def _RZ(bits: np.ndarray, Tb: float, Fs: float) -> Tuple[np.ndarray, np.ndarray]:
    N = int(Tb * Fs)                            # muestras por bit
    half = N // 2
    signal = []
    for b in bits:
        signal.extend([b] * half + [0] * (N - half))
    t = np.arange(len(signal)) / Fs
    return t, signal

def _constelate(bits:np.ndarray, constelation:dict, samples_per_symbol:int) -> Tuple[np.ndarray, np.ndarray]:
    bitsXsym = len(next(iter(constelation.keys())))
    cant_sym = len(bits)//bitsXsym

    I = np.empty(cant_sym, dtype=float)
    Q = np.empty(cant_sym, dtype=float)
    for i in range(cant_sym):
        symbol = tuple(bits[i*bitsXsym:i*bitsXsym+bitsXsym])
        if symbol not in constelation:
            raise ValueError(f'simbolo {symbol} no esta en la constelacion.')
        I[i], Q[i] = constelation[symbol]
    
    I = np.kron(I, np.ones(samples_per_symbol))
    Q = np.kron(Q, np.ones(samples_per_symbol))

    return I, Q

def _padding(bits:np.ndarray, multiple:int, add:int=0 ) -> np.ndarray:
    extra = (-len(bits))%multiple
    if extra == 0:
        return bits
    pad = np.full(extra,add,dtype=int)
    return np.concatenate([bits, pad])

def _gray_code(n: int) -> int:
    return n ^ (n >> 1)
