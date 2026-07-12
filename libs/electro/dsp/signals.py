import numpy as np
from numpy.typing import ArrayLike

def sin(vmax : float = 1,
        dc : float= 0,
        ff : float = 1,
        ph : float = 0,
        nn : int = 100,
        fs : float = 1000 
        ) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a sampled sine wave.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the sine wave.
    dc : float, default=0
        DC offset.
    ff : float, default=1
        Signal frequency in Hz.
    ph : float, default=0
        Initial phase in radians.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = vmax * np.sin(2*np.pi*ff*tt + ph) + dc
    xx = np.array(xx)

    return tt, xx

def square(vmax : float = 1,
           dc : float = 0,
           ff : float = 1,
           duty : float = .5,
           nn : int = 100,
           fs : float = 1000
           ) -> tuple[np.ndarray, np.ndarray] :
    """
    Generate a sampled square wave.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the waveform.
    dc : float, default=0
        DC offset.
    ff : float, default=1
        Signal frequency in Hz.
    duty : float, default=0.5
        Duty cycle expressed as a fraction between 0 and 1.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = np.where(tt % (1/ff) < (1/ff) * duty, 1, -1)
    xx = vmax * xx + dc
    #signal.square(2* np.pi * ff* tt, duty)

    xx = np.array(xx)

    return tt, xx

def sawtooth(vmax : float = 1,
             dc : float = 0,
             ff : float = 1,
             nn : int = 1,
             fs : float = 1000
             ) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a sampled sawtooth waveform.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the waveform.
    dc : float, default=0
        DC offset.
    ff : float, default=1
        Signal frequency in Hz.
    nn : int, default=1
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop= nn*ts, step=ts)
    T = 1/ff

    xx = [((vmax/T) * (i%T) + dc) for i in tt]
    #signal.sawtooth(2* np.pi * ff* tt, 0.5)

    xx = np.array(xx)

    return tt, xx

def triangle(vmax : float = 1,
             dc : float = 0,
             ff : float = 1,
             duty : float = 0.5,
             nn : int = 1,
             fs : float = 1000
             ) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a sampled triangular waveform.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the waveform.
    dc : float, default=0
        DC offset.
    ff : float, default=1
        Signal frequency in Hz.
    duty : float, default=0.5
        Fraction of the period used for the rising edge.
    nn : int, default=1
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop= nn*ts, step=ts)
    T = 1/ff

    xx = np.where(tt % T < duty*T, (vmax/(duty*T)) * (tt % T) + dc, (-vmax/(1-duty)) * (1 - (tt % T)/T) + dc)

    xx = np.array(xx)

    return tt, xx

def noise_generator(var : float = 1, nn : int = 100, fs : float = 1000) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate white Gaussian noise.

    Parameters
    ----------
    var : float, default=1
        Noise variance.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    xx : ndarray
        Noise samples.

    Notes
    -----
    The generated noise has zero mean and variance equal to ``var``.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = np.random.normal(loc=0, scale=np.sqrt(var), size=nn)
    xx = np.array(xx)

    return tt, xx

def noisy_sin(vmax : float = 1,
              dc : float = 0,
              ff : float = 1,
              ph : float = 0,
              nn : int = 100,
              fs : float = 1000,
              snr : float = 20) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate a sine wave corrupted by additive white Gaussian noise.

    The noise power is adjusted to achieve the specified signal-to-noise
    ratio (SNR).

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the sine wave.
    dc : float, default=0
        DC offset.
    ff : float, default=1
        Signal frequency in Hz.
    ph : float, default=0
        Initial phase in radians.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.
    snr : float, default=20
        Signal-to-noise ratio in dB.

    Returns
    -------
    xx : ndarray
        Noisy signal samples.
    tt : ndarray
        Time vector.
    """
    tt, xx = sin(vmax=vmax, dc=dc, ff=ff, ph=ph, nn=nn, fs=fs)
    pot_signal = np.mean(xx**2)
    var_noise = pot_signal / (10**(snr/10))
    
    _, noise = noise_generator(var_noise, nn, fs)
    xx = xx + noise

    return tt, xx

def kronecker_delta(n : int) -> np.ndarray:
    """
    Generate a discrete Kronecker delta sequence.

    Parameters
    ----------
    n : int
        Length of the sequence.

    Returns
    -------
    ndarray
        Sequence whose first sample is equal to one and all remaining
        samples are zero.
    """
    delta = np.zeros(n)
    delta[0] = 1

    return delta

def delay_signal(xx : ArrayLike, delay: int) -> np.ndarray:
    """
    Delay a discrete-time signal.

    The signal is shifted forward by the specified number of samples,
    inserting zeros at the beginning.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    delay : int
        Delay in samples.

    Returns
    -------
    ndarray
        Delayed signal.
    """
    y = np.zeros_like(xx)
    y[delay:] = xx[:-delay]
    return y
