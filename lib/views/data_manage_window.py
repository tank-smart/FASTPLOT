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
import sys
import os.path as osp
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QSize, QCoreApplication, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QAction,
                             QComboBox, QSpacerItem, QSizePolicy, QFrame, QMenu,
                             QListWidget, QListWidgetItem, QStackedWidget,
                             QLineEdit, QAbstractItemView, QGroupBox,
                             QMessageBox, QDialogButtonBox)

import views.constant as CONSTANT

# =============================================================================
# DataManageWindow
# =============================================================================
class DataManageWindow(QWidget):

    signal_display_paras_template = pyqtSignal()
    signal_display_plot_template = pyqtSignal()
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
#        导出参数的模板
        self.paras_temps = {}
#        绘图的模板
        self.plot_temps = {}
        
        self.tempicon = QIcon(CONSTANT.ICON_TEMPLATE)
        self.paraicon = QIcon(CONSTANT.ICON_PARA)
        
        self.SETUP_DIR = osp.abspath(osp.join(osp.dirname(sys.argv[0]), osp.pardir))

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):

        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_manage_type = QLabel(self)
        self.label_manage_type.setMinimumSize(QSize(100, 24))
        self.label_manage_type.setMaximumSize(QSize(100, 24))
        self.label_manage_type.setObjectName("label_manage_type")
        self.horizontalLayout.addWidget(self.label_manage_type)
        self.comboBox_manage_type = QComboBox(self)
        self.comboBox_manage_type.setMinimumSize(QSize(120, 24))
        self.comboBox_manage_type.setMaximumSize(QSize(120, 24))
        self.comboBox_manage_type.setObjectName("comboBox_manage_type")
        self.comboBox_manage_type.addItem("")
        self.comboBox_manage_type.addItem("")
        self.comboBox_manage_type.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_manage_type)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_para_templates = QWidget()
        self.page_para_templates.setObjectName("page_para_templates")
        self.horizontalLayout_2 = QHBoxLayout(self.page_para_templates)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.group_box_templates = QGroupBox(self.page_para_templates)
        self.group_box_templates.setObjectName("group_box_templates")
        self.verticalLayout = QVBoxLayout(self.group_box_templates)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.list_para_templates = QListWidget(self.group_box_templates)
        self.list_para_templates.setObjectName("list_para_templates")
        self.verticalLayout.addWidget(self.list_para_templates)
        self.horizontalLayout_2.addWidget(self.group_box_templates)
        self.group_box_template_setting = QGroupBox(self.page_para_templates)
        self.group_box_template_setting.setObjectName("group_box_template_setting")
        self.verticalLayout_2 = QVBoxLayout(self.group_box_template_setting)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_para_template = QLabel(self.group_box_template_setting)
        self.label_para_template.setMinimumSize(QSize(0, 24))
        self.label_para_template.setMaximumSize(QSize(16777215, 24))
        self.label_para_template.setObjectName("label_para_template")
        self.verticalLayout_2.addWidget(self.label_para_template)
        self.line_edit_paras_template_name = QLineEdit(self.group_box_template_setting)
        self.line_edit_paras_template_name.setMinimumSize(QSize(0, 24))
        self.line_edit_paras_template_name.setMaximumSize(QSize(16777215, 24))
        self.line_edit_paras_template_name.setObjectName("line_edit_paras_template_name")
        self.verticalLayout_2.addWidget(self.line_edit_paras_template_name)
        self.label_parameters = QLabel(self.group_box_template_setting)
        self.label_parameters.setMinimumSize(QSize(0, 24))
        self.label_parameters.setMaximumSize(QSize(16777215, 24))
        self.label_parameters.setObjectName("label_parameters")
        self.verticalLayout_2.addWidget(self.label_parameters)
        self.list_parameters_for_ana = QListWidget(self.group_box_template_setting)
        self.list_parameters_for_ana.setObjectName("list_parameters_for_ana")
        self.verticalLayout_2.addWidget(self.list_parameters_for_ana)
        self.btn_box_para_template = QDialogButtonBox(self.group_box_template_setting)
        self.btn_box_para_template.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.btn_box_para_template.setObjectName("btn_box_para_template")
        self.verticalLayout_2.addWidget(self.btn_box_para_template)
        self.horizontalLayout_2.addWidget(self.group_box_template_setting)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 5)
        self.stackedWidget.addWidget(self.page_para_templates)
        self.page_plot_templates = QWidget()
        self.page_plot_templates.setObjectName("page_plot_templates")
        self.stackedWidget.addWidget(self.page_plot_templates)
        self.page_parametes_dict = QWidget()
        self.page_parametes_dict.setObjectName("page_parametes_dict")
        self.stackedWidget.addWidget(self.page_parametes_dict)
        self.verticalLayout_3.addWidget(self.stackedWidget)

        self.retranslateUi()
#        加载模板
        self.load_temps()
        self.stackedWidget.setCurrentIndex(0)

#        设置每个item是可以被选择的
        self.list_para_templates.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        
#       让树可支持右键菜单(step 1)
        self.list_para_templates.setContextMenuPolicy(Qt.CustomContextMenu)
      
#        添加右键动作
        self.action_delete_templates = QAction(self.list_para_templates)
        self.action_delete_templates.setText(QCoreApplication.
                                             translate('ParalistDock', '删除模板'))

# =======连接信号与槽
# =============================================================================        
        self.comboBox_manage_type.currentIndexChanged.connect(self.slot_show_page)
        self.list_para_templates.itemClicked.connect(self.slot_display_template)
        
#        使右键时能弹出菜单(step 2)
        self.list_para_templates.customContextMenuRequested.connect(
                self.on_list_para_templates_menu)
        self.action_delete_templates.triggered.connect(self.slot_delete_templates)
        

# =============================================================================
# slots模块
# =============================================================================
#    右键菜单的事件处理(step 3)
    def on_list_para_templates_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.list_para_templates.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self.list_para_templates)
            menu.addActions([self.action_delete_templates])
            
            menu.exec_(self.list_para_templates.mapToGlobal(pos))
            
    def slot_show_page(self, index):
        
        self.stackedWidget.setCurrentIndex(index)
    
#    直接覆盖同名的模板,当分析参数窗口保存模板时触发
    def slot_add_para_template(self, template : dict):
        
        if template:
            for name in template:
                self.paras_temps[name] = template[name]
                self.redisplay_para_templates()
                
    def slot_add_plot_template(self, template : dict):
        
        if template:
            for name in template:
                self.plot_temps[name] = template[name]

#    显示模板信息
    def slot_display_template(self, item):

        self.list_parameters_for_ana.clear()
        self.line_edit_paras_template_name.clear()
#        显示参数列表
        for paraname in self.paras_temps[item.text()]:
            QListWidgetItem(paraname, self.list_parameters_for_ana).setIcon(self.paraicon)
#        显示模板名
        self.line_edit_paras_template_name.setText(item.text())
    
#    删除模板    
    def slot_delete_templates(self):
        
        sel_items = self.list_para_templates.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataExportWindow', '删除模板'),
                          QCoreApplication.translate('DataExportWindow', '确定要删除这些模板吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_para_templates.takeItem(self.list_para_templates.row(item))
                    self.paras_temps.pop(item.text())
#                如果删除完模板后，还有模板就显示第一个模板的信息
                if self.paras_temps:
                    self.list_para_templates.setCurrentRow(0)
                    self.slot_display_template(self.list_para_templates.currentItem())
        
            
# =============================================================================
# 功能函数模块
# =============================================================================
#    从文件中加载参数模板进入内存
    def load_temps(self):
        
#        导入导出参数的模板
        try:
            with open(self.SETUP_DIR + r'\data\templates_export_paras.txt', 'r') as file:
                while file.readline():
    #                readline函数会把'\n'也读进来
                     name = file.readline()
    #                 去除'\n'
                     name = name.strip('\n')
                     str_paralist = file.readline()
                     str_paralist = str_paralist.strip('\n')
                     paralist = str_paralist.split(' ')
                     self.paras_temps[name] = paralist
        except IOError:
#            对抛出的文件错误，不予理睬
            pass
        self.redisplay_para_templates()            
        
#        导入绘图模板
        try:
            with open(self.SETUP_DIR + r'\data\templates_plot.txt', 'r') as file:
                while file.readline():
    #                readline函数会把'\n'也读进来
                     name = file.readline()
    #                 去除'\n'
                     name = name.strip('\n')
                     str_paralist = file.readline()
                     str_paralist = str_paralist.strip('\n')
                     paralist = str_paralist.split(' ')
                     self.plot_temps[name] = paralist
        except IOError:
            pass
        
#    将内存中的模板导出到文件
    def output_temps(self):

#        判断是否有模板存在
        if self.paras_temps:
#                打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(self.SETUP_DIR + r'\data\templates_export_paras.txt', 'w') as file:
#                将内存中的模板一一写入文件
                for temp in self.paras_temps:
                    file.write('========\n')
                    file.write(temp)
                    file.write('\n')
                    paralist = ''
                    index = 1
                    length = len(self.paras_temps[temp])
                    for para in self.paras_temps[temp]:
                        if index == length:
                            paralist += (para + '\n')
                        else:
                            paralist += (para + ' ')
                        index += 1
                    file.write(paralist)
                    
#        判断是否有模板存在
        if self.plot_temps:
#                打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(self.SETUP_DIR + r'\data\templates_plot.txt', 'w') as file:
#                将内存中的模板一一写入文件
                for temp in self.plot_temps:
                    file.write('========\n')
                    file.write(temp)
                    file.write('\n')
                    paralist = ''
                    index = 1
                    length = len(self.plot_temps[temp])
                    for para in self.plot_temps[temp]:
                        if index == length:
                            paralist += (para + '\n')
                        else:
                            paralist += (para + ' ')
                        index += 1
                    file.write(paralist)
                    
#    更新模板显示
    def redisplay_para_templates(self):

#        显示模板信息
        if self.paras_temps:
            self.list_para_templates.clear()
#            显示模板列表
            for name in self.paras_temps:
                QListWidgetItem(name, self.list_para_templates).setIcon(self.tempicon)
#            设置当前的模板为第一个模板并显示模板信息
            self.list_para_templates.setCurrentRow(0)
            item = self.list_para_templates.currentItem()
            self.slot_display_template(item)
# =============================================================================
# 汉化
# =============================================================================
    
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label_manage_type.setText(_translate("DataManageWindow", "数据管理类型"))
        self.comboBox_manage_type.setItemText(0, _translate("DataManageWindow", "参数模板"))
        self.comboBox_manage_type.setItemText(1, _translate("DataManageWindow", "绘图模板"))
        self.comboBox_manage_type.setItemText(2, _translate("DataManageWindow", "参数字典"))
        self.group_box_templates.setTitle(_translate("DataManageWindow", "模板列表"))
        self.group_box_template_setting.setTitle(_translate("DataManageWindow", "模板信息"))
        self.label_para_template.setText(_translate("DataManageWindow", "模板名"))
        self.label_parameters.setText(_translate("DataManageWindow", "参数列表"))