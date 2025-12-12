import matplotlib.pyplot as plt
import matplotlib.figure as mpl_fig
import copy
from .FreqComponent import FreqComponent, DeltaComponent, BlockComponent, TriangleComponent, LeftTriangleComponent, RightTriangleComponent
from .FilterComponent import FilterComponent, BandPassFilterComponent, BandStopFilterComponent, LowPassFilterComponent, HighPassFilterComponent

class Spectrum:
    """
    Spectrum class for managing and visualizing frequency components and filters.
    This class provides functionality to create, manipulate, and visualize a spectrum
    composed of various frequency components (deltas, blocks, triangles) and filters
    (band-pass, band-stop, low-pass, high-pass).
    Attributes:
        components (list[FreqComponent]): List of frequency components and filters in the spectrum.
        active_filters (bool): Flag to enable/disable filter application when displaying the spectrum.
    Methods:
        add(component: FreqComponent) -> None:
            Add a frequency component to the spectrum.
        addDelta(f_center, height=1.0, color='blue', name=None, x_text=None, **kwargs) -> None:
            Add a delta (impulse) component at the specified center frequency.
        addBlock(f_center, width, height=1.0, color='skyblue', name=None, x_text=None, **kwargs) -> None:
            Add a rectangular block component to the spectrum.
        addTriangle(f_center, width, height=1.0, color='red', name=None, x_text=None, **kwargs) -> None:
            Add a symmetric triangle component to the spectrum.
        addRightTriangle(f_center, width, height=1.0, color='orange', name=None, x_text=None, **kwargs) -> None:
            Add a right-sloped triangle component to the spectrum.
        addLeftTriangle(f_center, width, height=1.0, color='orange', name=None, x_text=None, **kwargs) -> None:
            Add a left-sloped triangle component to the spectrum.
        addBandPassFilter(f_low=None, f_high=None, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs) -> None:
            Add a band-pass filter that allows frequencies between f_low and f_high.
        addBandStopFilter(f_low=None, f_high=None, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs) -> None:
            Add a band-stop (notch) filter that blocks frequencies between f_low and f_high.
        addLowPassFilter(f_cutoff, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs) -> None:
            Add a low-pass filter that allows frequencies below f_cutoff.
        addHighPassFilter(f_cutoff, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs) -> None:
            Add a high-pass filter that allows frequencies above f_cutoff.
        mix(f_osc, attenuation=0.5) -> Spectrum:
            Mix the spectrum with an oscillator at frequency f_osc, creating sum and difference frequencies.
            Returns a new Spectrum object with mixed components.
        enable_filters(a: bool) -> None:
            Enable or disable the application of filters when displaying the spectrum.
        show(ax: plt.Axes=None, only_positive=False, show_filters=True) -> tuple[fig, ax]:
            Display the spectrum on a matplotlib axes. Optionally show only positive frequencies
            and/or filter components. Returns the figure and axes objects.
        clean() -> None:
            Clear all components and close all matplotlib figures.
        get_passbands() -> list[tuple[float, float]] | None:
            Calculate the combined passband regions from all active filters.
            Returns a list of (min_freq, max_freq) tuples, or None if no filters are active.
        __mul__(other) -> Spectrum:
            Create a new Spectrum with all component heights multiplied by a scalar.
        __imul__(other) -> Spectrum:
            Multiply all component heights by a scalar in-place.
        __add__(other) -> Spectrum:
            Create a new Spectrum by adding components from another Spectrum, list, or FreqComponent.
        __iadd__(other) -> Spectrum:
            Add components from another Spectrum, list, or FreqComponent in-place.
        __repr__() -> str:
            Return a string representation of the Spectrum and its components.
        _filter_components(comps: list[FreqComponent], valid_ranges) -> list[FreqComponent]:
            Internal method to filter components based on valid frequency ranges.
    """
    def __init__(self):
        self.components: list[FreqComponent] = []
        self.active_filters = True

    def add(self, component: FreqComponent):
        """
        Add a frequency component to the collection of components.
        
        Args:
            component (FreqComponent): The frequency component to be added to the components list.
        
        Returns:
            None
        """
        self.components.append(component)

    def addDelta(self, f_center, height=1.0, color='blue', name=None, x_text=None, **kwargs):
        """
        Add a delta (impulse) component to the graphic at a specified frequency.
        
        Parameters
        ----------
        f_center : float
            The center frequency at which the delta component will be positioned.
        height : float, optional
            The height (amplitude) of the delta component. Default is 1.0.
        color : str, optional
            The color of the delta component. Default is 'blue'.
        name : str, optional
            The name identifier for the delta component. Default is None.
        x_text : float, optional
            The x-coordinate position for text labeling. Default is None.
        **kwargs
            Additional keyword arguments to pass to the DeltaComponent constructor.
        
        Returns
        -------
        None
            Adds the delta component to the current graphic.
        """
        self.add(DeltaComponent(f_center, height=height, color=color, name=name, x_text=x_text, **kwargs))

    def addBlock(self, f_center, width, height=1.0, color='skyblue', name=None, x_text=None, **kwargs):
        """
        Add a block component to the graphic.

        Args:
            f_center (float): The center frequency of the block.
            width (float): The width of the block in frequency units.
            height (float, optional): The height of the block. Defaults to 1.0.
            color (str, optional): The color of the block. Defaults to 'skyblue'.
            name (str, optional): The name identifier for the block. Defaults to None.
            x_text (float, optional): The x-coordinate for text placement. Defaults to None.
            **kwargs: Additional keyword arguments to pass to BlockComponent.

        Returns:
            None
        """
        self.add(BlockComponent(f_center, width=width, height=height, color=color, name=name, x_text=x_text, **kwargs))

    def addTriangle(self, f_center, width, height=1.0, color='red', name=None, x_text=None, **kwargs):
        """
        Add a triangle component to the graphic.
        
        Parameters
        ----------
        f_center : tuple or array-like
            The center position of the triangle (x, y coordinates).
        width : float
            The width of the triangle.
        height : float, optional
            The height of the triangle. Default is 1.0.
        color : str, optional
            The color of the triangle. Default is 'red'.
        name : str, optional
            The name identifier for the triangle component. Default is None.
        x_text : str or float, optional
            Text or value to display associated with the triangle. Default is None.
        **kwargs
            Additional keyword arguments to pass to the TriangleComponent constructor.
        
        Returns
        -------
        None
        """
        self.add(TriangleComponent(f_center, width=width, height=height, color=color, name=name, x_text=x_text, **kwargs))

    def addRightTriangle(self, f_center, width, height=1.0, color='orange', name=None, x_text=None, **kwargs):
        """
        Add a right triangle component to the graphic.

        Args:
            f_center (tuple): The center position of the right triangle as (x, y) coordinates.
            width (float): The width of the right triangle.
            height (float, optional): The height of the right triangle. Defaults to 1.0.
            color (str, optional): The color of the right triangle. Defaults to 'orange'.
            name (str, optional): The name identifier for the right triangle component. Defaults to None.
            x_text (str, optional): Text label to display on the x-axis. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the RightTriangleComponent constructor.

        Returns:
            None
        """
        self.add(RightTriangleComponent(f_center=f_center, width=width, height=height, color=color, name=name, x_text=x_text, **kwargs))

    def addLeftTriangle(self, f_center, width, height=1.0, color='orange', name=None, x_text=None, **kwargs):
        """
        Add a left-pointing triangle component to the graphic.

        Args:
            f_center (float): The center position of the triangle on the x-axis.
            width (float): The width of the triangle.
            height (float, optional): The height of the triangle. Defaults to 1.0.
            color (str, optional): The color of the triangle. Defaults to 'orange'.
            name (str, optional): The name identifier for the triangle component. Defaults to None.
            x_text (float, optional): The x-coordinate for text positioning. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the LeftTriangleComponent.

        Returns:
            None
        """
        self.add(LeftTriangleComponent(f_center=f_center, width=width, height=height, color=color, name=name, x_text=x_text, **kwargs))

    def addBandPassFilter(self, f_low=None, f_high=None, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs):
        """
        Add a band-pass filter component to the graphic.       
       
        Parameters
        ----------
        f_low : float, optional
            The lower cutoff frequency of the band-pass filter in Hz.
        f_high : float, optional
            The upper cutoff frequency of the band-pass filter in Hz.
        passband_gain : float, default=1.0
            The gain applied to frequencies within the pass band.
        color : str, default='gray'
            The color used to display the filter component.
        name : str, optional
            The name identifier for the filter component.
        x_text : float, optional
            The x-coordinate position for displaying text labels.
        **kwargs
            Additional keyword arguments passed to BandPassFilterComponent.
        
        Returns
        -------
        None
                
        Examples
        --------
        >>> graphic.addBandPassFilter(f_low=100, f_high=1000, passband_gain=1.5, color='blue')
        """
        self.add(BandPassFilterComponent(f_low=f_low, f_high=f_high, passband_gain=passband_gain,
                                color=color, name=name, x_text=x_text, **kwargs))
    def addBandStopFilter(self, f_low=None, f_high=None, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs):
        """
        Add a band-stop (notch) filter component to the graphic.
        
        Args:
            f_low (float, optional): The lower frequency boundary of the stop band in Hz.
                Defaults to None.
            f_high (float, optional): The upper frequency boundary of the stop band in Hz.
                Defaults to None.
            passband_gain (float, optional): The gain applied to frequencies outside the stop band.
                Defaults to 1.0 (unity gain).
            color (str, optional): The color used to display the filter component.
                Defaults to 'gray'.
            name (str, optional): A descriptive name for the filter component.
                Defaults to None.
            x_text (str, optional): Text label to display on the x-axis for this component.
                Defaults to None.
            **kwargs: Additional keyword arguments passed to BandStopFilterComponent.
        
        Returns:
            None
        """
        self.add(BandStopFilterComponent(f_low=f_low, f_high=f_high, passband_gain=passband_gain,
                                color=color, name=name, x_text=x_text, **kwargs))
    def addLowPassFilter(self, f_cutoff, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs):
        """
        Add a low-pass filter component to the graphic.

        Parameters
        ----------
        f_cutoff : float
            The cutoff frequency of the low-pass filter.
        passband_gain : float, optional
            The gain in the passband. Default is 1.0.
        color : str, optional
            The color of the filter component. Default is 'gray'.
        name : str, optional
            The name of the filter component. Default is None.
        x_text : float, optional
            The x-coordinate position for text annotation. Default is None.
        **kwargs
            Additional keyword arguments to pass to the LowPassFilterComponent.

        Returns
        -------
        None
        """
        self.add(LowPassFilterComponent(f_cutoff=f_cutoff, passband_gain=passband_gain,
                                color=color, name=name, x_text=x_text, **kwargs))
    def addHighPassFilter(self, f_cutoff, passband_gain=1.0, color='gray', name=None, x_text=None, **kwargs):
        """
        Add a high-pass filter component to the graphic.

        Args:
            f_cutoff (float): The cutoff frequency in Hz. Frequencies above this value will pass through the filter.
            passband_gain (float, optional): The gain applied to frequencies in the passband. Defaults to 1.0.
            color (str, optional): The color used to display the filter in the graphic. Defaults to 'gray'.
            name (str, optional): The name identifier for this filter component. Defaults to None.
            x_text (float or str, optional): The x-axis position for text label placement. Defaults to None.
            **kwargs: Additional keyword arguments passed to the HighPassFilterComponent.

        Returns:
            None

        Example:
            >>> graphic.addHighPassFilter(f_cutoff=1000, passband_gain=1.5, color='red', name='HPF1')
        """
        self.add(HighPassFilterComponent(f_cutoff=f_cutoff, passband_gain=passband_gain,
                                color=color, name=name, x_text=x_text, **kwargs))
                
    def mix(self, f_osc, attenuation = 0.5):
        """
        Mix the spectrum components with an oscillation frequency.
        This method creates a new spectrum by applying frequency mixing to all components.
        Filter components are mixed directly, while other components are frequency-shifted
        by both positive and negative oscillation frequencies with reduced amplitude.
        Args:
            f_osc (float): The oscillation frequency used for mixing.
            attenuation (float, optional): The amplitude reduction factor applied to 
                non-filter components. Defaults to 0.5.
        Returns:
            Spectrum: A new Spectrum object containing the mixed components. Filter 
                components are mixed in place, while other components are duplicated 
                with adjusted center frequencies and heights.
        """
        new_spectrum = Spectrum()

        filters = [c for c in self.components if isinstance(c, FilterComponent)]
        components = [c for c in self.components if not isinstance(c, FilterComponent)]

        for filt in filters:
            new_filt = copy.deepcopy(filt)
            new_filt.mix(f_osc)
            new_spectrum.add(new_filt)

        for comp in components:
            for val in [f_osc, -f_osc]:
                new_comp = copy.deepcopy(comp)
                new_comp.f_center += val
                new_comp.height = comp.height * attenuation
                new_spectrum.add(new_comp)

        return new_spectrum
    
    def enable_filters(self, a:bool):
        """
        Enable or disable filters.
        
        Args:
            a (bool): True to enable filters, False to disable them.
        """
        self.active_filters = a

    def show(self, ax: plt.Axes=None, only_positive=False, show_filters=True) -> list[mpl_fig.Figure, plt.Axes]:
        """
        Display the spectrum components and filters on a matplotlib axes.
        Parameters
        ----------
        ax : plt.Axes, optional
            The matplotlib axes to plot on. If None, a new figure and axes are created.
            Default is None.
        only_positive : bool, optional
            If True, only display components with non-negative center frequencies.
            Default is False.
        show_filters : bool, optional
            If True, display filter components on the plot. Default is True.
        Returns
        -------
        fig : matplotlib.figure.Figure
            The matplotlib figure object containing the plot.
        ax : plt.Axes
            The matplotlib axes object with the plotted spectrum.
        Notes
        -----
        - Filters are applied to components based on active passbands.
        - Components outside valid ranges are excluded from the plot.
        - The plot automatically adjusts x and y limits based on component bounds.
        - Grid lines are enabled on the plot.
        - Axes labels are set to "Frecuencia [Hz]" and "Amplitud".
        """

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.get_figure()
        
        components = [c for c in self.components if not isinstance(c, FilterComponent)]
        filters = [c for c in self.components if isinstance(c, FilterComponent)]

        # Erase all components outside passbands
        valid_range = None
        if self.active_filters:
            valid_range = self.get_passbands()
            comps = self._filter_components(components, valid_range)

        comps = comps if not only_positive else [c for c in comps if c.f_center >= 0]

        # Draw
        for comp in comps:
            comp.draw(ax, valid_range)
            
        # Limit adjustments
        if comps:
            bound = [c.get_bounds() for c in comps]
            xmin = min(r[0] for r in bound)
            xmax = max(r[1] for r in bound)
            max_amp = max(c.height for c in comps)

            padding = 0.1 * max(abs(xmin), abs(xmax))
            ax.set_xlim(0 if only_positive else xmin - padding, xmax + padding)
            ax.set_ylim(0, max_amp * 1.5)

        if show_filters:
            for filt in filters:
                filt.draw(ax, [(xmin, xmax) if comps else (-10e3, 10e3)])

        ax.grid(True)
        ax.set_xlabel("Frecuencia [Hz]")
        ax.set_ylabel("Amplitud")

        self.components = filters + comps

        return fig, ax
    
    def clean(self):
        """
        Removes all components from the current graphic and clears the matplotlib plot.

        This method resets the `components` list to empty, clears the current figure,
        and closes the matplotlib plot window.
        """
        self.components = []
        plt.clf()
        plt.close()

    def get_passbands(self):
        """
        Computes the effective passbands of the system by intersecting the passbands of all FilterComponent instances
        present in self.components.
        Returns:
            list of tuple or None: 
                - If no FilterComponent is present, returns None (all frequencies allowed).
                - Otherwise, returns a list of (min_freq, max_freq) tuples representing the allowed frequency intervals.
                - If the resulting passband is infinite, returns None.
        """
        filters = [c for c in self.components if isinstance(c, FilterComponent)]
        if not filters:
            return None  # All frequencies allowed

        # Infinite passband
        passband = [(float('-inf'), float('inf'))]

        for filt in filters:
            new_passband = []

            for a_min, a_max in passband:               # input of filter n (output n-1)
                for f_min, f_max in filt.get_passband():    # filter passband
                    # intersección
                    lo = max(a_min, f_min)
                    hi = min(a_max, f_max)
                    if lo <= hi:
                        new_passband.append((lo, hi))
            passband = new_passband                     # output of filter n

        if passband == [(float('-inf'), float('inf'))]:
            return None
        return passband
    
    def __mul__(self, other):
        new_spectrum = Spectrum()
        for comp in self.components:
            new_spectrum.add(comp * other)
        return new_spectrum
    
    def __imul__(self, other):
        for comp in self.components:
            comp.height *= other
        return self

    def __add__(self, other):
        result = copy.deepcopy(self)
        result += other
        return result
    
    def __iadd__(self, other):
        if isinstance(other, list):
            for comp in other:
                self += comp
            return self
        
        if isinstance(other, Spectrum):
            for comp in other.components:
                self += comp
            return self
        
        if isinstance(other, FreqComponent):
            self.add(other)
            return self
        
        raise TypeError("Unsupported type for addition to Spectrum")

    def __repr__(self):
        res = []
        res.append(f"Sprectrum(componentes={len(self.components)})\n")
        for comp in self.components:
            res.append("  " + repr(comp) + "\n")
        return "".join(res)
    
    def _filter_components(self, comps:list[FreqComponent], valid_ranges)->list[FreqComponent]:
        if valid_ranges is None:
            return comps
        new_components = []
        for comp in comps:
            if comp._intersects(valid_ranges):
                new_components.append(comp)

        return new_components
