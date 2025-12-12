# pythonLibs

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Last Update](https://img.shields.io/github/last-commit/agustin-d-martinez/pythonLibs)

`pythonLibs` Colección de módulos Python realizados a lo largo de la carrera y trabajo. Cumplen funciones variadas (y en su mayoría didácticas). Algunos ejemplos son: análisis de señales, comunicaciones, modulación digital/analógica y herramientas para representar o procesar espectros.  
Cada módulo es independiente y puede utilizarse por separado.

---

## 📑 Tabla de contenidos
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Módulos incluidos](#módulos-incluidos)
  - [circuitanalysis](#circuitanalysis)
  - [modulations](#modulations)
  - [spectrumgraphic](#spectrumgraphic)
- [Requerimientos](#requerimientos)
- [Notebooks de prueba](#notebooks-de-prueba)
- [Roadmap](#roadmap)
- [Licencia](#licencia)
- [Contribuciones](#contribuciones)

---

## Estructura del proyecto
### `circuitanalysis`
Herramientas para:
- FFT y análisis espectral  
- Gráficos  
- Análisis simbólico  
- Operaciones típicas de circuitos  

### `modulations`
Incluye modulaciones:
- Analógicas: DSB, DSB_SC, SSB, FM, PM  
- Digitales ASK, PSK, QAM, FSK  
- CPM (GMSK/MSK)  
- Códigos de línea clásicos  
- Generación de portadoras  

### `spectrumgraphic`
Librería para construir, combinar y filtrar componentes espectrales de forma modular.

---

## Instalación
Para instalar alguna de las librerías se deberán descargar las mismas y utilizarlas en un entorno de python. Se recomienda clonado del repo como se indica a continuación:

```bash
git clone https://github.com/agustin-d-martinez/pythonLibs.git
cd pythonLibs
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

---

## Módulos incluidos

### circuitanalysis
Incluye:

* `fft_analisys`
* `graphic`
* `symbolic`

**Importación recomendada:**
```python
from circuitanalysis import fft_analisys, graphic, symbolic
```

---

### modulations
1. **Modulación analógica**
   * `DSB`, `DSB_SC`, `SSB`
   * `FM`, `PM`

2. **ASK**
   * `bask`, `ask4`, `ask8`, `m_ask`

3. **PSK**
   * `bpsk`, `qpsk`, `oqpsk`, `pi4_qpsk`, `psk16`, `m_psk`

4. **QAM**
   * `qam16`, `qam64`, `qam1024`, `m_qam`

5. **FSK**
   * `bfsk`, `fsk4`, `gfsk`, `m_fsk`

6. **CPM**
   * `msk`, `gmsk`

7. **Códigos de línea**
   * `unipolar_nrz`, `polar_nrz`, `bipolar_nrz`
   * `unipolar_rz`, `polar_rz`, `bipolar_rz`
   * `manchester`, `differential_manchester`, `twoB1Q`

8. **Portadora**
   * `carrier`

**Importación recomendada:**
```python
from modulations import bpsk, qam16, FM
```

---

### spectrumgraphic
Incluye:
* `Spectrum`
* `FreqComponent`
* `DeltaComponent`
* `BlockComponent`
* `LeftTriangleComponent`
* `RightTriangleComponent`
* `TriangleComponent`
* `FilterComponent`
* `LowPassFilterComponent`
* `HighPassFilterComponent`
* `BandPassFilterComponent`
* `BandStopFilterComponent`

**Importación recomendada:**

```python
from spectrumgraphic import Spectrum, DeltaComponent, BandPassFilterComponent
```

---

## Requerimientos

```bash
pip install -r requirements.txt
```

---

## Notebooks de prueba

```
test_circuitanalisis.ipynb
test_modulation.ipynb
test_spectrum.ipynb
```

---

## Roadmap

### Mejoras planificadas
* [ ] Agregar OFDM y modulaciones multiportadora
* [ ] Implementar filtros digitales (FIR, IIR) dentro de circuitanalysis
* [ ] Ampliar CPM con variantes avanzadas
* [ ] Incorporar herramientas de demodulación
* [ ] Mejorar documentación interna con ejemplos detallados
* [ ] Subir el paquete a PyPI
* [ ] Agregar test unitarios automatizados (pytest)

---

## Licencia

MIT License — ver archivo `LICENSE`.

---

## Contribuciones

Las contribuciones son bienvenidas.
Para colaborar:

1. Hacer fork
2. Crear rama `feature/...`
3. Hacer PR

---
