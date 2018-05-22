# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-20
# 编码人员：王学良
# 简述：新建项目时的对话框
#
# =======使用说明
# 。。。
#
# =======日志
# 1.2018-05-20 王学良创建文件
# =============================================================================

import os

from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QToolButton,
                             QFileDialog, QDialogButtonBox, QMessageBox, 
                             QSizePolicy, QVBoxLayout, QHBoxLayout)

class NewProjectDialog(QDialog):
    
    #此处定义常量
    
    #此处定义信号

    def __init__(self):
        QDialog.__init__(self)
        self.project_dir = None
        self.project_name = None
        
    def setup(self):
        self.resize(450, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_project_name = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_project_name.sizePolicy().hasHeightForWidth())
        self.label_project_name.setSizePolicy(sizePolicy)
        self.label_project_name.setMinimumSize(QSize(80, 24))
        self.label_project_name.setMaximumSize(QSize(80, 24))
        self.label_project_name.setObjectName("label_project_name")
        self.horizontalLayout.addWidget(self.label_project_name)
        self.lineEdit_project_name = QLineEdit(self)
        self.lineEdit_project_name.setObjectName("lineEdit_project_name")
        self.horizontalLayout.addWidget(self.lineEdit_project_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_location = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_location.sizePolicy().hasHeightForWidth())
        self.label_location.setSizePolicy(sizePolicy)
        self.label_location.setMinimumSize(QSize(80, 24))
        self.label_location.setMaximumSize(QSize(80, 24))
        self.label_location.setObjectName("label_location")
        self.horizontalLayout_2.addWidget(self.label_location)
        self.lineEdit_location = QLineEdit(self)
        self.lineEdit_location.setObjectName("lineEdit_location")
        self.lineEdit_location.setReadOnly(True)
        self.lineEdit_location.setText(os.getcwd())
        self.horizontalLayout_2.addWidget(self.lineEdit_location)
        self.toolbutton_open = QToolButton(self)
        self.toolbutton_open.setMinimumSize(QSize(24, 24))
        self.toolbutton_open.setMaximumSize(QSize(24, 24))
        self.toolbutton_open.setObjectName("toolbutton_open")
        self.horizontalLayout_2.addWidget(self.toolbutton_open)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        
#        给项目路径和项目赋初值
        self.project_dir = self.lineEdit_location.text()
        self.project_name = self.lineEdit_project_name.text()
#        信号与槽进行连接
        self.buttonBox.accepted.connect(self.slot_accept)
        self.buttonBox.rejected.connect(self.reject)
        self.toolbutton_open.clicked.connect(self.slot_open)
        self.lineEdit_project_name.textChanged.connect(self.slot_set_dir)
        QMetaObject.connectSlotsByName(self)

    def get_project_info(self):
        self.setup()
        flag = self.exec_()
        if (flag == QDialog.Accepted):
#            返回一个元组，包含路径和项目名
            return (self.project_dir, 
                    self.project_name)
        else:
            return (None, None)  

# =============================================================================
# Slots
# =============================================================================
#    让用户选择项目的路径
    def slot_open(self):
        
        sel_dir = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if sel_dir:
            sel_dir = sel_dir.replace('/','\\')
            self.project_dir = sel_dir
            if self.project_name:
                self.lineEdit_location.setText(self.project_dir + '\\' +
                                           self.project_name)
            else:
                self.lineEdit_location.setText(self.project_dir)

#    自定义一个接受的事件，需要判断用户是否已完成项目的创建
    def slot_accept(self):
        
        if (self.project_dir and self.project_name):
            self.accept()
        else:
            tipDialog = QMessageBox(self)
            tipDialog.resize(300,100)
            tipDialog.setWindowTitle("Caution")
            tipDialog.setText("You have not created a project yet!")
            tipDialog.exec_()

    def slot_set_dir(self):

#        这里还应该判断用户输入正确的项目名字符串        
        self.project_name = self.lineEdit_project_name.text()
        if self.project_name:
            self.lineEdit_location.setText(self.project_dir + '\\' +
                                       self.project_name)
        else:
            self.lineEdit_location.setText(self.project_dir)
                
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("NewProjectDialog", "创建新项目"))
        self.label_project_name.setText(_translate("NewProjectDialog", "项目名"))
        self.label_location.setText(_translate("NewProjectDialog", "路径"))
        self.toolbutton_open.setText(_translate("NewProjectDialog", "..."))
        
#    def retranslateUi(self):
#        _translate = QCoreApplication.translate
#        self.setWindowTitle(_translate("NewProjectDialog", "Create new project"))
#        self.label_project_name.setText(_translate("NewProjectDialog", "Project name"))
#        self.label_location.setText(_translate("NewProjectDialog", "Location"))
#        self.toolbutton_open.setText(_translate("NewProjectDialog", "..."))