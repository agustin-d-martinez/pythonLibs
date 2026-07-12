# modulationToolkit

`modulationToolkit` librería en Python para la simulación y generación de señales de modulación digital y analógica.  
Incluye modulaciones ASK, PSK, QAM, FSK, CPM, códigos de línea y modulaciones analógicas clásicas.

---

## Contenido del paquete

### Modulación analógica
- `DSB`
- `DSB_SC`
- `SSB`
- `FM`
- `PM`

### ASK
- `bask`
- `ask4`
- `ask8`
- `m_ask`

### PSK
- `bpsk`
- `qpsk`
- `oqpsk`
- `pi4_qpsk`
- `psk16`
- `m_psk`

### QAM
- `qam16`
- `qam64`
- `qam1024`
- `m_qam`

### FSK
- `bfsk`
- `fsk4`
- `gfsk`
- `m_fsk`

### CPM
- `msk`
- `gmsk`

### Generación de portadora
- `carrier`

### Códigos de línea
- `unipolar_nrz`
- `polar_nrz`
- `bipolar_nrz`
- `unipolar_rz`
- `polar_rz`
- `bipolar_rz`
- `manchester`
- `differential_manchester`
- `twoB1Q`

### Helpers internos
- `_check_array`
- Predenta más helpers que no son publicados externamente.

---

## Estructura del paquete

```
modulationToolkit/
    __init__.py
    analog.py
    ask.py
    psk.py
    qam.py
    fsk.py
    cpm.py
    carriers.py
    line_code.py
    helpers.py
```

---

## Instalación

Simplemente copiar la carpeta dentro de tu proyecto:

```
your_project/
    modulations/
```

Luego importar:

```python
import modulations as mod
```

O funciones específicas:

```python
from modulations import bpsk, FM, qam16
```

---

## Ejemplos de uso

Ver notebooks de test

---

## Licencia

MIT License
