# -*- coding: utf-8 -*-

from matplotlib.lines import Line2D
from matplotlib.text import Annotation
from matplotlib.axes import Axes
import matplotlib.colors as Color
import matplotlib.dates as mdates
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QSize, QCoreApplication, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QPushButton, QMessageBox, QListWidget,
                             QListWidgetItem, QToolButton, QFrame, 
                             QAbstractItemView, QApplication, QComboBox,
                             QColorDialog, QGroupBox, QTreeWidget,
                             QTreeWidgetItem, QHeaderView, QFileDialog,
                             QAction, QMenu)

# =============================================================================
# Package models imports
# =============================================================================
from models.datafile_model import DataFile, Normal_DataFile
import views.constant as CONSTANT
import models.time_model as Time_Model
from models.data_model import DataFactory
from models.analysis_model import DataAnalysis

import os, sys, re
import pandas as pd

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
        self.verticalLayout.setObjectName('verticalLayout')
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.label = QLabel(self)
        self.label.setMinimumSize(QSize(0, 24))
        self.label.setMaximumSize(QSize(16777215, 24))
        self.label.setObjectName('label')
        self.horizontalLayout.addWidget(self.label)
        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMinimumSize(QSize(0, 24))
        self.line_edit_name.setMaximumSize(QSize(16777215, 24))
        self.line_edit_name.setObjectName('line_edit_name')
        self.horizontalLayout.addWidget(self.line_edit_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setObjectName('button_confirm')
        self.horizontalLayout_2.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
        self.button_cancel.setObjectName('button_cancle')
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


class SelectTemplateDialog(QDialog):
    
    def __init__(self, parent = None, templates = {}):
        
        super().__init__(parent)
        self.templates = templates
        self.sel_temp = ''
        self.tempicon = QIcon(CONSTANT.ICON_TEMPLATE)
        self.paraicon = QIcon(CONSTANT.ICON_PARA)
        self.setup()
    
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(560, 450)
        self.verticalLayout_3 = QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(4, 0, 4, 4)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.label_temp = QLabel(self)
        self.label_temp.setMinimumSize(QSize(0, 24))
        self.label_temp.setMaximumSize(QSize(16777215, 24))
        self.label_temp.setObjectName('label_temp')
        self.verticalLayout.addWidget(self.label_temp)
        self.list_temps = QListWidget(self)
        self.list_temps.setObjectName('list_temps')
        self.verticalLayout.addWidget(self.list_temps)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.label_para = QLabel(self)
        self.label_para.setMinimumSize(QSize(0, 24))
        self.label_para.setMaximumSize(QSize(16777215, 24))
        self.label_para.setObjectName('label_para')
        self.verticalLayout_2.addWidget(self.label_para)
        self.list_paras = QListWidget(self)
        self.list_paras.setObjectName('list_paras')
        self.verticalLayout_2.addWidget(self.list_paras)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName('horizontalLayout')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_confirm = QPushButton(self)
        self.button_confirm.setObjectName('button_confirm')
        self.horizontalLayout.addWidget(self.button_confirm)
        self.button_cancel = QPushButton(self)
        self.button_cancel.setObjectName('button_cancel')
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
        self.setWindowTitle(_translate('SelectTemplateself', '选择模板'))
        self.label_temp.setText(_translate('SelectTemplateself', '模板列表'))
        self.label_para.setText(_translate('SelectTemplateself', '参数列表'))
        self.button_confirm.setText(_translate('SelectTemplateself', '确定'))
        self.button_cancel.setText(_translate('SelectTemplateself', '取消'))

class SelParasDialog(QDialog):

    signal_add_paras = pyqtSignal()
    
    def __init__(self, parent = None, files = [], sel_mode = 0):
        
        super().__init__(parent)
        self.paraicon = QIcon(CONSTANT.ICON_PARA)
        if sel_mode == 0:
            self.sel_mode = QAbstractItemView.SingleSelection
        if sel_mode == 1:
            self.sel_mode = QAbstractItemView.ExtendedSelection
        self.setup()
        self.display_paras(files)

    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(260, 550)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout')
        self.line_edit_search = QLineEdit(self)
        self.line_edit_search.setMinimumSize(QSize(0, 24))
        self.line_edit_search.setMaximumSize(QSize(16777215, 24))
        self.line_edit_search.setObjectName('line_edit_search')
        self.verticalLayout.addWidget(self.line_edit_search)
        self.list_paras = QListWidget(self)
        self.list_paras.setSelectionMode(self.sel_mode)
        self.list_paras.setObjectName('list_paras')
        self.verticalLayout.addWidget(self.list_paras)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName('horizontalLayout')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.btn_confirm.setObjectName('btn_confirm')
        self.horizontalLayout.addWidget(self.btn_confirm)
        if self.sel_mode == QAbstractItemView.ExtendedSelection:
            self.btn_add = QPushButton(self)
            self.btn_add.setMinimumSize(QSize(0, 24))
            self.btn_add.setMaximumSize(QSize(16777215, 24))
            self.btn_add.setObjectName('btn_add')
            self.horizontalLayout.addWidget(self.btn_add)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.btn_cancel.setObjectName('btn_cancel')
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
        
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        if self.sel_mode == QAbstractItemView.ExtendedSelection:
            self.btn_add.clicked.connect(self.signal_add_paras)
        if self.sel_mode == QAbstractItemView.SingleSelection:
            self.list_paras.itemDoubleClicked.connect(self.accept)
        self.line_edit_search.textChanged.connect(self.slot_search_para)
    
    def slot_search_para(self, para_name):
        
        if self.list_paras:
            pattern = re.compile('.*' + para_name + '.*')
            count = self.list_paras.count()
            for i in range(count):
                item = self.list_paras.item(i)
                paraname = item.text()
                if re.match(pattern, paraname):
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def get_list_sel_paras(self):
        
        list_paras = []
        for item in self.list_paras.selectedItems():
            list_paras.append(item.text())
        return list_paras
        
#    不显示时间
    def display_paras(self, files):
        
        for file_dir in files:
            time_hide = False
            file = Normal_DataFile(file_dir)
            paras = file.paras_in_file
            for para in paras:
                if time_hide:
                    if para not in self.get_list_paras():
                        item = QListWidgetItem(para, self.list_paras)
                        item.setIcon(self.paraicon)
#                跳过第一个参数，这里默认第一个参数时间
                else:
                    time_hide = True
    
    def get_list_paras(self):
        
        list_paras = []
        count = self.list_paras.count()
        for i in range(count):
            item = self.list_paras.item(i)
            list_paras.append(item.text())
        return list_paras

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('SelParasDialog', '选择参数'))
        self.line_edit_search.setPlaceholderText(_translate('SelParasDialog', '过滤器'))
        self.btn_confirm.setText(_translate('SelParasDialog', '确定'))
        if self.sel_mode == QAbstractItemView.ExtendedSelection:
            self.btn_add.setText(_translate('SelParasDialog', '添加'))
        self.btn_cancel.setText(_translate('SelParasDialog', '取消'))

class LineSettingDialog(QDialog):

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
        self.setup()
    
    def setup(self):

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)        
        self.resize(320, 290)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName('verticalLayout')
        self.label_title = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
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
        self.line.setObjectName('line')
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
            istime = False
#            转换成功不一定就能判断这个是时间
            try:
#                将浮点值转换为时间，由于经过转换，有误差
                time = mdates.num2date(self.line_xdata[0]).time().isoformat(timespec='milliseconds')
                istime = True
            except:
                pass
            if istime:
                self.line_edit_line_x0.setText(str(time))
            else:
                self.line_edit_line_x0.setText(str(self.line_xdata[0]))
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
            istime = False
#            转换成功不一定就能判断这个是时间
            try:
#                将浮点值转换为时间，由于经过转换，有误差
                stime = mdates.num2date(self.line_xdata[0]).time().isoformat(timespec='milliseconds')
                etime = mdates.num2date(self.line_xdata[1]).time().isoformat(timespec='milliseconds')
                istime = True
            except:
                pass
            if istime:
                self.line_edit_line_x0.setText(str(stime))
                self.line_edit_line_x1.setText(str(etime))
            else:
                self.line_edit_line_x0.setText(str(self.line_xdata[0]))
                self.line_edit_line_x1.setText(str(self.line_xdata[1]))
            self.line_edit_line_y0.setText(str(self.line_ydata[0]))
            self.line_edit_line_y1.setText(str(self.line_ydata[1]))

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.label_line_ls = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_line_ls.sizePolicy().hasHeightForWidth())
        self.label_line_ls.setSizePolicy(sizePolicy)
        self.label_line_ls.setMinimumSize(QSize(75, 24))
        self.label_line_ls.setMaximumSize(QSize(75, 24))
        self.label_line_ls.setObjectName('label_line_ls')
        self.horizontalLayout_2.addWidget(self.label_line_ls)
        self.combo_box_linestyle = QComboBox(self)
        self.combo_box_linestyle.setMinimumSize(QSize(120, 24))
        self.combo_box_linestyle.setMaximumSize(QSize(16777215, 24))
        self.combo_box_linestyle.setObjectName('combo_box_linestyle')
        
        count = len(self.enum_linestyle)
        for i in range(count):
            self.combo_box_linestyle.addItem('')
            self.combo_box_linestyle.setItemData(i, self.enum_linestyle[i], Qt.UserRole)
        index = self.enum_linestyle.index(self.line_ls)
        self.combo_box_linestyle.setCurrentIndex(index)
        
        self.horizontalLayout_2.addWidget(self.combo_box_linestyle)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.label_line_lw = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_line_lw.sizePolicy().hasHeightForWidth())
        self.label_line_lw.setSizePolicy(sizePolicy)
        self.label_line_lw.setMinimumSize(QSize(75, 24))
        self.label_line_lw.setMaximumSize(QSize(75, 24))
        self.label_line_lw.setObjectName('label_line_lw')
        self.horizontalLayout_3.addWidget(self.label_line_lw)
        self.line_edit_line_width = QLineEdit(self)
        self.line_edit_line_width.setMinimumSize(QSize(120, 24))
        self.line_edit_line_width.setMaximumSize(QSize(16777215, 24))
        self.line_edit_line_width.setObjectName('line_edit_line_width')
        self.line_edit_line_width.setText(str(self.line_lw))
        self.horizontalLayout_3.addWidget(self.line_edit_line_width)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.label_line_lc = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_line_lc.sizePolicy().hasHeightForWidth())
        self.label_line_lc.setSizePolicy(sizePolicy)
        self.label_line_lc.setMinimumSize(QSize(75, 24))
        self.label_line_lc.setMaximumSize(QSize(75, 24))
        self.label_line_lc.setObjectName('label_line_lc')
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
        self.tool_btn_line_color.setObjectName('tool_btn_line_color')
        self.horizontalLayout_4.addWidget(self.tool_btn_line_color)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.label_line_marker = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_line_marker.sizePolicy().hasHeightForWidth())
        self.label_line_marker.setSizePolicy(sizePolicy)
        self.label_line_marker.setMinimumSize(QSize(75, 24))
        self.label_line_marker.setMaximumSize(QSize(75, 24))
        self.label_line_marker.setObjectName('label_line_marker')
        self.horizontalLayout_6.addWidget(self.label_line_marker)
        self.combo_box_line_marker = QComboBox(self)
        self.combo_box_line_marker.setMinimumSize(QSize(120, 24))
        self.combo_box_line_marker.setMaximumSize(QSize(16777215, 24))
        self.combo_box_line_marker.setObjectName('combo_box_line_marker')
        
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
        self.line_2.setObjectName('line_2')
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.btn_confirm.setObjectName('btn_confirm')
        self.horizontalLayout_5.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.btn_cancel.setObjectName('btn_cancel')
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
                x0 = mdates.date2num(Time_Model.str_to_datetime(str_x0))
                x1 = mdates.date2num(Time_Model.str_to_datetime(str_x1))
    #            python3.7才可使用fromisoformat函数
    #            x0 = mdates.date2num(datetime.fromisoformat('1900-01-01*' + x[0]))
    #            x1 = mdates.date2num(datetime.fromisoformat('1900-01-01*' + x[1]))
                self.line_xdata = [x0, x1]
                self.line_ydata = [float(str_y0), float(str_y1)]
            if self.linetype == 'Vertical':
                x = mdates.date2num(Time_Model.str_to_datetime(str_x0))
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
        self.verticalLayout.setObjectName('verticalLayout')
        self.label_title = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.label_title.setMinimumSize(QSize(120, 24))
        self.label_title.setMaximumSize(QSize(16777215, 24))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setObjectName('label_title')
        self.verticalLayout.addWidget(self.label_title)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName('line')
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.label_text = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_text.sizePolicy().hasHeightForWidth())
        self.label_text.setSizePolicy(sizePolicy)
        self.label_text.setMinimumSize(QSize(75, 24))
        self.label_text.setMaximumSize(QSize(75, 24))
        self.label_text.setObjectName('label_text')
        self.horizontalLayout.addWidget(self.label_text)
        self.line_edit_text = QLineEdit(self)
        self.line_edit_text.setMinimumSize(QSize(120, 24))
        self.line_edit_text.setMaximumSize(QSize(16777215, 24))
        self.line_edit_text.setText(self.text)
        self.line_edit_text.setObjectName('line_edit_text')
        self.horizontalLayout.addWidget(self.line_edit_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.label_text_rotation = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_text_rotation.sizePolicy().hasHeightForWidth())
        self.label_text_rotation.setSizePolicy(sizePolicy)
        self.label_text_rotation.setMinimumSize(QSize(75, 24))
        self.label_text_rotation.setMaximumSize(QSize(75, 24))
        self.label_text_rotation.setObjectName('label_text_rotation')
        self.horizontalLayout_2.addWidget(self.label_text_rotation)
        self.combo_box_text_rotation = QComboBox(self)
        self.combo_box_text_rotation.setMinimumSize(QSize(120, 24))
        self.combo_box_text_rotation.setMaximumSize(QSize(16777215, 24))
        self.combo_box_text_rotation.setObjectName('combo_box_text_rotation')
        
        count = len(self.enum_text_rotation)
        for i in range(count):
            self.combo_box_text_rotation.addItem('')
            self.combo_box_text_rotation.setItemData(i, self.enum_text_rotation[i], Qt.UserRole)
        index = self.enum_text_rotation.index(self.text_rotation)
        self.combo_box_text_rotation.setCurrentIndex(index)        
        
        self.horizontalLayout_2.addWidget(self.combo_box_text_rotation)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.label_text_size = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_text_size.sizePolicy().hasHeightForWidth())
        self.label_text_size.setSizePolicy(sizePolicy)
        self.label_text_size.setMinimumSize(QSize(75, 24))
        self.label_text_size.setMaximumSize(QSize(75, 24))
        self.label_text_size.setObjectName('label_text_size')
        self.horizontalLayout_3.addWidget(self.label_text_size)
        self.line_edit_text_size = QLineEdit(self)
        self.line_edit_text_size.setMinimumSize(QSize(120, 24))
        self.line_edit_text_size.setMaximumSize(QSize(16777215, 24))
        
        self.line_edit_text_size.setText(str(int(self.text_size)))
        
        self.line_edit_text_size.setObjectName('line_edit_text_size')
        self.horizontalLayout_3.addWidget(self.line_edit_text_size)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.label_text_color = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_text_color.sizePolicy().hasHeightForWidth())
        self.label_text_color.setSizePolicy(sizePolicy)
        self.label_text_color.setMinimumSize(QSize(75, 24))
        self.label_text_color.setMaximumSize(QSize(75, 24))
        self.label_text_color.setObjectName('label_text_color')
        self.horizontalLayout_4.addWidget(self.label_text_color)
        self.color_view = QLabel(self)
        self.color_view.setMinimumSize(QSize(90, 20))
        self.color_view.setMaximumSize(QSize(16777215, 20))
        
        self.color_view.setPalette(QPalette(QColor(self.text_color)))
        self.color_view.setAutoFillBackground(True)
        self.color_view.setText('')
        
        self.color_view.setObjectName('color_view')
        self.horizontalLayout_4.addWidget(self.color_view)
        self.tool_btn_text_color = QToolButton(self)
        self.tool_btn_text_color.setMinimumSize(QSize(24, 24))
        self.tool_btn_text_color.setMaximumSize(QSize(24, 24))
        self.tool_btn_text_color.setObjectName('tool_btn_text_color')
        self.horizontalLayout_4.addWidget(self.tool_btn_text_color)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.label_line_text_style = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(24)
        sizePolicy.setHeightForWidth(self.label_line_text_style.sizePolicy().hasHeightForWidth())
        self.label_line_text_style.setSizePolicy(sizePolicy)
        self.label_line_text_style.setMinimumSize(QSize(75, 24))
        self.label_line_text_style.setMaximumSize(QSize(75, 24))
        self.label_line_text_style.setObjectName('label_line_text_style')
        self.horizontalLayout_6.addWidget(self.label_line_text_style)
        self.combo_box_text_style = QComboBox(self)
        self.combo_box_text_style.setMinimumSize(QSize(120, 24))
        self.combo_box_text_style.setMaximumSize(QSize(16777215, 24))
        self.combo_box_text_style.setObjectName('combo_box_text_style')
        
        count = len(self.enum_text_style)
        for i in range(count):
            self.combo_box_text_style.addItem('')
            self.combo_box_text_style.setItemData(i, self.enum_text_style[i], Qt.UserRole)
        index = self.enum_text_style.index(self.text_style)
        self.combo_box_text_style.setCurrentIndex(index)  
        
        
        self.horizontalLayout_6.addWidget(self.combo_box_text_style)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName('line_2')
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 24))
        self.btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.btn_confirm.setObjectName('btn_confirm')
        self.horizontalLayout_5.addWidget(self.btn_confirm)
        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setMinimumSize(QSize(0, 24))
        self.btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.btn_cancel.setObjectName('btn_cancel')
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
        self.text_style = self.combo_box_text_style.currentData()
        
        self.annotation.set_text(self.text)
        self.annotation.set_rotation(self.text_rotation)
        self.annotation.set_size(self.text_size)
        self.annotation.set_color(self.text_color)
        self.annotation.set_style(self.text_style)
        
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
        self.label_line_text_style.setText(_translate('AnnotationSettingDialog', '文字样式'))
        self.combo_box_text_style.setItemText(0, _translate('AnnotationSettingDialog', 'Normal'))
        self.combo_box_text_style.setItemText(1, _translate('AnnotationSettingDialog', 'Italic'))
        self.combo_box_text_style.setItemText(2, _translate('AnnotationSettingDialog', 'Oblique'))
        self.btn_confirm.setText(_translate('AnnotationSettingDialog', '确定'))
        self.btn_cancel.setText(_translate('AnnotationSettingDialog', '取消'))
        count = len(self.enum_text_rotation_name)
        for i in range(count):
            self.combo_box_text_rotation.setItemText(i, _translate('AnnotationSettingDialog',
                                                                   self.enum_text_rotation_name[i]))
        count = len(self.enum_text_style_name)
        for i in range(count):
            self.combo_box_text_style.setItemText(i, _translate('AnnotationSettingDialog',
                                                                self.enum_text_style_name[i]))
            
class AxisSettingDialog(QDialog):
    
    def __init__(self, parent = None, axes : Axes = None):
        
        super().__init__(parent)
        
        self.axes = axes
        self.stime = ''
        self.etime = ''
        self.xlim = axes.get_xlim()
        self.ylim = axes.get_ylim()
#        !!只有当locator是MaxNLocator时才能使用下列语句!!
#        self.xlocator = axes.xaxis.get_major_locator()._nbins
#        self.ylocator = axes.yaxis.get_major_locator()._nbins
        
#        曲线设置成了不能pick所以可以这样判断，注意它只接受一条曲线
        self.curves = []
        line_info = {}
        lines = axes.get_lines()
        for line in lines:
            if line.pickable():
                pass
            else:
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
        
        stime = mdates.num2date(self.xlim[0]).time().isoformat(timespec='milliseconds')
        self.stime = str(stime)
        self.line_edit_x_left.setText(self.stime)
        
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
        
        etime = mdates.num2date(self.xlim[1]).time().isoformat(timespec='milliseconds')
        self.etime = str(etime)
        self.line_edit_x_right.setText(self.etime)
        
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
        
        self.line_edit_x_left.editingFinished.connect(self.slot_change_stime)
        self.line_edit_x_right.editingFinished.connect(self.slot_change_etime)
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
            x0 = mdates.date2num(Time_Model.str_to_datetime(str_x_left))
            x1 = mdates.date2num(Time_Model.str_to_datetime(str_x_right))
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
                         ncol=1, frameon=False, borderpad = 0.15,
                         prop = CONSTANT.FONT_MSYH)
        
        QDialog.accept(self)

    def slot_change_stime(self):
        
        etime = self.line_edit_x_right.text()
        stime = self.line_edit_x_left.text()
        if Time_Model.is_std_format(stime):
            if Time_Model.compare(stime, etime) != 1:
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                self.stime = Time_Model.timestr_to_stdtimestr(stime)
                self.line_edit_x_left.setText(self.stime)
            else:
                self.line_edit_x_left.setText(self.stime)
                QMessageBox.information(self,
                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                                QCoreApplication.translate('AxisSettingDialog', '起始时间大于终止时间'))
        else:
            self.line_edit_x_left.setText(self.stime)
            QMessageBox.information(self,
                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                            QCoreApplication.translate('AxisSettingDialog', '''<b>请输入正确时间格式</b>
                                                       <br>HH
                                                       <br>HH:MM
                                                       <br>HH:MM:SS
                                                       <br>HH:MM:SS.FFF
                                                       <br>HH:MM:SS:FFF'''))

    def slot_change_etime(self):
        
        etime = self.line_edit_x_right.text()
        stime = self.line_edit_x_left.text()
        if Time_Model.is_std_format(etime):
            if Time_Model.compare(stime, etime) != 1:
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                self.etime = Time_Model.timestr_to_stdtimestr(etime)
                self.line_edit_x_right.setText(self.etime)
            else:
                self.line_edit_x_right.setText(self.etime)
                QMessageBox.information(self,
                                QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                                QCoreApplication.translate('AxisSettingDialog', '终止时间小于起始时间'))
        else:
            self.line_edit_x_right.setText(self.etime)
            QMessageBox.information(self,
                            QCoreApplication.translate('AxisSettingDialog', '输入提示'),
                            QCoreApplication.translate('AxisSettingDialog', '''<b>请输入正确时间格式</b>
                                                       <br>HH
                                                       <br>HH:MM
                                                       <br>HH:MM:SS
                                                       <br>HH:MM:SS.FFF
                                                       <br>HH:MM:SS:FFF'''))
            
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
            self.combo_box_linestyle.setItemText(i, _translate('LineSettingDialog',
                                                               self.enum_linestyle_name[i]))
        count = len(self.enum_marker_name)
        for i in range(count):
            self.combo_box_marker.setItemText(i, _translate('LineSettingDialog',
                                                               self.enum_marker_name[i]))

class FigureCanvasSetiingDialog(QDialog):

    def __init__(self, parent = None, axes : Axes = None):
        
        super().__init__(parent)
        
        self.axes = axes
        self.axis_fontsize = axes[0].get_yticklabels()[0].get_fontsize()
        self.legend_fontsize = axes[0].get_legend()._fontsize
        
        self.setup()
        
    def setup(self):
        
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(260, 140)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setSpacing(4)
        self.group_box_fontsize = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.group_box_fontsize)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.horizontalLayout = QHBoxLayout()
        self.label_axis_fn = QLabel(self.group_box_fontsize)
        self.label_axis_fn.setMinimumSize(QSize(75, 24))
        self.label_axis_fn.setMaximumSize(QSize(75, 24))
        self.horizontalLayout.addWidget(self.label_axis_fn)
        self.line_edit_axis_fn = QLineEdit(self.group_box_fontsize)
        self.line_edit_axis_fn.setText(str(self.axis_fontsize))
        self.line_edit_axis_fn.setMinimumSize(QSize(0, 24))
        self.line_edit_axis_fn.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout.addWidget(self.line_edit_axis_fn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_legend_fn = QLabel(self.group_box_fontsize)
        self.label_legend_fn.setMinimumSize(QSize(75, 24))
        self.label_legend_fn.setMaximumSize(QSize(75, 24))
        self.horizontalLayout_2.addWidget(self.label_legend_fn)
        self.line_edit_legend_fn = QLineEdit(self.group_box_fontsize)
        self.line_edit_legend_fn.setText(str(self.legend_fontsize))
        self.line_edit_legend_fn.setMinimumSize(QSize(0, 24))
        self.line_edit_legend_fn.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_2.addWidget(self.line_edit_legend_fn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.group_box_fontsize)
        self.horizontalLayout_3 = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.push_btn_confirm = QPushButton(self)
        self.push_btn_confirm.setMinimumSize(QSize(0, 24))
        self.push_btn_confirm.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_3.addWidget(self.push_btn_confirm)
        self.push_btn_cancel = QPushButton(self)
        self.push_btn_cancel.setMinimumSize(QSize(0, 24))
        self.push_btn_cancel.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_3.addWidget(self.push_btn_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.retranslateUi()
        
        self.push_btn_confirm.clicked.connect(self.accept)
        self.push_btn_cancel.clicked.connect(self.reject)

    def accept(self):
        
        try:
            self.legend_fontsize = float(self.line_edit_legend_fn.text())
            self.axis_fontsize = float(self.line_edit_axis_fn.text())
        except:
            pass
        for axis in self.axes:
            axis.tick_params(labelsize = self.axis_fontsize)
            axis.legend(fontsize=self.legend_fontsize, loc=(0,1),
                        frameon=False, borderpad = 0.15)
        
        QDialog.accept(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('FigureCanvasSetiingDialog', '画布设置'))
        self.group_box_fontsize.setTitle(_translate('FigureCanvasSetiingDialog', '文字大小'))
        self.label_axis_fn.setText(_translate('FigureCanvasSetiingDialog', '刻度文字'))
        self.label_legend_fn.setText(_translate('FigureCanvasSetiingDialog', '图注文字'))
        self.push_btn_confirm.setText(_translate('FigureCanvasSetiingDialog', '确定'))
        self.push_btn_cancel.setText(_translate('FigureCanvasSetiingDialog', '取消'))
            
class ParameterExportDialog(QDialog):
    
    signal_send_status = pyqtSignal(str, int)
    def __init__(self, parent = None, dict_paras : dict = {}):
        
        super().__init__(parent)
        
        self.outfile_icon = QIcon(CONSTANT.ICON_FILE_EXPORT)
        self.para_icon = QIcon(CONSTANT.ICON_PARA)
        self.file_info = {}
        self.current_file_dir = ''
        
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
        self.horizontalLayout = QHBoxLayout(self.groupBox)
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
        self.push_btn_apply_all_files = QPushButton(self.groupBox)
        self.push_btn_apply_all_files.setFocusPolicy(Qt.NoFocus)
        self.push_btn_apply_all_files.setMinimumSize(QSize(100, 24))
        self.push_btn_apply_all_files.setMaximumSize(QSize(100, 24))
        self.horizontalLayout_5.addWidget(self.push_btn_apply_all_files)
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
# =======连接信号与槽
# =============================================================================
        self.tool_btn_sel_filedir.clicked.connect(self.slot_sel_dir)        
#        self.combo_box_filename.currentIndexChanged.connect(self.slot_change_current_file)        
        self.combo_box_filetype.currentIndexChanged.connect(self.slot_change_filetype)        
        self.line_edit_file_name.editingFinished.connect(self.slot_change_filename)
        self.line_edit_starttime.editingFinished.connect(self.slot_change_file_stime)
        self.line_edit_endtime.editingFinished.connect(self.slot_change_file_etime)
        self.push_btn_apply_all_files.clicked.connect(self.slot_change_all_file_time)
        self.tree_widget_export_paras.itemClicked.connect(self.slot_change_current_file)
        
        self.push_btn_confirm.clicked.connect(self.accept)
        self.push_btn_cancel.clicked.connect(self.reject)

#    让用户选择项目的路径
    def slot_sel_dir(self):
        
        filedir = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('ParameterExportDialog', '导出路径'),
                                                   CONSTANT.SETUP_DIR)
        if filedir:
            filedir = filedir.replace('/','\\')
            self.line_edit_file_dir.setText(filedir)
            
    def slot_change_current_file(self, item):
        
        index = self.tree_widget_export_paras.indexOfTopLevelItem(item)
        if index != -1:
            self.current_file_dir = item.data(0, Qt.UserRole)
        if self.current_file_dir:
            index, filename, filetype, stime, etime, paralist = self.file_info[self.current_file_dir]
            self.line_edit_starttime.setText(stime)
            self.line_edit_endtime.setText(etime)
            self.combo_box_filetype.setCurrentIndex(
                    self.combo_box_filetype.findData(filetype, Qt.UserRole))
            self.line_edit_file_name.setText(filename)
        
    def slot_change_filetype(self, index):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
            index, filename, filetype, stime, etime, paralist = self.file_info[file_dir]
            filetype = self.combo_box_filetype.currentData()
            item = self.tree_widget_export_paras.topLevelItem(index)
            item.setText(0, filename + filetype)
            self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist)
            
    def slot_change_filename(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
            f = self.line_edit_file_name.text()
            index, filename, filetype, stime, etime, paralist = self.file_info[file_dir]
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
                self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist)
            else:
                self.line_edit_file_name.setText(filename)
                
    def slot_change_file_stime(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
#            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
            if file_dir[0] == '_':
                data_stime = self.dict_data[file_dir].time_range[0]
            else:
                file = Normal_DataFile(file_dir)
                data_stime = file.time_range[0]
            starttime = self.line_edit_starttime.text()
            index, filename, filetype, stime, etime, paralist = self.file_info[file_dir]
            if Time_Model.is_std_format(starttime):
                if Time_Model.is_in_range(data_stime, etime, starttime):
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                    self.line_edit_starttime.setText(
                            Time_Model.timestr_to_stdtimestr(starttime))
                    stime = Time_Model.timestr_to_stdtimestr(starttime)
                    self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist)
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
                data_etime = self.dict_data[file_dir].time_range[1]
            else:
                file = Normal_DataFile(file_dir)
                data_etime = file.time_range[1]
            endtime = self.line_edit_endtime.text()
            index, filename, filetype, stime, etime, paralist = self.file_info[file_dir]
            if Time_Model.is_std_format(endtime):
                if Time_Model.is_in_range(stime, data_etime, endtime):
#                    输入正确的起始时间后，还需要转换成标准格式后再显示
                    self.line_edit_endtime.setText(
                            Time_Model.timestr_to_stdtimestr(endtime))
                    etime = Time_Model.timestr_to_stdtimestr(endtime)
                    self.file_info[file_dir] = (index, filename, filetype, stime, etime, paralist)
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
                
    def slot_change_all_file_time(self):
        
#        file_dir = self.combo_box_filename.currentData()
        file_dir = self.current_file_dir
        if file_dir:
#            确保时间是正确的
            self.slot_change_file_stime()
            self.slot_change_file_etime()
            index, fn, ft, tstime, tetime, pl = self.file_info[file_dir]
            for file in self.file_info:
                if file != file_dir:
                    index, filename, filetype, stime, etime, paralist = self.file_info[file]
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
                    self.file_info[file] = (index, filename, ft, stime, etime, paralist)
                        
    def accept(self):
        
        self.signal_send_status.emit('导出数据中...', 0)
        for file_dir in self.file_info:
            index, filename, filetype, stime, etime, paralist = self.file_info[file_dir]
#            判断是否为文件路径，其他类型的数据字典的键暂时约定在开头加‘_’前缀
            if file_dir[0] == '_':
                data = self.dict_data[file_dir].get_trange_data(stime, etime)
            else:
                data = DataFactory(file_dir, paralist)
                data = data.get_trange_data(stime, etime)
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
        self.signal_send_status.emit('导出数据成功！', 1500)
        
        QDialog.accept(self)
            
    def display_file_info(self, dict_paras):
        
        stime = ''
        etime = ''
        f = ''
        for index, file_dir in enumerate(dict_paras):
            if type(dict_paras[file_dir]) == list:
                file = Normal_DataFile(file_dir)
                filename = file.filename[:-4] + '(export' + str(index) + ')'
                start = file.time_range[0]
                end = file.time_range[1]
                paralist = dict_paras[file_dir]
            elif type(dict_paras[file_dir]) == pd.DataFrame:
                data = DataFactory(dict_paras[file_dir])
                self.dict_data[file_dir] = data
                filename = 'FastPlot DataFile ' + str(index)
                start = data.time_range[0]
                end = data.time_range[1]
                paralist = data.get_paralist()
            elif type(dict_paras[file_dir]) == DataFactory:
                data = dict_paras[file_dir]
                self.dict_data[file_dir] = data
                filename = 'FastPlot DataFile ' + str(index)
                start = data.time_range[0]
                end = data.time_range[1]
                paralist = data.get_paralist()
#            在树组件中显示
            item = QTreeWidgetItem(self.tree_widget_export_paras)
            item.setIcon(0, self.outfile_icon)
            item.setText(0, filename + '.txt')
            item.setData(0, Qt.UserRole, file_dir)
            item.setText(1, start)
            item.setText(2, end)
            for paraname in paralist:
                child_item = QTreeWidgetItem(item)
                child_item.setText(0, paraname)
                child_item.setIcon(0, self.para_icon)
#            在复选框中显示
#            self.combo_box_filename.addItem(filename)
#            self.combo_box_filename.setItemData(i, file_dir, Qt.UserRole)
#            存取文件信息（文件名，文件类型，起始时间，终止时间，排好序的参数列表），以供导出
            self.file_info[file_dir] = (index, filename, '.txt', start, end, paralist)
            if index == 0:
                stime = start
                etime = end
                f = filename
                self.current_file_dir = file_dir
#        self.combo_box_filename.setCurrentIndex(0)
        self.tree_widget_export_paras.setCurrentItem(self.tree_widget_export_paras.topLevelItem(0))
        self.combo_box_filetype.setCurrentIndex(0)
        self.line_edit_starttime.setText(stime)
        self.line_edit_endtime.setText(etime)
        self.line_edit_file_name.setText(f)
        self.line_edit_file_dir.setText(CONSTANT.SETUP_DIR)
            

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('ParameterExportDialog', '导出参数数据'))
        self.group_box_preview.setTitle(_translate('ParameterExportDialog', '导出预览'))
        self.tree_widget_export_paras.headerItem().setText(0, _translate('ParameterExportDialog', '文件名'))
        self.tree_widget_export_paras.headerItem().setText(1, _translate('ParameterExportDialog', '起始时间'))
        self.tree_widget_export_paras.headerItem().setText(2, _translate('ParameterExportDialog', '终止时间'))
        self.group_box_setting.setTitle(_translate('ParameterExportDialog', '导出设置'))
        self.groupBox.setTitle(_translate('ParameterExportDialog', '时间设置'))
        self.label_starttime.setText(_translate('ParameterExportDialog', '起始时间'))
        self.label_endtime.setText(_translate('ParameterExportDialog', '终止时间'))
        self.push_btn_apply_all_files.setText(_translate('ParameterExportDialog', '同步设置'))
        self.group_box_file_setting.setTitle(_translate('ParameterExportDialog', '文件设置'))
        self.label_file_type.setText(_translate('ParameterExportDialog', '文件类型'))
        self.label_file_name.setText(_translate('ParameterExportDialog', '文件名'))
        self.label_file_dir.setText(_translate('ParameterExportDialog', '文件路径'))
        self.tool_btn_sel_filedir.setText(_translate('ParameterExportDialog', '...'))
        self.combo_box_filetype.setItemText(0, _translate('ParameterExportDialog', 'TXT file'))
        self.combo_box_filetype.setItemText(1, _translate('ParameterExportDialog', 'CSV file'))
        self.combo_box_filetype.setItemText(2, _translate('ParameterExportDialog', 'MAT file'))
        self.push_btn_confirm.setText(_translate('ParameterExportDialog', '保存'))
        self.push_btn_cancel.setText(_translate('ParameterExportDialog', '取消'))
        
class FileProcessDialog(QDialog):
    
    signal_send_status = pyqtSignal(str, int)
    
    def __init__(self, parent = None, files = [], time_intervals = {}):
    
        super().__init__(parent)
        
        self.outfile_icon = QIcon(CONSTANT.ICON_FILE_EXPORT)
        self.para_icon = QIcon(CONSTANT.ICON_PARA)
        self.file_icon = QIcon(CONSTANT.ICON_FILE)
        self.file_info = {}
        self.current_interval_item = None
        self.current_floder_item = None
        
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
            file = Normal_DataFile(file_dir)
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
                                                   CONSTANT.SETUP_DIR)
        if filedir:
            filedir = filedir.replace('/','\\')
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
            file = Normal_DataFile(file_dir)
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
            file = Normal_DataFile(file_dir)
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
            file = Normal_DataFile(file_dir)
            folder = self.line_edit_file_dir.text() + '\\' + file.filename[:-4]
            if not os.path.exists(folder):
                os.mkdir(folder)
            data = file.cols_input(file_dir, file.paras_in_file, '\s+', stime, etime)
            ana = DataAnalysis()
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
            file = Normal_DataFile(file_dir)
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
        self.line_edit_file_dir.setText(CONSTANT.SETUP_DIR)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('FileProcessDialog', '文件处理'))
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
        self.push_btn_apply_all_files.setText(_translate('FileProcessDialog', '同步设置'))
        self.group_box_file_setting.setTitle(_translate('FileProcessDialog', '文件设置'))
        self.label_file_type.setText(_translate('FileProcessDialog', '文件类型'))
        self.label_file_name.setText(_translate('FileProcessDialog', '文件名'))
        self.label_file_dir.setText(_translate('FileProcessDialog', '文件路径'))
        self.tool_btn_sel_filedir.setText(_translate('FileProcessDialog', '...'))
        self.combo_box_filetype.setItemText(0, _translate('ParameterExportDialog', 'TXT file'))
        self.combo_box_filetype.setItemText(1, _translate('ParameterExportDialog', 'CSV file'))
        self.combo_box_filetype.setItemText(2, _translate('ParameterExportDialog', 'MAT file'))
        self.push_btn_confirm.setText(_translate('FileProcessDialog', '保存'))
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


#测试用     
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    d = SelFunctionDialog()
    d.show()
    app.exec_()