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
                             QTreeWidgetItem, QGroupBox)
# =============================================================================
# Package views imports
# =============================================================================
from models.mathematics_model import MathematicsEditor
from models.datafile_model import Normal_DataFile, DataFile
import views.constant as CONSTANT

class MathematicsWindow(QWidget):
    
    signal_plot_result_para = pyqtSignal(tuple)
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self._current_files = []
        self.dict_result_paras = {}
        self.time_series_icon = QIcon(CONSTANT.ICON_CURVE)
        
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
        self.tree_widget_result_paras.header().setMinimumSectionSize(100)
        
        self.tree_widget_result_paras.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_plot = QAction(self.tree_widget_result_paras)
        self.action_plot.setText(QCoreApplication.
                                 translate('MathematicsWindow', '绘图'))
        self.action_export = QAction(self.tree_widget_result_paras)
        self.action_export.setText(QCoreApplication.
                                   translate('MathematicsWindow', '导出'))
        
        self.verticalLayout_2.addWidget(self.tree_widget_result_paras)
        self.verticalLayout.addWidget(self.group_box_result_paras)

        self.tree_widget_result_paras.customContextMenuRequested.connect(
                self.result_paras_context_menu)
        self.action_plot.triggered.connect(self.slot_plot_result)
        self.action_export.triggered.connect(self.slot_export_result)
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
                             self.action_export])
            menu.exec_(self.tree_widget_result_paras.mapToGlobal(pos))
        
    def slot_plot_result(self):
        
        item = self.tree_widget_result_paras.currentItem()
        name = item.text(0)
#        emit一个tuple形式为([dataframelist],[paralist])
        self.signal_plot_result_para.emit(([self.dict_result_paras[name]],[name]))
    
    def slot_export_result(self):
        print('Export')

    def slot_add_result_para(self, result):
        col_list = result.columns.values.tolist()
#        length  = len(self.dict_result_paras)
#            yanhua修改

        paraname=col_list[1]

#            yanhua修改结束
        item = QTreeWidgetItem(self.tree_widget_result_paras)
        item.setText(0, paraname)
        item.setIcon(0, self.time_series_icon)
#        col_list = result.columns.values.tolist()
        if col_list[0] == 'Time':
#            max_value = result['Result'].max()
#            min_value = result['Result'].min()
#            yanhua修改
            max_value = result[col_list[1]].max()
            min_value = result[col_list[1]].min()
#            yanhua修改结束
            item.setText(1, 'Time Series: ' + result.iloc[0, 0] + ' - ' + result.iloc[-1, 0])
            item.setText(2, str(max_value))
            item.setText(3, str(min_value))         
        else:
            item.setText(1, str(result[col_list[1]].values[0]))        
        self.dict_result_paras[paraname] = result

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_commandline.setTitle(_translate('MathematicsWindow', '计算命令行'))
        self.group_box_result_paras.setTitle(_translate('MathematicsWindow', '计算结果参数'))
        self.tree_widget_result_paras.headerItem().setText(0, _translate('MathematicsWindow', '参数名'))
        self.tree_widget_result_paras.headerItem().setText(1, _translate('MathematicsWindow', '数值'))
        self.tree_widget_result_paras.headerItem().setText(2, _translate('MathematicsWindow', '最大值'))
        self.tree_widget_result_paras.headerItem().setText(3, _translate('MathematicsWindow', '最小值'))
#yanhua改，现实现方法，需要使用类方法实现qt界面上的clear    
    @classmethod
    def clear(self):
        self.dict_result_paras={}
        self.tree_widget_result_paras.clear()
