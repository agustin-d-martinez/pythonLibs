import matplotlib.pyplot as plt
from typing import Any, Optional, List, Tuple

FreqRange = List[Tuple[float, float]]


class FreqComponent:
    """
    FreqComponent represents a frequency-domain graphical component for visualization.
    Attributes:
        f_center (float): Center frequency of the component.
        width (float, optional): Width of the component in frequency units. If None, treated as a single frequency.
        height (float): Height of the component for visualization purposes.
        color (str): Color used for drawing the component.
        name (str, optional): Name identifier for the component.
        x_text (str, optional): Text to display at the center frequency.
        kwargs (dict): Additional keyword arguments for customization.
    Methods:
        draw(ax, valid_range=None):
            Draws the frequency component on the given matplotlib Axes object.
            Optionally restricts drawing to a valid frequency range.
        get_bounds():
            Returns the minimum and maximum frequency bounds of the component.
        intersects(ranges):
            Checks if the component intersects with any of the given frequency ranges.
        mirror():
            Mirrors the component by negating its center frequency.
        __mul__(other):
            Returns a new component with its height scaled by 'other'.
        __imult__(other):
            In-place multiplication of the component's height by 'other'.
        __repr__():
            Returns a string representation of the component.
    """
    def __init__(self, f_center, width=None, height=1.0, color='blue', name:str =None, x_text:str=None, **kwargs:Any):
        """
        Initializes a graphical object with specified properties.
        Args:
            f_center: The center frequency or position of the graphic element.
            width (optional): The width of the graphic element. Defaults to None.
            height (float, optional): The height of the graphic element. Defaults to 1.0.
            color (str, optional): The color of the graphic element. Defaults to 'blue'.
            name (str, optional): The name identifier for the graphic element. Defaults to None.
            x_text (str, optional): Text to display along the x-axis. Defaults to None.
            **kwargs: Additional keyword arguments for further customization.
        """
        self.f_center = f_center
        self.width = width
        self.height = height
        
        self.color = color
        self.name = name
        self.x_text = x_text
        self.kwargs = kwargs  

    def draw(self, ax: plt.Axes, valid_range:Optional[FreqRange]=None):
        """
        Draws the spectrum on the given matplotlib Axes object.
        Parameters:
            ax (plt.Axes): The matplotlib Axes on which to plot the spectrum.
            valid_range (Optional[FreqRange]): A list of (low, high) frequency tuples specifying the valid frequency ranges to display.
                If None, the full range from fmin to fmax is used.
        Plots the spectrum as a line and fills the area under the curve with transparency.
        Optionally adds a text label at the center frequency if `self.x_text` is set.
        """
        fmin, fmax = self.get_bounds()

        line_style = dict(color=self.color)
        fill_style = dict(color=self.color, alpha=0.3)
        line_style.update(self.kwargs)
        fill_style.update(self.kwargs)

        points = []

        if valid_range is None:             #Max range
            valid_range = [(fmin, fmax)]
        for low, high in valid_range:      
            x, y = self._get_segments(low, high)
            points.append( (x, y) )

        for x, y in points:
            ax.plot(x, y, **line_style)
            ax.fill_between(x, y, **fill_style)

        if self.x_text:
            ax.text(self.f_center, -0.1 * self.height, self.x_text, ha='center', va='top', fontsize=10)

    def get_bounds(self):
        """
        Calculates and returns the minimum and maximum frequency bounds.

        If `self.width` is None, both bounds are set to `self.f_center`.
        Otherwise, the bounds are computed as `self.f_center` minus and plus half of `self.width`.

        Returns:
            tuple: A tuple containing (fmin, fmax), the lower and upper frequency bounds.
        """
        if self.width is None:
            fmin = self.f_center
            fmax = self.f_center
        else:
            fmin = self.f_center - self.width/2
            fmax = self.f_center + self.width/2
        return fmin, fmax

    def mirror(self):
        self.f_center = -self.f_center
    
    def __mul__(self, other: float):
        new_component = self.__class__(**self.__dict__)
        new_component.height *= other
        return new_component
    
    def __imult__(self, other):
        return self.__mul__(other)
    
    def __repr__(self):
        res = []
        cname = self.__class__.__name__.replace("Component", "")
        res.append(f"{cname}(")
        res.append(f"  name=\t\t{self.name},")
        res.append(f"  f_center=\t{self.f_center},")
        res.append(f"  width=\t{self.width},")
        res.append(f"  height=\t{self.height},")
        res.append(f"  color=\t{self.color},")
        res.append(f")")
        return "\n".join(res)
    
    def _get_segments(self, xi, xo):
        raise NotImplementedError("Subclases deben implementar _get_segments(xi, xo)")
    
    def _intersects(self, ranges:FreqRange|None)->bool:
        """
        Determine if this frequency range intersects with any range in a collection.

        Args:
            ranges (FreqRange | None): A collection of frequency ranges to check for intersection.
                                       Each range is expected to be a tuple of (rmin, rmax).

        Returns:
            bool: True if this frequency range overlaps with any range in the provided collection,
                  False otherwise.

        Raises:
            TypeError: If ranges is not iterable (excluding None).
        """
        fmin, fmax = self.get_bounds()
        for rmin, rmax in ranges:
            if fmax >= rmin and fmin <= rmax:
                return True
        return False

# Basic geometry --------------------------------------------------------------------------------------------------------
class DeltaComponent(FreqComponent):
    """
    A frequency component class that represents a delta (impulse) in the frequency spectrum.
    This class extends FreqComponent to visualize a point frequency component as a vertical
    arrow at a specified center frequency with optional labels.
    Attributes:
        f_center (float): The center frequency of the delta component.
        height (float): The amplitude/height of the delta component. Defaults to 1.
        color (str): The color of the arrow. Defaults to 'blue'.
        name (str, optional): The name label displayed above the arrow.
        x_text (str, optional): The text label displayed below the arrow at the x-axis.
        **kwargs: Additional keyword arguments passed to the parent class and arrow styling.
    Methods:
        __init__(f_center, height=1, color='blue', name=None, x_text=None, **kwargs):
            Initializes a DeltaComponent with a center frequency and zero bandwidth.
        draw(ax, valid_range=None):
            Renders the delta component as a vertical arrow on the given matplotlib axes.
            Args:
                ax (plt.Axes): The matplotlib axes object to draw on.
                valid_range (list of tuples, optional): A list of (low, high) frequency ranges.
                    Only draws the component if f_center falls within one of the ranges.
    """
    def __init__(self, f_center, height=1, color='blue', name=None, x_text=None, **kwargs):
        """
        Initialize a graphic object with center frequency and visual properties.

        Parameters
        ----------
        f_center : float
            The center frequency for the graphic object.
        height : float, optional
            The height of the graphic object. Default is 1.
        color : str, optional
            The color of the graphic object. Default is 'blue'.
        name : str, optional
            The name identifier for the graphic object. Default is None.
        x_text : float, optional
            The x-coordinate position for text display. Default is None.
        **kwargs
            Additional keyword arguments passed to the parent class.
        """
        super().__init__(f_center, 0, height, color, name, x_text, **kwargs)
    
    def draw(self, ax: plt.Axes, valid_range=None):
        """
        Draw an annotated arrow on a matplotlib axes representing a spectral line or feature.
        This method renders a vertical arrow at a specified frequency with optional labels.
        The arrow is only drawn if its center frequency falls within valid frequency ranges.
        Args:
            ax (plt.Axes): The matplotlib axes object on which to draw the arrow.
            valid_range (list of tuples, optional): A list of (lower, upper) frequency tuples
                defining valid frequency ranges. If provided, the arrow is only drawn if
                `self.f_center` falls within at least one range. Defaults to None (no range check).
        Returns:
            None
        Side Effects:
            - Draws a vertical arrow on the axes from y=0 to y=self.height at x=self.f_center
            - Optionally displays `self.name` as text above the arrow
            - Optionally displays `self.x_text` as text below the arrow
        Notes:
            - Arrow appearance is controlled by `self.color`, `self.height`, and `self.kwargs`
            - Arrow has a black edge with 90% opacity
            - Text is centered horizontally at the arrow's x-position
        """
        if valid_range is not None:
            if not any(lo <= self.f_center <= hi for lo, hi in valid_range):
                return
        
        arrow_style = dict(facecolor=self.color, edgecolor='black', width=1.5, headwidth=8, alpha=0.9 )
        arrow_style.update(self.kwargs)

        ax.annotate('', xy=(self.f_center, self.height), xytext=(self.f_center, 0), arrowprops=arrow_style)
        if self.name:
            ax.text(self.f_center, self.height + 0.05, self.name, ha='center', va='bottom', fontsize=10)
        if self.x_text:
            ax.text(self.f_center, -0.1 * self.height, self.x_text, ha='center', va='top', fontsize=10)
    
class BlockComponent(FreqComponent):
    """
    BlockComponent represents a rectangular frequency component visualization.
    This class extends FreqComponent to render a block-shaped component in a frequency spectrum display.
    The block is defined by a center frequency, width, and height, and can be customized with color and labeling.
    Attributes:
        f_center (float): Center frequency of the block component.
        width (float, optional): Width of the block in frequency units. Defaults to None.
        height (float, optional): Height of the block visualization. Defaults to 1.
        color (str, optional): Color of the block. Defaults to 'blue'.
        name (str, optional): Name identifier for the component. Defaults to None.
        x_text (float, optional): X-coordinate position for text label. Defaults to None.
        **kwargs: Additional keyword arguments passed to the parent FreqComponent class.
    Methods:
        _get_segments(xi, xo): 
            Generates the x and y coordinates for the block segment within the specified frequency range.
            Args:
                xi (float): Lower bound of the frequency range (minimum frequency).
                xo (float): Upper bound of the frequency range (maximum frequency).
            Returns:
                tuple: A tuple of two lists (x, y) containing the coordinates of the rectangular block.
                       Returns ([], []) if xi > xo (invalid range).
                       The coordinates form a rectangle with corners at (fmin, 0), (fmin, height), 
                       (fmax, height), and (fmax, 0).
    """
    def __init__(self, f_center, width=None, height=1, color='blue', name=None, x_text=None, **kwargs):
        super().__init__(f_center, width, height, color, name, x_text, **kwargs)
    
    def _get_segments(self, xi, xo):
        if xi > xo:
            return [], []
        
        fmin, fmax = self.get_bounds()
        fmin = max(fmin, xi)
        fmax = min(fmax, xo)
        x = [fmin, fmin, fmax, fmax]
        y = [0, self.height, self.height, 0]
        return x, y
       
class TriangleComponent(FreqComponent):
    def __init__(self, f_center, width=None, height=1, color='blue', name=None, x_text=None, **kwargs):
        super().__init__(f_center, width, height, color, name, x_text, **kwargs)

    def function(self, f)->float:
        """
        Calculate the magnitude response at a given frequency.

        This function computes a triangular response centered at self.f_center,
        returning a value proportional to the distance from the center frequency.
        The response is maximum (self.height) at the center frequency and decreases
        linearly to zero at the frequency bounds.

        Args:
            f (float): The frequency at which to calculate the response.

        Returns:
            float: The magnitude response at frequency f. Returns self.height at the 
                   center frequency and decreases linearly to 0.0 at the bounds 
                   (fmin and fmax). Returns 0.0 if f is outside the bounds.
        """
        fmin, fmax = self.get_bounds()
        if fmin <= f <= fmax:
            return self.height * (1 - abs(f - self.f_center) / (self.width / 2))
        else:
            return 0.0

    def _get_segments(self, xi, xo):
        if xi > xo:
            return [], []
        
        fmin, fmax = self.get_bounds()
        fmin = max(fmin, xi)
        fmax = min(fmax, xo)
        x = [fmin]
        y = [self.function(fmin)]

        if fmin <= self.f_center <= fmax:
            x.append(self.f_center)
            y.append(self.function(self.f_center))
        x.append(fmax)
        y.append(self.function(fmax))
        return x, y
    
class RightTriangleComponent(FreqComponent):
    def __init__(self, f_center, width, height=1.0, color='orange', name=None, x_text=None, **kwargs):
        super().__init__(f_center=f_center, width=width, height=height, color=color, name=name, x_text=x_text, **kwargs)
       
    def function(self, f)->float:
        """
        Calculate the normalized height value for a given frequency within the bounds.
        
        Args:
            f (float): The frequency value to normalize.
        
        Returns:
            float: The normalized height value proportional to the frequency within bounds.
                   Returns 0.0 if the frequency is outside the valid range.
        
        Note:
            The function maps a frequency value to a height value based on the object's
            dimensions and bounds. If the frequency is within [fmin, fmax], it returns
            a proportional height value; otherwise returns 0.0.
        """
        fmin, fmax = self.get_bounds()
        if fmin <= f <= fmax:
            return self.height * (f - fmin) / self.width
        else:
            return 0.0
        
    def _get_segments(self, xi, xo):
        if xi > xo:
            return [], []
        
        fmin, fmax = self.get_bounds()
        fmin = max(fmin, xi)
        fmax = min(fmax, xo)
        x = []
        y = []

        if fmin == self.f_center:
            x.append(fmin)
            y.append(0)
        x.append(fmin)
        y.append(self.function(fmin))
        x.append(fmax)
        y.append(self.function(fmax))
        
        return x, y

class LeftTriangleComponent(FreqComponent):
    def __init__(self, f_center, width, height=1.0, color='orange', name=None, x_text=None, **kwargs):
        super().__init__(f_center=f_center, width=width, height=height, color=color, name=name, x_text=x_text, **kwargs)
    
    def function(self, f)->float:
        """
        Calculate the scaled vertical position for a given frequency value.
        Maps a frequency value within the defined bounds to a proportional height,
        returning 0.0 if the frequency is outside the valid range.
        Args:
            f: The frequency value to be mapped to a vertical position.
        Returns:
            float: The scaled height corresponding to the frequency value.
                   Returns the calculated position if f is within bounds [fmin, fmax],
                   otherwise returns 0.0.
        """
        fmin, fmax = self.get_bounds()

        if fmin <= f <= fmax:
            return self.height * (fmax - f) / self.width
        else:
            return 0.0
        
    def _get_segments(self, xi, xo):
        if xi > xo:
            return [], []
        
        fmin, fmax = self.get_bounds()
        fmin = max(fmin, xi)
        fmax = min(fmax, xo)
        x = [fmin, fmax]
        y = [self.function(fmin), self.function(fmax)]
        if fmax == self.f_center:
            x.append(fmax)
            y.append(0)
        
        return x, y

