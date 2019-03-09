#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Simple benchmarking utility to measure performance.

Ported from:
https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py
"""

import sys
import time
from PIL import Image, ImageDraw

from luma.core.sprite_system import framerate_regulator
from luma.core.render import canvas
from luma.oled.device import ssd1309

from ftdi import get_luma_compatible_serial_interface



def primitives(device, draw):
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = device.height - padding - 1
    # Move left to right keeping track of the current x position for drawing shapes.
    x = padding
    # Draw an ellipse.
    draw.ellipse((x, top, x + shape_width, bottom), outline="red", fill="black")
    x += shape_width + padding
    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, bottom), outline="blue", fill="black")
    x += shape_width + padding
    # Draw a triangle.
    draw.polygon([(x, bottom), (x + shape_width / 2, top), (x + shape_width, bottom)], outline="green", fill="black")
    x += shape_width + padding
    # Draw an X.
    draw.line((x, bottom, x + shape_width, top), fill="yellow")
    draw.line((x, top, x + shape_width, bottom), fill="yellow")
    x += shape_width + padding
    # Write two lines of text.
    size = draw.textsize('World!')
    x = device.width - padding - size[0]
    draw.rectangle((x, top + 4, x + size[0], top + size[1]), fill="black")
    draw.rectangle((x, top + 16, x + size[0], top + 16 + size[1]), fill="black")
    draw.text((device.width - padding - size[0], top + 4), 'Hello', fill="cyan")
    draw.text((device.width - padding - size[0], top + 16), 'World!', fill="purple")
    # Draw a rectangle of the same size of screen
    draw.rectangle(device.bounding_box, outline="white")


def main():
    print("Testing display rendering performance")
    print("Press Ctrl-C to abort test\n")

    regulator = framerate_regulator(fps=0)  # Unlimited
    serial = get_luma_compatible_serial_interface()
    device = ssd1309(serial)

    image = Image.new(device.mode, device.size)
    draw = ImageDraw.Draw(image)
    primitives(device, draw)

    for i in range(5, 0, -1):
        sys.stdout.write("Starting in {0} seconds...\r".format(i))
        sys.stdout.flush()
        time.sleep(1)

    try:
        while True:
            with regulator:
                device.display(image)

            if regulator.called % 31 == 0:
                avg_fps = regulator.effective_FPS()
                avg_transit_time = regulator.average_transit_time()

                sys.stdout.write("#### iter = {0:6d}: render time = {1:.2f} ms, frame rate = {2:.2f} FPS\r".format(regulator.called, avg_transit_time, avg_fps))
                sys.stdout.flush()

    except KeyboardInterrupt:
        del image


if __name__ == "__main__":
    main()