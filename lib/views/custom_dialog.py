# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QPushButton, QMessageBox, QListWidget,
                             QListWidgetItem)

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
        self.tempicon = QIcon(r"E:\DAGUI\lib\icon\template.ico")
        self.paraicon = QIcon(r"E:\DAGUI\lib\icon\parameter.png")
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