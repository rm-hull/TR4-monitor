# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from datetime import datetime
import psutil

from common import right_text
from fonts import proggy_tiny


def render(draw, width, height):
    uptime = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0].replace(' days', 'd')
    draw.text((0, 0), 'Uptime:', fill='white', font=proggy_tiny)
    right_text(draw, width, 0, text=uptime, font=proggy_tiny)
