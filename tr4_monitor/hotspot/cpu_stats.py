# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import psutil

from common import right_text
from fonts import default

height = 30


def render(draw, width, height):
    stats = psutil.cpu_stats()
    draw.text((10, 0), 'Ctx switch', fill='white', font=default)
    right_text(draw, width, 0, text=str(stats.ctx_switches), font=default)
    draw.text((10, 10), 'Intr', fill='white', font=default)
    right_text(draw, width, 10, text=str(stats.interrupts), font=default)
    draw.text((10, 20), 'Soft intr', fill='white', font=default)
    right_text(draw, width, 20, text=str(stats.soft_interrupts), font=default)
