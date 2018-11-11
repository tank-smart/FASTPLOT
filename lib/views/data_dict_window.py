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
import re, os, json

from PyQt5.QtCore import QSize, QCoreApplication, pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QLineEdit, 
                             QGroupBox, QSpacerItem, QTreeWidget, 
                             QTreeWidgetItem, QMessageBox, QMenu,
                             QAction, QAbstractItemView, QFileDialog)
from PyQt5.QtGui import QFont

import views.config_info as CONFIG


class DataDictWindow(QWidget):
    signal_data_dict_changed = pyqtSignal(dict)
    signal_close_dd_dock = pyqtSignal()
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.data_dict = {}
        self.current_para_item = None
        self.dir_import = CONFIG.SETUP_DIR
        self.current_para_change_status = False
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
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
#        设置选择模式
        self.tree_paras.setSelectionMode(QAbstractItemView.ExtendedSelection)
#        让树可支持右键菜单(step 1)
        self.tree_paras.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_delete = QAction(self.tree_paras)
        self.action_delete.setText(QCoreApplication.
                                   translate('DataDictWindow', '删除'))
        self.action_import = QAction(self.tree_paras)
        self.action_import.setText(QCoreApplication.
                                   translate('DataDictWindow', '批量导入'))
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
        self.btn_close = QPushButton(self.group_box_parachara)
        self.btn_close.setMinimumSize(QSize(0, 24))
        self.btn_close.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_2.addWidget(self.btn_close)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        
        spacerItem = QSpacerItem(20, 302, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.group_box_parachara)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 2)

#        使右键时能弹出菜单(step 2)
        self.tree_paras.customContextMenuRequested.connect(self.on_context_menu)
        self.line_edit_filter.textChanged.connect(self.slot_search_para)
        self.tree_paras.itemClicked.connect(self.slot_display_para)
        self.line_edit_paraname.editingFinished.connect(self.slot_paraname_change)
        self.line_edit_unit.editingFinished.connect(self.slot_unit_change)
        self.action_delete.triggered.connect(self.slot_delete_paras)
        self.action_import.triggered.connect(self.slot_import_dict)
        
        self.btn_save.clicked.connect(self.slot_save)
        self.btn_cancel.clicked.connect(self.slot_cancel)
        self.btn_close.clicked.connect(self.slot_close)
        
        self.retranslateUi()
#        加载数据字典
        self.load_data_dict()

# =============================================================================
# Slots模块
# =============================================================================
    def on_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.tree_paras.itemAt(pos)
        
#        创建菜单，添加动作，显示菜单
        menu = QMenu(self.tree_paras)
        menu.addActions([self.action_delete,
                         self.action_import])
        if sel_item:
            self.action_delete.setEnabled(True)
        else:
            self.action_delete.setEnabled(False)
        menu.exec_(self.tree_paras.mapToGlobal(pos))
        
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
            if self.current_para_change_status:
                message = QMessageBox.warning(self,
                              QCoreApplication.translate('DataDictWindow', '保存提示'),
                              QCoreApplication.translate('DataDictWindow',
                                                         '字典：' + self.label_symbol.text() + '未保存，是否保存？'),
                              QMessageBox.Yes | QMessageBox.No)
                if (message == QMessageBox.Yes):
                    self.slot_save()
                else:
                    self.current_para_change_status = False
            self.current_para_item = item
            symbol = item.text(0)
            paraname = self.data_dict[symbol][0]
            unit = self.data_dict[symbol][1]
            self.label_symbol.setText(symbol)
            if paraname != 'NaN':
                self.line_edit_paraname.setText(paraname)
            else:
                self.line_edit_paraname.setText('')
            if unit != 'NaN':
                self.line_edit_unit.setText(unit)
            else:
                self.line_edit_unit.setText('')
    
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
                self.line_edit_paraname.setText('')
            text = self.line_edit_paraname.text()
            if text != self.data_dict[symbol][0]:
                self.current_para_change_status = True
            else:
                self.current_para_change_status = False
                
    def slot_unit_change(self):
        
        if self.current_para_item:
            self.current_para_change_status = True
            symbol = self.label_symbol.text()
            text = self.line_edit_unit.text()
            text = text.split(',')
            if len(text) > 1:
                QMessageBox.information(self,
                                        QCoreApplication.translate('DataDictWindow', '修改提示'),
                                        QCoreApplication.translate('DataDictWindow', '不支持带逗号的单位。'))
                self.line_edit_unit.setText(self.data_dict[symbol][1])
            if not self.line_edit_unit.text():
                self.line_edit_unit.setText('')
            text = self.line_edit_unit.text()
            if text != self.data_dict[symbol][1]:
                self.current_para_change_status = True
            else:
                self.current_para_change_status = False
                
    def slot_save(self):
        
        if self.current_para_item:
            item = self.current_para_item
            symbol = self.label_symbol.text()
            paraname = self.line_edit_paraname.text()
            unit = self.line_edit_unit.text()
            if paraname != '':
                self.data_dict[symbol][0] = paraname
                item.setText(1, paraname)
            else:
                self.data_dict[symbol][0] = 'NaN'
                item.setText(1, '')
            if unit != '':
                self.data_dict[symbol][1] = unit
                item.setText(2, unit)
            else:
                self.data_dict[symbol][1] = 'NaN'
                item.setText(2, '')
            self.signal_data_dict_changed.emit(self.data_dict)
            self.save_data_dict()
            QMessageBox.information(self,
                                    QCoreApplication.translate('DataDictWindow', '保存提示'),
                                    QCoreApplication.translate('DataDictWindow', '保存成功！'))
            self.current_para_change_status = False
            
    def slot_cancel(self):
        
        if self.current_para_item:
            self.current_para_change_status = False
            self.slot_display_para(self.current_para_item)
            
    def slot_add_dict(self, symbol : str):
        
        if not(symbol in self.data_dict):
            item = QTreeWidgetItem(self.tree_paras)
            item.setText(0, symbol)
#            item.setIcon(0, QIcon(CONFIG.ICON_PARA))
#            item.setText(1, '')
#            item.setText(2, '')
            self.data_dict[symbol] = ['NaN', 'NaN']
            self.tree_paras.setCurrentItem(item)
            self.slot_display_para(item)
        else:
            items = self.tree_paras.findItems(symbol, Qt.MatchExactly)
            if items:
                self.tree_paras.setCurrentItem(items[0])
                self.slot_display_para(items[0])
            QMessageBox.information(self,
                                    QCoreApplication.translate('DataDictWindow', '增加提示'),
                                    QCoreApplication.translate('DataDictWindow', '该参数已存在！'))
    
    def slot_delete_paras(self):
        
        items = self.tree_paras.selectedItems()
        if items:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataDictWindow', '删除字典'),
                          QCoreApplication.translate('DataDictWindow', '确定要删除所选数据字典吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in items:
                    self.tree_paras.takeTopLevelItem(self.tree_paras.indexOfTopLevelItem(item))
                    del self.data_dict[item.text(0)]
                self.tree_paras.setCurrentItem(self.tree_paras.currentItem())
                self.slot_display_para(self.tree_paras.currentItem())
                self.save_data_dict()
                self.signal_data_dict_changed.emit(self.data_dict)
                if self.data_dict:
                    pass
                else:
                    self.label_symbol.setText('')
                    self.line_edit_paraname.setText('')
                    self.line_edit_unit.setText('')
    
    def slot_import_dict(self):
        
        data_dict = {}
        ex_paras = []
        if os.path.exists(self.dir_import):
            file_dir, unkown = QFileDialog.getOpenFileName(
                        self, 'Import data dictionary', self.dir_import, 'file (*.txt *.csv)')
        else:
            file_dir, unkown = QFileDialog.getOpenFileName(
                        self, 'Import data dictionary', CONFIG.SETUP_DIR, 'file (*.txt *.csv)')

        if file_dir:
            file_dir = file_dir.replace('/','\\')
            self.dir_import = os.path.dirname(file_dir)
            try:
                with open(file_dir, 'r') as file:
                    line = file.readline()
                    while line:
    #                        readline函数会把'\n'也读进来，去除'\n'
                        para_info = line.strip('\n')
                        para_info_list = para_info.split(',')
                        if not(para_info_list[0] in self.data_dict):
                            if len(para_info_list[1:]) == 0:
                                raise IOError('Unsupported file(FastPlot).')
                            self.data_dict[para_info_list[0]] = para_info_list[1:]
                            data_dict[para_info_list[0]] = para_info_list[1:]
                        else:
                            ex_paras.append(para_info_list[0])
                        line = file.readline()
                if data_dict or ex_paras:
                    self.display_data_dict(data_dict)
                    if ex_paras:
                        print_para = '以下软件标识符已存在：'
                        for pa in ex_paras:
                            print_para += ('<br>' + pa)
                        ms_box = QMessageBox(QMessageBox.Information,
                                             QCoreApplication.translate('DataDictWindow', '导入提示'),
                                             QCoreApplication.translate('DataDictWindow', print_para),
                                             QMessageBox.Ok,
                                             self)
                        ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                        ms_box.exec_()
                else:
                    QMessageBox.information(self,
                                            QCoreApplication.translate('DataDictWindow', '导入提示'),
                                            QCoreApplication.translate('DataDictWindow', '文件中无字典信息！'))
            except:
                QMessageBox.information(self,
                                        QCoreApplication.translate('DataDictWindow', '导入提示'),
                                        QCoreApplication.translate('DataDictWindow', 
                                                                   '''<p><b>文件内容格式不正确！</b></p>
                                                                   <p>1.请按下列格式输入：</p>
                                                                   <br>软件标识符+英文逗号+参数名+英文逗号+单位
                                                                   <p>2.单位输入是必须的，如果参数没单位，请用NaN代替</p>
                                                                   <p>3.示例：</p>
                                                                   <br>FCM1_Vmo,最大使用速度,kn
                                                                   <br>ACE1_STATUS,ACE1状态,NaN'''))
    def slot_close(self):
        
        if self.current_para_change_status:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataDictWindow', '关闭提示'),
                          QCoreApplication.translate('DataDictWindow',
                                                     '字典：' + self.label_symbol.text() + '未保存，是否保存后退出？'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.slot_save()
            else:
                self.slot_cancel()
        self.signal_close_dd_dock.emit()
# =============================================================================
# 功能函数模块
# =============================================================================
#    从文件中加载数据字典进入内存
    def load_data_dict(self):
        
        try:
            with open(CONFIG.SETUP_DIR + r'\data\data_dict.json') as f_obj:
                self.data_dict = json.load(f_obj)
#            with open(CONFIG.SETUP_DIR + r'\data\data_dict.txt', 'r') as file:
#                line = file.readline()
#                if line == 'DataDict\n':
#                    line = file.readline()
#                    while line:
##                        readline函数会把'\n'也读进来，去除'\n'
#                        para_info = line.strip('\n')
#                        para_info_list = para_info.split(',')
#                        if not(para_info_list[0] in self.data_dict):
#                            self.data_dict[para_info_list[0]] = para_info_list[1:]
#                        line = file.readline()
            self.display_data_dict(self.data_dict)
            self.signal_data_dict_changed.emit(self.data_dict)
        except:
            QMessageBox.information(self,
                                    QCoreApplication.translate('DataDictWindow', '提示'),
                                    QCoreApplication.translate('DataDictWindow', '数据字典载入失败！无法使用数据字典'))
        
    def save_data_dict(self):
        
        try:
            with open(CONFIG.SETUP_DIR + r'\data\data_dict.json', 'w') as f_obj:
                json.dump(self.data_dict, f_obj)
        except:
            QMessageBox.information(self,
                                    QCoreApplication.translate('DataDictWindow', '提示'),
                                    QCoreApplication.translate('DataDictWindow', '数据字典保存失败！'))
#    将内存中的数据字典导出到文件
#    def output_data_dict(self):
#
#        try:
##            打开保存模板的文件（将从头写入，覆盖之前的内容）
#            with open(CONFIG.SETUP_DIR + r'\data\data_dict.txt', 'w') as file:
#                file.write('DataDict\n')
##                将内存中的模板一一写入文件
#                for symbol in self.data_dict:
#                    temp = symbol + ','
#                    count = len(self.data_dict[symbol])
#                    for i, info in enumerate(self.data_dict[symbol]):
#                        if i != (count - 1):
#                            temp += info + ','
#                        else:
#                            temp += info
#                    file.write(temp + '\n')
#        except:
#            pass
        
    def display_data_dict(self, data_dict):
        
        if data_dict:
            for symbol in data_dict:
                item = QTreeWidgetItem(self.tree_paras)
                item.setText(0, symbol)
#                item.setIcon(0, QIcon(CONFIG.ICON_PARA))
                if data_dict[symbol][0] != 'NaN':
                    item.setText(1, data_dict[symbol][0])
                else:
                    item.setText(1, '')
                if data_dict[symbol][1] != 'NaN':
                    item.setText(2, data_dict[symbol][1])
                else:
                    
                    item.setText(2, '')
            self.slot_display_para(self.tree_paras.currentItem())
            
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
        self.btn_close.setText(_translate('DataDictWindow', '关闭窗口'))