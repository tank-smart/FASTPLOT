# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：绘图窗口类
#
# =======使用说明
# 
#
# =======日志
# 

# =============================================================================

import sys
sys.path.append(r"E:\DAGUI\lib")
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtWidgets import (QWidget, QToolButton, QSpacerItem, QFrame, 
                             QVBoxLayout, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtGui import QIcon

# =============================================================================
# Package views imports
# =============================================================================
from models.figure_model import PlotCanvas
from slider import Slider

# =============================================================================
# PlotWindow
# =============================================================================
class PlotWindow(QWidget):

# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):
        
        self.setObjectName("PlotWindow")
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#        创建画布部件
        self.plotcanvas = PlotCanvas(self)
        self.plotcanvas.setObjectName("plotcanvas")
        self.horizontalLayout_2.addWidget(self.plotcanvas)
#        创建右侧的工具栏
        self.widget_plot_tools = QWidget(self)
        self.widget_plot_tools.setMinimumSize(QSize(32, 0))
        self.widget_plot_tools.setMaximumSize(QSize(32, 16777215))
        self.widget_plot_tools.setObjectName("widget_plot_tools")
        self.verticalLayout = QVBoxLayout(self.widget_plot_tools)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
#        创建放大缩小按钮并加入工具栏
        self.button_zoom_out = QToolButton(self.widget_plot_tools)
        self.button_zoom_out.setMinimumSize(QSize(32, 32))
        self.button_zoom_out.setMaximumSize(QSize(32, 32))
        self.button_zoom_out.setObjectName("button_zoom_out")
        self.button_zoom_out.setIcon(QIcon(r"E:\DAGUI\lib\icon\zoom_out.ico"))
        self.verticalLayout.addWidget(self.button_zoom_out)
        self.button_zoom_in = QToolButton(self.widget_plot_tools)
        self.button_zoom_in.setMinimumSize(QSize(32, 32))
        self.button_zoom_in.setMaximumSize(QSize(32, 32))
        self.button_zoom_in.setObjectName("button_zoom_in")
        self.verticalLayout.addWidget(self.button_zoom_in)
        self.button_zoom_in.setIcon(QIcon(r"E:\DAGUI\lib\icon\zoom_in.ico"))
        spacerItem = QSpacerItem(20, 219, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.widget_plot_tools)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
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
        self.slider.setMinimumSize(QSize(0, 24))
        self.slider.setMaximumSize(QSize(16777215, 24))
        self.slider.setFrameShape(QFrame.StyledPanel)
        self.slider.setFrameShadow(QFrame.Raised)
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)
        self.button_move_right = QToolButton(self)
        self.button_move_right.setMinimumSize(QSize(24, 24))
        self.button_move_right.setMaximumSize(QSize(24, 24))
        self.button_move_right.setObjectName("button_move_right")
        self.button_move_right.setIcon(QIcon(r"E:\DAGUI\lib\icon\move_right.ico"))
        self.horizontalLayout.addWidget(self.button_move_right)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi()
# =======连接信号与槽
# =============================================================================
        self.button_move_left.triggered.connect()
        self.button_move_right.triggered.connect()
        self.button_zoom_in.triggered.connect()
        self.button_zoom_out.triggered.connect()
# =======slot函数   
# =============================================================================
    def slot_home(self):
        self.toolbar.home()
        
    def slot_pan(self):
        self.toolbar.pan()
        
    def slot_zoom(self):
        self.toolbar.zoom()
        
    def slot_config_subplots(self):
        self.toolbar.configure_subplots()
        
    def slot_save(self):
        self.toolbar.save_figure()
        
    def slot_back(self):
        self.toolbar.back()
        
    def slot_forward(self):
        self.toolbar.forward()
        
    def slot_edit(self):
        self.toolbar.edit_parameters()
# =============================================================================
     
# =============================================================================
# 功能函数模块
# =============================================================================
    def plot(self, filegroup):
        
        if filegroup:
            for file in filegroup:
                self.plotcanvas.plot_para(file, filegroup[file])
            self.toolbar=self.plotcanvas.add_toolbar(self.plotcanvas)
            self.plotcanvas.hide_toolbar(self.toolbar)
            
    
    
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("PlotWindow", "Plot"))
        self.button_zoom_out.setText(_translate("PlotWindow", "..."))
        self.button_zoom_in.setText(_translate("PlotWindow", "..."))
        self.button_move_left.setText(_translate("PlotWindow", "..."))
        self.button_move_right.setText(_translate("PlotWindow", "..."))