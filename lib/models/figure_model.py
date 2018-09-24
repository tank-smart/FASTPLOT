 # -*- coding: utf-8 -*-
# =============================================================================
# =======概述
# 文件名：figure_model.py
# 简述：绘图类
#
# =======内容
# 包含类：
# class PlotCanvas(FigureCanvas):
#
# =======使用说明
# 参考类的使用说明
#
# =======日志

# =======备注

# =============================================================================

# =======imports
import sys
sys.path.append(r'D:\Program Files\git\DAGUI\lib')

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#------王--改动开始
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
from PyQt5.QtCore import pyqtSignal, QCoreApplication, QPoint, Qt
import views.config_info as CONFIG
from views.custom_dialog import (LineSettingDialog, AnnotationSettingDialog,
                                 AxisSettingDialog, FigureCanvasSetiingDialog,
                                 ParameterExportDialog, SelFunctionDialog,
                                 FileProcessDialog)
import models.time_model as Time_Model
from models.data_model import DataFactory
from PyQt5.QtGui import QIcon
import scipy.io as sio
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
#------王--改动结束
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
from matplotlib.ticker import FuncFormatter, AutoMinorLocator, MaxNLocator, LinearLocator, FixedLocator
import pandas as pd
from models.datafile_model import Normal_DataFile
from PyQt5.QtWidgets import (QSizePolicy, QMenu, QAction, QMessageBox, QDialog,
                             QInputDialog, QLineEdit, QFileDialog)
# =======类基本信息
#class PlotCanvas
#说明：绘图类，继承自FigureCanvas
#功能：完成绘图相关功能
# =====properties：

# =====functions:
#my_format(self, x, pos=None):自定义时间轴的显示格式
#plot_para(self,source=None,para_list=[]):绘图函数，将para_list参数列表中额参数读入
#并在PlotCanvas画出；可接受的数据源source包括参数的文件路径或参数dataframe
#add_toolbar(self,parent=None)：增加绘图工具
#show_toolbar(self,toolbar)：显示qt NavigationTool
#hide_toolbar(self,toolbar)：隐藏qt NavigationTool
# =======使用说明
# 实例化类

class PlotCanvas(FigureCanvas):

#------王--改动开始
    signal_cursor_xdata = pyqtSignal(str, list)
    signal_send_time = pyqtSignal()
    signal_send_tinterval = pyqtSignal(tuple)
    signal_get_data_dict = pyqtSignal()

#------王--改动结束
    
    def __init__(self,parent=None,width=10,height=4,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=dpi)
        #self.fig=plt.figure()
#        self.poslist=[[0.1, 0.77, 0.8, 0.18],[0.1, 0.53, 0.8, 0.18],[0.1, 0.29, 0.8, 0.18],[0.1, 0.05, 0.8, 0.18]]
        #self.poslist=[[0.1,0.75,0.8,0.23],[0.1,0.5,0.8,0.23],[0.1,0.25,0.8,0.23],[0.1,0,0.8,0.23]]
#        self.pos=0
        #self.axes = fig.add_subplot(111)# 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        #self.axes = fig.add_axes([0,0,1,1])
        FigureCanvas.__init__(self, self.fig)# 初始化父类
        self.setParent(parent)
 
#        FigureCanvas.setSizePolicy(self,
#                QSizePolicy.Expanding,
#                QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#        self.toolbar=self.add_toolbar()
        self.toolbar=CustomToolbar(self,parent=None)
        self.toolbar.hide()
#------王--改动开始

#        Times New Roman字体的斜体
#        self.font_timesi = matplotlib.font_manager.FontProperties(
#                fname = CONFIG.SETUP_DIR + r'\data\fonts\timesi.ttf')
#        Times New Roman字体
#        self.font_times = matplotlib.font_manager.FontProperties(
#                fname = CONFIG.SETUP_DIR + r'\data\fonts\times.ttf')
#        微软雅黑
#        self.font_msyh = matplotlib.font_manager.FontProperties(
#                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf')
#        当前的数据字典
        self._data_dict = {}
        
#        画图风格是单坐标还是多坐标
        self.fig_style = None
#        存储曲线颜色
        prop_cycle = plt.rcParams['axes.prop_cycle']
#        默认的是十种颜色
        self.curve_colors = prop_cycle.by_key()['color']
        self.color_index = 0
#        默认字体大小
#        self.default_fontsize = 8
#        存储参数数据
        self.total_data = {}
        self.time_series_list = {}
        self.count_created_data = 0
        self.sorted_paralist = []
        self.count_axes = 0
#        定义下面这个变量是为了存入模板
        self.paralist = []
#        时间段
        self.time_intervals = {}
        
#        当前鼠标在坐标内的光标样式
        self.current_cursor_inaxes = None
#        当前鼠标所在的坐标
        self.current_axes = None

#        单击右键选到要删除的文字标注或标记线
        self.picked_del_artist = None
        
        self.axis_menu_on = None
        
        self.current_markline_color = 'red'
        self.current_markline_style = '-'
        
        self.cid_press_new_hline = None
        self.cid_press_new_vline = None
        self.cid_move_new_line = None
        self.cid_release_new_line = None
        self.newline = None
        
        self.show_hgrid = True
        self.show_vgrid = True
        
#        定义文字标注的默认属性
        self.current_text_color = 'black'
        self.current_text_size = 10.0
        self.current_text_style = 'normal'
#        记录pick到哪个文字标注
        self.picked_annotation = None
#        记录文字标注移动事件的id
        self.cid_move_annotation = None
        self.cid_release_annotation = None
#        记录pick时文字的位置和鼠标位置，格式(x,y,mx,my)
        self.annotation_init_loc = None
        self.cid_press_new_annotation = None
        
        self.cid_display_paravalue = None
        self.is_save_paravalue = False
        
#        添加右键菜单
        self.is_display_menu = True

        self.action_show_hgrid = QAction(self)
        self.action_show_hgrid.setCheckable(True)
        self.action_show_hgrid.setChecked(True)
        self.action_show_hgrid.setText(QCoreApplication.
                                       translate('PlotCanvas', '显示水平网格线'))
        self.action_show_vgrid = QAction(self)
        self.action_show_vgrid.setCheckable(True)
        self.action_show_vgrid.setChecked(True)
        self.action_show_vgrid.setText(QCoreApplication.
                                       translate('PlotCanvas', '显示垂直网格线'))
        self.action_save_tinterval = QAction(self)
        self.action_save_tinterval.setText(QCoreApplication.
                                           translate('PlotCanvas', '保存时间段'))
        self.action_save_time = QAction(self)
        self.action_save_time.setText(QCoreApplication.
                                      translate('PlotCanvas', '保存时刻'))
        self.action_axis_setting = QAction(self)
        self.action_axis_setting.setText(QCoreApplication.
                                         translate('PlotCanvas', '坐标轴设置'))
        self.action_add_text = QAction(self)
        self.action_add_text.setIcon(QIcon(CONFIG.ICON_TEXT))
        self.action_add_text.setText(QCoreApplication.
                                     translate('PlotCanvas', '添加文字'))
        self.action_add_mark_hline = QAction(self)
        self.action_add_mark_hline.setText(QCoreApplication.
                                           translate('PlotCanvas', '水平标记线'))
        self.action_add_mark_vline = QAction(self)
        self.action_add_mark_vline.setText(QCoreApplication.
                                           translate('PlotCanvas', '垂直标记线'))
        self.action_add_arb_markline = QAction(self)
        self.action_add_arb_markline.setText(QCoreApplication.
                                             translate('PlotCanvas', '任意标记线'))
        self.action_del_artist = QAction(self)
        self.action_del_artist.setText(QCoreApplication.
                                       translate('PlotCanvas', '删除标记'))
        self.action_del_artist.setIcon(QIcon(CONFIG.ICON_DEL))
        self.action_del_axis = QAction(self)
        self.action_del_axis.setText(QCoreApplication.
                                     translate('PlotCanvas', '删除曲线'))
        self.mpl_connect('button_press_event', 
                                         self.slot_on_tree_context_menu)
#        网格显示相关的动作连接
        self.action_show_hgrid.triggered.connect(self.slot_show_hgrid)
        self.action_show_vgrid.triggered.connect(self.slot_show_vgrid)
        
        self.action_axis_setting.triggered.connect(self.slot_axis_setting)
        
#        标注线相关的动作连接
        self.action_add_arb_markline.triggered.connect(self.slot_add_arb_markline)
        self.action_add_mark_hline.triggered.connect(self.slot_add_mark_hline)
        self.action_add_mark_vline.triggered.connect(self.slot_add_mark_vline)
        self.action_del_artist.triggered.connect(self.slot_del_artist)
#        文字相关的动作连接
        self.action_add_text.triggered.connect(self.slot_add_annotation)
        
        self.action_save_time.triggered.connect(self.slot_save_time)
        self.action_save_tinterval.triggered.connect(self.slot_save_tinterval)
        
        self.action_del_axis.triggered.connect(self.slot_del_axis)

        self.mpl_connect('motion_notify_event', self.slot_set_cursor)
        
#        Pick事件在进行缩放移动、框选缩放时不会触发，但是press事件却会触发，不知道为何
        self.mpl_connect('pick_event', self.on_pick)
        
    def slot_set_display_menu(self, is_display):

        self.is_display_menu = is_display
        
    def slot_on_tree_context_menu(self, event):
        
#        禁止缩放过程中弹出右键菜单
        if self.fig.axes and event.button == 3 and self.is_display_menu:
#            只要弹出了右键菜单，就把所有连接都断开
            self.slot_disconnect()
            menu = QMenu(self)
            menu.addActions([self.action_show_hgrid, 
                             self.action_show_vgrid,
                             self.action_save_tinterval,
                             self.action_save_time,
                             self.action_axis_setting,
                             self.action_add_text])
            menu_markline = QMenu(menu)
            menu_markline.setIcon(QIcon(CONFIG.ICON_ADD_LINE_MARK))
            menu_markline.setTitle(QCoreApplication.
                                  translate('PlotCanvas', '添加标记线'))
            menu_markline.addActions([self.action_add_mark_hline,
                                    self.action_add_mark_vline,
                                    self.action_add_arb_markline])
            menu.addAction(menu_markline.menuAction())
            menu.addAction(self.action_del_artist)
#            menu.addAction(self.action_del_axis)
            if event.inaxes:
                self.axis_menu_on = event.inaxes
                self.action_axis_setting.setEnabled(True)
                self.action_save_tinterval.setEnabled(True)
            else:
                self.action_axis_setting.setEnabled(False)
                self.action_save_tinterval.setEnabled(False)
                
            if self.is_save_paravalue and event.inaxes:
                self.action_save_time.setEnabled(True)
            else:
                self.action_save_time.setEnabled(False)
            if self.picked_del_artist:
                self.action_del_artist.setEnabled(True)
            else:
                self.action_del_artist.setEnabled(False)
            h = self.height()
            cor_y = h - event.y
            menu.exec_(self.mapToGlobal(QPoint(event.x, cor_y)))
#            无论是否触发删除事件，都将将选中的artist清空
            self.picked_del_artist = None
            self.axis_menu_on = None

#    pick函数
    def on_pick(self, event):
        
#        判断是否是双击
        if not event.mouseevent.dblclick:
            if event.mouseevent.button == 1:
                if type(event.artist) == Annotation:
                    self.picked_annotation = event.artist
                    self.setCursor(Qt.ClosedHandCursor)
                    self.current_cursor_inaxes = Qt.ClosedHandCursor
                    self.cid_move_annotation = self.mpl_connect('motion_notify_event',
                                                                self.slot_move_annotation)
                    self.cid_release_annotation = self.mpl_connect('button_release_event',
                                                                   self.slot_release_annotation)
                    self.annotation_init_loc = (self.picked_annotation.get_position() + 
                                                (event.mouseevent.xdata, event.mouseevent.ydata))
            if event.mouseevent.button == 3:
                if (type(event.artist) == Line2D or type(event.artist) == Annotation):
                    self.picked_del_artist = event.artist

        else:
            if type(event.artist) == Line2D:
                line = event.artist
                dialog = LineSettingDialog(self, line)
                return_signal = dialog.exec_()
                if (return_signal == QDialog.Accepted):
                    self.current_markline_color = dialog.line_color
                    self.current_markline_style = dialog.line_ls
#                    只更新Artist
#                    event.mouseevent.inaxes.draw_artist(line)
#                    更新所有对象
                    event.canvas.draw()
                    
            if type(event.artist) == Annotation:
                annotation = event.artist
                dialog = AnnotationSettingDialog(self, annotation)
                return_signal = dialog.exec_()
                if (return_signal == QDialog.Accepted):
                    self.current_text_color = dialog.text_color
                    self.current_text_size = dialog.text_size
                    self.current_text_style = dialog.text_style
#                    当设置文字方向时没法更新
#                    event.mouseevent.inaxes.draw_artist(annotation)
                    event.canvas.draw()

#    网格显示函数    
    def slot_show_hgrid(self):
        
        if self.show_hgrid:
            list_axis = self.fig.axes
            for axis in list_axis:
                axis.grid(False, which = 'both', axis = 'y')
            self.show_hgrid = False
        else:
            list_axis = self.fig.axes
            for axis in list_axis:
                axis.grid(True, which = 'both', axis = 'y')
            self.show_hgrid = True
        self.draw()
            
    def slot_show_vgrid(self):
        
        if self.show_vgrid:
            list_axis = self.fig.axes
            for axis in list_axis:
                axis.grid(False, which = 'both', axis = 'x')
            self.show_vgrid = False
        else:
            list_axis = self.fig.axes
            for axis in list_axis:
                axis.grid(True, which = 'both', axis = 'x')
            self.show_vgrid = True
        self.draw()
        
    def slot_axis_setting(self):
        
        dialog = AxisSettingDialog(self, self.axis_menu_on)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            pass
#        self.axis_menu_on.remove()
            self.draw()

#    标注线函数
    def slot_add_arb_markline(self):

        self.setCursor(Qt.CrossCursor)
        self.current_cursor_inaxes = Qt.CrossCursor
        self.cid_move_new_line = self.mpl_connect('motion_notify_event',
                                                  self.slot_onmove_newline)
        self.cid_release_new_line = self.mpl_connect('button_release_event',
                                                     self.slot_release_newline)
        
    def slot_onmove_newline(self, event):
        
        if event.inaxes and event.button == 1:
            if self.newline:
                x = self.newline.get_xdata()
                x[1] = event.xdata
                y = self.newline.get_ydata()
                y[1] = event.ydata
                self.newline.set_xdata(x)
                self.newline.set_ydata(y)
                self.draw()
            else:
                self.newline = self.current_axes.add_line(Line2D([event.xdata, event.xdata],
                                                                [event.ydata, event.ydata],
                                                                c = self.current_markline_color,
                                                                ls = self.current_markline_style,
                                                                picker = 5))
                
    def slot_release_newline(self, event):
        
        if event.button == 1:
            self.slot_disconnect()
    
    def slot_add_mark_hline(self):

        self.setCursor(Qt.SizeHorCursor)
        self.current_cursor_inaxes = Qt.SizeHorCursor
        self.cid_press_new_hline = self.mpl_connect('button_press_event',
                                                 self.slot_onpress_new_hline)
        
    def slot_onpress_new_hline(self, event):

        if event.inaxes and event.button == 1:
#            鼠标左键按下才生效，但鼠标右键会弹出右键菜单，此时左键选中一个动作后
#            再次按下右键又会执行下列语句，这是不合适的。因此在右键激活时也断开连接,
#            这在菜单函数里实现
            self.current_axes.axhline(event.ydata, c = self.current_markline_color,
                                     ls = self.current_markline_style, picker = 5)
            self.draw()
#            动作已完成，断开信号与槽的连接，后边相同
        if event.button == 1:
            self.slot_disconnect()
        
    def slot_add_mark_vline(self):

        self.setCursor(Qt.SizeVerCursor)
        self.current_cursor_inaxes = Qt.SizeVerCursor
        self.cid_press_new_vline = self.mpl_connect('button_press_event',
                                                 self.slot_onpress_new_vline)
        
    def slot_onpress_new_vline(self, event):

        if event.inaxes and event.button == 1:
            self.current_axes.axvline(event.xdata, c = self.current_markline_color,
                                     ls = self.current_markline_style, picker = 5)
            self.draw()
        if event.button == 1:
            self.slot_disconnect()
        
    def slot_del_artist(self):

        message = QMessageBox.warning(self,
                      QCoreApplication.translate('PlotCanvas', '删除标记'),
                      QCoreApplication.translate('PlotCanvas',
                                        '''<p>确定要删除吗？'''),
                      QMessageBox.Yes | QMessageBox.No)
        if (message == QMessageBox.Yes):
            self.picked_del_artist.remove()
            self.draw()
            
    def slot_del_axis(self):
        
        self.current_axes.remove()
        self.draw()

#    文字标注函数     
    def slot_add_annotation(self):
        
        self.setCursor(Qt.IBeamCursor)
        self.current_cursor_inaxes = Qt.IBeamCursor
        self.cid_press_new_annotation = self.mpl_connect('button_press_event',
                                                         self.slot_press_new_annotation)
        
    def slot_press_new_annotation(self, event):
        
        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        if event.inaxes and event.button == 1:
#            此处的字体大小size会覆盖fontproperties中size的属性
            self.current_axes.annotate(s = r'Text', 
                                      xy = (event.xdata, event.ydata),
                                      color = self.current_text_color,
                                      style = self.current_text_style,
                                      size = self.current_text_size,
                                      picker = 1,
                                      fontproperties = font)
            self.draw()
        if event.button == 1:
            self.slot_disconnect()
        
    def slot_move_annotation(self, event):
        
        if event.inaxes and event.button == 1:
            x0, y0, mx0, my0 = self.annotation_init_loc
            dx = event.xdata - mx0
            dy = event.ydata - my0
            self.picked_annotation.set_position((x0 + dx, y0 + dy))
            self.draw()
            
    def slot_release_annotation(self, event):
         
        if event.button == 1:
            self.slot_disconnect()

    def slot_set_cursor(self, event):
        
#        当鼠标在坐标轴内保持当前特定的光标状态，否则为箭头
        if event.inaxes and self.current_cursor_inaxes:
            self.setCursor(self.current_cursor_inaxes)
        else:
            self.setCursor(Qt.ArrowCursor)
#         获得鼠标所在坐标轴
        if event.inaxes:
            self.current_axes = event.inaxes
            
#    右键菜单时调用；相应动作完成也调用
    def slot_disconnect(self):

#        这个鼠标设置会在缩放时改变鼠标样式，因为绑定了鼠标释放事件
        self.setCursor(Qt.ArrowCursor)
        self.current_cursor_inaxes = Qt.ArrowCursor
#        移动artist是已鼠标释放作为结束标志
        if self.cid_move_annotation and self.cid_release_annotation:
            self.mpl_disconnect(self.cid_move_annotation)
            self.mpl_disconnect(self.cid_release_annotation)
            self.cid_release_annotation = None
            self.cid_move_annotation = None
            
        if self.cid_move_new_line and self.cid_release_new_line:
            self.mpl_disconnect(self.cid_move_new_line)
            self.mpl_disconnect(self.cid_release_new_line)
            self.cid_release_new_line = None
            self.cid_move_new_line = None
            self.newline = None
#        添加标注是已鼠标按下作为结束标志
        if self.cid_press_new_hline:
            self.mpl_disconnect(self.cid_press_new_hline)
            self.cid_press_new_hline = None

        if self.cid_press_new_vline:
            self.mpl_disconnect(self.cid_press_new_vline)
            self.cid_press_new_vline = None

        if self.cid_press_new_annotation:
            self.mpl_disconnect(self.cid_press_new_annotation)
            self.cid_press_new_annotation = None
            
    def slot_clear_canvas(self):
        
        self.fig.clf()
        self.draw()
        self.total_data = {}
        self.sorted_paralist = []
        self.time_series_list = {}
        self.color_index = 0
        
    def slot_plot_setting(self):
        
#        如果有图才弹出设置窗口
        if self.fig.axes:
            dialog = FigureCanvasSetiingDialog(self, self.fig.axes)
            rs = dialog.exec_()
            if rs == QDialog.Accepted:
                self.draw()
                
    def slot_connect_display_paravalue(self):
        
        self.is_save_paravalue = True
        self.cid_display_paravalue = self.mpl_connect('motion_notify_event',
                                                      self.slot_display_paravalue)
    
    def slot_diaconnect_display_paravalue(self):
        
        self.is_save_paravalue = False
        self.mpl_disconnect(self.cid_display_paravalue)
        
    def slot_save_time(self):
        
        self.signal_send_time.emit()
        
    def slot_save_tinterval(self):
        
        ti_name = 'Interval0'
        i = 1
        while ti_name in self.time_intervals:
            ti_name = 'Interval' + str(i)
            i += 1
        name, ok = QInputDialog.getText(self,
                                        QCoreApplication.translate('PlotCanvas', '命名时间段'),
                                        QCoreApplication.translate('PlotCanvas', '时间段名'),
                                        QLineEdit.Normal,
                                        ti_name)
        
        if (ok and name):
            axes = self.fig.axes
            if axes:
                axis = axes[0]
                st,et = axis.get_xlim()
                stime = mdates.num2date(st).time().isoformat(timespec='milliseconds')
                etime = mdates.num2date(et).time().isoformat(timespec='milliseconds')
                self.time_intervals[name] = (stime, etime)
                self.signal_send_tinterval.emit((name, stime, etime))
        
    def slot_display_paravalue(self, event):
        
        if event.inaxes:
            time = mdates.num2date(event.xdata).time().isoformat(timespec='milliseconds')
            datatime_sel = mdates.num2date(event.xdata)
            self.signal_cursor_xdata.emit(time, self.get_paravalue(datatime_sel))
                
    def slot_set_tlim(self, name):
        
        axes = self.fig.axes
        stime, etime = self.time_intervals[name]
        if axes:
            st = mdates.date2num(Time_Model.str_to_datetime(stime))
            et = mdates.date2num(Time_Model.str_to_datetime(etime))
            axis = axes[0]
            axis.set_xlim(st, et)
            for ax in axes:
                ax.autoscale(axis = 'y')
            self.draw()    
                    
    def slot_sel_function(self, cur_files):
        
        if self.time_intervals:
            dialog = SelFunctionDialog(self)
            return_signal = dialog.exec_()
            if return_signal == QDialog.Accepted:
                index = dialog.index
                try:
                    if index == 0:
                        self.slot_export_tinterval_data_fig()
                    elif index == 1:
                        self.slot_export_tinterval_data_file(cur_files)
                    elif index == 2:
                        self.slot_export_tinterval_data_aggregate('mean')
                    elif index == 3:
                        self.slot_export_tinterval_data_aggregate('max')
                    elif index == 4:
                        self.slot_export_tinterval_data_aggregate('min')
                    else:
                        pass
                except:
                    QMessageBox.information(self,
                            QCoreApplication.translate('PlotCanvas', '保存提示'),
                            QCoreApplication.translate('PlotCanvas', '出现错误！'))

    def slot_export_tinterval_data_fig(self):
        
        if self.time_intervals:
            data_container = {}
            for i, data_factory in enumerate(self.total_data):
                for j, tname in enumerate(self.time_intervals):
                    name = '_PLOTDATA '+ tname + str(i + 1) + str(j + 1)
                    stime, etime = self.time_intervals[tname]
    #                get到的数据是拷贝，注意内存空间和速度
                    data = self.total_data[data_factory].get_trange_data(stime, etime)
                    if not data.empty:
                        data_container[name] = data
            if data_container:
                dialog = ParameterExportDialog(self, data_container)
                return_signal = dialog.exec_()
                if return_signal == QDialog.Accepted:
                    QMessageBox.information(self,
                            QCoreApplication.translate('PlotCanvas', '保存提示'),
                            QCoreApplication.translate('PlotCanvas', '保存成功！'))
    
    def slot_export_tinterval_data_file(self, files):
        
        if self.time_intervals:
            dialog = FileProcessDialog(self, files, self.time_intervals)
            return_signal = dialog.exec_()
            if return_signal == QDialog.Accepted:
                QMessageBox.information(self,
                        QCoreApplication.translate('PlotCanvas', '保存提示'),
                        QCoreApplication.translate('PlotCanvas', '保存成功！'))
                
    def slot_export_tinterval_data_aggregate(self, flag):
        
        if self.time_intervals:
            para_list = ['INTERVAL_NAME']
            for tuple_para in self.sorted_paralist:
                pn, pos = tuple_para
                para_list.append(pn)
            dict_intervals = {}
            dict_intervals['INTERVAL_NAME'] = []
            df_total = None
            for i, data_factory in enumerate(self.total_data):
                list_paravalue = []
                for j, tname in enumerate(self.time_intervals):
                    stime, etime = self.time_intervals[tname]
                    data = self.total_data[data_factory].get_trange_data(stime, etime, [], False)
                    if not data.empty:
                        if flag == 'mean':
                            list_paravalue.append(data.mean())
                        elif flag == 'max':
                            list_paravalue.append(data.max())
                        elif flag == 'min':
                            list_paravalue.append(data.min())
                    if i == 0:
                        dict_intervals['INTERVAL_NAME'].append(tname)
                if i == 0:
                    df_intervals = pd.DataFrame(dict_intervals)
                    df_total = df_intervals
                if list_paravalue:
                    df_paravalue = pd.DataFrame(list_paravalue)
                    if not df_paravalue.empty:
                        df_total = pd.concat([df_total, df_paravalue], axis = 1)

            if not df_total.empty:
                self.import_value(df_total, para_list)
    
# =============================================================================
# 功能函数模块
# =============================================================================
    def import_value(self, value, paralist):
        
        if not value.empty:
            if type(value) == pd.DataFrame:
                df = value
            if type(value) == dict:
                df = pd.DataFrame(value)
#            按指定顺序放置列
            df = df[paralist]
            file_dir, flag = QFileDialog.getSaveFileName(self, 
                                                         QCoreApplication.translate('PlotCanvas', '保存参数值'),
                                                         CONFIG.SETUP_DIR,
                                                         QCoreApplication.translate('PlotCanvas', 'Text Files (*.txt);;CSV Files (*.csv);;Matlab Files (*.mat)'))
            if file_dir:
                if flag == 'Text Files (*.txt)':
                    df.to_csv(file_dir, '\t' , index=False, encoding='utf-8')
                if flag == 'CSV Files (*.csv)':
                    df.to_csv(file_dir, ',' , index=False, encoding='utf-8')
                if flag == 'Matlab Files (*.mat)':
                    sio.savemat(file_dir, df.to_dict('list'))
                QMessageBox.information(self,
                        QCoreApplication.translate('PlotCanvas', '保存提示'),
                        QCoreApplication.translate('PlotCanvas', '保存成功！'))
    
    def my_format(self, x, pos=None):
        x = matplotlib.dates.num2date(x)
#        fmt = '%H:%M:%S.%f' 
#        label = x.strftime(fmt)
#        label = label[0:-3]
#        return label
        return Time_Model.datetime_to_timestr(x)

#    datadict中的参数和sorted_paras中的参数个数是一致的，这在输入时就保证了
    def process_data(self, datadict, sorted_paras):
        
        if datadict:
            dict_data_project = {}
            for datasource in datadict:
                data = datadict[datasource]
                if type(data) == list:
#                    此时datasource是文件路径，data是参数列表
                    data_factory = DataFactory(datasource, data)
                elif type(data) == pd.DataFrame:
                    data_factory = DataFactory(data)
                elif type(data) == DataFactory:
                    data_factory = data
                else:
                    data_factory = None
                if data_factory:
                    get_same_time_df = False
                    for index_df in self.total_data:
                        if self.total_data[index_df].is_extended_by(data_factory):
                            get_same_time_df = True
                            dict_data_project[datasource] = index_df
                            self.total_data[index_df].extend_data(data_factory)
                            break
                    if not get_same_time_df:
                        data_label = '_figure_data_' + str(self.count_created_data)
                        dict_data_project[datasource] = data_label
#                        total_data里存的就是当前绘图的参数数据，没有多余参数
                        self.total_data[data_label] = data_factory
#                        把时间列读出来
                        self.time_series_list[data_label] = pd.to_datetime(data_factory.data.iloc[:, 0],
                                                                           format='%H:%M:%S:%f')
                        self.count_created_data += 1

            exit_paras = []
            for index_para in sorted_paras:
                pn, sr = index_para
                new_sr = dict_data_project[sr]
                get_same_para = False
                for index_sp in self.sorted_paralist:
                    spn, sp_sr = index_sp
                    if (pn == spn) and (new_sr == sp_sr):
                        get_same_para = True
                        break
                if not get_same_para:
                    self.sorted_paralist.append((pn, new_sr))
                else:
                    exit_paras.append(pn)
            
            self.paralist = self.sorted_paralist
                    
            if exit_paras:
                print_para = '以下参数已存在：'
                for pa in exit_paras:
                    print_para += ('<br>' + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate('PlotCanvas', '绘图提示'),
                        QCoreApplication.translate('PlotCanvas', print_para))
#            如果要绘制的参数都在，则不执行画图函数
            if len(exit_paras) == len(sorted_paras):
                return False
            else:
                return True
            
    def get_paravalue(self, dt):
        
        paravalue = []
        for para_tuple in self.sorted_paralist:
            paraname, index= para_tuple
            pv = self.total_data[index].get_time_paravalue(dt, paraname)
#            这样做会在数据字典很大时暴露出卡顿的问题
            if (self._data_dict and 
                CONFIG.OPTION['data dict scope plot'] and
                paraname in self._data_dict):
                pn = self._data_dict[paraname][0]
                if pn != 'NaN':
                    paraname = pn
            if pv != None:
                paravalue.append((paraname, pv))
            else:
                paravalue.append((paraname, 'NaN'))
        return paravalue
        
    def plot_paras(self, datalist, sorted_paras):
        
        if self.fig_style == 'mult_axis':
            self.subplot_para_wxl(datalist, sorted_paras)
        if self.fig_style == 'sin_axis':
            self.an_plot_paras(datalist, sorted_paras)
        if self.fig_style == 'stack_axis':
            self.plot_stack_paras(datalist, sorted_paras)
    
    def subplot_para_wxl(self, datalist, sorted_paras):

        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
            self.fig.clf()
            self.count_axes = 0
            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
            matplotlib.rcParams['ytick.direction'] = 'in'
#            支持中文显示
#            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['axes.unicode_minus'] = False
            
            count = len(self.sorted_paralist)
    
            axeslist = []
            self.color_index = 0
            for i, para_tuple in enumerate(self.sorted_paralist):
                paraname, index = para_tuple
                ax = None
                if i == 0:
                    ax = self.fig.add_subplot(count, 1, 1)
                else:
                    ax = self.fig.add_subplot(count, 1, i+1, sharex = axeslist[0])
                axeslist.append(ax)
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope plot'] and
                    paraname in self._data_dict):
                    pn = self._data_dict[paraname][0]
                    unit = self._data_dict[paraname][1]
                    if pn != 'NaN':
                        if unit != 'NaN' and unit != '1':
                            pn = pn + '(' + unit + ')'
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                label = pn,
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                    else:
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                else:
                    ax.plot(self.time_series_list[index], 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1)
                
                if i != (count - 1):
                    plt.setp(ax.get_xticklabels(), visible = False)
                else:
                    ax.set_xlabel('时间', fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
#                    若已指定fontproperties属性，则fontsize不起作用
                    plt.setp(ax.get_xticklabels(),
                             horizontalalignment = 'center',
                             rotation = 'horizontal',
                             fontproperties = CONFIG.FONT_MSYH)
#                    ax.set_xlabel('Time', fontproperties = self.font_times)
                plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
#                ax.legend(fontsize = self.default_fontsize,
#                          loc=(0,1), ncol=1, frameon=False, borderpad = 0.15,
#                          prop = CONFIG.FONT_MSYH)
                ax.legend(loc=(0,1), ncol=1, frameon=False, borderpad = 0.15,
                          prop = CONFIG.FONT_MSYH)
                ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
                ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
                ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
                ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
                ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
                ax.grid(which='major',linestyle='--',color = '0.45')
                ax.grid(which='minor',linestyle='--',color = '0.75')
    #                一共有十种颜色可用
                if self.color_index == 9:
                    self.color_index = 0
                else:
                    self.color_index += 1
                self.count_axes += 1
                
            self.set_subplot_adjust()
#        Easter Egg
#        if count >= 12:
#            QMessageBox.information(self,
#                                    QCoreApplication.translate('PlotCanvas', 'Easter Egg'),
#                                    QCoreApplication.translate('PlotCanvas', '别再画了，图快画到脚上了！'))

    def plot_stack_paras(self, datalist, sorted_paras):

        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
            self.fig.clf()
            self.count_axes = 1
            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
            matplotlib.rcParams['ytick.direction'] = 'in'
#            支持中文显示
#            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['axes.unicode_minus'] = False
            
#            count = len(self.sorted_paralist)
    
            host = self.fig.add_subplot(1, 1, 1)
            plt.setp(host.get_xticklabels(),
                     horizontalalignment = 'center',
                     rotation = 'horizontal',
                     fontproperties = CONFIG.FONT_MSYH)
            plt.setp(host.get_yticklabels(), visible = False)
#            yaxis = host.get_yaxis()
#            ymatl = yaxis.get_majorticklines()
#            for li in ymatl:
#                li.set_visible(False)
#            ymitl = yaxis.get_minorticklines()
#            for li in ymitl:
#                li.set_visible(False)
            host.grid(which='major',linestyle='--',color = '0.45')
            host.grid(which='minor',linestyle='--',color = '0.75')
            host.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            host.xaxis.set_major_locator(MaxNLocator(nbins=6))
            host.xaxis.set_minor_locator(AutoMinorLocator(n=2))
            host.yaxis.set_major_locator(LinearLocator(numticks=21))
            plt.setp(host.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
            
            axeslist = []
            axeslist.append(host)
            self.color_index = 0
            for i, para_tuple in enumerate(reversed(self.sorted_paralist)):
                paraname, index = para_tuple
#                if axeslist:
                ax = host.twinx()
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope plot'] and
                    paraname in self._data_dict):
                    pn = self._data_dict[paraname][0]
                    unit = self._data_dict[paraname][1]
                    if pn != 'NaN':
                        if unit != 'NaN' and unit != '1':
                            pn = pn + '(' + unit + ')'
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                label = pn,
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                        ax.set_ylabel(pn, fontproperties = CONFIG.FONT_MSYH,
                                      color = self.curve_colors[self.color_index])
                    else:
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                        ax.set_ylabel(pn, fontproperties = CONFIG.FONT_MSYH, 
                                      color = self.curve_colors[self.color_index])
                else:
                    ax.plot(self.time_series_list[index], 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1)
                    ax.set_ylabel(paraname, fontproperties = CONFIG.FONT_MSYH, 
                                  color = self.curve_colors[self.color_index])
                
                axeslist.append(ax)
                    
                ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
                ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
                ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
#                ax.yaxis.set_major_locator(LinearLocator(numticks=21))
                ax.tick_params(axis='y', colors=self.curve_colors[self.color_index])
                plt.setp(ax.get_xticklabels(), visible = False)
                ax.yaxis.tick_left()
                ax.yaxis.set_label_position('left')
                ax.spines['left'].set_color(self.curve_colors[self.color_index])
                llimit, ulimit = ax.get_ylim()
#                delta = (ulimit - llimit) / 4
                new_delta = self.num_adjust((ulimit - llimit) / 2)
                mid = int((llimit + ulimit) / 2 / new_delta) * new_delta
                lb = mid - new_delta
                ub = mid + new_delta
#                lb = llimit +  3 * i * delta
#                ub = lb + 4 * delta
                if i % 2 == 1:
                    ax.spines['left'].set_position(('axes', -0.12))
                else:
                    ax.spines['left'].set_position(('axes', -0.03))
                ax.set_yticks([lb,(lb + ub) / 2, ub])
                ax.spines['left'].set_bounds(lb, ub)
                ax.set_ylabel(ax.get_ylabel(), y = (3 * i + 2) / 20)
                ax.set_ylim(lb - 3 * i * new_delta / 2, ub + (16 - 3 * i) * new_delta / 2)
                plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
#                else:
#                    ax = host
##                    ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
##                    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
##                    ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
#                    plt.setp(ax.get_xticklabels(),
#                             horizontalalignment = 'center',
#                             rotation = 'horizontal',
#                             fontproperties = CONFIG.FONT_MSYH)
#                    ax.grid(which='major',linestyle='--',color = '0.45')
#                    ax.grid(which='minor',linestyle='--',color = '0.75')
                
#                if i != (count - 1):
#                    plt.setp(ax.get_xticklabels(), visible = False)
#                    xaxis = ax.get_xaxis()
#                    xmatl = xaxis.get_majorticklines()
#                    for li in xmatl:
#                        li.set_visible(False)
#                    xmitl = xaxis.get_minorticklines()
#                    for li in xmitl:
#                        li.set_visible(False)
#                else:
#                    ax.set_xlabel('时间', fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
##                    若已指定fontproperties属性，则fontsize不起作用
#                    plt.setp(ax.get_xticklabels(),
#                             horizontalalignment = 'center',
#                             rotation = 'horizontal',
#                             fontproperties = CONFIG.FONT_MSYH)
##                    ax.set_xlabel('Time', fontproperties = self.font_times)
#                if i % 2 == 0:
#                    ax.spines['left'].set_position(('axes', -0.05))
#                if i !=0:
#                    ax.spines['top'].set_visible(False)
#                    ax.tick_params()
#                plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
#                ax.tick_params(axis='y', colors=self.curve_colors[self.color_index])
#                ax.spines['left'].set_color(self.curve_colors[self.color_index])
#                ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
#                ax.grid(which='major',linestyle='--',color = '0.45')
#                ax.grid(which='minor',linestyle='--',color = '0.75')
    #                一共有十种颜色可用
                if self.color_index == 9:
                    self.color_index = 0
                else:
                    self.color_index += 1
                
            self.fig.subplots_adjust(left = 0.21, right = 0.95, top = 0.95, bottom = 0.05)
            self.draw()
    
    def an_plot_paras(self, datalist, sorted_paras):

        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
            self.fig.clf()
            self.count_axes = 1
            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
            matplotlib.rcParams['ytick.direction'] = 'in'
#            支持中文显示
#            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['axes.unicode_minus'] = False
            
            ax = self.fig.add_subplot(1, 1, 1)
    
            self.color_index = 0
            for i, para_tuple in enumerate(self.sorted_paralist):
                paraname, index = para_tuple
                if paraname in self._data_dict:
                    pn = self._data_dict[paraname][0]
                    unit = self._data_dict[paraname][1]
                    if pn != 'NaN':
                        if unit != 'NaN' and unit != '1':
                            pn = pn + '(' + unit + ')'
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                label = pn,
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                    else:
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                else:
                    ax.plot(self.time_series_list[index], 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1)
#                一共有十种颜色可用
                if self.color_index == 9:
                    self.color_index = 0
                else:
                    self.color_index += 1
            
            ax.set_xlabel('时间', fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
#            若已指定fontproperties属性，则fontsize不起作用
            plt.setp(ax.get_xticklabels(),
                     horizontalalignment = 'center',
                     rotation = 'horizontal',
                     fontproperties = CONFIG.FONT_MSYH)
            plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
            ax.legend(loc=(0,1), ncol=4, frameon=False, borderpad = 0.15,
                      prop = CONFIG.FONT_MSYH)
            ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.grid(which='major',linestyle='--',color = '0.45')
            ax.grid(which='minor',linestyle='--',color = '0.75')
                
            self.set_subplot_adjust()
            
#    def research(self):
#        
#        def make_patch_spines_invisible(ax):
#            ax.set_frame_on(True)
#            ax.patch.set_visible(False)
#            for sp in ax.spines.values():
#                sp.set_visible(False)
#        
#        
#        host = self.fig.add_subplot(1, 1, 1)
#        self.fig.subplots_adjust(right=0.75)
#        
#        par1 = host.twinx()
#        par2 = host.twinx()
#        
#        par2.yaxis.tick_left()
#        # Offset the right spine of par2.  The ticks and label have already been
#        # placed on the right by twinx above.
#        par2.spines["left"].set_position(("axes", -0.1))
#        par2.spines["left"].set_bounds(10,60)
#        # Having been created by twinx, par2 has its frame off, so the line of its
#        # detached spine is invisible.  First, activate the frame but make the patch
#        # and spines invisible.
#        make_patch_spines_invisible(par2)
#        # Second, show the right spine.
#        par2.spines["left"].set_visible(True)
#        
#        p1, = host.plot([0, 1, 2], [0, 1, 2], "b-", label="Density")
#        p2, = par1.plot([0, 1, 2], [0, 3, 2], "r-", label="Temperature")
#        p3, = par2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")
#        
#        host.set_xlim(0, 2)
#        host.set_ylim(0, 2)
#        par1.set_ylim(0, 4)
#        par2.set_ylim(1, 65)
#        
#        host.set_xlabel("Distance")
#        host.set_ylabel("Density")
#        par1.set_ylabel("Temperature")
#        par2.set_ylabel("Velocity")
#        
#        host.yaxis.label.set_color(p1.get_color())
#        par1.yaxis.label.set_color(p2.get_color())
#        par2.yaxis.label.set_color(p3.get_color())
#        
#        tkw = dict(size=4, width=1.5)
#        host.tick_params(axis='y', colors=p1.get_color(), **tkw)
#        par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
#        par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
#        host.tick_params(axis='x', **tkw)
#        
#        lines = [p1, p2, p3]
#        
#        host.legend(lines, [l.get_label() for l in lines])
#        
#        plt.show()

    def set_subplot_adjust(self):
#        设置图四边的空白宽度
        h = self.height()
        w = self.width()
        left_gap = round(70 / w, 2)
        bottom_gap = round(50 / h, 2)
        right_gap = round((w - 40) / w, 2)
        top_gap = round((h - 40) / h, 2)
        self.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
                                 right=right_gap,top=top_gap,hspace=0.16)
        self.draw()
        
    def num_adjust(self, num):
        
        base_values = [1, 2, 5]
        digits = 0
        init_value = num
        result = 0
        abs_num = num = abs(num)
        if num >= 1:
            while num != 0:
                num = int(num / 10)
                digits += 1
            t_delta = -1
            for base in base_values:
                delta = abs(base * pow(10, digits - 1) - abs_num) 
                if t_delta == -1:
                    t_delta = delta
                    result =  base * pow(10, digits - 1)
                else:
                    if delta < t_delta:
                        t_delta = delta
                        result =  base * pow(10, digits - 1)
        elif num != 0:
            while num < 1:
                num = num * 10
                digits += 1
            t_delta = -1
            for base in base_values:
                delta = abs(base * pow(10, -digits) - abs_num) 
                if t_delta == -1:
                    t_delta = delta
                    result =  base * pow(10, -digits)
                else:
                    if delta < t_delta:
                        t_delta = delta
                        result =  base * pow(10, -digits)
        else:
            result = 0
        if init_value < 0:
            result = -1 * result
            
        return result

#------王--改动结束        
#        
#    def plot_para(self,source=None,para_list=[]):
#        if isinstance(source,(str,unicode)): #！！！！python 2
#            file_plot=Normal_DataFile(source)
#            para_list.insert(0,file_plot.paras_in_file[0])
#            df=file_plot.cols_input(source,para_list)
#        elif isinstance(source,pd.DataFrame):
#            df=source
#        else:
#            return
#        ax1 = self.fig.add_subplot(1,1,1)
#        df.plot(para_list[0],ax=ax1)
#        #self.draw()
#        self.show()
        
    def add_toolbar(self,parent=None):
        toolbar=NavigationToolbar(self,parent)
        return toolbar
    
    def show_toolbar(self,toolbar):
        toolbar.show()
        
    def hide_toolbar(self,toolbar):
        toolbar.hide()

class CustomToolbar(NavigationToolbar):
    
     def __init__(self, canvas, parent, coordinates=True):
         super().__init__(canvas, parent, coordinates)
         
     def custom_pan_left(self):
         
         ONE_SCREEN = 1
         for axes in self.canvas.figure.axes:
             
#         axes = self.canvas.figure.axes[1]
             x1,x2 = axes.get_xlim()
             ONE_SCREEN = x2 - x1
             axes.set_xlim(x1 - ONE_SCREEN, x2 - ONE_SCREEN)
         self.canvas.draw()
        
    

if __name__ == '__main__':
    filename=u'D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt'
    #filename=u'D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664003-16.txt'
    #filename=u'C:/Users/admin/Desktop/5008问题汇总.xlsx'
    #df=chunk_input(filename,sep='all')
    #df=all_input(filename)
    file_plot=Normal_DataFile(filename)
    para_name=file_plot.header_input(filename,sep='all')
    #df=cols_input(filename,['time','HF_FSECU_1_L354_HLS_OMS_Status_Flap_Inoperative','FCM3_Voted_True_Airspeed'])
        #df=cols_input(filename,[u'日期']
    #df.plot('time','FCM3_Voted_True_Airspeed')
    #plt.show()
    #plt.figure()
    #plt.plot(df['time'],df['FCM3_Voted_True_Airspeed'])
    #plt.show()
    #para_list=['time','HF_FSECU_1_L354_HLS_OMS_Status_Flap_Inoperative','FCM3_Voted_True_Airspeed']
    para_list=para_name.values[:,1:2].tolist()[0]
    #plot_para(filename,para_list)
    canvas=PlotCanvas()
    canvas.plot_para(filename,para_list)
#    canvas.plot_para(filename,para_list)
#    canvas.plot_para(filename,para_list)
#    canvas.plot_para(filename,para_list)
    toolbar=canvas.add_toolbar() #toolbar is widget, add it by specify its parent
    toolbar.show()
    #para_list=para_name.values[:,23:25].tolist()[0]
    #plot_para(filename,para_list)