# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import psutil

from common import right_text
from fonts import default


def _get_current(reading):
    return reading.current


def render(draw, width, height):
    percent = psutil.cpu_percent()
    cpu_freqs = psutil.cpu_freq(percpu=True)
    max_freq = max(cpu_freqs, key=_get_current).current / 1024.0
    min_freq = min(cpu_freqs, key=_get_current).current / 1024.0
    
    draw.text((0, 0), 'CPU', fill='white', font=default)
    right_text(draw, width, 0, text=f'{percent:.1f}%', font=default)

    if max_freq != min_freq:
        right_text(draw, width - 32, 0, text=f'{min_freq:.2f}/{max_freq:.2f} GHz', fill='white', font=default)
    else:
        right_text(draw, width - 40, 0, text=f'{max_freq:.2f} GHz', fill='white', font=default)
    