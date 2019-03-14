# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import miniupnpc

from common import right_text
from fonts import proggy_tiny


def discover():
    u = miniupnpc.UPnP()
    u.discoverdelay = 200
    u.discover()
    u.selectigd()

    local_ip_addr = u.lanaddr
    ext_ip_addr = u.externalipaddress()

    def render(draw, width, height):
        draw.text((0, 0), f'IP:', fill='white', font=proggy_tiny)
        right_text(draw, width, 0, text=local_ip_addr, font=proggy_tiny)
        right_text(draw, width, 12, text=ext_ip_addr, font=proggy_tiny)

    return render

