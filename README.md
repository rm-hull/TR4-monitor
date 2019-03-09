# TR4 Monitor
Small utility script to display TR4 system information on a 2.42" SSD1309 OLED

## Bill of materials

### Software
* Python 3
* [Luma.OLED](https://luma-oled.readthedocs.io/en/latest/)
* [PySensors3](https://pypi.org/project/PySensors3/)
* [PyFTDI](http://eblot.github.io/pyftdi)

### Hardware
* [2.42" OLED display](https://www.aliexpress.com/item/2-42-inch-LCD-Screen-12864-OLED-Display-Module-IIC-I2C-SPI-Serial-C51-STM32-SSD1309/32857123469.html)
* [USB FT232H Adapter](https://www.aliexpress.com/item/NEW-CJMCU-FT232H-Multifunction-High-Speed-USB-to-JTAG-UART-FIFO-SPI-I2C-Module/32817479989.html)
* [Dark smoked grey acrylic sheet](https://www.ebay.co.uk/itm/142366439906)
* [9 Pin Header To Dual USB 2.0 Type A Female](https://www.ebay.co.uk/itm/283026195250)

## Installation

1. Instal natve dependencies as follows:

```
sudo apt install libusb-1.0 libftdi1-2
```

2. Create a _udev_ configuration file to allow user-space processes to access
   the FTDI device. Typically, create a file, _/etc/udev/rules.d/11-ftdi.rules_:

```
# /etc/udev/rules.d/11-ftdi.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6001", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6011", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6014", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6015", GROUP="plugdev", MODE="0666"
```

3. Add your user to the _plugdev_ group (log out and back in again to get the
   command to be effective):

```
sudo adduser $USER plugdev
```

## Pin-outs

| OLED Pin | OLED Name | FT232 Pin | FT232 Function | Remarks |
|----------|----------|---------|----------|-------|
| 1 | GND | GND | GND | Ground |
| 2 | VCC | +3.3V | 3V3 | +3.3V Power |
| 3 | SCL | AD0 | SCLK | Serial Clock |
| 4 | SDA | AD1 | MOSI | Serial Data |
| 5 | RES | AD6 | GPIO 6 | Reset |
| 6 | DC | AD5 | GPIO 5 | Data/Command |
| 7 | CS | AD3 | CE0 | Chip Select |


## References
* https://github.com/rm-hull/luma.oled/pull/231
* https://github.com/rm-hull/luma.oled/issues/185
* https://github.com/eblot/pyftdi/issues/38#issuecomment-267062576
* http://eblot.github.io/pyftdi/pinout.html
* https://developer.amd.com/resources/developer-guides-manuals/
