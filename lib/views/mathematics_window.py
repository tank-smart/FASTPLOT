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
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal, QSize, QObject
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QMenu, QAction,
                             QTreeWidgetItem, QGroupBox, QAbstractItemView,
                             QHeaderView, QMessageBox, QHBoxLayout,
                              QPushButton, QGridLayout, QSpacerItem, QSizePolicy)
# =============================================================================
# Package views imports
# =============================================================================
from models.mathematics_model import MathematicsEditor
import views.config_info as CONFIG
from models.data_model import DataFactory

class MathematicsWindow(QWidget):
    
    signal_plot_result_para = pyqtSignal(tuple)
    signal_sendto_ananlysis = pyqtSignal(dict)
#    操作与函数名字符串
    signal_op_fun_str = pyqtSignal(str)
# =============================================================================
# 初始化    
# =============================================================================    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self._current_files = []
        self.dict_result_paras = {}
        self.count_created_result = 0
        self.math_result_icon = QIcon(CONFIG.ICON_MATH_RESULT)
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.group_box_commandline = QGroupBox(self)
        self.horizontalLayout_3 = QHBoxLayout(self.group_box_commandline)
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setSpacing(2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.plain_text_edit_conmandline = MathematicsEditor(self.group_box_commandline)
        self.verticalLayout_3.addWidget(self.plain_text_edit_conmandline)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.btn_add_paras = QPushButton(self.group_box_commandline)
        self.btn_add_paras.setMinimumSize(QSize(0, 24))
        self.btn_add_paras.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_add_paras)
        self.btn_add_funs = QPushButton(self.group_box_commandline)
        self.btn_add_funs.setMinimumSize(QSize(0, 24))
        self.btn_add_funs.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_add_funs)
        self.btn_mathe_script = QPushButton(self.group_box_commandline)
        self.btn_mathe_script.setMinimumSize(QSize(0, 24))
        self.btn_mathe_script.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_mathe_script)
#        self.btn_last_cmd = QPushButton(self.group_box_commandline)
#        self.btn_last_cmd.setMinimumSize(QSize(0, 24))
#        self.btn_last_cmd.setMaximumSize(QSize(16777215, 24))
#        self.horizontalLayout.addWidget(self.btn_last_cmd)
        self.btn_clear_input = QPushButton(self.group_box_commandline)
        self.btn_clear_input.setMinimumSize(QSize(0, 24))
        self.btn_clear_input.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_clear_input)
        self.btn_clc = QPushButton(self.group_box_commandline)
        self.btn_clc.setMinimumSize(QSize(0, 24))
        self.btn_clc.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_clc)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(4)
        self.btn_add = QPushButton(self.group_box_commandline)
        self.btn_add.setMinimumSize(QSize(40, 30))
        self.btn_add.setMaximumSize(QSize(40, 30))
        font_12 = QFont()
        font_12.setPointSize(12)
        self.btn_add.setFont(font_12)
        self.gridLayout.addWidget(self.btn_add, 0, 0, 1, 1)
        self.btn_sub = QPushButton(self.group_box_commandline)
        self.btn_sub.setMinimumSize(QSize(40, 30))
        self.btn_sub.setMaximumSize(QSize(40, 30))
        self.btn_sub.setFont(font_12)
        self.gridLayout.addWidget(self.btn_sub, 0, 1, 1, 1)
        self.btn_mult = QPushButton(self.group_box_commandline)
        self.btn_mult.setMinimumSize(QSize(40, 30))
        self.btn_mult.setMaximumSize(QSize(40, 30))
        self.btn_mult.setFont(font_12)
        self.gridLayout.addWidget(self.btn_mult, 0, 2, 1, 1)
        self.btn_div = QPushButton(self.group_box_commandline)
        self.btn_div.setMinimumSize(QSize(40, 30))
        self.btn_div.setMaximumSize(QSize(40, 30))
        self.btn_div.setFont(font_12)
        self.gridLayout.addWidget(self.btn_div, 0, 3, 1, 1)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.btn_left_bra = QPushButton(self.group_box_commandline)
        self.btn_left_bra.setMinimumSize(QSize(40, 30))
        self.btn_left_bra.setMaximumSize(QSize(40, 30))
        font_10 = QFont()
        font_10.setPointSize(10)
        self.btn_left_bra.setFont(font_10)
        self.gridLayout.addWidget(self.btn_left_bra, 1, 0, 1, 1)
        self.btn_right_bra = QPushButton(self.group_box_commandline)
        self.btn_right_bra.setMinimumSize(QSize(40, 30))
        self.btn_right_bra.setMaximumSize(QSize(40, 30))
        self.btn_right_bra.setFont(font_10)
        self.gridLayout.addWidget(self.btn_right_bra, 1, 1, 1, 1)
        self.btn_square = QPushButton(self.group_box_commandline)
        self.btn_square.setMinimumSize(QSize(40, 30))
        self.btn_square.setMaximumSize(QSize(40, 30))
        self.btn_square.setFont(font_10)
        self.gridLayout.addWidget(self.btn_square, 1, 2, 1, 1)
        self.btn_sqrt = QPushButton(self.group_box_commandline)
        self.btn_sqrt.setMinimumSize(QSize(40, 30))
        self.btn_sqrt.setMaximumSize(QSize(40, 30))
        self.btn_sqrt.setFont(font_10)
        self.gridLayout.addWidget(self.btn_sqrt, 1, 3, 1, 1)
        spacerItem2 = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 4, 1, 1)
        self.btn_abs = QPushButton(self.group_box_commandline)
        self.btn_abs.setMinimumSize(QSize(40, 30))
        self.btn_abs.setMaximumSize(QSize(40, 30))
        self.btn_abs.setFont(font_10)
        self.gridLayout.addWidget(self.btn_abs, 2, 0, 1, 1)
        self.btn_pow_ten = QPushButton(self.group_box_commandline)
        self.btn_pow_ten.setMinimumSize(QSize(40, 30))
        self.btn_pow_ten.setMaximumSize(QSize(40, 30))
        self.btn_pow_ten.setFont(font_10)
        self.gridLayout.addWidget(self.btn_pow_ten, 2, 1, 1, 1)
        self.btn_pow = QPushButton(self.group_box_commandline)
        self.btn_pow.setMinimumSize(QSize(40, 30))
        self.btn_pow.setMaximumSize(QSize(40, 30))
        self.btn_pow.setFont(font_10)
        self.gridLayout.addWidget(self.btn_pow, 2, 2, 1, 1)
        self.btn_log = QPushButton(self.group_box_commandline)
        self.btn_log.setMinimumSize(QSize(40, 30))
        self.btn_log.setMaximumSize(QSize(40, 30))
        self.btn_log.setFont(font_10)
        self.gridLayout.addWidget(self.btn_log, 2, 3, 1, 1)
        spacerItem3 = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 4, 1, 1)
        self.btn_sin = QPushButton(self.group_box_commandline)
        self.btn_sin.setMinimumSize(QSize(40, 30))
        self.btn_sin.setMaximumSize(QSize(40, 30))
        self.btn_sin.setFont(font_10)
        self.gridLayout.addWidget(self.btn_sin, 3, 0, 1, 1)
        self.btn_cos = QPushButton(self.group_box_commandline)
        self.btn_cos.setMinimumSize(QSize(40, 30))
        self.btn_cos.setMaximumSize(QSize(40, 30))
        self.btn_cos.setFont(font_10)
        self.gridLayout.addWidget(self.btn_cos, 3, 1, 1, 1)
        self.btn_tan = QPushButton(self.group_box_commandline)
        self.btn_tan.setMinimumSize(QSize(40, 30))
        self.btn_tan.setMaximumSize(QSize(40, 30))
        self.btn_tan.setFont(font_10)
        self.gridLayout.addWidget(self.btn_tan, 3, 2, 1, 1)
        spacerItem4 = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 4, 1, 1)
        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 4, 0, 1, 1)
        spacerItem6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 4, 1, 1, 1)
        spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 4, 2, 1, 1)
        spacerItem8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 4, 3, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
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
#        self.action_export = QAction(self.tree_widget_result_paras)
#        self.action_export.setText(QCoreApplication.
#                                   translate('MathematicsWindow', '导出'))
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
#        self.action_export.triggered.connect(self.slot_export_result)
        self.action_analysis.triggered.connect(self.slot_sendto_analysis)
        self.action_delete.triggered.connect(self.slot_delete)
        
        self.plain_text_edit_conmandline.signal_compute_result.connect(
                self.slot_add_result_para)
#----------yanhua加：
        self.plain_text_edit_conmandline.signal_clc.connect(
                self.slot_clear)
#----------yanhua加
        self.btn_add_paras.clicked.connect(self.plain_text_edit_conmandline.slot_add_para)
        self.btn_add_funs.clicked.connect(self.plain_text_edit_conmandline.slot_add_func)
        self.btn_mathe_script.clicked.connect(self.plain_text_edit_conmandline.slot_math_script)
        self.btn_clear_input.clicked.connect(self.plain_text_edit_conmandline.slot_clear)
        self.btn_clc.clicked.connect(self.plain_text_edit_conmandline.clc)
        
        self.signal_op_fun_str.connect(self.plain_text_edit_conmandline.slot_insert_op_func_str)
        self.btn_add.clicked.connect(self.slot_send_op_func_str)
        self.btn_sub.clicked.connect(self.slot_send_op_func_str)
        self.btn_mult.clicked.connect(self.slot_send_op_func_str)
        self.btn_div.clicked.connect(self.slot_send_op_func_str)
        self.btn_left_bra.clicked.connect(self.slot_send_op_func_str)
        self.btn_right_bra.clicked.connect(self.slot_send_op_func_str)
        self.btn_square.clicked.connect(self.slot_send_op_func_str)
        self.btn_sqrt.clicked.connect(self.slot_send_op_func_str)
        self.btn_pow_ten.clicked.connect(self.slot_send_op_func_str)
        self.btn_pow.clicked.connect(self.slot_send_op_func_str)
        self.btn_log.clicked.connect(self.slot_send_op_func_str)
        self.btn_abs.clicked.connect(self.slot_send_op_func_str)
        self.btn_sin.clicked.connect(self.slot_send_op_func_str)
        self.btn_cos.clicked.connect(self.slot_send_op_func_str)
        self.btn_tan.clicked.connect(self.slot_send_op_func_str)

        self.retranslateUi()

    def result_paras_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.tree_widget_result_paras.itemAt(pos)        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
            menu = QMenu(self.tree_widget_result_paras)
            menu.addActions([self.action_plot,
#                             self.action_export,
                             self.action_analysis,
                             self.action_delete])
            menu.exec_(self.tree_widget_result_paras.mapToGlobal(pos))
        
    def slot_plot_result(self):
        
        items = self.tree_widget_result_paras.selectedItems()
        dsp = {}
        paras = []
        for item in items:
            name = item.text(0)
            if name in self.dict_result_paras:
                dsp[name] = self.dict_result_paras[name]
                paralist = self.dict_result_paras[name].get_paralist()
                for paraname in paralist:
                    paras.append((paraname, name))
            else:   
                QMessageBox.information(self,
                            QCoreApplication.translate('MathematicsWindow','提示'),
                            QCoreApplication.translate('MathematicsWindow','无法对选中的常数绘图'))
        if dsp and paras:
            self.signal_plot_result_para.emit((dsp, paras))
    
    def slot_export_result(self):
        
        print('Export')
        
    def slot_sendto_analysis(self):
        
        items = self.tree_widget_result_paras.selectedItems()
        dsp = {}
        for item in items:
            name = item.data(0, Qt.UserRole)
            if name in self.dict_result_paras:
                dsp[name] = self.dict_result_paras[name]
            else:
                QMessageBox.information(self,
                            QCoreApplication.translate('MathematicsWindow','提示'),
                            QCoreApplication.translate('MathematicsWindow','无法添加常数到分析参数'))
                
        if dsp:
            self.signal_sendto_ananlysis.emit(dsp)
    
    def slot_delete(self):
        
        sel_items = self.tree_widget_result_paras.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('MathematicsWindow', '删除参数'),
                          QCoreApplication.translate('MathematicsWindow', '确定要删除所选参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    if item.data(0, Qt.UserRole) in self.dict_result_paras:
                        self.dict_result_paras.pop(item.data(0, Qt.UserRole))
                    self.tree_widget_result_paras.takeTopLevelItem(
                            self.tree_widget_result_paras.indexOfTopLevelItem(item))

    def slot_add_result_para_wxl(self, result):
        
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

#            yanhua修改        
    def slot_add_result_para(self, result):
        col_list = result.columns.values.tolist()
#        length  = len(self.dict_result_paras)

        paraname=col_list[1]


        item = QTreeWidgetItem(self.tree_widget_result_paras)
        item.setText(0, paraname)
        item.setData(0, Qt.UserRole, paraname)
        item.setIcon(0, self.math_result_icon)
#        col_list = result.columns.values.tolist()
        if col_list[0] == 'Time':
#            max_value = result['Result'].max()
#            min_value = result['Result'].min()
#            yanhua修改
            max_value = result[col_list[1]].max()
            min_value = result[col_list[1]].min()
#            yanhua修改结束
            item.setText(1, 'Time Series: ' + str(result.iloc[0, 0]) + ' - ' + str(result.iloc[-1, 0]))
            item.setText(2, str(max_value))
            item.setText(3, str(min_value))
            self.dict_result_paras[paraname] = DataFactory(result)
        else:
#            self.dict_result_paras[paraname] = result
#!!!!            单值不加入self.dict_result_paras，也不进行绘图和分析
            item.setText(1, str(result[col_list[1]].values[0]))        
#            yanhua修改结束
            
    def slot_send_op_func_str(self):
        
        sender = QObject.sender(self)
        if sender == self.btn_add:
            self.signal_op_fun_str.emit('+')
        if sender == self.btn_sub:
            self.signal_op_fun_str.emit('-')
        if sender == self.btn_mult:
            self.signal_op_fun_str.emit('*')
        if sender == self.btn_div:
            self.signal_op_fun_str.emit('/')
        if sender == self.btn_left_bra:
            self.signal_op_fun_str.emit('(')
        if sender == self.btn_right_bra:
            self.signal_op_fun_str.emit(')')
        if sender == self.btn_square:
            self.signal_op_fun_str.emit('**2')
        if sender == self.btn_sqrt:
            self.signal_op_fun_str.emit('sqrt()')
        if sender == self.btn_pow_ten:
            self.signal_op_fun_str.emit('pow(10, )')
        if sender == self.btn_pow:
            self.signal_op_fun_str.emit('pow()')
        if sender == self.btn_log:
            self.signal_op_fun_str.emit('log()')
        if sender == self.btn_abs:
            self.signal_op_fun_str.emit('abs()')
        if sender == self.btn_sin:
            self.signal_op_fun_str.emit('sin()')
        if sender == self.btn_cos:
            self.signal_op_fun_str.emit('cos()')
        if sender == self.btn_tan:
            self.signal_op_fun_str.emit('tan()')
            

#yanhua改，现实现方法，需要使用类方法实现qt界面上的clear    
    
    def slot_clear(self, clear_signal):
        if clear_signal:
            self.dict_result_paras={}
            self.tree_widget_result_paras.clear()
            
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.group_box_commandline.setTitle(_translate('MathematicsWindow', '计算命令行'))
        self.btn_add_paras.setText(_translate('MathematicsWindow', '添加参数'))
        self.btn_add_funs.setText(_translate('MathematicsWindow', '添加函数'))
        self.btn_mathe_script.setText(_translate('MathematicsWindow', '计算脚本'))
#        self.btn_last_cmd.setText(_translate('MathematicsWindow', '上条指令'))
        self.btn_clear_input.setText(_translate('MathematicsWindow', '清空指令'))
        self.btn_clc.setText(_translate('MathematicsWindow', '清空变量'))
        self.btn_add.setText(_translate('MathematicsWindow', '+'))
        self.btn_sub.setText(_translate('MathematicsWindow', '-'))
        self.btn_mult.setText(_translate('MathematicsWindow', '*'))
        self.btn_div.setText(_translate('MathematicsWindow', '/'))
        self.btn_left_bra.setText(_translate('MathematicsWindow', '('))
        self.btn_right_bra.setText(_translate('MathematicsWindow', ')'))
        self.btn_sqrt.setText(_translate('MathematicsWindow', 'sqrt'))
        self.btn_square.setText(_translate('MathematicsWindow', '^2'))
        self.btn_pow_ten.setText(_translate('MathematicsWindow', '10^x'))
        self.btn_pow.setText(_translate('MathematicsWindow', 'pow'))
        self.btn_log.setText(_translate('MathematicsWindow', 'log'))
        self.btn_abs.setText(_translate('MathematicsWindow', 'abs'))
        self.btn_abs.setToolTip(_translate('MathematicsWindow', '取绝对值函数，a可以是参数时\n间序列向量、数值或矩阵，对a中所有元素取绝对值，返回a的原类型'))
        self.btn_sin.setText(_translate('MathematicsWindow', 'sin'))
        self.btn_cos.setText(_translate('MathematicsWindow', 'cos'))
        self.btn_tan.setText(_translate('MathematicsWindow', 'tan'))
        self.group_box_result_paras.setTitle(_translate('MathematicsWindow', '计算结果参数'))
        self.tree_widget_result_paras.headerItem().setText(0, _translate('MathematicsWindow', '参数名'))
        self.tree_widget_result_paras.headerItem().setText(1, _translate('MathematicsWindow', '数值'))
        self.tree_widget_result_paras.headerItem().setText(2, _translate('MathematicsWindow', '最大值'))
        self.tree_widget_result_paras.headerItem().setText(3, _translate('MathematicsWindow', '最小值'))

