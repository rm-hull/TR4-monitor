# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from humanize import naturalsize
import psutil

from common import right_text
from fonts import default


def interface(iface):

    def render(draw, width, height):
        stat = psutil.net_io_counters(pernic=True)[iface]
        draw.text((0, 0), f'{iface}', fill='white', font=default)
        right_text(draw, width, 0, text=f'{naturalsize(stat.bytes_sent, gnu=True)}B / {naturalsize(stat.bytes_recv, gnu=True)}B', font=default)

    return render
