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
# =============================================================================
# imports
# =============================================================================
import re

from PyQt5.QtCore import QSize, QCoreApplication, pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QLineEdit, 
                             QGroupBox, QSpacerItem, QTreeWidget, 
                             QTreeWidgetItem, QMessageBox)

import views.constant as CONSTANT


class DataDictWindow(QWidget):
    signal_data_dict_changed = pyqtSignal(dict)
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.data_dict = {}
        self.current_para_item = None
        
    def setup(self):

        self.horizontalLayout_3 = QHBoxLayout(self)
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setSpacing(2)
        self.group_box_paras = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_paras)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.line_edit_filter = QLineEdit(self.group_box_paras)
        self.line_edit_filter.setMinimumSize(QSize(0, 24))
        self.line_edit_filter.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_filter)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tree_paras = QTreeWidget(self.group_box_paras)
#        让顶级项没有扩展符空白
        self.tree_paras.setRootIsDecorated(False)
        self.tree_paras.header().setDefaultSectionSize(150)
        self.tree_paras.header().setMinimumSectionSize(150)
        
        self.verticalLayout.addWidget(self.tree_paras)
        self.horizontalLayout_3.addWidget(self.group_box_paras)
        self.group_box_parachara = QGroupBox(self)
        self.verticalLayout_3 = QVBoxLayout(self.group_box_parachara)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.label_symbol = QLabel(self.group_box_parachara)
#        支持label中的文字可选择
        self.label_symbol.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_symbol.setMinimumSize(QSize(0, 24))
        self.label_symbol.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_3.addWidget(self.label_symbol)
        self.group_box_name = QGroupBox(self.group_box_parachara)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_name)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.line_edit_paraname = QLineEdit(self.group_box_name)
        self.line_edit_paraname.setMinimumSize(QSize(0, 24))
        self.line_edit_paraname.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_2.addWidget(self.line_edit_paraname)
        self.verticalLayout_3.addWidget(self.group_box_name)
        
        self.group_box_unit = QGroupBox(self.group_box_parachara)
        self.vlayout_unit = QVBoxLayout(self.group_box_unit)
        self.vlayout_unit.setContentsMargins(2, 2, 2, 2)
        self.vlayout_unit.setSpacing(2)
        self.line_edit_unit = QLineEdit(self.group_box_unit)
        self.line_edit_unit.setMinimumSize(QSize(0, 24))
        self.line_edit_unit.setMaximumSize(QSize(16777215, 24))
        self.vlayout_unit.addWidget(self.line_edit_unit)
        self.verticalLayout_3.addWidget(self.group_box_unit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btn_save = QPushButton(self.group_box_parachara)
        self.btn_save.setMinimumSize(QSize(0, 24))
        self.btn_save.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.btn_cancel = QPushButton(self.group_box_parachara)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        
        spacerItem = QSpacerItem(20, 302, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.group_box_parachara)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 2)

        self.retranslateUi()
#        加载数据字典
        self.load_data_dict()
        
        self.line_edit_filter.textChanged.connect(self.slot_search_para)
        self.tree_paras.itemClicked.connect(self.slot_display_para)
        self.line_edit_paraname.editingFinished.connect(self.slot_paraname_change)
        self.line_edit_unit.editingFinished.connect(self.slot_unit_change)
        
        self.btn_save.clicked.connect(self.slot_save)
        self.btn_cancel.clicked.connect(self.slot_cancel)

# =============================================================================
# Slots模块
# =============================================================================
#    搜索参数并显示在参数窗口里
    def slot_search_para(self, para_name):
        
        if self.tree_paras:
            count = self.tree_paras.topLevelItemCount()
            pattern = re.compile('.*' + para_name + '.*')
            for i in range(count):
                item = self.tree_paras.topLevelItem(i)
                symbol = item.text(0)
                paraname = item.text(1)
                if re.match(pattern, symbol) or re.match(pattern, paraname):
                    item.setHidden(False)
                else:
                    item.setHidden(True)
                    
    def slot_display_para(self, item):
        
        if item:
            self.current_para_item = item
            symbol = item.text(0)
            paraname = self.data_dict[symbol][0]
            unit = self.data_dict[symbol][1]
            self.label_symbol.setText(symbol)
            self.line_edit_paraname.setText(paraname)
            self.line_edit_unit.setText(unit)
    
    def slot_paraname_change(self):
        
        if self.current_para_item:
            symbol = self.label_symbol.text()
            text = self.line_edit_paraname.text()
            text = text.split(',')
            if len(text) > 1:
                QMessageBox.information(self,
                                QCoreApplication.translate('DataDictWindow', '修改提示'),
                                QCoreApplication.translate('DataDictWindow', '不支持带逗号的参数名。'))
                self.line_edit_paraname.setText(self.data_dict[symbol][0])
            if not self.line_edit_paraname.text():
                self.line_edit_paraname.setText('NaN')
                
    def slot_unit_change(self):
        
        if self.current_para_item:
            symbol = self.label_symbol.text()
            text = self.line_edit_unit.text()
            text = text.split(',')
            if len(text) > 1:
                QMessageBox.information(self,
                                        QCoreApplication.translate('DataDictWindow', '修改提示'),
                                        QCoreApplication.translate('DataDictWindow', '不支持带逗号的单位。'))
                self.line_edit_unit.setText(self.data_dict[symbol][1])
            if not self.line_edit_unit.text():
                self.line_edit_unit.setText('NaN')
                
    def slot_save(self):
        
        if self.current_para_item:
            item = self.current_para_item
            symbol = self.label_symbol.text()
            paraname = self.line_edit_paraname.text()
            unit = self.line_edit_unit.text()
            self.data_dict[symbol][0] = paraname
            self.data_dict[symbol][1] = unit
            self.signal_data_dict_changed.emit(self.data_dict)
            item.setText(1, paraname)
            item.setText(2, unit)
            QMessageBox.information(self,
                                    QCoreApplication.translate('DataDictWindow', '保存提示'),
                                    QCoreApplication.translate('DataDictWindow', '保存成功！'))
            
    def slot_cancel(self):
        
        if self.current_para_item:
            self.slot_display_para(self.current_para_item)
            
    def slot_add_dict(self, symbol : str):
        
        if not(symbol in self.data_dict):
            item = QTreeWidgetItem(self.tree_paras)
            item.setText(0, symbol)
            item.setText(1, 'NaN')
            item.setText(2, 'NaN')
            self.data_dict[symbol] = ['NaN', 'NaN']
#            设置当前的模板为第一个模板并显示模板信息
            self.tree_paras.setCurrentItem(item)
            self.current_para_item = item
            self.slot_display_para(self.current_para_item)
        else:
            QMessageBox.information(self,
                                    QCoreApplication.translate('DataDictWindow', '增加提示'),
                                    QCoreApplication.translate('DataDictWindow', '该参数已存在！'))
                
# =============================================================================
# 功能函数模块
# =============================================================================
#    从文件中加载数据字典进入内存
    def load_data_dict(self):
        
        try:
#            导入导出参数的模板
            with open(CONSTANT.SETUP_DIR + r'\data\data_dict.txt', 'r') as file:
                line = file.readline()
                if line == 'DataDict\n':
                    line = file.readline()
                    while line:
#                        readline函数会把'\n'也读进来，去除'\n'
                        para_info = line.strip('\n')
                        para_info_list = para_info.split(',')
                        if not(para_info_list[0] in self.data_dict):
                            self.data_dict[para_info_list[0]] = para_info_list[1:]
                        line = file.readline()
        except:
            pass
        
        self.redisplay_data_dict()
        self.signal_data_dict_changed.emit(self.data_dict)
        
#    将内存中的数据字典导出到文件
    def output_data_dict(self):

        try:
#            打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(CONSTANT.SETUP_DIR + r'\data\data_dict.txt', 'w') as file:
                file.write('DataDict\n')
#                将内存中的模板一一写入文件
                for symbol in self.data_dict:
                    temp = symbol + ','
                    count = len(self.data_dict[symbol])
                    for i, info in enumerate(self.data_dict[symbol]):
                        if i != (count - 1):
                            temp += info + ','
                        else:
                            temp += info
                    file.write(temp + '\n')
        except:
            pass
        
    def redisplay_data_dict(self):
        
        if self.data_dict:
            for symbol in self.data_dict:
                item = QTreeWidgetItem(self.tree_paras)
                item.setText(0, symbol)
                item.setText(1, self.data_dict[symbol][0])
                item.setText(2, self.data_dict[symbol][1])
#            设置当前的模板为第一个模板并显示模板信息
            self.tree_paras.setCurrentItem(self.tree_paras.topLevelItem(0))
            self.current_para_item = self.tree_paras.currentItem()
            self.slot_display_para(self.current_para_item)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_paras.setTitle(_translate('DataDictWindow', '字典浏览器'))
        self.line_edit_filter.setPlaceholderText(_translate('DataDictWindow', '过滤器'))
        self.tree_paras.headerItem().setText(0, _translate('DataDictWindow', '软件标识符'))
        self.tree_paras.headerItem().setText(1, _translate('DataDictWindow', '参数名'))
        self.tree_paras.headerItem().setText(2, _translate('DataDictWindow', '单位'))
        self.group_box_parachara.setTitle(_translate('DataDictWindow', '参数属性设置'))
        self.label_symbol.setText(_translate('DataDictWindow', ' '))
        self.group_box_name.setTitle(_translate('DataDictWindow', '参数名'))
        self.group_box_unit.setTitle(_translate('DataDictWindow', '单位'))
        self.btn_save.setText(_translate('DataDictWindow', '保存'))
        self.btn_cancel.setText(_translate('DataDictWindow', '取消'))