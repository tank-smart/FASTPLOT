# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：自定义绘图窗口中的滑块
#
# =======使用说明
# 
#
# =======日志
# 

# =============================================================================

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPaintEvent, QMouseEvent, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

# =============================================================================
# Slider
# =============================================================================
class Slider(QFrame):

    MARIGIN = 2
# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.mouse_press = False
        
        self.frame_width = 0
        self.frame_height = self.height()
        self.slider_top = self.MARIGIN
        self.slider_left = self.MARIGIN
        self.slider_width = 300 - self.MARIGIN
        self.slider_height = self.frame_height - 2 * self.MARIGIN

# =============================================================================
# 自定义UI   
# =============================================================================
#    重载函数
    def paintEvent(self, event : QPaintEvent):
        
        painter = QPainter(self)
        self.frame_width = self.width()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(210, 210, 210)))
        painter.drawRect(0, 0, self.frame_width, self.frame_height)
        painter.setPen(QColor(195, 195, 195))
        painter.setBrush(QBrush(QColor(175, 175, 175)))
        painter.drawRect(self.slider_left, self.slider_top, 
                         self.slider_width,
                         self.slider_height)

# =============================================================================
# slots函数        
# =============================================================================
    def mouseMoveEvent(self, event : QMouseEvent):
        
        self.setMouseTracking(True)
        pos = self.pos_cursor_in_margin(event.pos())
        
        if pos != 0:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
            
        if self.mouse_press:
            if pos == -1:
                self.setCursor(Qt.SizeHorCursor)
                length = self.slider_left + self.slider_width
                self.slider_left = event.x()
                self.slider_width = length - self.slider_left
                self.update()
            elif pos == 1:
                self.setCursor(Qt.SizeHorCursor)
                self.slider_width = event.x() - self.slider_left
                self.update()
    
    def mousePressEvent(self, event : QMouseEvent):
        
        self.mouse_press = True
        
    def mouseReleaseEven(self, event : QMouseEvent):
        
        self.mouse_press = False
            
    
# =============================================================================
# 功能函数    
# =============================================================================
#    判断鼠标是否在边界上
    def pos_cursor_in_margin(self, pos):
        
        x = pos.x()
        left_l = self.slider_left - self.MARIGIN
        left_r = self.slider_left + self.MARIGIN
        right_l = self.slider_left + self.slider_width - self.MARIGIN
        right_r = self.slider_left + self.slider_width + self.MARIGIN
#        如果在左边界
        if (left_l <= x and x <= left_r):
            return -1
#        如果在右边界
        elif (right_l <= x and x <= right_r):
            return 1
#        如果不在边界上
        else:
            return 0
    
    
    
    
    
    