# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from common import right_text
from fonts import default
from nice import nice_ticks


def get_temperature_scale(snapshot, temp_spec):
    readings = []
    for _, reading in temp_spec.items():
        readings += [x['value'].get(reading, 0) for x in snapshot]

    max_temp = max(readings, default=0)
    return nice_ticks(0, max_temp)


def using(datalogger, temp_spec, fan_spec):
    def render(draw, width, height):
        snapshot = list(datalogger.entries)
        y_offset = 0
        height = 12

        min_temp, max_temp, _ = get_temperature_scale(snapshot, temp_spec)

        for label, reading in temp_spec.items():
            latest_temp = snapshot[-1]['value'].get(reading)
            latest_temp = 'n/a' if latest_temp is None else f'{latest_temp:.0f}°C'

            draw.text((0, y_offset + 1), label, fill='white', font=default)
            right_text(draw, width / 2 + 8, y_offset + 1, text=latest_temp, font=default)

            for index, entry in enumerate(reversed(snapshot)):
                x_offset = width - index - 2
                y_value = int((height - 2) * entry['value'].get(reading, 0) / max_temp)
                draw.line([x_offset, y_offset + height - 2, x_offset, y_offset + height - y_value], fill='grey', width=1)

            draw.rectangle([width - datalogger.max_entries - 2, y_offset, width - 2, y_offset + height - 2], outline='white', width=1)
            y_offset += height

        draw.text((0, y_offset + 1), 'Fans', fill='white', font=default)
        for index, (label, reading) in enumerate(fan_spec.items()):
            latest_speed = int(snapshot[-1]['value'].get(reading, 0))
            right_text(draw, 56 + (index * 24), y_offset + 1, text=f'{latest_speed}', font=default)

    return render
