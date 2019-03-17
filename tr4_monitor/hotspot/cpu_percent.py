# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import psutil

from common import right_text
from fonts import default


def render(draw, width, height):
    pct = psutil.cpu_percent()
    draw.text((0, 0), 'CPU', fill='white', font=default)
    right_text(draw, width, 0, text=f'{pct:.2f}%', font=default)
