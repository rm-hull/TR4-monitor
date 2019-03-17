# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

import os

from PIL import ImageFont


def load_font(name, size):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), name))
    return ImageFont.truetype(font_path, size)


proggy_tiny = load_font('ProggyTiny.ttf', 16)
chicago = load_font('ChiKareGo.ttf', 16)
code2000 = load_font('code2000.ttf', 12)
pixelmix = load_font('pixelmix.ttf', 8)

default = pixelmix
fixed = proggy_tiny
