import matplotlib.pyplot as plt
from typing import Any, Optional
from .FreqComponent import FreqComponent, FreqRange

## Filters ----------------------------------------------------------------------------------------------------------------
class FilterComponent(FreqComponent):
    """
    FilterComponent class for managing frequency filter visualization and operations.
    A FilterComponent represents a frequency filter with defined passbands, gains, and visualization properties.
    It inherits from FreqComponent and provides methods for drawing filters, mixing with oscillator frequencies,
    and managing passband ranges.
    Attributes:
        filter_type (str): Type of filter (e.g., 'generic', 'lowpass', 'highpass', 'bandpass').
        passband_gain (float): Gain applied within the passband. Default is 1.0.
        stopband_gain (float): Gain applied outside the passband. Default is 0.
        passbands (FreqRange | None): List of tuples defining frequency ranges (low, high) where the filter passes signal.
        color (str): Color for visualization. Default is "gray".
        name (str | None): Optional name identifier for the filter.
        x_text (str | None): Optional x-axis label text.
    Methods:
        get_passband() -> FreqRange:
            Returns the current passband frequency ranges.
        draw(ax: plt.Axes, valid_range: Optional[FreqRange]) -> None:
            Draws the filter representation on a matplotlib axes within the specified valid frequency range.
            Fills areas between passbands with semi-transparent color and displays filter name if provided.
        mix(f_osc: float) -> None:
            Applies frequency mixing by shifting passbands by ±f_osc and merges overlapping ranges.
        _get_segments(xi: float, xo: float) -> tuple[list, list]:
            Generates x and y coordinate segments for the filter within frequency range [xi, xo].
            Returns lists of x and y values representing the filter's frequency response.
        _clip_interval(fmin: float, fmax: float, low: float, high: float) -> tuple | None:
            Clips a frequency interval [fmin, fmax] to a valid range [low, high].
            Returns clipped interval or None if no overlap exists.
        _merge_ranges() -> None:
            Sorts passbands and merges overlapping or adjacent frequency ranges into single ranges.
    """
    def __init__(self, passbands:FreqRange|None, filter_type='generic', passband_gain=1.0, stopband_gain = 0, color="gray", name=None, x_text=None, **kwargs:Any):
        """
        Initialize a filter graphic object.

        Args:
            passbands (FreqRange | None): The frequency range(s) for the filter passbands.
                None if no passband is specified.
            filter_type (str, optional): The type of filter. Defaults to 'generic'.
            passband_gain (float, optional): The gain applied in the passband region.
                Defaults to 1.0.
            stopband_gain (float, optional): The gain applied in the stopband region.
                Defaults to 0.
            color (str, optional): The color for the graphic representation.
                Defaults to "gray".
            name (str, optional): The name identifier for the filter. Defaults to None.
            x_text (str, optional): Text label for the x-axis. Defaults to None.
            **kwargs (Any): Additional keyword arguments passed to the parent class.
        """
        super().__init__(0, height=passband_gain, color=color, name=name, x_text=x_text, **kwargs)
        self.filter_type = filter_type
        self.passband_gain = passband_gain
        self.stopband_gain = stopband_gain
        self.passbands =  passbands

    def get_passband(self) -> FreqRange:
        """
        Retrieve the passband frequency range.

        Returns:
            FreqRange: The passband object containing the frequency range information.
        """
        return self.passbands

    def draw(self, ax: plt.Axes, valid_range: Optional[FreqRange]=None):
        fill_style = dict(color=self.color, alpha=0.3)
        fill_style.update(self.kwargs)

        if valid_range is None:
            return  # Nothing to draw

        for low, high in valid_range:
            for fmin, fmax in self.passbands:
                clipped = self._clip_interval(fmin, fmax, low, high)
                if clipped is None:
                    continue

                xmin, xmax = clipped
                ax.fill_between([xmin, xmax],0,self.passband_gain,**fill_style)

                # Center text
                if self.name:
                    ax.text((xmin + xmax) / 2,self.passband_gain + 0.05,self.name,ha='center', va='bottom', fontsize=10)     

    def mix(self, f_osc):
        """
        Mix the passbands by shifting them by a given oscillation frequency.
        
        This method creates new passbands by shifting each existing passband
        by both positive and negative values of the oscillation frequency.
        The new passbands are then merged to combine any overlapping ranges.
        
        Args:
            f_osc (float): The oscillation frequency used to shift the passbands.
                          Both +f_osc and -f_osc shifts are applied.
        
        Returns:
            None: Modifies self.passbands in-place with the shifted and merged ranges.
        """
        new_passbands = []
        for low, high in self.passbands:
            for val in [-f_osc, f_osc]:
                new_low = high + val
                new_high = low + val 
                new_passbands.append((new_low, new_high))
        self.passbands = new_passbands
        self._merge_ranges()

    def __repr__(self):
        res = []
        res.append(f"Filter {self.filter_type}(")
        res.append(f"  name=\t\t{self.name},")        
        res.append(f"  passbands=\t{self.passbands},")
        res.append(f"  passband_gain=\t{self.passband_gain},")
        res.append(f"  stopband_gain=\t{self.stopband_gain},")
        res.append(f")")
        return "\n".join(res)

    def _get_segments(self, xi, xo):
        if xi > xo:
            return [], []
        
        x = []
        y = []

        for low, high in self.passbands:
            fmin = max(low, xi)
            fmax = min(high, xo)
            if fmin <= fmax:
                x += [fmin, fmin, fmax, fmax]
                y += [self.stopband_gain, self.passband_gain, self.passband_gain, self.stopband_gain]
        
        return x, y
    def _clip_interval(self, fmin, fmax, low, high):
        clipped_min = max(fmin, low)
        clipped_max = min(fmax, high)
        if clipped_min >= clipped_max:
            return None
        return (clipped_min, clipped_max)
    

    def _merge_ranges(self):
        self.passbands.sort()
        merged = []
        
        for current in self.passbands:
            if not merged:
                merged.append(current)
            else:
                last = merged[-1]
                if current[0] <= last[1]:
                    merged[-1] = (last[0], max(last[1], current[1]))
                else:
                    merged.append(current)
        self.passbands = merged

class BandPassFilterComponent(FilterComponent):
    """
    A band-pass filter component that allows frequencies within two symmetric frequency ranges to pass.

    This filter component creates a band-pass filter with symmetric passbands centered around
    zero frequency (positive and negative frequencies). It inherits from FilterComponent and
    configures the appropriate passband ranges for the filter.

    Attributes:
        f_low (float): The lower cutoff frequency of the band-pass filter (in Hz).
        f_high (float): The upper cutoff frequency of the band-pass filter (in Hz).
        passband_gain (float, optional): The gain applied to frequencies within the passband.
            Defaults to 1.0.
        color (str, optional): The color used to represent this filter component in visualizations.
            Defaults to "gray".
        name (str, optional): A descriptive name for this filter component. If not provided,
            a default name will be used.
        x_text (str, optional): Text label to display on the x-axis for this component.
        **kwargs: Additional keyword arguments to pass to the parent FilterComponent class.

    Note:
        The filter creates symmetric passbands at (-f_high, -f_low) and (f_low, f_high)
        to represent both negative and positive frequency components.
    """
    def __init__(self, f_low, f_high, passband_gain=1.0, color="gray", name=None, x_text=None, **kwargs):
        passbands=[(-f_high, -f_low), (f_low, f_high)]
        super().__init__(passbands=passbands, filter_type="bandpass", passband_gain=passband_gain, color=color, name=name, x_text=x_text, **kwargs)

class BandStopFilterComponent(FilterComponent):
    """
    A band-stop (notch) filter component that attenuates frequencies within a specified band.

    This filter allows frequencies outside the specified range to pass through while
    suppressing frequencies between f_low and f_high.

    Parameters
    ----------
    f_low : float
        The lower cutoff frequency of the stop band.
    f_high : float
        The upper cutoff frequency of the stop band.
    passband_gain : float, optional
        The gain applied to the passband frequencies. Default is 1.0.
    color : str, optional
        The color used for visualization. Default is "gray".
    name : str, optional
        A descriptive name for the filter component. Default is None.
    x_text : str, optional
        Text label for the x-axis or display. Default is None.
    **kwargs : dict
        Additional keyword arguments to pass to the parent FilterComponent class.

    Notes
    -----
    The filter creates three passbands:
        - (-∞, -f_high): Frequencies below the stop band
        - (-f_low, f_low): Frequencies within the stop band (centered at zero)
        - (f_high, ∞): Frequencies above the stop band

    Examples
    --------
    >>> filter_component = BandStopFilterComponent(f_low=100, f_high=200, passband_gain=1.0)
    """
    def __init__(self, f_low, f_high, passband_gain=1.0, color="gray", name=None, x_text=None, **kwargs):
        passbands = [(float('-inf'), -f_high), (-f_low, f_low), (f_high, float('inf'))]
        super().__init__(passbands=passbands, filter_type="bandstop", passband_gain=passband_gain, color=color, name=name, x_text=x_text, **kwargs)
   
class LowPassFilterComponent(FilterComponent):
    """
    Low-pass filter component that attenuates frequencies above a cutoff frequency.

    This class creates a low-pass filter with a single passband ranging from negative
    to positive cutoff frequency. Frequencies within this range are allowed to pass,
    while frequencies outside are attenuated.

    Args:
        f_cutoff (float): The cutoff frequency that defines the passband limits.
            The passband extends from -f_cutoff to +f_cutoff.
        passband_gain (float, optional): The gain applied to frequencies in the passband.
            Defaults to 1.0 (unity gain).
        color (str, optional): The color used to display the filter component.
            Defaults to "gray".
        name (str, optional): A display name for the filter component.
            Defaults to None.
        x_text (str, optional): Text to display on the x-axis.
            Defaults to None.
        **kwargs: Additional keyword arguments passed to the parent FilterComponent class.

    Attributes:
        Inherits all attributes from FilterComponent, including filter configuration
        and visualization properties.

    Example:
        >>> lpf = LowPassFilterComponent(f_cutoff=1000, passband_gain=1.0, color="blue", name="LPF_1kHz")
    """
    def __init__(self, f_cutoff, passband_gain=1.0, color="gray", name=None, x_text=None, **kwargs):
        passbands = [(-f_cutoff, f_cutoff)]
        super().__init__(passbands = passbands, filter_type="lowpass", passband_gain=passband_gain, color=color, name=name, x_text=x_text, **kwargs)
    
class HighPassFilterComponent(FilterComponent):
    """
    A high-pass filter component that allows frequencies above and below specified cutoff thresholds to pass.

    This class represents a high-pass filter with two passbands: one below the negative cutoff frequency
    and one above the positive cutoff frequency. It inherits from FilterComponent and is used to visualize
    and apply high-pass filtering operations.

    Args:
        f_cutoff (float): The cutoff frequency. Defines the threshold frequencies for the passbands
                         at -f_cutoff and +f_cutoff.
        passband_gain (float, optional): The gain applied to the passband. Defaults to 1.0.
        color (str, optional): The color of the filter component in the graphical representation.
                              Defaults to "gray".
        name (str, optional): The name/label for this filter component. Defaults to None.
        x_text (str, optional): Text label for the x-axis representation. Defaults to None.
        **kwargs: Additional keyword arguments passed to the parent FilterComponent class.

    Returns:
        None
    """
    def __init__(self, f_cutoff, passband_gain=1.0, color="gray", name=None, x_text=None, **kwargs):
        passbands = [(float('-inf'), -f_cutoff), (f_cutoff, float('inf'))]
        super().__init__(passbands=passbands, filter_type="highpass", passband_gain=passband_gain, color=color, name=name, x_text=x_text, **kwargs)

