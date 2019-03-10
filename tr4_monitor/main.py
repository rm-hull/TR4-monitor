# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import os
import argparse
import time

from luma.core.cmdline import get_choices, get_transformer_choices
from luma.core.virtual import viewport, snapshot
from luma.core.render import canvas
from PIL import Image

from fonts import chicago, proggy_tiny
from common import center_text


def create_parser():
    emulator_choices = sorted(get_choices('luma.emulator.device'))
    rotation_choices = [0, 1, 2, 3]
    transformer_choices = get_transformer_choices()

    parser = argparse.ArgumentParser(description='TR4 system monitor',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--emulator', '-e',
        type=str,
        dest='emulator',
        default=None,
        help=f'Use specific luma.emulator device, one of: {", ".join(emulator_choices)}',
        choices=emulator_choices,
        metavar='DISPLAY')

    parser.add_argument('--rotate', '-r',
        type=int,
        default=0,
        help='Rotation factor. Allowed values are: {0}'.format(', '.join([str(x) for x in rotation_choices])),
        choices=rotation_choices,
        metavar='ROTATION')

    emulator_group = parser.add_argument_group('Emulator')
    emulator_group.add_argument('--transform', type=str, default='scale2x', help='Scaling transform to apply (emulator only). Allowed values are: {0}'.format(', '.join(transformer_choices)), choices=transformer_choices, metavar='TRANSFORM')
    emulator_group.add_argument('--scale', type=int, default=2, help='Scaling factor to apply (emulator only)')
    emulator_group.add_argument('--duration', type=float, default=0.01, help='Animation frame duration (gifanim emulator only)')
    emulator_group.add_argument('--loop', type=int, default=0, help='Repeat loop, zero=forever (gifanim emulator only)')
    emulator_group.add_argument('--max-frames', type=int, help='Maximum frames to record (gifanim emulator only)')

    try:  # pragma: no cover
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    return parser


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


def hw_monitor(device):
    from hotspot import cpu_percent, uptime, system_load, network, memory, disk
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'amd-ryzen-logo.png'))
    logo = Image.open(img_path)

    virtual = viewport(device, width=device.width, height=768)
    with canvas(virtual) as draw:
        draw.bitmap((0, 0), logo, fill='white')
        center_text(draw, device.width, 40, 'Threadripper 1950x', font=chicago, fill='white')
        center_text(draw, device.width, 54, '4.18.0-16-generic', font=proggy_tiny, fill='white')

    time.sleep(5.0)

    offset = 76
    virtual.add_hotspot(snapshot(device.width, 12, cpu_percent.render, interval=0.5), (0, offset))
    virtual.add_hotspot(snapshot(device.width, 12, system_load.render, interval=1.0), (0, offset + 12))
    virtual.add_hotspot(snapshot(device.width, 12, uptime.render, interval=0.1), (0, offset + 24))
    virtual.add_hotspot(snapshot(device.width, 12, memory.render, interval=5.0), (0, offset + 36))
    virtual.add_hotspot(snapshot(device.width, 12, disk.directory('/'), interval=5.0), (0, offset + 48))
    virtual.add_hotspot(snapshot(device.width, 12, network.interface('wlp2s0'), interval=2.0), (0, offset + 60))

    for y in pause_every(12, 40, position(128)):
        virtual.set_position((0, y))
        time.sleep(0.05)


def main():
    args = create_parser().parse_args()
    if args.emulator:
        import luma.emulator.device
        Device = getattr(luma.emulator.device, args.emulator)
        device = Device(mode='1', **vars(args))
    else:
        from luma.oled.device import ssd1309
        from ftdi import get_luma_compatible_serial_interface
        serial = get_luma_compatible_serial_interface()
        device = ssd1309(serial, **vars(args))

    hw_monitor(device)


if __name__ == '__main__':
    main()
