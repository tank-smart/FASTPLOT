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
# Qt imports
# =============================================================================
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpacerItem, QSizePolicy, QFrame,
                             QListWidget, QStackedWidget, QLineEdit,
                             QPushButton)

# =============================================================================
# DataManageWindow
# =============================================================================
class DataManageWindow(QWidget):

# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(4, 4, 4, 0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_datatype = QLabel(self)
        self.label_datatype.setMinimumSize(QSize(80, 24))
        self.label_datatype.setMaximumSize(QSize(80, 24))
        self.label_datatype.setObjectName("label_datatype")
        self.horizontalLayout.addWidget(self.label_datatype)
        self.combobox_index = QComboBox(self)
        self.combobox_index.setMinimumSize(QSize(120, 24))
        self.combobox_index.setMaximumSize(QSize(120, 24))
        self.combobox_index.setObjectName("combobox_index")
        self.combobox_index.addItem("")
        self.combobox_index.addItem("")
        self.combobox_index.addItem("")
        self.horizontalLayout.addWidget(self.combobox_index)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QWidget(self)
        self.widget.setMinimumSize(QSize(220, 0))
        self.widget.setMaximumSize(QSize(220, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout_temp = QVBoxLayout(self.widget)
        self.verticalLayout_temp.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_temp.setSpacing(4)
        self.verticalLayout_temp.setObjectName("verticalLayout_temp")
        self.label_templist = QLabel(self.widget)
        self.label_templist.setMinimumSize(QSize(60, 24))
        self.label_templist.setMaximumSize(QSize(60, 24))
        self.label_templist.setObjectName("label_templist")
        self.verticalLayout_temp.addWidget(self.label_templist)
        self.list_templates = QListWidget(self)
        self.list_templates.setMinimumSize(QSize(220, 0))
        self.list_templates.setMaximumSize(QSize(220, 16777215))
        self.list_templates.setObjectName("list_templates")
        self.verticalLayout_temp.addWidget(self.list_templates)
        self.horizontalLayout_2.addWidget(self.widget)
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
        
#        参数导出模板编辑页
        self.export_temp_page = QWidget()
        self.export_temp_page.setObjectName("page")
        self.horizontalLayout_5 = QHBoxLayout(self.export_temp_page)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_temp_name_export = QLabel(self.export_temp_page)
        self.label_temp_name_export.setMinimumSize(QSize(0, 24))
        self.label_temp_name_export.setMaximumSize(QSize(16777215, 24))
        self.label_temp_name_export.setObjectName("label_temp_name_export")
        self.verticalLayout_2.addWidget(self.label_temp_name_export)
        self.line_edit_temp_name_export = QLineEdit(self.export_temp_page)
        self.line_edit_temp_name_export.setMinimumSize(QSize(0, 24))
        self.line_edit_temp_name_export.setMaximumSize(QSize(16777215, 24))
        self.line_edit_temp_name_export.setObjectName("line_edit_temp_name_export")
        self.verticalLayout_2.addWidget(self.line_edit_temp_name_export)
        self.label_paralist_export = QLabel(self.export_temp_page)
        self.label_paralist_export.setMinimumSize(QSize(0, 24))
        self.label_paralist_export.setMaximumSize(QSize(16777215, 24))
        self.label_paralist_export.setObjectName("label_paralist_export")
        self.verticalLayout_2.addWidget(self.label_paralist_export)
        self.list_paralist_export = QListWidget(self.export_temp_page)
        self.list_paralist_export.setObjectName("list_paralist_export")
        self.verticalLayout_2.addWidget(self.list_paralist_export)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.button_save_export = QPushButton(self.export_temp_page)
        self.button_save_export.setMinimumSize(QSize(0, 24))
        self.button_save_export.setMaximumSize(QSize(16777215, 24))
        self.button_save_export.setObjectName("button_save_export")
        self.horizontalLayout_3.addWidget(self.button_save_export)
        self.button_cancel_export = QPushButton(self.export_temp_page)
        self.button_cancel_export.setMinimumSize(QSize(0, 24))
        self.button_cancel_export.setMaximumSize(QSize(16777215, 24))
        self.button_cancel_export.setObjectName("button_cancel_export")
        self.horizontalLayout_3.addWidget(self.button_cancel_export)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.stackedWidget.addWidget(self.export_temp_page)
        
#        绘图模板编辑页
        self.plot_temp_page = QWidget()
        self.plot_temp_page.setObjectName("page_2")
        self.horizontalLayout_6 = QHBoxLayout(self.plot_temp_page)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QLabel(self.plot_temp_page)
        self.label_5.setMinimumSize(QSize(0, 24))
        self.label_5.setMaximumSize(QSize(16777215, 24))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.line_edit_temp_name_plot = QLineEdit(self.plot_temp_page)
        self.line_edit_temp_name_plot.setMinimumSize(QSize(0, 24))
        self.line_edit_temp_name_plot.setMaximumSize(QSize(16777215, 24))
        self.line_edit_temp_name_plot.setObjectName("line_edit_temp_name_plot")
        self.verticalLayout_4.addWidget(self.line_edit_temp_name_plot)
        self.label_4 = QLabel(self.plot_temp_page)
        self.label_4.setMinimumSize(QSize(0, 24))
        self.label_4.setMaximumSize(QSize(16777215, 24))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.list_paralist_plot = QListWidget(self.plot_temp_page)
        self.list_paralist_plot.setObjectName("list_paralist_plot")
        self.verticalLayout_4.addWidget(self.list_paralist_plot)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.button_save_plot = QPushButton(self.plot_temp_page)
        self.button_save_plot.setMinimumSize(QSize(0, 24))
        self.button_save_plot.setMaximumSize(QSize(16777215, 24))
        self.button_save_plot.setObjectName("button_save_plot")
        self.horizontalLayout_4.addWidget(self.button_save_plot)
        self.button_cancel_plot = QPushButton(self.plot_temp_page)
        self.button_cancel_plot.setMinimumSize(QSize(0, 24))
        self.button_cancel_plot.setMaximumSize(QSize(16777215, 24))
        self.button_cancel_plot.setObjectName("button_cancel_plot")
        self.horizontalLayout_4.addWidget(self.button_cancel_plot)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.stackedWidget.addWidget(self.plot_temp_page)
        
#        参数字典编辑页
        self.para_dictionary_page = QWidget()
        self.stackedWidget.addWidget(self.para_dictionary_page)
        
        self.horizontalLayout_2.addWidget(self.stackedWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)

# =======连接信号与槽
# =============================================================================        
        self.combobox_index.currentIndexChanged.connect(self.slot_show_page)

# =============================================================================
# slots模块
# =============================================================================
    def slot_show_page(self, index):
        
        self.stackedWidget.setCurrentIndex(index)



# =============================================================================
# 功能函数模块
# =============================================================================

# =============================================================================
# 汉化
# =============================================================================
    
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label_datatype.setText(_translate("DataManageWindow", "数据管理对象"))
        self.combobox_index.setItemText(0, _translate("DataManageWindow", "参数导出模板"))
        self.combobox_index.setItemText(1, _translate("DataManageWindow", "绘图模板"))
        self.combobox_index.setItemText(2, _translate("DataManageWindow", "参数字典"))
        self.label_templist.setText(_translate("Form", "模板列表"))
        self.label_temp_name_export.setText(_translate("DataManageWindow", "模板名"))
        self.label_paralist_export.setText(_translate("DataManageWindow", "参数列表"))
        self.button_save_export.setText(_translate("DataManageWindow", "保存"))
        self.button_cancel_export.setText(_translate("DataManageWindow", "取消"))
        self.label_5.setText(_translate("DataManageWindow", "模板名"))
        self.label_4.setText(_translate("DataManageWindow", "参数列表"))
        self.button_save_plot.setText(_translate("DataManageWindow", "保存"))
        self.button_cancel_plot.setText(_translate("DataManageWindow", "取消"))