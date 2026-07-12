# Circuitanalysis

`Circuitanalysis` librería en Python orientada al análisis de circuitos tanto en el dominio del tiempo como en el dominio de la frecuencia. Incluye herramientas simbólicas y funciones de visualización.  

---

## Características principales

### Análisis en frecuencia
Incluye métodos para realizar análisis espectral por FFT, obteniendo magnitudes, fases y componentes relevantes.

Clases disponibles:
- `fft_analisys`

---

## Visualización
Herramientas para graficar señales, espectros y resultados de análisis.

Clases disponibles:
- `graphic`

---

## Análisis simbólico
Módulo para trabajar con expresiones simbólicas aplicadas a circuitos eléctricos: impedancias, admitancias, funciones de transferencia, transformada de Laplace y otras utilidades.

Clases disponibles:
- `symbolic`

---

## Estructura del paquete

```
Circuitanalysis/
    __init__.py
    fft.py
    graphic.py
    symbolic.py
    setup.py
```

---

## Importación

```python
from Circuitanalysis import fft_analisys, graphic, symbolic
```

---

## Metadatos

```
Author: Agustin Damian Martinez
Version: 0.1.0
Credits: None
```

---

## Licencia

MIT License
