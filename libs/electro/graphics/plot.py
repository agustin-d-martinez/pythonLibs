import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as col
from numpy.typing import ArrayLike

def pzmap(z: ArrayLike,
          p: ArrayLike,
          ax : plt.Axes = None,
          *args,
          **kwargs
          ) -> tuple[col.PatchCollection, col.PatchCollection]:
    """
    Plot the pole-zero map of a discrete-time system.

    Zeros are represented with circles and poles with crosses on the
    complex plane. The unit circle is also displayed as a reference.

    Parameters
    ----------
    z : list of complex
        List of system zeros.
    p : list of complex
        List of system poles.
    ax : matplotlib.axes.Axes, optional
        Axes where the plot is drawn. If omitted, a new figure and axes
        are created.
    *args, **kwargs
        Additional keyword arguments forwarded to the plotting functions.

    Returns
    -------
    matplotlib.collections.PatchCollection
        pcol, zcol: Colecctions of the scatter of zeros and poles.
    """
    if ax is None:
        _, ax = plt.subplots(*args, **kwargs)
    z_path = plt.scatter(np.real(z), np.imag(z), color='b', marker='o')
    p_path = plt.scatter(np.real(p), np.imag(p), color='r', marker='x')
    circle = plt.Circle((0,0), 1, fill=False)
    ax.add_patch(circle)
    ax.set_xlim((-1.1, 1.1))
    ax.set_ylim((-1.1, 1.1))

    ax.axhline(0, color='black')
    ax.axvline(0, color='black')
    plt.grid(True, which='both', ls='--')
    plt.title('Polos y Ceros del Filtro')
    plt.ylabel('Re')
    plt.xlabel('Im')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    return (p_path, z_path)

def plot_mag(*args : ArrayLike,
             ax : plt.Axes | None = None, 
             title : str | None = None, 
             label : str | None = None,
             **kwargs,
             ) -> plt.Line2D:
    """
    Plot the magnitude response of a filter.

    Parameters
    ----------
    ff, H : array-like or float
        The horizontal / vertical coordinates of the data points. ff values are optional and default to range(len(H)).
        H is the Complex frequency response or a frequency domain signal.    
    ax : matplotlib.axes.Axes, optional
        Axes where the plot is drawn.
    title : str, optional
        Figure title.
    label : str, optional
        Label for the plotted curve.
    **kwargs
        Additional arguments passed to ``Axes.plot()``.

    Returns
    -------
    matplotlib.lines.Line2D
        Line object corresponding to the plotted response.
    """
    ff, H = _get_args(*args)
    if ax is None:
        ax = plt.gca()

    mag = 20*np.log10(np.maximum(np.abs(H), 1e-13))
    line, = ax.plot(ff, mag, label=label, **kwargs)
    ax.set_title(title)
    ax.set_ylabel('Magnitud [dB]')
    ax.set_xlabel('Frecuencia [Hz]')
    ax.grid(True, which='both', ls='--')

    if label is not None:
        ax.legend()

    return line

def plot_phase(*args : ArrayLike,
               ax : plt.Axes | None = None, 
               title : str | None = None, 
               label : str | None = None,
               **kargs,
               ) -> plt.Line2D:
    """
    Plot the phase response of a filter.

    Parameters
    ----------
    ff, H : array-like or float
        The horizontal / vertical coordinates of the data points. ff values are optional and default to range(len(H)).
        H is the Complex frequency response or a frequency domain signal.    
    ax : matplotlib.axes.Axes, optional
        Axes where the plot is drawn.
    title : str, optional
        Figure title.
    label : str, optional
        Label for the plotted curve.
    **kwargs
        Additional arguments passed to ``Axes.plot()``.

    Returns
    -------
    matplotlib.lines.Line2D
        Line object corresponding to the plotted response.
    """
    ff, H = _get_args(*args)
    if ax is None:
        ax = plt.gca()

    phase = np.unwrap(np.angle(H))
    line, =ax.plot(ff, phase, label=label, **kargs)
    ax.set_title(title)
    ax.set_ylabel('Fase [rad]')
    ax.set_xlabel('Frecuencia [Hz]')
    ax.grid(True, which='both', ls='--')

    if label is not None:
        ax.legend()

    return line

def plot_delay(*args : ArrayLike, 
               ax : plt.Axes | None = None, 
               title : str | None = None, 
               label : str | None = None,
               **kargs,
               ) -> plt.Line2D:
    """
    Plot the group delay of a filter.

    Parameters
    ----------
    ff, H : array-like or float
        The horizontal / vertical coordinates of the data points. ff values are optional and default to range(len(H)).
        H is the Complex frequency response or a frequency domain signal.    
    ax : matplotlib.axes.Axes, optional
        Axes where the plot is drawn.
    title : str, optional
        Figure title.
    label : str, optional
        Label for the plotted curve.
    **kwargs
        Additional arguments passed to ``Axes.plot()``.

    Returns
    -------
    matplotlib.lines.Line2D
        Line object corresponding to the plotted response.
    """
    ff, H = _get_args(*args)
    if ax is None:
        ax = plt.gca()

    phase = np.unwrap(np.angle(H))
    gd = -np.diff(phase)/(2*np.pi*np.diff(ff))
    gd = np.append(gd, gd[-1])

    line, = ax.plot(ff, gd, label=label, **kargs)
    ax.set_title(title)
    ax.set_ylabel('Retardo [s]')
    ax.set_xlabel('Frecuencia [Hz]')
    ax.grid(True, which='both', ls='--')

    if label is not None:
        ax.legend()

    return line

def plot_all(*args : ArrayLike,
             ax : np.ndarray[plt.Axes] | None = None, 
             title : str | None = None, 
             label : str | None = None, 
             **kargs
             ) -> None:
    """
    Plot the complete frequency response of a filter.

    This function generates the magnitude, phase, and group delay
    responses using a common frequency vector.

    Parameters
    ----------
    ff, H : array-like or float
        The horizontal / vertical coordinates of the data points. ff values are optional and default to range(len(H)).
        H is the Complex frequency response or a frequency domain signal.    
    ax : np.ndarray[matplotlib.axes.Axes], optional
        Axes or container used for the generated plots.
    title : str, optional
        Common title for the response plots.
    label : str, optional
        Label for the plotted curves.
    **kwargs
        Additional plotting arguments.

    Returns
    -------
    None
    """
    ff, H = _get_args(*args)
    if ax is None:
        _, ax = plt.subplots(3, 1, sharex=True)

    plot_mag(ff, H, title=title, ax=ax[0], label=label, **kargs)
    plot_phase(ff, H, title=title, ax=ax[1], label=label, **kargs)
    plot_delay(ff, H, title=title, ax=ax[2], label=label, **kargs)


def plot_template(  fpass : float | ArrayLike, 
                    fstop : float | ArrayLike, 
                    attpass : float | ArrayLike = 0.5,
                    attstop : float | ArrayLike = 40) -> None: 
    """
    Plot the filter specification template.

    The template defines the passband and stopband frequency limits together
    with their corresponding attenuation requirements.

    Parameters
    ----------
    fpass : ArrayLike
        Passband edge frequency or frequencies.
    fstop : ArrayLike
        Stopband edge frequency or frequencies.
    attpass : ArrayLike, default=0.5
        Maximum attenuation allowed in the passband (dB).
    attstop : ArrayLike, default=40
        Minimum attenuation required in the stopband (dB).

    Returns
    -------
    None
        
    Example
    --------
    >>> import matplotlib.pyplot as plt
    >>> from PSD.plot import plot_template
    >>> fpass = [1, 20, 30]
    >>> fstop = [10, 15, 40]
    >>> attepass = [10, 1]
    >>> attestop = [20, 20]
    >>> PSD.plot.plot_template(fpass, fstop, attepass, attestop)
    >>> plt.legend()

    >>> fpass = 10
    >>> fstop = 50
    >>> plt.xlim(0, 100)
    >>> plt.ylim(-50, 10)
    >>> PSD.plot.plot_template(fpass, fstop)
    >>> plt.legend()

    """

    # Axis limits
    xmin, xmax, ymin, ymax = plt.axis()
    fpass = np.atleast_1d(fpass)
    fstop = np.atleast_1d(fstop)
    attpass = np.atleast_1d(attpass)
    attstop = np.atleast_1d(attstop)

    puntos = []
    puntos.extend((f, 'pass') for f in fpass)
    puntos.extend((f, 'stop') for f in fstop)
    puntos.sort(key=lambda x: x[0])

    # Range of pass bands and stop bands
    ranges = []
    if puntos[0][0] > xmin:
        ranges.append((xmin, puntos[0][0], puntos[0][1]))
    for a, b in zip(puntos[:-1], puntos[1:]):
        if a[1] == b[1]:
            ranges.append((a[0], b[0], a[1]))
    if puntos[-1][0] < xmax:
        ranges.append((puntos[-1][0], xmax, puntos[-1][1]))

    # Range fill 
    i_pass, i_stop = 0, 0
    for f1, f2, tipo in ranges:
        if tipo == 'pass':
            plt.fill([f1, f1, f2, f2], [ymin, -attpass[i_pass], -attpass[i_pass], ymin], 
                     'lightgrey', alpha=0.4, hatch='x', lw=1, ls='--', ec='k', 
                     label='Plantilla' if i_pass == 0 else None)
            i_pass += 1
        else:
            plt.fill([f1, f2, f2, f1], [-attstop[i_stop], -attstop[i_stop], ymax, ymax], 
                     'lightgrey', alpha=0.4, hatch='x', lw=1, ls='--', ec='k')
            i_stop += 1

def _get_args(*args):
    match len(args):
        case 1:
            y = args[0]
            x = range(len(y))
        case 2:
            y = args[1]
            x = args[0]
        case _:
            raise ValueError("It needs to pass 1 or 2 argumets to work")
    
    return x, y
