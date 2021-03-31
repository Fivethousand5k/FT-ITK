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



def array_preprocess(array, min, max,type="axial",target_output_size=512):
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
    if type == "axial":
        pass
    elif type == "sagittal":
        print(array.shape)
        array=flip90_left(array)
        array=np.flipud(array)
        height,width=array.shape
        up_index=target_output_size//2-height//2
        bottom_index=up_index+height
        tmp_array=np.ones((target_output_size,target_output_size), dtype=np.uint8)*20
        tmp_array[up_index:bottom_index,:]=array
        array=tmp_array

    elif type == "coronal":
        print(array.shape)
        array=flip90_left(array)
        array = np.flipud(array)
        height,width=array.shape
        up_index=target_output_size//2-height//2
        bottom_index=up_index+height
        tmp_array=np.ones((target_output_size,target_output_size), dtype=np.uint8)*20
        tmp_array[up_index:bottom_index,:]=array
        array=tmp_array

    array = skimage.color.gray2rgb(array)
    showImage = QImage(array.copy(), array.shape[1], array.shape[0],
                       QImage.Format_RGB888)  # 转换成QImage类型
    return showImage



def flip180(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    return new_arr

def flip90_left(arr):
    arr = arr.T
    arr = arr[::-1]
    return arr

def flip90_right(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    new_arr = np.transpose(new_arr)[::-1]
    return new_arr

def place_on_center(background_array,array):
    """
    place the array onto the central part of background array
    :param background_array:
    :param array:
    :return:
    """
    bg_height,bg_width=background_array.shape
    height,width=array.shape


