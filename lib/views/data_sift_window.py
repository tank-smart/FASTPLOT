# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：数据分析类
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
from PyQt5.QtCore import (QSize, QCoreApplication, Qt, QObject)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                             QTabWidget, QPushButton, QGroupBox,
                             QPlainTextEdit, QMessageBox, QTreeWidget, 
                             QTreeWidgetItem, QDialog, QDialogButtonBox,
                             QMenu, QAction, QLineEdit, QHeaderView,
                             QSpacerItem, QSizePolicy)

# =============================================================================
# Package models imports
# =============================================================================
from views.custom_dialog import SelParasDialog
from models.analysis_model import DataAnalysis
import views.config_info as CONFIG
import models.time_model as Time_Model

class SiftResultViewWidget(QWidget):

    def __init__(self, parent = None, expr = ''):
        
        super().__init__(parent)
        
        self.expr = expr
        self.setup()
        
    def setup(self):

        self.verticalLayout_8 = QVBoxLayout(self)
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_8.setSpacing(2)
        self.group_box_view_expression = QGroupBox(self)
        self.verticalLayout_6 = QVBoxLayout(self.group_box_view_expression)
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_6.setSpacing(2)
        self.plain_text_edit_view_expression = QPlainTextEdit(self.group_box_view_expression)
        self.plain_text_edit_view_expression.setEnabled(False)
        self.plain_text_edit_view_expression.setPlainText(self.expr)
        self.verticalLayout_6.addWidget(self.plain_text_edit_view_expression)
        self.verticalLayout_8.addWidget(self.group_box_view_expression)
        self.group_box_sift_result = QGroupBox(self)
        self.verticalLayout_7 = QVBoxLayout(self.group_box_sift_result)
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_7.setSpacing(2)
        self.tree_widget_sift_result = QTreeWidget(self.group_box_sift_result)
#        设置树组件头部显示方式
        headerview = self.tree_widget_sift_result.header()
        headerview.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerview.setMinimumSectionSize(100)
        self.tree_widget_sift_result.setHeader(headerview)
        
        self.verticalLayout_7.addWidget(self.tree_widget_sift_result)
        self.verticalLayout_8.addWidget(self.group_box_sift_result)
        self.verticalLayout_8.setStretch(0, 2)
        self.verticalLayout_8.setStretch(1, 5)
        
        self.retranslateUi()
        
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_view_expression.setTitle(_translate('DataAnalysisWindow', '条件表达式'))
        self.group_box_sift_result.setTitle(_translate('DataAnalysisWindow', '结果'))
        self.tree_widget_sift_result.headerItem().setText(0, _translate('DataAnalysisWindow', '文件对象'))
        self.tree_widget_sift_result.headerItem().setText(1, _translate('DataAnalysisWindow', '状态'))
        self.tree_widget_sift_result.headerItem().setText(2, _translate('DataAnalysisWindow', '捕捉点'))
        self.tree_widget_sift_result.headerItem().setText(3, _translate('DataAnalysisWindow', '持续时间'))

class DataSiftWindow(QWidget):
    
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)

#        计算产生的数据
        self.dict_data = {}
#        不允许改动这个变量，因为该变量连接着主窗口的变量
        self._current_files = []
        
        self.sift_search_paras = []
        
        self.tab_result_count = 0
        
        self.file_icon = QIcon(CONFIG.ICON_FILE)
        self.time_icon = QIcon(CONFIG.ICON_TIME)

# =============================================================================
# UI模块
# =============================================================================        
    def setup(self):
        
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout.setSpacing(2)
        
        self.tab_widget_datasift = QTabWidget(self)
        self.tab_widget_datasift.setTabsClosable(True)
        self.tab_sift = QWidget()
        self.verticalLayout_4 = QVBoxLayout(self.tab_sift)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(2)
        self.group_box_expression = QGroupBox(self.tab_sift)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_expression)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.plain_text_edit_expression = QPlainTextEdit(self.group_box_expression)
        
        self.plain_text_edit_expression.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_add_para = QAction(self.plain_text_edit_expression)
        self.action_add_para.setText(QCoreApplication.
                                   translate('DataAnalysisWindow', '添加参数'))
        
        self.verticalLayout_2.addWidget(self.plain_text_edit_expression)
        self.verticalLayout_4.addWidget(self.group_box_expression)
#        self.group_box_aggregates = QGroupBox(self.tab_sift)
#        self.verticalLayout_3 = QVBoxLayout(self.group_box_aggregates)
#        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
#        self.verticalLayout_3.setSpacing(2)
#        self.push_btn_add_aggregate = QPushButton(self.group_box_aggregates)
#        self.push_btn_add_aggregate.setMinimumSize(QSize(0, 24))
#        self.push_btn_add_aggregate.setMaximumSize(QSize(16777215, 24))
#        self.verticalLayout_3.addWidget(self.push_btn_add_aggregate)
#        self.tree_widget_aggragate_para = QTreeWidget(self.group_box_aggregates)
#        
##        让顶级项没有扩展符空白
#        self.tree_widget_aggragate_para.setRootIsDecorated(False)
#        
#        self.verticalLayout_3.addWidget(self.tree_widget_aggragate_para)
#        self.verticalLayout_4.addWidget(self.group_box_aggregates)
#        self.button_box_sift = QDialogButtonBox(self.tab_sift)
#        self.button_box_sift.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
#        self.verticalLayout_4.addWidget(self.button_box_sift)
        self.hlayout_btn_sc = QHBoxLayout()
        self.hlayout_btn_sc.setSpacing(4)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout_btn_sc.addItem(spacerItem1)
        self.btn_confirm = QPushButton(self.group_box_expression)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.hlayout_btn_sc.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self.group_box_expression)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.hlayout_btn_sc.addWidget(self.btn_cancel)
        self.verticalLayout_4.addLayout(self.hlayout_btn_sc)
        
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 4)
        self.tab_widget_datasift.addTab(self.tab_sift, '')
        
        self.verticalLayout.addWidget(self.tab_widget_datasift)

        self.retranslateUi()
        self.tab_widget_datasift.setCurrentIndex(0)
        
# =======连接信号与槽
# =============================================================================        
#        self.button_box_sift.accepted.connect(self.slot_sift_ok)
#        self.button_box_sift.rejected.connect(self.slot_sift_cancel)
        self.btn_confirm.clicked.connect(self.slot_sift_ok)
        self.btn_cancel.clicked.connect(self.slot_sift_cancel)
        
        self.plain_text_edit_expression.customContextMenuRequested.connect(
                self.expression_context_menu)
        self.action_add_para.triggered.connect(self.slot_add_para)
        
        self.tab_widget_datasift.tabCloseRequested.connect(self.slot_close_tab)
#        self.push_btn_add_aggregate.clicked.connect(self.slot_add_aggregate)
                
# =============================================================================
# slots模块
# =============================================================================
    def slot_sift_ok(self):
        
        list_files = self._current_files
        str_condition = self.plain_text_edit_expression.toPlainText()
        if list_files and str_condition:
            sift_object = DataAnalysis()
#            result_tuple = sift_object.condition_sift_class(list_files,
#                                                            str_condition,
#                                                            self.sift_search_paras)
            
            result_dict = sift_object.condition_sift_wxl(list_files,
                                                          str_condition,
                                                          self.sift_search_paras)
            
            if result_dict:
                

#                创建一个结果显示窗口
                self.tab_result_count += 1
                tab_sift_result = SiftResultViewWidget(self.tab_widget_datasift,  str_condition)
#                for file in list_files:
                for key_file in result_dict:
                    sift_results=result_dict[key_file]#a list
                    item = None
#                    total_time = None
                    first_hit = True
                    for result in sift_results:

                        if first_hit:
                            item = QTreeWidgetItem(tab_sift_result.tree_widget_sift_result)
                            tab_sift_result.tree_widget_sift_result.addTopLevelItem(item)
                            filedir = key_file
                            pos = filedir.rindex('\\')
                            filename = filedir[pos+1:]
                            item.setText(0, filename)
                            item.setIcon(0, self.file_icon)
                            item.setText(1, 'Hit')
                            child = QTreeWidgetItem(item)
                            child.setIcon(0, self.time_icon)
                            child.setText(2, result[0] + ' - ' + result[1])
                            child.setText(3, result[2])
                            first_hit = False
                        else:
                            child = QTreeWidgetItem(item)
                            child.setIcon(0, self.time_icon)
                            child.setText(2, result[0] + ' - ' + result[1])
                            child.setText(3, result[2])
                    if first_hit:
                            item = QTreeWidgetItem(tab_sift_result.tree_widget_sift_result)
                            tab_sift_result.tree_widget_sift_result.addTopLevelItem(item)
                            pos = key_file.rindex('\\')
                            filename = key_file[pos+1:]
                            item.setText(0, filename)
                            item.setText(1, 'No Fit')

                self.tab_widget_datasift.addTab(
                        tab_sift_result, 
                        QCoreApplication.translate('DataAnalysisWindow',
                                                   '筛选结果' + str(self.tab_result_count)))
                self.tab_widget_datasift.setCurrentIndex(
                        self.tab_widget_datasift.indexOf(tab_sift_result))
            else:
                QMessageBox.information(self,
                        QCoreApplication.translate("DataAnalysisWindow", "提示"),
                        QCoreApplication.translate("DataAnalysisWindow", '语法错误'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('DataAnalysisWindow', '提示'),
                    QCoreApplication.translate('DataAnalysisWindow','没有足够的输入'))
        
        
    def slot_sift_cancel(self):
        
        self.plain_text_edit_expression.clear()
#        self.tree_widget_aggragate_para.clear()
        self.sift_search_paras = []
        
    def expression_context_menu(self, pos):

        menu = QMenu(self.plain_text_edit_expression)
        menu.addActions([self.action_add_para])
        menu.exec_(self.plain_text_edit_expression.mapToGlobal(pos))
        
#    def slot_add_aggregate(self):
#        
##        采用单选模式
#        dialog = SelParasDialog(self, self._current_files, 0)
#        return_signal = dialog.exec_()
#        paras = []
#        if (return_signal == QDialog.Accepted):
#            paras = dialog.get_list_sel_paras()
#            if paras:
#                widget_aggregate = QWidget(self.tree_widget_aggragate_para)
#                vlayout = QVBoxLayout()
#                vlayout.setContentsMargins(2, 2, 2, 2)
#                combo_box = QComboBox(widget_aggregate)
#                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '整段数据'))
#                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '最大值'))
#                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '最小值'))
#                combo_box.addItem(QCoreApplication.translate('DataAnalysisWindow', '平均值'))
#                vlayout.addWidget(combo_box)
#                widget_aggregate.setLayout(vlayout)
#                
#                widget_para = QWidget(self.tree_widget_aggragate_para)
#                hlayout = QHBoxLayout()
#                hlayout.setContentsMargins(2, 2, 2, 2)
#                hlayout.setSpacing(2)
#                line_edit = QLineEdit(widget_para)
#                line_edit.setReadOnly(True)
#                line_edit.setText(paras[0])
#                hlayout.addWidget(line_edit)
#                button = QPushButton(widget_para)
#                button.setText(QCoreApplication.translate('DataAnalysisWindow', '删除'))
#                hlayout.addWidget(button)
#                widget_para.setLayout(hlayout)
#                item = QTreeWidgetItem(self.tree_widget_aggragate_para)
#                self.tree_widget_aggragate_para.addTopLevelItem(item)
#                self.tree_widget_aggragate_para.setItemWidget(item, 0, widget_aggregate)
#                self.tree_widget_aggragate_para.setItemWidget(item, 1, widget_para)
#                button.clicked.connect(self.slot_delete_aggregate)
                
#    def slot_delete_aggregate(self):
#        
#        sender = QObject.sender(self)
#        item = self.tree_widget_aggragate_para.itemAt(sender.pos())
#        self.tree_widget_aggragate_para.takeTopLevelItem(
#                self.tree_widget_aggragate_para.indexOfTopLevelItem(item))
        
    def slot_update_current_files(self, files : list):
        
        self._current_files = files
    
    def slot_add_para(self):
        
#        采用单选模式
        dialog = SelParasDialog(self, self._current_files, 0)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                self.plain_text_edit_expression.insertPlainText(paras[0])
                self.sift_search_paras.append(paras[0])
                
    def slot_close_tab(self, index : int):
        
#        不允许关闭第一个tab
        if index > 0:
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('DataAnalysisWindow', '关闭'),
                          QCoreApplication.translate('DataAnalysisWindow',
                                            '''<p>确定要关闭吗？'''),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.tab_widget_datasift.removeTab(index)

# =============================================================================
# 功能函数模块   
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_expression.setTitle(_translate('DataAnalysisWindow', '条件表达式'))
#        self.group_box_aggregates.setTitle(_translate('DataAnalysisWindow', '筛选目标'))
#        self.push_btn_add_aggregate.setText(_translate('DataAnalysisWindow', '添加新目标'))
#        self.tree_widget_aggragate_para.headerItem().setText(0, _translate('DataAnalysisWindow', '条件'))
#        self.tree_widget_aggragate_para.headerItem().setText(1, _translate('DataAnalysisWindow', '参数'))
        self.tab_widget_datasift.setTabText(self.tab_widget_datasift.indexOf(self.tab_sift), _translate('DataAnalysisWindow', '数据筛选'))
        self.btn_confirm.setText(_translate("DataManageWindow", "确定"))
        self.btn_cancel.setText(_translate("DataManageWindow", "取消"))