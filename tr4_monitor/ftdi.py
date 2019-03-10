# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from pyftdi.spi import SpiController

import luma


def ftdi_pin(pin):
    return 1 << pin


class FTDI_WRAPPER_SPI:
    def __init__(self, spi_port):
        self._spi_port = spi_port

    def open(self, port, device):
        pass

    def writebytes(self, data):
        self._spi_port.write(data)

    def close(self):
        pass


class FTDI_WRAPPER_GPIO:

    LOW = 0
    HIGH = OUT = 1

    def __init__(self, gpio):
        self._gpio = gpio
        self._data = 0

    def setup(self, pin, direction):
        pass

    def output(self, pin, value):
        mask = ftdi_pin(pin)
        self._data &= ~mask
        if value:
            self._data |= mask

        self._gpio.write(self._data)


def get_luma_compatible_serial_interface(CS=3, DC=5, RESET=6):
    spi = SpiController(cs_count=1)
    spi.configure('ftdi://::/1')

    slave = spi.get_port(cs=CS - 3, freq=12E6, mode=0)
    gpio = spi.get_gpio()

    # RESET and DC configured as outputs
    pins = ftdi_pin(RESET) | ftdi_pin(DC)
    gpio.set_direction(pins, pins & 0xFF)

    return luma.core.interface.serial.spi(
        FTDI_WRAPPER_SPI(slave),
        FTDI_WRAPPER_GPIO(gpio),
        gpio_DC=DC,
        gpio_RST=RESET)
