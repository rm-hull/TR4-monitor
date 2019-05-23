# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from datetime import datetime
import psutil
import miniupnpc

from filesize import naturalsize
from common import right_text
from fonts import default

last_invoked = None
prev = None
count = 0


def interface(iface):
    u = miniupnpc.UPnP()
    u.discoverdelay = 200
    u.discover()
    u.selectigd()

    local_ip_addr = u.lanaddr
    ext_ip_addr = u.externalipaddress()

    def render(draw, width, height):
        global count
        global last_invoked
        global prev

        stat = psutil.net_io_counters(pernic=True)[iface]

        if last_invoked:
            elapsed = (datetime.now() - last_invoked).total_seconds()
            upload_rate = (stat.bytes_sent - prev.bytes_sent) / elapsed
            download_rate = (stat.bytes_recv - prev.bytes_recv) / elapsed
        else:
            upload_rate = 0
            download_rate = 0

        ip_addr = ext_ip_addr if count % 10 < 5 else local_ip_addr

        draw.text((0, 0), f'Net: {iface}', fill="white", font=default)
        right_text(draw, width, 0, text=ip_addr, fill="white", font=default)

        draw.text((0, 10), f' Up:', fill='white', font=default)
        draw.text((36, 10), f'{naturalsize(upload_rate)}B/s', fill='white', font=default)
        right_text(draw, width, 10, text=f'{naturalsize(stat.bytes_sent)}B', fill='white', font=default)

        draw.text((0, 20), f' Down:', fill='white', font=default)
        draw.text((36, 20), f'{naturalsize(download_rate)}B/s', fill='white', font=default)
        right_text(draw, width, 20, text=f'{naturalsize(stat.bytes_recv)}B', fill='white', font=default)

        last_invoked = datetime.now()
        prev = stat
        count += 1

    return render
