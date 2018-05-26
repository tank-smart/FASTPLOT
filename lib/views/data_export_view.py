# -*- coding: utf-8 -*-


from PyQt5.QtCore import Qt, QCoreApplication, QSize, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QListWidget, 
                             QListWidgetItem, QSpacerItem, QLineEdit, 
                             QToolButton, QFileDialog, QSizePolicy, 
                             QVBoxLayout,QHBoxLayout)

class DataExport(QWidget):
 
    def __init__(self):
        QWidget.__init__(self)
    
    def setup(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sel_para = QLabel(self)
        self.sel_para.setObjectName("sel_para")
        self.verticalLayout.addWidget(self.sel_para)
        self.sel_para_list = QListWidget(self)
        self.sel_para_list.setObjectName("sel_para_list")
        self.verticalLayout.addWidget(self.sel_para_list)
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
        self.button_cancel = QPushButton(self)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

#        信号与槽进行连接
        self.sel_dir.clicked.connect(self.slot_sel_dir)

        self.retranslateUi()
 
# =============================================================================
# 功能函数
# =============================================================================
    def display_sel_para(self, list_paras):
        if list_paras:
            for paraname in list_paras:
                if (not self.sel_para_list.findItems(paraname, Qt.MatchExactly)):
                    item = QListWidgetItem(self.sel_para_list)
                    item.setText(paraname) 
       
# =============================================================================
# Slots
# =============================================================================
#    让用户选择项目的路径
    def slot_sel_dir(self):
        
        sel_dir = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if sel_dir:
            sel_dir = sel_dir.replace('/','\\')
            self.location_view.setText(sel_dir)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.sel_para.setText(_translate("DataExport", "Selected parameters"))
        self.sel_testpoint.setText(_translate("DataExport", "Select testpoint"))
        self.export_loc.setText(_translate("DataExport", "Export location"))
        self.sel_dir.setText(_translate("DataExport", "..."))
        self.button_confirm.setText(_translate("DataExport", "Confirm"))
        self.button_cancel.setText(_translate("DataExport", "Cancel"))
