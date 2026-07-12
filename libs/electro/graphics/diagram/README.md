# SpectrumGraphics

`SpectrumGraphics` Librería en Python diseñada para la representación visual de espectros de frecuencia.  
Permite generar componentes espectrales ideales, combinarlos, filtrarlos y visualizar su estructura de manera clara y modular.

---

## Características principales

### Representación de espectros
La librería permite construir espectros a partir de diferentes tipos de componentes fundamentales.

Clases disponibles:
- `Spectrum`

### Componentes espectrales
Componentes básicos y compuestos para formar espectros arbitrarios:

- `FreqComponent`
- `DeltaComponent`
- `BlockComponent`
- `LeftTriangleComponent`
- `RightTriangleComponent`
- `TriangleComponent`

### Componentes de filtrado
Filtros ideales representados como componentes espectrales:

- `FilterComponent`
- `LowPassFilterComponent`
- `HighPassFilterComponent`
- `BandPassFilterComponent`
- `BandStopFilterComponent`

---

## Estructura del paquete

```
SpectrumGraphics/
    __init__.py
    Spectrum.py
    FreqComponent.py
    FilterComponent.py
    setup.py
```

---

## Importación

```python
from SpectrumGraphics import (
    Spectrum,
    FreqComponent, DeltaComponent, BlockComponent,
    LeftTriangleComponent, RightTriangleComponent, TriangleComponent,
    FilterComponent, LowPassFilterComponent, HighPassFilterComponent,
    BandPassFilterComponent, BandStopFilterComponent
)
```

---

## Licencia

MIT License
