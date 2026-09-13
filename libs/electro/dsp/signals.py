import numpy as np
from numpy.typing import ArrayLike
from functools import reduce

def time_axis(start : float = 0,  nn : int = 100, fs : float = 1000):
    """
    Generate the time axis off lenght nn and sampling fs.
    Parameters
    ----------
    start : float, default=0
        Initial time.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.
    Returns
    -------
    tt : ndarray
        Time vector.
    """
    return start + np.arange(stop=nn/fs, step=1/fs)

def sin(vmax : float = 1,
        dc : float= 0,
        ff : float = 1,
        ph : float = 0,
        nn : int = 100,
        fs : float = 1000 
        ) -> np.ndarray:
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
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = vmax * np.sin(2*np.pi*ff*tt + ph) + dc
    xx = np.array(xx)

    return xx

def rmmo(vmax : float = 1,
        ff : float = 1,
        ph : float = 0,
        alpha : float = 0,
        nn : int = 100,
        fs : float = 1000 
        ) -> np.ndarray:
    """
    Generate a Half-Wave Rectifier Sine.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the sine wave.
    ff : float, default=1
        Signal frequency in Hz.
    ph : float, default=0
        Initial phase in radians.
    alpha : float, default=0
        Angle of conductions in radians. From 0 to pi radians. 
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.
    Returns
    -------
    xx : ndarray
        Signal samples.
    """
    if alpha < 0 or alpha > np.pi:
        raise ValueError("Alpha must be in the range [0, pi] radians.")

    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = vmax * np.sin(2*np.pi*ff*tt + ph)
    if alpha == 0:
        return np.maximum(xx, 0)
    wt = 2*np.pi*ff*tt + ph
    cond = (xx > 0) & (wt % (2*np.pi) > alpha)
    xx = np.where(cond, xx, 0)
    return xx

def rmoc(vmax : float = 1,
        ff : float = 1,
        ph : float = 0,
        alpha : float = 0,
        nn : int = 100,
        fs : float = 1000 
        ) -> np.ndarray:
    """
    Generate a Full-Wave Rectifier Sine.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the sine wave.
    ff : float, default=1
        Signal frequency in Hz.
    ph : float, default=0
        Initial phase in radians.
    alpha : float, default=0
        Angle of conductions in radians. From 0 to pi radians. 
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.
    Returns
    -------
    xx : ndarray
        Signal samples.
    """
    if alpha < 0 or alpha > np.pi:
        raise ValueError("Alpha must be in the range [0, pi] radians.")

    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = abs(vmax * np.sin(2*np.pi*ff*tt + ph))
    if alpha == 0:
        return xx
    wt = 2*np.pi*ff*tt + ph
    cond = wt % np.pi > alpha
    xx = np.where(cond, xx, 0)
    return xx

def rtmo(vmax : float = 1,
        ff : float = 1,
        ph : float = 0,
        alpha : float = 0,
        nn : int = 100,
        fs : float = 1000 
        ) -> np.ndarray:
    """
    Generate a Three-Phase Half-Wave Rectifier Sine.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the sine wave.
    ff : float, default=1
        Signal frequency in Hz.
    ph : float, default=0
        Initial phase in radians.
    alpha : float, default=0
        Angle of conductions in radians. From 0 to 5/6pi radians.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.
    Returns
    -------
    xx : ndarray
        Signal samples.
    """
    if alpha < 0 or alpha > 5*np.pi/6:
        raise ValueError("Alpha must be in the range [0, 5/6pi] radians.")

    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    x1 = rmmo(vmax=vmax, ff=ff, ph=ph, alpha=np.pi/6 + alpha, nn=nn, fs=fs)
    x2 = rmmo(vmax=vmax, ff=ff, ph=ph + 2*np.pi/3, alpha=np.pi/6 + alpha, nn=nn, fs=fs)
    x3 = rmmo(vmax=vmax, ff=ff, ph=ph + 4*np.pi/3, alpha=np.pi/6 + alpha, nn=nn, fs=fs)
    xx = reduce(np.maximum, [x1, x2, x3])

    return xx

def rtoc(vmax : float = 1,
        ff : float = 1,
        ph : float = 0,
        alpha : float = 0,
        nn : int = 100,
        fs : float = 1000 
        ) -> np.ndarray:
    """
    Generate a Three-Phase Full-Wave Rectifier Sine.

    Parameters
    ----------
    vmax : float, default=1
        Peak amplitude of the sine wave.
    ff : float, default=1
        Signal frequency in Hz.
    ph : float, default=0
        Initial phase in radians.
    alpha : float, default=0
        Angle of conductions in radians. From 0 to 2/3pi radians.
    nn : int, default=100
        Number of samples.
    fs : float, default=1000
        Sampling frequency in Hz.
    Returns
    -------
    xx : ndarray
        Signal samples.
    """
    if alpha < 0 or alpha > 2*np.pi/3:
        raise ValueError("Alpha must be in the range [0, 2/3pi] radians.")

    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    x1 = rmoc(vmax=3**.5 * vmax, ff=ff, ph=ph - np.pi/6, alpha=np.pi/3 + alpha, nn=nn, fs=fs)
    x2 = rmoc(vmax=3**.5 * vmax, ff=ff, ph=ph + 2*np.pi/3 - np.pi/6, alpha=np.pi/3 + alpha, nn=nn, fs=fs)
    x3 = rmoc(vmax=3**.5 * vmax, ff=ff, ph=ph + 4*np.pi/3 - np.pi/6, alpha=np.pi/3 + alpha, nn=nn, fs=fs)
    xx = reduce(np.maximum, [x1, x2, x3])
    return xx


def square(vmax : float = 1,
           dc : float = 0,
           ff : float = 1,
           duty : float = .5,
           nn : int = 100,
           fs : float = 1000
           ) -> np.ndarray:
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
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop=nn*ts, step=ts)

    xx = np.where(tt % (1/ff) < (1/ff) * duty, 1, -1)
    xx = vmax * xx + dc
    #signal.square(2* np.pi * ff* tt, duty)

    xx = np.array(xx)

    return xx

def sawtooth(vmax : float = 1,
             dc : float = 0,
             ff : float = 1,
             nn : int = 1,
             fs : float = 1000
             ) -> np.ndarray:
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
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop= nn*ts, step=ts)
    T = 1/ff

    xx = [((vmax/T) * (i%T) + dc) for i in tt]
    #signal.sawtooth(2* np.pi * ff* tt, 0.5)

    xx = np.array(xx)

    return xx

def triangle(vmax : float = 1,
             dc : float = 0,
             ff : float = 1,
             duty : float = 0.5,
             nn : int = 1,
             fs : float = 1000
             ) -> np.ndarray:
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
    xx : ndarray
        Signal samples.
    """
    ts = 1/fs
    tt: np.ndarray = np.arange(stop= nn*ts, step=ts)
    T = 1/ff

    xx = np.where(tt % T < duty*T, (vmax/(duty*T)) * (tt % T) + dc, (-vmax/(1-duty)) * (1 - (tt % T)/T) + dc)
    xx = np.array(xx)

    return xx

def noise_generator(var : float = 1, nn : int = 100, fs : float = 1000) -> np.ndarray:
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
    xx : ndarray
        Noise samples.

    Notes
    -----
    The generated noise has zero mean and variance equal to ``var``.
    """
    xx = np.random.normal(loc=0, scale=np.sqrt(var), size=nn)
    xx = np.array(xx)

    return xx

def noisy_sin(vmax : float = 1,
              dc : float = 0,
              ff : float = 1,
              ph : float = 0,
              nn : int = 100,
              fs : float = 1000,
              snr : float = 20) -> np.ndarray:
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
    """
    xx = sin(vmax=vmax, dc=dc, ff=ff, ph=ph, nn=nn, fs=fs)
    pot_signal = np.mean(xx**2)
    var_noise = pot_signal / (10**(snr/10))
    
    noise = noise_generator(var_noise, nn, fs)
    xx = xx + noise

    return xx

def kronecker_delta(n : int, to : int = 0, fs : float = 1000) -> np.ndarray:
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
    delta[int(to*fs)] = 1

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
