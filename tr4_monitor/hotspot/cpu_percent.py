# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import psutil

from common import right_text
from fonts import default


def render(draw, width, height):
    percent = psutil.cpu_percent()
    freq = psutil.cpu_freq().current
    draw.text((0, 0), f'CPU   {freq:.0f} MHz', fill='white', font=default)
    right_text(draw, width, 0, text=f'{percent:.2f}%', font=default)
