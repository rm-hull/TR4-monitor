# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from datetime import datetime
from humanize import naturaldelta
import psutil

from common import right_text
from fonts import default


def render(draw, width, height):
    uptime = naturaldelta(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    draw.text((0, 0), 'Uptime', fill='white', font=default)
    right_text(draw, width, 0, text=uptime, font=default)
