from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from enum import Enum

from .portmonitor import PortMonitor

class SerialManagerState(Enum):
    DISCONNECTED = 0
    IDENTIFYING = 1
    CONNECTED = 2


class SerialManager(QObject):
    """
    Manages automatic discovery, connection and identification of serial devices.

    Responsibilities:
    - Monitor serial ports
    - Attempt automatic reconnection
    - Run device identification strategy
    - Provide high-level signals for application use
    """

    ################### Signals #################
    connected = Signal(str)  
    disconnected = Signal()
    data_received = Signal(bytes)
    error_occurred = Signal(str)

    ################### Constructor #################
    def __init__(self, port_monitor : PortMonitor , identifier: SerialDeviceIdentifier, parent = None):
        super().__init__(parent)
        self._vid = None
        self._pid = None

        self._serial = QSerialPort()
        self._serial.readyRead.connect(self._on_ready_read)
        self._serial.errorOccurred.connect(self._on_error)

        self._port_monitor = port_monitor
        self._port_monitor.port_removed.connect(self._handle_port_removed)

        self._state = SerialManagerState.DISCONNECTED
        self._identifier = identifier

        self._available_ports = []

    ################### Public API #################
    # AUTO-CONNECT Logic
    def auto_connect(self, vid: int|None = None, pid: int|None = None):
        self._vid = vid
        self._pid = pid

        # Existing ports
        self._available_ports = list(QSerialPortInfo.availablePorts())
        
        # Periodic check for new ports
        self._port_monitor.port_added.connect(self._on_port_added)
        self._try_next_port()

    # Serial Port Operations
    def disconnect(self):
        if self._serial.isOpen():
            self._serial.close()

        previous_state = self._state
        self._state = SerialManagerState.DISCONNECTED
        if previous_state != SerialManagerState.IDENTIFYING:
            self.disconnected.emit()      
            self._try_next_port()

    def send(self, data: bytes):
        if self._serial.isOpen():
            self._serial.write(data)

    def configure(self, baudrate: int = 115200, data_bits=QSerialPort.DataBits.Data8, 
                  parity=QSerialPort.Parity.NoParity, 
                  stop_bits=QSerialPort.StopBits.OneStop,
                  flow_control=QSerialPort.FlowControl.NoFlowControl):
        self._serial.setBaudRate(baudrate)
        self._serial.setDataBits(data_bits)
        self._serial.setParity(parity)
        self._serial.setStopBits(stop_bits)
        self._serial.setFlowControl(flow_control)

    def is_connected(self) -> bool:
        return self._state == SerialManagerState.CONNECTED

    ################### Auto-connect logic #################
    def _try_next_port(self):
        if self._serial.isOpen() or self._state != SerialManagerState.DISCONNECTED:
            return
        while self._available_ports:
            port_info = self._available_ports.pop(0)

            if not self._port_matches_filters(port_info):    #Needs to reactive this function
                continue

            self._serial.setPort(port_info)
            if not self._serial.open(QSerialPort.OpenModeFlag.ReadWrite):
                self.error_occurred.emit(self._serial.errorString())
                continue 

            self._identify_device()
            break
    
    def _port_matches_filters(self, port_info: QSerialPortInfo) -> bool:
        if self._vid is not None:
            if not (port_info.hasVendorIdentifier() and
                    port_info.vendorIdentifier() == self._vid):
                return False

        if self._pid is not None:
            if not (port_info.hasProductIdentifier() and
                    port_info.productIdentifier() == self._pid):
                return False

        return True

    def _handle_port_removed(self, port_info: QSerialPortInfo):
        if self._serial.isOpen() and self._serial.portName() == port_info.portName():
            self.disconnect()
        else:
            self._available_ports = [p for p in self._available_ports if p.portName() != port_info.portName()]

    def _on_port_added(self, port_info: QSerialPortInfo):
        self._available_ports.append(port_info)
        if self._state == SerialManagerState.DISCONNECTED and len(self._available_ports) == 1:
            self._try_next_port()

    ################### Identification logic #################
    def _identify_device(self):
        self._state = SerialManagerState.IDENTIFYING
        self._serial.readyRead.disconnect(self._on_ready_read)

        self._identifier.identified.connect(self._on_identified)
        self._identifier.failed.connect(self.disconnect)
        self._identifier.start(self._serial)
        
    def _on_identified(self):
        self._state = SerialManagerState.CONNECTED
        self._available_ports = []

        # De activate port monitor
        self._identifier.identified.disconnect(self._on_identified)
        self._identifier.failed.disconnect(self.disconnect)

        # Re activate serial port reading
        self._serial.readyRead.connect(self._on_ready_read)
        self.connected.emit(self._serial.portName())

    ################### Qt callbacks #################
    def _on_ready_read(self):
        data = self._serial.readAll().data()
        self.data_received.emit(data)

    def _on_error(self, error):
        if error != QSerialPort.SerialPortError.NoError:
            error_message = self._serial.errorString()
            if self._state == SerialManagerState.IDENTIFYING:
                error_message = f"Identification failed: {error_message}"
            self.disconnect()
            self.error_occurred.emit(error_message)


class SerialDeviceIdentifier(QObject):
    """
    Abstract base class for serial device identification strategies.

    Subclasses must implement `start()` and emit exactly one of:

    - `identified` when the device matches expected criteria.
    - `failed` when identification fails.

    The implementation may be blocking or non-blocking.
    """

    identified = Signal()
    failed = Signal()
    
    def start(self, serial: QSerialPort) -> None:
        raise NotImplementedError(
            "Subclasses must implement start() and emit either "
            "`identified` or `failed`."
        )


class BlockingIdentifier(SerialDeviceIdentifier):
    """
    Blocking identifier.

    Sends `id_command` and waits synchronously for `expected_response`.
    Fails if the expected response is not received within `timeout_ms`.
    """
    def __init__(self, id_command: bytes, expected_response: bytes, timeout_ms: int = 500, parent=None):
        super().__init__(parent)
        self._id_command = id_command
        self._expected_response = expected_response
        self._timeout_ms = timeout_ms

    def start(self, serial: QSerialPort) -> None:
        serial.write(self._id_command)
        if serial.waitForReadyRead(self._timeout_ms): 
            response = serial.readAll().data().strip() 
            if response == self._expected_response:
                self.identified.emit()
                return
        self.failed.emit()

class SimpleIdentifier(SerialDeviceIdentifier):
    '''
    Non blocking identifier. Sends "id_command" and waits "timeout_ms" for a response. Checks if the response is "expected_response". 
    '''
    def __init__(self, id_command: bytes, expected_response: bytes, timeout_ms: int = 500, parent=None):
        super().__init__(parent)
        self._id_command = id_command
        self._expected_response = expected_response
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_timeout)
        self._timeout_ms = timeout_ms
        self._serial: QSerialPort|None = None

    def start(self, serial: QSerialPort) -> None:
        self._serial = serial
        self._serial.write(self._id_command)
        self._timer.start(self._timeout_ms)

        try:
            self._serial.readyRead.disconnect(self._on_ready_read)
        except (TypeError, RuntimeError):
            pass
        self._serial.readyRead.connect(self._on_ready_read)
    
    def _on_ready_read(self):
        # Deactivate all
        self._timer.stop() 
        self._serial.readyRead.disconnect(self._on_ready_read)

        # Check Response
        response = self._serial.readAll().data().strip() 
        if response == self._expected_response:
            self.identified.emit()
            return
        self.failed.emit()

    def _on_timeout(self):
        try:
            self._serial.readyRead.disconnect(self._on_ready_read)
        except (TypeError, RuntimeError):
            pass
        self.failed.emit()

