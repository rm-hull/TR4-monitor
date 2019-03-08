import time

from luma.core.render import canvas
from luma.emulator.device import pygame

device = pygame()

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "Hello World", fill="white")

time.sleep(5)