# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import psutil

bar_height = 5
cpu_count = psutil.cpu_count()


def render(draw, width, height):
    pct = psutil.cpu_percent(percpu=True)
    bar_width = width / 4 - 2
    bar_height = 5

    def draw_gauge(xy, percent):
        x, y = xy
        draw.rectangle([x, y, x + (bar_width * percent / 100), y + bar_height], fill='grey', width=1)
        draw.rectangle([x, y, x + bar_width, y + bar_height], outline='white', width=1)

    for i in range(0, cpu_count, 4):
        y_offset = i * (bar_height + 1)
        draw_gauge([0, y_offset], pct[i])
        draw_gauge([width * 0.25, y_offset], pct[i + 1])
        draw_gauge([width * 0.50, y_offset], pct[i + 2])
        draw_gauge([width * 0.75, y_offset], pct[i + 3])


height = int((bar_height + 1) * (cpu_count / 4))
