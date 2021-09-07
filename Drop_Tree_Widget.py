 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/5/8 14:43
    @Describe 
    @Version 1.0
"""
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow, QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget, QTreeView, QFileDialog, QWidget, QFileSystemModel, QAbstractItemView
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import sys

class Drop_Tree_Widget(QTreeView):
    """
    1)inherit QTreeWidget
    2)Users could drop a file onto the Widget and then the file would be read
    """
    file_text_signal = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(Drop_Tree_Widget, self).__init__(parent)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, e):
        # if e.mimeData().hasFormat('text/plain'):
        #     e.accept()
        # else:
        #     e.ignore()
        e.accept()

    def dropEvent(self, e):
        self.text = e.mimeData().text()
        self.text = self.text.replace("file:///", "")
        print(self.text)
        self.file_text_signal.emit(self.text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Drop_Tree_Widget()
    gui.show()
    sys.exit(app.exec_())


