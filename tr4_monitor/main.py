# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import os
import sys
import platform
import time

from luma.core.sprite_system import framerate_regulator
from luma.core.virtual import viewport, snapshot
from luma.core.cmdline import load_config
from luma.core.render import canvas
from PIL import Image

from cmdline import create_parser
from fonts import chicago, proggy_tiny
from common import center_text


def position(max):
    forwards = range(0, max)
    backwards = range(max, 0, -1)
    while True:
        for x in forwards:
            yield x
        for x in backwards:
            yield x


def pause_every(interval, stop_for, generator):
    try:
        while True:
            x = next(generator)
            if x % interval == 0:
                for _ in range(stop_for):
                    yield x
            else:
                yield x
    except StopIteration:
        pass


def hw_monitor(device, args):
    from hotspot import cpu_percent, uptime, system_load, network, memory, disk, ip_addrs
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'amd-ryzen-logo.png'))
    logo = Image.open(img_path)

    virtual = viewport(device, width=device.width, height=768)
    with canvas(virtual) as draw:
        draw.bitmap((0, 0), logo, fill='white')
        center_text(draw, device.width, 40, args.title or 'Threadripper 1950x', font=chicago, fill='white')
        center_text(draw, device.width, 54, f'{platform.system()} {platform.release().replace("-generic", "")}', font=proggy_tiny, fill='white')

    offset = 76
    virtual.add_hotspot(snapshot(device.width, 12, cpu_percent.render, interval=0.5), (0, offset))
    virtual.add_hotspot(snapshot(device.width, 12, system_load.render, interval=1.0), (0, offset + 12))
    virtual.add_hotspot(snapshot(device.width, 12, uptime.render, interval=0.1), (0, offset + 24))
    virtual.add_hotspot(snapshot(device.width, 12, memory.render, interval=5.0), (0, offset + 36))
    virtual.add_hotspot(snapshot(device.width, 12, disk.directory('/'), interval=5.0), (0, offset + 48))
    virtual.add_hotspot(snapshot(device.width, 12, network.interface(args.network), interval=2.0), (0, offset + 60))
    virtual.add_hotspot(snapshot(device.width, 24, ip_addrs.discover(), interval=1000), (0, offset + 72))

    time.sleep(5.0)
    for y in pause_every(12, 40, position(132)):
        with framerate_regulator():
            virtual.set_position((0, y))


def get_args():
    actual_args = sys.argv[1:]
    parser = create_parser()
    args = parser.parse_args(actual_args)
    if args.config:
        config = load_config(args.config)
        args = parser.parse_args(config + actual_args)
    return args


def get_device(args):
    if args.emulator:
        import luma.emulator.device
        Device = getattr(luma.emulator.device, args.emulator)
        return Device(mode='1', **vars(args))
    else:
        from luma.oled.device import ssd1309
        from ftdi import get_luma_compatible_serial_interface
        serial = get_luma_compatible_serial_interface()
        return ssd1309(serial, **vars(args))


def main():
    try:
        args = get_args()
        device = get_device(args)
        hw_monitor(device, args)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
