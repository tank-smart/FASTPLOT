# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
<<<<<<< HEAD:lib/views/data_export_window.py
=======
# 创建日期：2018-05-16
# 编码人员：王学良
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/data_export_view.py
# 简述：数据导出类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================
<<<<<<< HEAD:lib/views/data_export_window.py

import pandas as pd
=======
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/data_export_view.py

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import Qt, QCoreApplication, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QTreeWidget, 
                             QTreeWidgetItem, QSpacerItem, QLineEdit, 
                             QMenu, QMessageBox, QToolButton, QFileDialog,
                             QAction, QSizePolicy, QVBoxLayout,QHBoxLayout,
                             QAbstractItemView)

# =============================================================================
<<<<<<< HEAD:lib/views/data_export_window.py
# Package models imports
# =============================================================================
from models.datafile_model import DataFile, Normal_DataFile

# =============================================================================
# DataExportWindow
# =============================================================================
class DataExportWindow(QWidget):
=======
# DataExport
# =============================================================================
class DataExport(QWidget):
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/data_export_view.py
 
# =============================================================================
# 初始化
# =============================================================================
<<<<<<< HEAD:lib/views/data_export_window.py
    def __init__(self, parent = None):
        super().__init__(parent)
=======
    def __init__(self):
        QWidget.__init__(self)
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d:lib/views/data_export_view.py
#        选择的参数，键为文件路径，值为参数列表
        self.sel_paras = {}
#        设置文件与参数的图标
        self.fileicon = QIcon(r"E:\DAGUI\lib\icon\datafile.png")
        self.paraicon = QIcon(r"E:\DAGUI\lib\icon\parameter.png")

# =============================================================================
# UI模块    
# =============================================================================
    def setup(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sel_para = QLabel(self)
        self.sel_para.setObjectName("sel_para")
        self.verticalLayout.addWidget(self.sel_para)
        
        self.sel_para_tree = QTreeWidget(self)
        self.sel_para_tree.setObjectName("sel_para_tree")
        self.sel_para_tree.setColumnCount(2)
        self.sel_para_tree.header().setDefaultSectionSize(240)
        self.sel_para_tree.header().setMinimumSectionSize(240)
#        让树可支持右键菜单
        self.sel_para_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sel_para_tree.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        self.verticalLayout.addWidget(self.sel_para_tree)
        
        self.sel_testpoint = QLabel(self)
        self.sel_testpoint.setObjectName("sel_testpoint")
        self.verticalLayout.addWidget(self.sel_testpoint)
        spacerItem = QSpacerItem(20, 164, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.export_loc = QLabel(self)
        self.export_loc.setObjectName("export_loc")
        self.verticalLayout.addWidget(self.export_loc)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.location_view = QLineEdit(self)
        self.location_view.setMinimumSize(QSize(0, 24))
        self.location_view.setMaximumSize(QSize(16777215, 24))
        self.location_view.setObjectName("location_view")
        self.location_view.setReadOnly(True)
        self.horizontalLayout_2.addWidget(self.location_view)
        self.sel_dir = QToolButton(self)
        self.sel_dir.setMinimumSize(QSize(24, 24))
        self.sel_dir.setMaximumSize(QSize(24, 24))
        self.sel_dir.setObjectName("sel_dir")
        self.horizontalLayout_2.addWidget(self.sel_dir)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setObjectName("button_confirm")
        self.horizontalLayout.addWidget(self.button_confirm)
        self.button_reset = QPushButton(self)
        self.button_reset.setObjectName("button_reset")
        self.horizontalLayout.addWidget(self.button_reset)
        self.verticalLayout.addLayout(self.horizontalLayout)
 
        self.action_delete = QAction(self)
        self.action_delete.setText(QCoreApplication.
                                   translate("DataExport", "删除参数"))

# =======连接信号与槽
# =============================================================================
        self.sel_dir.clicked.connect(self.slot_sel_dir)
#        使右键时能弹出菜单
        self.sel_para_tree.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        self.action_delete.triggered.connect(self.slot_delete)
        self.button_confirm.clicked.connect(self.slot_confirm)
        self.button_reset.clicked.connect(self.slot_reset)
        
        self.retranslateUi()

# =============================================================================
# Slots模块
# =============================================================================
#    右键菜单的事件处理
    def on_tree_context_menu(self, pos):
        #        记录右击时鼠标所在的item
        sel_item = self.sel_para_tree.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self.sel_para_tree)
            menu.addAction(self.action_delete)
            menu.exec_(self.sel_para_tree.mapToGlobal(pos))

#    让用户选择项目的路径
    def slot_sel_dir(self):
        
        filename, null = QFileDialog.getSaveFileName(self, "Export Data",
                                    r"E:\\untitled.csv",
                                    "CSV data (*.csv);;txt data (*.txt)")
        if filename:
            filename = filename.replace('/','\\')
            self.location_view.setText(filename)
    
    def slot_delete(self):
        
        pos = self.sel_para_tree.pos()
        sel_item = self.sel_para_tree.itemAt(pos)
        if sel_item.parent():
            message = QMessageBox.warning(self,
                          QCoreApplication.translate("DataExportWindowt", "删除参数"),
                          QCoreApplication.translate("DataExportWindow", "确定要删除这些参数吗"),
                          QMessageBox.Yes | QMessageBox.No)
            if ( message == QMessageBox.Yes):
                sel_items = self.sel_para_tree.selectedItems()
                for item in sel_items:
                    if item.parent():
                        file = item.parent().data(0, Qt.UserRole)
                        self.sel_paras[file].remove(item.text(0))
                self.display_sel_para(self.sel_paras)
                
    def slot_confirm(self):

        filepath = self.location_view.text()        
        if self.sel_paras and filepath:  #sel_para is QLabel, sel_paras is dict
            df_list = []
            for filedir in self.sel_paras:
                file = Normal_DataFile(filedir)
                cols = self.sel_paras[filedir]
                df = file.cols_input(filedir, cols, sep = '\s+')
                df_list.append(df)
            df_all = pd.concat(df_list,axis = 1,join = 'outer',
                               ignore_index = False) #merge different dataframe
            file_outpout = DataFile(filepath)
            file_outpout.save_file(filepath , df_all , sep = '\t') #/update for more sep/
        else:
             QMessageBox.information(self,
                    QCoreApplication.translate("DataExportWindow", "导出错误"),
                    QCoreApplication.translate("DataExportWindow", "没有选择参数或文件"))            
    
    def slot_reset(self):
        self.sel_paras = {}
        self.sel_para_tree.clear()
        self.location_view.setText("")
    
# =============================================================================
# 功能函数模块
# =============================================================================
    def import_para(self, paras_with_file):
        
        if paras_with_file:
            for file in paras_with_file:
#                判断是否导入的文件已经存在
                if (file in self.sel_paras):
                    for para in paras_with_file[file]:
#                        判断导入的参数是否已存在
                        if (self.sel_paras[file].count(para) == 0):
                            self.sel_paras[file].append(para)
                else:
                    self.sel_paras[file] = paras_with_file[file]
#        每次导入参数后都需要更新已选参数的显示
        self.display_sel_para(self.sel_paras)
    
    def display_sel_para(self, file_group):
        if file_group:  #file_name is a dict
#            不确定是否真的删除了
            self.sel_para_tree.clear()
            
            for file_dir in file_group:
                if (len(file_group[file_dir]) > 0):
                    root = QTreeWidgetItem(self.sel_para_tree) #QTreeWidgetItem object: root
    #                设置图标
                    root.setIcon(0,self.fileicon)
    #                显示文件名而不是路径
                    pos = file_dir.rindex('\\')
                    filename = file_dir[pos+1:]
                    root.setText(0, filename) #set text of treewidget
    #                将路径作为数据存入item中
                    root.setData(0, Qt.UserRole, file_dir)
                    for para in file_group[file_dir]:
                        child = QTreeWidgetItem(root)  #child of root
                        child.setIcon(0,self.paraicon)
                        child.setText(0,para)
                        child.setText(1,para)
                        
                    self.sel_para_tree.expandAll()
       
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.sel_para.setText(_translate("DataExportWindow", "Selected parameters"))
        self.sel_para_tree.headerItem().setText(0,
                                     _translate("DataExportWindow", "Original Name"))
        self.sel_para_tree.headerItem().setText(1,
                                     _translate("DataExportWindow", "Output Name"))
        self.sel_testpoint.setText(_translate("DataExportWindow", "Select testpoint"))
        self.export_loc.setText(_translate("DataExportWindow", "Export location"))
        self.sel_dir.setText(_translate("DataExportWindow", "..."))
        self.button_confirm.setText(_translate("DataExportWindow", "Confirm"))
        self.button_reset.setText(_translate("DataExportWindow", "Reset"))
