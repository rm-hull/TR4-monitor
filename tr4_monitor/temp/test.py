import time

from luma.core.render import canvas
from luma.oled.device import ssd1309

from ftdi import get_luma_compatible_serial_interface

serial = get_luma_compatible_serial_interface()
device = ssd1309(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "Hello World", fill="white")

time.sleep(5)
