# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull
# See LICENSE.rst for details.

from dataclasses import dataclass
from itertools import groupby
from bs4 import BeautifulSoup
import requests
from luma.core import legacy

# from common import right_text
from fonts import default


CUSTOM_BITMAP_FONT = [
    [0x08, 0x24, 0x12, 0xD2, 0xD2, 0x12, 0x24, 0x08],  # WIFI icon
    [0xC0, 0xF0, 0xD6, 0x1E, 0xD6, 0xF0, 0xC0, 0x00],  # Ethernet icon
]


@dataclass
class Device:
    name: str
    network: str
    macAddress: str
    ipAddress: str


def extract_device_from(row, network):
    cells = [cell.text for cell in row.find_all("td")]
    device = Device(
        network=network if cells[0] == "\xa0" else cells[0][:-1],
        name=cells[1],
        macAddress=cells[2],
        ipAddress=cells[3],
    )
    return None if device.name == "No devices detected" else device


def get_devices(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find(
        string="Devices currently connected to your Plusnet Hub:"
    ).find_parent("table")
    devices = []
    device = None
    for row in table.find_all("tr")[2:]:
        device = extract_device_from(row, network=device.network if device else None)
        if device:
            devices.append(device)

    return devices


def init(url):

    def render(draw, width, height):

        by_name = lambda device: device.name.lower()
        devices = sorted(get_devices(url), key=by_name)
        print(devices)

        y_offset = 0
        for index, group in groupby(devices, key=by_name):
            group = sorted(group, key=lambda device: device.ipAddress)
            draw.text((1, y_offset), text=group[0].name, fill="white", font=default)
            y_offset += 11
            for device in group:
                draw.text(
                    (10, y_offset), text=device.ipAddress, fill="white", font=default
                )
                legacy.text(
                    draw,
                    (width - 8, y_offset),
                    "\1" if device.network == "Ethernet" else "\0",
                    fill="white",
                    font=CUSTOM_BITMAP_FONT,
                )
                y_offset += 11

            draw.line((0, y_offset, width, y_offset), fill="grey")
            y_offset += 2

    return render
