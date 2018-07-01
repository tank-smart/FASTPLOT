# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：数据分析类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================
import os
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QSize, QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpacerItem, QSizePolicy, QFrame,
                             QListWidget, QStackedWidget, QPushButton,
                             QToolButton, QPlainTextEdit, QFileDialog,
                             QMessageBox, QListWidgetItem, QAbstractItemView,
                             QDialog)
from models.analysis_model import DataAnalysis
# =============================================================================
# Package models imports
# =============================================================================
from models.datafile_model import Normal_DataFile
from views.custom_dialog import SelParasDialog
import views.src_icon as ICON

class DataAnalysisWindow(QWidget):
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.current_dir = ""
#        设置文件与参数的图标
        self.fileicon = QIcon(ICON.ICON_FILE)
        self.paraicon = QIcon(ICON.ICON_PARA)

# =============================================================================
# UI模块
# =============================================================================        
    def setup(self):
        
        self.resize(740, 513)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(4, 4, 4, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_analysis_type = QLabel(self)
        self.label_analysis_type.setMinimumSize(QSize(100, 24))
        self.label_analysis_type.setMaximumSize(QSize(100, 24))
        self.label_analysis_type.setObjectName("label_analysis_type")
        self.horizontalLayout.addWidget(self.label_analysis_type)
        self.combo_box_analysis_type = QComboBox(self)
        self.combo_box_analysis_type.setMinimumSize(QSize(120, 24))
        self.combo_box_analysis_type.setMaximumSize(QSize(120, 24))
        self.combo_box_analysis_type.setObjectName("combo_box_analysis_type")
        self.combo_box_analysis_type.addItem("")
        self.combo_box_analysis_type.addItem("")
        self.horizontalLayout.addWidget(self.combo_box_analysis_type)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.page_data_sift = QWidget()
        self.page_data_sift.setObjectName("page_data_sift")
        self.verticalLayout_5 = QVBoxLayout(self.page_data_sift)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QLabel(self.page_data_sift)
        self.label.setMinimumSize(QSize(120, 24))
        self.label.setMaximumSize(QSize(120, 24))
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tool_btn_add_file = QToolButton(self.page_data_sift)
        self.tool_btn_add_file.setIcon(QIcon(ICON.ICON_ADD))
        self.tool_btn_add_file.setMinimumSize(QSize(24, 24))
        self.tool_btn_add_file.setMaximumSize(QSize(24, 24))
        self.tool_btn_add_file.setObjectName("tool_btn_add_file")
        self.horizontalLayout_3.addWidget(self.tool_btn_add_file)
        self.tool_btn_delete_file = QToolButton(self.page_data_sift)
        self.tool_btn_delete_file.setIcon(QIcon(ICON.ICON_DEL))
        self.tool_btn_delete_file.setMinimumSize(QSize(24, 24))
        self.tool_btn_delete_file.setMaximumSize(QSize(24, 24))
        self.tool_btn_delete_file.setObjectName("tool_btn_delete_file")
        self.horizontalLayout_3.addWidget(self.tool_btn_delete_file)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.list_widget_src_files = QListWidget(self.page_data_sift)
        self.list_widget_src_files.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        self.list_widget_src_files.setObjectName("list_widget_src_files")
        self.verticalLayout_2.addWidget(self.list_widget_src_files)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.line_2 = QFrame(self.page_data_sift)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QLabel(self.page_data_sift)
        self.label_2.setMinimumSize(QSize(120, 24))
        self.label_2.setMaximumSize(QSize(120, 24))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tool_btn_add_paras = QToolButton(self.page_data_sift)
        self.tool_btn_add_paras.setIcon(QIcon(ICON.ICON_ADD))
        self.tool_btn_add_paras.setMinimumSize(QSize(24, 24))
        self.tool_btn_add_paras.setMaximumSize(QSize(24, 24))
        self.tool_btn_add_paras.setObjectName("tool_btn_add_paras")
        self.horizontalLayout_5.addWidget(self.tool_btn_add_paras)
        self.tool_btn_delete_paras = QToolButton(self.page_data_sift)
        self.tool_btn_delete_paras.setIcon(QIcon(ICON.ICON_DEL))
        self.tool_btn_delete_paras.setMinimumSize(QSize(24, 24))
        self.tool_btn_delete_paras.setMaximumSize(QSize(24, 24))
        self.tool_btn_delete_paras.setObjectName("tool_btn_delete_paras")
        self.horizontalLayout_5.addWidget(self.tool_btn_delete_paras)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.list_widget_target_paras = QListWidget(self.page_data_sift)
        self.list_widget_target_paras.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        self.list_widget_target_paras.setObjectName("list_widget_target_paras")
        self.verticalLayout_3.addWidget(self.list_widget_target_paras)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.line_3 = QFrame(self.page_data_sift)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_5.addWidget(self.line_3)
        self.label_3 = QLabel(self.page_data_sift)
        self.label_3.setMinimumSize(QSize(120, 24))
        self.label_3.setMaximumSize(QSize(120, 24))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.plain_text_edit_ser_condition = QPlainTextEdit(self.page_data_sift)
        self.plain_text_edit_ser_condition.setObjectName("plain_text_edit_ser_condition")
        self.horizontalLayout_4.addWidget(self.plain_text_edit_ser_condition)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tool_btn_add_condition_para = QToolButton(self.page_data_sift)
        self.tool_btn_add_condition_para.setIcon(QIcon(ICON.ICON_ADD))
        self.tool_btn_add_condition_para.setMinimumSize(QSize(24, 24))
        self.tool_btn_add_condition_para.setMaximumSize(QSize(24, 24))
        self.tool_btn_add_condition_para.setObjectName("tool_btn_add_condition_para")
        self.verticalLayout_4.addWidget(self.tool_btn_add_condition_para)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.line_4 = QFrame(self.page_data_sift)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_5.addWidget(self.line_4)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.btn_confirm = QPushButton(self.page_data_sift)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout_6.addWidget(self.btn_confirm)
        self.btn_reset = QPushButton(self.page_data_sift)
        self.btn_reset.setMinimumSize(QSize(0, 24))
        self.btn_reset.setMaximumSize(QSize(16777215, 24))
        self.btn_reset.setObjectName("btn_reset")
        self.horizontalLayout_6.addWidget(self.btn_reset)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.stackedWidget.addWidget(self.page_data_sift)
        
        self.page_data_process = QWidget()
        self.page_data_process.setObjectName("page_data_process")
        self.stackedWidget.addWidget(self.page_data_process)
        self.verticalLayout.addWidget(self.stackedWidget)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        
# =======连接信号与槽
# =============================================================================        
        self.combo_box_analysis_type.currentIndexChanged.connect(self.slot_show_page)
        self.tool_btn_add_file.clicked.connect(self.slot_import_src_datafiles)
        self.tool_btn_delete_file.clicked.connect(self.slot_delete_files)
        self.tool_btn_add_paras.clicked.connect(self.slot_add_paras)
        self.tool_btn_add_condition_para.clicked.connect(self.slot_add_condition_para)
        self.tool_btn_delete_paras.clicked.connect(self.slot_delete_paras)
        self.btn_reset.clicked.connect(self.slot_reset)
        self.btn_confirm.clicked.connect(self.slot_confirm)
        
# =============================================================================
# slots模块
# =============================================================================
    def slot_show_page(self, index):
        
        self.stackedWidget.setCurrentIndex(index)
        
    def slot_import_src_datafiles(self):

        init_dir = self.current_dir
        if init_dir:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, 'Open', init_dir, "Datafiles (*.txt *.csv *.dat)")
        else:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, 'Open', r'E:\\', "Datafiles (*.txt *.csv *.dat)")
        if file_dir_list:
            file_dir_list = [file.replace('/','\\') for file in file_dir_list]
            if os.path.exists(file_dir_list[0]):
                self.current_dir = os.path.dirname(file_dir_list[0])
            for file_dir in file_dir_list:
                try:
                    Normal_DataFile(file_dir)
                    pos = file_dir.rindex('\\')
                    filename = file_dir[pos+1:]
                    if file_dir not in self.get_list_files():
                        item_file = QListWidgetItem(filename, self.list_widget_src_files)
                        item_file.setIcon(self.fileicon)
                        item_file.setData(Qt.UserRole, file_dir)
#                        此处需要修改，不然有可能连续弹出窗口
                    else:
                        QMessageBox.information(self,
                            QCoreApplication.translate("DataAnalysisWindow", "打开文件提示"),
                            QCoreApplication.translate("DataAnalysisWindow", "文件已存在"))
                except:
                    info = "文件" + "<br>" + file_dir + "<br>不正确"
                    QMessageBox.information(self,
                        QCoreApplication.translate("DataAnalysisWindow", "打开文件提示"),
                        QCoreApplication.translate("DataAnalysisWindow", info))

    def slot_delete_files(self):
        
        sel_items = self.list_widget_src_files.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate("DataAnalysisWindow", "删除参数"),
                          QCoreApplication.translate("DataAnalysisWindow", "确定要删除这些文件吗"),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_widget_src_files.takeItem(self.list_widget_src_files.row(item))
                    if self.list_widget_src_files.count():
                        pass
                    else:
                        self.list_widget_target_paras.clear()
                        self.plain_text_edit_ser_condition.clear()
                        
    def slot_delete_paras(self):
        
        sel_items = self.list_widget_target_paras.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate("DataAnalysisWindow", "删除参数"),
                          QCoreApplication.translate("DataAnalysisWindow", "确定要删除这些参数吗"),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_widget_target_paras.takeItem(self.list_widget_target_paras.row(item))
                        
    def slot_add_paras(self):

        list_paras = []
        def add_paras():
            ex_paras = []
            paras = dialog.get_list_sel_paras()
            for para in paras:
                cur_paras = self.get_list_paras()
                if para not in cur_paras:
                    item = QListWidgetItem(para, self.list_widget_target_paras)
                    item.setIcon(self.paraicon)
                    item.setSelected(True)
                    list_paras.append(item)
                else:
                    ex_paras.append(para)
                if ex_paras:
                    print_para = "<br>以下参数已存在："
                    for pa in ex_paras:
                        print_para += ("<br>" + pa)
                    QMessageBox.information(self,
                            QCoreApplication.translate("DataAnalysisWindow", "添加提示"),
                            QCoreApplication.translate("DataAnalysisWindow",
                                                       print_para))
                
#        采用多选模式
        dialog = SelParasDialog(self, self.get_list_files(), 1)
        dialog.signal_add_paras.connect(add_paras)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Rejected):
            for item in list_paras:
                self.list_widget_target_paras.takeItem(self.list_widget_target_paras.row(item))
    
    def slot_add_condition_para(self):
        
#        采用单选模式
        dialog = SelParasDialog(self, self.get_list_files(), 0)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                self.plain_text_edit_ser_condition.insertPlainText(paras[0])
                
    def slot_reset(self):
        
        self.list_widget_src_files.clear()
        self.list_widget_target_paras.clear()
        self.plain_text_edit_ser_condition.clear()
    
    def slot_confirm(self):
        
        list_files = self.get_list_files()
        list_paras = self.get_list_paras()
        str_condition = self.plain_text_edit_ser_condition.toPlainText()
        if list_files and list_paras and str_condition:
            da=DataAnalysis()
            result_dict=da.condition_sift_1(list_files, str_condition,list_paras)
            print(result_dict)
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate("DataAnalysisWindow", "提示"),
                    QCoreApplication.translate("DataAnalysisWindow","没有足够的输入"))

# =============================================================================
# 功能函数模块   
# =============================================================================
    def get_list_files(self):
        
        list_files = []
        count = self.list_widget_src_files.count()
        for i in range(count):
            item = self.list_widget_src_files.item(i)
            list_files.append(item.data(Qt.UserRole))
        return list_files
    
    def get_list_paras(self):
        
        list_paras = []
        count = self.list_widget_target_paras.count()
        for i in range(count):
            item = self.list_widget_target_paras.item(i)
            list_paras.append(item.text())
        return list_paras

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label_analysis_type.setText(_translate("DataAnalysisWindow", "数据分析类型"))
        self.combo_box_analysis_type.setItemText(0, _translate("DataAnalysisWindow", "数据筛选"))
        self.combo_box_analysis_type.setItemText(1, _translate("DataAnalysisWindow", "数据处理"))
        self.label.setText(_translate("DataAnalysisWindow", "源文件"))
        self.tool_btn_add_file.setToolTip(_translate("DataAnalysisWindow", "添加文件"))
        self.tool_btn_delete_file.setToolTip(_translate("DataAnalysisWindow", "删除文件"))
        self.label_2.setText(_translate("DataAnalysisWindow", "结果参数"))
        self.tool_btn_add_paras.setToolTip(_translate("DataAnalysisWindow", "添加参数"))
        self.tool_btn_delete_paras.setToolTip(_translate("DataAnalysisWindow", "删除参数"))
        self.label_3.setText(_translate("DataAnalysisWindow", "搜索条件"))
        self.tool_btn_add_condition_para.setToolTip(_translate("DataAnalysisWindow", "添加参数"))
        self.btn_confirm.setText(_translate("DataAnalysisWindow", "确认"))
        self.btn_reset.setText(_translate("DataAnalysisWindow", "重置"))

