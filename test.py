import time

from pyftdi.spi import SpiController
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1309

CS = 3
RESET = 4
DC = 5

def ftdi_pin(pin):
    return 2 << pin

class FTDI_WRAPPER_SPI:
    def __init__(self, spi_port):
        self._spi_port = spi_port

    def open(self, port, device):
        print(f'SPI: open(port={port}, device={device})')

    def writebytes(self, data):
        print(f'SPI: writebytes(data={data})')
        self._spi_port.write(data)

    def close(self):
        print('SPI: close()')


class FTDI_WRAPPER_GPIO:

    OUT = 1
    LOW = 0
    HIGH = 1

    def __init__(self, gpio):
        self._gpio = gpio
        self._data = 0

    def setup(self, pin, direction):
        print(f'GPIO: setup(pin={pin}, direction={direction}')

    def output(self, pin, value):
        mask = ftdi_pin(pin)
        self._data &= ~mask
        if value:
            self._data |= mask

        print(f'GPIO: output(pin={pin}, value={value}) --> {self._data}')
        self._gpio.write(self._data)


ftdi_spi = SpiController(cs_count=1)
ftdi_spi.configure('ftdi://::/1')

slave = ftdi_spi.get_port(cs=CS-3, freq=1E6, mode=0)
ftdi_gpio = ftdi_spi.get_gpio()

# AD4 (RES) and AD5 (DC) configured as outputs
reset_and_dc = outputs = ftdi_pin(RESET) | ftdi_pin(DC)
print(reset_and_dc)
ftdi_gpio.set_direction(reset_and_dc, outputs)

serial = spi(
    FTDI_WRAPPER_SPI(slave),
    gpio=FTDI_WRAPPER_GPIO(ftdi_gpio),
    gpio_DC=DC,
    gpio_RST=RESET)

device = ssd1309(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "Hello World", fill="white")

time.sleep(5)

