import numpy as np
import scipy.signal as sig

from numpy.typing import ArrayLike

from typing import Literal

from .windows import WindowFunct, WindowType, WINDOWS_FUNCT_DICT

def fft(xx : ArrayLike,
        nfft : int | None = None,
        window : WindowType | WindowFunct | None = None,
        axis : int = -1,
        only_positive : bool = False,
        ) -> np.ndarray:
    """
    Compute the normalized Fast Fourier Transform (FFT) of a signal.

    The result is divided by the number of samples so that the spectral
    amplitudes correspond to the original signal amplitudes.

    A window can be applied to the signal before computing the FFT, if specified.
    The window is amplitude-corrected using its mean value.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    nfft : int, optional
        Number of FFT points. If omitted, the signal length is used.
    window : WindowType or WindowFunct, optional
        Window applied before computing the FFT. The window is amplitude-corrected using its mean value. 
        If a function is passed, it applies that window to the FFT.
    axis : int, default=-1
        Axis along which the FFT is computed.
    only_positive : bool, default=False
        If True, return only the positive frequency spectrum.

    Returns
    -------
    ndarray
        Normalized FFT of the input signal.
    """    
    xx = np.asarray(xx)
    xx = np.moveaxis(xx, axis, -1)
    N = xx.shape[-1]

    if callable(window):
        win = window(N)
    elif window is not None:
        if window not in WINDOWS_FUNCT_DICT:
            raise ValueError(f'Window {window} not found. Available windows: {list(WINDOWS_FUNCT_DICT.keys())}')
        win = WINDOWS_FUNCT_DICT[window](N)
        err_win = np.mean(win)
        xx = xx * win/err_win
    xx_f = np.fft.fft(xx, n=nfft)/N
    
    if only_positive:
        xx_f = _positive_spectrum(xx_f)

    return np.moveaxis(xx_f, -1, axis)

def _positive_spectrum(xx: ArrayLike, axis : int = -1 ) -> np.ndarray:
    """
    Extract the positive frequency spectrum from an FFT result.

    Parameters
    ----------
    xx : ArrayLike
        FFT result.
    axis : int, default=-1
        Axis along which the FFT was computed.

    Returns
    -------
    ndarray
        Positive frequency spectrum (N/2 + 1 points).
    """
    xx = np.asarray(xx)
    half = xx.shape[axis] // 2 + 1  # N/2 + 1

    sl = [slice(None)] * xx.ndim    # [:, :, :] with ndim 3
    sl[axis] = slice(0, half)       # [:, 0:half, :]

    return xx[tuple(sl)]

def fft_freq(xx : ArrayLike | int, 
             fs: float = 1, 
             axis : int = -1,
             only_positive=False
             ) -> np.ndarray:
    """
    Generate the frequency axis associated with an FFT.

    The returned axis follows the ordering used by ``numpy.fft.fft``:
        [0, Δf, ..., fs/2, -fs/2, ..., -Δf]
    Equivalent to numpy.fft.fftfreq(N, d=1/fs, axis=axis)

    Parameters
    ----------
    xx : ArrayLike or int
        Input signal or number of samples.
    fs : float
        Sampling frequency.
    axis : int, default=-1
        Axis along which the FFT is computed.
    only_positive : bool, default=False
        If True, return only the positive frequency spectrum.

    Returns
    -------
    ndarray
        Frequency vector with the same length as the FFT output.
    """
    if isinstance(xx, int):
        N = xx
    else:
        xx = np.asarray(xx)
        N = xx.shape[axis]

    if only_positive:
        return np.arange(N//2 + 1)* fs/N

    half = (N - 1) // 2
    p1 = np.arange(0, half + 1)
    p2 = np.arange(-(N//2), 0)

    ff = np.zeros(N)
    ff[:half+1] = p1
    ff[half+1:] = p2
    return ff * fs/N

def fft_shift(xx: ArrayLike, axis : int = -1) -> np.ndarray:
    """
    Shift the zero-frequency component to the center of the spectrum.
    Equivalent to np.fft.fftshift(xx, axes=axis).

    Parameters
    ----------
    xx : ArrayLike
        Spectrum or FFT result.
    axis : int, default=-1
        Axis along which to perform the shift.

    Returns
    -------
    ndarray
        Shifted spectrum.
    """
    xx = np.asarray(xx)
    N = xx.shape[axis]

    idx1 = [slice(None)] * xx.ndim              #[:, :, :]
    idx2 = [slice(None)] * xx.ndim
    idx1[axis] = slice((N + 1) // 2, None)      #[:, half:0, :]
    idx2[axis] = slice(None, (N + 1) // 2)      #[:, 0:half, : ]

    return np.concatenate( (xx[tuple(idx1)], xx[tuple(idx2)]), axis=axis)

def blackman_tukey(xx : ArrayLike, 
                   fs : float = 1, 
                   M : int = None, 
                   nfft : int = None
                   ) -> tuple[np.ndarray, np.ndarray]:
    """
    Estimate the Power Spectral Density (PSD) using the Blackman-Tukey method.

    The algorithm computes the autocorrelation of the input signal, truncates
    it to the desired lag length, applies a Blackman window, and computes the
    Fourier transform of the windowed autocorrelation.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    fs : float, default=1
        Sampling frequency.
    M : int, optional
        Maximum correlation lag. If omitted, ``N // 5`` is used.
    nfft : int, optional
        Number of FFT points. If omitted, the signal length is used.

    Returns
    -------
    f : ndarray
        Frequency vector.
    Pxx : ndarray
        Estimated power spectral density.
    """
    xx = np.asarray(xx)
    N = np.max(xx.shape)     # Cant muestras

    if nfft is None:
        nfft = N
    if M is None:
        M = N//5

    xx = xx - np.mean(xx)

    # 1. correlation    
    r = autocorrelate(xx, mode='full')
    r = r[N-M-1 : N+M]
    # Note: correlate returns a 2N-1 vector. Blackman-Tuckey wants the 2M+1 (the center part).
    #       The function trim the ends of lenght N-M-1.

    # 2. window
    win = WINDOWS_FUNCT_DICT['blackman'](len(r))
    
    # 3. FFT
    Pxx = np.abs(np.fft.rfft(r*win, n=nfft))
    Pxx[1:-1] *= 2                              # Correction positive frequency
    Pxx /= fs                                   # Normalization to fs

    f_ = np.fft.rfftfreq(nfft, 1/fs)
    return f_, Pxx

def autocorrelate(xx: ArrayLike, 
                  mode : Literal['full', 'positive'] = 'positive',
                  axis : int = -1) -> np.ndarray:
    """
    Compute the autocorrelation of a signal.

    The autocorrelation is normalized by the signal length.

    Parameters
    ----------
    xx : ArrayLike
        Input signal(s). If two-dimensional, each row is treated as an
        independent signal.
    mode : {"full", "positive"}, default="positive"
        Portion of the autocorrelation sequence to return.

        - ``"full"`` returns the complete sequence, including negative
          and positive lags.
        - ``"positive"`` returns only the non-negative lags, starting
          from zero.
    axis : int, default=-1
        Axis along which the autocorrelation is computed.

    Returns
    -------
    ndarray
        Autocorrelation sequence.
    """
    xx = np.asarray(xx)

    N = xx.shape[axis]
    xx = np.moveaxis(xx, axis, -1)

    corr_lenght = 2 * N - 1 if mode == "full" else N
    corr = np.empty(xx.shape[:-1] + (corr_lenght,))

    for index in np.ndindex(xx.shape[:-1]):
        r = sig.correlate(xx[index], xx[index], mode="full") / N        # Faster than np.correlate()

        if mode == "positive":
            r = r[N-1:]
        elif mode != "full":
            raise ValueError("mode must be either 'full' or 'positive'.")

        corr[index] = r

    corr = np.moveaxis(corr, -1, axis)

    return corr