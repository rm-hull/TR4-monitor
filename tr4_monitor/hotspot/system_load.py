# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import os

from common import right_text
from fonts import proggy_tiny


def render(draw, width, height):
    av1, av2, av3 = os.getloadavg()
    draw.text((0, 0), 'Load:', fill='white', font=proggy_tiny)
    right_text(draw, width, 0, text=f'{av1:.1f}/{av2:.1f}/{av3:.1f}', font=proggy_tiny)
