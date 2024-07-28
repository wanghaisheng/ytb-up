#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/2/12 11:20
@Author  : 余半盏
@Email   : 2466857975@@qq.com
@File    : rotate_captcha.py
@Software: PyCharm
"""
import os
import time

import cv2 as cv2
import math
import numpy as np

from tiktok_config import Verication_Tk_Dir


def circle_point_px(img, accuracy_angle, r=None):
    rows, cols, channel = img.shape
    assert 360 % accuracy_angle == 0
    x0, y0 = r0, _ = (rows // 2, cols // 2)
    if r: r0 = r
    circle_px_list = []
    for angle in np.arange(0, 360, accuracy_angle):
        # 圆上点 x=x0 + r*cosθ; y=y0 + r*sinθ
        x = x0 + r0 * math.cos(angle / 180 * math.pi)
        y = y0 + r0 * math.sin(angle / 180 * math.pi)
        circle_px_list.append(img[int(x)][int(y)])
    return circle_px_list


def rotate(image, angle, center=None, scale=1.0):  # 1
    (h, w) = image.shape[:2]  # 2
    if center is None:  # 3
        center = (w // 2, h // 2)  # 4

    M = cv2.getRotationMatrix2D(center, angle, scale)  # 5

    rotated = cv2.warpAffine(image, M, (w, h))  # 6
    return rotated


def HSVDistance(c1, c2):
    y1 = 0.299 * c1[0] + 0.587 * c1[1] + 0.114 * c1[2]
    u1 = -0.14713 * c1[0] - 0.28886 * c1[1] + 0.436 * c1[2]
    v1 = 0.615 * c1[0] - 0.51498 * c1[1] - 0.10001 * c1[2]
    y2 = 0.299 * c2[0] + 0.587 * c2[1] + 0.114 * c2[2]
    u2 = -0.14713 * c2[0] - 0.28886 * c2[1] + 0.436 * c2[2]
    v2 = 0.615 * c2[0] - 0.51498 * c2[1] - 0.10001 * c2[2]
    rlt = math.sqrt((y1 - y2) * (y1 - y2) + (u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2))
    return rlt


def circle_discern(inner_image_brg, outer_image_brg, result_img=None, angle=2, default_dis=5):
    inner_image_brg = cv2.imread(inner_image_brg)
    outer_image_brg = cv2.imread(outer_image_brg)
    inner_image = cv2.cvtColor(inner_image_brg, cv2.COLOR_BGR2HSV)
    outer_image = cv2.cvtColor(outer_image_brg, cv2.COLOR_BGR2HSV)
    all_deviation = []
    for result in range(0, 180):
        inner = rotate(inner_image, -result)  # 顺时针
        outer = rotate(outer_image, result)
        inner_circle_point_px = circle_point_px(inner, angle, (inner.shape[0] // 2) - default_dis)
        outer_circle_point_px = circle_point_px(outer, angle, (inner.shape[0] // 2) + default_dis)
        total_deviation = 0
        for i in range(len(inner_circle_point_px)):
            in_px = inner_circle_point_px[i]
            out_px = outer_circle_point_px[i]
            deviation = HSVDistance(in_px, out_px)
            total_deviation += deviation
        all_deviation.append(total_deviation)
    result = all_deviation.index(min(all_deviation))
    print(result)

    if result_img:
        inner = rotate(inner_image_brg, -result)  # 顺时针
        outer = rotate(outer_image_brg, result)
        left_point = outer.shape[0] / 2 - inner.shape[0] / 2
        right_point = outer.shape[0] / 2 + inner.shape[0] / 2
        replace_area = outer[int(left_point):int(right_point), int(left_point):int(right_point)]
        outer[int(left_point):int(right_point), int(left_point):int(right_point)] = replace_area + inner
        cv2.imwrite(result_img, outer)
    return result


def tk_circle_discern(inner_image, outer_image):
    def check_png(name):
        if not name.endswith('.png'):  # 确保有后缀名
            name = "%s.png" % name
        return name
    inner_image = check_png(inner_image)
    outer_image = check_png(outer_image) # 确保后缀名
    inner_png_dir = os.path.join(Verication_Tk_Dir, inner_image)
    outer_png_dir = os.path.join(Verication_Tk_Dir, outer_image) # 路径拼接
    res = circle_discern(inner_png_dir,outer_png_dir)   # 调用函数来识别
    return res