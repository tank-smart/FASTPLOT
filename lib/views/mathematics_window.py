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
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QMenu, QAction,
                             QTreeWidgetItem, QGroupBox, QAbstractItemView,
                             QHeaderView, QMessageBox)
# =============================================================================
# Package views imports
# =============================================================================
from models.mathematics_model import MathematicsEditor
import views.constant as CONSTANT
from models.data_model import DataFactory

class MathematicsWindow(QWidget):
    
    signal_plot_result_para = pyqtSignal(tuple)
    signal_sendto_ananlysis = pyqtSignal(dict)
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self._current_files = []
        self.dict_result_paras = {}
        self.count_created_result = 0
        self.math_result_icon = QIcon(CONSTANT.ICON_MATH_RESULT)
        
    def setup(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.group_box_commandline = QGroupBox(self)
        self.verticalLayout_1 = QVBoxLayout(self.group_box_commandline)
        self.verticalLayout_1.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_1.setSpacing(2)
        self.plain_text_edit_conmandline = MathematicsEditor(self.group_box_commandline)
        self.verticalLayout_1.addWidget(self.plain_text_edit_conmandline)
        self.verticalLayout.addWidget(self.group_box_commandline)
        self.group_box_result_paras = QGroupBox(self)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_result_paras)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.tree_widget_result_paras = QTreeWidget(self.group_box_result_paras)
        self.tree_widget_result_paras.setRootIsDecorated(False)

#        设置树组件头部显示方式
        headerview = self.tree_widget_result_paras.header()
        headerview.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerview.setMinimumSectionSize(100)
        self.tree_widget_result_paras.setHeader(headerview)
        
        self.tree_widget_result_paras.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
        
        self.tree_widget_result_paras.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_plot = QAction(self.tree_widget_result_paras)
        self.action_plot.setText(QCoreApplication.
                                 translate('MathematicsWindow', '绘图'))
        self.action_export = QAction(self.tree_widget_result_paras)
        self.action_export.setText(QCoreApplication.
                                   translate('MathematicsWindow', '导出'))
        self.action_analysis = QAction(self.tree_widget_result_paras)
        self.action_analysis.setText(QCoreApplication.
                                     translate('MathematicsWindow', '添加到分析参数'))
        self.action_delete = QAction(self.tree_widget_result_paras)
        self.action_delete.setText(QCoreApplication.
                                   translate('MathematicsWindow', '删除'))
        
        self.verticalLayout_2.addWidget(self.tree_widget_result_paras)
        self.verticalLayout.addWidget(self.group_box_result_paras)

        self.tree_widget_result_paras.customContextMenuRequested.connect(
                self.result_paras_context_menu)
        
        self.action_plot.triggered.connect(self.slot_plot_result)
        self.action_export.triggered.connect(self.slot_export_result)
        self.action_analysis.triggered.connect(self.slot_sendto_analysis)
        self.action_delete.triggered.connect(self.slot_delete)
        
        self.plain_text_edit_conmandline.signal_compute_result.connect(
                self.slot_add_result_para)

        self.retranslateUi()

    def result_paras_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.tree_widget_result_paras.itemAt(pos)        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
            menu = QMenu(self.tree_widget_result_paras)
            menu.addActions([self.action_plot,
                             self.action_export,
                             self.action_analysis,
                             self.action_delete])
            menu.exec_(self.tree_widget_result_paras.mapToGlobal(pos))
        
    def slot_plot_result(self):
        
        items = self.tree_widget_result_paras.selectedItems()
        dsp = {}
        paras = []
        for item in items:
            name = item.text(0)
            dsp[name] = self.dict_result_paras[name]
            paralist = self.dict_result_paras[name].get_paralist()
            for paraname in paralist:
                paras.append((paraname, name))
        if dsp and paras:
            self.signal_plot_result_para.emit((dsp, paras))
    
    def slot_export_result(self):
        print('Export')
        
    def slot_sendto_analysis(self):
        
        items = self.tree_widget_result_paras.selectedItems()
        dsp = {}
        for item in items:
            name = item.data(0, Qt.UserRole)
            dsp[name] = self.dict_result_paras[name]
        if dsp:
            self.signal_sendto_ananlysis.emit(dsp)
    
    def slot_delete(self):
        
        sel_items = self.tree_widget_result_paras.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('MathematicsWindow', '删除参数'),
                          QCoreApplication.translate('MathematicsWindow', '确定要删除这些参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.dict_result_paras.pop(item.data(0, Qt.UserRole))
                    self.tree_widget_result_paras.takeTopLevelItem(
                            self.tree_widget_result_paras.indexOfTopLevelItem(item))

    def slot_add_result_para(self, result):
        
        num  = self.count_created_result + 1
        paraname = 'result' + str(num)
        item = QTreeWidgetItem(self.tree_widget_result_paras)
        item.setText(0, paraname)
        item.setData(0, Qt.UserRole, paraname)
        item.setIcon(0, self.math_result_icon)
        col_list = result.columns.values.tolist()
        if col_list[0] == 'Time':
            max_value = result['Result'].max()
            min_value = result['Result'].min()
            item.setText(1, 'Time Series: ' + result.iloc[0, 0] + ' - ' + result.iloc[-1, 0])
            item.setText(2, str(max_value))
            item.setText(3, str(min_value))         
        else:
            item.setText(1, str(result['Result']))
        result.rename(columns = {'Result' : paraname}, inplace=True)
        self.dict_result_paras[paraname] = DataFactory(result)
        self.count_created_result += 1

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_commandline.setTitle(_translate('MathematicsWindow', '计算命令行'))
        self.group_box_result_paras.setTitle(_translate('MathematicsWindow', '计算结果参数'))
        self.tree_widget_result_paras.headerItem().setText(0, _translate('MathematicsWindow', '参数名'))
        self.tree_widget_result_paras.headerItem().setText(1, _translate('MathematicsWindow', '数值'))
        self.tree_widget_result_paras.headerItem().setText(2, _translate('MathematicsWindow', '最大值'))
        self.tree_widget_result_paras.headerItem().setText(3, _translate('MathematicsWindow', '最小值'))

