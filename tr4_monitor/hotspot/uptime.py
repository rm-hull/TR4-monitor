# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from datetime import datetime
from humanize import naturaldelta
import psutil

from common import right_text
from fonts import default

height = 20


def render(draw, width, height):
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = naturaldelta(datetime.now() - boot_time)
    draw.text((0, 0), 'Uptime', fill='white', font=default)
    right_text(draw, width, 0, text=uptime, font=default)
    draw.text((0, 10), 'Booted', fill='white', font=default)
    right_text(draw, width, 10, text=boot_time.strftime("%Y/%m/%d %H:%M"), font=default)
