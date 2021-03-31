#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/3/30 13:55
    @Describe 
    @Version 1.0
"""
class SCPU_Message_Box():
    def __init__(self,x,y,slice_index):
        self.x=x
        self.y=y
        self.slice_index=slice_index

class Message_box():
    def __init__(self,type,mouse_x,mouse_y,slice_index):
        self.slice_viewer_type=type
        self.x=mouse_x
        self.y=mouse_y
        self.slice_index=slice_index