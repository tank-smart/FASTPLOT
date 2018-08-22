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
from datetime import datetime
import pandas as pd
import scipy.io as sio
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtWidgets import (QWidget, QToolButton, QSpacerItem,
                             QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMessageBox, QScrollArea, QTableWidget,
                             QFileDialog, QTableWidgetItem, 
                             QComboBox, QGroupBox, QLabel)
from PyQt5.QtCore import (QCoreApplication, QSize, pyqtSignal, QDataStream,
                          QIODevice, Qt)
from PyQt5.QtGui import QIcon

# =============================================================================
# Package views imports
# =============================================================================
from models.figure_model import PlotCanvas
#from views.custom_dialog import SelectTemplateDialog, SaveTemplateDialog
import views.constant as CONSTANT
# =============================================================================
# CustomScrollArea
# =============================================================================
class CustomScrollArea(QScrollArea):

    signal_resize = pyqtSignal(QSize)
    signal_drop_paras = pyqtSignal(tuple)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        
    def resizeEvent(self, event):
        
        self.signal_resize.emit(event.size())
        QScrollArea.resizeEvent(self, event)
        
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
            self.signal_drop_paras.emit((paras, sorted_paras))
            event.acceptProposedAction()
        else:
            event.ignore()
        
# =============================================================================
# PlotWindow
# =============================================================================
class PlotWindow(QWidget):

    signal_request_temps = pyqtSignal(str)
    signal_save_temp = pyqtSignal(dict)
    signal_use_markline = pyqtSignal(bool)
    signal_is_display_menu = pyqtSignal(bool)
# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pan_on = False
        self.zoom_on = False
        self.use_markline = False
        
        self.count_axis = 0
#        用户保存的时刻
        self.timestamps = []

# =============================================================================
# UI模块        
# =============================================================================
    def setup(self):
        
#        该窗口的主布局器，水平
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
#        创建画布部件
        self.scrollarea = CustomScrollArea(self)
        self.plotcanvas = PlotCanvas(self.scrollarea)
        self.scrollarea.setWidget(self.plotcanvas)
#        创建右侧的工具栏
        self.widget_plot_tools = QWidget(self)
        self.widget_plot_tools.setMinimumSize(QSize(32, 0))
        self.widget_plot_tools.setMaximumSize(QSize(32, 16777215))
#        子布局器，垂直，布局工具按钮
        self.verticalLayout = QVBoxLayout(self.widget_plot_tools)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
#        创建放大缩小按钮并加入工具栏
        self.button_home = QToolButton(self.widget_plot_tools)
        self.button_home.setMinimumSize(QSize(30, 30))
        self.button_home.setMaximumSize(QSize(30, 30))
        self.button_home.setIconSize(QSize(22, 22))
        self.button_home.setIcon(QIcon(CONSTANT.ICON_HOME))
        self.verticalLayout.addWidget(self.button_home)
        self.button_pan = QToolButton(self.widget_plot_tools)
        self.button_pan.setMinimumSize(QSize(30, 30))
        self.button_pan.setMaximumSize(QSize(30, 30))
        self.button_pan.setIconSize(QSize(22, 22))
        self.button_pan.setCheckable(True)
        self.button_pan.setIcon(QIcon(CONSTANT.ICON_PAN))
        self.verticalLayout.addWidget(self.button_pan)
        self.button_zoom = QToolButton(self.widget_plot_tools)
        self.button_zoom.setMinimumSize(QSize(30, 30))
        self.button_zoom.setMaximumSize(QSize(30, 30))
        self.button_pan.setIconSize(QSize(22, 22))
        self.button_zoom.setCheckable(True)
        self.button_zoom.setIcon(QIcon(CONSTANT.ICON_ZOOM))
        self.verticalLayout.addWidget(self.button_zoom)
#        self.button_plot_setting = QToolButton(self.widget_plot_tools)
#        self.button_plot_setting.setMinimumSize(QSize(30, 30))
#        self.button_plot_setting.setMaximumSize(QSize(30, 30))
#        self.button_plot_setting.setIconSize(QSize(22, 22))
#        self.button_plot_setting.setIcon(QIcon(CONSTANT.ICON_PLOT_SETTING))
#        self.verticalLayout.addWidget(self.button_plot_setting)
#        self.button_edit = QToolButton(self.widget_plot_tools)
#        self.button_edit.setMinimumSize(QSize(30, 30))
#        self.button_edit.setMaximumSize(QSize(30, 30))
#        self.button_edit.setObjectName('button_edit')
#        self.button_edit.setIcon(QIcon(CONSTANT.ICON_EDIT))
#        self.verticalLayout.addWidget(self.button_edit)
#        self.button_config = QToolButton(self.widget_plot_tools)
#        self.button_config.setMinimumSize(QSize(30, 30))
#        self.button_config.setMaximumSize(QSize(30, 30))
#        self.button_config.setObjectName('button_config')
#        self.button_config.setIcon(QIcon(CONSTANT.ICON_CONFIG))
#        self.verticalLayout.addWidget(self.button_config)
        self.button_back = QToolButton(self.widget_plot_tools)
        self.button_back.setMinimumSize(QSize(30, 30))
        self.button_back.setMaximumSize(QSize(30, 30))
        self.button_back.setIconSize(QSize(22, 22))
        self.button_back.setIcon(QIcon(CONSTANT.ICON_BACK))
        self.verticalLayout.addWidget(self.button_back)
        self.button_forward = QToolButton(self.widget_plot_tools)
        self.button_forward.setMinimumSize(QSize(30, 30))
        self.button_forward.setMaximumSize(QSize(30, 30))
        self.button_forward.setIconSize(QSize(22, 22))
        self.button_forward.setIcon(QIcon(CONSTANT.ICON_FORWARD))
        self.verticalLayout.addWidget(self.button_forward)    
        self.button_save = QToolButton(self.widget_plot_tools)
        self.button_save.setMinimumSize(QSize(30, 30))
        self.button_save.setMaximumSize(QSize(30, 30))
        self.button_save.setIconSize(QSize(22, 22))
        self.button_save.setIcon(QIcon(CONSTANT.ICON_SAVE))
        self.verticalLayout.addWidget(self.button_save)
#        self.button_sel_temp = QToolButton(self.widget_plot_tools)
#        self.button_sel_temp.setMinimumSize(QSize(30, 30))
#        self.button_sel_temp.setMaximumSize(QSize(30, 30))
#        self.button_sel_temp.setObjectName('button_sel_temp')
#        self.button_sel_temp.setIcon(QIcon(CONSTANT.ICON_SEL_TEMP))
#        self.verticalLayout.addWidget(self.button_sel_temp)
#        self.button_save_temp = QToolButton(self.widget_plot_tools)
#        self.button_save_temp.setMinimumSize(QSize(30, 30))
#        self.button_save_temp.setMaximumSize(QSize(30, 30))
#        self.button_save_temp.setObjectName('button_save_temp')
#        self.button_save_temp.setIcon(QIcon(CONSTANT.ICON_SAVE_TEMP))
#        self.verticalLayout.addWidget(self.button_save_temp)
        self.button_clear_canvas = QToolButton(self.widget_plot_tools)
        self.button_clear_canvas.setMinimumSize(QSize(30, 30))
        self.button_clear_canvas.setMaximumSize(QSize(30, 30))
        self.button_clear_canvas.setIconSize(QSize(22, 22))
        self.button_clear_canvas.setIcon(QIcon(CONSTANT.ICON_CLEAR))
        self.verticalLayout.addWidget(self.button_clear_canvas)
        self.button_get_paravalue = QToolButton(self.widget_plot_tools)
        self.button_get_paravalue.setCheckable(True)
        self.button_get_paravalue.setMinimumSize(QSize(30, 30))
        self.button_get_paravalue.setMaximumSize(QSize(30, 30))
        self.button_get_paravalue.setIconSize(QSize(22, 22))
        self.button_get_paravalue.setIcon(QIcon(CONSTANT.ICON_PARA_VALUE))
        self.verticalLayout.addWidget(self.button_get_paravalue)
        spacerItem = QSpacerItem(20, 219, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        self.para_value_window = QWidget(self)
        self.para_value_window.setMinimumSize(QSize(250, 0))
        self.para_value_window.setMaximumSize(QSize(250, 16777215))
        
        self.vl_para_window = QVBoxLayout(self.para_value_window)
        self.vl_para_window.setContentsMargins(2, 2, 2, 0)
        self.vl_para_window.setSpacing(2)
        self.group_box_time_interval = QGroupBox(self.para_value_window)
        self.vl_gbtr = QVBoxLayout(self.group_box_time_interval)
        self.vl_gbtr.setContentsMargins(2, 2, 2, 2)
        self.vl_gbtr.setSpacing(2)
        self.hl_combo = QHBoxLayout()
        self.hl_combo.setSpacing(4)
        self.combo_box_time_intervals = QComboBox(self.group_box_time_interval)
        self.combo_box_time_intervals.setMinimumSize(QSize(0, 24))
        self.combo_box_time_intervals.setMaximumSize(QSize(16777215, 24))
        self.hl_combo.addWidget(self.combo_box_time_intervals)
        self.tool_btn_time_interval = QToolButton(self.group_box_time_interval)
        self.tool_btn_time_interval.setMinimumSize(QSize(24, 24))
        self.tool_btn_time_interval.setMaximumSize(QSize(24, 24))
        self.hl_combo.addWidget(self.tool_btn_time_interval)
        self.vl_gbtr.addLayout(self.hl_combo)
        self.hl_combo_2 = QHBoxLayout()
        self.hl_combo_2.setSpacing(4)
        self.combo_box_time = QComboBox(self.group_box_time_interval)
        self.combo_box_time.setMinimumSize(QSize(0, 24))
        self.combo_box_time.setMaximumSize(QSize(16777215, 24))
        self.hl_combo_2.addWidget(self.combo_box_time)
        self.tool_btn_time = QToolButton(self.group_box_time_interval)
        self.tool_btn_time.setMinimumSize(QSize(24, 24))
        self.tool_btn_time.setMaximumSize(QSize(24, 24))
        self.hl_combo_2.addWidget(self.tool_btn_time)
        self.vl_gbtr.addLayout(self.hl_combo_2)
        self.vl_para_window.addWidget(self.group_box_time_interval)
        self.group_box_time = QGroupBox(self.para_value_window)
        self.vl_gbt = QVBoxLayout(self.group_box_time)
        self.vl_gbt.setContentsMargins(2, 2, 2, 0)
        self.vl_gbt.setSpacing(2)
        self.label_time = QLabel(self.group_box_time)
        self.label_time.setMinimumSize(QSize(0, 24))
        self.label_time.setMaximumSize(QSize(16777215, 24))
        self.vl_gbt.addWidget(self.label_time)
        self.table_widget_value = QTableWidget(self.group_box_time)
        self.table_widget_value.setColumnCount(2)
        self.table_widget_value.setRowCount(0)
        item = QTableWidgetItem()
        self.table_widget_value.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.table_widget_value.setHorizontalHeaderItem(1, item)
        self.table_widget_value.horizontalHeader().setDefaultSectionSize(119)
        self.table_widget_value.verticalHeader().setVisible(False)
        self.vl_gbt.addWidget(self.table_widget_value)
        self.vl_para_window.addWidget(self.group_box_time)
        
#        先添加工具栏在添加包括画布/滑块的水平子布局器
        self.horizontalLayout_2.addWidget(self.widget_plot_tools)
        self.horizontalLayout_2.addWidget(self.scrollarea)
        self.horizontalLayout_2.addWidget(self.para_value_window)
        self.para_value_window.setHidden(True)

        self.retranslateUi()
# =======连接信号与槽
# =============================================================================
        self.button_home.clicked.connect(self.plotcanvas.toolbar.home)
        self.button_pan.clicked.connect(self.slot_pan)
        self.button_zoom.clicked.connect(self.slot_zoom)
#        self.button_plot_setting.clicked.connect(self.plotcanvas.slot_plot_setting)
#        self.button_edit.clicked.connect(self.plotcanvas.toolbar.edit_parameters)
#        self.button_config.clicked.connect(self.plotcanvas.toolbar.configure_subplots)
        self.button_save.clicked.connect(self.slot_save_figure)
        self.button_back.clicked.connect(self.plotcanvas.toolbar.back)
        self.button_forward.clicked.connect(self.plotcanvas.toolbar.forward)
#        self.button_sel_temp.clicked.connect(self.slot_emit_request_plot_temps)
#        self.button_save_temp.clicked.connect(self.slot_save_temp)
        self.button_clear_canvas.clicked.connect(self.slot_clear_canvas)
        self.button_get_paravalue.clicked.connect(self.slot_paravalue_btn_clicked)
        
        self.scrollarea.signal_resize.connect(self.slot_resize_canvas)
        self.scrollarea.signal_drop_paras.connect(self.slot_plot)
        
        self.combo_box_time.activated.connect(self.slot_display_paravalue_ontime)
        self.tool_btn_time.clicked.connect(self.slot_import_paravalue)
        
        self.combo_box_time_intervals.activated.connect(self.slot_display_tinterval)
        self.tool_btn_time_interval.clicked.connect(self.plotcanvas.slot_sel_function)
        
#        画布的右键菜单
        self.signal_is_display_menu.connect(self.plotcanvas.slot_set_display_menu)
        
        self.plotcanvas.signal_cursor_xdata.connect(self.slot_display_paravalue)
        self.plotcanvas.signal_send_time.connect(self.slot_save_time)
        self.plotcanvas.signal_send_tinterval.connect(self.slot_save_tinterval)

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
        
#    输入参数为一个包含两个参数的元组，元组第一个参数是字典型，存储文件名及与之对应的变量列表
#    元组第二个参数是列表，存储已排序的参数
#    这样定义数据类型的原因是绘图既需要读取数据也需要参数排列顺序
    def slot_plot(self, datadict_and_paralist : tuple):
        
        datadict, sorted_paras = datadict_and_paralist
        if datadict and sorted_paras:
            self.plotcanvas.subplot_para_wxl(datadict, sorted_paras)
            self.count_axis = self.plotcanvas.count_axes
            if self.count_axis > 4:
                self.scrollarea.setWidgetResizable(False)
#                    乘以1.05是估计的，刚好能放下四张图，
#                    减去的19是滚动条的宽度
                height = int(self.scrollarea.height() * 1.05) / 4
                self.plotcanvas.resize(self.scrollarea.width() - 19,
                                       self.count_axis * height)
#                height = self.count_axis * 180
#                self.plotcanvas.resize(self.scrollarea.width() - 19,
#                                       height)
            else:
                self.scrollarea.setWidgetResizable(True)
            

    def slot_resize_canvas(self, scroll_area_size):
        
        if not self.scrollarea.widgetResizable():
            if scroll_area_size.height() > self.plotcanvas.size().height():
                self.plotcanvas.resize(scroll_area_size)
            else:
                self.plotcanvas.resize(scroll_area_size.width(),
                                       self.plotcanvas.size().height())
    #        设置图四边的空白宽度
            self.plotcanvas.set_subplot_adjust()
        
    def slot_pan(self):
        self.plotcanvas.toolbar.pan()
        
#        完成按钮按下和弹起的效果
        if self.pan_on:
            self.plotcanvas.current_cursor_inaxes = Qt.ArrowCursor
            self.button_pan.setChecked(False)
            self.pan_on = False
#            因为缩放时占用了右键，所以需要禁止右键菜单弹出
            self.signal_is_display_menu.emit(True)
        else:
            self.plotcanvas.current_cursor_inaxes = Qt.SizeAllCursor
            self.button_pan.setChecked(True)
            self.pan_on = True
            self.signal_is_display_menu.emit(False)
#            保证pan按钮和zoom按钮不能同时按下
            if self.zoom_on:
                self.button_zoom.setChecked(False)
                self.zoom_on = False
        
    def slot_zoom(self):
        self.plotcanvas.toolbar.zoom()
        
#        完成按钮按下和弹起的效果
        if self.zoom_on:
            self.plotcanvas.current_cursor_inaxes = Qt.ArrowCursor
            self.button_zoom.setChecked(False)
            self.zoom_on = False
            self.signal_is_display_menu.emit(True)
        else:
            self.plotcanvas.current_cursor_inaxes = Qt.CrossCursor
            self.button_zoom.setChecked(True)
            self.zoom_on = True
            self.signal_is_display_menu.emit(False)
#            保证pan按钮和zoom按钮不能同时按下
            if self.pan_on:
                self.button_pan.setChecked(False)
                self.pan_on = False
        
#    def slot_emit_request_plot_temps(self):
#        
#        self.signal_request_temps.emit('plot_template')
        
#    def slot_sel_temp(self, dict_files, templates):
#
#        if templates:
#            export_paras = {}
#            sorted_paras = []
#            dialog = SelectTemplateDialog(self, templates)
#            return_signal = dialog.exec_()
#            if (return_signal == QDialog.Accepted):
#                if dict_files:
#        #            遍历文件，搜索是否存在模板中的参数
#        #            不同文件下的同一参数都会找出（这样耗时较长）
#        #            也可以找到第一个就停止
#                    for paraname in templates[dialog.sel_temp]:
#                        for file_dir in dict_files:
#                            if paraname in dict_files[file_dir]:
#                                if file_dir in export_paras:
#                                    export_paras[file_dir].append(paraname)
#                                else:
#                                    export_paras[file_dir] = []
#                                    export_paras[file_dir].append(paraname)
#                                sorted_paras.append(paraname)
#        #                        加入以下语句实现找到第一个就停止的功能
#        #                        break
#                    self.slot_plot((export_paras, sorted_paras))
#                else:
#                    QMessageBox.information(self,
#                            QCoreApplication.translate('DataExportWindow', '导入模板错误'),
#                            QCoreApplication.translate('DataExportWindow', '没有发现数据文件'))
#        else:
#            QMessageBox.information(self,
#                    QCoreApplication.translate('DataExportWindow', '导入模板错误'),
#                    QCoreApplication.translate('DataExportWindow', '没有模板')) 
    
#    def slot_save_temp(self):
#        
#        if self.plotcanvas.paralist:
#            temp = {}
#            dialog = SaveTemplateDialog(self)
#            return_signal = dialog.exec_()
#            if (return_signal == QDialog.Accepted):
#                temp_name = dialog.temp_name
#                if temp_name:
#                    temp[temp_name] = self.plotcanvas.paralist[1:]
#                    self.signal_save_temp.emit(temp)
#                else:
#                    QMessageBox.information(self,
#                            QCoreApplication.translate('DataExportWindow', '输入提示'),
#                            QCoreApplication.translate('DataExportWindow', '未输入模板名'))
#        else:
#            QMessageBox.information(self,
#                    QCoreApplication.translate('DataExportWindow', '保存错误'),
#                    QCoreApplication.translate('DataExportWindow', '没有发现图表')) 
        
    def slot_paravalue_btn_clicked(self):
        
        if self.para_value_window.isHidden():
            self.para_value_window.setHidden(False)
            self.plotcanvas.slot_connect_display_paravalue()
        else:
            self.para_value_window.setHidden(True)
            self.plotcanvas.slot_diaconnect_display_paravalue()
            
    def slot_save_time(self):

        self.timestamps.append(self.label_time.text())
        self.combo_box_time.addItem(self.label_time.text())
        self.combo_box_time.setCurrentIndex(self.combo_box_time.count() - 1)
        
    def slot_save_tinterval(self, timeinterval : tuple):
        
        name, stime, etime = timeinterval
        tinterval = name + '(' + stime + ' - ' + etime + ')'
        self.combo_box_time_intervals.addItem(tinterval, name)
        self.combo_box_time_intervals.setCurrentIndex(self.combo_box_time_intervals.count() - 1)
        
    def slot_import_paravalue(self):
        
        dict_paravalue = {}
        paralist = ['TIME']
        for time in self.timestamps:
            dt = datetime.strptime(time, '%H:%M:%S.%f')
            paravalue = self.plotcanvas.get_paravalue(dt)
            for para_tuple in paravalue:
                paraname, value = para_tuple
                if paraname in dict_paravalue:
                    dict_paravalue[paraname].append(value)
                else:
                    dict_paravalue[paraname] = []
                    dict_paravalue[paraname].append(value)
                if not(paraname in paralist):
                    paralist.append(paraname)
            if 'TIME' in dict_paravalue:
                dict_paravalue['TIME'].append(time)
            else:
                dict_paravalue['TIME'] = []
                dict_paravalue['TIME'].append(time)
        if dict_paravalue:
            df = pd.DataFrame(dict_paravalue)
#            按指定顺序放置列
            df = df[paralist]
            file_dir, flag = QFileDialog.getSaveFileName(self, 
                                                         QCoreApplication.translate('PlotWindow', '保存参数值'),
                                                         CONSTANT.SETUP_DIR,
                                                         QCoreApplication.translate('PlotWindow', 'Text Files (*.txt);;CSV Files (*.csv);;Matlab Files (*.mat)'))
            if file_dir:
                if flag == 'Text Files (*.txt)':
                    df.to_csv(file_dir, '\t' , index=False, encoding='utf-8')
                if flag == 'CSV Files (*.csv)':
                    df.to_csv(file_dir, ',' , index=False, encoding='utf-8')
                if flag == 'Matlab Files (*.mat)':
                    sio.savemat(file_dir, df.to_dict('list'))
                QMessageBox.information(self,
                        QCoreApplication.translate('PlotWindow', '保存提示'),
                        QCoreApplication.translate('PlotWindow', '保存成功'))
                                                 
#    显示复选框中选中时刻对应的参数值
    def slot_display_paravalue_ontime(self, index):
        
        str_time = self.combo_box_time.itemText(index)
        if str_time:
            self.label_time.setText(str_time)
            dt = datetime.strptime(str_time, '%H:%M:%S.%f')
            paravalue = self.plotcanvas.get_paravalue(dt)
            count = len(paravalue)
            self.table_widget_value.clearContents()
            self.table_widget_value.setRowCount(count)
            for row, para_tuple in enumerate(paravalue):
                paraname, value = para_tuple
                item1 = QTableWidgetItem(paraname)
                self.table_widget_value.setItem(row, 0, item1)
                item2 = QTableWidgetItem(str(value))
                self.table_widget_value.setItem(row, 1, item2)
                
    def slot_display_tinterval(self, index):
        
        name = self.combo_box_time_intervals.itemData(index)
        self.plotcanvas.slot_set_tlim(name)
            
#    实时显示参数值
    def slot_display_paravalue(self, time : str, paravalue : list):
        
#        显示时间
        self.label_time.setText(time)
        
        count = len(paravalue)
        self.table_widget_value.clearContents()
        self.table_widget_value.setRowCount(count)
        for row, para_tuple in enumerate(paravalue):
            paraname, value = para_tuple
            item1 = QTableWidgetItem(paraname)
            self.table_widget_value.setItem(row, 0, item1)
            item2 = QTableWidgetItem(str(value))
            self.table_widget_value.setItem(row, 1, item2)

    def slot_clear_canvas(self):
        
        if self.count_axis:
            message = QMessageBox.warning(self,
                  QCoreApplication.translate('PlotWindow', '清除画布'),
                  QCoreApplication.translate('PlotWindow', '确定要清除画布吗'),
                  QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.plotcanvas.slot_clear_canvas()
#                如果画的图多会出现滚动条，此时清除画布，滚动条不会消失，因此采用此行解决
                self.scrollarea.setWidgetResizable(True)
                self.count_axis = 0
                self.timestamps = []
                self.plotcanvas.time_intervals = {}
                self.combo_box_time.clear()
                self.combo_box_time_intervals.clear()
                self.label_time.setText('00:00:00.000')
                self.table_widget_value.clearContents()
                self.table_widget_value.setRowCount(0)
        
    def slot_save_figure(self):
        
#        将画布变形成合适的尺寸
        self.scrollarea.setWidgetResizable(False)
#        图注高度
        legend_h = 18
#        坐标高度
        axis_h = 100
#        画布尺寸
        h = self.count_axis * (axis_h + legend_h) + legend_h
        w = 650
        left_gap = round(50 / w, 2)
        bottom_gap = round(legend_h * 1.2 / h, 2)
        right_gap = round((w - 10) / w, 2)
        top_gap = round((h - legend_h) / h, 2)
        hs = round(legend_h / (axis_h + legend_h), 2)
        self.plotcanvas.resize(w, h)
        self.plotcanvas.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
                                            right=right_gap,top=top_gap,hspace=hs)
#        保存变形后的画布
        self.plotcanvas.toolbar.save_figure()
        
#        将画布还原回查看状态下的尺寸
        if self.count_axis > 4:
            self.scrollarea.setWidgetResizable(False)
            height = int(self.scrollarea.height() * 1.05) / 4
            self.plotcanvas.resize(self.scrollarea.width() - 19,
                                   self.count_axis * height)
#            height = self.count_axis * 180
#            self.plotcanvas.resize(self.scrollarea.width() - 19,
#                                   height)
        else:
            self.scrollarea.setWidgetResizable(True)
        self.plotcanvas.set_subplot_adjust()
# =============================================================================
# 功能函数模块
# =============================================================================
                
    
    
# =============================================================================
# 汉化
# =============================================================================
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('PlotWindow', 'Plot'))
        self.button_home.setToolTip(_translate('PlotWindow', '初始状态'))
        self.button_pan.setToolTip(_translate('PlotWindow', '移动与缩放'))
        self.button_zoom.setToolTip(_translate('PlotWindow', '框选缩放'))
#        self.button_plot_setting.setToolTip(_translate('PlotWindow', '绘图设置'))
#        self.button_config.setToolTip(_translate('PlotWindow', '画布设置'))
#        self.button_edit.setToolTip(_translate('PlotWindow', '图表设置'))
        self.button_forward.setToolTip(_translate('PlotWindow', '前进'))
        self.button_back.setToolTip(_translate('PlotWindow', '后退'))
        self.button_save.setToolTip(_translate('PlotWindow', '保存'))
#        self.button_save_temp.setToolTip(_translate('PlotWindow', '保存模板'))
#        self.button_sel_temp.setToolTip(_translate('PlotWindow', '选择模板'))
        self.button_clear_canvas.setToolTip(_translate('PlotWindow', '清空画布'))
        self.button_get_paravalue.setToolTip(_translate('PlotWindow', '取参数值'))
        
        self.group_box_time_interval.setTitle(_translate('PlotWindow', '时间查看器'))
        self.tool_btn_time_interval.setText(_translate('PlotWindow', '...'))
        self.tool_btn_time.setText(_translate('PlotWindow', '...'))
        self.group_box_time.setTitle(_translate('PlotWindow', '参数值'))
        self.label_time.setText(_translate('PlotWindow', '00:00:00.000'))
        item = self.table_widget_value.horizontalHeaderItem(0)
        item.setText(_translate('PlotWindow', '参数名'))
        item = self.table_widget_value.horizontalHeaderItem(1)
        item.setText(_translate('PlotWindow', '参数值'))
