#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/3/29 13:27
    @Describe 
    @Version 1.0
"""
from PyQt5 import QtCore

from Message_Boxes import Message_box,SCPU_Message_Box
class SCPU():           #Signal_Central_Process_Unit
    def __init__(self):
        self.init_Signal_Channels()

    def init_Signal_Channels(self):
        self.command_to_axial=QtCore.pyqtSignal(SCPU_Message_Box)
        self.command_to_sagittal=QtCore.pyqtSignal(SCPU_Message_Box)
        self.command_to_coronal=QtCore.pyqtSignal(SCPU_Message_Box)


    def Process_Core(self,message: Message_box):
        source=message.Slice_Viewer_Widget_type
        x,y=message.mouse_x,message.mouse_y
        if source=="axial":         #from axial viewer
            self.command_to_sagittal.emit()
            self.command_to_coronal.emit()
        elif source=="sagittal":     #from sagittal viewer
            self.command_to_axial.emit()
            self.command_to_coronal.emit()
        elif source=="coronal":     #from coronal viewer
            self.command_to_axial.emit()
            self.command_to_sagittal.emit()


