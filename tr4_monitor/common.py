# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.


def center_text(draw, width, y, text, fill="white", font=None):
    x = (width - draw.textsize(text, font=font)[0]) / 2
    draw.text((x, y), text=text, font=font, fill=fill)


def right_text(draw, width, y, text, fill="white", font=None):
    x = width - draw.textsize(text, font=font)[0]
    draw.text((x, y), text=text, font=font, fill=fill)
