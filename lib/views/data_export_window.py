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
                             QMessageBox, QToolButton, QFileDialog,
                             QSizePolicy, QVBoxLayout,QHBoxLayout,
                             QAbstractItemView, QFrame, QTableWidget,
                             QTableWidgetItem, QComboBox, QDialog)

# =============================================================================
# Package models imports
# =============================================================================
from models.datafile_model import DataFile, Normal_DataFile
import models.time_model as Time
from custom_dialog import SelectTemplateDialog, SaveTemplateDialog
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
        
        paras = {}
        if event.mimeData().hasFormat('application/x-parasname'):
            item_data = event.mimeData().data('application/x-parasname')
            item_stream = QDataStream(item_data, QIODevice.ReadOnly)
            while (not item_stream.atEnd()):
                paraname = item_stream.readQString()
                file_dir = item_stream.readQString()
                if not (file_dir in paras):
                    paras[file_dir] = []
                    paras[file_dir].append(paraname)
                else:
                    paras[file_dir].append(paraname)  
            self.signal_import_para.emit(paras)
            event.acceptProposedAction()
        else:
            event.ignore()

# =============================================================================
# DataExportWindow
# =============================================================================
class DataExportWindow(QWidget):

    signal_get_export_temps = pyqtSignal()
    signal_save_temp = pyqtSignal(dict)
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
#        判断是否删除缺省试验点（即整段时间）
        self.default_testpoint_del = False
        self.testpoint_count = 0
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
        
        self.hlayout_paras_tool = QHBoxLayout()
        self.hlayout_paras_tool.setSpacing(2)
        self.hlayout_paras_tool.setObjectName("hlayout_paras_tool")
        self.tool_button_sel_temp = QToolButton(self)
        self.tool_button_sel_temp.setMinimumSize(QSize(24, 24))
        self.tool_button_sel_temp.setMaximumSize(QSize(24, 24))
        self.tool_button_sel_temp.setObjectName("tool_button_sel_temp")
        self.tool_button_sel_temp.setIcon(QIcon(r"E:\DAGUI\lib\icon\use_template.ico"))
        self.hlayout_paras_tool.addWidget(self.tool_button_sel_temp)
        self.tool_button_save_temp = QToolButton(self)
        self.tool_button_save_temp.setMinimumSize(QSize(24, 24))
        self.tool_button_save_temp.setMaximumSize(QSize(24, 24))
        self.tool_button_save_temp.setObjectName("tool_button_save_temp")
        self.tool_button_save_temp.setIcon(QIcon(r"E:\DAGUI\lib\icon\save_template.ico"))
        self.hlayout_paras_tool.addWidget(self.tool_button_save_temp)
        self.tool_button_del_para = QToolButton(self)
        self.tool_button_del_para.setMinimumSize(QSize(24, 24))
        self.tool_button_del_para.setMaximumSize(QSize(24, 24))
        self.tool_button_del_para.setObjectName("tool_button_del_para")
        self.tool_button_del_para.setIcon(QIcon(r"E:\DAGUI\lib\icon\delete.ico"))
        self.hlayout_paras_tool.addWidget(self.tool_button_del_para)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout_paras_tool.addItem(spacerItem)
        self.vlayout_sel_para.addLayout(self.hlayout_paras_tool)
        
#        使用自定义的树控件
        self.tree_sel_para = SelectedParasTree(self)
        self.tree_sel_para.setColumnCount(2)
        self.tree_sel_para.setObjectName("tree_sel_para")
        self.tree_sel_para.header().setDefaultSectionSize(225)
        self.tree_sel_para.header().setMinimumSectionSize(225)
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

# =======连接信号与槽
# =============================================================================
        self.button_sel_dir.clicked.connect(self.slot_sel_dir)
        
        self.tree_sel_para.signal_import_para.connect(self.slot_import_para)
        self.table_testpoint.cellChanged.connect(self.slot_table_item_changed)
        self.button_confirm.clicked.connect(self.slot_confirm)
        self.button_reset.clicked.connect(self.slot_reset)
        self.tool_button_add.clicked.connect(self.slot_add_testpoint)
        self.tool_button_copy.clicked.connect(self.slot_copy_testpoint)
        self.tool_button_delete.clicked.connect(self.slot_delete_testpoint)
        
        self.tool_button_del_para.clicked.connect(self.slot_delete_paras)
        self.tool_button_save_temp.clicked.connect(self.slot_save_temp)
        self.tool_button_sel_temp.clicked.connect(self.signal_get_export_temps)
        
        self.retranslateUi()

# =============================================================================
# Slots模块
# =============================================================================
    def slot_import_para(self, paras_dict):
        
        if paras_dict:
            ex_paras = []
            for file_dir in paras_dict:
#                判断是否导入的文件已经存在
                index = self.index_in_files_tree(file_dir)
                if  index != -1:
                    for para in paras_dict[file_dir]:
#                        判断导入的参数是否已存在
                        if self.is_in_sel_paras(file_dir, para):
                            ex_paras.append(para)
                        else:
                            child = QTreeWidgetItem(self.tree_sel_para.topLevelItem(index))
                            child.setIcon(0,self.paraicon)
                            child.setText(0,para)
                            child.setText(1,para)
                else:
                    tr = Normal_DataFile(file_dir).time_range
                    row_count = self.table_testpoint.rowCount()
                    if row_count == 0:
                        self.table_testpoint.insertRow(0)
                        name = QTableWidgetItem("Default(total time)")
                        name.setData(Qt.UserRole, "Default(total time)")
                        name.setFlags(Qt.NoItemFlags)
                        self.table_testpoint.setItem(0, 0, name)
                        start = QTableWidgetItem(tr[0])
                        start.setData(Qt.UserRole, tr[0])
                        start.setFlags(Qt.NoItemFlags) 
                        self.table_testpoint.setItem(0, 1, start)
                        end = QTableWidgetItem(tr[1])
                        end.setData(Qt.UserRole, tr[1])
                        end.setFlags(Qt.NoItemFlags) 
                        self.table_testpoint.setItem(0, 2, end)
                        filename = QTableWidgetItem("Untitled")
                        filename.setData(Qt.UserRole, "Untitled")
                        self.table_testpoint.setItem(0, 3, filename)

                        self.add_file_para(file_dir, paras_dict[file_dir])
                    else:
                        if (self.table_testpoint.item(0, 1).data(Qt.UserRole) == tr[0] and 
                            self.table_testpoint.item(0, 2).data(Qt.UserRole) == tr[1]):
                            self.add_file_para(file_dir, paras_dict[file_dir])
                        else:
                            QMessageBox.information(self,
                                    QCoreApplication.translate("DataExportWindow", "导入错误"),
                                    QCoreApplication.translate("DataExportWindow", "文件时间不一致"))
            if ex_paras:
                print_para = "<br>以下参数已存在："
                for pa in ex_paras:
                    print_para += ("<br>" + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate("DataExportWindow", "导入提示"),
                        QCoreApplication.translate("DataExportWindow",
                                                   print_para))
        self.tree_sel_para.expandAll()

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
#                    判断选中的是参数还是文件
                    parent = item.parent() 
                    if parent:
                        child_index = parent.indexOfChild(item)
                        parent.takeChild(child_index)
                        if parent.childCount() == 0:
                            index = self.tree_sel_para.indexOfTopLevelItem(parent)
                            self.tree_sel_para.takeTopLevelItem(index)
                            if self.tree_sel_para.topLevelItemCount() == 0:
                                self.table_testpoint.clearContents()
                                self.table_testpoint.setRowCount(0)

#    选择参数导出模板
    def slot_sel_temp(self, dict_files, templates):

        if templates:
            export_paras = {}
            dialog = SelectTemplateDialog(self, templates)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                if dict_files:
        #            遍历文件，搜索是否存在模板中的参数
        #            不同文件下的同一参数都会找出（这样耗时较长）
        #            也可以找到第一个就停止
                    for paraname in templates[dialog.sel_temp]:
                        for file_dir in dict_files:
                            if paraname in dict_files[file_dir]:
                                if file_dir in export_paras:
                                    export_paras[file_dir].append(paraname)
                                else:
                                    export_paras[file_dir] = []
                                    export_paras[file_dir].append(paraname)
        #                        加入以下语句实现找到第一个就停止的功能
        #                        break
                    self.slot_import_para(export_paras)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate("DataExportWindow", "导入模板错误"),
                            QCoreApplication.translate("DataExportWindow", "没有发现数据文件"))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate("DataExportWindow", "导入模板错误"),
                    QCoreApplication.translate("DataExportWindow", "没有模板"))            

#    保存参数导出模板
    def slot_save_temp(self):
        
        count = self.tree_sel_para.topLevelItemCount()
        if count:
            temp = {}
            dialog = SaveTemplateDialog(self)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                temp_name = dialog.temp_name
                if temp_name:
                    temp[temp_name] = []
                    dict_paras = self.get_dict_sel_paras()
                    for file_dir in dict_paras:
                        for paraname in dict_paras[file_dir]:
                            if paraname in temp[temp_name]:
                                pass
                            else:
                                temp[temp_name].append(paraname)
                    self.signal_save_temp.emit(temp)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate("DataExportWindow", "输入提示"),
                            QCoreApplication.translate("DataExportWindow", "未输入模板名"))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate("DataExportWindow", "保存错误"),
                    QCoreApplication.translate("DataExportWindow", "没有发现参数"))
                
#    确认导出            
    def slot_confirm(self):

        if self.can_export():
            filetype_index = self.combo_box_file_type.currentIndex()
            row_count = self.table_testpoint.rowCount()
            for i in range(row_count):
                filename = self.table_testpoint.item(i, 3).data(Qt.UserRole)
                filepath = (self.line_edit_location.text() +
                            filename +
                            self.combo_box_file_type.currentData(Qt.UserRole))
                if filename != ' ':
                    df_list = []
                    count = self.tree_sel_para.topLevelItemCount()
                    for i in range(count):
                        filedir = self.tree_sel_para.topLevelItem(i).data(0, Qt.UserRole)
                        file = Normal_DataFile(filedir)
                        cols = []
                        paras_count = self.tree_sel_para.topLevelItem(i).childCount()
                        for child_index in range(paras_count):
                            paraname = self.tree_sel_para.topLevelItem(i).child(child_index).text(0)
                            cols.append(paraname)
                        df = file.cols_input(filedir, cols, '\s+', 
                                             self.table_testpoint.item(i, 1).data(Qt.UserRole),
                                             self.table_testpoint.item(i, 2).data(Qt.UserRole))
                        df_list.append(df)
                    df_all = pd.concat(df_list,axis = 1,join = 'outer',
                                       ignore_index = False) #merge different dataframe
                    
#                    按照选择列表中参数的顺序导出数据
                    sort_list = []
                    dict_df = self.get_dict_sel_paras()
                    for file_dir in dict_df:
                        for paraname in dict_df[file_dir]:
                            if paraname in sort_list:
                                pass
                            else:
                                sort_list.append(paraname)
                    df_all = df_all.ix[:, sort_list]
                    
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
        
        self.default_testpoint_del = False
        self.tree_sel_para.clear()
        self.table_testpoint.clearContents()
        self.table_testpoint.setRowCount(0)
        self.line_edit_location.setText("")
    
#    表格中的数据改变后存储试验点的变量的值也要发生改变
    def slot_table_item_changed(self, row, col):
        
        item = self.table_testpoint.item(row, col)
        def_start_item = self.table_testpoint.item(0, 1)
        def_end_item = self.table_testpoint.item(0, 2)
        start_item = self.table_testpoint.item(row, 1)
        end_item = self.table_testpoint.item(row, 2)
        changed_str =  item.data(Qt.DisplayRole)
#        这样判断是为了保证后面的语句不会访问不存在变量
        if changed_str and def_start_item and def_end_item and start_item and end_item:
            if (col == 1 or col == 2):
                if Time.is_std_format(changed_str): 
                    if col == 1:
                        lim_start = def_start_item.data(Qt.UserRole)
                        lim_end = end_item.data(Qt.UserRole)
                        is_in = Time.is_in_range(lim_start,
                                                 lim_end,
                                                 changed_str)
                    if col == 2:
                        lim_start = start_item.data(Qt.UserRole)
                        lim_end = def_end_item.data(Qt.UserRole)
                        is_in = Time.is_in_range(lim_start,
                                                 lim_end,
                                                 changed_str)
                    if is_in:
                        item.setText(changed_str)
                        item.setData(Qt.UserRole, changed_str)
                    else:
                        QMessageBox.information(self,
                                QCoreApplication.translate("DataExportWindow", "时间错误"),
                                QCoreApplication.translate("DataExportWindow", "时间不在范围内"))
                        item.setData(Qt.DisplayRole, item.data(Qt.UserRole))
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate("DataExportWindow", "时间错误"),
                            QCoreApplication.translate("DataExportWindow", "时间格式错误"))
                    item.setData(Qt.DisplayRole, item.data(Qt.UserRole))
            else:
                item.setText(changed_str)
                item.setData(Qt.UserRole, changed_str)
        else:
            item.setData(Qt.DisplayRole, item.data(Qt.UserRole))
            
    def slot_add_testpoint(self):

        row_count = self.table_testpoint.rowCount()
        if row_count:
            self.testpoint_count += 1
            self.table_testpoint.insertRow(row_count)
            t_name = 'Testpoint' + str(self.testpoint_count)
            lim_start = self.table_testpoint.item(0, 1).data(Qt.UserRole)
            lim_end = self.table_testpoint.item(0, 2).data(Qt.UserRole)
            
            name = QTableWidgetItem(t_name)
            name.setData(Qt.UserRole, t_name)
            self.table_testpoint.setItem(row_count, 0, name)
            start = QTableWidgetItem(lim_start)
            start.setData(Qt.UserRole, lim_start)
            self.table_testpoint.setItem(row_count, 1, start)
            end = QTableWidgetItem(lim_end)
            end.setData(Qt.UserRole, lim_end)
            self.table_testpoint.setItem(row_count, 2, end)
            filename = QTableWidgetItem(t_name + ' datafile')
            filename.setData(Qt.UserRole, t_name + ' datafile')
            self.table_testpoint.setItem(row_count, 3, filename)
    
    def slot_copy_testpoint(self):
        
        row = self.table_testpoint.currentRow()

        if row >= 0:
            self.testpoint_count += 1
            row_count = self.table_testpoint.rowCount()
            self.table_testpoint.insertRow(row_count)
            t_name = 'Testpoint' + str(self.testpoint_count)
            lim_start = self.table_testpoint.item(row, 1).data(Qt.UserRole)
            lim_end = self.table_testpoint.item(row, 2).data(Qt.UserRole)
            
            name = QTableWidgetItem(t_name)
            name.setData(Qt.UserRole, t_name)
            self.table_testpoint.setItem(row_count, 0, name)
            start = QTableWidgetItem(lim_start)
            start.setData(Qt.UserRole, lim_start)
            self.table_testpoint.setItem(row_count, 1, start)
            end = QTableWidgetItem(lim_end)
            end.setData(Qt.UserRole, lim_end)
            self.table_testpoint.setItem(row_count, 2, end)
            filename = QTableWidgetItem(t_name + ' datafile')
            filename.setData(Qt.UserRole, t_name + ' datafile')
            self.table_testpoint.setItem(row_count, 3, filename)
    
    def slot_delete_testpoint(self):
        
        row = self.table_testpoint.currentRow()
        if row > 0:
            self.table_testpoint.removeRow(row)
        if row == 0:
            self.default_testpoint_del = True
            self.table_testpoint.item(0, 3).setText(' ')
            self.table_testpoint.item(0, 3).setData(Qt.UserRole, ' ')
            self.table_testpoint.item(0, 3).setFlags(Qt.NoItemFlags)
    
# =============================================================================
# 功能函数模块
# =============================================================================
    def index_in_files_tree(self, file_dir):
        
        count = self.tree_sel_para.topLevelItemCount()
        for index in range(count):
            fd = self.tree_sel_para.topLevelItem(index).data(0, Qt.UserRole)
            if file_dir == fd:
                return index
        return -1
    
    def is_in_sel_paras(self, file_dir, para):

        count = self.tree_sel_para.topLevelItemCount()
        for i in range(count):
            item = self.tree_sel_para.topLevelItem(i)
            filename = item.data(0, Qt.UserRole)
            child_count = item.childCount()
            for child_index in range(child_count):
                paraname = item.child(child_index).text(0)
                if para == paraname and file_dir == filename:
                    return True
        return False

    def add_file_para(self, file_dir, paras):

        root = QTreeWidgetItem(self.tree_sel_para)
        root.setIcon(0,self.fileicon)
        pos = file_dir.rindex('\\')
        filename = file_dir[pos+1:]
        root.setText(0, filename)
        root.setData(0, Qt.UserRole, file_dir)
        root.setFlags(Qt.ItemIsEnabled)
        
        for para in paras:
            child = QTreeWidgetItem(root)
            child.setIcon(0,self.paraicon)
            child.setText(0,para)
            child.setText(1,para)
        
    def get_dict_sel_paras(self):
        
        result = {}
        if self.tree_sel_para:
            count = self.tree_sel_para.topLevelItemCount()
            for i in range(count):
                item = self.tree_sel_para.topLevelItem(i)
                file_dir = item.data(0, Qt.UserRole)
                result[file_dir] = []
                child_count = item.childCount()
                for child_index in range(child_count):
                    paraname = item.child(child_index).text(0)
                    result[file_dir].append(paraname)
        return result
  
    def get_list_testpoints(self):
        
        result = []
        if self.table_testpoint:
            row_count = self.table_testpoint.rowCount()
            for i in range(row_count):
                testpoint = []
                testpoint.append(self.table_testpoint.item(i, 0).data(Qt.UserRole))
                testpoint.append(self.table_testpoint.item(i, 1).data(Qt.UserRole))
                testpoint.append(self.table_testpoint.item(i, 2).data(Qt.UserRole))
                testpoint.append(self.table_testpoint.item(i, 3).data(Qt.UserRole))
                result.append(testpoint)
        return result
    
#    判断是否可以导出
    def can_export(self):
        
        if (self.tree_sel_para.topLevelItemCount and self.line_edit_location.text()):
            if ((not self.default_testpoint_del) and self.table_testpoint.rowCount() >= 1):
                return True
            if (self.default_testpoint_del and self.table_testpoint.rowCount() > 1):
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
        self.tool_button_add.setToolTip(_translate("DataExportWindow", "新增试验点"))
        self.tool_button_delete.setToolTip(_translate("DataExportWindow", "删除试验点"))
        self.tool_button_copy.setToolTip(_translate("DataExportWindow", "拷贝试验点"))
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
        self.tool_button_del_para.setToolTip(_translate("DataExportWindow", "删除参数"))
        self.tool_button_save_temp.setToolTip(_translate("DataExportWindow", "保存模板"))
        self.tool_button_sel_temp.setToolTip(_translate("DataExportWindow", "选择模板"))