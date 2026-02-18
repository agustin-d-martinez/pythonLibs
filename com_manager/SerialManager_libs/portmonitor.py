from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtSerialPort import QSerialPortInfo


class PortMonitor(QObject):
    port_added = Signal(QSerialPortInfo)
    port_removed = Signal(QSerialPortInfo)

    def __init__(self, interval=1000):
        super().__init__()
        self._known_ports = {
            port.portName()
            for port in QSerialPortInfo.availablePorts()
        }

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._scan)
        self._timer.start(interval)

    def _scan(self):
        ports = QSerialPortInfo.availablePorts()
        current_names = {port.portName() for port in ports}

        # Nuevos
        for port in ports:
            name = port.portName()
            if name not in self._known_ports:
                self.port_added.emit(port)

        # Eliminados
        for port in ports:
            name = port.portName()
            if name in self._known_ports - current_names:
                self.port_removed.emit(port)
                
        self._known_ports = current_names
