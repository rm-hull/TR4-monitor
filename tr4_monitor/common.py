# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.


def center_text(draw, width, y, text, fill="white", font=None):
    x = (width - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text=text, font=font, fill=fill)


def right_text(draw, width, y, text, fill="white", font=None):
    x = width - draw.textlength(text, font=font)
    draw.text((x, y), text=text, font=font, fill=fill)
