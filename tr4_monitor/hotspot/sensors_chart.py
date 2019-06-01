# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from common import right_text
from fonts import default


def using(datalogger, temp_spec, fan_spec):
    def render(draw, width, height):
        snapshot = list(datalogger.entries)
        y_offset = 0
        height = 12

        for label, reading in temp_spec.items():
            max_temp = max(snapshot, key=lambda x: x['value'][reading])
            latest_temp = int(snapshot[-1]['value'][reading])

            draw.text((0, y_offset + 1), label, fill='white', font=default)
            right_text(draw, width / 2 + 8, y_offset + 1, text=f'{latest_temp}°C', font=default)

            for index, entry in enumerate(reversed(snapshot)):
                x_offset = width - index - 2
                y_value = int((height - 2) * entry['value'][reading] / max_temp['value'][reading])
                draw.line([x_offset, y_offset + height - 2, x_offset, y_offset + height - y_value], fill='grey', width=1)

            draw.rectangle([width - datalogger.max_entries - 2, y_offset, width - 2, y_offset + height - 2], outline='white', width=1)
            y_offset += height

        draw.text((0, y_offset + 1), 'Fans', fill='white', font=default) 
        for index, (label, reading) in enumerate(fan_spec.items()):
            latest_speed = int(snapshot[-1]['value'][reading])
            right_text(draw, 56 + (index * 24), y_offset + 1, text=f'{latest_speed}', font=default)

    return render