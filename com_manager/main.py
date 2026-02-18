import sys

from PySide6.QtWidgets import *

from SerialManager_libs.serialmanager import SerialManager, SerialDeviceIdentifier
from SerialManager_libs.portmonitor import PortMonitor


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Test App")
        self.resize(500, 400)

        # UI
        layout = QVBoxLayout(self)

        self.status_label = QLabel("Status: Disconnected")
        layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.disconnect_btn)
        layout.addLayout(btn_layout)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        send_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.send_btn = QPushButton("Send")
        send_layout.addWidget(self.input_line)
        send_layout.addWidget(self.send_btn)
        layout.addLayout(send_layout)

        # Serial infrastructure
        self.port_monitor = PortMonitor()
        self.identifier = my_identifier()  # tu implementación
        self.serial_manager = SerialManager(self.port_monitor, self.identifier)

        # Signals
        self.connect_btn.clicked.connect(self.on_connect_clicked)
        self.disconnect_btn.clicked.connect(self.serial_manager.disconnect)
        self.send_btn.clicked.connect(self.on_send_clicked)

        self.serial_manager.connected.connect(self.on_connected)
        self.serial_manager.disconnected.connect(self.on_disconnected)
        self.serial_manager.data_received.connect(self.on_data_received)
        self.serial_manager.error_occurred.connect(self.on_error)

    # UI handlers
    def on_connect_clicked(self):
        # VID/PID de prueba (ajustalos)
        VID = None
        PID = None
        self.log.append("Trying to connect...")
        self.serial_manager.auto_connect(VID, PID)

    def on_send_clicked(self):
        text = self.input_line.text()
        if text:
            self.serial_manager.send((text + "\n").encode())
            self.log.append(f"> {text}")
            self.input_line.clear()

    # Serial callbacks
    def on_connected(self, port_name):
        self.status_label.setText(f"Status: Connected ({port_name})")
        self.log.append(f"Connected to {port_name}")

    def on_disconnected(self):
        self.status_label.setText("Status: Disconnected")
        self.log.append("Disconnected")

    def on_data_received(self, data: bytes):
        self.log.append(f"< {data.decode(errors='ignore')}")

    def on_error(self, message):
        self.log.append(f"[ERROR] {message}")


class my_identifier(SerialDeviceIdentifier):
    def start(self, serial):
        serial.write(b"ID?\n")
        if serial.waitForReadyRead(5000): 
            response = serial.readAll().data().decode().strip() 
            print(f"received: {response}")
            if response == "MEDIDAS_1_PROY":
                self.identified.emit()
                return
        
        self.failed.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
