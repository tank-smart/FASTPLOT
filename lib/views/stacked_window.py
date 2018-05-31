# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：堆叠窗口类
#
# =======使用说明
# 。。。
#
# =======日志
# 
# =============================================================================

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QRect, Qt, QMetaObject, QCoreApplication,
                          pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QMenuBar, QPushButton,
                             QMenu, QToolBar, QAction, QStatusBar, QDockWidget, 
                             QStackedWidget, QLineEdit, QTreeWidget, QSizePolicy, 
                             QVBoxLayout, QHBoxLayout, QFrame)

# =============================================================================
# Package views imports
# =============================================================================
from views.data_export_window import DataExportWindow
from views.plot_window import PlotWindow

# =============================================================================
# StackedWindow
# =============================================================================
class StackedWindow(QStackedWidget):

# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)

# =============================================================================
# UI模块    
# =============================================================================
    def setup(self):
        self.setEnabled(True)
        self.setAcceptDrops(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        
#        数据导入界面索引值为0
        self.setup_data_export()
#        绘图界面索引值为1
        self.setup_plot()
#        数学计算界面索引值为2
        self.setup_mathematics()
#        数据操作界面索引值为3
        self.setup_data_manipulate()
#        数据管理界面索引值为4
        self.setup_data_manage()
        
        self.setCurrentIndex(0)

# =============================================================================
# 功能函数模块
# =============================================================================
    def setup_data_export(self):
        self.qwidget_data_export = DataExportWindow(self)
        self.qwidget_data_export.setup()
        self.addWidget(self.qwidget_data_export)

    def setup_plot(self):
        self.qwidget_plot = PlotWindow(self)
        self.qwidget_plot.setup()
        self.addWidget(self.qwidget_plot)

    def setup_mathematics(self):
        self.qwidget_mathematics = QWidget(self)
        self.qwidget_mathematics.setObjectName("qwidget_mathematics")
        self.addWidget(self.qwidget_mathematics)
    
    def setup_data_manipulate(self):
        self.qwidget_data_mani = QWidget(self)
        self.qwidget_data_mani.setObjectName("qwidget_data_mani")
        self.addWidget(self.qwidget_data_mani)
    
    def setup_data_manage(self):
        self.qwidget_data_manage = QWidget(self)
        self.qwidget_data_manage.setObjectName("qwidget_data_manage")
        self.addWidget(self.qwidget_data_manage)

    def show_page(self, pageindex):
        if self.isHidden():
            self.show()
            self.setCurrentIndex(pageindex)
        else:
            self.setCurrentIndex(pageindex)
        