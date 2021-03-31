#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/3/29 13:27
    @Describe 
    @Version 1.0
"""
from PyQt5 import QtCore
from PyQt5.Qt import *
from Message_Boxes import Message_box,SCPU_Message_Box
class SCPU(QObject):           #Signal_Central_Process_Unit
    command_to_axial = QtCore.pyqtSignal(SCPU_Message_Box)
    command_to_sagittal = QtCore.pyqtSignal(SCPU_Message_Box)
    command_to_coronal = QtCore.pyqtSignal(SCPU_Message_Box)
    def __init__(self,parent=None):
        super(SCPU, self).__init__(parent)
#


    def Process_Core(self,message: Message_box):
        source=message.slice_viewer_type
        x,y=message.x,message.y
        slice_index=message.slice_index
        print(source)
        # if source=="axial":         #from axial viewer
        #     command_box_to_sagittal=SCPU_Message_Box(x=slice_index,y=y,slice_index=x)
        #     command_box_to_coronal=SCPU_Message_Box(x=slice_index,y=x,slice_index=y)
        #     self.command_to_sagittal.emit(command_box_to_sagittal)
        #     self.command_to_coronal.emit(command_box_to_coronal)
        # elif source=="sagittal":     #from sagittal viewer
        #     command_box_to_axial=SCPU_Message_Box(x=x,y=slice_index,slice_index=y)
        #     command_box_to_coronal=SCPU_Message_Box(x=y,y=slice_index,slice_index=x)
        #     self.command_to_axial.emit(command_box_to_axial)
        #     self.command_to_coronal.emit(command_box_to_coronal)
        #
        # elif source=="coronal":     #from coronal viewer
        #     command_box_to_axial = SCPU_Message_Box(x=x, y=slice_index, slice_index=y)
        #     command_box_to_sagittal = SCPU_Message_Box(x=slice_index, y=x, slice_index=x)
        #     self.command_to_axial.emit(command_box_to_axial)
        #     self.command_to_sagittal.emit(command_box_to_sagittal)

        if source=="axial":         #from axial viewer
            command_box_to_sagittal=SCPU_Message_Box(y=slice_index,x=y,slice_index=x)
            command_box_to_coronal=SCPU_Message_Box(y=slice_index,x=x,slice_index=y)
            self.command_to_sagittal.emit(command_box_to_sagittal)
            self.command_to_coronal.emit(command_box_to_coronal)
        elif source=="sagittal":     #from sagittal viewer
            command_box_to_axial=SCPU_Message_Box(y=x,x=slice_index,slice_index=y)
            command_box_to_coronal=SCPU_Message_Box(y=y,x=slice_index,slice_index=x)
            self.command_to_axial.emit(command_box_to_axial)
            self.command_to_coronal.emit(command_box_to_coronal)

        elif source=="coronal":     #from coronal viewer
            command_box_to_axial = SCPU_Message_Box(x=x, y=slice_index, slice_index=y)
            command_box_to_sagittal = SCPU_Message_Box(x=slice_index, y=y, slice_index=x)
            self.command_to_axial.emit(command_box_to_axial)
            self.command_to_sagittal.emit(command_box_to_sagittal)



