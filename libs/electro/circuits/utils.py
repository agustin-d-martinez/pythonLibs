import numpy as np
from numpy.typing import ArrayLike

def parallel(x : ArrayLike) :
    y = None
    for arg in x:
        if y is None:
            y = arg
        else:
            y += 1/arg 
    return 1/y

def rms(xx : ArrayLike, *, axis : int = -1) -> float:
    return np.sqrt(np.mean(xx**2, axis=axis))

def power(xx : ArrayLike, *, axis : int = -1) -> float:
    """
    Compute the average power of a signal.

    The signal power is defined as the mean squared value of the samples.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    axis : int, default=-1
        Axis along which the autocorrelation is computed.
    Returns
    -------
    float
        Average signal power.
    """
    return np.mean(np.abs(xx)**2, axis=axis)

def snr(signal: ArrayLike, noise: ArrayLike, *, axis : int = -1) -> float:
    """
    Compute the signal-to-noise ratio (SNR).

    Parameters
    ----------
    signal : ArrayLike
        Signal component.
    noise : ArrayLike
        Noise component.
    axis : int, default=-1
        Axis along which the autocorrelation is computed.

    Returns
    -------
    float
        Signal-to-noise ratio in decibels (dB).
    """
    return 10 * np.log10(power(signal, axis=axis) / power(noise, axis=axis))

def voltage_db(xx: ArrayLike) -> np.ndarray:
    """
    Compute the magnitude of a quantity in decibels.

    The conversion is defined as
        20 log10(|x|)

    and is typically used for amplitudes or voltage ratios.

    Parameters
    ----------
    xx : ArrayLike
        Input values.

    Returns
    -------
    ndarray
        Magnitude expressed in decibels.
    """
    return 20*np.log10(np.abs(xx))

def power_db(xx: ArrayLike) -> np.ndarray:
    """
    Compute the power of a quantity in decibels.

    The conversion is defined as
        10 log10(|x|)

    and is typically used for power ratios.

    Parameters
    ----------
    xx : ArrayLike
        Input values.

    Returns
    -------
    ndarray
        Power expressed in decibels.
    """
    return 10*np.log10(np.abs(xx))

def quantizer(xx: ArrayLike, Vfs: float, bits: int = 4) -> np.ndarray:
    """
    Quantize a signal using a uniform ADC model.

    Samples are rounded to the nearest quantization level and clipped to
    the converter input range.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    Vfs : float
        Full-scale input voltage.
    bits : int, default=4
        ADC resolution in bits.

    Returns
    -------
    ndarray
        Quantized signal.
    """    
    q = Vfs/(2**bits) 
    xq = np.round(xx/q) * q

    vmax =  q*(2**(bits-1)-1)
    vmin = -q*2**(bits-1)

    np.clip(xq, vmin, vmax, out=xq)
    return xq

