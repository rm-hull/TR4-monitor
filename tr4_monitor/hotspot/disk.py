# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from humanize import naturalsize
import psutil

from common import right_text
from fonts import proggy_tiny


def directory(dir):

    def render(draw, width, height):
        usage = psutil.disk_usage(dir)
        draw.text((0, 0), f'Disk:', fill='white', font=proggy_tiny)
        right_text(draw, width, 0, text=f'{naturalsize(usage.used, gnu=True)}B/{usage.percent}%', font=proggy_tiny)

    return render
