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
import os


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
def array_preprocess_with_label(array,label_array, min, max,type="axial",target_output_size=512):
    """
    preprocess the array with min and max value, for the points that CT slices could be processed as
    :param array: input grayscale 2-dimention array
    :param min: min_pixel_value, pixels with value less than it would be set to min
    :param max: max_pixel_value, pixels with value larger that it would be set to max
    :return: showImage:  QImage type, which could be later directly shown on a labelwidget through "self.label_screen.setPixmap(QPixmap(showImage))
    """
    assert type in ["axial", "sagittal",
                    "coronal"], "the type of slice viewer must be in [\"axial\",\"sagittal\",\"coronal\"]"
    array_copy=array.copy()
    array_copy[array_copy < min] = min
    array_copy[array_copy > max] = max
    array_copy=((array_copy-min)/(max-min)*255).astype(np.uint8)
    tmp_label_array=label_array.copy()
    tmp_label_array*=255
    #array=np.flipud(array)
    if type == "axial":
        pass
    elif type == "sagittal":
        print(array_copy.shape)
        ###########
        array_copy=flip90_left(array_copy)
        array_copy=np.flipud(array_copy)
        ###########
        tmp_label_array=flip90_left(tmp_label_array)
        tmp_label_array=np.flipud(tmp_label_array)
        ###########
        height,width=array_copy.shape
        up_index=target_output_size//2-height//2
        bottom_index=up_index+height
        tmp_array=np.ones((target_output_size,target_output_size), dtype=np.uint8)*20
        tmp_array[up_index:bottom_index,:]=array_copy
        tmp_tmp_label_array=np.ones((target_output_size,target_output_size), dtype=np.uint8)*20
        tmp_tmp_label_array[up_index:bottom_index,:]=tmp_label_array
        array_copy=tmp_array
        tmp_label_array=tmp_tmp_label_array

    elif type == "coronal":
        print(array_copy.shape)
        array_copy=flip90_left(array_copy)
        array_copy = np.flipud(array_copy)
        tmp_label_array=flip90_left(tmp_label_array)
        tmp_label_array=np.flipud(tmp_label_array)
        height,width=array_copy.shape
        up_index=target_output_size//2-height//2
        bottom_index=up_index+height
        tmp_array=np.ones((target_output_size,target_output_size), dtype=np.uint8)*20
        tmp_array[up_index:bottom_index,:]=array_copy
        tmp_tmp_label_array=np.ones((target_output_size,target_output_size), dtype=np.uint8)*20
        tmp_tmp_label_array[up_index:bottom_index,:]=tmp_label_array
        array_copy=tmp_array
        tmp_label_array=tmp_tmp_label_array

    array_copy = skimage.color.gray2rgb(array_copy)
    zero_slice=np.zeros(tmp_label_array.shape)
    zero_slice=zero_slice[:,:,np.newaxis]
    tmp_label_array=tmp_label_array[:,:,np.newaxis]
    tmp_label_array=np.concatenate((tmp_label_array,tmp_label_array,zero_slice),axis=2)
    array_copy[tmp_label_array!=0]=(array_copy[tmp_label_array!=0]*0+tmp_label_array[tmp_label_array!=0]*1).astype(np.uint8)
    showImage = QImage(array_copy.copy(), array_copy.shape[1], array_copy.shape[0],
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


## 得到2D/3D的医学图像(除.dcm序列图像)
def get_medical_image(path):
    import SimpleITK as sitk
    '''
    加载一幅2D/3D医学图像(除.dcm序列图像)，支持格式：.nii, .nrrd, ...
    :param path: 医学图像的路径/SimpleITK.SimpleITK.Image
    :return:(array,origin,spacing,direction)
    array:  图像数组
    origin: 三维图像坐标原点
    spacing: 三维图像坐标间距
    direction: 三维图像坐标方向
    image_type: 图像像素的类型
    注意：实际取出的数组不一定与MITK或其他可视化工具中的方向一致！
    可能会出现旋转\翻转等现象，这是由于dicom头文件中的origin,spacing,direction的信息导致的
    在使用时建议先用matplotlib.pyplot工具查看一下切片的方式是否异常，判断是否需要一定的预处理
    '''

    if isinstance(path, sitk.Image):
        reader = path
    else:
        assert os.path.exists(path), "{} is not existed".format(path)
        assert os.path.isfile(path), "{} is not a file".format(path)
        reader = sitk.ReadImage(path)

    array = sitk.GetArrayFromImage(reader)
    spacing = reader.GetSpacing()  ## 间隔
    origin = reader.GetOrigin()  ## 原点
    direction = reader.GetDirection()  ## 方向
    image_type = reader.GetPixelID()  ## 原图像每一个像素的类型，
    return array, origin, spacing, direction, image_type

