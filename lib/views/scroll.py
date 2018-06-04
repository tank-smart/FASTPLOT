# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：自定义绘图窗口中的滚动条类
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
from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QToolButton
from PyQt5.QtGui import (QPaintEvent, QMouseEvent, QPainter, QBrush,
                         QColor, QIcon)
from PyQt5.QtCore import Qt, QPoint, QSize

# =============================================================================
# Slider
# =============================================================================
class Slider(QFrame):

    MARGIN = 2
# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.setMouseTracking(True)
        self.mouse_press_in_left_margin = False
        self.mouse_press_in_right_margin = False
        self.mouse_press_in_slider = False
#        记住当鼠标按住滑块时，滑块左侧的位置
        self.slider_left_press_in_slider = 0
#        记住鼠标按住滑块时的位置
        self.mouse_pos_press_in_slider = QPoint(0, 0)
        
#        绘图涉及到的特征量
        self.frame_width = 0
        self.frame_height = 0
        self.slider_top = self.MARGIN
        self.slider_left = 0
        self.slider_width = 0
        self.slider_height = 0
        self.slider_width_limit = 0
        
#        三个用百分比表示的区域，滑块前、中、后区域，三者之和定为100
        self.per_forward_length = 0
        self.per_slider_length = 0
        self.per_back_length = 0

# =============================================================================
# 自定义UI   
# =============================================================================
#    重载函数
    def paintEvent(self, event : QPaintEvent):
        
        painter = QPainter(self)

        pos = self.pos_cursor(self.mapFromGlobal(self.cursor().pos()))
#        当鼠标在边界上时改变鼠标显示，一种是仅鼠标移动时（仅有这种时，
#        鼠标快速移动pos将会是0或2，而不是-1或1），一种是鼠标按压时
        if ((pos == -1 or pos == 1) or self.mouse_press_in_left_margin or
            self.mouse_press_in_right_margin):
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        
        self.frame_width = self.width()
        self.frame_height = self.height()
        self.slider_left = self.frame_width * self.per_forward_length / 100
        self.slider_width = self.frame_width * self.per_slider_length / 100
        self.slider_height = self.frame_height - 2 * self.MARGIN
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(210, 210, 210)))
        painter.drawRect(0, 0, self.frame_width, self.frame_height)
#        按住滑块时，滑块灰度改变
        if self.mouse_press_in_slider:
            painter.setBrush(QBrush(QColor(150, 150, 150)))
        else:
            painter.setBrush(QBrush(QColor(175, 175, 175)))
        painter.drawRect(self.slider_left, self.slider_top, 
                         self.slider_width,
                         self.slider_height)

# =============================================================================
# slots函数        
# =============================================================================
    def mouseMoveEvent(self, event : QMouseEvent):

        self.slider_width_limit = int(0.01 * self.width())
        if self.mouse_press_in_left_margin:
            length = self.slider_left + self.slider_width
            width = length - event.x()
            if (width < self.slider_width_limit):
                self.slider_left = length - self.slider_width_limit
                self.slider_width = self.slider_width_limit
            else:
                if (event.x() < 0):
                    self.slider_left = 0
                else:
                    self.slider_left = event.x()
                self.slider_width = length - self.slider_left
            self.update_per_length()
            self.update()
        elif self.mouse_press_in_right_margin:
            width = event.x() - self.slider_left
            if (width < self.slider_width_limit):
                self.slider_width = self.slider_width_limit
            else:
                if (event.x() < self.width()):
                    self.slider_width = event.x() - self.slider_left
                else:
                    self.slider_width = self.width()- self.slider_left
            self.update_per_length()
            self.update()
        elif self.mouse_press_in_slider:
            left = self.slider_left_press_in_slider + (event.x() -
                                    self.mouse_pos_press_in_slider.x())
            if (left < 0):
                self.slider_left = 0
            elif ((left + self.slider_width) > self.width()):
                self.slider_left = self.width() - self.slider_width
            else:
                self.slider_left = left
            self.update_per_length()
            self.update()
        else:
            self.update()
    
    def mousePressEvent(self, event : QMouseEvent):
        
#        鼠标按下时，将鼠标在哪里按下记住
        pos = self.pos_cursor(event.pos())
        if pos == -1:
            self.mouse_press_in_left_margin = True
        if pos == 1:
            self.mouse_press_in_right_margin = True
        if pos == 0:
            self.mouse_press_in_slider = True
            self.slider_left_press_in_slider = self.slider_left
#            记住鼠标按下时的位置
            self.mouse_pos_press_in_slider = event.pos()
#            当鼠标按住滑块是滑块应改变灰度
            self.update()
        
    def mouseReleaseEvent(self, event : QMouseEvent):
        
#        鼠标释放时，重置所有状态
        self.mouse_press_in_left_margin = False
        self.mouse_press_in_right_margin = False
        self.mouse_press_in_slider = False
        self.mouse_pos_press_in_slider = QPoint(0, 0)
            
    
# =============================================================================
# 功能函数    
# =============================================================================
#    判断鼠标是否在边界上
    def pos_cursor(self, pos):
        
        x = pos.x()
        left_l = self.slider_left - self.MARGIN
        left_r = self.slider_left + self.MARGIN
        right_l = self.slider_left + self.slider_width - self.MARGIN
        right_r = self.slider_left + self.slider_width + self.MARGIN
#        如果在左边界
        if (left_l <= x and x <= left_r):
            return -1
#        如果在右边界
        elif (right_l <= x and x <= right_r):
            return 1
#        如果在中间上
        elif (left_r <= x and x <= right_l):
            return 0
#        如果不在滑块在空白处
        else:
            return 2

#    设置滑块长度和位置
    def set_slider(self, forward_len, slider_len):
        if ((forward_len + slider_len) <= 100):
            self.per_forward_length = forward_len
            self.per_slider_length = slider_len
            self.per_back_length = 100 - self.per_forward_length - self.per_slider_length
            self.update()

    def update_per_length(self):
        self.per_forward_length = round(float(self.slider_left) / self.frame_width, 2) * 100
        self.per_slider_length = round(float(self.slider_width) / self.frame_width, 2) * 100
        self.per_back_length = 100 - self.per_forward_length - self.per_slider_length
        
# =============================================================================
# Scroll  
# =============================================================================
class Scroll(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setup()
        
    def setup(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_move_left = QToolButton(self)
        self.button_move_left.setMinimumSize(QSize(24, 24))
        self.button_move_left.setMaximumSize(QSize(24, 24))
        self.button_move_left.setObjectName("button_move_left")
        self.button_move_left.setIcon(QIcon(r"E:\DAGUI\lib\icon\move_left.ico"))
        self.horizontalLayout.addWidget(self.button_move_left)
#        创建自定义的滑块部件
        self.slider = Slider(self)
        self.slider.setMinimumSize(QSize(0, 22))
        self.slider.setMaximumSize(QSize(16777215, 22))
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)
        self.button_move_right = QToolButton(self)
        self.button_move_right.setMinimumSize(QSize(24, 24))
        self.button_move_right.setMaximumSize(QSize(24, 24))
        self.button_move_right.setObjectName("button_move_right")
        self.button_move_right.setIcon(QIcon(r"E:\DAGUI\lib\icon\move_right.ico"))
        self.horizontalLayout.addWidget(self.button_move_right)








 
    