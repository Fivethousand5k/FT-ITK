#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/3/26 11:47
    @Describe 
    @Version 1.0
"""
import numpy as np
from PyQt5.QtGui import QImage
import skimage.io
import skimage.transform
import skimage.color
import skimage



def array_preprocess(array, min, max,type="axial"):
    """
    preprocess the array with min and max value, for the points that CT slices could be processed as
    :param array: input grayscale 2-dimention array
    :param min: min_pixel_value, pixels with value less than it would be set to min
    :param max: max_pixel_value, pixels with value larger that it would be set to max
    :return: showImage:  QImage type, which could be later directly shown on a labelwidget through "self.label_screen.setPixmap(QPixmap(showImage))
    """
    assert type in ["axial", "sagittal",
                    "coronal"], "the type of slice viewer must be in [\"axial\",\"sagittal\",\"coronal\"]"
    array[array < min] = min
    array[array > max] = max
    array=((array-min)/(max-min)*255).astype(np.uint8)
    #array=np.flipud(array)
    array = skimage.color.gray2rgb(array)
    if type == "axial":
        pass
    elif type=="sagittal":
        pass
    elif type=="coronal":
        pass
    showImage = QImage(array, array.shape[1], array.shape[0],
                       QImage.Format_RGB888)  # 转换成QImage类型
    return showImage
