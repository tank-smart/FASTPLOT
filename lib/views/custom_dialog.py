# -*- coding: utf-8 -*-
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QSize, QCoreApplication, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QPushButton, QMessageBox, QListWidget,
                             QListWidgetItem, QToolButton, QFrame, 
                             QAbstractItemView, QApplication)

# =============================================================================
# Package models imports
# =============================================================================
from models.datafile_model import Normal_DataFile
import views.src_icon as ICON

import sys, re

class SaveTemplateDialog(QDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.setup()
        self.temp_name = ''
    
    def setup(self):
        
        font = QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.resize(400, 80)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self)
        self.label.setMinimumSize(QSize(0, 24))
        self.label.setMaximumSize(QSize(16777215, 24))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMinimumSize(QSize(0, 24))
        self.line_edit_name.setMaximumSize(QSize(16777215, 24))
        self.line_edit_name.setObjectName("line_edit_name")
        self.horizontalLayout.addWidget(self.line_edit_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setObjectName("button_confirm")
        self.horizontalLayout_2.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
        self.button_cancel.setObjectName("button_cancle")
        self.horizontalLayout_2.addWidget(self.button_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi()
        
        self.button_cancel.clicked.connect(self.reject)
        self.button_confirm.clicked.connect(self.accept)

    def accept(self):
        
        self.temp_name = self.line_edit_name.text()
        if self.temp_name:
            QDialog.accept(self)
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate("SaveTemplateDialog", "输入提示"),
                    QCoreApplication.translate("SaveTemplateDialog", "未输入模板名"))
    
    def retranslateUi(self):
        
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SaveTemplateDialog", "模板名称"))
        self.label.setText(_translate("SaveTemplateDialog", "模板名称"))
        self.button_confirm.setText(_translate("SaveTemplateDialog", "确定"))
        self.button_cancel.setText(_translate("SaveTemplateDialog", "取消"))


class SelectTemplateDialog(QDialog):
    
    def __init__(self, parent = None, templates = {}):
        
        super().__init__(parent)
        self.templates = templates
        self.sel_temp = ''
        self.tempicon = QIcon(ICON.ICON_TEMPLATE)
        self.paraicon = QIcon(ICON.ICON_PARA)
        self.setup()
    
    def setup(self):

        font = QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.resize(580, 450)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(4, 0, 4, 4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_temp = QLabel(self)
        self.label_temp.setMinimumSize(QSize(0, 24))
        self.label_temp.setMaximumSize(QSize(16777215, 24))
        self.label_temp.setObjectName("label_temp")
        self.verticalLayout.addWidget(self.label_temp)
        self.list_temps = QListWidget(self)
        self.list_temps.setObjectName("list_temps")
        self.verticalLayout.addWidget(self.list_temps)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_para = QLabel(self)
        self.label_para.setMinimumSize(QSize(0, 24))
        self.label_para.setMaximumSize(QSize(16777215, 24))
        self.label_para.setObjectName("label_para")
        self.verticalLayout_2.addWidget(self.label_para)
        self.list_paras = QListWidget(self)
        self.list_paras.setObjectName("list_paras")
        self.verticalLayout_2.addWidget(self.list_paras)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setObjectName("button_confirm")
        self.horizontalLayout.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.button_cancel.clicked.connect(self.reject)
        self.button_confirm.clicked.connect(self.accept)
        self.list_temps.itemClicked.connect(self.slot_display_paras)
        
        self.retranslateUi()
        self.display_templates(self.templates)

    def accept(self):
        
        item = self.list_temps.currentItem()
        self.sel_temp = item.text()
        QDialog.accept(self)
    
    def slot_display_paras(self, item):
        
        name = item.text()
        self.list_paras.clear()
        for paraname in self.templates[name]:
            QListWidgetItem(paraname, self.list_paras).setIcon(self.paraicon)
        
    
    def display_templates(self, templates):
        
        flag = True
        if templates:
            for name in templates:
                QListWidgetItem(name, self.list_temps).setIcon(self.tempicon)
                if flag:
                    for paraname in templates[name]:
                        QListWidgetItem(paraname, self.list_paras).setIcon(self.paraicon)
                    flag = False
                    
            self.list_temps.setCurrentRow(0)


    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SelectTemplateself", "选择模板"))
        self.label_temp.setText(_translate("SelectTemplateself", "模板列表"))
        self.label_para.setText(_translate("SelectTemplateself", "参数列表"))
        self.button_confirm.setText(_translate("SelectTemplateself", "确认"))
        self.button_cancel.setText(_translate("SelectTemplateself", "取消"))
        

class SelParaForPlotDialog(QDialog):

    signal_para_for_plot = pyqtSignal(tuple)
    signal_close = pyqtSignal()
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.setup()
        self.paraicon = QIcon(ICON.ICON_PARA)
        
    def setup(self):

        font = QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.resize(400, 350)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_up = QToolButton(self)
        self.button_up.setIcon(QIcon(ICON.ICON_UP))
        self.button_up.setMinimumSize(QSize(24, 24))
        self.button_up.setMaximumSize(QSize(24, 24))
        self.button_up.setObjectName("button_up")
        self.horizontalLayout.addWidget(self.button_up)
        self.button_down = QToolButton(self)
        self.button_down.setIcon(QIcon(ICON.ICON_DOWN))
        self.button_down.setMinimumSize(QSize(24, 24))
        self.button_down.setMaximumSize(QSize(24, 24))
        self.button_down.setObjectName("button_down")
        self.horizontalLayout.addWidget(self.button_down)
        self.button_delete = QToolButton(self)
        self.button_delete.setIcon(QIcon(ICON.ICON_DEL))
        self.button_delete.setMinimumSize(QSize(24, 24))
        self.button_delete.setMaximumSize(QSize(24, 24))
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.list_paras = QListWidget(self)
        self.list_paras.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        self.list_paras.setObjectName("list_paras")
        self.verticalLayout.addWidget(self.list_paras)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setMinimumSize(QSize(0, 24))
        self.button_confirm.setMaximumSize(QSize(16777215, 24))
        self.button_confirm.setObjectName("button_confirm")
        self.horizontalLayout_2.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
        self.button_cancel.setMinimumSize(QSize(0, 24))
        self.button_cancel.setMaximumSize(QSize(16777215, 24))
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout_2.addWidget(self.button_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi()
        
        self.button_confirm.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)
        self.button_up.clicked.connect(self.slot_up_para)
        self.button_down.clicked.connect(self.slot_down_para)
        self.button_delete.clicked.connect(self.slot_delete_paras)
        
    def accept(self):
        
        self.signal_para_for_plot.emit(self.get_sel_paras())
        QDialog.accept(self)
        self.signal_close.emit()
        
    def reject(self):
        
        QDialog.reject(self)
        self.signal_close.emit()        
    
    def slot_import_para(self, paras_dict):
        
        if paras_dict:
            ex_paras = []
            for file_dir in paras_dict:
                ex_paras += self.add_file_para(file_dir,
                                               paras_dict[file_dir])
            if ex_paras:
                print_para = "<br>以下参数已存在："
                for pa in ex_paras:
                    print_para += ("<br>" + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate("DataExportWindow", "导入提示"),
                        QCoreApplication.translate("DataExportWindow",
                                                   print_para))
                
    def slot_up_para(self):
        
        if self.list_paras:
            loc = self.list_paras.currentRow()
            item = self.list_paras.takeItem(loc)
            if loc == 0:
                self.list_paras.insertItem(0, item)
                self.list_paras.setCurrentItem(item)
            else:
                self.list_paras.insertItem(loc - 1, item)
                self.list_paras.setCurrentItem(item)
    
    def slot_down_para(self):

        if self.list_paras:
            count = self.list_paras.count()
            loc = self.list_paras.currentRow()
            item = self.list_paras.takeItem(loc)
            if loc == count:
                self.list_paras.insertItem(count, item)
                self.list_paras.setCurrentItem(item)
            else:
                self.list_paras.insertItem(loc + 1, item)
                self.list_paras.setCurrentItem(item)
                
    def slot_delete_paras(self):
        
        sel_items = self.list_paras.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate("DataExportWindow", "删除参数"),
                          QCoreApplication.translate("DataExportWindow", "确定要删除这些参数吗"),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_paras.takeItem(self.list_paras.row(item))

#    只要参数名一致就认为在这个参数列表中，不区分是否是在不同文件
    def is_in_sel_paras(self, para):

        count = self.list_paras.count()
        for i in range(count):
            item = self.list_paras.item(i)
            paraname = item.text()
            if para == paraname:
                return True
        return False
                
#    将此文件中的参数加入到列表中
    def add_file_para(self, file_dir, paras):

#        返回已存在的参数
        ex_paras = []
        for para in paras:
#            判断导入的参数是否已存在
            if self.is_in_sel_paras(para):
                ex_paras.append(para)
            else:
                item_para = QListWidgetItem(para, self.list_paras)
                item_para.setIcon(self.paraicon)
                item_para.setData(Qt.UserRole, file_dir)
        return ex_paras
    
    def get_sel_paras(self):
        
        result = {}
        sorted_paras = []
        if self.list_paras:
            count = self.list_paras.count()
            for i in range(count):
                item = self.list_paras.item(i)
                sorted_paras.append(item.text())
                file_dir = item.data(Qt.UserRole)
                if file_dir in result:
                    result[file_dir].append(item.text())
                else:
                    result[file_dir] = []
                    result[file_dir].append(item.text())
        return (result, sorted_paras)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SelParaForPlot", "绘图参数"))
        self.button_up.setText(_translate("SelParaForPlot", "上移"))
        self.button_down.setText(_translate("SelParaForPlot", "下移"))
        self.button_delete.setText(_translate("SelParaForPlot", "删除"))
        self.button_confirm.setText(_translate("SelParaForPlot", "确定"))
        self.button_cancel.setText(_translate("SelParaForPlot", "取消"))

class SelParasDialog(QDialog):

    signal_add_paras = pyqtSignal()
    
    def __init__(self, parent = None, files = [], sel_mode = 0):
        
        super().__init__(parent)
        self.paraicon = QIcon(ICON.ICON_PARA)
        if sel_mode == 0:
            self.sel_mode = QAbstractItemView.SingleSelection
        if sel_mode == 1:
            self.sel_mode = QAbstractItemView.ExtendedSelection
        self.setup()
        self.display_paras(files)

    def setup(self):

        font = QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.resize(260, 550)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_edit_search = QLineEdit(self)
        self.line_edit_search.setMinimumSize(QSize(0, 24))
        self.line_edit_search.setMaximumSize(QSize(16777215, 24))
        self.line_edit_search.setObjectName("line_edit_search")
        self.verticalLayout.addWidget(self.line_edit_search)
        self.list_paras = QListWidget(self)
        self.list_paras.setSelectionMode(self.sel_mode)
        self.list_paras.setObjectName("list_paras")
        self.verticalLayout.addWidget(self.list_paras)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout.addWidget(self.btn_confirm)
        if self.sel_mode == QAbstractItemView.ExtendedSelection:
            self.btn_add = QPushButton(self)
            self.btn_add.setMinimumSize(QSize(0, 24))
            self.btn_add.setMaximumSize(QSize(16777215, 24))
            self.btn_add.setObjectName("btn_add")
            self.horizontalLayout.addWidget(self.btn_add)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
        
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        if self.sel_mode == QAbstractItemView.ExtendedSelection:
            self.btn_add.clicked.connect(self.signal_add_paras)
        if self.sel_mode == QAbstractItemView.SingleSelection:
            self.list_paras.itemDoubleClicked.connect(self.accept)
        self.line_edit_search.textChanged.connect(self.slot_search_para)
    
    def slot_search_para(self, para_name):
        
        if self.list_paras:
            pattern = re.compile('.*' + para_name + '.*')
            count = self.list_paras.count()
            for i in range(count):
                item = self.list_paras.item(i)
                paraname = item.text()
                if re.match(pattern, paraname):
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def get_list_sel_paras(self):
        
        list_paras = []
        for item in self.list_paras.selectedItems():
            list_paras.append(item.text())
        return list_paras
        
#    不显示时间
    def display_paras(self, files):
        
        for file_dir in files:
            time_hide = False
            file = Normal_DataFile(file_dir)
            paras = file.paras_in_file
            for para in paras:
                if time_hide:
                    if para not in self.get_list_paras():
                        item = QListWidgetItem(para, self.list_paras)
                        item.setIcon(self.paraicon)
#                跳过第一个参数，这里默认第一个参数时间
                else:
                    time_hide = True
    
    def get_list_paras(self):
        
        list_paras = []
        count = self.list_paras.count()
        for i in range(count):
            item = self.list_paras.item(i)
            list_paras.append(item.text())
        return list_paras

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SelParasDialog", "选择参数"))
        self.line_edit_search.setPlaceholderText(_translate("SelParasDialog", "过滤器"))
        self.btn_confirm.setText(_translate("SelParasDialog", "确认"))
        if self.sel_mode == QAbstractItemView.ExtendedSelection:
            self.btn_add.setText(_translate("SelParasDialog", "添加"))
        self.btn_cancel.setText(_translate("SelParasDialog", "取消"))

#测试用     
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    d = SelParaForPlotDialog()
    d.slot_import_para({'E:\\ss' : ['A', 'B'],
                        'E:\\dd' : ['C']})
    d.show()
    app.exec_()