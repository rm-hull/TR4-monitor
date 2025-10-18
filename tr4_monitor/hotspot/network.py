# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import math
import miniupnpc
from itertools import tee

from filesize import naturalsize
from common import right_text
from fonts import default


count = 0
height = 62


def arrow(draw, xy, fill, direction, size=8):
    size_12 = size / 2.0
    size_14 = math.ceil(size / 4.0)
    size_34 = math.floor(size * 3.0 / 4.0)

    x, y = xy

    if direction == "up":
        shape = [
            (x + size_12, y),
            (x + size, y + size_12),
            (x + size_34, y + size_12),
            (x + size_34, y + size),
            (x + size_14, y + size),
            (x + size_14, y + size_12),
            (x, y + size_12),
        ]
    else:
        shape = [
            (x + size_12, y + size),
            (x + size, y + size_12),
            (x + size_34, y + size_12),
            (x + size_34, y),
            (x + size_14, y),
            (x + size_14, y + size_12),
            (x, y + size_12),
        ]

    draw.polygon(shape, fill=fill)


def window(iterable, size):
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    return zip(*iters)


def chart(draw, xy, height, width, data):
    max_value = 0 if len(data) == 0 else max(data)
    x, y = xy

    if max_value > 0:
        for index, value in enumerate(reversed(data)):
            x_offset = x + width - index
            y_value = math.floor(height * value / max_value)
            draw.line(
                [x_offset, y + height, x_offset, y + height - y_value],
                fill="grey",
                width=1,
            )

    draw.rectangle([x, y, x + width, y + height], outline="white", width=1)


def using(iface, datalogger):
    u = miniupnpc.UPnP()
    u.discoverdelay = 200
    u.discover()
    try:
        u.selectigd()
        ext_ip_addr = u.externalipaddress()
    except Exception:
        ext_ip_addr = None

    local_ip_addr = u.lanaddr

    def render(draw, width, height):
        global count

        snapshot = list(datalogger.entries)
        stat = snapshot[-1]["value"]
        last_invoked = snapshot[-1]["timestamp"]

        if len(snapshot) > 1:
            prev_stat = snapshot[-2]["value"]
            prev_invoked = snapshot[-2]["timestamp"]
            elapsed = (last_invoked - prev_invoked).total_seconds()
            upload_rate = (stat.bytes_sent - prev_stat.bytes_sent) / elapsed
            download_rate = (stat.bytes_recv - prev_stat.bytes_recv) / elapsed
        else:
            upload_rate = 0
            download_rate = 0

        ip_addr = ext_ip_addr if ext_ip_addr and count % 10 < 5 else local_ip_addr

        draw.text((0, 0), f"Net: {iface}", fill="white", font=default)
        right_text(draw, width, 0, text=ip_addr, fill="white", font=default)

        draw.text((5, 10), "Up:", fill="white", font=default)
        right_text(
            draw,
            width - 44,
            10,
            text=f"{naturalsize(upload_rate)}B/s",
            fill="white",
            font=default,
        )
        right_text(
            draw,
            width,
            10,
            text=f"{naturalsize(stat.bytes_sent)}B",
            fill="white",
            font=default,
        )

        draw.text((0, 20), " Down:", fill="white", font=default)
        right_text(
            draw,
            width - 44,
            20,
            text=f"{naturalsize(download_rate)}B/s",
            fill="white",
            font=default,
        )
        right_text(
            draw,
            width,
            20,
            text=f"{naturalsize(stat.bytes_recv)}B",
            fill="white",
            font=default,
        )

        pairs = list(window(snapshot, size=2))
        bytes_sent = [
            second["value"].bytes_sent - first["value"].bytes_sent
            for first, second in pairs
        ]
        bytes_recv = [
            second["value"].bytes_recv - first["value"].bytes_recv
            for first, second in pairs
        ]

        arrow(draw, (5, 33), fill="white", direction="up", size=6)
        chart(draw, (13, 30), height=12, width=datalogger.max_entries, data=bytes_sent)
        arrow(draw, (width / 2 + 5, 33), fill="white", direction="down", size=6)
        chart(
            draw,
            ((width / 2) + 13, 30),
            height=12,
            width=datalogger.max_entries,
            data=bytes_recv,
        )

        count += 1

    return render
