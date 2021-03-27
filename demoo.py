#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/3/27 20:02
    @Describe 
    @Version 1.0
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Widget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)

        painter.drawLine(10, 10, 100, 140)

        painter.setPen(Qt.blue)
        painter.drawRect(120, 10, 80, 80)

        rectf = QRectF(230.0, 10.0, 80.0, 80.0)
        painter.drawRoundedRect(rectf, 20, 20)

        p1 = [QPoint(10, 100), QPoint(220, 110), QPoint(220, 190)]
        painter.drawPolyline(QPolygon(p1))

        p2 = [QPoint(120, 110), QPoint(220, 110), QPoint(220, 190)]
        painter.drawPolygon(QPolygon(p2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.resize(400, 280)
    ex.show()
    sys.exit(app.exec_())