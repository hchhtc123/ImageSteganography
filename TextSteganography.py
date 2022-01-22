# -*- coding: utf-8 -*-

"""
    文本信息隐藏及提取算法
"""

from __future__ import absolute_import, unicode_literals

import sys
from PIL import Image
import random
import binascii

DIST = 8

def normalize_pixel(r, g, b):
    if is_modify_pixel(r, g, b):
        seed = random.randint(1, 3)
        if seed == 1:
            r = _normalize(r)
        if seed == 2:
            g = _normalize(g)
        if seed == 3:
            b = _normalize(b)
    return r, g, b

def modify_pixel(r, g, b):
    return map(_modify, [r, g, b])

def is_modify_pixel(r, g, b):
    return r % DIST == g % DIST == b % DIST == 1

def _modify(i):
    if i >= 128:
        for x in range(DIST + 1):
            if i % DIST == 1:
                return i
            i -= 1
    else:
        for x in range(DIST + 1):
            if i % DIST == 1:
                return i
            i += 1
    raise ValueError

def _normalize(i):
    if i >= 128:
        i -= 1
    else:
        i += 1
    return i

def normalize(path, output):
    img = Image.open(path)
    img = img.convert('RGB')
    size = img.size
    new_img = Image.new('RGB', size)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            _r, _g, _b = normalize_pixel(r, g, b)
            new_img.putpixel((x, y), (_r, _g, _b))
    new_img.save(output, "PNG", optimize=True)


def hide_text(path, text):
    text = str(text)

    write_param = []
    _base = 0
    for _ in to_hex(text):
        write_param.append(int(_, 16) + _base)
        _base += 16

    img = Image.open(path)
    counter = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if counter in write_param:
                r, g, b = img.getpixel((x, y))
                r, g, b = modify_pixel(r, g, b)
                img.putpixel((x, y), (r, g, b))
            counter += 1
    img.save(path, "PNG", optimize=True)

def to_hex(s):
    return binascii.hexlify(s.encode()).decode()

def to_str(s):
    if (len(s)%2) == 1:
        return 0
    else:
        return binascii.unhexlify(s).decode()

def read_text(path):
    img = Image.open(path)
    counter = 0
    result = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            if is_modify_pixel(r, g, b):
                result.append(counter)
            counter += 1
            if counter == 16:
                counter = 0
    return to_str(''.join([hex(_)[-1:] for _ in result]))

class TextSteganography(object):
    # 在图片中隐藏文本信息
    @classmethod
    def encode(cls, input_image_path, output_image_path, encode_text):
        """
            隐藏私密信息到载体图片中
        """
        normalize(input_image_path, output_image_path)
        hide_text(output_image_path, encode_text)
        assert read_text(output_image_path) == encode_text, read_text(output_image_path)

    @classmethod
    def decode(cls, image_path):
        """
            提取隐藏在图片中的文本信息
        """
        return read_text(image_path)