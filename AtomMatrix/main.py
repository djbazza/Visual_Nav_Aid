# This example demonstrates a peripheral implementing the Nordic UART Service (NUS).

# This example demonstrates the low-level bluetooth module. For most
# applications, we recommend using the higher-level aioble library which takes
# care of all IRQ handling and connection management. See
# https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble

import atom
import time
import bluetooth
from ble_advertising import advertising_payload

from micropython import const

COLOUR_OFF = (0, 0, 0)
COLOUR = (200, 200, 0)
delay = 100

dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

a = atom.Matrix()
a.set_pixels_color(*COLOUR_OFF)
dispType = "2lines"
i = 0
j = 0

def set_screen(dm):
    i = 0
    for n in dm:
        if n == 0:
            a.set_pixel_color(i, 0, 0, 0)
        else:
            a.set_pixel_color(i, *COLOUR)
        i += 1

def dispMatrix(i, j):
    DispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(5):
        for y in range(5):
            if x == i:
                DispMatrix[x*5+y] = 1
            elif y == j:
                DispMatrix[x*5+y] = 1
            else:
                DispMatrix[x*5+y] = 0
    return DispMatrix

def rotMatrix(m, q):
    if q == 1:
        for o in range(5):
            m[(o*5)-5] = 0
    elif q == 5:
        for o in range(5):
            m[o] = 0
    for a in range(q):
        m.insert(len(m) - 1, m.pop(0))
    return m

def revMatrix(m, q):
    if q == 1:
        for o in range(5):
            m[(o*5)-1] = 0
    elif q == 5:
        for o in range(5):
            m[24-o] = 0
    for a in range(q):
        m.insert(0, m.pop(len(m) - 1))
    return m


def goForward():
    global i
    global dispMatrix
    dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if dispType == "arrow":
        dispMatrix = [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    elif dispType == "shortArrow":
        dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
    elif dispType == "2lines":
        dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    else:
        dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    for i in range(5):
        # dispMatrix = dispMatrix [5: ] + dispMatrix[ :5]
        set_screen(dispMatrix)
        dispMatrix = rotMatrix(dispMatrix, 5)
        time.sleep_ms(delay)

def goBack():
    global i
    global dispMatrix
    dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if dispType == "arrow":
        dispMatrix = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
    elif dispType == "shortArrow":
        dispMatrix = [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif dispType == "2lines":
        dispMatrix = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        dispMatrix = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(5):
        set_screen(dispMatrix)
        dispMatrix = revMatrix(dispMatrix, 5)
        time.sleep_ms(delay)

def goLeft():
    global i
    global dispMatrix
    dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if dispType == "arrow":
        dispMatrix = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
    elif dispType == "shortArrow":
        dispMatrix = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    elif dispType == "2lines":
        dispMatrix = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1]
    else:
        dispMatrix = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    for i in range(5):
        set_screen(dispMatrix)
        dispMatrix = rotMatrix(dispMatrix, 1)
        # dispMatrix.insert(len(dispMatrix) - 1, dispMatrix.pop(0))
        time.sleep_ms(delay)

def goRight():
    global i
    global dispMatrix
    dispMatrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if dispType == "arrow":
        dispMatrix = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    elif dispType == "shortArrow":
        dispMatrix = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    elif dispType == "2lines":
        dispMatrix = [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0]
    else:
        dispMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    for i in range(5):
        set_screen(dispMatrix)
        dispMatrix = revMatrix(dispMatrix, 1)
        # dispMatrix.insert(0, dispMatrix.pop(len(dispMatrix) - 1))
        time.sleep_ms(delay)

def update_display(new_val):
    global dispType
    # Clear the display.
    a.set_pixels_color(*COLOUR_OFF)

    global COLOUR
    if new_val == "FORWARD":
        goForward()
    elif new_val == "BACK":
        goBack()
    elif new_val == "LEFT":
        goLeft()
    elif new_val == "RIGHT":
        goRight()
    elif new_val == "arrow" or new_val == "shortArrow" or new_val == "2lines" or new_val == "lines":
        dispType = new_val
    elif new_val[0] == 'C':
        nc = list(COLOUR)
        i = 0
        for c in tuple(new_val.split(" ")):
            if c != 'C':
                print("c: ", c)
                nc[i] = int(c)
                i += 1
        COLOUR = tuple(nc)
    elif new_val[0] == 'D':
        print("delay: ", new_val[1: ], "ms")
        global delay
        delay = int(new_val[1: ])

    a.set_pixels_color(*COLOUR_OFF)


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)


class BLEUART:
    def __init__(self, ble, name="direction-assist", rxbuf=100):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        # Increase the size of the rx buffer and enable append mode.
        self._ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        # Optionally add services=[_UART_UUID], but this is likely to make the payload too large.
        self._payload = advertising_payload(name=name, appearance=_ADV_APPEARANCE_GENERIC_COMPUTER)
        self._advertise()

    def irq(self, handler):
        self._handler = handler

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if conn_handle in self._connections and value_handle == self._rx_handle:
                self._rx_buffer += self._ble.gatts_read(self._rx_handle)
                if self._handler:
                    self._handler()

    def any(self):
        return len(self._rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def write(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def close(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


def nav():

    ble = bluetooth.BLE()
    uart = BLEUART(ble)

    def on_rx():
        direct = uart.read().decode().strip()
        update_display(direct)
        print("rx: ", direct)

    uart.irq(handler=on_rx)
    try:
        while True:
            # uart.write(uart.read().decode().strip() + "\n")
            time.sleep_ms(1000)
    except KeyboardInterrupt:
        pass

    uart.close()


if __name__ == "__main__":
    nav()
