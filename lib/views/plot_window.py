# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：绘图窗口类
#
# =======使用说明
# 
#
# =======日志
# 

# =============================================================================

import sys
import pandas as pd
sys.path.append(r"E:\DAGUI\lib")
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtWidgets import (QWidget, QToolButton, QSpacerItem,
                             QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QDialog, QMessageBox, QScrollArea)
from PyQt5.QtCore import QCoreApplication, QSize, pyqtSignal
from PyQt5.QtGui import QIcon

# =============================================================================
# Package views imports
# =============================================================================
from models.figure_model import PlotCanvas
from custom_dialog import SelectTemplateDialog, SaveTemplateDialog
from models.datafile_model import Normal_DataFile
# =============================================================================
# CustomScrollArea
# =============================================================================
class CustomScrollArea(QScrollArea):

    signal_resize = pyqtSignal(QSize)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
    def resizeEvent(self, event):
        
        self.signal_resize.emit(event.size())
        QScrollArea.resizeEvent(self, event)
        
# =============================================================================
# PlotWindow
# =============================================================================
class PlotWindow(QWidget):

    signal_get_plot_temps = pyqtSignal()
    signal_save_temp = pyqtSignal(dict)
    signal_use_subline = pyqtSignal(bool)
# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pan_on = False
        self.zoom_on = False
        self.use_subline = False

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):
        
        self.setObjectName("PlotWindow")
#        该窗口的主布局器，水平
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(4, 0, 4, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#        创建画布部件
        self.scrollarea = CustomScrollArea(self)
        self.plotcanvas = PlotCanvas(self.scrollarea)
        self.scrollarea.setWidget(self.plotcanvas)
#        创建右侧的工具栏
        self.widget_plot_tools = QWidget(self)
        self.widget_plot_tools.setMinimumSize(QSize(32, 0))
        self.widget_plot_tools.setMaximumSize(QSize(32, 16777215))
        self.widget_plot_tools.setObjectName("widget_plot_tools")
#        子布局器，垂直，布局工具按钮
        self.verticalLayout = QVBoxLayout(self.widget_plot_tools)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
#        创建放大缩小按钮并加入工具栏
        self.button_home = QToolButton(self.widget_plot_tools)
        self.button_home.setMinimumSize(QSize(32, 32))
        self.button_home.setMaximumSize(QSize(32, 32))
        self.button_home.setObjectName("button_home")
        self.button_home.setIcon(QIcon(r"E:\DAGUI\lib\icon\home.ico"))
        self.verticalLayout.addWidget(self.button_home)
        self.button_pan = QToolButton(self.widget_plot_tools)
        self.button_pan.setMinimumSize(QSize(32, 32))
        self.button_pan.setMaximumSize(QSize(32, 32))
        self.button_pan.setCheckable(True)
        self.button_pan.setObjectName("button_pan")
        self.button_pan.setIcon(QIcon(r"E:\DAGUI\lib\icon\pan.png"))
        self.verticalLayout.addWidget(self.button_pan)
        self.button_zoom = QToolButton(self.widget_plot_tools)
        self.button_zoom.setMinimumSize(QSize(32, 32))
        self.button_zoom.setMaximumSize(QSize(32, 32))
        self.button_zoom.setCheckable(True)
        self.button_zoom.setObjectName("button_zoom")
        self.button_zoom.setIcon(QIcon(r"E:\DAGUI\lib\icon\zoom.ico"))
        self.verticalLayout.addWidget(self.button_zoom)
        self.button_edit = QToolButton(self.widget_plot_tools)
        self.button_edit.setMinimumSize(QSize(32, 32))
        self.button_edit.setMaximumSize(QSize(32, 32))
        self.button_edit.setObjectName("button_edit")
        self.button_edit.setIcon(QIcon(r"E:\DAGUI\lib\icon\edit.png"))
        self.verticalLayout.addWidget(self.button_edit)
        self.button_config = QToolButton(self.widget_plot_tools)
        self.button_config.setMinimumSize(QSize(32, 32))
        self.button_config.setMaximumSize(QSize(32, 32))
        self.button_config.setObjectName("button_config")
        self.button_config.setIcon(QIcon(r"E:\DAGUI\lib\icon\config.ico"))
        self.verticalLayout.addWidget(self.button_config)
        self.button_back = QToolButton(self.widget_plot_tools)
        self.button_back.setMinimumSize(QSize(32, 32))
        self.button_back.setMaximumSize(QSize(32, 32))
        self.button_back.setObjectName("button_back")
        self.button_back.setIcon(QIcon(r"E:\DAGUI\lib\icon\back.ico"))
        self.verticalLayout.addWidget(self.button_back)
        self.button_forward = QToolButton(self.widget_plot_tools)
        self.button_forward.setMinimumSize(QSize(32, 32))
        self.button_forward.setMaximumSize(QSize(32, 32))
        self.button_forward.setObjectName("button_forward")
        self.button_forward.setIcon(QIcon(r"E:\DAGUI\lib\icon\forward.ico"))
        self.verticalLayout.addWidget(self.button_forward)    
        self.button_save = QToolButton(self.widget_plot_tools)
        self.button_save.setMinimumSize(QSize(32, 32))
        self.button_save.setMaximumSize(QSize(32, 32))
        self.button_save.setObjectName("button_save")
        self.button_save.setIcon(QIcon(r"E:\DAGUI\lib\icon\save.ico"))
        self.verticalLayout.addWidget(self.button_save)
        self.button_sel_temp = QToolButton(self.widget_plot_tools)
        self.button_sel_temp.setMinimumSize(QSize(32, 32))
        self.button_sel_temp.setMaximumSize(QSize(32, 32))
        self.button_sel_temp.setObjectName("button_sel_temp")
        self.button_sel_temp.setIcon(QIcon(r"E:\DAGUI\lib\icon\use_template.ico"))
        self.verticalLayout.addWidget(self.button_sel_temp)
        self.button_save_temp = QToolButton(self.widget_plot_tools)
        self.button_save_temp.setMinimumSize(QSize(32, 32))
        self.button_save_temp.setMaximumSize(QSize(32, 32))
        self.button_save_temp.setObjectName("button_save_temp")
        self.button_save_temp.setIcon(QIcon(r"E:\DAGUI\lib\icon\save_template.ico"))
        self.verticalLayout.addWidget(self.button_save_temp)
        self.button_add_line_marker = QToolButton(self.widget_plot_tools)
        self.button_add_line_marker.setCheckable(True)
        self.button_add_line_marker.setMinimumSize(QSize(32, 32))
        self.button_add_line_marker.setMaximumSize(QSize(32, 32))
        self.button_add_line_marker.setIcon(QIcon(r"E:\DAGUI\lib\icon\line_marker.ico"))
        self.verticalLayout.addWidget(self.button_add_line_marker)
        self.button_add_text = QToolButton(self.widget_plot_tools)
        self.button_add_text.setMinimumSize(QSize(32, 32))
        self.button_add_text.setMaximumSize(QSize(32, 32))
        self.button_add_text.setIcon(QIcon(r"E:\DAGUI\lib\icon\text.ico"))
        self.verticalLayout.addWidget(self.button_add_text)
        spacerItem = QSpacerItem(20, 219, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
#        先添加工具栏在添加包括画布/滑块的水平子布局器
        self.horizontalLayout_2.addWidget(self.widget_plot_tools)
        self.horizontalLayout_2.addWidget(self.scrollarea)

        self.retranslateUi()
# =======连接信号与槽
# =============================================================================
        self.button_home.clicked.connect(self.slot_home)
        self.button_pan.clicked.connect(self.slot_pan)
        self.button_zoom.clicked.connect(self.slot_zoom)
        self.button_edit.clicked.connect(self.slot_edit)
        self.button_config.clicked.connect(self.slot_config_subplots)
        self.button_save.clicked.connect(self.slot_save)
        self.button_back.clicked.connect(self.slot_back)
        self.button_forward.clicked.connect(self.slot_forward)
        self.button_sel_temp.clicked.connect(self.signal_get_plot_temps)
        self.button_save_temp.clicked.connect(self.slot_save_temp)
#        添加辅助线
        self.button_add_line_marker.clicked.connect(self.slot_subline_connect)
        self.signal_use_subline.connect(self.plotcanvas.slot_use_subline)
        
        self.scrollarea.signal_resize.connect(self.slot_resize_canvas)
#        临时连接
        self.plotcanvas.signal_temp.connect(self.slot_plot)

# =============================================================================
# slots模块
# =============================================================================   
#    def slot_plot(self, filegroup):
#        
#        if filegroup:
#            for filedir in filegroup:
#                cols = len(filegroup[filedir])
#                if cols > 4:
#                    self.scrollarea.setWidgetResizable(False)
##                    乘以1.05是估计的，刚好能放下四张图，
##                    减去的19是滚动条的宽度
#                    height = int(self.scrollarea.height() * 1.05) / 4
#                    self.plotcanvas.resize(self.scrollarea.width() - 19,
#                                           cols * height)
#                else:
#                    self.scrollarea.setWidgetResizable(True)
#                self.plotcanvas.subplot_para_wxl(filedir, filegroup[filedir])
        
    def slot_plot(self, filegroup):
        
        if filegroup:
            
            df_list = []
            flag = True
            for filedir in filegroup:
                file = Normal_DataFile(filedir)
                if flag:
                    filegroup[filedir].insert(0, file.paras_in_file[0])
                    flag = False
                df = file.cols_input(filedir, filegroup[filedir], '\s+')
            df_list.append(df)
            df_all = pd.concat(df_list,axis = 1,join = 'outer',
                               ignore_index = False)            
            cols = df_all.columns.size - 1
            if cols > 4:
                self.scrollarea.setWidgetResizable(False)
#                    乘以1.05是估计的，刚好能放下四张图，
#                    减去的19是滚动条的宽度
                height = int(self.scrollarea.height() * 1.05) / 4
                self.plotcanvas.resize(self.scrollarea.width() - 19,
                                       cols * height)
            else:
                self.scrollarea.setWidgetResizable(True)
            self.plotcanvas.subplot_para_wxl(df_all, df_all.columns.values.tolist())

    def slot_resize_canvas(self, scroll_area_size):
        
        if not self.scrollarea.widgetResizable():
            if scroll_area_size.height() > self.plotcanvas.size().height():
                self.plotcanvas.resize(scroll_area_size)
            else:
                self.plotcanvas.resize(scroll_area_size.width(),
                                       self.plotcanvas.size().height())

    def slot_home(self):
        self.plotcanvas.toolbar.home()
        
    def slot_pan(self):
        self.plotcanvas.toolbar.pan()
#        完成按钮按下和弹起的效果
        if self.pan_on:
            self.button_pan.setChecked(False)
            self.pan_on = False
        else:
            self.button_pan.setChecked(True)
            self.pan_on = True
#            保证pan按钮和zoom按钮不能同时按下
            if self.zoom_on:
                self.button_zoom.setChecked(False)
                self.zoom_on = False
        
    def slot_zoom(self):
        self.plotcanvas.toolbar.zoom()
#        完成按钮按下和弹起的效果
        if self.zoom_on:
            self.button_zoom.setChecked(False)
            self.zoom_on = False
        else:
            self.button_zoom.setChecked(True)
            self.zoom_on = True
#            保证pan按钮和zoom按钮不能同时按下
            if self.pan_on:
                self.button_pan.setChecked(False)
                self.pan_on = False
        
    def slot_config_subplots(self):
        self.plotcanvas.toolbar.configure_subplots()
        
    def slot_save(self):
        self.plotcanvas.toolbar.save_figure()
        
    def slot_back(self):        
        self.plotcanvas.toolbar.back()
        
    def slot_forward(self):
        self.plotcanvas.toolbar.forward()
        
    def slot_edit(self):
        self.plotcanvas.toolbar.edit_parameters()
        
    def slot_sel_temp(self, dict_files, templates):

        if templates:
            export_paras = {}
            dialog = SelectTemplateDialog(self, templates)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                if dict_files:
        #            遍历文件，搜索是否存在模板中的参数
        #            不同文件下的同一参数都会找出（这样耗时较长）
        #            也可以找到第一个就停止
                    for paraname in templates[dialog.sel_temp]:
                        for file_dir in dict_files:
                            if paraname in dict_files[file_dir]:
                                if file_dir in export_paras:
                                    export_paras[file_dir].append(paraname)
                                else:
                                    export_paras[file_dir] = []
                                    export_paras[file_dir].append(paraname)
        #                        加入以下语句实现找到第一个就停止的功能
        #                        break
                    self.slot_plot(export_paras)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate("DataExportWindow", "导入模板错误"),
                            QCoreApplication.translate("DataExportWindow", "没有发现数据文件"))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate("DataExportWindow", "导入模板错误"),
                    QCoreApplication.translate("DataExportWindow", "没有模板")) 
    
    def slot_save_temp(self):
        
        if self.plotcanvas.paralist:
            temp = {}
            dialog = SaveTemplateDialog(self)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                temp_name = dialog.temp_name
                if temp_name:
                    temp[temp_name] = self.plotcanvas.paralist
                    self.signal_save_temp.emit(temp)
                else:
                    QMessageBox.information(self,
                            QCoreApplication.translate("DataExportWindow", "输入提示"),
                            QCoreApplication.translate("DataExportWindow", "未输入模板名"))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate("DataExportWindow", "保存错误"),
                    QCoreApplication.translate("DataExportWindow", "没有发现图表")) 
    
    def slot_subline_connect(self):
        
        if self.use_subline:
            self.button_add_line_marker.setChecked(False)
            self.use_subline = False
            self.signal_use_subline.emit(False)
        else:
            self.button_add_line_marker.setChecked(True)
            self.use_subline = True
            self.signal_use_subline.emit(True)
        
# =============================================================================
# 功能函数模块
# =============================================================================
                
    
    
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("PlotWindow", "Plot"))
        self.button_home.setToolTip(_translate("PlotWindow", "初始状态"))
        self.button_pan.setToolTip(_translate("PlotWindow", "移动与缩放"))
        self.button_zoom.setToolTip(_translate("PlotWindow", "框选缩放"))
        self.button_config.setToolTip(_translate("PlotWindow", "画布设置"))
        self.button_edit.setToolTip(_translate("PlotWindow", "图表设置"))
        self.button_forward.setToolTip(_translate("PlotWindow", "前进"))
        self.button_back.setToolTip(_translate("PlotWindow", "后退"))
        self.button_save.setToolTip(_translate("PlotWindow", "保存"))
        self.button_save_temp.setToolTip(_translate("PlotWindow", "保存模板"))
        self.button_sel_temp.setToolTip(_translate("PlotWindow", "选择模板"))
        self.button_add_line_marker.setToolTip(_translate("PlotWindow", "增加辅助线"))