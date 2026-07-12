# com_manager

`COM Manager` librería en Python con un único propósito. Administrar los puertos COM, permitiendo la conexión automática de un SerialPort al dispositivo conectado.  

La librería funciona para utilizar con `PySide6`.

---

## Características principales

### SerialManager
Incluye métodos para crear un serial y permitir que se autoconecte si logra reconocer la placa en un puerto com.
Además, incluye una clase base llamada `SerialDeviceIdentifier`. Esta permite al usuario colocar su propio protocolo de detección que será usado por el SerialManager. Se incluyen 2 ejemplos, uno bloqueante y otro que no lo es.

Clases disponibles:
- `SerialManager`
- `SerialDeviceIdentifier`

---

## PortMonitor
Herramientas auxiliar del manager. Lee periodicamente los puertos COM disponibles y emite una Signal si alguno se añadió o eliminó.

Clases disponibles:
- `PortMonitor`

---

## Estructura del paquete

```
lib/
    __init__.py
    portmonitor.py
    serialmanager.py
```

---

## Importación

```python
from SerialManager_libs.serialmanager import SerialManager, SerialDeviceIdentifier
from SerialManager_libs.portmonitor import PortMonitor
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
