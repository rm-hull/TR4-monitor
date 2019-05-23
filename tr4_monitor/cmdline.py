# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import argparse

from luma.core.cmdline import get_choices, get_transformer_choices


def create_parser():
    rotation_choices = [0, 1, 2, 3]
    color_choices = ['1', 'RGB', 'RGBA']

    parser = argparse.ArgumentParser(description='TR4 system monitor',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--config', '-f',
        type=str,
        help='Load configuration settings from a file')

    parser.add_argument('--rotate', '-r',
        type=int,
        default=0,
        help='Rotation factor. Allowed values are: {0}'.format(', '.join([str(x) for x in rotation_choices])),
        choices=rotation_choices,
        metavar='ROTATION')

    parser.add_argument('--title', '-t',
        type=str,
        help='Show title instead of CPU name',
        metavar='TITLE')

    parser.add_argument('--network', '-n',
        type=str,
        default='en0',
        help='Network interface to report usage against.',
        metavar='NETWORK')

    parser.add_argument('--mode', type=str, default='RGB', help='Colour mode (SSD1322, SSD1325 and emulator only). Allowed values are: {0}'.format(', '.join(color_choices)), choices=color_choices, metavar='MODE')

    emulator_choices = sorted(get_choices('luma.emulator.device'))
    if emulator_choices:
        transformer_choices = get_transformer_choices()

        parser.add_argument('--emulator', '-e',
            type=str,
            default=None,
            help=f'Use specific luma.emulator device (rather than a real display), one of: {", ".join(emulator_choices)}',
            choices=emulator_choices,
            metavar='DISPLAY')

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
