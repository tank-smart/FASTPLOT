# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：数据导出类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================

import pandas as pd

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (Qt, QCoreApplication, QSize, pyqtSignal, 
                          QDataStream, QIODevice)
from PyQt5.QtGui import QIcon, QDropEvent, QDragEnterEvent
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QTreeWidget, 
                             QTreeWidgetItem, QSpacerItem, QLineEdit, 
                             QMenu, QMessageBox, QToolButton, QFileDialog,
                             QAction, QSizePolicy, QVBoxLayout,QHBoxLayout,
                             QAbstractItemView, QFrame, QTableWidget,
                             QTableWidgetItem, QComboBox)

# =============================================================================
# Package models imports
# =============================================================================
from models.datafile_model import DataFile, Normal_DataFile
import models.time_model as Time
# =============================================================================
# SelectedParasTree
# =============================================================================
class SelectedParasTree(QTreeWidget):

    signal_import_para = pyqtSignal(dict)    
#    用于显示已选参数，因为需要增加
    def __init__(self, parent = None):
        super().__init__(parent)
#        接受拖放
        self.setAcceptDrops(True)
        self.paras = {}
        
#    重写拖放相关的事件
#    设置部件可接受的MIME type列表，此处的类型是自定义的
    def mimeTypes(self):
        return ['application/x-parasname']
#    拖进事件处理    
    def dragEnterEvent(self, event : QDragEnterEvent):
#        如果拖进来的时树列表才接受
        if event.mimeData().hasFormat('application/x-parasname'):
            event.acceptProposedAction()
        else:
            event.ignore()
#     放下事件处理   
    def dropEvent(self, event : QDropEvent):
        
        if event.mimeData().hasFormat('application/x-parasname'):
            item_data = event.mimeData().data('application/x-parasname')
            item_stream = QDataStream(item_data, QIODevice.ReadOnly)
            while (not item_stream.atEnd()):
                paraname = item_stream.readQString()
                file_dir = item_stream.readQString()
                if not (file_dir in self.paras):
                    self.paras[file_dir] = []
                    self.paras[file_dir].append(paraname)
                else:
                    self.paras[file_dir].append(paraname)  
            self.signal_import_para.emit(self.paras)
            self.paras = {}
            event.acceptProposedAction()
        else:
            event.ignore()

# =============================================================================
# DataExportWindow
# =============================================================================
class DataExportWindow(QWidget):
 
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)
#        选择的参数，键为文件路径，值为参数列表
        self.sel_paras = {}
#        存储试验点信息，第一个固定存储完整时间跨度
        self.testpoints_info = []
#        判断是否删除缺省试验点（即整段时间）
        self.default_testpoint_del = False
#        设置文件与参数的图标
        self.fileicon = QIcon(r"E:\DAGUI\lib\icon\datafile.png")
        self.paraicon = QIcon(r"E:\DAGUI\lib\icon\parameter.png")

# =============================================================================
# UI模块    
# =============================================================================
    def setup(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(4, 0, 4, 0)
        self.verticalLayout.setSpacing(4)
        
        self.vlayout_sel_testpoints = QVBoxLayout()
        self.vlayout_sel_testpoints.setObjectName("vlayout_sel_testpoints")
        self.label_sel_testpoint = QLabel(self)
        self.label_sel_testpoint.setMinimumSize(QSize(0, 24))
        self.label_sel_testpoint.setMaximumSize(QSize(16777215, 24))
        self.label_sel_testpoint.setObjectName("label_sel_testpoint")
        self.vlayout_sel_testpoints.addWidget(self.label_sel_testpoint)
        self.hlayout_sel_testpoints_tool = QHBoxLayout()
        self.hlayout_sel_testpoints_tool.setSpacing(2)
        self.hlayout_sel_testpoints_tool.setObjectName("hlayout_sel_testpoints_tool")
        self.tool_button_add = QToolButton(self)
        self.tool_button_add.setMinimumSize(QSize(24, 24))
        self.tool_button_add.setMaximumSize(QSize(24, 24))
        self.tool_button_add.setObjectName("tool_button_add")
        self.tool_button_add.setIcon(QIcon(r"E:\DAGUI\lib\icon\add.ico"))
        self.hlayout_sel_testpoints_tool.addWidget(self.tool_button_add)
        self.tool_button_delete = QToolButton(self)
        self.tool_button_delete.setMinimumSize(QSize(24, 24))
        self.tool_button_delete.setMaximumSize(QSize(24, 24))
        self.tool_button_delete.setObjectName("tool_button_delete")
        self.tool_button_delete.setIcon(QIcon(r"E:\DAGUI\lib\icon\delete.ico"))
        self.hlayout_sel_testpoints_tool.addWidget(self.tool_button_delete)
        self.tool_button_copy = QToolButton(self)
        self.tool_button_copy.setMinimumSize(QSize(24, 24))
        self.tool_button_copy.setMaximumSize(QSize(24, 24))
        self.tool_button_copy.setObjectName("tool_button_copy")
        self.tool_button_copy.setIcon(QIcon(r"E:\DAGUI\lib\icon\copy.ico"))
        self.hlayout_sel_testpoints_tool.addWidget(self.tool_button_copy)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout_sel_testpoints_tool.addItem(spacerItem)
        self.vlayout_sel_testpoints.addLayout(self.hlayout_sel_testpoints_tool)
        self.table_testpoint = QTableWidget(self)
        self.table_testpoint.setObjectName("table_testpoint")
        self.table_testpoint.setColumnCount(4)
        item = QTableWidgetItem()
        self.table_testpoint.setHorizontalHeaderItem(0, item)
        item.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter)
        item = QTableWidgetItem()
        self.table_testpoint.setHorizontalHeaderItem(1, item)
        item.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter)
        item = QTableWidgetItem()
        self.table_testpoint.setHorizontalHeaderItem(2, item)
        item.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter)
        self.table_testpoint.setHorizontalHeaderItem(3, item)
        self.table_testpoint.horizontalHeader().setDefaultSectionSize(220)
        self.table_testpoint.horizontalHeader().setMinimumSectionSize(220)
        self.vlayout_sel_testpoints.addWidget(self.table_testpoint)
        self.verticalLayout.addLayout(self.vlayout_sel_testpoints)
        
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.hlayout_selpara_and_output = QHBoxLayout()
        self.hlayout_selpara_and_output.setObjectName("hlayout_selpara_and_output")
        self.hlayout_selpara_and_output.setSpacing(4)
        self.vlayout_sel_para = QVBoxLayout()
        self.vlayout_sel_para.setObjectName("vlayout_sel_para")
        self.label_sel_para = QLabel(self)
        self.label_sel_para.setMinimumSize(QSize(0, 24))
        self.label_sel_para.setMaximumSize(QSize(16777215, 24))
        self.label_sel_para.setObjectName("label_sel_para")
        self.vlayout_sel_para.addWidget(self.label_sel_para)
#        使用自定义的树控件
        self.tree_sel_para = SelectedParasTree(self)
        self.tree_sel_para.setColumnCount(2)
        self.tree_sel_para.setObjectName("tree_sel_para")
        self.tree_sel_para.header().setDefaultSectionSize(225)
        self.tree_sel_para.header().setMinimumSectionSize(225)
#        让树可支持右键菜单
        self.tree_sel_para.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_sel_para.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        self.vlayout_sel_para.addWidget(self.tree_sel_para)
        self.hlayout_selpara_and_output.addLayout(self.vlayout_sel_para)        
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.hlayout_selpara_and_output.addWidget(self.line_2)
        self.vlayout_output_config = QVBoxLayout()
        self.vlayout_output_config.setObjectName("vlayout_output_config")
        self.label = QLabel(self)
        self.label.setMinimumSize(QSize(0, 24))
        self.label.setMaximumSize(QSize(16777215, 24))
        self.label.setObjectName("label")
        self.vlayout_output_config.addWidget(self.label)
        self.hlayout_out_filetype = QHBoxLayout()
        self.hlayout_out_filetype.setObjectName("hlayout_out_filetype")
        self.label_file_type = QLabel(self)
        self.label_file_type.setMinimumSize(QSize(80, 24))
        self.label_file_type.setMaximumSize(QSize(80, 24))
        self.label_file_type.setObjectName("label_file_type")
        self.hlayout_out_filetype.addWidget(self.label_file_type)
        self.combo_box_file_type = QComboBox(self)
        self.combo_box_file_type.setMinimumSize(QSize(0, 24))
        self.combo_box_file_type.setMaximumSize(QSize(16777215, 24))
        self.combo_box_file_type.setObjectName("combo_box_file_type")
        self.combo_box_file_type.addItem("")
#        设置每个项目的数据，为后续选择导出文件所使用
        self.combo_box_file_type.setItemData(0, ".txt", Qt.UserRole)
        self.combo_box_file_type.addItem("")
        self.combo_box_file_type.setItemData(1, ".csv", Qt.UserRole)
        self.combo_box_file_type.addItem("")
        self.combo_box_file_type.setItemData(2, ".mat", Qt.UserRole)
        self.hlayout_out_filetype.addWidget(self.combo_box_file_type)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout_out_filetype.addItem(spacerItem1)
        self.vlayout_output_config.addLayout(self.hlayout_out_filetype)
        self.hlayout_out_loc = QHBoxLayout()
        self.hlayout_out_loc.setObjectName("hlayout_out_loc")
        self.label_output_loc = QLabel(self)
        self.label_output_loc.setMinimumSize(QSize(80, 0))
        self.label_output_loc.setMaximumSize(QSize(80, 16777215))
        self.label_output_loc.setObjectName("label_output_loc")
        self.hlayout_out_loc.addWidget(self.label_output_loc)
        self.line_edit_location = QLineEdit(self)
        self.line_edit_location.setMinimumSize(QSize(0, 24))
        self.line_edit_location.setMaximumSize(QSize(16777215, 24))
        self.line_edit_location.setObjectName("line_edit_location")
        self.hlayout_out_loc.addWidget(self.line_edit_location)
        self.button_sel_dir = QToolButton(self)
        self.button_sel_dir.setMinimumSize(QSize(24, 24))
        self.button_sel_dir.setMaximumSize(QSize(24, 24))
        self.button_sel_dir.setObjectName("button_sel_dir")
        self.hlayout_out_loc.addWidget(self.button_sel_dir)
        self.vlayout_output_config.addLayout(self.hlayout_out_loc)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vlayout_output_config.addItem(spacerItem2)
        self.hlayout_selpara_and_output.addLayout(self.vlayout_output_config)
        self.verticalLayout.addLayout(self.hlayout_selpara_and_output)
        
        self.line_3 = QFrame(self)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setMinimumSize(QSize(0, 24))
        self.button_confirm.setMaximumSize(QSize(16777215, 24))
        self.button_confirm.setObjectName("button_confirm")
        self.horizontalLayout.addWidget(self.button_confirm)
        self.button_reset = QPushButton(self)
        self.button_reset.setMinimumSize(QSize(0, 24))
        self.button_reset.setMaximumSize(QSize(16777215, 24))
        self.button_reset.setObjectName("button_reset")
        self.horizontalLayout.addWidget(self.button_reset)
        self.verticalLayout.addLayout(self.horizontalLayout)

#        设置布局中部件的占比，0指选时间点的部件，2指选参数和输出设置的部件
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(2, 3)
        
        self.label_sel_para.raise_()
        self.tree_sel_para.raise_()
        self.label_output_loc.raise_()
        self.label_sel_testpoint.raise_()
        self.label_sel_testpoint.raise_()
        self.combo_box_file_type.raise_()
        self.label_file_type.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
 
        self.action_delete = QAction(self)


# =======连接信号与槽
# =============================================================================
        self.button_sel_dir.clicked.connect(self.slot_sel_dir)
#        使右键时能弹出菜单
        self.tree_sel_para.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        self.tree_sel_para.signal_import_para.connect(self.import_para)
        self.table_testpoint.cellChanged.connect(self.slot_table_item_changed)
        self.action_delete.triggered.connect(self.slot_delete_paras)
        self.button_confirm.clicked.connect(self.slot_confirm)
        self.button_reset.clicked.connect(self.slot_reset)
        self.tool_button_add.clicked.connect(self.slot_add_testpoint)
        self.tool_button_copy.clicked.connect(self.slot_copy_testpoint)
        self.tool_button_delete.clicked.connect(self.slot_delete_testpoint)
        
        self.retranslateUi()

# =============================================================================
# Slots模块
# =============================================================================
#    右键菜单的事件处理
    def on_tree_context_menu(self, pos):
        #        记录右击时鼠标所在的item
        sel_item = self.tree_sel_para.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self.tree_sel_para)
            menu.addAction(self.action_delete)
            menu.exec_(self.tree_sel_para.mapToGlobal(pos))

#    让用户选择项目的路径
    def slot_sel_dir(self):
        
        filedir = QFileDialog.getExistingDirectory(self, "Export directory",
                                                   r"E:\\")
        if filedir:
            filedir = filedir.replace('/','\\')
            self.line_edit_location.setText(filedir)
    
    def slot_delete_paras(self):
        
        sel_items = self.tree_sel_para.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate("DataExportWindow", "删除参数"),
                          QCoreApplication.translate("DataExportWindow", "确定要删除这些参数吗"),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    if item.parent():
                        file = item.parent().data(0, Qt.UserRole)
                        self.sel_paras[file].remove(item.text(0))
#                        删除参数后，清除已没有参数的文件
                        if len(self.sel_paras[file]) == 0:
                            self.sel_paras.pop(file)
                            if len(self.sel_paras) == 0:
                                self.testpoints_info = []
                self.display_sel_para()
                self.display_testpoints()
                
#    确认导出            
    def slot_confirm(self):

        if self.can_export():
            filetype_index = self.combo_box_file_type.currentIndex()
            for test_p in self.testpoints_info:
                filepath = (self.line_edit_location.text() +
                            test_p[3] +
                            self.combo_box_file_type.currentData(Qt.UserRole))
                if test_p[3]:
                    df_list = []
                    for filedir in self.sel_paras:
                        file = Normal_DataFile(filedir)
                        cols = self.sel_paras[filedir]
                        df = file.cols_input(filedir, cols, '\s+', test_p[1], test_p[2])
                        df_list.append(df)
                    df_all = pd.concat(df_list,axis = 1,join = 'outer',
                                       ignore_index = False) #merge different dataframe
                    file_outpout = DataFile(filepath)
    #                导出TXT文件
                    if filetype_index == 0:
                        file_outpout.save_file(filepath , df_all , sep = '\t')
    #                导出CSV文件
                    if filetype_index == 1:
                        file_outpout.save_file(filepath , df_all , sep = ',')
    #                导出MAT文件
                    if filetype_index == 2:
                        file_outpout.save_matfile(filepath, df_all)
            QMessageBox.information(self,
                QCoreApplication.translate("DataExportWindow", "导出提示"),
                QCoreApplication.translate("DataExportWindow", "导出成功"))   
        else:
            QMessageBox.information(self,
                QCoreApplication.translate("DataExportWindow", "导出错误"),
                QCoreApplication.translate("DataExportWindow", "没有选择参数或文件"))            
#    重置
    def slot_reset(self):
        self.sel_paras = {}
        self.testpoints_info = []
        self.default_testpoint_del = False
        self.tree_sel_para.clear()
        self.table_testpoint.clearContents()
        self.table_testpoint.setRowCount(0)
        self.line_edit_location.setText("")
    
#    表格中的数据改变后存储试验点的变量的值也要发生改变
    def slot_table_item_changed(self, row, col):
        
        item = self.table_testpoint.item(row, col)
        changed_str =  item.data(Qt.DisplayRole)
        if changed_str:
    #        第一行存储的试验点名和起止时间不能改变
            if (row != 0 or col == 3):
                if col == 1 or col == 2:
                    if Time.is_std_format(changed_str):
                        if col == 1:
                            is_in = Time.is_in_range(self.testpoints_info[0][1],
                                                     self.testpoints_info[row][2],
                                                     changed_str)
                        if col == 2:
                            is_in = Time.is_in_range(self.testpoints_info[row][1],
                                                     self.testpoints_info[0][2],
                                                     changed_str)
                        if is_in:
                            self.testpoints_info[row][col] = changed_str
                        else:
                            QMessageBox.information(self,
                                    QCoreApplication.translate("DataExportWindow", "时间错误"),
                                    QCoreApplication.translate("DataExportWindow", "时间不在范围内"))
                            item.setData(Qt.DisplayRole, self.testpoints_info[row][col])
                    else:
                        QMessageBox.information(self,
                                QCoreApplication.translate("DataExportWindow", "时间错误"),
                                QCoreApplication.translate("DataExportWindow", "时间格式错误"))
                        item.setData(Qt.DisplayRole, self.testpoints_info[row][col])
                else:
                    self.testpoints_info[row][col] = changed_str
            else:
                item.setData(Qt.DisplayRole, self.testpoints_info[row][col])
        else:
            item.setData(Qt.DisplayRole, self.testpoints_info[row][col])
            
    def slot_add_testpoint(self):
        
        if self.testpoints_info:
            t_name = 'Testpoint' + str(len(self.testpoints_info))
            self.testpoints_info.append([t_name, self.testpoints_info[0][1],
                                         self.testpoints_info[0][2],
                                         t_name + ' datafile'])
            self.display_testpoints()
    
    def slot_copy_testpoint(self):
        
        row = self.table_testpoint.currentRow()
#        不能使用testpoint = self.testpoints_info[row]代替下面这条语句，
#        因为上面这条相等于引用而不是拷贝对象
        t_name = 'Testpoint' + str(len(self.testpoints_info))
        testpoint = [t_name, self.testpoints_info[row][1],
                     self.testpoints_info[row][2],t_name + ' datafile']
        if row >= 0:
            self.testpoints_info.append(testpoint)
            self.display_testpoints()
    
    def slot_delete_testpoint(self):
        
        row = self.table_testpoint.currentRow()
        if row > 0:
            self.testpoints_info.pop(row)
        if row == 0:
            self.default_testpoint_del = True
            self.testpoints_info[0][3] = ''
        self.display_testpoints()
    
# =============================================================================
# 功能函数模块
# =============================================================================
    def import_para(self, paras_with_file):
        
        if paras_with_file:
            for file in paras_with_file:
#                判断是否导入的文件已经存在
                if (file in self.sel_paras):
#                    此变量用于判断导入的参数是否已存在，存在的话提示用户
                    is_exit = False
                    for para in paras_with_file[file]:
#                        判断导入的参数是否已存在
                        if (self.sel_paras[file].count(para) == 0):
                            self.sel_paras[file].append(para)
                        else:
                            is_exit = True
                    if is_exit:
                        QMessageBox.information(self,
                                QCoreApplication.translate("DataExportWindow", "导入提示"),
                                QCoreApplication.translate("DataExportWindow", "参数已存在")) 
                else:
                    tr = Normal_DataFile(file).time_range
                    if not self.testpoints_info:
                        self.testpoints_info.append([])
                        self.testpoints_info[0].append("Default(total time)")
                        self.testpoints_info[0].append(tr[0])
                        self.testpoints_info[0].append(tr[1])
                        self.testpoints_info[0].append("Untitled")
                        self.sel_paras[file] = paras_with_file[file]
                    else:
                        if (self.testpoints_info[0][1] == tr[0] and 
                            self.testpoints_info[0][2] == tr[1]):
                            self.sel_paras[file] = paras_with_file[file]
                        else:
                            QMessageBox.information(self,
                                    QCoreApplication.translate("DataExportWindow", "导入错误"),
                                    QCoreApplication.translate("DataExportWindow", "文件时间不一致"))
                            
#        每次导入参数后都需要更新已选参数的显示
        self.display_sel_para()
        self.display_testpoints()
    
    def display_sel_para(self):

#        不确定是否真的删除了
        self.tree_sel_para.clear()        
        if self.sel_paras:  #file_name is a dict
            for file_dir in self.sel_paras:
                if (len(self.sel_paras[file_dir]) > 0):
                    root = QTreeWidgetItem(self.tree_sel_para) #QTreeWidgetItem object: root
    #                设置图标
                    root.setIcon(0,self.fileicon)
    #                显示文件名而不是路径
                    pos = file_dir.rindex('\\')
                    filename = file_dir[pos+1:]
                    root.setText(0, filename) #set text of treewidget
    #                将路径作为数据存入item中
                    root.setData(0, Qt.UserRole, file_dir)
                    for para in self.sel_paras[file_dir]:
                        child = QTreeWidgetItem(root)  #child of root
                        child.setIcon(0,self.paraicon)
                        child.setText(0,para)
                        child.setText(1,para)
                        
                    self.tree_sel_para.expandAll()
                    
    def display_testpoints(self):
        
        i = 0
        j = 0
        self.table_testpoint.clearContents()
        self.table_testpoint.setRowCount(len(self.testpoints_info))
        if self.testpoints_info:
            for test_p in self.testpoints_info:
                j = 0
                for info in test_p:
                    info_item = QTableWidgetItem(info)
#                    缺省的试验点被删除后设置不可用
                    if i == 0:
                        if j != 3 or self.default_testpoint_del:
                            info_item.setFlags(Qt.NoItemFlags)
                    self.table_testpoint.setItem(i, j, info_item)
                    j += 1
                i += 1
    
#    判断是否可以导出
    def can_export(self):
        
        if (self.sel_paras and self.line_edit_location.text()):
            if ((not self.default_testpoint_del) and len(self.testpoints_info) >= 1):
                return True
            if (self.default_testpoint_del and len(self.testpoints_info) > 1):
                return True
        else:
            return False
        
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("DataExportWindow", "DataExportWindow"))
        self.label_sel_para.setText(_translate("DataExportWindow", "已选参数"))
        self.tree_sel_para.headerItem().setText(0, _translate("DataExportWindow", "初始参数名"))
        self.tree_sel_para.headerItem().setText(1, _translate("DataExportWindow", "参数输出名"))
        self.label_sel_testpoint.setText(_translate("DataExportWindow", "已选试验点"))
        self.tool_button_add.setText(_translate("DataExportWindow", "ADD"))
        self.tool_button_delete.setText(_translate("DataExportWindow", "DEL"))
        self.tool_button_copy.setText(_translate("DataExportWindow", "COPY"))
        item = self.table_testpoint.horizontalHeaderItem(0)
        item.setText(_translate("DataExportWindow", "试验点"))
        item = self.table_testpoint.horizontalHeaderItem(1)
        item.setText(_translate("DataExportWindow", "起始时间"))
        item = self.table_testpoint.horizontalHeaderItem(2)
        item.setText(_translate("DataExportWindow", "终止时间"))
        item = self.table_testpoint.horizontalHeaderItem(3)
        item.setText(_translate("DataExportWindow", "输出文件名"))
        self.label.setText(_translate("DataExportWindow", "输出设置"))
        self.label_file_type.setText(_translate("DataExportWindow", "输出文件类型"))
        self.combo_box_file_type.setItemText(0, _translate("DataExportWindow", "TXT file"))
        self.combo_box_file_type.setItemText(1, _translate("DataExportWindow", "CSV file"))
        self.combo_box_file_type.setItemText(2, _translate("DataExportWindow", "MAT file"))
        self.label_output_loc.setText(_translate("DataExportWindow", "输出文件路径"))
        self.button_sel_dir.setText(_translate("DataExportWindow", "..."))
        self.button_confirm.setText(_translate("DataExportWindow", "确认导出"))
        self.button_reset.setText(_translate("DataExportWindow", "重置"))
        self.action_delete.setText(_translate("DataExport", "删除参数"))