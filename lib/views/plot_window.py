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
                             QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QFileDialog)
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
#        该窗口的主布局器，水平
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")        
#        子布局器，垂直，布局画布，水平子布局器
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
#        创建画布部件
        self.plotcanvas = PlotCanvas(self)
        self.plotcanvas.setObjectName("plotcanvas")
        self.verticalLayout_2.addWidget(self.plotcanvas)
#        子布局器，布局左移/右移按钮和滑块
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
        self.slider.setMinimumSize(QSize(0, 22))
        self.slider.setMaximumSize(QSize(16777215, 22))
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
#        创建右侧的工具栏
        self.widget_plot_tools = QWidget(self)
        self.widget_plot_tools.setMinimumSize(QSize(32, 0))
        self.widget_plot_tools.setMaximumSize(QSize(32, 16777215))
        self.widget_plot_tools.setObjectName("widget_plot_tools")
#        子布局器，垂直，布局工具按钮
        self.verticalLayout = QVBoxLayout(self.widget_plot_tools)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
#        创建放大缩小按钮并加入工具栏
#        self.button_home = QToolButton(self.widget_plot_tools)
#        self.button_home.setMinimumSize(QSize(32, 32))
#        self.button_home.setMaximumSize(QSize(32, 32))
#        self.button_home.setObjectName("button_home")
#        self.button_home.setIcon(QIcon(r"E:\DAGUI\lib\icon\home.ico"))
#        self.verticalLayout.addWidget(self.button_home)
#        self.button_pan = QToolButton(self.widget_plot_tools)
#        self.button_pan.setMinimumSize(QSize(32, 32))
#        self.button_pan.setMaximumSize(QSize(32, 32))
#        self.button_pan.setObjectName("button_pan")
#        self.button_pan.setIcon(QIcon(r"E:\DAGUI\lib\icon\pan.ico"))
#        self.verticalLayout.addWidget(self.button_pan)
        self.button_zoom = QToolButton(self.widget_plot_tools)
        self.button_zoom.setMinimumSize(QSize(32, 32))
        self.button_zoom.setMaximumSize(QSize(32, 32))
        self.button_zoom.setObjectName("button_zoom")
        self.button_zoom.setIcon(QIcon(r"E:\DAGUI\lib\icon\zoom.ico"))
        self.verticalLayout.addWidget(self.button_zoom)
        self.button_edit = QToolButton(self.widget_plot_tools)
        self.button_edit.setMinimumSize(QSize(32, 32))
        self.button_edit.setMaximumSize(QSize(32, 32))
        self.button_edit.setObjectName("button_edit")
        self.button_edit.setIcon(QIcon(r"E:\DAGUI\lib\icon\edit.ico"))
        self.verticalLayout.addWidget(self.button_edit)
#        self.button_back = QToolButton(self.widget_plot_tools)
#        self.button_back.setMinimumSize(QSize(32, 32))
#        self.button_back.setMaximumSize(QSize(32, 32))
#        self.button_back.setObjectName("button_back")
#        self.button_back.setIcon(QIcon(r"E:\DAGUI\lib\icon\back.ico"))
#        self.verticalLayout.addWidget(self.button_back)
#        self.button_forward = QToolButton(self.widget_plot_tools)
#        self.button_forward.setMinimumSize(QSize(32, 32))
#        self.button_forward.setMaximumSize(QSize(32, 32))
#        self.button_forward.setObjectName("button_forward")
#        self.button_forward.setIcon(QIcon(r"E:\DAGUI\lib\icon\forward.ico"))
#        self.verticalLayout.addWidget(self.button_forward)    
        self.button_save = QToolButton(self.widget_plot_tools)
        self.button_save.setMinimumSize(QSize(32, 32))
        self.button_save.setMaximumSize(QSize(32, 32))
        self.button_save.setObjectName("button_save")
        self.button_save.setIcon(QIcon(r"E:\DAGUI\lib\icon\save.ico"))
        self.verticalLayout.addWidget(self.button_save)        
        spacerItem = QSpacerItem(20, 219, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
#        先添加工具栏在添加包括画布/滑块的水平子布局器
        self.horizontalLayout_2.addWidget(self.widget_plot_tools)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi()
# =======连接信号与槽
# =============================================================================
#        self.button_move_left.triggered.connect()
#        self.button_move_right.triggered.connect()
#        self.button_home.clicked.connect(self.slot_home)
#        self.button_pan.clicked.connect(self.slot_pan)
        self.button_zoom.clicked.connect(self.slot_zoom)
        self.button_edit.clicked.connect(self.slot_edit)
        self.button_save.clicked.connect(self.slot_save)
#        self.button_back.clicked.connect(self.slot_back)
#        self.button_forward.clicked.connect(self.slot_forward)

# =============================================================================
# slots模块
# =============================================================================
    def slot_home(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.home()
        
    def slot_pan(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.pan()
        
    def slot_zoom(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.zoom()
        
    def slot_config_subplots(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.config_subplots()
        
    def slot_save(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.save_figure()
        
    def slot_back(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.back()
        
    def slot_forward(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.forward()
        
    def slot_edit(self):
        toolbar = self.plotcanvas.add_toolbar()
        toolbar.edit_parameters()
       
#    def slot_save(self):
#        
#        filename, null = QFileDialog.getSaveFileName(self, "Save picture",
#                                    r"E:\\untitled.png",
#                                    "PNG (*.png);;EPS (*.eps)")
#        self.plotcanvas.fig.savefig(filename, dpi = 300)
        
# =============================================================================
# 功能函数模块
# =============================================================================
    def plot(self, filegroup):
        
        if filegroup:         
            for file in filegroup:
                self.plotcanvas.plot_para(file, filegroup[file])
                self.slider.set_slider(0, 100)
                
    
    
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("PlotWindow", "Plot"))
        self.button_zoom.setText(_translate("PlotWindow", "..."))
        self.button_move_left.setText(_translate("PlotWindow", "..."))
        self.button_move_right.setText(_translate("PlotWindow", "..."))