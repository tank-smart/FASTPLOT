# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-17
# 编码人员：王学良
# 简述：参数窗口类
#
# =======使用说明
# 。。。
#
# =======日志
# 1.2018-05-17 王学良创建文件
# =============================================================================

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (QWidget, QDockWidget, QStackedWidget, QLineEdit,
                             QTreeWidget, QTreeWidgetItem, QSizePolicy,
                             QVBoxLayout, QAbstractItemView)

# =============================================================================
# Stacked Widget
# =============================================================================
class ParalistDock(QDockWidget):
    signal_close = pyqtSignal()
    
    def __init__(self):
        QStackedWidget.__init__(self)
    
    def setup(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.layout_paralist_dock = QWidget(self)
        self.layout_paralist_dock.setObjectName("layout_paralist_dock")
        self.vlayout_paralist_dock = QVBoxLayout(self.layout_paralist_dock)
        self.vlayout_paralist_dock.setContentsMargins(1, 1, 1, 1)
        self.vlayout_paralist_dock.setSpacing(2)
        self.vlayout_paralist_dock.setObjectName("vlayout_paralist_dock")
        self.line_edit_search_para = QLineEdit(self.layout_paralist_dock)
        self.line_edit_search_para.setToolTip("")
        self.line_edit_search_para.setInputMask("")
        self.line_edit_search_para.setText("")
        self.line_edit_search_para.setMaxLength(32766)
        self.line_edit_search_para.setFrame(True)
        self.line_edit_search_para.setEchoMode(QLineEdit.Normal)
        self.line_edit_search_para.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.line_edit_search_para.setReadOnly(False)
        self.line_edit_search_para.setObjectName("line_edit_search_para")
        self.vlayout_paralist_dock.addWidget(self.line_edit_search_para)
        self.tree_widget_display_datafile = QTreeWidget(self.layout_paralist_dock)
        self.tree_widget_display_datafile.setObjectName("tree_widget_display_datafile")
        self.tree_widget_display_datafile.headerItem().setText(0, "1")
        self.tree_widget_display_datafile.header().setVisible(False)
        self.vlayout_paralist_dock.addWidget(self.tree_widget_display_datafile)
        self.setWidget(self.layout_paralist_dock)

    def display(self, file_name):
        if file_name:  #file_name is a list
            for each_file in file_name:
                self.tree_widget_display_datafile.setSelectionMode(QAbstractItemView.ExtendedSelection)
                root=QTreeWidgetItem(self.tree_widget_display_datafile) #QTreeWidgetItem object: root
                root.setText(0,each_file) #set text of treewidget
                para_list=  file_name[each_file]#ndarray to list
                for i in range(len(para_list)):
                    child=QTreeWidgetItem(root)  #child of root
                    child.setText(0,para_list[i])


#    重载关闭事件，需要增加一个关闭的信号让视图的勾选去掉        
    def closeEvent(self, event: QCloseEvent):
        event.accept()
        self.signal_close.emit()
        