# -*- coding: utf-8 -*-
# =============================================================================
# Dialog Content
# 
# SaveTemplateDialog
# SelectTemplateBaseDialog
# SelectParasTemplateDialog
# SelectPlotTemplateDialog
# MathScriptDialog
# SelParasDialog
# SelfuncDialog
# SelXParaDialog
# ParaSetupDialog
# Base_LineSettingDialog
# LineSettingDialog
# AnnotationSettingDialog
# Base_AxisSettingDialog
# AxisSettingDialog
# SingleUtAxisSettingDialog
# StackAxisSettingDialog
# FigureCanvasSetiingDialog
# ParameterExportDialog
# FileProcessDialog
# SelFunctionDialog
# OptionDialog
# DsiplayParaInfoBaseDialog
# DisplayParaValuesDialog
# DisplayParaAggregateInfoDialog
# ImportDataFileDialog
# =============================================================================
# =============================================================================
# Imports
# =============================================================================
import os, sys, re, json
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
from matplotlib.axes import Axes
import matplotlib.colors as Color
import matplotlib.dates as mdates

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QCoreApplication, Qt, pyqtSignal, QObject,
                          QDataStream, QIODevice)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QPushButton, QMessageBox, QListWidget,
                             QListWidgetItem, QToolButton, QFrame, 
                             QAbstractItemView, QApplication, QComboBox,
                             QColorDialog, QGroupBox, QTreeWidget,
                             QTreeWidgetItem, QHeaderView, QFileDialog,
                             QAction, QMenu, QStackedWidget, QWidget,
                             QCheckBox, QTableWidget, QTableWidgetItem,
                             QSpinBox, QGraphicsScene, QGraphicsView,
                             QPlainTextEdit)

# =============================================================================
# Package models imports
# =============================================================================
from models.datafile_model import DataFile, Normal_DataFile, DataFile_Factory
import views.config_info as CONFIG
import models.time_model as Time_Model
from models.data_model import DataFactory
from models.analysis_model import DataAnalysis

#这个类可以用QInputDialog类代替，所以没必要创建，后续改进
class SaveTemplateDialog(QDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.setup()
        self.temp_name = ''
    
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(400, 60)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setMinimumSize(QSize(0, 24))
        self.label.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.label)
        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMinimumSize(QSize(0, 24))
        self.line_edit_name.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_confirm = QPushButton(self)
        self.horizontalLayout_2.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
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
                    QCoreApplication.translate('SaveTemplateDialog', '输入提示'),
                    QCoreApplication.translate('SaveTemplateDialog', '未输入模板名'))
    
    def retranslateUi(self):
        
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('SaveTemplateDialog', '模板名称'))
        self.label.setText(_translate('SaveTemplateDialog', '模板名称'))
        self.button_confirm.setText(_translate('SaveTemplateDialog', '确定'))
        self.button_cancel.setText(_translate('SaveTemplateDialog', '取消'))

class SelectTemplateBaseDialog(QDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.sel_temp = ''
        self.tempicon = QIcon(CONFIG.ICON_TEMPLATE)
        self.setup()
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(700, 450)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(4, 0, 4, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.verticalLayout = QVBoxLayout()
        self.label_temp = QLabel(self)
        self.label_temp.setMinimumSize(QSize(0, 24))
        self.label_temp.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.label_temp)
        self.list_temps = QListWidget(self)
        self.list_temps.setMinimumWidth(200)
        self.list_temps.setMaximumWidth(200)
        self.verticalLayout.addWidget(self.list_temps)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.label_preview = QLabel(self)
        self.label_preview.setMinimumSize(QSize(0, 24))
        self.label_preview.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_2.addWidget(self.label_preview)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_confirm = QPushButton(self)
        self.horizontalLayout.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.signal_slot_connect()
        
        self.retranslateUi()
        
    def accept(self):
        
        item = self.list_temps.currentItem()
        if item:
            self.sel_temp = item.text()
        QDialog.accept(self)
        
    def signal_slot_connect(self):
        
        self.button_cancel.clicked.connect(self.reject)
        self.button_confirm.clicked.connect(self.accept)
        
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('SelectTemplateBaseDialog', '选择模板'))
        self.label_temp.setText(_translate('SelectTemplateBaseDialog', '模板列表'))
        self.label_preview.setText(_translate('SelectTemplateBaseDialog', '模板预览'))
        self.button_confirm.setText(_translate('SelectTemplateBaseDialog', '确定'))
        self.button_cancel.setText(_translate('SelectTemplateBaseDialog', '取消'))

class SelectParasTemplateDialog(SelectTemplateBaseDialog):
    
    def __init__(self, parent = None, templates = {}):
        
        super().__init__(parent)
#        在预览标签下添加预览控件，这里为列表控件
        self.preview_widget = QListWidget(self)
        self.verticalLayout_2.addWidget(self.preview_widget)
        self.list_temps.itemClicked.connect(self.slot_display_paras)
        self.label_preview.setText(QCoreApplication.translate('SelectParasTemplateDialog', '参数列表'))
#        初始化参数列表的信息
        self._data_dict = None
        self.templates = templates
        self.paraicon = QIcon(CONFIG.ICON_PARA)
        
        self.load_data_dict()
        self.load_templates()

    def slot_display_paras(self, item):
        
        name = item.text()
        self.preview_widget.clear()
        for paraname in self.templates[name]:
            para_item = QListWidgetItem(paraname, self.preview_widget)
            para_item.setIcon(self.paraicon)
            if (self._data_dict and 
                CONFIG.OPTION['data dict scope paralist'] and
                paraname in self._data_dict):
                if CONFIG.OPTION['data dict scope style'] == 0:
#                    如果是0，那不安只有参数名的风格显示，这是模板，应尽量有软件标识符信息
                    temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                if CONFIG.OPTION['data dict scope style'] == 1:
                    temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                if CONFIG.OPTION['data dict scope style'] == 2:
                    temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                para_item.setText(temp_str)
            else:
                para_item.setText(paraname)
            para_item.setData(Qt.UserRole, paraname)
    
    def load_templates(self):
        
        flag = True
        if self.templates:
            for name in self.templates:
                item = QListWidgetItem(name, self.list_temps)
                item.setIcon(self.tempicon)
                if flag:
                    self.slot_display_paras(item)
                    flag = False
                    
            self.list_temps.setCurrentRow(0)
            
    def load_data_dict(self):
        
        try:
            with open(CONFIG.SETUP_DIR + r'\data\data_dicts\\' + CONFIG.OPTION['data dict version']) as f_obj:
                self._data_dict = json.load(f_obj)
        except:
            pass
        
class SelectPlotTemplateDialog(SelectTemplateBaseDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
#        在预览标签下添加预览控件，这里为列表控件
        self.gp_scene = QGraphicsScene(self)
        self.preview_widget = QGraphicsView(self.gp_scene, self)
        self.verticalLayout_2.addWidget(self.preview_widget)
        self.list_temps.itemClicked.connect(self.slot_display_plot_temp)
        
        self.templates = {}
        self.load_templates()
        
    def load_templates(self):
        
        dirs = []
        try:
            dirs = os.listdir(CONFIG.SETUP_DIR + '\\data\\plot_temps')
        except FileNotFoundError:
            QMessageBox.information(self,
                                    QCoreApplication.translate('SelectPlotTemplateDialog', '提示'),
                                    QCoreApplication.translate('SelectPlotTemplateDialog', '找不到模板数据存储路径！'))
        for d in dirs:
            name,suffix = os.path.splitext(d)
            self.templates[name] = CONFIG.SETUP_DIR + '\\data\\plot_temps' + d
        if self.templates:
            for i, name in enumerate(self.templates):
                item = QListWidgetItem(name, self.list_temps)
                item.setIcon(self.tempicon)
                if i == 0:
                    self.slot_display_plot_temp(item)
            self.list_temps.setCurrentRow(0)
    
    def slot_display_plot_temp(self, item):
        
        name = item.text()
        temp_png_dir = CONFIG.SETUP_DIR + '\\data\\plot_temps\\' + name + '.png'
        self.gp_scene.clear()
        if os.path.isfile(temp_png_dir):
            temp_png_pixmap = QPixmap(temp_png_dir)
#            temp_png_pixmap.setDevicePixelRatio(2.0)
#            size = temp_png_pixmap.size()
            temp_png_pixmap = temp_png_pixmap.scaled(482, 382, transformMode = Qt.SmoothTransformation)
#            print('w %d, h %d' % (self.preview_widget.width(), self.preview_widget.height()))
            self.gp_scene.addPixmap(temp_png_pixmap)
            
class MathScriptDialog(SelectTemplateBaseDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
#        UI改动
        self.script_edit_win = QPlainTextEdit(self)
        self.verticalLayout_2.addWidget(self.script_edit_win)
        
        self.setWindowTitle(QCoreApplication.translate('MathScriptDialog', '计算脚本'))
        self.label_temp.setText(QCoreApplication.translate('MathScriptDialog', '脚本列表'))
        self.label_preview.setText(QCoreApplication.translate('MathScriptDialog', '编辑脚本'))
        self.button_confirm.setText(QCoreApplication.translate('MathScriptDialog', '保存'))
        self.button_cancel.setText(QCoreApplication.translate('MathScriptDialog', '重置'))
        self.button_exec.setText(QCoreApplication.translate('MathScriptDialog', '执行'))
        
#        脚本的字符串
        self.script = ''
        self.dict_scripts = {}
        self.current_script_item = None
        self.load_scripts()
        
    def signal_slot_connect(self):
        
        self.button_exec = QPushButton(self)
        self.horizontalLayout.addWidget(self.button_exec)
        self.list_temps.setContextMenuPolicy(Qt.CustomContextMenu)
        self.action_create_scp = QAction(self.list_temps)
        self.action_create_scp.setText(QCoreApplication.
                                       translate('MathScriptDialog', '创建脚本'))
        self.action_delete_scp = QAction(self.list_temps)
        self.action_delete_scp.setText(QCoreApplication.
                                       translate('MathScriptDialog', '删除脚本'))
        
        self.button_confirm.clicked.connect(self.slot_save_script)
        self.button_cancel.clicked.connect(self.slot_reset_script)
        self.button_exec.clicked.connect(self.accept)
        self.list_temps.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        self.action_create_scp.triggered.connect(self.slot_create_scp)
        self.action_delete_scp.triggered.connect(self.slot_delete_scp)
        self.list_temps.itemClicked.connect(self.slot_display_script)
        self.list_temps.itemChanged.connect(self.slot_script_name_change)
        
    def on_tree_context_menu(self, pos):
#        记录右击时鼠标所在的item
        sel_item = self.list_temps.itemAt(pos)
        
#        创建菜单，添加动作，显示菜单
        menu = QMenu(self.list_temps)
        menu.addActions([self.action_create_scp,
                         self.action_delete_scp])
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
            self.action_delete_scp.setEnabled(True)
        else:
            self.action_delete_scp.setEnabled(False)
        menu.exec_(self.list_temps.mapToGlobal(pos))
    
    def slot_create_scp(self):
        
        temp_name = 'untitled0'
        i = 1
        while temp_name in self.dict_scripts:
            temp_name = 'untitled' + str(i)
            i += 1
        self.dict_scripts[temp_name] = CONFIG.SETUP_DIR + '\\data\\math_scripts\\' + temp_name + '.json'
        item = QListWidgetItem(temp_name, self.list_temps)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        item.setData(Qt.UserRole, temp_name)
        item.setIcon(self.tempicon)
        self.current_script_item = item
        self.list_temps.setCurrentItem(item)
#        self.list_temps.openPersistentEditor(item)
        self.list_temps.editItem(item)
        self.script_edit_win.clear()
        try:
            with open(self.dict_scripts[temp_name], 'w') as file:
                json.dump(self.script_edit_win.toPlainText(), file)
        except:
            pass
    
    def slot_delete_scp(self):
        
        if self.current_script_item:
            message = QMessageBox.warning(self,
                                          QCoreApplication.translate('SelectPlotTemplateDialog', '删除脚本'),
                                          QCoreApplication.translate('SelectPlotTemplateDialog', '确定要删除所选脚本吗'),
                                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.list_temps.takeItem(self.list_temps.row(self.current_script_item))
                os.remove(self.dict_scripts[self.current_script_item.text()])
                self.dict_scripts.pop(self.current_script_item.text())
                if self.list_temps:
                    self.slot_display_script(self.list_temps.currentItem())
                    self.list_temps.setCurrentItem(self.list_temps.currentItem())
                else:
                    self.script_edit_win.clear()
        
#    保存当前脚本
    def slot_save_script(self):
        
        script_name = self.current_script_item.text()
        try:
            with open(CONFIG.SETUP_DIR + '\\data\\math_scripts\\' + script_name + '.json', 'w') as file:
                json.dump(self.script_edit_win.toPlainText(), file)
            QMessageBox.information(self,
                                    QCoreApplication.translate('SelectPlotTemplateDialog', '提示'),
                                    QCoreApplication.translate('SelectPlotTemplateDialog', '保存成功！'))
        except:
            pass
    
#    还原脚本的最初状态
    def slot_reset_script(self):
        
        if self.current_script_item:
            self.slot_display_script(self.current_script_item)
            
    def slot_script_name_change(self, item):
        
        new_name = item.text()
        old_name = item.data(Qt.UserRole)
        if new_name and old_name:
            if new_name != old_name:
                new_dir = CONFIG.SETUP_DIR + '\\data\\math_scripts\\' + new_name + '.json'
                os.rename(self.dict_scripts[old_name], new_dir)
                del self.dict_scripts[old_name]
                self.dict_scripts[new_name] = new_dir
                item.setData(Qt.UserRole, new_name)
        else:
            item.setText(item.data(Qt.UserRole))
            
    
#    执行脚本
    def accept(self):
        
        self.script = self.script_edit_win.toPlainText()
        QDialog.accept(self)

    def slot_display_script(self, item):
        
        name = item.text()
        script_dir = CONFIG.SETUP_DIR + '\\data\\math_scripts\\' + name + '.json'
        try:
            with open(script_dir, 'r') as file:
                script = json.load(file)
                self.current_script_item = item
                self.script_edit_win.clear()
                self.script_edit_win.setPlainText(script)
        except:
            pass

    def load_scripts(self):
        
        dirs = []
        try:
            dirs = os.listdir(CONFIG.SETUP_DIR + '\\data\\math_scripts')
        except FileNotFoundError:
            QMessageBox.information(self,
                                    QCoreApplication.translate('SelectPlotTemplateDialog', '提示'),
                                    QCoreApplication.translate('SelectPlotTemplateDialog', '找不到计算脚本存储路径！'))
        for d in dirs:
            name,suffix = os.path.splitext(d)
            self.dict_scripts[name] = CONFIG.SETUP_DIR + '\\data\\math_scripts\\' + d
        if self.dict_scripts:
            for i, name in enumerate(self.dict_scripts):
                item = QListWidgetItem(name, self.list_temps)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
#                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                item.setIcon(self.tempicon)
                item.setData(Qt.UserRole, name)
                if i == 0:
                    self.slot_display_script(item)
            self.list_temps.setCurrentRow(0)
            

class SelParasDialog(QDialog):

    signal_add_paras = pyqtSignal()
    
    def __init__(self, parent = None, files = [], sel_mode = 0, dict_filetype = None):
        
        super().__init__(parent)
        
        self._data_dict = None
        self.paraicon = QIcon(CONFIG.ICON_PARA)
        if sel_mode == 0:
            self.sel_mode = QAbstractItemView.SingleSelection
        if sel_mode == 1:
            self.sel_mode = QAbstractItemView.ExtendedSelection
        
        self.setup()
        self.display_paras(files, dict_filetype)

    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(260, 550)
        self.verticalLayout = QVBoxLayout(self)
        self.line_edit_search = QLineEdit(self)
        self.line_edit_search.setMinimumSize(QSize(0, 24))
        self.line_edit_search.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.line_edit_search)
        self.preview_widget = QListWidget(self)
        self.preview_widget.setSelectionMode(self.sel_mode)
        self.verticalLayout.addWidget(self.preview_widget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_confirm)
#        暂时屏蔽添加按钮，预留！！！！！！！！！
        if self.sel_mode == QAbstractItemView.ExtendedSelection & 0==1:
            self.btn_add = QPushButton(self)
            self.btn_add.setMinimumSize(QSize(0, 24))
            self.btn_add.setMaximumSize(QSize(16777215, 24))
            self.horizontalLayout.addWidget(self.btn_add)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
#        暂时屏蔽添加按钮，预留！！！！！！！！！同上
        if self.sel_mode == QAbstractItemView.ExtendedSelection & 0==1:
            self.btn_add.clicked.connect(self.signal_add_paras)
        if self.sel_mode == QAbstractItemView.SingleSelection:
            self.preview_widget.itemDoubleClicked.connect(self.accept)
        self.line_edit_search.textChanged.connect(self.slot_search_para)
        
        self.load_data_dict()
        self.retranslateUi()
    
    def slot_search_para(self, para_name):
        
        if self.preview_widget:
            pattern = re.compile('.*' + para_name + '.*')
            count = self.preview_widget.count()
            for i in range(count):
                item = self.preview_widget.item(i)
                paraname = item.data(Qt.UserRole)
                para_alias = item.text()
                if re.match(pattern, paraname) or re.match(pattern, para_alias):
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def get_list_sel_paras(self):
        
        preview_widget = []
        for item in self.preview_widget.selectedItems():
            preview_widget.append(item.data(Qt.UserRole))
        return preview_widget
        
#    不显示时间
    def display_paras(self, files, dict_filetype):
        if files is None:
            return
        
        for file_dir in files:
            time_hide = False
            file = DataFile_Factory(file_dir, **dict_filetype[file_dir])
            paras = file.paras_in_file
            for para in paras:
                if time_hide:
                    if para not in self.get_preview_widget():
                        item = QListWidgetItem(para, self.preview_widget)
                        item.setIcon(self.paraicon)
                        if (self._data_dict and 
                            CONFIG.OPTION['data dict scope paralist'] and
                            para in self._data_dict):
                            if CONFIG.OPTION['data dict scope style'] == 0:
                                temp_str = para + '(' + self._data_dict[para][0] + ')'
                            if CONFIG.OPTION['data dict scope style'] == 1:
                                temp_str = para + '(' + self._data_dict[para][0] + ')'
                            if CONFIG.OPTION['data dict scope style'] == 2:
                                temp_str = self._data_dict[para][0] + '(' + para + ')'
                            item.setText(temp_str)
                        else:
                            item.setText(para)
                        item.setData(Qt.UserRole, para)
#                跳过第一个参数，这里默认第一个参数时间
                else:
                    time_hide = True
    
    def get_preview_widget(self):
        
        preview_widget = []
        count = self.preview_widget.count()
        for i in range(count):
            item = self.preview_widget.item(i)
            preview_widget.append(item.data(Qt.UserRole))
        return preview_widget
    
    def load_data_dict(self):
        
        try:
            with open(CONFIG.SETUP_DIR + r'\data\data_dicts\\' + CONFIG.OPTION['data dict version']) as f_obj:
                self._data_dict = json.load(f_obj)
        except:
            pass

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('SelParasDialog', '选择参数'))
        self.line_edit_search.setPlaceholderText(_translate('SelParasDialog', '过滤器'))
        self.btn_confirm.setText(_translate('SelParasDialog', '确定'))
#        暂时屏蔽添加按钮，预留！！！！！！！！！,同上
        if self.sel_mode == QAbstractItemView.ExtendedSelection and 0==1:
            self.btn_add.setText(_translate('SelParasDialog', '添加'))
        self.btn_cancel.setText(_translate('SelParasDialog', '取消'))
        
class SelfuncDialog(QDialog):

    signal_add_paras = pyqtSignal()
    
    def __init__(self, parent = None, df_func = None, sel_mode = 0):
        
        super().__init__(parent)
        
#        self._data_dict = None
#        self.paraicon = QIcon(CONFIG.ICON_PARA)
        if sel_mode == 0:
            self.sel_mode = QAbstractItemView.SingleSelection
        if sel_mode == 1:
            self.sel_mode = QAbstractItemView.ExtendedSelection
        
        self.setup()
        self.preview_widget.setColumnCount(2)
        self.preview_widget.setRowCount(len(df_func))
        
        self.display_paras(df_func)

    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(550, 550)
        self.verticalLayout = QVBoxLayout(self)
        self.line_edit_search = QLineEdit(self)
        self.line_edit_search.setMinimumSize(QSize(0, 24))
        self.line_edit_search.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.line_edit_search)
        self.preview_widget = QTableWidget(self)
        self.preview_widget.setSelectionMode(self.sel_mode)
        self.preview_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.preview_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.preview_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.preview_widget.horizontalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.preview_widget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_confirm)
#        暂时屏蔽添加按钮，预留！！！！！！！！！
        if self.sel_mode == QAbstractItemView.ExtendedSelection & 0==1:
            self.btn_add = QPushButton(self)
            self.btn_add.setMinimumSize(QSize(0, 24))
            self.btn_add.setMaximumSize(QSize(16777215, 24))
            self.horizontalLayout.addWidget(self.btn_add)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
#        暂时屏蔽添加按钮，预留！！！！！！！！！同上
        if self.sel_mode == QAbstractItemView.ExtendedSelection & 0==1:
            self.btn_add.clicked.connect(self.signal_add_paras)
        if self.sel_mode == QAbstractItemView.SingleSelection:
            self.preview_widget.itemDoubleClicked.connect(self.accept)
        self.line_edit_search.textChanged.connect(self.slot_search_func)
        
#        self.load_desc()
        self.retranslateUi()
    
    def slot_search_func(self, func_name):
        
        if self.preview_widget:
            pattern = re.compile('.*' + func_name + '.*')
            count = self.preview_widget.rowCount()
            for i in range(count):
                item = self.preview_widget.item(i,0)
                funcname = item.data(Qt.UserRole)
                func_alias = item.text()
                if re.match(pattern, funcname) or re.match(pattern, func_alias):
                    self.preview_widget.setRowHidden(i, False)
                else:
                    self.preview_widget.setRowHidden(i, True)

    def get_list_sel_paras(self):
        
        preview_widget = []
        for item in self.preview_widget.selectedItems():
            
            preview_widget.append(item.data(Qt.UserRole))
        return preview_widget
        
#    不显示时间
    def display_paras(self, df_func):
        if df_func is not None:
            for i in range(len(df_func)):
                item0 = QTableWidgetItem(df_func.iat[i,0])
                item1 = QTableWidgetItem(df_func.iat[i,1])
                item0.setData(Qt.UserRole, df_func.iat[i,0])
                self.preview_widget.setItem(i,0,item0)
                self.preview_widget.setItem(i,1,item1)
                
    
    def get_preview_widget(self):
        
        preview_widget = []
        count = self.preview_widget.count()
        for i in range(count):
            item = self.preview_widget.item(i)
            preview_widget.append(item.data(Qt.UserRole))
        return preview_widget
    
    def load_desc(self):
        
        try:
            filedir = CONFIG.SETUP_DIR + r'\data\func_desc.txt'
            funcfile = DataFile(filedir, sep='\t')
            df_func = funcfile.all_input()
            self.df_func = df_func
        except:
            pass

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('SelfuncsDialog', '选择函数'))
        self.line_edit_search.setPlaceholderText(_translate('SelParasDialog', '过滤器'))
        self.btn_confirm.setText(_translate('SelfuncsDialog', '确定'))
#        暂时屏蔽添加按钮，预留！！！！！！！！！,同上
        if self.sel_mode == QAbstractItemView.ExtendedSelection and 0==1:
            self.btn_add.setText(_translate('SelfuncsDialog', '添加'))
        self.btn_cancel.setText(_translate('SelfuncsDialog', '取消'))



class SelXParaDialog(SelParasDialog):
    
    def __init__(self, parent = None, files = [], sel_mode = 0, dict_filetype = None):
        
        super().__init__(parent, files, sel_mode, dict_filetype)
        
    def display_paras(self, files, dict_filetype):
        if files is None:
            return
        
        for file_dir in files:
            time_hide = False
            file = Normal_DataFile(file_dir)
            paras = file.paras_in_file
            for para in paras:
                if time_hide:
                    if para not in self.get_preview_widget():
                        item = QListWidgetItem(para, self.preview_widget)
                        item.setIcon(self.paraicon)
                        if (self._data_dict and 
                            CONFIG.OPTION['data dict scope paralist'] and
                            para in self._data_dict):
                            if CONFIG.OPTION['data dict scope style'] == 0:
                                temp_str = para + '(' + self._data_dict[para][0] + ')'
                            if CONFIG.OPTION['data dict scope style'] == 1:
                                temp_str = para + '(' + self._data_dict[para][0] + ')'
                            if CONFIG.OPTION['data dict scope style'] == 2:
                                temp_str = self._data_dict[para][0] + '(' + para + ')'
                            item.setText(temp_str)
                        else:
                            item.setText(para)
                        item.setData(Qt.UserRole, (para, file_dir))
#                跳过第一个参数，这里默认第一个参数时间
                else:
                    time_hide = True
        
class ParasListDropEvent(QListWidget):

    signal_drop_paras = pyqtSignal(tuple)    

    def __init__(self, parent = None, name = 'yaxis'):
        super().__init__(parent)
#        接受拖放
        self.setAcceptDrops(True)
        self.name = name
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._data_dict = None

#    重写拖放相关的事件
#    设置部件可接受的MIME type列表，此处的类型是自定义的
    def mimeTypes(self):
        return ['application/x-parasname']
#    拖进事件处理    
    def dragEnterEvent(self, event):
#        如果拖进来的时树列表才接受
        if event.mimeData().hasFormat('application/x-parasname'):
            event.acceptProposedAction()
        else:
            event.ignore()
#     放下事件处理   
            
    def dropEvent(self, event):
        
        paras = {}
        if event.mimeData().hasFormat('application/x-parasname'):
            item_data = event.mimeData().data('application/x-parasname')
            item_stream = QDataStream(item_data, QIODevice.ReadOnly)
#            对拖进来的数据进行解析
#            按数据流中的参数排列顺序存储参数到此参数列表
            sorted_paras = []
            while (not item_stream.atEnd()):
                paraname = item_stream.readQString()
                file_dir = item_stream.readQString()
                sorted_paras.append((paraname, file_dir))
                if not (file_dir in paras):
                    paras[file_dir] = []
                    paras[file_dir].append(paraname)
                else:
                    paras[file_dir].append(paraname)  
            self.signal_drop_paras.emit((self.name, paras, sorted_paras))
            event.acceptProposedAction()
        else:
            event.ignore()
            
#    def replace_para(self):
        

#    def dropEvent(self, event):
#        
#        sorted_paras = []
#        if event.mimeData().hasFormat('application/x-parasname'):
#            item_data = event.mimeData().data('application/x-parasname')
#            item_stream = QDataStream(item_data, QIODevice.ReadOnly)
#            while (not item_stream.atEnd()):
##                不同于绘图的解析，因为此处更关注的是参数的排列顺序
#                paraname = item_stream.readQString()
#                file_dir = item_stream.readQString()
#                sorted_paras.append((paraname, file_dir))
#            self.signal_drop_paras.emit(sorted_paras)
#            event.acceptProposedAction()
#        else:
#            event.ignore()

class ParaSetupDialog(QDialog):
    
    signal_accept = pyqtSignal(tuple)
    
    def __init__(self, parent = None, current_files = None, data_dict = None, dict_filetype  = None):
        super().__init__(parent)
#        self.setAcceptDrops(True)
        self.setup()
        self.setWindowModality(Qt.NonModal)
        self.dictdata = None  
        self.sorted_paras = None
        self._current_files = current_files
        self._data_dict = data_dict
        self._dict_filetype = dict_filetype 
        
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font) 
        self.resize(550, 450)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4 = QHBoxLayout()
        self.gb_xaxis = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.gb_xaxis)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.btn_sel_x = QToolButton(self.gb_xaxis)
        self.btn_sel_x.setMinimumSize(QSize(30, 30))
        self.btn_sel_x.setMaximumSize(QSize(30, 30))
        self.btn_sel_x.setIconSize(QSize(22, 22))
        self.horizontalLayout_3.addWidget(self.btn_sel_x)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.list_wi_xpara = ParasListDropEvent(self.gb_xaxis, 'xaxis')
        self.list_wi_xpara.addItem('')
        self.verticalLayout.addWidget(self.list_wi_xpara)
        self.horizontalLayout_4.addWidget(self.gb_xaxis)
        self.gb_yaxis = QGroupBox(self)
        self.verticalLayout_2 = QVBoxLayout(self.gb_yaxis)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.btn_up = QToolButton(self.gb_yaxis)
        self.btn_up.setIcon(QIcon(CONFIG.ICON_UP))
        self.btn_up.setMinimumSize(QSize(30, 30))
        self.btn_up.setMaximumSize(QSize(30, 30))
        self.btn_up.setIconSize(QSize(22, 22))
        self.horizontalLayout_2.addWidget(self.btn_up)
        self.btn_down = QToolButton(self.gb_yaxis)
        self.btn_down.setIcon(QIcon(CONFIG.ICON_DOWN))
        self.btn_down.setMinimumSize(QSize(30, 30))
        self.btn_down.setMaximumSize(QSize(30, 30))
        self.btn_down.setIconSize(QSize(22, 22))
        self.horizontalLayout_2.addWidget(self.btn_down)
        self.btn_del = QToolButton(self.gb_yaxis)
        self.btn_del.setIcon(QIcon(CONFIG.ICON_DEL))
        self.btn_del.setMinimumSize(QSize(30, 30))
        self.btn_del.setMaximumSize(QSize(30, 30))
        self.btn_del.setIconSize(QSize(22, 22))
        self.horizontalLayout_2.addWidget(self.btn_del)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.list_wi_yparas = ParasListDropEvent(self.gb_yaxis)
        self.verticalLayout_2.addWidget(self.list_wi_yparas)
        self.horizontalLayout_4.addWidget(self.gb_yaxis)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi()
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.list_wi_xpara.signal_drop_paras.connect(self.slot_display_paras)
        self.list_wi_yparas.signal_drop_paras.connect(self.slot_display_paras)
        self.btn_up.clicked.connect(self.slot_up_para)
        self.btn_down.clicked.connect(self.slot_down_para)
        self.btn_del.clicked.connect(self.slot_delete_paras)
        self.btn_sel_x.clicked.connect(self.slot_change_paras)

    def accept(self):
        signal_tuple = self.get_paras()
        QDialog.accept(self)
        self.signal_accept.emit(signal_tuple)
    
    def slot_display_paras(self, flag_datadict_and_paralist : tuple):
        
        flag, datadict, sorted_paras = flag_datadict_and_paralist
        
        if flag == 'xaxis' and sorted_paras:
            if len(sorted_paras) != 1:
                print_msg = 'X轴参数个数不为1，将选用第一个参数作为X轴参数：'
                ms_box = QMessageBox(QMessageBox.Information,
                                     QCoreApplication.translate('ParaSetupDialog', '提示'),
                                     QCoreApplication.translate('ParaSetupDialog', print_msg),
                                     QMessageBox.Ok,
                                     self)
#                xpara = sorted_paras[0]
                ms_box.exec_()
            xpara, file_dir = sorted_paras[0]
            if (self._data_dict and 
                CONFIG.OPTION['data dict scope paralist'] and
                xpara in self._data_dict):
                if CONFIG.OPTION['data dict scope style'] == 0:
                    temp_str = self._data_dict[xpara][0]
                if CONFIG.OPTION['data dict scope style'] == 1:
                    temp_str = xpara + '(' + self._data_dict[xpara][0] + ')'
                if CONFIG.OPTION['data dict scope style'] == 2:
                    temp_str = self._data_dict[xpara][0] + '(' + xpara + ')'
                self.list_wi_xpara.item(0).setText(temp_str)
                
            else:
                self.list_wi_xpara.item(0).setText(xpara)
            self.list_wi_xpara.item(0).setData(Qt.UserRole, (xpara, file_dir))

            
        if flag == 'yaxis' and sorted_paras:
            
            ex_paras = []
#            norfile_list = {}
            
            for para_info in sorted_paras:
                paraname, file_dir = para_info
#                判断导入的参数是否已存在
                if self.is_in_sel_paras((paraname, file_dir)):
                    ex_paras.append(paraname)
                else:
#                    避免重复创建文件对象
#                    if not (file_dir in norfile_list):
#                        norfile_list[file_dir] = Normal_DataFile(file_dir)
#                    file = norfile_list[file_dir]
#                    filename = file.filename
                    item_para = QListWidgetItem(self.list_wi_yparas)
                    
                    if (self._data_dict and 
                        CONFIG.OPTION['data dict scope paralist'] and
                        paraname in self._data_dict):
                        if CONFIG.OPTION['data dict scope style'] == 0:
                            temp_str = self._data_dict[paraname][0]
                        if CONFIG.OPTION['data dict scope style'] == 1:
                            temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                        if CONFIG.OPTION['data dict scope style'] == 2:
                            temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                        item_para.setText(temp_str)
                    else:
                        item_para.setText(paraname)
                    item_para.setData(Qt.UserRole, (paraname, file_dir))
#                    item_para.setText(1, filename)
#                    item_para.setData(1, Qt.UserRole, file_dir)
#                    item_para.setText(2, file.time_range[0])
#                    item_para.setText(3, file.time_range[1])
#                    item_para.setText(4, str(file.sample_frequency))
            if ex_paras:
                print_para = '以下参数已存在：'
                for pa in ex_paras:
                    print_para += ('<br>' + pa)
                ms_box = QMessageBox(QMessageBox.Information,
                                     QCoreApplication.translate('ParaSetupDialog', '导入参数提示'),
                                     QCoreApplication.translate('ParaSetupDialog', print_para),
                                     QMessageBox.Ok,
                                     self)
                ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                ms_box.exec_()


#x轴toolbutton操作
    def slot_change_paras(self):
#        单选dialog
        dialog = SelXParaDialog(self, self._current_files, 0, self._dict_filetype)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            paras = dialog.get_list_sel_paras()
            if paras:
                if len(paras) != 1:
                    print_msg = 'X轴参数个数不为1，将选用第一个参数作为X轴参数：'
                    ms_box = QMessageBox(QMessageBox.Information,
                                         QCoreApplication.translate('ParaSetupDialog', '提示'),
                                         QCoreApplication.translate('ParaSetupDialog', print_msg),
                                         QMessageBox.Ok,
                                         self)
    #                xpara = sorted_paras[0]
                    ms_box.exec_()
                xpara, file_dir = paras[0]
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope paralist'] and
                    xpara in self._data_dict):
                    if CONFIG.OPTION['data dict scope style'] == 0:
                        temp_str = self._data_dict[xpara][0]
                    if CONFIG.OPTION['data dict scope style'] == 1:
                        temp_str = xpara + '(' + self._data_dict[xpara][0] + ')'
                    if CONFIG.OPTION['data dict scope style'] == 2:
                        temp_str = self._data_dict[xpara][0] + '(' + xpara + ')'
                    self.list_wi_xpara.item(0).setText(temp_str)
                    
                else:
                    self.list_wi_xpara.item(0).setText(xpara)
                    
#                self.list_wi_xpara.item(0).setText(xpara)
                self.list_wi_xpara.item(0).setData(Qt.UserRole, (xpara, file_dir))
                
                
#    def slot_set_timeaxis(self):
#        self.list_wi_xpara.item(0).setText('Time（时间）')

#Y轴toolbuttton操作 

#    def slot_add_paras(self):
##        单选dialog
#        dialog = SelParasDialog_xparasetting(self, self._current_files, 1)
#        return_signal = dialog.exec_()
#        if (return_signal == QDialog.Accepted):
#            paraslist = dialog.get_list_sel_paras()
#            if paraslist:
#                
#                ex_paras = []
#    #            norfile_list = {}
#                
#                for para_info in paraslist:
#                    paraname, file_dir = para_info
#    #                判断导入的参数是否已存在
#                    if self.is_in_sel_paras((paraname, file_dir)):
#                        ex_paras.append(paraname)
#                    else:
#    #                    避免重复创建文件对象
#    #                    if not (file_dir in norfile_list):
#    #                        norfile_list[file_dir] = Normal_DataFile(file_dir)
#    #                    file = norfile_list[file_dir]
#    #                    filename = file.filename
#                        item_para = QListWidgetItem(self.list_wi_yparas)
#                        
#                        if (self._data_dict and 
#                            CONFIG.OPTION['data dict scope paralist'] and
#                            paraname in self._data_dict):
#                            if CONFIG.OPTION['data dict scope style'] == 0:
#                                temp_str = self._data_dict[paraname][0]
#                            if CONFIG.OPTION['data dict scope style'] == 1:
#                                temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
#                            if CONFIG.OPTION['data dict scope style'] == 2:
#                                temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
#                            item_para.setText(temp_str)
#                        else:
#                            item_para.setText(paraname)
#                        item_para.setData(Qt.UserRole, (paraname, file_dir))
#    #                    item_para.setText(1, filename)
#    #                    item_para.setData(1, Qt.UserRole, file_dir)
#    #                    item_para.setText(2, file.time_range[0])
#    #                    item_para.setText(3, file.time_range[1])
#    #                    item_para.setText(4, str(file.sample_frequency))
#                if ex_paras:
#                    print_para = '以下参数已存在：'
#                    for pa in ex_paras:
#                        print_para += ('<br>' + pa)
#                    ms_box = QMessageBox(QMessageBox.Information,
#                                         QCoreApplication.translate('DataAnalysisWindow', '导入参数提示'),
#                                         QCoreApplication.translate('DataAnalysisWindow', print_para),
#                                         QMessageBox.Ok,
#                                         self)
#                    ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
#                    ms_box.exec_()
               
    def slot_up_para(self):
        
        if self.list_wi_yparas:
            row = self.list_wi_yparas.row(self.list_wi_yparas.currentItem())
            item = self.list_wi_yparas.takeItem(row)
            if row == 0:
                self.list_wi_yparas.insertItem(0, item)
                self.list_wi_yparas.setCurrentItem(item)
            else:
                self.list_wi_yparas.insertItem(row - 1, item)
                self.list_wi_yparas.setCurrentItem(item)
    
    def slot_down_para(self):

        if self.list_wi_yparas:
            count = self.list_wi_yparas.count()
            row = self.list_wi_yparas.row(self.list_wi_yparas.currentItem())
            item = self.list_wi_yparas.takeItem(row)
            if row == count - 1:
                self.list_wi_yparas.insertItem(count - 1, item)
                self.list_wi_yparas.setCurrentItem(item)
            else:
                self.list_wi_yparas.insertItem(row + 1, item)
                self.list_wi_yparas.setCurrentItem(item)
                
    def slot_delete_paras(self):
        
        sel_items = self.list_wi_yparas.selectedItems()
        if len(sel_items):
            message = QMessageBox.warning(self,
                          QCoreApplication.translate('ParaSetupDialog', '删除参数'),
                          QCoreApplication.translate('ParaSetupDialog', '确定要删除所选参数吗'),
                          QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                for item in sel_items:
                    self.list_wi_yparas.takeItem(self.list_wi_yparas.row(item))

    def is_in_sel_paras(self, file_tuple):
        paraname, file_dir = file_tuple
        count = self.list_wi_yparas.count()
        for i in range(count):
            item = self.list_wi_yparas.item(i)
            pn = item.data(Qt.UserRole)[0]
            fd = item.data(Qt.UserRole)[1]
            if pn == paraname and fd == file_dir:
                return True
        return False 

    def get_y_paras(self):
        
        result = {}
        sorted_paras = []
        dict_df = {}
        if self.list_wi_yparas:
            count = self.list_wi_yparas.count()
            for i in range(count):
                item = self.list_wi_yparas.item(i)
                sorted_paras.append((item.data(Qt.UserRole)[0], item.data(Qt.UserRole)[1]))
                file_dir = item.data(Qt.UserRole)[1]
                if file_dir[0] == '_':
                    if file_dir in dict_df:
                        dict_df[file_dir].append(item.data(Qt.UserRole)[0])
                    else:
                        dict_df[file_dir] = []
                        dict_df[file_dir].append(item.data(Qt.UserRole)[0])
                else:
                    if file_dir in result:
                        result[file_dir].append(item.data(Qt.UserRole)[0])
                    else:
                        result[file_dir] = []
                        result[file_dir].append(item.data(Qt.UserRole)[0])
            for name in dict_df:
                result[name] = self.dictdata[name].get_sub_data(dict_df[name])
        return (result, sorted_paras)

    def get_x_paras(self):
        
        if self.list_wi_xpara:
            item = self.list_wi_xpara.item(0)
            paraname, file_dir = item.data(Qt.UserRole)
#                xpara不应加入self.sorted_paras
#                if item.data(Qt.UserRole) not in self.sorted_paras:
#                    self.sorted_paras.append((paraname, file_dir))
            if file_dir in self.dictdata:
                if paraname not in self.dictdata[file_dir]:
                    self.dictdata[file_dir].append(paraname)
            else:
                self.dictdata[file_dir] = []
                self.dictdata[file_dir].append(paraname)
            xpara = paraname
        return (xpara, file_dir)
    
    def get_paras(self):
        
        datadict, paralist = self.get_y_paras()
        self.dictdata = datadict
        self.sorted_paras = paralist
        xp = self.get_x_paras()
        self.sorted_paras.insert(0, xp)
    
        return (self.dictdata, self.sorted_paras)

    def retranslateUi(self):
        
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('ParaSetupDialog', '创建自定义坐标图'))
        self.gb_xaxis.setTitle(_translate('ParaSetupDialog', 'X轴参数设置'))
        self.btn_sel_x.setText(_translate('ParaSetupDialog', '...'))
        self.gb_yaxis.setTitle(_translate('ParaSetupDialog', 'Y轴参数设置'))
        self.btn_up.setText(_translate('ParaSetupDialog', '...'))
        self.btn_down.setText(_translate('ParaSetupDialog', '...'))
        self.btn_del.setText(_translate('ParaSetupDialog', '...'))
        self.btn_confirm.setText(_translate('ParaSetupDialog', '确定'))
        self.btn_cancel.setText(_translate('ParaSetupDialog', '取消')) 

class Base_LineSettingDialog(QDialog):

#    linetype = 0为任意线，1为垂直线，2为水平线
    def __init__(self, parent = None, line : Line2D = None):
        
        super().__init__(parent)

        self.markline = line
        self.line_xdata = line.get_xdata()
        self.line_ydata = line.get_ydata()
        self.linetype = self.linetype(line)

        self.line_ls = line.get_linestyle()
        self.line_lw = line.get_linewidth()
        self.line_marker = line.get_marker()
#        按#RRGGBB格式赋值
        self.line_color = Color.to_hex(line.get_color())
        
        self.enum_linestyle = ['None','-', '--', '-.', ':']
        self.enum_linestyle_name = ['Nothing', 'Solid', 'Dashed', 
                                    'Dashdot', 'Dotted']
        self.enum_marker = ['None', '.', 'o', 'v', '^', '<', '>', '1', '2',
                            '3', '4', 's', '*', '+', 'x', 'D']
        self.enum_marker_name = ['Nothing', 'Point', 'Circle', 'Triangle_down',
                                 'Triangle_up', 'Triangle_left', 'Triangle_right',
                                 'Tri_down', 'Tri_up', 'Tri_left', 'Tri_right', 
                                 'Square', 'Star', 'Plus', 'x', 'Diamond']
#        判断是否是取值标记线，是的话就将文字标注对象保存起来
        self.text_mark = None
        ax = self.markline.axes
        if ax:
            list_text = ax.findobj(Annotation)
            for text in list_text:
                if self.markline.get_gid() and self.markline.get_gid() == text.get_gid():
                    self.text_mark = text
        
        self.setup()
    
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)        
        self.resize(320, 290)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.label_title = QLabel(self)
        self.label_title.setMinimumSize(QSize(120, 24))
        self.label_title.setMaximumSize(QSize(16777215, 24))
        titile_font = QFont()
        titile_font.setBold(True)
        titile_font.setWeight(75)
        self.label_title.setFont(titile_font)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_title)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        
        self.hlayout_x0 = QHBoxLayout()
        self.label_line_x0 = QLabel(self)
        self.label_line_x0.setMinimumSize(QSize(75, 24))
        self.label_line_x0.setMaximumSize(QSize(75, 24))
        self.hlayout_x0.addWidget(self.label_line_x0)
        self.line_edit_line_x0 = QLineEdit(self)
        self.line_edit_line_x0.setMinimumSize(QSize(120, 24))
        self.line_edit_line_x0.setMaximumSize(QSize(16777215, 24))
        self.hlayout_x0.addWidget(self.line_edit_line_x0)
        self.verticalLayout.addLayout(self.hlayout_x0)
        self.hlayout_x1 = QHBoxLayout()
        self.label_line_x1 = QLabel(self)
        self.label_line_x1.setMinimumSize(QSize(75, 24))
        self.label_line_x1.setMaximumSize(QSize(75, 24))
        self.hlayout_x1.addWidget(self.label_line_x1)
        self.line_edit_line_x1 = QLineEdit(self)
        self.line_edit_line_x1.setMinimumSize(QSize(120, 24))
        self.line_edit_line_x1.setMaximumSize(QSize(16777215, 24))
        self.hlayout_x1.addWidget(self.line_edit_line_x1)
        self.verticalLayout.addLayout(self.hlayout_x1)
        self.hlayout_y0 = QHBoxLayout()
        self.label_line_y0 = QLabel(self)
        self.label_line_y0.setMinimumSize(QSize(75, 24))
        self.label_line_y0.setMaximumSize(QSize(75, 24))
        self.hlayout_y0.addWidget(self.label_line_y0)
        self.line_edit_line_y0 = QLineEdit(self)
        self.line_edit_line_y0.setMinimumSize(QSize(120, 24))
        self.line_edit_line_y0.setMaximumSize(QSize(16777215, 24))
        self.line_edit_line_y0.setPlaceholderText('')
        self.hlayout_y0.addWidget(self.line_edit_line_y0)
        self.verticalLayout.addLayout(self.hlayout_y0)
        
        if self.linetype == 'Vertical':
            self.label_title.setText(QCoreApplication.translate('LineSettingDialog',
                                                                '垂直标记线'))
            self.label_line_x0.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '标记线位置'))
            self.label_line_x1.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '标记线起始'))
            self.label_line_y0.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '标记线终止'))
#            istime = False
#            转换成功不一定就能判断这个是时间
            try:
#                将浮点值转换为时间，由于经过转换，有误差
                text_x0 = self.value_to_text(self.line_xdata[0])
#                time = mdates.num2date(self.line_xdata[0]).time().isoformat(timespec='milliseconds')
#                istime = True
            except:
                pass
            self.line_edit_line_x0.setText(text_x0)
            
            self.line_edit_line_x1.setText(str(self.line_ydata[0]))
            self.line_edit_line_y0.setText(str(self.line_ydata[1]))
        if self.linetype == 'Horizontal':
            self.label_title.setText(QCoreApplication.translate('LineSettingDialog',
                                                                '水平标记线'))
            self.label_line_x0.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '标记线位置'))
            self.label_line_x1.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '标记线起始'))
            self.label_line_y0.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '标记线终止'))
            self.line_edit_line_x0.setText(str(self.line_ydata[0]))
            self.line_edit_line_x1.setText(str(self.line_xdata[0]))
            self.line_edit_line_y0.setText(str(self.line_xdata[1]))            
        if self.linetype == 'Line':
            self.hlayout_y1 = QHBoxLayout()
            self.label_line_y1 = QLabel(self)
            self.label_line_y1.setMinimumSize(QSize(75, 24))
            self.label_line_y1.setMaximumSize(QSize(75, 24))
            self.hlayout_y1.addWidget(self.label_line_y1)
            self.line_edit_line_y1 = QLineEdit(self)
            self.line_edit_line_y1.setMinimumSize(QSize(120, 24))
            self.line_edit_line_y1.setMaximumSize(QSize(16777215, 24))
            self.line_edit_line_y1.setPlaceholderText('')
            self.hlayout_y1.addWidget(self.line_edit_line_y1)
            self.verticalLayout.addLayout(self.hlayout_y1)
            
            self.label_title.setText(QCoreApplication.translate('LineSettingDialog',
                                                                '标记线'))
            self.label_line_x0.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '左端点横坐标'))
            self.label_line_x1.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '右端点横坐标'))
            self.label_line_y0.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '左端点纵坐标'))
            self.label_line_y1.setText(QCoreApplication.translate('LineSettingDialog',
                                                                  '右端点纵坐标'))
#            istime = False
#            转换成功不一定就能判断这个是时间
            try:
#                将浮点值转换为时间，由于经过转换，有误差
#                stime = mdates.num2date(self.line_xdata[0]).time().isoformat(timespec='milliseconds')
                start = self.value_to_text(self.line_xdata[0])
                end = self.value_to_text(self.line_xdata[1])
#                etime = mdates.num2date(self.line_xdata[1]).time().isoformat(timespec='milliseconds')
#                istime = True
            except:
                pass
            
            self.line_edit_line_x0.setText(start)
            self.line_edit_line_x1.setText(end)
#            else:
#                self.line_edit_line_x0.setText(str(self.line_xdata[0]))
#                self.line_edit_line_x1.setText(str(self.line_xdata[1]))
            self.line_edit_line_y0.setText(str(self.line_ydata[0]))
            self.line_edit_line_y1.setText(str(self.line_ydata[1]))

        self.horizontalLayout_2 = QHBoxLayout()
        self.label_line_ls = QLabel(self)
        self.label_line_ls.setMinimumSize(QSize(75, 24))
        self.label_line_ls.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_2.addWidget(self.label_line_ls)
        self.combo_box_linestyle = QComboBox(self)
        self.combo_box_linestyle.setMinimumSize(QSize(120, 24))
        self.combo_box_linestyle.setMaximumSize(QSize(16777215, 24))
        
        count = len(self.enum_linestyle)
        for i in range(count):
            self.combo_box_linestyle.addItem('')
            self.combo_box_linestyle.setItemData(i, self.enum_linestyle[i], Qt.UserRole)
        index = self.enum_linestyle.index(self.line_ls)
        self.combo_box_linestyle.setCurrentIndex(index)
        
        self.horizontalLayout_2.addWidget(self.combo_box_linestyle)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_line_lw = QLabel(self)
        self.label_line_lw.setMinimumSize(QSize(75, 24))
        self.label_line_lw.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_3.addWidget(self.label_line_lw)
        self.line_edit_line_width = QLineEdit(self)
        self.line_edit_line_width.setMinimumSize(QSize(120, 24))
        self.line_edit_line_width.setMaximumSize(QSize(16777215, 24))
        self.line_edit_line_width.setText(str(self.line_lw))
        self.horizontalLayout_3.addWidget(self.line_edit_line_width)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_line_lc = QLabel(self)
        self.label_line_lc.setMinimumSize(QSize(75, 24))
        self.label_line_lc.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_4.addWidget(self.label_line_lc)
        self.color_view = QLabel(self)
        self.color_view.setMinimumSize(QSize(90, 20))
        self.color_view.setMaximumSize(QSize(16777215, 20))
        self.color_view.setPalette(QPalette(QColor(self.line_color)))
        self.color_view.setAutoFillBackground(True)
        self.color_view.setText('')
        self.horizontalLayout_4.addWidget(self.color_view)
        self.tool_btn_line_color = QToolButton(self)
        self.tool_btn_line_color.setMinimumSize(QSize(24, 24))
        self.tool_btn_line_color.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_4.addWidget(self.tool_btn_line_color)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QHBoxLayout()
        self.label_line_marker = QLabel(self)
        self.label_line_marker.setMinimumSize(QSize(75, 24))
        self.label_line_marker.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_6.addWidget(self.label_line_marker)
        self.combo_box_line_marker = QComboBox(self)
        self.combo_box_line_marker.setMinimumSize(QSize(120, 24))
        self.combo_box_line_marker.setMaximumSize(QSize(16777215, 24))
        
        count = len(self.enum_marker)
        for i in range(count):
            self.combo_box_line_marker.addItem('')
            self.combo_box_line_marker.setItemData(i, self.enum_marker[i], Qt.UserRole)
        index = self.enum_marker.index(self.line_marker)
        self.combo_box_line_marker.setCurrentIndex(index)
        
        self.horizontalLayout_6.addWidget(self.combo_box_line_marker)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_5 = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_5.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_5.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi()
        
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.tool_btn_line_color.clicked.connect(self.slot_sel_color)
        
    def accept(self):
        
        try:
            str_x0 = self.line_edit_line_x0.text()
            str_x1 = self.line_edit_line_x1.text()
            str_y0 = self.line_edit_line_y0.text()
            if self.linetype == 'Line':
                str_y1 = self.line_edit_line_y1.text()
    #                将时间转换为浮点值坐标
                x0 = self.text_to_value(str_x0)
                x1 = self.text_to_value(str_x1)
#                x0 = mdates.date2num(Time_Model.str_to_datetime(str_x0))
#                x1 = mdates.date2num(Time_Model.str_to_datetime(str_x1))
    #            python3.7才可使用fromisoformat函数
    #            x0 = mdates.date2num(datetime.fromisoformat('1900-01-01*' + x[0]))
    #            x1 = mdates.date2num(datetime.fromisoformat('1900-01-01*' + x[1]))
                self.line_xdata = [x0, x1]
                self.line_ydata = [float(str_y0), float(str_y1)]
            if self.linetype == 'Vertical':
                x = self.text_to_value(str_x0)
#                x = mdates.date2num(Time_Model.str_to_datetime(str_x0))
    #            x = mdates.date2num(datetime.fromisoformat('1900-01-01*' + str_x))
                self.line_xdata = [x, x]
                if self.is_in_01(float(str_x1), float(str_y0)):
                    self.line_ydata = [float(str_x1), float(str_y0)]
            if self.linetype == 'Horizontal':
                if self.is_in_01(float(str_x1), float(str_y0)):
                    self.line_xdata = [float(str_x1), float(str_y0)]
                self.line_ydata = [float(str_x0), float(str_x0)]
                
            self.line_lw = float(self.line_edit_line_width.text())
        except:
            pass
        self.line_ls = self.combo_box_linestyle.currentData()
        self.line_marker = self.combo_box_line_marker.currentData()
        
        self.markline.set_xdata(self.line_xdata)
        self.markline.set_ydata(self.line_ydata)
        self.markline.set_linewidth(self.line_lw)
        self.markline.set_linestyle(self.line_ls)
        self.markline.set_color(self.line_color)
        self.markline.set_marker(self.line_marker)
        
        QDialog.accept(self)
        
    def slot_sel_color(self):
        
        color = QColorDialog.getColor(QColor(self.line_color), self, 'Select Color')
        self.color_view.setPalette(QPalette(color))
#        按##RRGGBB的格式赋值颜色
        self.line_color = color.name()
        
    def linetype(self, line : Line2D):
        
        x0 = line.get_xdata()[0]
        x1 = line.get_xdata()[1]
        y0 = line.get_ydata()[0]
        y1 = line.get_ydata()[1]
        if (x0 == x1 and self.is_in_01(y0, y1)):
            return 'Vertical'
        if (y0 == y1 and self.is_in_01(x0, x1)):
            return 'Horizontal'
        return 'Line'
    
#    判断区间[left, right]是否在区间[0, 1]内
    def is_in_01(self, left, right):
        
        if left > right:
            return False
        else:
            if (left >= 0 and right <= 1):
                return True
            else:
                return False
            
    def value_to_text(self, value):
        text = str(value)            
        return text
    
    def text_to_value(self, text):
        value = float(text)
        return value
    
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('LineSettingDialog', '标记线设置'))
        self.label_line_ls.setText(_translate('LineSettingDialog', '线型'))
        self.label_line_lw.setText(_translate('LineSettingDialog', '线宽'))
        self.label_line_lc.setText(_translate('LineSettingDialog', '线条颜色'))
        self.label_line_marker.setText(_translate('LineSettingDialog', '标记'))
        self.tool_btn_line_color.setText(_translate('LineSettingDialog', 'C'))
        self.btn_confirm.setText(_translate('LineSettingDialog', '确定'))
        self.btn_cancel.setText(_translate('LineSettingDialog', '取消'))
        count = len(self.enum_linestyle_name)
        for i in range(count):
            self.combo_box_linestyle.setItemText(i, _translate('LineSettingDialog',
                                                               self.enum_linestyle_name[i]))
        count = len(self.enum_marker_name)
        for i in range(count):
            self.combo_box_line_marker.setItemText(i, _translate('LineSettingDialog',
                                                               self.enum_marker_name[i]))
    

class LineSettingDialog(Base_LineSettingDialog):
    
    def __init__(self, parent = None, line : Line2D = None):

        super().__init__(parent, line)
        if self.linetype != 'Horizontal':
            self.line_edit_line_x0.editingFinished.connect(self.time_change)
        if self.linetype == 'Line':
            self.line_edit_line_x1.editingFinished.connect(self.time_change)
            
    def time_change(self):
        
        sender = QObject.sender(self)
        time = sender.text()
        if Time_Model.is_std_format(time):
            if sender == self.line_edit_line_x0:
                self.line_edit_line_x0.setText(Time_Model.timestr_to_stdtimestr(time))
            if sender == self.line_edit_line_x1:
                self.line_edit_line_x1.setText(Time_Model.timestr_to_stdtimestr(time))
        else:
            if sender == self.line_edit_line_x0:
                self.line_edit_line_x0.setText(self.value_to_text(self.line_xdata[0]))
            if sender == self.line_edit_line_x1:
                self.line_edit_line_x1.setText(self.value_to_text(self.line_xdata[1]))
            QMessageBox.information(self,
                            QCoreApplication.translate('LineSettingDialog', '输入提示'),
                            QCoreApplication.translate('LineSettingDialog', '''<b>请输入正确时间格式</b>
                                                       <br>HH
                                                       <br>HH:MM
                                                       <br>HH:MM:SS
                                                       <br>HH:MM:SS.FFF
                                                       <br>HH:MM:SS:FFF'''))

    def value_to_text(self, value):
        time = mdates.num2date(value).time().isoformat(timespec='milliseconds')
        text = str(time)
        return text
    
    def text_to_value(self, text):
        
        value = mdates.date2num(Time_Model.str_to_datetime(text))
        return value
    
    

class AnnotationSettingDialog(QDialog):
    
    def __init__(self, parent = None, annotation : Annotation = None):
        
        super().__init__(parent)
        
        self.annotation = annotation
        self.text = annotation.get_text()
        self.text_rotation = annotation.get_rotation()
        self.enum_text_rotation = [0.0, 90.0]
        self.enum_text_rotation_name = ['Horizontal', 'Vertical']
        self.text_size = annotation.get_fontsize()
        self.text_color = Color.to_hex(annotation.get_color())
        self.text_style = annotation.get_style()
        self.text_arrow = annotation.arrow_patch.get_visible()
        self.text_bbox = annotation.get_bbox_patch().get_visible()
        self.enum_text_style = ['normal', 'italic', 'oblique']
        self.enum_text_style_name = ['Normal', 'Italic', 'Oblique']
        
        self.setup()
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(230, 240)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.label_title = QLabel(self)
        self.label_title.setMinimumSize(QSize(120, 24))
        self.label_title.setMaximumSize(QSize(16777215, 24))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_title)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QHBoxLayout()
        self.label_text = QLabel(self)
        self.label_text.setMinimumSize(QSize(75, 24))
        self.label_text.setMaximumSize(QSize(75, 24))
        self.horizontalLayout.addWidget(self.label_text)
        self.line_edit_text = QLineEdit(self)
        self.line_edit_text.setMinimumSize(QSize(120, 24))
        self.line_edit_text.setMaximumSize(QSize(16777215, 24))
        self.line_edit_text.setText(self.text)
        self.horizontalLayout.addWidget(self.line_edit_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_text_rotation = QLabel(self)
        self.label_text_rotation.setMinimumSize(QSize(75, 24))
        self.label_text_rotation.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_2.addWidget(self.label_text_rotation)
        self.combo_box_text_rotation = QComboBox(self)
        self.combo_box_text_rotation.setMinimumSize(QSize(120, 24))
        self.combo_box_text_rotation.setMaximumSize(QSize(16777215, 24))
        
        count = len(self.enum_text_rotation)
        for i in range(count):
            self.combo_box_text_rotation.addItem('')
            self.combo_box_text_rotation.setItemData(i, self.enum_text_rotation[i], Qt.UserRole)
        index = self.enum_text_rotation.index(self.text_rotation)
        self.combo_box_text_rotation.setCurrentIndex(index)        
        
        self.horizontalLayout_2.addWidget(self.combo_box_text_rotation)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_text_size = QLabel(self)
        self.label_text_size.setMinimumSize(QSize(75, 24))
        self.label_text_size.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_3.addWidget(self.label_text_size)
        self.line_edit_text_size = QLineEdit(self)
        self.line_edit_text_size.setMinimumSize(QSize(120, 24))
        self.line_edit_text_size.setMaximumSize(QSize(16777215, 24))
        
        self.line_edit_text_size.setText(str(int(self.text_size)))
        
        self.horizontalLayout_3.addWidget(self.line_edit_text_size)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_text_color = QLabel(self)
        self.label_text_color.setMinimumSize(QSize(75, 24))
        self.label_text_color.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_4.addWidget(self.label_text_color)
        self.color_view = QLabel(self)
        self.color_view.setMinimumSize(QSize(90, 20))
        self.color_view.setMaximumSize(QSize(16777215, 20))
        
        self.color_view.setPalette(QPalette(QColor(self.text_color)))
        self.color_view.setAutoFillBackground(True)
        self.color_view.setText('')
        
        self.horizontalLayout_4.addWidget(self.color_view)
        self.tool_btn_text_color = QToolButton(self)
        self.tool_btn_text_color.setMinimumSize(QSize(24, 24))
        self.tool_btn_text_color.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_4.addWidget(self.tool_btn_text_color)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
#        self.horizontalLayout_6 = QHBoxLayout()
#        self.label_line_text_style = QLabel(self)
#        self.label_line_text_style.setMinimumSize(QSize(75, 24))
#        self.label_line_text_style.setMaximumSize(QSize(75, 24))
#        self.horizontalLayout_6.addWidget(self.label_line_text_style)
#        self.combo_box_text_style = QComboBox(self)
#        self.combo_box_text_style.setMinimumSize(QSize(120, 24))
#        self.combo_box_text_style.setMaximumSize(QSize(16777215, 24))
#        
#        count = len(self.enum_text_style)
#        for i in range(count):
#            self.combo_box_text_style.addItem('')
#            self.combo_box_text_style.setItemData(i, self.enum_text_style[i], Qt.UserRole)
#        index = self.enum_text_style.index(self.text_style)
#        self.combo_box_text_style.setCurrentIndex(index)  

#        self.horizontalLayout_6.addWidget(self.combo_box_text_style)
#        self.verticalLayout.addLayout(self.horizontalLayout_6)
        
        self.hlayout_arrow = QHBoxLayout()
        self.label_arrow = QLabel(self)
        self.label_arrow.setMinimumSize(QSize(75, 24))
        self.label_arrow.setMaximumSize(QSize(75, 24))
        self.hlayout_arrow.addWidget(self.label_arrow)
        self.check_box_arrow = QCheckBox(self)
        self.check_box_arrow.setMinimumSize(QSize(0, 24))
        self.check_box_arrow.setMaximumSize(QSize(16777215, 24))
        if self.text_arrow:
            self.check_box_arrow.setChecked(True)
        else:
            self.check_box_arrow.setChecked(False)
        self.hlayout_arrow.addWidget(self.check_box_arrow)
        self.verticalLayout.addLayout(self.hlayout_arrow)
        
        self.hlayout_bbox = QHBoxLayout()
        self.label_bbox = QLabel(self)
        self.label_bbox.setMinimumSize(QSize(75, 24))
        self.label_bbox.setMaximumSize(QSize(75, 24))
        self.hlayout_bbox.addWidget(self.label_bbox)
        self.check_box_bbox = QCheckBox(self)
        self.check_box_bbox.setMinimumSize(QSize(0, 24))
        self.check_box_bbox.setMaximumSize(QSize(16777215, 24))
        if self.text_bbox:
            self.check_box_bbox.setChecked(True)
        else:
            self.check_box_bbox.setChecked(False)
        self.hlayout_bbox.addWidget(self.check_box_bbox)
        self.verticalLayout.addLayout(self.hlayout_bbox)

        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_5 = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_5.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_5.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi()
        
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.tool_btn_text_color.clicked.connect(self.slot_sel_color)

    def accept(self):

        self.text = self.line_edit_text.text()
        self.text_rotation = self.combo_box_text_rotation.currentData()
        try:
            self.text_size = int(self.line_edit_text_size.text())
        except:
            pass
        self.text_arrow = self.check_box_arrow.isChecked()
#        self.text_style = self.combo_box_text_style.currentData()
        self.text_bbox = self.check_box_bbox.isChecked()
        
        self.annotation.set_text(self.text)
        self.annotation.set_rotation(self.text_rotation)
        self.annotation.set_size(self.text_size)
        self.annotation.set_color(self.text_color)
        self.annotation.set_style(self.text_style)
        if self.text_arrow:
            self.annotation.arrow_patch.set_visible(True)
            self.annotation.arrow_patch.set_color(self.text_color)
        else:
            self.annotation.arrow_patch.set_visible(False)
            self.annotation.arrow_patch.set_color(self.text_color)
        if self.text_bbox:
            self.annotation.set_bbox(dict(boxstyle = 'square, pad = 0.5', 
                                          fc = 'w', ec = self.text_color,
                                          visible = True))
        else:
            self.annotation.set_bbox(dict(boxstyle = 'square, pad = 0.5', 
                                          fc = 'w', ec = self.text_color,
                                          visible = False))
        
        QDialog.accept(self)
        
    def slot_sel_color(self):
        
        color = QColorDialog.getColor(QColor(self.text_color), self, 'Select Color')
        self.color_view.setPalette(QPalette(color))
#        按##RRGGBB的格式赋值颜色
        self.text_color = color.name()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('AnnotationSettingDialog', '标注设置'))
        self.label_title.setText(_translate('AnnotationSettingDialog', '文字标注'))
        self.label_text.setText(_translate('AnnotationSettingDialog', '内容'))
        self.label_text_rotation.setText(_translate('AnnotationSettingDialog', '文字方向'))
        self.label_text_size.setText(_translate('AnnotationSettingDialog', '文字大小'))
        self.label_text_color.setText(_translate('AnnotationSettingDialog', '文字颜色'))
        self.tool_btn_text_color.setText(_translate('AnnotationSettingDialog', 'C'))
        self.label_arrow.setText(_translate('AnnotationSettingDialog', '箭头'))
        self.label_bbox.setText(_translate('AnnotationSettingDialog', '边框'))
#        self.label_line_text_style.setText(_translate('AnnotationSettingDialog', '文字样式'))
#        self.combo_box_text_style.setItemText(0, _translate('AnnotationSettingDialog', 'Normal'))
#        self.combo_box_text_style.setItemText(1, _translate('AnnotationSettingDialog', 'Italic'))
#        self.combo_box_text_style.setItemText(2, _translate('AnnotationSettingDialog', 'Oblique'))
        self.btn_confirm.setText(_translate('AnnotationSettingDialog', '确定'))
        self.btn_cancel.setText(_translate('AnnotationSettingDialog', '取消'))
        count = len(self.enum_text_rotation_name)
        for i in range(count):
            self.combo_box_text_rotation.setItemText(i, _translate('AnnotationSettingDialog',
                                                                   self.enum_text_rotation_name[i]))
        count = len(self.enum_text_style_name)
#        for i in range(count):
#            self.combo_box_text_style.setItemText(i, _translate('AnnotationSettingDialog',
#                                                                self.enum_text_style_name[i]))
            
class Base_AxisSettingDialog(QDialog):
    
    def __init__(self, parent = None, axes : Axes = None):
        
        super().__init__(parent)
        
        self.axes = axes
        self.start = ''
        self.end = ''
        self.xlim = axes.get_xlim()
        self.ylim = axes.get_ylim()
        
            
#        !!只有当locator是MaxNLocator时才能使用下列语句!!
#        self.xlocator = axes.xaxis.get_major_locator()._nbins
#        self.ylocator = axes.yaxis.get_major_locator()._nbins
        
#        曲线设置成了不能pick所以可以这样判断，注意它只接受一条曲线
        self.curves = []
        lines = axes.get_lines()
        for line in lines:
            line_info = {}
#            忽略取值线和标记线
            if line.get_gid() and line.get_gid().find('dataline') != -1:
                line_info['line'] = line
                line_info['line_label'] = line.get_label()
                line_info['linestyle'] = line.get_linestyle()
                line_info['linewidth'] = line.get_linewidth()
                line_info['line_marker'] = line.get_marker()
        #        按#RRGGBB格式赋值
                line_info['line_color'] = Color.to_hex(line.get_color())
                self.curves.append(line_info)
        
        self.enum_linestyle = ['None','-', '--', '-.', ':']
        self.enum_linestyle_name = ['Nothing', 'Solid', 'Dashed', 
                                    'Dashdot', 'Dotted']
        self.enum_marker = ['None', '.', 'o', 'v', '^', '<', '>', '1', '2',
                            '3', '4', 's', '*', '+', 'x', 'D']
        self.enum_marker_name = ['Nothing', 'Point', 'Circle', 'Triangle_down',
                                 'Triangle_up', 'Triangle_left', 'Triangle_right',
                                 'Tri_down', 'Tri_up', 'Tri_left', 'Tri_right', 
                                 'Square', 'Star', 'Plus', 'x', 'Diamond']
        
        self.setup()
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(340, 350)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.group_box_axis_lim = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_axis_lim)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.horizontalLayout = QHBoxLayout()
        self.label_x_left = QLabel(self.group_box_axis_lim)
        self.label_x_left.setMinimumSize(QSize(75, 24))
        self.label_x_left.setMaximumSize(QSize(75, 24))
        self.horizontalLayout.addWidget(self.label_x_left)
        self.line_edit_x_left = QLineEdit(self.group_box_axis_lim)
        self.line_edit_x_left.setMinimumSize(QSize(120, 24))
        self.line_edit_x_left.setMaximumSize(QSize(16777215, 24))
        
        self.start = self.value_to_text(self.xlim[0])
        self.line_edit_x_left.setText(self.start)
        
        self.horizontalLayout.addWidget(self.line_edit_x_left)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_8 = QHBoxLayout()
        self.label_x_right = QLabel(self.group_box_axis_lim)
        self.label_x_right.setMinimumSize(QSize(75, 24))
        self.label_x_right.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_8.addWidget(self.label_x_right)
        self.line_edit_x_right = QLineEdit(self.group_box_axis_lim)
        self.line_edit_x_right.setMinimumSize(QSize(120, 24))
        self.line_edit_x_right.setMaximumSize(QSize(16777215, 24))
        
        self.end = self.value_to_text(self.xlim[1])
        self.line_edit_x_right.setText(self.end)
        
        self.horizontalLayout_8.addWidget(self.line_edit_x_right)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QHBoxLayout()
        self.label_y_top = QLabel(self.group_box_axis_lim)
        self.label_y_top.setMinimumSize(QSize(75, 24))
        self.label_y_top.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_9.addWidget(self.label_y_top)
        self.line_edit_y_top = QLineEdit(self.group_box_axis_lim)
        self.line_edit_y_top.setMinimumSize(QSize(120, 24))
        self.line_edit_y_top.setMaximumSize(QSize(16777215, 24))
        
        self.line_edit_y_top.setText(str(self.ylim[1]))
        
        self.horizontalLayout_9.addWidget(self.line_edit_y_top)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_7 = QHBoxLayout()
        self.label_y_bottom = QLabel(self.group_box_axis_lim)
        self.label_y_bottom.setMinimumSize(QSize(75, 24))
        self.label_y_bottom.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_7.addWidget(self.label_y_bottom)
        self.line_edit_y_bottom = QLineEdit(self.group_box_axis_lim)
        self.line_edit_y_bottom.setMinimumSize(QSize(120, 24))
        self.line_edit_y_bottom.setMaximumSize(QSize(16777215, 24))
        
        self.line_edit_y_bottom.setText(str(self.ylim[0]))
        
        self.horizontalLayout_7.addWidget(self.line_edit_y_bottom)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addWidget(self.group_box_axis_lim)
        self.group_box_curves = QGroupBox(self)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_curves)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.combo_box_curvename = QComboBox(self.group_box_curves)
        self.combo_box_curvename.setMinimumSize(QSize(0, 24))
        self.combo_box_curvename.setMaximumSize(QSize(16777215, 24))
        
        count = len(self.curves)
        for i in range(count):
            self.combo_box_curvename.addItem('')
            self.combo_box_curvename.setItemText(i, self.curves[i]['line_label'])
        self.combo_box_curvename.setCurrentIndex(0)
        
        self.verticalLayout_2.addWidget(self.combo_box_curvename)
        self.horizontalLayout_10 = QHBoxLayout()
        self.label_legend = QLabel(self.group_box_curves)
        self.label_legend.setMinimumSize(QSize(75, 24))
        self.label_legend.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_10.addWidget(self.label_legend)
        self.line_edit_legend = QLineEdit(self.group_box_curves)
        self.line_edit_legend.setMinimumSize(QSize(120, 24))
        self.line_edit_legend.setMaximumSize(QSize(16777215, 24))

#        只显示第一条曲线的label
        self.line_edit_legend.setText(self.curves[0]['line_label'])
        
        self.horizontalLayout_10.addWidget(self.line_edit_legend)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_text_linestyle = QLabel(self.group_box_curves)
        self.label_text_linestyle.setMinimumSize(QSize(75, 24))
        self.label_text_linestyle.setMaximumSize(QSize(57, 24))
        self.horizontalLayout_2.addWidget(self.label_text_linestyle)
        self.combo_box_linestyle = QComboBox(self.group_box_curves)
        self.combo_box_linestyle.setMinimumSize(QSize(120, 24))
        self.combo_box_linestyle.setMaximumSize(QSize(16777215, 24))

        count = len(self.enum_linestyle)
        for i in range(count):
            self.combo_box_linestyle.addItem('')
            self.combo_box_linestyle.setItemData(i, self.enum_linestyle[i], Qt.UserRole)
        index = self.enum_linestyle.index(self.curves[0]['linestyle'])
        self.combo_box_linestyle.setCurrentIndex(index)

        self.horizontalLayout_2.addWidget(self.combo_box_linestyle)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_line_width = QLabel(self.group_box_curves)
        self.label_line_width.setMinimumSize(QSize(75, 24))
        self.label_line_width.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_3.addWidget(self.label_line_width)
        self.line_edit_line_width = QLineEdit(self.group_box_curves)
        self.line_edit_line_width.setMinimumSize(QSize(120, 24))
        self.line_edit_line_width.setMaximumSize(QSize(16777215, 24))
        
        self.line_edit_line_width.setText(str(self.curves[0]['linewidth']))
        
        self.horizontalLayout_3.addWidget(self.line_edit_line_width)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_text_color = QLabel(self.group_box_curves)
        self.label_text_color.setMinimumSize(QSize(75, 24))
        self.label_text_color.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_4.addWidget(self.label_text_color)
        self.label = QLabel(self.group_box_curves)
        self.label.setMinimumSize(QSize(90, 20))
        self.label.setMaximumSize(QSize(16777215, 20))
        
        self.label.setPalette(QPalette(QColor(self.curves[0]['line_color'])))
        self.label.setAutoFillBackground(True)
        
        self.horizontalLayout_4.addWidget(self.label)
        self.tool_btn_text_color = QToolButton(self.group_box_curves)
        self.tool_btn_text_color.setMinimumSize(QSize(24, 24))
        self.tool_btn_text_color.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_4.addWidget(self.tool_btn_text_color)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QHBoxLayout()
        self.label_marker = QLabel(self.group_box_curves)
        self.label_marker.setMinimumSize(QSize(75, 24))
        self.label_marker.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_6.addWidget(self.label_marker)
        self.combo_box_marker = QComboBox(self.group_box_curves)
        self.combo_box_marker.setMinimumSize(QSize(120, 24))
        self.combo_box_marker.setMaximumSize(QSize(16777215, 24))

        count = len(self.enum_marker)
        for i in range(count):
            self.combo_box_marker.addItem('')
            self.combo_box_marker.setItemData(i, self.enum_marker[i], Qt.UserRole)
        index = self.enum_marker.index(self.curves[0]['line_marker'])
        self.combo_box_marker.setCurrentIndex(index)

        self.horizontalLayout_6.addWidget(self.combo_box_marker)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addWidget(self.group_box_curves)
        self.horizontalLayout_5 = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.push_btn_easter_egg = QPushButton(self)
        self.push_btn_easter_egg.setHidden(True)
        self.horizontalLayout_5.addWidget(self.push_btn_easter_egg)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
#        避免按钮默认选中并按Enter键会执行的情况
#        self.btn_confirm.setFocusPolicy(Qt.NoFocus) 
        self.horizontalLayout_5.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
#        避免按钮默认选中并按Enter键会执行的情况
#        self.btn_cancel.setFocusPolicy(Qt.NoFocus) 
        self.horizontalLayout_5.addWidget(self.btn_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.retranslateUi()
        
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.line_edit_x_left.editingFinished.connect(self.slot_change_start)
        self.line_edit_x_right.editingFinished.connect(self.slot_change_end)
        self.line_edit_legend.editingFinished.connect(self.slot_change_legend)
        self.line_edit_line_width.editingFinished.connect(self.slot_change_lw)
        
        self.combo_box_curvename.currentIndexChanged.connect(self.slot_change_curve)
        self.combo_box_linestyle.currentIndexChanged.connect(self.slot_change_ls)
        self.combo_box_marker.currentIndexChanged.connect(self.slot_change_line_marker)
        
        self.tool_btn_text_color.clicked.connect(self.slot_sel_color)
        
    def accept(self):
        
        try:
            str_x_left = self.line_edit_x_left.text()
            str_x_right = self.line_edit_x_right.text()
            str_y_bottom = self.line_edit_y_bottom.text()
            str_y_top = self.line_edit_y_top.text()
#            将时间转换为浮点值坐标
            x0 = self.text_to_value(str_x_left)
            x1 = self.text_to_value(str_x_right)
#            x0 = mdates.date2num(Time_Model.str_to_datetime(str_x_left))
#            x1 = mdates.date2num(Time_Model.str_to_datetime(str_x_right))
            self.xlim = (x0, x1)
            self.ylim = (float(str_y_bottom), float(str_y_top))
        except:
            pass
        self.axes.set_xlim(self.xlim)
        self.axes.set_ylim(self.ylim)
        
#        设置图注
        hs, ls = self.axes.get_legend_handles_labels()
        for i, curve in enumerate(self.curves):
            ls[i] = curve['line_label']
            hs[i].set_color(curve['line_color'])
            curve['line'].set_label(curve['line_label'])
            curve['line'].set_linestyle(curve['linestyle'])
            curve['line'].set_color(curve['line_color'])
            curve['line'].set_linewidth(curve['linewidth'])
            curve['line'].set_marker(curve['line_marker'])
#        似乎获得图注labels时是返回曲线的label而不是当前状态，所以需要用下面这个设置下
        self.axes.legend(hs, ls, loc=(0,1), fontsize = self.axes.get_legend()._fontsize,
                         ncol=4, frameon=False, borderpad = 0.15,
                         prop = CONFIG.FONT_MSYH)
        
        QDialog.accept(self)
        
    def slot_change_start(self):
        end = self.line_edit_x_right.text()
        start = self.line_edit_x_left.text()
        if start<=end:
            self.line_edit_x_left.setText(start)
        else:
            self.line_edit_x_left.setText(self.start)
            QMessageBox.information(self,
                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                            QCoreApplication.translate('AxisSettingDialog', '起始值大于终止值'))
            
    def slot_change_end(self):
        end = self.line_edit_x_right.text()
        start = self.line_edit_x_left.text()
        if start<=end:
            self.line_edit_x_right.setText(end)
        else:
            self.line_edit_x_right.setText(self.end)
            QMessageBox.information(self,
                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                            QCoreApplication.translate('AxisSettingDialog', '终止值小于起始值'))
            
                

#    def slot_change_stime(self):
#        
#        etime = self.line_edit_x_right.text()
#        stime = self.line_edit_x_left.text()
#        if Time_Model.is_std_format(stime):
#            if Time_Model.compare(stime, etime) != 1:
##                    输入正确的起始时间后，还需要转换成标准格式后再显示
#                self.stime = Time_Model.timestr_to_stdtimestr(stime)
#                self.line_edit_x_left.setText(self.stime)
#            else:
#                self.line_edit_x_left.setText(self.stime)
#                QMessageBox.information(self,
#                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
#                                QCoreApplication.translate('AxisSettingDialog', '起始时间大于终止时间'))
#        else:
#            self.line_edit_x_left.setText(self.stime)
#            QMessageBox.information(self,
#                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
#                            QCoreApplication.translate('AxisSettingDialog', '''<b>请输入正确时间格式</b>
#                                                       <br>HH
#                                                       <br>HH:MM
#                                                       <br>HH:MM:SS
#                                                       <br>HH:MM:SS.FFF
#                                                       <br>HH:MM:SS:FFF'''))

#    def slot_change_etime(self):
#        
#        etime = self.line_edit_x_right.text()
#        stime = self.line_edit_x_left.text()
#        if Time_Model.is_std_format(etime):
#            if Time_Model.compare(stime, etime) != 1:
##                    输入正确的起始时间后，还需要转换成标准格式后再显示
#                self.etime = Time_Model.timestr_to_stdtimestr(etime)
#                self.line_edit_x_right.setText(self.etime)
#            else:
#                self.line_edit_x_right.setText(self.etime)
#                QMessageBox.information(self,
#                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
#                                QCoreApplication.translate('AxisSettingDialog', '终止时间小于起始时间'))
#        else:
#            self.line_edit_x_right.setText(self.etime)
#            QMessageBox.information(self,
#                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
#                            QCoreApplication.translate('AxisSettingDialog', '''<b>请输入正确时间格式</b>
#                                                       <br>HH
#                                                       <br>HH:MM
#                                                       <br>HH:MM:SS
#                                                       <br>HH:MM:SS.FFF
#                                                       <br>HH:MM:SS:FFF'''))
            
    def slot_change_legend(self):
        
        label = self.combo_box_curvename.currentText()
        index = self.combo_box_curvename.currentIndex()
        if label:
            legend_label = self.line_edit_legend.text()
            if legend_label:
                self.combo_box_curvename.setItemText(index, legend_label)
                self.curves[index]['line_label'] = legend_label
            else:
                self.line_edit_legend.setText(label)
                
    def slot_change_lw(self):
        
        label = self.combo_box_curvename.currentText()
        index = self.combo_box_curvename.currentIndex()
        if label:
            lw = self.line_edit_line_width.text()
            try:
                linewidth = float(lw)
                self.curves[index]['linewidth'] = linewidth
            except:
                self.line_edit_line_width.setText(str(self.curves[index]['linewidth']))
                QMessageBox.information(self,
                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                                QCoreApplication.translate('AxisSettingDialog', '非浮点值'))
                
    def slot_change_curve(self, index):
        
        label = self.combo_box_curvename.currentText()
#        不明白为什么不能用信号中的index
        index_t = self.combo_box_curvename.currentIndex()
        if label:
            self.line_edit_legend.setText(self.curves[index_t]['line_label'])
            index_ls = self.enum_linestyle.index(self.curves[index_t]['linestyle'])
            self.combo_box_linestyle.setCurrentIndex(index_ls)
            self.line_edit_line_width.setText(str(self.curves[index_t]['linewidth']))
            self.label.setPalette(QPalette(QColor(self.curves[index_t]['line_color'])))
            index_lm = self.enum_marker.index(self.curves[index_t]['line_marker'])
            self.combo_box_marker.setCurrentIndex(index_lm)
    
    def slot_change_ls(self, index):
        
        label = self.combo_box_curvename.currentText()
#        不明白为什么不能用信号中的index
        index_t = self.combo_box_curvename.currentIndex()
        if label:
            ls = self.combo_box_linestyle.currentData()
            if ls:
                self.curves[index_t]['linestyle'] = ls
                
    def slot_change_line_marker(self, index):
        
        label = self.combo_box_curvename.currentText()
#        不明白为什么不能用信号中的index
        index_t = self.combo_box_curvename.currentIndex()
        if label:
            marker = self.combo_box_marker.currentData()
            if marker:
                self.curves[index_t]['line_marker'] = marker
        
    def slot_sel_color(self):
        
        label = self.combo_box_curvename.currentText()
        index = self.combo_box_curvename.currentIndex()
        if label:
            color = QColorDialog.getColor(
                    QColor(self.curves[index]['line_color']), self, 'Select Color')
            self.label.setPalette(QPalette(color))
    #        按##RRGGBB的格式赋值颜色
            self.curves[index]['line_color'] = color.name()
    
    def value_to_text(self, value):
        text = str(value)
#        out_value = mdates.num2date(in_value).time().isoformat(timespec='milliseconds')
            
        return text
    
    def text_to_value(self, text):
        value = float(text)
#        out_value = mdates.date2num(Time_Model.str_to_datetime(in_value))
            
        return value

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('AxisSettingDialog', '坐标设置'))
        self.group_box_axis_lim.setTitle(_translate('AxisSettingDialog', '坐标轴范围'))
        self.label_x_left.setText(_translate('AxisSettingDialog', 'X轴左边界'))
        self.label_x_right.setText(_translate('AxisSettingDialog', 'X轴右边界'))
        self.label_y_bottom.setText(_translate('AxisSettingDialog', 'Y轴下边界'))
        self.label_y_top.setText(_translate('AxisSettingDialog', 'Y轴上边界'))
        self.group_box_curves.setTitle(_translate('AxisSettingDialog', '曲线设置'))
        self.label_legend.setText(_translate('AxisSettingDialog', '图注'))
        self.label_text_linestyle.setText(_translate('AxisSettingDialog', '曲线类型'))
        self.label_line_width.setText(_translate('AxisSettingDialog', '曲线宽度'))
        self.label_text_color.setText(_translate('AxisSettingDialog', '曲线颜色'))
        self.label.setText(_translate('AxisSettingDialog', ''))
        self.tool_btn_text_color.setText(_translate('AxisSettingDialog', 'C'))
        self.label_marker.setText(_translate('AxisSettingDialog', '标记类型'))
        self.btn_confirm.setText(_translate('AxisSettingDialog', '确定'))
        self.btn_cancel.setText(_translate('AxisSettingDialog', '取消'))
        
        count = len(self.enum_linestyle_name)
        for i in range(count):
            self.combo_box_linestyle.setItemText(i, _translate('AxisSettingDialog',
                                                               self.enum_linestyle_name[i]))
        count = len(self.enum_marker_name)
        for i in range(count):
            self.combo_box_marker.setItemText(i, _translate('AxisSettingDialog',
                                                               self.enum_marker_name[i]))

class AxisSettingDialog(Base_AxisSettingDialog):

    

    def __init__(self, parent = None, axes : Axes = None):

        super().__init__(parent, axes)

    def slot_change_start(self):
        
        etime = self.line_edit_x_right.text()
        stime = self.line_edit_x_left.text()
        if Time_Model.is_std_format(stime):
            if Time_Model.compare(stime, etime) != 1:
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                self.start = Time_Model.timestr_to_stdtimestr(stime)
                self.line_edit_x_left.setText(self.start)
            else:
                self.line_edit_x_left.setText(self.start)
                QMessageBox.information(self,
                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                                QCoreApplication.translate('AxisSettingDialog', '起始时间大于终止时间'))
        else:
            self.line_edit_x_left.setText(self.start)
            QMessageBox.information(self,
                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                            QCoreApplication.translate('AxisSettingDialog', '''<b>请输入正确时间格式</b>
                                                       <br>HH
                                                       <br>HH:MM
                                                       <br>HH:MM:SS
                                                       <br>HH:MM:SS.FFF
                                                       <br>HH:MM:SS:FFF'''))

    def slot_change_end(self):
        
        etime = self.line_edit_x_right.text()
        stime = self.line_edit_x_left.text()
        if Time_Model.is_std_format(etime):
            if Time_Model.compare(stime, etime) != 1:
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                self.end = Time_Model.timestr_to_stdtimestr(etime)
                self.line_edit_x_right.setText(self.end)
            else:
                self.line_edit_x_right.setText(self.end)
                QMessageBox.information(self,
                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                                QCoreApplication.translate('AxisSettingDialog', '终止时间小于起始时间'))
        else:
            self.line_edit_x_right.setText(self.end)
            QMessageBox.information(self,
                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                            QCoreApplication.translate('AxisSettingDialog', '''<b>请输入正确时间格式</b>
                                                       <br>HH
                                                       <br>HH:MM
                                                       <br>HH:MM:SS
                                                       <br>HH:MM:SS.FFF
                                                       <br>HH:MM:SS:FFF'''))

    def value_to_text(self, value):
        time_value = mdates.num2date(value).time().isoformat(timespec='milliseconds')
        text = str(time_value)  
        return text
    
    def text_to_value(self, text):
        value = mdates.date2num(Time_Model.str_to_datetime(text))
        return value 

class SingleUtAxisSettingDialog(Base_AxisSettingDialog):

    def __init__(self, parent = None, axes : Axes = None, data_timerange : dict = {}):

        super().__init__(parent, axes)
        self.data_timerange = data_timerange
        if self.data_timerange['enable']:
            self.add_timerange()

    def add_timerange(self):
        
        self.group_timerange = QGroupBox(self)
        self.group_timerange.setTitle(QCoreApplication.translate('SingleUtAxisSettingDialog', '显示范围'))
        self.vlayout_tr = QVBoxLayout(self.group_timerange)
        self.vlayout_tr.setContentsMargins(2, 2, 2, 2)
        self.vlayout_tr.setSpacing(2)
        self.label_whole_time = QLabel(self.group_timerange)
        self.label_whole_time.setMinimumSize(QSize(16777215, 24))
        self.label_whole_time.setMaximumSize(QSize(16777215, 24))
        self.label_whole_time.setText(QCoreApplication.translate('SingleUtAxisSettingDialog',
                                                                 '完整时间段：' + self.data_timerange['whole_stime'] + ' - ' + self.data_timerange['whole_etime']))
        self.vlayout_tr.addWidget(self.label_whole_time)
        
        self.hlayout_stime = QHBoxLayout()
        self.label_stime = QLabel(self.group_timerange)
        self.label_stime.setText(QCoreApplication.translate('SingleUtAxisSettingDialog', '开始时间'))
        self.label_stime.setMinimumSize(QSize(75, 24))
        self.label_stime.setMaximumSize(QSize(75, 24))
        self.hlayout_stime.addWidget(self.label_stime)
        self.line_edit_stime = QLineEdit(self.group_timerange)
        self.line_edit_stime.setMinimumSize(QSize(120, 24))
        self.line_edit_stime.setMaximumSize(QSize(16777215, 24))
        self.line_edit_stime.setText(self.data_timerange['view_stime'])
        self.hlayout_stime.addWidget(self.line_edit_stime)
        self.vlayout_tr.addLayout(self.hlayout_stime)
        
        self.hlayout_etime = QHBoxLayout()
        self.label_etime = QLabel(self.group_timerange)
        self.label_etime.setText(QCoreApplication.translate('SingleUtAxisSettingDialog', '结束时间'))
        self.label_etime.setMinimumSize(QSize(75, 24))
        self.label_etime.setMaximumSize(QSize(75, 24))
        self.hlayout_etime.addWidget(self.label_etime)
        self.line_edit_etime = QLineEdit(self.group_timerange)
        self.line_edit_etime.setMinimumSize(QSize(120, 24))
        self.line_edit_etime.setMaximumSize(QSize(16777215, 24))
        self.line_edit_etime.setText(self.data_timerange['view_etime'])
        self.hlayout_etime.addWidget(self.line_edit_etime)
        self.vlayout_tr.addLayout(self.hlayout_etime)
        
        self.verticalLayout_3.insertWidget(1, self.group_timerange)
        
        self.line_edit_stime.editingFinished.connect(self.slot_change_stime)
        self.line_edit_etime.editingFinished.connect(self.slot_change_etime)
        
    def slot_change_stime(self):
        
        etime = self.line_edit_etime.text()
        stime = self.line_edit_stime.text()
        if Time_Model.is_std_format(stime):
            if Time_Model.compare(stime, etime) != 1:
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                self.data_timerange['view_stime'] = Time_Model.timestr_to_stdtimestr(stime)
                self.line_edit_stime.setText(self.data_timerange['view_stime'])
            else:
                self.line_edit_stime.setText(self.data_timerange['view_stime'])
                QMessageBox.information(self,
                                        QCoreApplication.translate('SingleUtAxisSettingDialog', '输入提示'),
                                        QCoreApplication.translate('SingleUtAxisSettingDialog', '起始时间大于终止时间'))
        else:
            self.line_edit_stime.setText(self.data_timerange['view_stime'])
            QMessageBox.information(self,
                                    QCoreApplication.translate('SingleUtAxisSettingDialog', '输入提示'),
                                    QCoreApplication.translate('SingleUtAxisSettingDialog', '''<b>请输入正确时间格式</b>
                                                               <br>HH
                                                               <br>HH:MM
                                                               <br>HH:MM:SS
                                                               <br>HH:MM:SS.FFF
                                                               <br>HH:MM:SS:FFF'''))
            
    def slot_change_etime(self):
        
        etime = self.line_edit_etime.text()
        stime = self.line_edit_stime.text()
        if Time_Model.is_std_format(etime):
            if Time_Model.compare(stime, etime) != 1:
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                self.data_timerange['view_etime'] = Time_Model.timestr_to_stdtimestr(etime)
                self.line_edit_etime.setText(self.data_timerange['view_etime'])
            else:
                self.line_edit_etime.setText(self.data_timerange['view_etime'])
                QMessageBox.information(self,
                                        QCoreApplication.translate('SingleUtAxisSettingDialog', '输入提示'),
                                        QCoreApplication.translate('SingleUtAxisSettingDialog', '终止时间小于起始时间'))
        else:
            self.line_edit_etime.setText(self.data_timerange['view_etime'])
            QMessageBox.information(self,
                                    QCoreApplication.translate('SingleUtAxisSettingDialog', '输入提示'),
                                    QCoreApplication.translate('SingleUtAxisSettingDialog', '''<b>请输入正确时间格式</b>
                                                               <br>HH
                                                               <br>HH:MM
                                                               <br>HH:MM:SS
                                                               <br>HH:MM:SS.FFF
                                                               <br>HH:MM:SS:FFF'''))
            

class StackAxisSettingDialog(AxisSettingDialog):

    def __init__(self, parent = None, axes : Axes = None, layout_info : tuple = None):

        super().__init__(parent, axes)
        
        self.num_yscales, self.num_scales_between_ylabel, self.num_view_yscales, self.num_yview_scales, self.i = layout_info
        self.view_llimit = axes.get_yticks()[0]
        self.view_ulimit = axes.get_yticks()[2]
        self.line_edit_y_top.setText(str(self.view_ulimit))
        self.line_edit_y_bottom.setText(str(self.view_llimit))
        
    def accept(self):
        
        try:
            str_x_left = self.line_edit_x_left.text()
            str_x_right = self.line_edit_x_right.text()
            str_y_bottom = self.line_edit_y_bottom.text()
            str_y_top = self.line_edit_y_top.text()
#            将时间转换为浮点值坐标
            x0 = self.text_to_value(str_x_left)
            x1 = self.text_to_value(str_x_right)
#            x0 = mdates.date2num(Time_Model.str_to_datetime(str_x_left))
#            x1 = mdates.date2num(Time_Model.str_to_datetime(str_x_right))
            self.xlim = (x0, x1)
            self.view_llimit = float(str_y_bottom)
            self.view_ulimit = float(str_y_top)
            new_scale = (self.view_ulimit - self.view_llimit) / self.num_yview_scales
            self.ylim = (self.view_llimit - (self.num_yscales - self.num_scales_between_ylabel * self.i - self.num_view_yscales) * new_scale / self.num_yview_scales, 
                         self.view_ulimit + self.num_scales_between_ylabel * self.i * new_scale / self.num_yview_scales)
        except:
            pass
        self.axes.set_xlim(self.xlim)
        self.axes.set_ylim(self.ylim)
        self.axes.set_yticks([self.view_llimit,(self.view_llimit + self.view_ulimit) / 2, self.view_ulimit])
        self.axes.spines['left'].set_bounds(self.view_llimit, self.view_ulimit)
        
#        设置图注
        curve = self.curves[0]
        curve['line'].set_label(curve['line_label'])
        self.axes.set_ylabel(curve['line_label'])
        curve['line'].set_linestyle(curve['linestyle'])
        curve['line'].set_color(curve['line_color'])
        self.axes.spines['left'].set_color(curve['line_color'])
        self.axes.tick_params(axis='y', colors=curve['line_color'])
        self.axes.set_ylabel(self.axes.get_ylabel(), color = curve['line_color'])
        curve['line'].set_linewidth(curve['linewidth'])
        curve['line'].set_marker(curve['line_marker'])
        
        QDialog.accept(self)
            
class ParameterExportDialog(QDialog):
    
    signal_send_status = pyqtSignal(str, int)
    def __init__(self, parent = None, dict_paras : dict = {}, dict_filetype = None):
        
        super().__init__(parent)
        
        self.outfile_icon = QIcon(CONFIG.ICON_FILE)
        self.para_icon = QIcon(CONFIG.ICON_PARA)
        self.file_info = {}
        self.current_file_dir = ''
        self._data_dict = None
        self.is_merge = False
        self.merge_use_file_info = {}
        self.merge_start_time_limit = ''
        self.merge_end_time_limit = ''
        if dict_filetype:
            self._dict_filetype = dict_filetype
        if os.path.exists(CONFIG.OPTION['dir of export data']):
            self.dir = CONFIG.OPTION['dir of export data']
        elif os.path.exists(CONFIG.OPTION['work dir']):
            self.dir = CONFIG.OPTION['work dir']
        else:
            self.dir = CONFIG.SETUP_DIR
        
        self.setup()
        self.dict_data = {}
        self.display_file_info(dict_paras)
        
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(700, 500)
        self.verticalLayout_4 = QVBoxLayout(self)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(2)
        self.group_box_preview = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_preview)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.tree_widget_export_paras = QTreeWidget(self.group_box_preview)
#        设置树组件头部显示方式
        headerview = self.tree_widget_export_paras.header()
        headerview.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerview.setMinimumSectionSize(100)
        self.tree_widget_export_paras.setHeader(headerview)
        
        self.verticalLayout.addWidget(self.tree_widget_export_paras)
        self.verticalLayout_4.addWidget(self.group_box_preview)
        self.group_box_setting = QGroupBox(self)
        self.verticalLayout_3 = QVBoxLayout(self.group_box_setting)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
#        self.combo_box_filename = QComboBox(self.group_box_setting)
#        self.combo_box_filename.setMinimumSize(QSize(0, 24))
#        self.combo_box_filename.setMaximumSize(QSize(16777215, 24))
#        self.verticalLayout_3.addWidget(self.combo_box_filename)
        self.groupBox = QGroupBox(self.group_box_setting)
        self.vlayout_gb_time_setting = QVBoxLayout(self.groupBox)
        self.vlayout_gb_time_setting.setContentsMargins(2, 2, 2, 2)
        self.vlayout_gb_time_setting.setSpacing(2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(4, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.label_starttime = QLabel(self.groupBox)
        self.label_starttime.setMinimumSize(QSize(60, 24))
        self.label_starttime.setMaximumSize(QSize(60, 24))
        self.horizontalLayout.addWidget(self.label_starttime)
        self.line_edit_starttime = QLineEdit(self.groupBox)
        self.line_edit_starttime.setMinimumSize(QSize(0, 24))
        self.line_edit_starttime.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_starttime)
        self.label_endtime = QLabel(self.groupBox)
        self.label_endtime.setMinimumSize(QSize(60, 24))
        self.label_endtime.setMaximumSize(QSize(60, 24))
        self.horizontalLayout.addWidget(self.label_endtime)
        self.line_edit_endtime = QLineEdit(self.groupBox)
        self.line_edit_endtime.setMinimumSize(QSize(0, 24))
        self.line_edit_endtime.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_endtime)
        self.vlayout_gb_time_setting.addLayout(self.horizontalLayout)
        self.hlayout_fre = QHBoxLayout()
        self.hlayout_fre.setContentsMargins(4, 2, 2, 2)
        self.hlayout_fre.setSpacing(2)
        self.label_fre = QLabel(self.groupBox)
        self.label_fre.setMinimumSize(QSize(60, 24))
        self.label_fre.setMaximumSize(QSize(60, 24))
        self.hlayout_fre.addWidget(self.label_fre)
        self.line_edit_fre = QLineEdit(self.groupBox)
        self.line_edit_fre.setMinimumSize(QSize(0, 24))
        self.line_edit_fre.setMaximumSize(QSize(16777215, 24))
        self.hlayout_fre.addWidget(self.line_edit_fre)
        self.vlayout_gb_time_setting.addLayout(self.hlayout_fre)
        
#        self.push_btn_apply_all_files = QPushButton(self.groupBox)
##        避免按钮默认选中并按Enter键会执行的情况
#        self.push_btn_apply_all_files.setFocusPolicy(Qt.NoFocus)        
#        self.push_btn_apply_all_files.setMinimumSize(QSize(100, 24))
#        self.push_btn_apply_all_files.setMaximumSize(QSize(100, 24))
#        self.horizontalLayout.addWidget(self.push_btn_apply_all_files)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.group_box_file_setting = QGroupBox(self.group_box_setting)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_file_setting)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_file_type = QLabel(self.group_box_file_setting)
        self.label_file_type.setMinimumSize(QSize(60, 24))
        self.label_file_type.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_3.addWidget(self.label_file_type)
        self.combo_box_filetype = QComboBox(self.group_box_file_setting)
        self.combo_box_filetype.setMinimumSize(QSize(0, 24))
        self.combo_box_filetype.setMaximumSize(QSize(16777215, 24))
        self.combo_box_filetype.addItem('')
#        设置每个项目的数据，为后续选择导出文件所使用
        self.combo_box_filetype.setItemData(0, '.txt', Qt.UserRole)
        self.combo_box_filetype.addItem('')
        self.combo_box_filetype.setItemData(1, '.csv', Qt.UserRole)
        self.combo_box_filetype.addItem('')
        self.combo_box_filetype.setItemData(2, '.mat', Qt.UserRole)
        self.horizontalLayout_3.addWidget(self.combo_box_filetype)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_file_name = QLabel(self.group_box_file_setting)
        self.label_file_name.setMinimumSize(QSize(60, 24))
        self.label_file_name.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_4.addWidget(self.label_file_name)
        self.line_edit_file_name = QLineEdit(self.group_box_file_setting)
        self.line_edit_file_name.setMinimumSize(QSize(0, 24))
        self.line_edit_file_name.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_4.addWidget(self.line_edit_file_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_file_dir = QLabel(self.group_box_file_setting)
        self.label_file_dir.setMinimumSize(QSize(60, 24))
        self.label_file_dir.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_2.addWidget(self.label_file_dir)
        self.line_edit_file_dir = QLineEdit(self.group_box_file_setting)
        self.line_edit_file_dir.setMinimumSize(QSize(0, 24))
        self.line_edit_file_dir.setMaximumSize(QSize(16777215, 24))
        self.line_edit_file_dir.setReadOnly(True)
        self.horizontalLayout_2.addWidget(self.line_edit_file_dir)
        self.tool_btn_sel_filedir = QToolButton(self.group_box_file_setting)
        self.tool_btn_sel_filedir.setMinimumSize(QSize(24, 24))
        self.tool_btn_sel_filedir.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_2.addWidget(self.tool_btn_sel_filedir)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.group_box_file_setting)
        self.verticalLayout_4.addWidget(self.group_box_setting)
        self.horizontalLayout_5 = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
#        这个彩蛋按钮，只是奇思妙想到的一个bug解决方案，信不信由你
        self.push_btn_easter_egg = QPushButton(self)
        self.push_btn_easter_egg.setHidden(True)
        self.horizontalLayout_5.addWidget(self.push_btn_easter_egg)
        self.push_btn_apply_all_files = QPushButton(self)
        self.push_btn_apply_all_files.setFocusPolicy(Qt.NoFocus)
        self.push_btn_apply_all_files.setMinimumSize(QSize(100, 24))
        self.push_btn_apply_all_files.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_5.addWidget(self.push_btn_apply_all_files)

        self.push_btn_merge = QPushButton(self)
        self.push_btn_merge.setFocusPolicy(Qt.NoFocus)
        self.push_btn_merge.setMinimumSize(QSize(100, 24))
        self.push_btn_merge.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_5.addWidget(self.push_btn_merge)
        
        self.push_btn_confirm = QPushButton(self)
        self.push_btn_confirm.setMinimumSize(QSize(0, 24))
        self.push_btn_confirm.setMaximumSize(QSize(16777215, 24))
#        避免按钮默认选中并按Enter键会执行的情况
#        self.push_btn_confirm.setFocusPolicy(Qt.NoFocus) 
        self.horizontalLayout_5.addWidget(self.push_btn_confirm)
        self.push_btn_cancel = QPushButton(self)
        self.push_btn_cancel.setMinimumSize(QSize(0, 24))
        self.push_btn_cancel.setMaximumSize(QSize(16777215, 24))
#        避免按钮默认选中并按Enter键会执行的情况
#        self.push_btn_cancel.setFocusPolicy(Qt.NoFocus) 
        self.horizontalLayout_5.addWidget(self.push_btn_cancel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.retranslateUi()
        self.load_data_dict()
# =======连接信号与槽
# =============================================================================
        self.tool_btn_sel_filedir.clicked.connect(self.slot_sel_dir)        
#        self.combo_box_filename.currentIndexChanged.connect(self.slot_change_current_file)        
        self.combo_box_filetype.currentIndexChanged.connect(self.slot_change_filetype)        
        self.line_edit_file_name.editingFinished.connect(self.slot_change_filename)
        self.line_edit_starttime.editingFinished.connect(self.slot_change_file_stime)
        self.line_edit_endtime.editingFinished.connect(self.slot_change_file_etime)
        self.line_edit_fre.editingFinished.connect(self.slot_change_fre)
        self.push_btn_apply_all_files.clicked.connect(self.slot_change_all_file_time)
        self.push_btn_merge.clicked.connect(self.slot_merge)
        self.tree_widget_export_paras.itemClicked.connect(self.slot_change_current_file)
        
        self.push_btn_confirm.clicked.connect(self.accept)
        self.push_btn_cancel.clicked.connect(self.reject)

#    让用户选择项目的路径
    def slot_sel_dir(self):
        
        filedir = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('ParameterExportDialog', '导出路径'),
                                                   self.dir)
        if filedir:
            filedir = filedir.replace('/','\\')
            self.dir = filedir
            self.line_edit_file_dir.setText(filedir)
            
    def slot_change_current_file(self, item):
        
        index = self.tree_widget_export_paras.indexOfTopLevelItem(item)
        if index != -1:
            self.current_file_dir = item.data(0, Qt.UserRole)
        if self.current_file_dir:
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[self.current_file_dir]
            self.line_edit_starttime.setText(stime)
            self.line_edit_endtime.setText(etime)
            self.combo_box_filetype.setCurrentIndex(
                    self.combo_box_filetype.findData(filetype, Qt.UserRole))
            self.line_edit_file_name.setText(filename)
            self.line_edit_fre.setText(str(fre))
        
    def slot_change_filetype(self, index):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
            filetype = self.combo_box_filetype.currentData()
            item = self.tree_widget_export_paras.topLevelItem(index)
            item.setText(0, filename + filetype)
            self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist, fre)
            
    def slot_change_filename(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
            f = self.line_edit_file_name.text()
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
            count = self.tree_widget_export_paras.topLevelItemCount()
            target_item = None
            is_exit = False
            for i in range(count):
                item = self.tree_widget_export_paras.topLevelItem(i)
                if item.data(0, Qt.UserRole) == file_dir:
                    target_item = item
                if f == item.text(0):
                    is_exit = True
            if (not is_exit) and f:
#                self.combo_box_filename.setItemText(self.combo_box_filename.currentIndex(), f)
                target_item.setText(0, f + filetype)
                filename = f
                self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist, fre)
            else:
                self.line_edit_file_name.setText(filename)
                
    def slot_change_file_stime(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
#            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
            if file_dir[0] == '_':
                if file_dir == '_mergefile':
                    data_stime = self.merge_start_time_limit
                else:
                    data_stime = self.dict_data[file_dir].time_range[0]
            else:
#                file = Normal_DataFile(file_dir)
                file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
                data_stime = file.time_range[0]
            starttime = self.line_edit_starttime.text()
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
            if Time_Model.is_std_format(starttime):
                if Time_Model.is_in_range(data_stime, etime, starttime):
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                    self.line_edit_starttime.setText(
                            Time_Model.timestr_to_stdtimestr(starttime))
                    stime = Time_Model.timestr_to_stdtimestr(starttime)
                    self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist, fre)
                    item = self.tree_widget_export_paras.topLevelItem(index)
                    item.setText(1, stime)
                else:
                    self.line_edit_starttime.setText(stime)
                    QMessageBox.information(self,
                                    QCoreApplication.translate('ParameterExportDialog', '输入提示'),
                                    QCoreApplication.translate('ParameterExportDialog', '起始时间不在范围内'))
            else:
                self.line_edit_starttime.setText(stime)
                QMessageBox.information(self,
                                QCoreApplication.translate('ParameterExportDialog', '输入提示'),
                                QCoreApplication.translate('ParameterExportDialog', '''<b>请输入正确时间格式</b>
                                                           <br>HH
                                                           <br>HH:MM
                                                           <br>HH:MM:SS
                                                           <br>HH:MM:SS.FFF
                                                           <br>HH:MM:SS:FFF'''))
    
    def slot_change_file_etime(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
#            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
            if file_dir[0] == '_':
                if file_dir == '_mergefile':
                    data_etime = self.merge_end_time_limit
                else:
                    data_etime = self.dict_data[file_dir].time_range[1]
            else:
#                file = Normal_DataFile(file_dir)
                file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
                data_etime = file.time_range[1]
            endtime = self.line_edit_endtime.text()
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
            if Time_Model.is_std_format(endtime):
                if Time_Model.is_in_range(stime, data_etime, endtime):
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                    self.line_edit_endtime.setText(
                            Time_Model.timestr_to_stdtimestr(endtime))
                    etime = Time_Model.timestr_to_stdtimestr(endtime)
                    self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist, fre)
                    item = self.tree_widget_export_paras.topLevelItem(index)
                    item.setText(2, etime)
                else:
                    self.line_edit_endtime.setText(etime)
                    QMessageBox.information(self,
                                    QCoreApplication.translate('ParameterExportDialog', '输入提示'),
                                    QCoreApplication.translate('ParameterExportDialog', '终止时间不在范围内'))
            else:
                self.line_edit_endtime.setText(etime)
                QMessageBox.information(self,
                                QCoreApplication.translate('ParameterExportDialog', '输入提示'),
                                QCoreApplication.translate('ParameterExportDialog', '''<b>请输入正确时间格式</b>
                                                           <br>HH
                                                           <br>HH:MM
                                                           <br>HH:MM:SS
                                                           <br>HH:MM:SS.FFF
                                                           <br>HH:MM:SS:FFF'''))

    def slot_change_fre(self):
        
        file_dir = self.current_file_dir
        if file_dir:
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
            str_fre = self.line_edit_fre.text()
            if str_fre:
                try:
                    f = int(str_fre)
                    if f <= 0:
                        QMessageBox.information(self,
                                        QCoreApplication.translate('ParameterExportDialog', '输入提示'),
                                        QCoreApplication.translate('ParameterExportDialog', '频率不能小于等于0'))
                    else:
                        fre = f
                except:
                    QMessageBox.information(self,
                                    QCoreApplication.translate('ParameterExportDialog', '输入提示'),
                                    QCoreApplication.translate('ParameterExportDialog', '频率非整数'))
                finally:
                    pass
                self.line_edit_fre.setText(str(fre))
                item = self.tree_widget_export_paras.topLevelItem(index)
                item.setText(3, str(fre))
                self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist, fre)
                
    def slot_change_all_file_time(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
#            确保时间是正确的
            self.slot_change_file_stime()
            self.slot_change_file_etime()
            index, fn, ft, tstime, tetime, pl, fr = self.file_info[file_dir]
            for file in self.file_info:
                if file != file_dir:
                    index, filename, filetype, stime, etime, paralist, fre = self.file_info[file]
#                    先判断开始时间
                    if Time_Model.is_in_range(stime, etime, tstime):
                        stime = tstime
#                    在判断结束时间
                    if Time_Model.is_in_range(stime, etime, tetime):
                        etime = tetime
                    item = self.tree_widget_export_paras.topLevelItem(index)
                    item.setText(0, filename + ft)
                    item.setText(1, stime)
                    item.setText(2, etime)
                    item.setText(3, str(fr))
                    self.file_info[file] = (index, filename, ft, stime, etime, paralist, fr)
                    
#    合并
    def slot_merge(self):
        
        if self.file_info and not self.is_merge:
            self.is_merge = True
            self.merge_use_file_info = self.file_info
            self.current_file_dir = '_mergefile'
    
            st = None
            et = None
            pl = None
            fr = None
            for file_dir in self.file_info:
                index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
                if not st:
                    st = stime
                else:
                    if Time_Model.compare(st, stime) == -1:
                        st = stime
                if not et:
                    et = etime
                else:
                    if Time_Model.compare(et, etime) == 1:
                        et = etime
                if not pl:
                    pl = paralist
                else:
                    pl.extend(paralist)
                if not fr:
                    fr = fre
                else:
                    if fr > fre:
                        fr = fre
            i = 0
            fn = 'merge_result'
            ft = '.txt'
            self.tree_widget_export_paras.clear()
#            在树组件中显示
            item = QTreeWidgetItem(self.tree_widget_export_paras)
            item.setIcon(0, self.outfile_icon)
            item.setText(0, fn + ft)
            item.setData(0, Qt.UserRole, '_mergefile')
            item.setText(1, st)
            item.setText(2, et)
            item.setText(3, str(fr))
            for paraname in pl:
                child_item = QTreeWidgetItem(item)
                child_item.setIcon(0, self.para_icon)
                child_item.setData(0, Qt.UserRole, paraname)
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope paralist'] and
                    paraname in self._data_dict):
                    if CONFIG.OPTION['data dict scope style'] == 0:
                        temp_str = self._data_dict[paraname][0]
                    if CONFIG.OPTION['data dict scope style'] == 1:
                        temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                    if CONFIG.OPTION['data dict scope style'] == 2:
                        temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                    child_item.setText(0, temp_str)
                else:
                    child_item.setText(0, paraname)

            self.file_info.clear()
            self.merge_start_time_limit = st
            self.merge_end_time_limit = et
            self.file_info['_mergefile'] = (i, fn, ft, st, et, pl, fr)
            
            self.combo_box_filetype.setCurrentIndex(0)
            self.line_edit_starttime.setText(st)
            self.line_edit_endtime.setText(et)
            self.line_edit_fre.setText(str(fr))
            self.line_edit_file_name.setText(fn)
            self.line_edit_file_dir.setText(self.dir)

    def accept(self):
        
        self.signal_send_status.emit('导出数据中...', 0)
        existint_file = ''
        for file_dir in self.file_info:
            index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
            filepath = self.line_edit_file_dir.text() + '\\' + filename + filetype
            if os.path.exists(filepath):
                existint_file += filename + filetype + '\n'
        if existint_file:
            existint_file = '以下文件已存在导出路径中：\n' + existint_file
            QMessageBox.information(self,
                                    QCoreApplication.translate('ParameterExportDialog', '导出提示'),
                                    QCoreApplication.translate('ParameterExportDialog', existint_file))
        else:
            if not self.is_merge:
                for file_dir in self.file_info:
                    index, filename, filetype, stime, etime, paralist, fre = self.file_info[file_dir]
        #            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
                    if file_dir[0] == '_':
                        real_timerange, data = self.dict_data[file_dir].get_trange_data(stime, etime)
                    else:
                        data = DataFactory(file_dir, paralist, self._dict_filetype[file_dir])
                        real_timerange, data = data.get_trange_data(stime, etime)
                    filepath = self.line_edit_file_dir.text() + '\\' + filename + filetype
                    file_outpout = DataFile(filepath)
        #            导出TXT文件
                    if filetype == '.txt':
                        file_outpout.save_file(filepath , data , sep = '\t')
        #            导出CSV文件
                    if filetype == '.csv':
                        file_outpout.save_file(filepath , data , sep = ',')
        #            导出MAT文件
                    if filetype == '.mat':
                        file_outpout.save_matfile(filepath, data)
                    CONFIG.OPTION['dir of export data'] = self.line_edit_file_dir.text()
                self.signal_send_status.emit('导出数据成功！', 1500)
            else:
#                在这里添加同步导出的
#                self.merge_use_file_info和self.file_info['mergefile']变量存储着导出所需的文件信息
                pass
            
            QDialog.accept(self)
            
    def display_file_info(self, dict_paras):
        
        stime = ''
        etime = ''
        f = ''
        sf = ''
        for index, file_dir in enumerate(dict_paras):
            if type(dict_paras[file_dir]) == list:
#                file = Normal_DataFile(file_dir)
                file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
                filename = file.filename[:-4] + '(export' + str(index) + ')'
                start = file.time_range[0]
                end = file.time_range[1]
                paralist = dict_paras[file_dir]
                fre = file.sample_frequency
            elif type(dict_paras[file_dir]) == pd.DataFrame:
                data = DataFactory(dict_paras[file_dir])
                self.dict_data[file_dir] = data
                filename = 'FastPlot DataFile ' + str(index)
                start = data.time_range[0]
                end = data.time_range[1]
                paralist = data.get_paralist()
                fre = data.sample_frequency
            elif type(dict_paras[file_dir]) == DataFactory:
                data = dict_paras[file_dir]
                self.dict_data[file_dir] = data
                filename = 'FastPlot DataFile ' + str(index)
                start = data.time_range[0]
                end = data.time_range[1]
                paralist = data.get_paralist()
                fre = data.sample_frequency
#            在树组件中显示
            item = QTreeWidgetItem(self.tree_widget_export_paras)
            item.setIcon(0, self.outfile_icon)
            item.setText(0, filename + '.txt')
            item.setData(0, Qt.UserRole, file_dir)
            item.setText(1, start)
            item.setText(2, end)
            item.setText(3, str(fre))
            for paraname in paralist:
                child_item = QTreeWidgetItem(item)
                child_item.setIcon(0, self.para_icon)
                child_item.setData(0, Qt.UserRole, paraname)
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope paralist'] and
                    paraname in self._data_dict):
                    if CONFIG.OPTION['data dict scope style'] == 0:
                        temp_str = self._data_dict[paraname][0]
                    if CONFIG.OPTION['data dict scope style'] == 1:
                        temp_str = paraname + '(' + self._data_dict[paraname][0] + ')'
                    if CONFIG.OPTION['data dict scope style'] == 2:
                        temp_str = self._data_dict[paraname][0] + '(' + paraname + ')'
                    child_item.setText(0, temp_str)
                else:
                    child_item.setText(0, paraname)
#            在复选框中显示
#            self.combo_box_filename.addItem(filename)
#            self.combo_box_filename.setItemData(i, file_dir, Qt.UserRole)
#            存取文件信息（文件名，文件类型，起始时间，终止时间，排好序的参数列表），以供导出
            self.file_info[file_dir] = (index, filename, '.txt', start, end, paralist, fre)
            if index == 0:
                stime = start
                etime = end
                f = filename
                sf = str(fre)
                self.current_file_dir = file_dir
#        self.combo_box_filename.setCurrentIndex(0)
        self.tree_widget_export_paras.setCurrentItem(self.tree_widget_export_paras.topLevelItem(0))
        self.combo_box_filetype.setCurrentIndex(0)
        self.line_edit_starttime.setText(stime)
        self.line_edit_endtime.setText(etime)
        self.line_edit_fre.setText(sf)
        self.line_edit_file_name.setText(f)
        self.line_edit_file_dir.setText(self.dir)
        
    def load_data_dict(self):
        
        try:
            with open(CONFIG.SETUP_DIR + r'\data\data_dicts\\' + CONFIG.OPTION['data dict version']) as f_obj:
                self._data_dict = json.load(f_obj)
        except:
            pass            

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('ParameterExportDialog', '导出参数数据'))
        self.group_box_preview.setTitle(_translate('ParameterExportDialog', '导出预览'))
        self.tree_widget_export_paras.headerItem().setText(0, _translate('ParameterExportDialog', '文件名'))
        self.tree_widget_export_paras.headerItem().setText(1, _translate('ParameterExportDialog', '起始时间'))
        self.tree_widget_export_paras.headerItem().setText(2, _translate('ParameterExportDialog', '终止时间'))
        self.tree_widget_export_paras.headerItem().setText(3, _translate('ParameterExportDialog', '频率'))
        self.group_box_setting.setTitle(_translate('ParameterExportDialog', '导出设置'))
        self.groupBox.setTitle(_translate('ParameterExportDialog', '时间设置'))
        self.label_starttime.setText(_translate('ParameterExportDialog', '起始时间'))
        self.label_endtime.setText(_translate('ParameterExportDialog', '终止时间'))
        self.label_fre.setText(_translate('ParameterExportDialog', '频率'))
        self.push_btn_apply_all_files.setText(_translate('ParameterExportDialog', '全部设置'))
        self.group_box_file_setting.setTitle(_translate('ParameterExportDialog', '文件设置'))
        self.label_file_type.setText(_translate('ParameterExportDialog', '文件类型'))
        self.label_file_name.setText(_translate('ParameterExportDialog', '文件名'))
        self.label_file_dir.setText(_translate('ParameterExportDialog', '文件路径'))
        self.tool_btn_sel_filedir.setText(_translate('ParameterExportDialog', '...'))
        self.combo_box_filetype.setItemText(0, _translate('ParameterExportDialog', 'TXT file'))
        self.combo_box_filetype.setItemText(1, _translate('ParameterExportDialog', 'CSV file'))
        self.combo_box_filetype.setItemText(2, _translate('ParameterExportDialog', 'MAT file'))
        self.push_btn_merge.setText(_translate('ParameterExportDialog', '合并'))
        self.push_btn_confirm.setText(_translate('ParameterExportDialog', '导出'))
        self.push_btn_cancel.setText(_translate('ParameterExportDialog', '取消'))
        
class FileProcessDialog(QDialog):
    
    signal_send_status = pyqtSignal(str, int)
    
    def __init__(self, parent = None, files = [], time_intervals = {}, dict_filetype = None):
    
        super().__init__(parent)
        
        self.outfile_icon = QIcon(CONFIG.ICON_FILE_EXPORT)
        self.para_icon = QIcon(CONFIG.ICON_PARA)
        self.file_icon = QIcon(CONFIG.ICON_FILE)
        self.file_info = {}
        self.current_interval_item = None
        self.current_floder_item = None
        if dict_filetype:
            self._dict_filetype = dict_filetype
        if os.path.exists(CONFIG.OPTION['work dir']):
            self.dir = CONFIG.OPTION['work dir']
        else:
            self.dir = CONFIG.SETUP_DIR
        
        self.setup()
        self.display_file_info(files, time_intervals)
    
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(700, 480)
        self.verticalLayout_5 = QVBoxLayout(self)
        self.verticalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_5.setSpacing(2)
        self.group_box_preview = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_preview)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.tree_widget_files = QTreeWidget(self.group_box_preview)
#        让树可支持右键菜单(step 1)
        self.tree_widget_files.setContextMenuPolicy(Qt.CustomContextMenu)
#        添加右键动作
        self.action_add_interval = QAction(self.tree_widget_files)
        self.action_add_interval.setText(QCoreApplication.
                                         translate('FileProcessDialog', '增加时间段'))
        self.action_del_interval = QAction(self.tree_widget_files)
        self.action_del_interval.setText(QCoreApplication.
                                         translate('FileProcessDialog', '删除时间段'))
        self.action_del_file = QAction(self.tree_widget_files)
        self.action_del_file.setText(QCoreApplication.
                                     translate('FileProcessDialog', '删除文件'))
#        让顶级项没有扩展符空白
#        self.tree_widget_files.setRootIsDecorated(False)
#        设置树组件头部显示方式
        headerview = self.tree_widget_files.header()
        headerview.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerview.setMinimumSectionSize(100)
        self.tree_widget_files.setHeader(headerview)
        
        self.verticalLayout.addWidget(self.tree_widget_files)
        self.verticalLayout_5.addWidget(self.group_box_preview)
        self.group_box_setting = QGroupBox(self)
        self.verticalLayout_4 = QVBoxLayout(self.group_box_setting)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(2)
#        self.combo_box_filename = QComboBox(self.group_box_setting)
#        self.combo_box_filename.setMinimumSize(QSize(0, 24))
#        self.combo_box_filename.setMaximumSize(QSize(16777215, 24))
#        self.verticalLayout_4.addWidget(self.combo_box_filename)
        self.groupBox = QGroupBox(self.group_box_setting)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_7.setSpacing(2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.horizontalLayout = QHBoxLayout()
        self.label_starttime = QLabel(self.groupBox)
        self.label_starttime.setMinimumSize(QSize(60, 24))
        self.label_starttime.setMaximumSize(QSize(60, 24))
        self.horizontalLayout.addWidget(self.label_starttime)
        self.line_edit_starttime = QLineEdit(self.groupBox)
        self.line_edit_starttime.setMinimumSize(QSize(0, 24))
        self.line_edit_starttime.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_starttime)
        self.label_endtime = QLabel(self.groupBox)
        self.label_endtime.setMinimumSize(QSize(60, 24))
        self.label_endtime.setMaximumSize(QSize(60, 24))
        self.horizontalLayout.addWidget(self.label_endtime)
        self.line_edit_endtime = QLineEdit(self.groupBox)
        self.line_edit_endtime.setMinimumSize(QSize(0, 24))
        self.line_edit_endtime.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_endtime)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QHBoxLayout()
        self.label_fre = QLabel(self.groupBox)
        self.label_fre.setMinimumSize(QSize(60, 24))
        self.label_fre.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_6.addWidget(self.label_fre)
        self.line_edit_fre = QLineEdit(self.groupBox)
        self.line_edit_fre.setMinimumSize(QSize(0, 24))
        self.line_edit_fre.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_6.addWidget(self.line_edit_fre)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
#        self.push_btn_apply_all_files = QPushButton(self.groupBox)
#        self.push_btn_apply_all_files.setMinimumSize(QSize(100, 24))
#        self.push_btn_apply_all_files.setMaximumSize(QSize(100, 24))
##        避免按钮默认选中并按Enter键会执行的情况
#        self.push_btn_apply_all_files.setFocusPolicy(Qt.NoFocus) 
#        self.horizontalLayout_7.addWidget(self.push_btn_apply_all_files)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.group_box_file_setting = QGroupBox(self.group_box_setting)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_file_setting)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_file_type = QLabel(self.group_box_file_setting)
        self.label_file_type.setMinimumSize(QSize(60, 24))
        self.label_file_type.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_3.addWidget(self.label_file_type)
        self.combo_box_filetype = QComboBox(self.group_box_file_setting)
        self.combo_box_filetype.setMinimumSize(QSize(0, 24))
        self.combo_box_filetype.setMaximumSize(QSize(16777215, 24))
        self.combo_box_filetype.addItem('')
#        设置每个项目的数据，为后续选择导出文件所使用
        self.combo_box_filetype.setItemData(0, '.txt', Qt.UserRole)
        self.combo_box_filetype.addItem('')
        self.combo_box_filetype.setItemData(1, '.csv', Qt.UserRole)
        self.combo_box_filetype.addItem('')
        self.combo_box_filetype.setItemData(2, '.mat', Qt.UserRole)
        self.horizontalLayout_3.addWidget(self.combo_box_filetype)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_file_name = QLabel(self.group_box_file_setting)
        self.label_file_name.setMinimumSize(QSize(60, 24))
        self.label_file_name.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_4.addWidget(self.label_file_name)
        self.line_edit_file_name = QLineEdit(self.group_box_file_setting)
        self.line_edit_file_name.setMinimumSize(QSize(0, 24))
        self.line_edit_file_name.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_4.addWidget(self.line_edit_file_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_file_dir = QLabel(self.group_box_file_setting)
        self.label_file_dir.setMinimumSize(QSize(60, 24))
        self.label_file_dir.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_2.addWidget(self.label_file_dir)
        self.line_edit_file_dir = QLineEdit(self.group_box_file_setting)
        self.line_edit_file_dir.setMinimumSize(QSize(0, 24))
        self.line_edit_file_dir.setMaximumSize(QSize(16777215, 24))
        self.line_edit_file_dir.setReadOnly(True)
        self.horizontalLayout_2.addWidget(self.line_edit_file_dir)
        self.tool_btn_sel_filedir = QToolButton(self.group_box_file_setting)
        self.tool_btn_sel_filedir.setMinimumSize(QSize(24, 24))
        self.tool_btn_sel_filedir.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_2.addWidget(self.tool_btn_sel_filedir)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.group_box_file_setting)
        self.verticalLayout_5.addWidget(self.group_box_setting)
        self.horizontalLayout_5 = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.push_btn_easter_egg = QPushButton(self)
        self.push_btn_easter_egg.setHidden(True)
        self.horizontalLayout_5.addWidget(self.push_btn_easter_egg)
        self.push_btn_apply_all_files = QPushButton(self.groupBox)
        self.push_btn_apply_all_files.setMinimumSize(QSize(100, 24))
        self.push_btn_apply_all_files.setMaximumSize(QSize(100, 24))
#        避免按钮默认选中并按Enter键会执行的情况
        self.push_btn_apply_all_files.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout_5.addWidget(self.push_btn_apply_all_files)
        self.push_btn_confirm = QPushButton(self)
        self.push_btn_confirm.setMinimumSize(QSize(0, 24))
        self.push_btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_5.addWidget(self.push_btn_confirm)
        self.push_btn_cancel = QPushButton(self)
        self.push_btn_cancel.setMinimumSize(QSize(0, 24))
        self.push_btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_5.addWidget(self.push_btn_cancel)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.retranslateUi()
# =======连接信号与槽
# =============================================================================
#        使右键时能弹出菜单(step 2)
        self.tree_widget_files.customContextMenuRequested.connect(
                self.on_tree_context_menu)
        self.action_add_interval.triggered.connect(self.slot_add_interval)
        self.action_del_interval.triggered.connect(self.slot_del_interval)
        self.action_del_file.triggered.connect(self.slot_del_file)
        
        self.tool_btn_sel_filedir.clicked.connect(self.slot_sel_dir)        
#        self.combo_box_filename.currentIndexChanged.connect(self.slot_change_current_file)
        self.tree_widget_files.itemClicked.connect(self.slot_change_current_file)
        self.combo_box_filetype.currentIndexChanged.connect(self.slot_change_filetype)        
        self.line_edit_file_name.editingFinished.connect(self.slot_change_filename)
        self.line_edit_starttime.editingFinished.connect(self.slot_change_file_stime)
        self.line_edit_endtime.editingFinished.connect(self.slot_change_file_etime)
        self.line_edit_fre.editingFinished.connect(self.slot_change_fre)
        self.push_btn_apply_all_files.clicked.connect(self.slot_change_all_file_time)
        
        self.push_btn_confirm.clicked.connect(self.accept)
        self.push_btn_cancel.clicked.connect(self.reject)

#    右键菜单的事件处理(step 3)
    def on_tree_context_menu(self, pos):
        
#        记录右击时鼠标所在的item
        sel_item = self.tree_widget_files.itemAt(pos)
        
#        如果鼠标不在item上，不显示右键菜单
        if sel_item:
#            创建菜单，添加动作，显示菜单
            menu = QMenu(self.tree_widget_files)
            menu.addActions([self.action_add_interval,
                             self.action_del_interval,
                             self.action_del_file])
            if sel_item.parent():
                self.slot_change_current_file(sel_item)
                self.action_add_interval.setDisabled(True)
                self.action_del_interval.setDisabled(False)
                self.action_del_file.setDisabled(True)
            else:
                self.current_floder_item = sel_item
                self.action_add_interval.setDisabled(False)
                self.action_del_interval.setDisabled(True)
                self.action_del_file.setDisabled(False)
            menu.exec_(self.tree_widget_files.mapToGlobal(pos))
            
    def slot_add_interval(self):
        
        if self.current_floder_item:
            file_dir = self.current_floder_item.data(0, Qt.UserRole)
#            file = Normal_DataFile(file_dir)
            file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
            start = file.time_range[0]
            end = file.time_range[1]
            fre = file.sample_frequency
            
            label_file =  file_dir + 'Interval1'
            i = 1
            while label_file in self.file_info:
                i += 1
                label_file = file_dir + 'Interval' + str(i)
            filename = 'Interval' + str(i)
            
            item = QTreeWidgetItem(self.current_floder_item)
            item.setIcon(0, self.file_icon)
            item.setText(0, filename + '.txt')
            item.setData(0, Qt.UserRole, label_file)
            item.setText(1, start)
            item.setText(2, end)
            item.setText(3, str(fre))
            self.file_info[label_file] = (item, file_dir, filename, '.txt', start, end, fre)
            self.slot_change_current_file(item)
    
    def slot_del_interval(self):
        
        if self.current_interval_item:
            label_file = self.current_interval_item.data(0, Qt.UserRole)
            del self.file_info[label_file] 
            parent = self.current_interval_item.parent()
            parent.takeChild(parent.indexOfChild(self.current_interval_item))
            if parent.childCount() == 0:
                self.tree_widget_files.takeTopLevelItem(
                    self.tree_widget_files.indexOfTopLevelItem(parent))
            self.current_interval_item = None
            self.slot_change_current_file(None)
    
    def slot_del_file(self):
        
        if self.current_floder_item:
            childs = self.current_floder_item.takeChildren()
            if self.current_interval_item in childs:
                self.current_interval_item = None
                self.slot_change_current_file(None)
            for child in childs:
                label_file = child.data(0, Qt.UserRole)
                del self.file_info[label_file]
            self.tree_widget_files.takeTopLevelItem(
                    self.tree_widget_files.indexOfTopLevelItem(self.current_floder_item))
            self.current_floder_item = None
        
#    让用户选择项目的路径
    def slot_sel_dir(self):
        
        filedir = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('FileProcessDialog', '导出路径'),
                                                   self.dir)
        if filedir:
            filedir = filedir.replace('/','\\')
            self.dir = filedir
            self.line_edit_file_dir.setText(filedir)
            
    def slot_change_current_file(self, item):
        
#        file_dir = self.combo_box_filename.itemData(index, Qt.UserRole)
        index = self.tree_widget_files.indexOfTopLevelItem(item)
        if index == -1:
            self.current_interval_item = item
        if self.current_interval_item:
            self.group_box_setting.setEnabled(True)
            label = self.current_interval_item.data(0, Qt.UserRole)
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
            self.line_edit_starttime.setText(stime)
            self.line_edit_endtime.setText(etime)
            self.line_edit_fre.setText(str(fre))
            self.combo_box_filetype.setCurrentIndex(
                    self.combo_box_filetype.findData(filetype, Qt.UserRole))
            self.line_edit_file_name.setText(filename)
        else:
            self.group_box_setting.setEnabled(False)
            self.line_edit_endtime.clear()
            self.line_edit_starttime.clear()
            self.line_edit_fre.clear()
            self.line_edit_file_name.clear()
        
    def slot_change_filetype(self, index):
        
#        file_dir = self.combo_box_filename.currentData()
#        file_dir = self.current_file_dir
        if self.current_interval_item:
            label = self.current_interval_item.data(0, Qt.UserRole)
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
            filetype = self.combo_box_filetype.currentData()
            file_item.setText(0, filename + filetype)
            self.file_info[label] = (file_item, file_dir, filename, filetype, stime, etime, fre)
            
    def slot_change_filename(self):
        
#        file_dir = self.combo_box_filename.currentData()
#        file_dir = self.current_file_dir
        if self.current_interval_item:
            label = self.current_interval_item.data(0, Qt.UserRole)
            f = self.line_edit_file_name.text()
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
            is_exit = False
            for file_label in self.file_info:
                fi, fd, fn, ft, st, et, fr = self.file_info[file_label]
                if f == fn and label != file_label:
                    is_exit = True
            if (not is_exit) and f:
#                self.combo_box_filename.setItemText(self.combo_box_filename.currentIndex(), f)
                file_item.setText(0, f + filetype)
                self.file_info[label] = (file_item, file_dir, f, filetype, stime, etime, fre)
            else:
                self.line_edit_file_name.setText(filename)
                
    def slot_change_file_stime(self):
        
#        file_dir = self.combo_box_filename.currentData()
#        file_dir = self.current_file_dir
        if self.current_interval_item:
            parent = self.current_interval_item.parent()
            file_dir = parent.data(0, Qt.UserRole)
            label = self.current_interval_item.data(0, Qt.UserRole)
#            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
#            file = Normal_DataFile(file_dir)
            file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
            data_stime = file.time_range[0]
            starttime = self.line_edit_starttime.text()
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
            if Time_Model.is_std_format(starttime):
                if Time_Model.is_in_range(data_stime, etime, starttime):
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                    self.line_edit_starttime.setText(
                            Time_Model.timestr_to_stdtimestr(starttime))
                    stime = Time_Model.timestr_to_stdtimestr(starttime)
                    self.file_info[label] = (file_item, file_dir, filename, filetype, stime, etime, fre)
                    file_item.setText(1, stime)
                else:
                    self.line_edit_starttime.setText(stime)
                    QMessageBox.information(self,
                                    QCoreApplication.translate('FileProcessDialog', '输入提示'),
                                    QCoreApplication.translate('FileProcessDialog', '起始时间不在范围内'))
            else:
                self.line_edit_starttime.setText(stime)
                QMessageBox.information(self,
                                QCoreApplication.translate('FileProcessDialog', '输入提示'),
                                QCoreApplication.translate('FileProcessDialog', '''<b>请输入正确时间格式</b>
                                                           <br>HH
                                                           <br>HH:MM
                                                           <br>HH:MM:SS
                                                           <br>HH:MM:SS.FFF
                                                           <br>HH:MM:SS:FFF'''))
    
    def slot_change_file_etime(self):
        
#        file_dir = self.combo_box_filename.currentData()
#        file_dir = self.current_file_dir
        if self.current_interval_item:
            parent = self.current_interval_item.parent()
            file_dir = parent.data(0, Qt.UserRole)
            label = self.current_interval_item.data(0, Qt.UserRole)
#            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
#            file = Normal_DataFile(file_dir)
            file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
            data_etime = file.time_range[1]
            endtime = self.line_edit_endtime.text()
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
            if Time_Model.is_std_format(endtime):
                if Time_Model.is_in_range(stime, data_etime, endtime):
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                    self.line_edit_endtime.setText(
                            Time_Model.timestr_to_stdtimestr(endtime))
                    etime = Time_Model.timestr_to_stdtimestr(endtime)
                    self.file_info[label] = (file_item, file_dir, filename, filetype, stime, etime, fre)
                    file_item.setText(2, etime)
                else:
                    self.line_edit_endtime.setText(etime)
                    QMessageBox.information(self,
                                    QCoreApplication.translate('FileProcessDialog', '输入提示'),
                                    QCoreApplication.translate('FileProcessDialog', '终止时间不在范围内'))
            else:
                self.line_edit_endtime.setText(etime)
                QMessageBox.information(self,
                                QCoreApplication.translate('FileProcessDialog', '输入提示'),
                                QCoreApplication.translate('FileProcessDialog', '''<b>请输入正确时间格式</b>
                                                           <br>HH
                                                           <br>HH:MM
                                                           <br>HH:MM:SS
                                                           <br>HH:MM:SS.FFF
                                                           <br>HH:MM:SS:FFF'''))
    
    def slot_change_fre(self):
        
#        file_dir = self.combo_box_filename.currentData()
#        file_dir = self.current_file_dir
        if self.current_interval_item:
            label = self.current_interval_item.data(0, Qt.UserRole)
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
            str_fre = self.line_edit_fre.text()
            if str_fre:
                try:
                    f = int(str_fre)
                    if f <= 0:
                        QMessageBox.information(self,
                                        QCoreApplication.translate('FileProcessDialog', '输入提示'),
                                        QCoreApplication.translate('FileProcessDialog', '频率不能小于等于0'))
                    else:
                        fre = f
                except:
                    QMessageBox.information(self,
                                    QCoreApplication.translate('FileProcessDialog', '输入提示'),
                                    QCoreApplication.translate('FileProcessDialog', '频率非整数'))
                finally:
                    pass
                self.line_edit_fre.setText(str(fre))
                file_item.setText(3, str(fre))
                self.file_info[label] = (file_item, file_dir, filename, filetype, stime, etime, fre)
                
    def slot_change_all_file_time(self):
        
#        file_dir = self.combo_box_filename.currentData()
#        file_dir = self.current_file_dir
        if self.current_interval_item:
            label = self.current_interval_item.data(0, Qt.UserRole)
#            确保时间是正确的
            self.slot_change_file_stime()
            self.slot_change_file_etime()
            self.slot_change_fre()
            file_item, fd, fn, ft, tstime, tetime, f = self.file_info[label]
            for file in self.file_info:
                if file != label:
                    file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[file]
#                    先判断开始时间
#                    if Time_Model.is_in_range(stime, etime, tstime):
#                        stime = tstime
#                    在判断结束时间
#                    if Time_Model.is_in_range(stime, etime, tetime):
#                        etime = tetime
                    file_item.setText(0, filename + ft)
#                    file_item.setText(1, stime)
#                    file_item.setText(2, etime)
                    file_item.setText(3, str(f))
                    self.file_info[file] = (file_item, file_dir, filename, ft, stime, etime, f)
                        
    def accept(self):
        
        self.signal_send_status.emit('导出数据中...', 0)
#        if self.tree_widget_files:
#            count = self.tree_widget_files.topLevelItemCount()
#            for i in range(count):
#                parent = self.tree_widget_files.topLevelItem(i)
#                file_dir = parent.data(0, Qt.UserRole)
#                file = Normal_DataFile(file_dir)
#                data = file.cols_input(file_dir, file.paras_in_file, '\s+', stime, etime)
#                childs = parent.child()
#        这样实现效率偏低
        for label in self.file_info:
            file_item, file_dir, filename, filetype, stime, etime, fre = self.file_info[label]
#            file = Normal_DataFile(file_dir)
            file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
            folder = self.line_edit_file_dir.text() + '\\' + file.filename[:-4]
            if not os.path.exists(folder):
                os.mkdir(folder)
            data = file.cols_input(file_dir, file.paras_in_file, file.sep, stime, etime)
            ana = DataAnalysis(file.time_format)
            if fre > file.sample_frequency:
                data = ana.upsample(data, fre)
            if fre < file.sample_frequency:
                data = ana.downsample(data, fre)
            filepath = folder + '\\' + filename + filetype
            file_outpout = DataFile(filepath)
#            导出TXT文件
            if filetype == '.txt':
                file_outpout.save_file(filepath , data , sep = '\t')
#            导出CSV文件
            if filetype == '.csv':
                file_outpout.save_file(filepath , data , sep = ',')
#            导出MAT文件
            if filetype == '.mat':
                file_outpout.save_matfile(filepath, data)
        self.signal_send_status.emit('导出数据成功！', 1500)
        
        QDialog.accept(self)
            
    def display_file_info(self, files, time_intervals):

        for index, file_dir in enumerate(files):
#            file = Normal_DataFile(file_dir)
            file = DataFile_Factory(file_dir, **self._dict_filetype[file_dir])
            filename = file.filename[:-4]
            start = file.time_range[0]
            end = file.time_range[1]
            fre = file.sample_frequency
#            在树组件中显示
            item = QTreeWidgetItem(self.tree_widget_files)
            item.setIcon(0, self.outfile_icon)
            dis_str= filename + '-(' + start + '-' + end + ')-' + str(fre)
            item.setText(0, dis_str)
            item.setData(0, Qt.UserRole, file_dir)
#            item.setText(1, start)
#            item.setText(2, end)
#            item.setText(3, str(fre))
            if time_intervals:
                for i, interval_name in enumerate(time_intervals):
                    ti = time_intervals[interval_name]
                    result_ti = Time_Model.and_time_intervals((start, end), ti)
                    if result_ti:
                        ti_st, ti_et = result_ti
                        label_file = file_dir + interval_name
                        child = QTreeWidgetItem(item)
                        child.setIcon(0, self.file_icon)
                        ti_name = interval_name
                        child.setText(0, ti_name + '.txt')
                        child.setData(0, Qt.UserRole, label_file)
                        child.setText(1, ti_st)
                        child.setText(2, ti_et)
                        child.setText(3, str(fre))
                        self.file_info[label_file] = (child, file_dir, ti_name, '.txt', ti_st, ti_et, fre)
                        if index == 0 and i == 0:
                            display_stime = ti_st
                            display_etime = ti_et
                            display_f = fre
                            display_fname = ti_name
                            self.current_interval_item = child
#            如果没有输入时间段，则默认导出整段时间
            else:
                label_file = file_dir + ' Whole'
                child = QTreeWidgetItem(item)
                child.setIcon(0, self.file_icon)
                child.setText(0, filename + '.txt')
                child.setData(0, Qt.UserRole, label_file)
                child.setText(1, start)
                child.setText(2, end)
                child.setText(3, str(fre))
#            在复选框中显示
#            self.combo_box_filename.addItem(filename)
#            self.combo_box_filename.setItemData(i, file_dir, Qt.UserRole)
#            存取文件信息（文件对应的item，文件路径，输出文件名，输出文件类型，起始时间，终止时间，频率），以供导出
                self.file_info[label_file] = (child, file_dir, filename, '.txt', start, end, fre)
                if index == 0:
                    self.current_interval_item = child
                    display_stime = start
                    display_etime = end
                    display_f = fre
                    display_fname = filename
#        self.combo_box_filename.setCurrentIndex(0)
        self.tree_widget_files.setCurrentItem(self.current_interval_item)
        self.tree_widget_files.expandAll()
        self.combo_box_filetype.setCurrentIndex(0)
        self.line_edit_starttime.setText(display_stime)
        self.line_edit_endtime.setText(display_etime)
        self.line_edit_fre.setText(str(display_f))
        self.line_edit_file_name.setText(display_fname)
        self.line_edit_file_dir.setText(self.dir)      

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('FileProcessDialog', '文件数据导出'))
        self.group_box_preview.setTitle(_translate('FileProcessDialog', '预览'))
        self.tree_widget_files.headerItem().setText(0, _translate('FileProcessDialog', '文件名'))
        self.tree_widget_files.headerItem().setText(1, _translate('FileProcessDialog', '起始时间'))
        self.tree_widget_files.headerItem().setText(2, _translate('FileProcessDialog', '终止时间'))
        self.tree_widget_files.headerItem().setText(3, _translate('FileProcessDialog', '频率'))
        self.group_box_setting.setTitle(_translate('FileProcessDialog', '设置'))
        self.groupBox.setTitle(_translate('FileProcessDialog', '时间设置'))
        self.label_starttime.setText(_translate('FileProcessDialog', '起始时间'))
        self.label_endtime.setText(_translate('FileProcessDialog', '终止时间'))
        self.label_fre.setText(_translate('FileProcessDialog', '频率'))
        self.push_btn_apply_all_files.setText(_translate('FileProcessDialog', '全部设置'))
        self.group_box_file_setting.setTitle(_translate('FileProcessDialog', '文件设置'))
        self.label_file_type.setText(_translate('FileProcessDialog', '文件类型'))
        self.label_file_name.setText(_translate('FileProcessDialog', '文件名'))
        self.label_file_dir.setText(_translate('FileProcessDialog', '文件路径'))
        self.tool_btn_sel_filedir.setText(_translate('FileProcessDialog', '...'))
        self.combo_box_filetype.setItemText(0, _translate('FileProcessDialog', 'TXT file'))
        self.combo_box_filetype.setItemText(1, _translate('FileProcessDialog', 'CSV file'))
        self.combo_box_filetype.setItemText(2, _translate('FileProcessDialog', 'MAT file'))
        self.push_btn_confirm.setText(_translate('FileProcessDialog', '导出'))
        self.push_btn_cancel.setText(_translate('FileProcessDialog', '取消'))
        
class SelFunctionDialog(QDialog):
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
        
        self.index = -1
        
        self.setup()
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(250, 180)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.groupBox = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.btn_import_fig_paras = QPushButton(self.groupBox)
        self.btn_import_fig_paras.setMinimumSize(QSize(0, 24))
        self.btn_import_fig_paras.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.btn_import_fig_paras)
        self.btn_import_files = QPushButton(self.groupBox)
        self.btn_import_files.setMinimumSize(QSize(0, 24))
        self.btn_import_files.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.btn_import_files)
        self.btn_aver = QPushButton(self.groupBox)
        self.btn_aver.setMinimumSize(QSize(0, 24))
        self.btn_aver.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.btn_aver)
        self.btn_max = QPushButton(self.groupBox)
        self.btn_max.setMinimumSize(QSize(0, 24))
        self.btn_max.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.btn_max)
        self.btn_min = QPushButton(self.groupBox)
        self.btn_min.setMinimumSize(QSize(0, 24))
        self.btn_min.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.btn_min)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi()
        
        self.btn_import_fig_paras.clicked.connect(self.slot_get_index)
        self.btn_import_files.clicked.connect(self.slot_get_index)
        self.btn_aver.clicked.connect(self.slot_get_index)
        self.btn_max.clicked.connect(self.slot_get_index)
        self.btn_min.clicked.connect(self.slot_get_index)
        
    def slot_get_index(self):
        
#        接收发出信号的那个对象
        sender = QObject.sender(self)
        if (sender == self.btn_import_fig_paras):
            self.index = 0
        if (sender == self.btn_import_files):
            self.index = 1
        if (sender == self.btn_aver):
            self.index = 2
        if (sender == self.btn_max):
            self.index = 3
        if (sender == self.btn_min):
            self.index = 4
        QDialog.accept(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('SelFunctionDialog', '选择功能'))
        self.groupBox.setTitle(_translate('SelFunctionDialog', '请选择功能'))
        self.btn_import_fig_paras.setText(_translate('SelFunctionDialog', '导出时间段数据（绘图参数）'))
        self.btn_import_files.setText(_translate('SelFunctionDialog', '导出时间段数据（文件）'))
        self.btn_aver.setText(_translate('SelFunctionDialog', '导出各时间段的平均值'))
        self.btn_max.setText(_translate('SelFunctionDialog', '导出各时间段的最大值'))
        self.btn_min.setText(_translate('SelFunctionDialog', '导出各时间段的最小值'))
        
class OptionDialog(QDialog):
    
    def __init__(self, parent = None):
    
        if not os.path.exists(CONFIG.OPTION['work dir']):
            CONFIG.OPTION['work dir'] = CONFIG.SETUP_DIR
#        按#RRGGBB格式赋值
        self.font_color = Color.to_hex(CONFIG.OPTION['plot fontcolor'])
        self.line_color = Color.to_hex(CONFIG.OPTION['plot markline color'])
#        字典版本是否被改变
        self.dd_version_changed = False
        super().__init__(parent)
        
        self.setup()
        
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(600, 400)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(6)
        self.horizontalLayout_2 = QHBoxLayout()
        self.list_option = QListWidget(self)
        self.list_option.setMinimumSize(QSize(200, 0))
        self.list_option.setMaximumSize(QSize(200, 16777215))
        item = QListWidgetItem()
        self.list_option.addItem(item)
        item = QListWidgetItem()
        self.list_option.addItem(item)
        item = QListWidgetItem()
        self.list_option.addItem(item)
        self.horizontalLayout_2.addWidget(self.list_option)
        self.stack_option_win = QStackedWidget(self)
        
        self.page_general = QWidget()
        self.verticalLayout_2 = QVBoxLayout(self.page_general)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.groupBox_2 = QGroupBox(self.page_general)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_4.setSpacing(2)
        self.line_edit_work_dir = QLineEdit(self.groupBox_2)
        self.line_edit_work_dir.setMinimumSize(QSize(0, 24))
        self.line_edit_work_dir.setMaximumSize(QSize(16777215, 24))
        self.line_edit_work_dir.setReadOnly(True)
        self.line_edit_work_dir.setText(CONFIG.OPTION['work dir'])
        self.horizontalLayout_4.addWidget(self.line_edit_work_dir)
        self.btn_sel_work_dir = QToolButton(self.groupBox_2)
        self.btn_sel_work_dir.setMinimumSize(QSize(24, 24))
        self.btn_sel_work_dir.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_4.addWidget(self.btn_sel_work_dir)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.stack_option_win.addWidget(self.page_general)
        
        self.page_plot = QWidget()
        self.verticalLayout_3 = QVBoxLayout(self.page_plot)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.group_box_text = QGroupBox(self.page_plot)
        self.verticalLayout_6 = QVBoxLayout(self.group_box_text)
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_6.setSpacing(2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.label_fontszie = QLabel(self.group_box_text)
        self.label_fontszie.setMinimumSize(QSize(100, 24))
        self.label_fontszie.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_5.addWidget(self.label_fontszie)
        self.spinBox = QSpinBox(self.group_box_text)
        self.spinBox.setMinimumSize(QSize(0, 24))
        self.spinBox.setMaximumSize(QSize(16777215, 24))
        self.spinBox.setValue(CONFIG.OPTION['plot fontsize'])
#        字体大小范围在1-40内
#        self.spinBox.setRange(1, 40)
        self.horizontalLayout_5.addWidget(self.spinBox)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.label_fontcolor = QLabel(self.group_box_text)
        self.label_fontcolor.setMinimumSize(QSize(100, 24))
        self.label_fontcolor.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_6.addWidget(self.label_fontcolor)
        self.label_color = QLabel(self.group_box_text)
        self.label_color.setMinimumSize(QSize(0, 24))
        self.label_color.setMaximumSize(QSize(16777215, 24))
        self.label_color.setPalette(QPalette(QColor(self.font_color)))
        self.label_color.setAutoFillBackground(True)
        self.horizontalLayout_6.addWidget(self.label_color)
        self.btn_sel_color = QToolButton(self.group_box_text)
        self.btn_sel_color.setMinimumSize(QSize(24, 24))
        self.btn_sel_color.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_6.addWidget(self.btn_sel_color)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        
        self.hlayout_arrow = QHBoxLayout()
        self.label_arrow = QLabel(self)
        self.label_arrow.setMinimumSize(QSize(100, 24))
        self.label_arrow.setMaximumSize(QSize(100, 24))
        self.hlayout_arrow.addWidget(self.label_arrow)
        self.check_box_arrow = QCheckBox(self)
        self.check_box_arrow.setMinimumSize(QSize(0, 24))
        self.check_box_arrow.setMaximumSize(QSize(16777215, 24))
        if CONFIG.OPTION['plot font arrow']:
            self.check_box_arrow.setChecked(True)
        else:
            self.check_box_arrow.setChecked(False)
        self.hlayout_arrow.addWidget(self.check_box_arrow)
        self.verticalLayout_6.addLayout(self.hlayout_arrow)
        
        self.hlayout_bbox = QHBoxLayout()
        self.label_bbox = QLabel(self)
        self.label_bbox.setMinimumSize(QSize(100, 24))
        self.label_bbox.setMaximumSize(QSize(100, 24))
        self.hlayout_bbox.addWidget(self.label_bbox)
        self.check_box_bbox = QCheckBox(self)
        self.check_box_bbox.setMinimumSize(QSize(0, 24))
        self.check_box_bbox.setMaximumSize(QSize(16777215, 24))
        if CONFIG.OPTION['plot font bbox']:
            self.check_box_bbox.setChecked(True)
        else:
            self.check_box_bbox.setChecked(False)
        self.hlayout_bbox.addWidget(self.check_box_bbox)
        self.verticalLayout_6.addLayout(self.hlayout_bbox)
        
        self.verticalLayout_3.addWidget(self.group_box_text)
        self.group_box_line = QGroupBox(self.page_plot)
        self.verticalLayout_7 = QVBoxLayout(self.group_box_line)
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_7.setSpacing(2)
        self.horizontalLayout_7 = QHBoxLayout()
        self.label_ls = QLabel(self.group_box_line)
        self.label_ls.setMinimumSize(QSize(100, 24))
        self.label_ls.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_7.addWidget(self.label_ls)
        self.cb_ls = QComboBox(self.group_box_line)
        self.cb_ls.setMinimumSize(QSize(0, 24))
        self.cb_ls.setMaximumSize(QSize(16777215, 24))  
        enum_linestyle = ['None','-', '--', '-.', ':']
        count = len(enum_linestyle)
        for i in range(count):
            self.cb_ls.addItem('')
            self.cb_ls.setItemData(i, enum_linestyle[i], Qt.UserRole)
        index = enum_linestyle.index(CONFIG.OPTION['plot markline style'])
        self.cb_ls.setCurrentIndex(index)
        
        self.horizontalLayout_7.addWidget(self.cb_ls)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
#        self.horizontalLayout_8 = QHBoxLayout()
#        self.label_lw = QLabel(self.group_box_line)
#        self.label_lw.setMinimumSize(QSize(100, 24))
#        self.label_lw.setMaximumSize(QSize(100, 24))
#        self.horizontalLayout_8.addWidget(self.label_lw)
#        self.spin_box_lw = QSpinBox(self.group_box_line)
#        self.spin_box_lw.setMinimumSize(QSize(0, 24))
#        self.spin_box_lw.setMaximumSize(QSize(16777215, 24))
#        self.horizontalLayout_8.addWidget(self.spin_box_lw)
#        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QHBoxLayout()
        self.label_lc = QLabel(self.group_box_line)
        self.label_lc.setMinimumSize(QSize(100, 24))
        self.label_lc.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_9.addWidget(self.label_lc)
        self.label_lc_view = QLabel(self.group_box_line)
        self.label_lc_view.setMinimumSize(QSize(0, 24))
        self.label_lc_view.setMaximumSize(QSize(16777215, 24))
        self.label_lc_view.setPalette(QPalette(QColor(self.line_color)))
        self.label_lc_view.setAutoFillBackground(True)
        self.horizontalLayout_9.addWidget(self.label_lc_view)
        self.btn_sel_lc = QToolButton(self.group_box_line)
        self.btn_sel_lc.setMinimumSize(QSize(24, 24))
        self.btn_sel_lc.setMaximumSize(QSize(24, 24))
        self.horizontalLayout_9.addWidget(self.btn_sel_lc)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QHBoxLayout()
        self.label_lm = QLabel(self.group_box_line)
        self.label_lm.setMinimumSize(QSize(100, 24))
        self.label_lm.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_10.addWidget(self.label_lm)
        self.cb_lm = QComboBox(self.group_box_line)
        self.cb_lm.setMinimumSize(QSize(0, 24))
        self.cb_lm.setMaximumSize(QSize(16777215, 24))
        enum_marker = ['None', '.', 'o', 'v', '^', '<', '>', '1', '2',
                            '3', '4', 's', '*', '+', 'x', 'D']
        count = len(enum_marker)
        for i in range(count):
            self.cb_lm.addItem('')
            self.cb_lm.setItemData(i, enum_marker[i], Qt.UserRole)
        index = enum_marker.index(CONFIG.OPTION['plot markline marker'])
        self.cb_lm.setCurrentIndex(index)
        self.horizontalLayout_10.addWidget(self.cb_lm)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.verticalLayout_3.addWidget(self.group_box_line)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.stack_option_win.addWidget(self.page_plot)
        
        self.page_data_dict = QWidget()
        self.verticalLayout_5 = QVBoxLayout(self.page_data_dict)
        self.verticalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_5.setSpacing(2)
        self.groupBox = QGroupBox(self.page_data_dict)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(4)
        self.horizontalLayout_3 = QHBoxLayout()
        self.cb_paralist_win = QCheckBox(self.groupBox)
        self.cb_paralist_win.setMinimumSize(QSize(110, 24))
        self.cb_paralist_win.setMaximumSize(QSize(110, 24))
        self.horizontalLayout_3.addWidget(self.cb_paralist_win)
        self.com_box_style = QComboBox(self.groupBox)
        self.com_box_style.setMinimumSize(QSize(150, 24))
        self.com_box_style.setMaximumSize(QSize(150, 24))
        self.com_box_style.addItem('')
        self.com_box_style.addItem('')
        self.com_box_style.addItem('')
        self.com_box_style.setCurrentIndex(CONFIG.OPTION['data dict scope style'])
        self.horizontalLayout_3.addWidget(self.com_box_style)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.cb_plot_win = QCheckBox(self.groupBox)
        self.cb_plot_win.setMinimumSize(QSize(0, 24))
        self.cb_plot_win.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout_4.addWidget(self.cb_plot_win)
        self.verticalLayout_5.addWidget(self.groupBox)
        
        self.gb_data_dict_version = QGroupBox(self.page_data_dict)
        self.verticalLayout_8 = QVBoxLayout(self.gb_data_dict_version)
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_8.setSpacing(2)
        self.horizontalLayout_11 = QHBoxLayout()
        self.cb_dd_version = QComboBox(self.gb_data_dict_version)
        self.cb_dd_version.setMinimumSize(QSize(150, 24))
        self.cb_dd_version.setMaximumSize(QSize(150, 24))
        enum_dd_version = ['custom.json', '102test.json']
        for i, name in enumerate(enum_dd_version):
            self.cb_dd_version.addItem('')
            self.cb_dd_version.setItemData(i, name, Qt.UserRole)
        index = enum_dd_version.index(CONFIG.OPTION['data dict version'])
        self.cb_dd_version.setCurrentIndex(index)
        
        self.horizontalLayout_11.addWidget(self.cb_dd_version)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.verticalLayout_5.addWidget(self.gb_data_dict_version)
        
        spacerItem = QSpacerItem(20, 269, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.stack_option_win.addWidget(self.page_data_dict)
        self.horizontalLayout_2.addWidget(self.stack_option_win)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.btn_reset = QPushButton(self)
        self.btn_reset.setFocusPolicy(Qt.NoFocus)
        self.btn_reset.setMinimumSize(QSize(0, 24))
        self.btn_reset.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_reset)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_ok = QPushButton(self)
        self.btn_ok.setMinimumSize(QSize(0, 24))
        self.btn_ok.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_ok)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.btn_cancel)
#        self.btn_apply = QPushButton(self)
#        self.btn_apply.setMinimumSize(QSize(0, 24))
#        self.btn_apply.setMaximumSize(QSize(16777215, 24))
#        self.horizontalLayout.addWidget(self.btn_apply)
        self.verticalLayout.addLayout(self.horizontalLayout)

        if CONFIG.OPTION['data dict scope paralist']:
            self.cb_paralist_win.setChecked(True)
            self.com_box_style.setEnabled(True)
        else:
            self.cb_paralist_win.setChecked(False)
            self.com_box_style.setEnabled(False)
        if CONFIG.OPTION['data dict scope plot']:
            self.cb_plot_win.setChecked(True)
        else:
            self.cb_plot_win.setChecked(False)
        self.list_option.setCurrentRow(0)
        self.stack_option_win.setCurrentIndex(0)    

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_reset.clicked.connect(self.reset)
        self.list_option.currentRowChanged.connect(self.slot_option_win_change)
        self.cb_paralist_win.stateChanged.connect(self.slot_pw_check_change)
        
#        通用设置页
        self.btn_sel_work_dir.clicked.connect(self.slot_sel_work_dir)
#        绘图设置页
        self.btn_sel_color.clicked.connect(self.slot_sel_font_color)
        self.btn_sel_lc.clicked.connect(self.slot_sel_lc)
        
        self.retranslateUi()
        
    def accept(self):
        
        if self.cb_paralist_win.isChecked():
            CONFIG.OPTION['data dict scope paralist'] = True
            CONFIG.OPTION['data dict scope style'] = self.com_box_style.currentIndex()
        else:
            CONFIG.OPTION['data dict scope paralist'] = False
        if self.cb_plot_win.isChecked():
            CONFIG.OPTION['data dict scope plot'] = True
        else:
            CONFIG.OPTION['data dict scope plot'] = False
        CONFIG.OPTION['work dir'] = self.line_edit_work_dir.text()
        CONFIG.OPTION['plot fontsize'] = self.spinBox.value()
        CONFIG.OPTION['plot fontcolor'] = self.font_color
        CONFIG.OPTION['plot font arrow'] = self.check_box_arrow.isChecked()
        CONFIG.OPTION['plot font bbox'] = self.check_box_bbox.isChecked()
        CONFIG.OPTION['plot markline style'] = self.cb_ls.currentData()
        CONFIG.OPTION['plot markline color'] = self.line_color
        CONFIG.OPTION['plot markline marker'] = self.cb_lm.currentData()
        if CONFIG.OPTION['data dict version'] != self.cb_dd_version.currentData():
            CONFIG.OPTION['data dict version'] = self.cb_dd_version.currentData()
            self.dd_version_changed = True
        
        
        try:
    #        打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(CONFIG.SETUP_DIR + r'\data\configuration.json', 'w') as file:
                json.dump(CONFIG.OPTION, file)
        except IOError:
            QMessageBox.information(self,
                                    QCoreApplication.translate('OptionDialog', '软件配置提示'),
                                    QCoreApplication.translate('OptionDialog', '无法保存软件配置！'))
        
        QDialog.accept(self)
        
    def reset(self):
        
        index = self.stack_option_win.currentIndex()
        if index == 0:
            self.line_edit_work_dir.setText(CONFIG.SETUP_DIR)
        if index == 1:
            self.spinBox.setValue(8)
            self.font_color = '#aa0000'
            self.label_color.setPalette(QPalette(QColor(self.font_color)))
            self.check_box_arrow.setChecked(False)
            self.check_box_bbox.setChecked(True)
            self.cb_ls.setCurrentIndex(2)
            self.line_color = '#aa0000'
            self.label_lc_view.setPalette(QPalette(QColor(self.line_color)))
            self.cb_lm.setCurrentIndex(0)
        if index == 2:
            self.cb_paralist_win.setChecked(True)
            self.cb_plot_win.setChecked(True)
            self.com_box_style.setCurrentIndex(1) 
#            self.cb_dd_version.setCurrentIndex(1)
    
    def slot_option_win_change(self, cur_row):
        
        self.stack_option_win.setCurrentIndex(cur_row)
        
    def slot_pw_check_change(self):
        
        if self.cb_paralist_win.isChecked():
            self.com_box_style.setEnabled(True)
        else:
            self.com_box_style.setEnabled(False)
            
    def slot_sel_work_dir(self):
        
        filedir = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('OptionDialog', '设置工作路径'),
                                                   CONFIG.OPTION['work dir'])
        if filedir:
            filedir = filedir.replace('/','\\')
            self.line_edit_work_dir.setText(filedir)
            
    def slot_sel_font_color(self):
        
        color = QColorDialog.getColor(QColor(self.font_color), self, 'Select Color')
        self.label_color.setPalette(QPalette(color))
#        按##RRGGBB的格式赋值颜色
        self.font_color = color.name()
    
    def slot_sel_lc(self):
        
        color = QColorDialog.getColor(QColor(self.line_color), self, 'Select Color')
        self.label_lc_view.setPalette(QPalette(color))
#        按##RRGGBB的格式赋值颜色
        self.line_color = color.name()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('OptionDialog', '软件设置'))
        __sortingEnabled = self.list_option.isSortingEnabled()
        self.list_option.setSortingEnabled(False)
        item = self.list_option.item(0)
        item.setText(_translate('OptionDialog', '通用'))
        item = self.list_option.item(1)
        item.setText(_translate('OptionDialog', '绘图'))
        item = self.list_option.item(2)
        item.setText(_translate('OptionDialog', '数据字典'))
        self.list_option.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate('OptionDialog', '作用范围'))
        self.cb_paralist_win.setText(_translate('OptionDialog', '参数列表'))
        self.com_box_style.setItemText(0, _translate('OptionDialog', '参数名'))
        self.com_box_style.setItemText(1, _translate('OptionDialog', '标识符(参数名)'))
        self.com_box_style.setItemText(2, _translate('OptionDialog', '参数名(标识符)'))
        self.cb_plot_win.setText(_translate('OptionDialog', '绘图'))
        self.btn_reset.setText(_translate('OptionDialog', '默认设置'))
        self.btn_ok.setText(_translate('OptionDialog', '确认'))
        self.btn_cancel.setText(_translate('OptionDialog', '取消'))
#        self.btn_apply.setText(_translate('OptionDialog', '应用'))
        self.groupBox_2.setTitle(_translate('OptionDialog', '工作路径'))
        self.btn_sel_work_dir.setText(_translate('OptionDialog', '...'))
        self.group_box_text.setTitle(_translate('OptionDialog', '文字标注'))
        self.label_fontszie.setText(_translate('OptionDialog', '字体大小'))
        self.label_fontcolor.setText(_translate('OptionDialog', '字体颜色'))
        self.label_arrow.setText(_translate('OptionDialog', '箭头'))
        self.label_bbox.setText(_translate('OptionDialog', '边框'))
        self.label_color.setText(_translate('OptionDialog', ''))
        self.btn_sel_color.setText(_translate('OptionDialog', 'C'))
        self.group_box_line.setTitle(_translate('OptionDialog', '标注线'))
        self.label_ls.setText(_translate('OptionDialog', '线型'))
#        self.label_lw.setText(_translate('OptionDialog', '线宽'))
        self.label_lc.setText(_translate('OptionDialog', '颜色'))
        self.label_lc_view.setText(_translate('OptionDialog', ''))
        self.btn_sel_lc.setText(_translate('OptionDialog', 'C'))
        self.label_lm.setText(_translate('OptionDialog', '标记'))
        self.gb_data_dict_version.setTitle(_translate('Dialog', '字典版本'))
        
        enum_dd_version_name = ['自定义', '102实时预处理任务书']
        for i, name in enumerate(enum_dd_version_name):
            self.cb_dd_version.setItemText(i, _translate('OptionDialog', name))
        
        enum_linestyle_name = ['Nothing', 'Solid', 'Dashed', 
                                    'Dashdot', 'Dotted']
        count = len(enum_linestyle_name)
        for i in range(count):
            self.cb_ls.setItemText(i, _translate('OptionDialog',
                                                 enum_linestyle_name[i]))
        enum_marker_name = ['Nothing', 'Point', 'Circle', 'Triangle_down',
                                 'Triangle_up', 'Triangle_left', 'Triangle_right',
                                 'Tri_down', 'Tri_up', 'Tri_left', 'Tri_right', 
                                 'Square', 'Star', 'Plus', 'x', 'Diamond']
        count = len(enum_marker_name)
        for i in range(count):
            self.cb_lm.setItemText(i, _translate('OptionDialog',
                                                 enum_marker_name[i]))

class DsiplayParaInfoBaseDialog(QDialog):
    
    def __init__(self, parent = None, cols : int = 0, cols_info : list = []):
    
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(250, 480)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(2)
        self.group_box_tip = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_tip)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.label_tip = QLabel(self.group_box_tip)
        self.label_tip.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_tip.setMinimumSize(QSize(0, 24))
        self.label_tip.setMaximumSize(QSize(16777215, 24))
        self.verticalLayout.addWidget(self.label_tip)
        self.verticalLayout_3.addWidget(self.group_box_tip)
        self.group_box_para_info = QGroupBox(self)
        self.verticalLayout_2 = QVBoxLayout(self.group_box_para_info)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.table_widget_para_info = QTableWidget(self.group_box_para_info)
        self.table_widget_para_info.setColumnCount(cols)
        self.table_widget_para_info.setRowCount(0)
        for i in range(cols):
            item = QTableWidgetItem()
            self.table_widget_para_info.setHorizontalHeaderItem(i, item)
        self.table_widget_para_info.horizontalHeader().setDefaultSectionSize(119)
        self.table_widget_para_info.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table_widget_para_info.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.table_widget_para_info)
        self.verticalLayout_3.addWidget(self.group_box_para_info)

        self.retranslateUi(cols_info)

    def retranslateUi(self, cols_info):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('DsiplayParaInfoBaseDialog', '标题'))
        self.group_box_tip.setTitle(_translate('DsiplayParaInfoBaseDialog', '提示信息'))
        self.label_tip.setText(_translate('DsiplayParaInfoBaseDialog', '提示信息'))
        self.group_box_para_info.setTitle(_translate('DsiplayParaInfoBaseDialog', '参数信息'))
        for i, info in enumerate(cols_info):
            item = self.table_widget_para_info.horizontalHeaderItem(i)
            item.setText(_translate('DisplayParaValuesDialog', info))

class DisplayParaValuesDialog(DsiplayParaInfoBaseDialog):
    
    def __init__(self, parent = None):
    
        super().__init__(parent, 2, ['参数名', '参数值'])

        self.retranslateUi_custom()

#    实时显示参数值
    def slot_display_paravalue(self, time : str, list_paravalue_info : list):
        
#        显示时间
        if time != '':
            self.label_tip.setText(time)
        else:
            self.label_tip.setText('No Data!')
        
        count = len(list_paravalue_info)
        self.table_widget_para_info.clearContents()
        self.table_widget_para_info.setRowCount(count)
        for row, para_tuple in enumerate(list_paravalue_info):
            time, paraname, value = para_tuple
            item1 = QTableWidgetItem(paraname)
            self.table_widget_para_info.setItem(row, 0, item1)
            item2 = QTableWidgetItem(str(value))
            self.table_widget_para_info.setItem(row, 1, item2)

    def retranslateUi_custom(self):
        
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('DisplayParaValuesDialog', '参数值'))
        self.group_box_tip.setTitle(_translate('DisplayParaValuesDialog', '时刻'))
        self.label_tip.setText(_translate('DisplayParaValuesDialog', '00:00:00.000'))
        self.group_box_para_info.setTitle(_translate('DisplayParaValuesDialog', '参数信息'))
        
class DisplayParaAggregateInfoDialog(DsiplayParaInfoBaseDialog):

    def __init__(self, parent = None):
    
        super().__init__(parent, 4, ['参数名', '平均值', '最大值', '最小值'])

        self.resize(488, 480)

        self.retranslateUi_custom()
        
    def display_para_agg_info(self, time_info : tuple, para_info_list : list):
        
#        显示时间
        if time_info != '':
            self.label_tip.setText(time_info[0] + ' - ' + time_info[1])
        else:
            self.label_tip.setText('No Data!')
        
        count = len(para_info_list)
        self.table_widget_para_info.clearContents()
        self.table_widget_para_info.setRowCount(count)
        for row, para_tuple in enumerate(para_info_list):
            paraname, mean_, max_, min_ = para_tuple
            item1 = QTableWidgetItem(paraname)
            self.table_widget_para_info.setItem(row, 0, item1)
            item2 = QTableWidgetItem(str(mean_))
            self.table_widget_para_info.setItem(row, 1, item2)
            item3 = QTableWidgetItem(str(max_))
            self.table_widget_para_info.setItem(row, 2, item3)
            item4 = QTableWidgetItem(str(min_))
            self.table_widget_para_info.setItem(row, 3, item4)
        
    def retranslateUi_custom(self):
        
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('DisplayParaAggregateInfoDialog', '数据聚合'))
        self.group_box_tip.setTitle(_translate('DisplayParaAggregateInfoDialog', '时间段'))
        self.label_tip.setText(_translate('DisplayParaAggregateInfoDialog', '00:00:00.000 - 00:00:00.000'))
        self.group_box_para_info.setTitle(_translate('DisplayParaAggregateInfoDialog', '参数信息'))
        
class ImportDataFileDialog(QDialog):
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
#        数据文件路径
        self.datafile_dir = ''
#        数据类型，普通试飞数据、GPS数据、QAR数据、自定义数据
        self.datafile_type = ''
#        导入起始行 - 1
        self.skiprows = 0
#        时间列为0时表示无时间
        self.timecol = 0
#        分隔符
        self.sep = ''
#        时间格式
        self.time_format = ''
        self.setup()
        
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(450, 220)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setSpacing(4)
        self.gb_sel_file = QGroupBox(self)
        self.horizontalLayout = QHBoxLayout(self.gb_sel_file)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.line_edit_file_dir = QLineEdit(self.gb_sel_file)
        self.line_edit_file_dir.setReadOnly(True)
        self.line_edit_file_dir.setMinimumSize(QSize(0, 24))
        self.line_edit_file_dir.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_file_dir)
        self.btn_sel_file = QPushButton(self.gb_sel_file)
        self.btn_sel_file.setMinimumSize(QSize(24, 24))
        self.btn_sel_file.setMaximumSize(QSize(24, 24))
        self.horizontalLayout.addWidget(self.btn_sel_file)
        self.verticalLayout_3.addWidget(self.gb_sel_file)
        self.gb_data_type = QGroupBox(self)
        self.horizontalLayout_2 = QHBoxLayout(self.gb_data_type)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.cb_data_type = QComboBox(self.gb_data_type)
        self.cb_data_type.setMinimumSize(QSize(200, 24))
        self.cb_data_type.setMaximumSize(QSize(200, 24))
#        普通试飞数据
        self.cb_data_type.addItem('', 'normal datafile')
#        GPS数据
        self.cb_data_type.addItem('', 'GPS datafile')
#        QAR数据
        self.cb_data_type.addItem('', 'QAR datafile')
#        自定义数据
        self.cb_data_type.addItem('', 'custom datafile')
        self.horizontalLayout_2.addWidget(self.cb_data_type)
        spacerItem = QSpacerItem(231, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.gb_data_type)
        self.gb_import_datafile = QGroupBox(self)
        self.horizontalLayout_7 = QHBoxLayout(self.gb_import_datafile)
        self.horizontalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.frame_left = QFrame(self.gb_import_datafile)
        self.frame_left.setFrameShape(QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_left)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_first_line_num = QLabel(self.frame_left)
        self.label_first_line_num.setMinimumSize(QSize(140, 24))
        self.label_first_line_num.setMaximumSize(QSize(140, 24))
        self.horizontalLayout_4.addWidget(self.label_first_line_num)
        self.spb_first_line_num = QSpinBox(self.frame_left)
        self.spb_first_line_num.setMinimum(1)
        self.spb_first_line_num.setMinimumSize(QSize(60, 24))
        self.spb_first_line_num.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_4.addWidget(self.spb_first_line_num)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QHBoxLayout()
        self.label_time_col = QLabel(self.frame_left)
        self.label_time_col.setMinimumSize(QSize(140, 24))
        self.label_time_col.setMaximumSize(QSize(140, 24))
        self.horizontalLayout_6.addWidget(self.label_time_col)
        self.spb_time_col = QSpinBox(self.frame_left)
        self.spb_time_col.setValue(1)
        self.spb_time_col.setMinimumSize(QSize(60, 24))
        self.spb_time_col.setMaximumSize(QSize(60, 24))
        self.horizontalLayout_6.addWidget(self.spb_time_col)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addWidget(self.frame_left)
        self.frame_left_2 = QFrame(self.gb_import_datafile)
        self.frame_left_2.setFrameShape(QFrame.StyledPanel)
        self.frame_left_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_left_2)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.horizontalLayout_8 = QHBoxLayout()
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.label_sep = QLabel(self.frame_left_2)
        self.label_sep.setMinimumSize(QSize(80, 24))
        self.label_sep.setMaximumSize(QSize(80, 24))
        self.horizontalLayout_8.addWidget(self.label_sep)
        self.cb_sep = QComboBox(self.frame_left_2)
        self.cb_sep.setMinimumSize(QSize(120, 24))
        self.cb_sep.setMaximumSize(QSize(120, 24))
#        tab键分隔
        self.cb_sep.addItem('', r'\t')
#        分号分隔
        self.cb_sep.addItem('', ';')
#        逗号分隔
        self.cb_sep.addItem('', ',')
#        空格分隔
        self.cb_sep.addItem('', r'\s+')
        self.horizontalLayout_8.addWidget(self.cb_sep)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QHBoxLayout()
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.label_time_format = QLabel(self.frame_left_2)
        self.label_time_format.setMinimumSize(QSize(80, 24))
        self.label_time_format.setMaximumSize(QSize(80, 24))
        self.horizontalLayout_9.addWidget(self.label_time_format)
        self.cb_time_format = QComboBox(self.frame_left_2)
        self.cb_time_format.setMinimumSize(QSize(120, 24))
        self.cb_time_format.setMaximumSize(QSize(120, 24))
        self.cb_time_format.addItem('')
        self.cb_time_format.addItem('')
        self.cb_time_format.addItem('')
        self.cb_time_format.addItem('')
        self.cb_time_format.addItem('')
        self.cb_time_format.addItem('')
        self.cb_time_format.addItem('')
        self.horizontalLayout_9.addWidget(self.cb_time_format)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_7.addWidget(self.frame_left_2)
        self.verticalLayout_3.addWidget(self.gb_import_datafile)
        spacerItem5 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.horizontalLayout_3 = QHBoxLayout()
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_3.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_3.addWidget(self.btn_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        
        
        self.gb_import_datafile.setEnabled(False)
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_sel_file.clicked.connect(self.slot_sel_datafile)
        self.cb_data_type.currentIndexChanged.connect(self.slot_data_type_change)

        self.retranslateUi()
        
    def accept(self):
        
        self.datafile_dir = self.line_edit_file_dir.text()
        self.datafile_type = self.cb_data_type.currentData()
#        自定义数据
        if self.cb_data_type.currentIndex() == 3:
            self.skiprows = self.spb_first_line_num.value() - 1
            self.timecol = self.spb_time_col.value()
            self.time_format = self.cb_time_format.currentText()
            self.sep = self.cb_sep.currentData()
        QDialog.accept(self)
        
#    让用户选择项目的路径
    def slot_sel_datafile(self):
        
        if CONFIG.OPTION['dir of custom import']:
            sel_dir = CONFIG.OPTION['dir of custom import']
        else:
            sel_dir = CONFIG.SETUP_DIR
        filename, temp = QFileDialog.getOpenFileName(self, QCoreApplication.translate('ImportDataFileDialog', '选择文件'),
                                                     sel_dir,
                                                     QCoreApplication.translate('ImportDataFileDialog', '数据文件(*.*)'))
        if filename:
            CONFIG.OPTION['dir of custom import'] = os.path.dirname(filename)
            self.line_edit_file_dir.setText(filename)
            
    def slot_data_type_change(self, index):
        
        if index == 3:
            self.gb_import_datafile.setEnabled(True)
        else:
            self.gb_import_datafile.setEnabled(False)

    def retranslateUi(self):
        
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('ImportDataFileDialog', '数据导入'))
        self.gb_sel_file.setTitle(_translate('ImportDataFileDialog', '选择文件'))
        self.btn_sel_file.setText(_translate('ImportDataFileDialog', '...'))
        self.gb_data_type.setTitle(_translate('ImportDataFileDialog', '数据类型'))
        self.cb_data_type.setItemText(0, _translate('ImportDataFileDialog', '普通试飞数据'))
        self.cb_data_type.setItemText(1, _translate('ImportDataFileDialog', 'GPS数据'))
        self.cb_data_type.setItemText(2, _translate('ImportDataFileDialog', 'QAR数据'))
        self.cb_data_type.setItemText(3, _translate('ImportDataFileDialog', '自定义数据'))
        self.gb_import_datafile.setTitle(_translate('ImportDataFileDialog', '文件读取方式'))
        self.label_first_line_num.setText(_translate('ImportDataFileDialog', '导入起始行'))
        self.label_time_col.setText(_translate('ImportDataFileDialog', '时间列（0表示无时间列）'))
        self.label_sep.setText(_translate('ImportDataFileDialog', '分隔符'))
        self.cb_sep.setItemText(0, _translate('ImportDataFileDialog', 'Tab键'))
        self.cb_sep.setItemText(1, _translate('ImportDataFileDialog', '分号'))
        self.cb_sep.setItemText(2, _translate('ImportDataFileDialog', '逗号'))
        self.cb_sep.setItemText(3, _translate('ImportDataFileDialog', '空格'))
        self.label_time_format.setText(_translate('ImportDataFileDialog', '时间格式'))
        self.cb_time_format.setItemText(0, _translate('ImportDataFileDialog', '%H:%M:%S:%f'))
        self.cb_time_format.setItemText(1, _translate('ImportDataFileDialog', '%H:%M:%S.%f'))
        self.cb_time_format.setItemText(2, _translate('ImportDataFileDialog', '%H:%M:%S'))
        self.cb_time_format.setItemText(3, _translate('ImportDataFileDialog', '%H-%M-%S.%f'))
        self.cb_time_format.setItemText(4, _translate('ImportDataFileDialog', '%H-%M-%S-%f'))
        self.cb_time_format.setItemText(5, _translate('ImportDataFileDialog', '%H-%M-%S'))
        self.cb_time_format.setItemText(6, _translate('ImportDataFileDialog', '推断'))
        self.btn_confirm.setText(_translate('ImportDataFileDialog', '导入'))
        self.btn_cancel.setText(_translate('ImportDataFileDialog', '取消'))
        
#测试用     
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    d = DisplayParaValuesDialog()
    d.show()
    app.exec_()