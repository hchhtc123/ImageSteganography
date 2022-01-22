# -*- coding: utf-8 -*-
"""
    图像隐藏与提取算法
"""

from PIL import Image

class ImageSteganography(object):

    @staticmethod
    def __int_to_bin(rgb):
        """
            将整数元组转换为二进制（字符串）元组。
        """
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))

    @staticmethod
    def __bin_to_int(rgb):
        """
            将二进制（字符串）元组转换为整数元组。
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        """
            合并两个RGB元组
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb
    # 隐藏私密图片到图片中
    @staticmethod
    def merge(img1, img2):
        """
            将第二张图片隐藏到第一张图片中并返回隐藏后图片
        """
        # 要求要隐藏的图片大小需小于载体图片大小
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            return 0

        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = ImageSteganography.__int_to_bin(pixel_map1[i, j])
                rgb2 = ImageSteganography.__int_to_bin((0, 0, 0))
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = ImageSteganography.__int_to_bin(pixel_map2[i, j])

                rgb = ImageSteganography.__merge_rgb(rgb1, rgb2)
                pixels_new[i, j] = ImageSteganography.__bin_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        """
            提取隐藏在图片中的私密图片，返回私密图片
        """

        pixel_map = img.load()

        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b = ImageSteganography.__int_to_bin(pixel_map[i, j])
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                pixels_new[i, j] = ImageSteganography.__bin_to_int(rgb)
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
        return new_image
