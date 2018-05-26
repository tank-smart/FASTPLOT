# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-17
# 编码人员：王学良
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

from views.data_export_view import DataExport

# =============================================================================
# Stacked Widget
# =============================================================================
class StackedWidget(QStackedWidget):
    def __init__(self):
        QStackedWidget.__init__(self)
    
    def setup(self):
        self.setEnabled(True)
        self.setAcceptDrops(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        
        self.setup_data_export()
        self.setup_fig_canvas()
        self.setup_data_manipulate()
        self.setup_data_manage()
        
        self.setCurrentIndex(0)

    def setup_data_export(self):
        self.qwidget_data_export = DataExport()
        self.qwidget_data_export.setup()
        self.addWidget(self.qwidget_data_export)

    def setup_fig_canvas(self):
        self.qwidget_fig_canvas = QWidget(self)
        self.qwidget_fig_canvas.setObjectName("qwidget_fig_canvas")
        self.addWidget(self.qwidget_fig_canvas)
    
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
        else:
            self.setCurrentIndex(pageindex)
        