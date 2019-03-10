# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import psutil

from common import right_text
from fonts import proggy_tiny


def render(draw, width, height):
    pct = psutil.cpu_percent()
    draw.text((0, 0), 'CPU:', fill='white', font=proggy_tiny)
    right_text(draw, width, 0, text=f'{pct:.2f}%', font=proggy_tiny)
