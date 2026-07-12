import numpy as np
from numpy.typing import ArrayLike 
from .signals import delay_signal

def complementary_delay_filter(xx : ArrayLike, 
                               xx_filtered : ArrayLike, 
                               delay: int
                               ) -> np.ndarray:
    """
    Compute the complementary response of a delayed filter.

    The complementary output is defined as

        y[n] = x[n-delay] - x_filtered[n]

    where the delayed input is aligned with the filtered signal.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    xx_filtered : ArrayLike
        Filtered version of the input signal.
    delay : int
        Filter group delay in samples.

    Returns
    -------
    ndarray
        Complementary filtered signal.
    """
    hp = np.zeros_like(xx_filtered)
    hp[delay:] = xx[:-delay] - xx_filtered[delay:]

    return hp

def recursive_moving_average(xx : ArrayLike , 
                             window_lenght : int, 
                             interpolation : int = 1,
                             axis : int = -1 
                             ) -> np.ndarray:
    """
    Apply a recursive moving average filter.

    The filter computes the moving average over a window of ``N`` samples
    using a recursive implementation with constant computational complexity
    per output sample after initialization.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    window_lenght : int
        Length of the moving average window.
    interpolation : int, default=1
        Interpolation factor between successive samples.

    Returns
    -------
    ndarray
        Filtered signal.

    Notes
    -----
    The recursive difference equation is

        y[n] = y[n-L] + (x[n] - x[n-NL]) / N
    """
    xx = np.asarray(xx)
    y = np.zeros_like(xx)
    N = xx.shape[-1]
    
    for n in range(N):
        x_n_N = xx[n-window_lenght*interpolation] if n >= window_lenght*interpolation else 0.0
        y_old = y[n-interpolation] if n >= interpolation else 0.0

        y[n] = y_old + (xx[n] - x_n_N)/window_lenght             # Funcion de diferencia recursiva para promedio movil
    return y

def lyons_lowpass(xx : ArrayLike, N : int, C : int = 2, L : int = 1) -> np.ndarray:
    """
    Apply a recursive Lyons low-pass filter.

    The filter consists of ``C`` cascaded recursive moving average filters.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    N : int
        Order of the filter.
    C : int, default=2
        Number of cascaded stages.
    L : int, default=1
        Interpolation factor.

    Returns
    -------
    ndarray
        Low-pass filtered signal.

    Notes
    -----
    The transfer function is

        H(z) = (z^(-M) (1/N) (1-z^-N)/(1-z^-1))^C
    """
    if L == 0:
        raise ValueError("L must be greater than 0.")
    
    # Check imputs
    xx = np.asarray(xx, dtype=float)

    # Apply the recursive moving average filter C times. 
    tr = xx.copy()
    for _ in range(C):
        tr = recursive_moving_average(tr, N, L)

    return tr

def lyons_highpass(xx : ArrayLike, N : int, C : int = 2, interpolation : int = 1) -> np.ndarray:
    """
    Apply a recursive Lyons high-pass filter.

    The high-pass response is obtained by subtracting the low-pass output
    from a properly delayed version of the input signal.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    N : int
        Order of the filter.
    C : int, default=2
        Number of cascaded stages.
    interpolation : int, default=1
        Interpolation factor.

    Returns
    -------
    ndarray
        High-pass filtered signal.

    Notes
    -----
    The transfer function is

        H(z) = z^(-MC) - (z^(-M) (1/N) (1-z^-N)/(1-z^-1))^C
    """
    if interpolation == 0:
        raise ValueError("L must be greater than 0.")
    # Check imputs
    xx = np.asarray(xx, dtype=float)

    # delay value
    delay =  C*interpolation*(N-1)/2
    if delay != int(delay) :
        raise ValueError("Delay must M be an int. Ensure that C is even when N is even.")
    delay = int(delay)

    # Apply the recursive moving average filter C times. 
    tr = xx.copy()
    for _ in range(C):
        tr = recursive_moving_average(tr, N, interpolation)

    # Delayed input signal
    xd = delay_signal(xx, delay)

    return xd - tr

def delay_lyons_filter(N : int, C : int = 2, interpolation : int = 1, fs : float = 1) -> int:
    """
    Compute the group delay of a Lyons filter.

    Parameters
    ----------
    N : int
        Length of each moving average stage.
    C : int, default=2
        Number of cascaded stages.
    interpolation : int, default=1
        Interpolation factor.

    Returns
    -------
    int
        Filter delay in samples.
    """
    if interpolation == 0:
        raise ValueError("L debe ser mayor que 0.")

    delay =  C*interpolation*(N-1)/2
    if delay != int(delay) :
        raise ValueError("Delay M must be an int. Ensure that C is even when N is even.")

    return delay/fs