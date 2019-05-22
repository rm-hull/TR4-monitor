# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

height = 16


def using(datalogger):    
    def render(draw, width, height):
        snapshot = list(datalogger.entries)
        max_1min_avg = max(snapshot, key=lambda x: x['value'][0])

        for index, entry in enumerate(reversed(snapshot)):
            x_offset = width - index - 2
            y_value = int((height - 2) * entry['value'][0] / max_1min_avg['value'][0])
            draw.line([x_offset, height - 1, x_offset, height - y_value], fill='grey', width=1)
            
        draw.rectangle([width - datalogger.max_entries - 2, 0, width - 2, height - 1], outline='white', width=1)
       
    return render
