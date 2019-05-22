# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import os
import sys
import platform
import psutil
import signal

from luma.core.sprite_system import framerate_regulator
from luma.core.virtual import viewport, snapshot
from luma.core.cmdline import load_config
from luma.core.render import canvas
from PIL import Image

from cmdline import create_parser
from fonts import chicago, default
from common import center_text
from hotspot import cpu_percent, cpu_barchart, cpu_stats
from hotspot import uptime, system_load, loadavg_chart
from hotspot import network, memory, disk
from data_logger import DataLogger


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
    loadavg_data_logger = DataLogger(psutil.getloadavg, max_entries=device.width - 2).start()

    def keyboardInterruptHandler(signal, frame):
        loadavg_data_logger.stop()
        exit(0)

    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # Needs luma.core PR #161 merging
    # virtual = viewport(device, width=device.width, height=768, mode='RGBA', dither=True)
    virtual = viewport(device, width=device.width, height=768)
    with canvas(virtual) as draw:
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'amd-ryzen-logo.png'))
        logo = Image.open(img_path)
        draw.bitmap((0, 0), logo, fill='white')
        center_text(draw, device.width, 40, args.title or 'Threadripper 1950x', font=chicago, fill='white')
        center_text(draw, device.width, 54, f'{platform.system()} {platform.release().replace("-generic", "")}', font=default, fill='white')
        
    hotspots = [
        snapshot(device.width, 10, cpu_percent.render, interval=0.5),
        snapshot(device.width, cpu_barchart.height + 4, cpu_barchart.render, interval=0.5),
        snapshot(device.width, cpu_stats.height + 13, cpu_stats.render, interval=2),
        snapshot(device.width, uptime.height, uptime.render, interval=10),
        snapshot(device.width, 10, system_load.render, interval=1.0),
        snapshot(device.width, loadavg_chart.height, loadavg_chart.using(loadavg_data_logger), interval=1.0),
        snapshot(device.width, 10, memory.render, interval=5.0),
        snapshot(device.width, 20, disk.directory('/'), interval=5.0),
        snapshot(device.width, 30, network.interface(args.network), interval=2.0)
    ]

    offset = 64
    for hotspot in hotspots:
        virtual.add_hotspot(hotspot, (0, offset))
        offset += hotspot.height

    # time.sleep(5.0)
    for y in pause_every(64, 64, position(170)):
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
    if 'emulator' in args and args.emulator:
        import luma.emulator.device
        Device = getattr(luma.emulator.device, args.emulator)
        return Device(**vars(args))
    else:
        from luma.oled.device import ssd1309
        from luma.core.interface.serial import ftdi_spi
        return ssd1309(ftdi_spi(), **vars(args))


def main():
    try:
        args = get_args()
        device = get_device(args)
        hw_monitor(device, args)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
