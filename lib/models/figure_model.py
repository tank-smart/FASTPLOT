 # -*- coding: utf-8 -*-
# =============================================================================
# =======概述
# 文件名：figure_model.py
# 简述：绘图类
#
# =======内容
# 包含类：
# PlotCanvasBase
# FTDataPlotCanvasBase
# FastPlotCanvas
# SingleAxisPlotCanvas
# SingleAxisXTimePlotCanvas
# StackAxisPlotCanvas
# =======使用说明
# 参考类的使用说明
#
# =======日志

# =======备注

# =============================================================================
# =============================================================================
# 导入所需的包
# =============================================================================
# 用于数据处理的包
#import scipy.io as sio
import numpy as np
import pandas as pd
import json
# 用于绘图的包
import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, AutoMinorLocator, MaxNLocator, LinearLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.text import Annotation, Text
# 用于PyQt交互的包
from PyQt5.QtCore import pyqtSignal, QCoreApplication, QPoint, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMenu, QAction, QMessageBox, QDialog)
# 自定义的包
import views.config_info as CONFIG
from views.custom_dialog import (Base_LineSettingDialog, LineSettingDialog, 
                                 AnnotationSettingDialog, AxisSettingDialog,
                                 StackAxisSettingDialog, DisplayParaAggregateInfoDialog, 
                                 SaveTemplateDialog, ParameterExportDialog,
                                 SingleUtAxisSettingDialog)
import models.time_model as Time_Model
from models.data_model import DataFactory
# =============================================================================
# 画布类的定义
# =============================================================================
# 基础画布类
class PlotCanvasBase(FigureCanvas):
    
    signal_added_artist = pyqtSignal(str)
    
    def __init__(self, parent = None):
        
        self.fig = Figure(figsize = (10, 4), dpi = 100)
        FigureCanvas.__init__(self, self.fig)# 初始化父类
        self.setParent(parent)
        self.toolbar = NavigationToolbar(self, parent = None)
        self.toolbar.hide()
        
#        存储曲线颜色，默认的是十种颜色
        prop_cycle = plt.rcParams['axes.prop_cycle']
        self.curve_colors = prop_cycle.by_key()['color']
        self.color_index = 0
        
#        当前坐标个数，基类的坐标只有一个，曲线都画在这个坐标内
        self.count_axes = 1
        self.count_curves = 0
#        坐标信息
        self.axes_info = {}
        self.init_axes_lim = {}

#        当前光标在坐标内的样式
        self.current_cursor_inaxes = None
#        当前光标所在的坐标
        self.current_axes = None
#        单击右键选到要删除的文字标注或标记线
        self.picked_del_artist = None
#        右键菜单出现在的坐标
        self.axis_menu_on = None
        
#        当前标注的属性
        self.current_markline_color = CONFIG.OPTION['plot markline color']
        self.current_markline_style = CONFIG.OPTION['plot markline style']
        self.current_markline_marker = CONFIG.OPTION['plot markline marker']
        
#        与标注线有关的事件id
        self.cid_press_new_hline = None
        self.cid_press_new_vline = None
        self.cid_move_new_line = None
        self.cid_release_new_line = None
#        任意标注线的对象
        self.newline = None
        
#        是否显示网格线
        self.show_hgrid = True
        self.show_vgrid = True
        
#        当前文字标注的属性
        self.current_text_color = CONFIG.OPTION['plot fontcolor']
        self.current_text_size = CONFIG.OPTION['plot fontsize']
        self.current_text_arrow = CONFIG.OPTION['plot font arrow']
        self.current_text_bbox = CONFIG.OPTION['plot font bbox']
        
#        记录pick到哪个文字标注
        self.picked_annotation = None
#        记录文字标注移动事件的id
        self.cid_move_annotation = None
        self.cid_release_annotation = None
#        记录pick时文字的位置和鼠标位置，格式(x,y,mx,my)
        self.annotation_init_loc = None
        self.cid_press_new_annotation = None
        
#        添加右键菜单
        self.is_display_menu = True
#        当前标注的鼠标事件被激活
        self.marker_event_active = False

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

        self.mpl_connect('button_press_event', 
                                         self.slot_show_context_menu)
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

        self.mpl_connect('motion_notify_event', self.slot_set_cursor)
        
#        Pick事件在进行缩放移动、框选缩放时不会触发，但是press事件却会触发，不知道为何
        self.cid_on_pick = self.mpl_connect('pick_event', self.on_pick)
        
    def slot_set_display_menu(self, is_display):

        self.is_display_menu = is_display
        
    def slot_show_context_menu(self, event):
        
#        禁止缩放过程中弹出右键菜单
        if self.fig.axes and event.button == 3 and self.is_display_menu:
#            只要弹出了右键菜单，就把所有连接都断开
            self.slot_disconnect()
            
            h = self.height()
            cor_y = h - event.y
            menu = self.custom_context_menu(event)
            menu.exec_(self.mapToGlobal(QPoint(event.x, cor_y)))
            
#            无论是否触发删除事件，都将将选中的artist清空
            self.picked_del_artist = None
            self.axis_menu_on = None
            
    def custom_context_menu(self, event):
        
        menu = QMenu(self)
        menu.addActions([self.action_show_hgrid, 
                         self.action_show_vgrid,
                         self.action_axis_setting,
#                         self.action_add_text,
                         self.action_del_artist])
#        menu_markline = QMenu(menu)
#        menu_markline.setIcon(QIcon(CONFIG.ICON_ADD_LINE_MARK))
#        menu_markline.setTitle(QCoreApplication.
#                              translate('PlotCanvas', '添加标记线'))
#        menu_markline.addActions([self.action_add_mark_hline,
#                                self.action_add_mark_vline,
#                                self.action_add_arb_markline])
#        menu.addAction(menu_markline.menuAction())
#        menu.addAction(self.action_del_artist)
        
        if event.inaxes:
            self.axis_menu_on = event.inaxes
            self.action_axis_setting.setEnabled(True)
        else:
            self.action_axis_setting.setEnabled(False)

        if self.picked_del_artist:
            self.action_del_artist.setEnabled(True)
        else:
            self.action_del_artist.setEnabled(False)
            
        return menu
        
#    pick函数
    def on_pick(self, event):
        
#        判断是否是双击
        if not event.mouseevent.dblclick:
            if event.mouseevent.button == 1:
                if type(event.artist) == Annotation and event.mouseevent.inaxes:
                    self.picked_annotation = event.artist
                    self.create_move_annotation_event(event)
            if event.mouseevent.button == 3:
                if (type(event.artist) == Line2D or type(event.artist) == Annotation):
                    self.picked_del_artist = event.artist

        else:
            if event.mouseevent.button == 1:
                if type(event.artist) == Line2D:
                    self.set_line_props(event)
                if type(event.artist) == Annotation:
                    self.set_annotation_props(event)

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
        
        pass

#    标注线函数
    def slot_add_arb_markline(self):

        self.marker_event_active = True
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
                                                                gid = 'arb_markline',
                                                                c = self.current_markline_color,
                                                                ls = self.current_markline_style,
                                                                marker = self.current_markline_marker,
                                                                picker = 5))
                
    def set_line_props(self, event):
        
        line = event.artist
        dialog = Base_LineSettingDialog(self, line)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.current_markline_color = dialog.line_color
            self.current_markline_style = dialog.line_ls
            self.current_markline_marker = dialog.line_marker
            self.draw()
    
    def set_annotation_props(self, event):
        
        annotation = event.artist
        dialog = AnnotationSettingDialog(self, annotation)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.current_text_color = dialog.text_color
            self.current_text_size = dialog.text_size
            self.current_text_arrow = dialog.text_arrow
            self.current_text_bbox = dialog.text_bbox
            self.draw()
    
    def create_move_annotation_event(self, event):
        
        self.marker_event_active = True
        self.setCursor(Qt.ClosedHandCursor)
        self.current_cursor_inaxes = Qt.ClosedHandCursor
        self.cid_move_annotation = self.mpl_connect('motion_notify_event',
                                                    self.slot_move_annotation)
        self.cid_release_annotation = self.mpl_connect('button_release_event',
                                                       self.slot_release_annotation)
        self.annotation_init_loc = (self.picked_annotation.get_position() + 
                                    (event.mouseevent.xdata, event.mouseevent.ydata))
                
    def slot_release_newline(self, event):
        
        if event.button == 1:
            self.slot_disconnect()
    
    def slot_add_mark_hline(self):

        self.marker_event_active = True
        self.setCursor(Qt.SizeHorCursor)
        self.current_cursor_inaxes = Qt.SizeHorCursor
        self.cid_press_new_hline = self.mpl_connect('button_press_event',
                                                 self.slot_onpress_new_hline)
        
    def slot_onpress_new_hline(self, event):

        if event.inaxes and event.button == 1:
#            鼠标左键按下才生效，但鼠标右键会弹出右键菜单，此时左键选中一个动作后
#            再次按下右键又会执行下列语句，这是不合适的。因此在右键激活时也断开连接,
#            这在菜单函数里实现
            self.current_axes.axhline(event.ydata,
                                      gid = 'h_markline',
                                      c = self.current_markline_color,
                                      ls = self.current_markline_style,
                                      marker = self.current_markline_marker,
                                      picker = 5)
            self.draw()
#            动作已完成，断开信号与槽的连接，后边相同
        if event.button == 1:
            self.slot_disconnect()
        
    def slot_add_mark_vline(self):

        self.marker_event_active = True
        self.setCursor(Qt.SizeVerCursor)
        self.current_cursor_inaxes = Qt.SizeVerCursor
        self.cid_press_new_vline = self.mpl_connect('button_press_event',
                                                 self.slot_onpress_new_vline)
        
    def slot_onpress_new_vline(self, event):

        if event.inaxes and event.button == 1:
            self.current_axes.axvline(event.xdata,
                                      gid = 'v_markline',
                                      c = self.current_markline_color,
                                      ls = self.current_markline_style,
                                      marker = self.current_markline_marker,
                                      picker = 5)
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

#    文字标注函数     
    def slot_add_annotation(self):
        
        self.marker_event_active = True
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
            self.current_axes.annotate(text = r'Text',
                                       gid = 'marktext',
                                       xy = (event.xdata, event.ydata),
                                       color = self.current_text_color,
                                       size = self.current_text_size,
                                       bbox = dict(boxstyle = 'square, pad = 0.5', 
                                                   fc = 'w', ec = self.current_text_color,
                                                   visible = self.current_text_bbox),
                                       arrowprops = dict(arrowstyle = '->',
                                                         color = self.current_text_color,
                                                         visible = self.current_text_arrow),
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
            
    def slot_pan(self):
        
        self.toolbar.pan()
            
    def slot_disconnect_pan(self):
        
        pass
    
    def slot_home(self):
        
        if self.init_axes_lim:
            self.set_axes_init_lim(self.init_axes_lim)

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

        self.marker_event_active = False
#        这个鼠标设置会在缩放时改变鼠标样式，因为绑定了鼠标释放事件
        self.setCursor(Qt.ArrowCursor)
        self.current_cursor_inaxes = Qt.ArrowCursor
#        移动artist是已鼠标释放作为结束标志
        if self.cid_move_annotation and self.cid_release_annotation:
            self.mpl_disconnect(self.cid_move_annotation)
            self.mpl_disconnect(self.cid_release_annotation)
            self.cid_release_annotation = None
            self.cid_move_annotation = None
            self.picked_annotation = None
            self.annotation_init_loc = None
            
        if self.cid_move_new_line and self.cid_release_new_line:
            self.mpl_disconnect(self.cid_move_new_line)
            self.mpl_disconnect(self.cid_release_new_line)
            self.cid_release_new_line = None
            self.cid_move_new_line = None
            self.newline = None
            self.signal_added_artist.emit('line')
#        添加标注是已鼠标按下作为结束标志
        if self.cid_press_new_hline:
            self.mpl_disconnect(self.cid_press_new_hline)
            self.cid_press_new_hline = None
            self.signal_added_artist.emit('hline')

        if self.cid_press_new_vline:
            self.mpl_disconnect(self.cid_press_new_vline)
            self.cid_press_new_vline = None
            self.signal_added_artist.emit('vline')

        if self.cid_press_new_annotation:
            self.mpl_disconnect(self.cid_press_new_annotation)
            self.cid_press_new_annotation = None
            self.signal_added_artist.emit('text')
            
    def slot_clear_canvas(self):
        
        self.color_index = 0
#        当前坐标个数，基类的坐标只有一个，曲线都画在这个坐标内
        self.count_axes = 1
        self.count_curves = 0
#        坐标信息
        self.axes_info = {}
        self.init_axes_lim = {}

#        当前光标所在的坐标
        self.current_axes = None
        
#        当前标注的属性
        self.current_markline_color = CONFIG.OPTION['plot markline color']
        self.current_markline_style = CONFIG.OPTION['plot markline style']
        self.current_markline_marker = CONFIG.OPTION['plot markline marker']
        
#        是否显示网格线
        self.show_hgrid = True
        self.show_vgrid = True
        
#        当前文字标注的属性
        self.current_text_color = CONFIG.OPTION['plot fontcolor']
        self.current_text_size = CONFIG.OPTION['plot fontsize']
        self.current_text_arrow = CONFIG.OPTION['plot font arrow']
        self.current_text_bbox = CONFIG.OPTION['plot font bbox']
        
        self.fig.clf()
        self.draw()

    def custom_plot(self):
        
        pass
    
    def update_config_info(self):
        
        self.current_markline_color = CONFIG.OPTION['plot markline color']
        self.current_markline_style = CONFIG.OPTION['plot markline style']
        self.current_markline_marker = CONFIG.OPTION['plot markline marker']
        self.current_text_color = CONFIG.OPTION['plot fontcolor']
        self.current_text_size = CONFIG.OPTION['plot fontsize']
        self.current_text_arrow = CONFIG.OPTION['plot font arrow']
        self.current_text_bbox = CONFIG.OPTION['plot font bbox']
        
    def get_current_axes_lim(self):
        
        axes_lim = {}
        label = ''
        if self.fig.axes:
            for i, ax in enumerate(self.fig.axes):
                label = 'axis_' + str(i)
                axes_lim[label] = (ax, ax.get_xlim(), ax.get_ylim())
                
        return axes_lim
                
    def set_axes_init_lim(self, axes_lim : dict):
        
        if axes_lim:
            for label, ax_info in axes_lim.items():
                ax, xlim, ylim = ax_info
                ax.set_xlim(xlim[0], xlim[1])
                ax.set_ylim(ylim[0], ylim[1])
            self.draw()

#    def slot_save_time(self):
#        
#        self.signal_send_time.emit()
        
#    def slot_save_tinterval(self):
#        
#        ti_name = 'Interval0'
#        i = 1
#        while ti_name in self.time_intervals:
#            ti_name = 'Interval' + str(i)
#            i += 1
#        name, ok = QInputDialog.getText(self,
#                                        QCoreApplication.translate('PlotCanvas', '命名时间段'),
#                                        QCoreApplication.translate('PlotCanvas', '时间段名'),
#                                        QLineEdit.Normal,
#                                        ti_name)
#        
#        if (ok and name):
#            axes = self.fig.axes
#            if axes:
#                axis = axes[0]
#                st,et = axis.get_xlim()
#                stime = mdates.num2date(st).time().isoformat(timespec='milliseconds')
#                etime = mdates.num2date(et).time().isoformat(timespec='milliseconds')
#                self.time_intervals[name] = (stime, etime)
#                self.signal_send_tinterval.emit((name, stime, etime))
        
#    def slot_set_tlim(self, name):
#        
#        axes = self.fig.axes
#        stime, etime = self.time_intervals[name]
#        if axes:
#            st = mdates.date2num(Time_Model.str_to_datetime(stime))
#            et = mdates.date2num(Time_Model.str_to_datetime(etime))
#            axis = axes[0]
#            axis.set_xlim(st, et)
#            for ax in axes:
#                ax.autoscale(axis = 'y')
#            self.draw()    
                    
#    def slot_sel_function(self, cur_files):
#        
#        if self.time_intervals:
#            dialog = SelFunctionDialog(self)
#            return_signal = dialog.exec_()
#            if return_signal == QDialog.Accepted:
#                index = dialog.index
#                try:
#                    if index == 0:
#                        self.slot_export_tinterval_data_fig()
#                    elif index == 1:
#                        self.slot_export_tinterval_data_file(cur_files)
#                    elif index == 2:
#                        self.slot_export_tinterval_data_aggregate('mean')
#                    elif index == 3:
#                        self.slot_export_tinterval_data_aggregate('max')
#                    elif index == 4:
#                        self.slot_export_tinterval_data_aggregate('min')
#                    else:
#                        pass
#                except:
#                    QMessageBox.information(self,
#                            QCoreApplication.translate('PlotCanvas', '保存提示'),
#                            QCoreApplication.translate('PlotCanvas', '出现错误！'))

#    def slot_export_tinterval_data_fig(self):
#        
#        if self.time_intervals:
#            data_container = {}
#            for i, data_factory in enumerate(self.total_data):
#                for j, tname in enumerate(self.time_intervals):
#                    name = '_PLOTDATA '+ tname + str(i + 1) + str(j + 1)
#                    stime, etime = self.time_intervals[tname]
#    #                get到的数据是拷贝，注意内存空间和速度
#                    data = self.total_data[data_factory].get_trange_data(stime, etime)
#                    if not data.empty:
#                        data_container[name] = data
#            if data_container:
#                dialog = ParameterExportDialog(self, data_container)
#                return_signal = dialog.exec_()
#                if return_signal == QDialog.Accepted:
#                    QMessageBox.information(self,
#                            QCoreApplication.translate('PlotCanvas', '保存提示'),
#                            QCoreApplication.translate('PlotCanvas', '保存成功！'))
#    
#    def slot_export_tinterval_data_file(self, files):
#        
#        if self.time_intervals:
#            dialog = FileProcessDialog(self, files, self.time_intervals)
#            return_signal = dialog.exec_()
#            if return_signal == QDialog.Accepted:
#                QMessageBox.information(self,
#                        QCoreApplication.translate('PlotCanvas', '保存提示'),
#                        QCoreApplication.translate('PlotCanvas', '保存成功！'))
#                
#    def slot_export_tinterval_data_aggregate(self, flag):
#        
#        if self.time_intervals:
#            para_list = ['INTERVAL_NAME']
#            for tuple_para in self.sorted_paralist:
#                pn, pos = tuple_para
#                para_list.append(pn)
#            dict_intervals = {}
#            dict_intervals['INTERVAL_NAME'] = []
#            df_total = None
#            for i, data_factory in enumerate(self.total_data):
#                list_paravalue = []
#                for j, tname in enumerate(self.time_intervals):
#                    stime, etime = self.time_intervals[tname]
#                    data = self.total_data[data_factory].get_trange_data(stime, etime, [], False)
#                    if not data.empty:
#                        if flag == 'mean':
#                            list_paravalue.append(data.mean())
#                        elif flag == 'max':
#                            list_paravalue.append(data.max())
#                        elif flag == 'min':
#                            list_paravalue.append(data.min())
#                    if i == 0:
#                        dict_intervals['INTERVAL_NAME'].append(tname)
#                if i == 0:
#                    df_intervals = pd.DataFrame(dict_intervals)
#                    df_total = df_intervals
#                if list_paravalue:
#                    df_paravalue = pd.DataFrame(list_paravalue)
#                    if not df_paravalue.empty:
#                        df_total = pd.concat([df_total, df_paravalue], axis = 1)
#
#            if not df_total.empty:
#                self.import_value(df_total, para_list)
    
# =============================================================================
# 功能函数模块
# =============================================================================
#    def import_value(self, value, paralist):
#        
#        if not value.empty:
#            if type(value) == pd.DataFrame:
#                df = value
#            if type(value) == dict:
#                df = pd.DataFrame(value)
##            按指定顺序放置列
#            df = df[paralist]
#            file_dir, flag = QFileDialog.getSaveFileName(self, 
#                                                         QCoreApplication.translate('PlotCanvas', '保存参数值'),
#                                                         CONFIG.SETUP_DIR,
#                                                         QCoreApplication.translate('PlotCanvas', 'Text Files (*.txt);;CSV Files (*.csv);;Matlab Files (*.mat)'))
#            if file_dir:
#                if flag == 'Text Files (*.txt)':
#                    df.to_csv(file_dir, '\t' , index=False, encoding='utf-8')
#                if flag == 'CSV Files (*.csv)':
#                    df.to_csv(file_dir, ',' , index=False, encoding='utf-8')
#                if flag == 'Matlab Files (*.mat)':
#                    sio.savemat(file_dir, df.to_dict('list'))
#                QMessageBox.information(self,
#                        QCoreApplication.translate('PlotCanvas', '保存提示'),
#                        QCoreApplication.translate('PlotCanvas', '保存成功！'))

class FTDataPlotCanvasBase(PlotCanvasBase):

    signal_progress = pyqtSignal(int)
    signal_cursor_xdata = pyqtSignal(str, list)
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
#        当前的数据字典
        self._data_dict = {}
#        参数数据相关变量
#        数据
        self.total_data = {}
#        时间
        self.time_series_list = {}
#        所有数据的长度是否一致,用于判读能否绘制非时间图
        self.is_same_length = True
#        已创建的DataFactory个数
        self.count_created_data = 0
#        顺序排列的参数及其对应的数据索引
        self.sorted_paralist = []
#        filedir:filetype用于识别不同文件类型
        self.dict_filetype = None
#        读参数值的辅助线
        self.aux_line = None
        self.cid_dppv_move = None
        self.cid_dppv_press = None
        
#    datadict中的参数和sorted_paras中的参数个数是一致的，这在输入时就保证了
    def process_data(self, datadict, sorted_paras, dict_filetype):
        
        if datadict:
            dict_data_project = {}
            for datasource in datadict:
                data = datadict[datasource]
                if type(data) == list and dict_filetype:
#                    此时datasource是文件路径，data是参数列表
                    data_factory = DataFactory(datasource, data, dict_filetype[datasource])
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
                        if self.total_data:
                            self.is_same_length = False
                        data_label = '_figure_data_' + str(self.count_created_data)
                        dict_data_project[datasource] = data_label
#                        total_data里存的就是当前绘图的参数数据，没有多余参数
                        self.total_data[data_label] = data_factory
#                        把时间列读出来，因为matplotlib只识别ndarray，所以进行类型转换
                        if data_factory.time_format is not None:
                            self.time_series_list[data_label] = np.array(pd.to_datetime(data_factory.data.iloc[:, 0],format=data_factory.time_format))
#                        实际应该推断dataframe的timeformat
                        else:
                            self.time_series_list[data_label] = np.array(pd.to_datetime(data_factory.data.iloc[:, 0],format='%H:%M:%S:%f'))
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
            
                    
            if exit_paras:
                print_para = '以下参数已存在：'
                for pa in exit_paras:
                    print_para += ('<br>' + pa)
                QMessageBox.information(self,
                        QCoreApplication.translate('FTDataPlotCanvasBase', '绘图提示'),
                        QCoreApplication.translate('FTDataPlotCanvasBase', print_para))
#            如果要绘制的参数都在，则不执行画图函数
            if len(exit_paras) == len(sorted_paras):
                return False
            else:
                return True
            
    def delete_para_data(self, index):
        
        if index >= 0 and index < len(self.sorted_paralist):
            pn, index_sr = self.sorted_paralist[index]
            self.total_data[index_sr].delete_col(pn)
            if not self.total_data[index_sr].get_paralist():
                del self.total_data[index_sr]
            self.sorted_paralist.pop(index)
            
    def slot_connect_display_paravalue(self):
        
        if self.fig.axes and self.aux_line == None:
            ax = self.fig.axes[0]
            time = (15 * ax.get_xlim()[0] + ax.get_xlim()[1]) / 16
            datatime_sel = mdates.num2date(time)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            real_time = ''
#            当时间不一致时，选择第一个不为空的时刻作为真实时刻
            for para in list_paravalue_info:
                if para[0] != '':
                    real_time = para[0]
                    break
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.signal_cursor_xdata.emit(real_time, list_paravalue_info)
                self.aux_line = ax.axvline(rt, 
                                           gid = 'getvalue',
                                           c = 'black',
                                           ls = '--',
                                           marker = 'd',
                                           markerfacecolor = 'green',
                                           markersize = 8)
                self.draw()
        self.cid_dppv_move = self.mpl_connect('motion_notify_event',
                                              self.slot_display_paravalue)
        self.cid_dppv_press = self.mpl_connect('button_press_event',
                                               self.slot_display_paravalue)
    
    def slot_diaconnect_display_paravalue(self):
        
        if self.aux_line:
            self.aux_line.remove()
            self.aux_line = None
            self.draw()
        self.mpl_disconnect(self.cid_dppv_move)
        self.mpl_disconnect(self.cid_dppv_press)

    def slot_display_paravalue(self, event):
        
        if event.inaxes and event.button == 1 and not self.marker_event_active:
            datatime_sel = mdates.num2date(event.xdata)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            real_time = ''
#            当时间不一致时，选择第一个不为空的时刻作为真实时刻
            for para in list_paravalue_info:
                if para[0] != '':
                    real_time = para[0]
                    break
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.signal_cursor_xdata.emit(real_time, list_paravalue_info)
                if self.aux_line:
                    if self.aux_line.axes == event.inaxes:
                        self.aux_line.set_xdata([rt, rt])
                    else:
                        self.aux_line.remove()
                        self.aux_line = event.inaxes.axvline(rt,
                                                             gid = 'getvalue',
                                                             c = 'black',
                                                             ls = '--',
                                                             marker = 'd',
                                                             markerfacecolor = 'green',
                                                             markersize = 8)
                else:
                    self.aux_line = event.inaxes.axvline(rt,
                                                         gid = 'getvalue',
                                                         c = 'black',
                                                         ls = '--',
                                                         marker = 'd',
                                                         markerfacecolor = 'green',
                                                         markersize = 8)
                self.draw()

    def get_paravalue(self, dt):
        
        list_paravalue_info = []
        for para_tuple in self.sorted_paralist:
            paraname, index= para_tuple
            time_str, pv = self.total_data[index].get_time_paravalue(dt, paraname)
#            这样做会在数据字典很大时暴露出卡顿的问题
            if (self._data_dict and 
                CONFIG.OPTION['data dict scope plot'] and
                paraname in self._data_dict):
                pn = self._data_dict[paraname][0]
                if pn != 'NaN':
                    paraname = pn
            if time_str != '':
                list_paravalue_info.append((time_str, paraname, pv))
            else:
                list_paravalue_info.append(('', paraname, 'NaN'))
        return list_paravalue_info
    
#    将从图中选择的时间段数据导出
    def slot_export_tinterval_data_fig(self, stime, etime):
        
        data_container = {}
        for i, data_factory in enumerate(self.total_data):
#            get到的数据是拷贝，注意内存空间和速度
            timerange, data = self.total_data[data_factory].get_trange_data(stime, etime)
            if not data.empty:
                data_container['_PLOTDATA'] = self.total_data[data_factory]
        if data_container:
            dialog = ParameterExportDialog(self, data_container)
            return_signal = dialog.exec_()
            if return_signal == QDialog.Accepted:
                QMessageBox.information(self,
                                        QCoreApplication.translate('FTDataPlotCanvasBase', '保存提示'),
                                        QCoreApplication.translate('FTDataPlotCanvasBase', '保存成功！'))
    
    def slot_clear_canvas(self):
        
        PlotCanvasBase.slot_clear_canvas(self)
        self.total_data = {}
        self.sorted_paralist = []
        self.time_series_list = {}
        self.is_same_length = True
        self.count_created_data = 0

#    当新建一种画布类时必须重载绘图函数
    def plot_paras(self, datalist, sorted_paras):
        
        raise KeyError('must overload function \'plot_paras\'(FastPlot).')
        
#    画布布局函数
    def adjust_figure(self):

        raise KeyError('must overload function \'adjust_figure\'(FastPlot).')
    
#    保存是的布局函数
    def adjust_savefig(self):
        
        raise KeyError('must overload function \'adjust_savefig\'(FastPlot).')

#    存储当前画布里的对象信息        
    def restore_axes_info(self):
        
        raise KeyError('must overload function \'restore_axes_info\'(FastPlot).')
        
    def save_plot_temp(self):
        
        raise KeyError('must overload function \'save_plot_temp\'(FastPlot).')
        
class FastPlotCanvas(FTDataPlotCanvasBase):
    
    signal_adjust_win = pyqtSignal()
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
        
        self.aux_lines = []
        self._count_value_mark = 0
#        数据选段
        self.data_span = None
        self.cid_drag_data_inter = None
        self.cid_release_data_inter = None
        
        self.action_display_data_info = QAction(self)
        self.action_display_data_info.setText(QCoreApplication.
                                              translate('FastPlotCanvas', '数据聚合'))
        self.action_display_data_info.triggered.connect(self.slot_display_aggregate_info)
        self.action_mark_data = QAction(self)
        self.action_mark_data.setText(QCoreApplication.
                                      translate('FastPlotCanvas', '取值标注'))
        self.action_mark_data.triggered.connect(self.slot_mark_data)
        self.action_up_axis = QAction(self)
        self.action_up_axis.setText(QCoreApplication.
                                    translate('FastPlotCanvas', '上移曲线'))
        self.action_up_axis.triggered.connect(self.slot_up_axis)
        self.action_down_axis = QAction(self)
        self.action_down_axis.setText(QCoreApplication.
                                      translate('FastPlotCanvas', '下移曲线'))
        self.action_down_axis.triggered.connect(self.slot_down_axis)
        self.action_del_axis = QAction(self)
        self.action_del_axis.setText(QCoreApplication.
                                     translate('FastPlotCanvas', '删除曲线'))
        self.action_del_axis.triggered.connect(self.slot_del_axis)
        self.action_sel_data_inter = QAction(self)
        self.action_sel_data_inter.setText(QCoreApplication.
                                           translate('FastPlotCanvas', '选择数据'))
        self.action_del_axis.triggered.connect(self.slot_sel_data_inter)
        
        
    def custom_context_menu(self, event):
#        如果重载函数内有单独使用self变量的情况，调用重载函数时需要加上self作为参数
        menu = PlotCanvasBase.custom_context_menu(self, event)
        menu.addSeparator()
        menu.addActions([self.action_up_axis,
                         self.action_down_axis,
                         self.action_del_axis])
        if event.inaxes:
            self.action_up_axis.setEnabled(True)
            self.action_down_axis.setEnabled(True)
            self.action_del_axis.setEnabled(True)
        else:
            self.action_up_axis.setEnabled(False)
            self.action_down_axis.setEnabled(False)
            self.action_del_axis.setEnabled(False)
        menu.addSeparator()
        menu.addActions([self.action_display_data_info,
                         self.action_mark_data])
        return menu
    
    def slot_axis_setting(self):
        
        dialog = AxisSettingDialog(self, self.axis_menu_on)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.draw()
        
    def slot_display_aggregate_info(self):
        
        if self.total_data:
#            获得开始时间和结束时间
            axes = self.fig.axes
            st,et = axes[0].get_xlim()
            stime = mdates.num2date(st).time().isoformat(timespec='milliseconds')
            etime = mdates.num2date(et).time().isoformat(timespec='milliseconds')
            
            para_info_list = []
            for para_tuple in self.sorted_paralist:
                paraname_init, index= para_tuple
                paraname = paraname_init
                real_timerange, data = self.total_data[index].get_trange_data(stime, etime, [paraname_init], False)
#                替换参数名
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope plot'] and
                    paraname_init in self._data_dict):
                    pn = self._data_dict[paraname_init][0]
                    if pn != 'NaN':
                        paraname = pn
                        
                if not data.empty:
                    para_info_list.append((paraname,
                                           data.mean()[paraname_init], 
                                           data.max()[paraname_init], 
                                           data.min()[paraname_init]))
                        
            dialog = DisplayParaAggregateInfoDialog(self)
            dialog.display_para_agg_info(real_timerange, para_info_list)
            dialog.exec_()
            
    def slot_mark_data(self):

        self.marker_event_active = True
        self.setCursor(Qt.SizeVerCursor)
        self.current_cursor_inaxes = Qt.SizeVerCursor
        self.cid_press_new_vline = self.mpl_connect('button_press_event',
                                                 self.slot_onpress_mark_data)
    
    def slot_onpress_mark_data(self, event):

        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        if event.inaxes and event.button == 1:
            index = 0
            for i, axis in enumerate(self.fig.axes):
                if event.inaxes == axis:
                    index = i
                    break
            datatime_sel = mdates.num2date(event.xdata)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            real_time = list_paravalue_info[index][0]
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.current_axes.axvline(rt, c = self.current_markline_color,
                                          ls = self.current_markline_style,
                                          marker = self.current_markline_marker,
                                          picker = 5,
                                          gid = '_valuemark' + str(self._count_value_mark))
                self.current_axes.annotate(text = '时间 = ' + real_time + '\n' + list_paravalue_info[index][1] + ' = ' + str(list_paravalue_info[index][2]),
                                           xy = (rt, list_paravalue_info[index][2]),
                                           color = self.current_text_color,
                                           size = self.current_text_size,
                                           picker = 1,
                                           bbox = dict(boxstyle = 'square, pad = 0.5', 
                                                       fc = 'w', ec = self.current_text_color,
                                                       visible = self.current_text_bbox),
                                           arrowprops = dict(arrowstyle = '->',
                                                             color = self.current_text_color,
                                                             visible = self.current_text_arrow),
                                           fontproperties = font,
                                           gid = '_valuemark' + str(self._count_value_mark))
                self._count_value_mark += 1
                self.draw()
            else:
                QMessageBox.information(self,
                                        QCoreApplication.translate('FastPlotCanvas', '绘图提示'),
                                        QCoreApplication.translate('FastPlotCanvas', '时间：' + Time_Model.datetime_to_timestr(datatime_sel) + '处无数据'))
        if event.button == 1:
            self.slot_disconnect()

    def set_line_props(self, event):
        
        line = event.artist
        xdata = line.get_xdata()
        dialog = LineSettingDialog(self, line)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.current_markline_color = dialog.line_color
            self.current_markline_style = dialog.line_ls
            self.current_markline_marker = dialog.line_marker
            if dialog.text_mark and xdata[0] != dialog.line_xdata[0]:
                index = 0
                for i, axis in enumerate(self.fig.axes):
                    if line.axes == axis:
                        index = i
                        break
                datatime_sel = mdates.num2date(dialog.line_xdata[0])
                list_paravalue_info = self.get_paravalue(datatime_sel)
                real_time = ''
    #            当时间不一致时，选择第一个不为空的时刻作为真实时刻
                for para in list_paravalue_info:
                    if para[0] != '':
                        real_time = para[0]
                        break
                
                if real_time != '':
                    rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                    line.set_xdata([rt, rt])
                    dialog.text_mark.xy = (rt, list_paravalue_info[index][2])
                    dialog.text_mark.set_text('时间 = ' + real_time + '\n' + list_paravalue_info[index][1] + ' = ' + str(list_paravalue_info[index][2]))
                    dialog.text_mark.set_position((rt, list_paravalue_info[index][2]))
                else:
                    line.set_xdata(xdata)
                    QMessageBox.information(self,
                                            QCoreApplication.translate('FastPlotCanvas', '绘图提示'),
                                            QCoreApplication.translate('FastPlotCanvas', '时间：' + Time_Model.datetime_to_timestr(datatime_sel) + '处无数据'))
            self.draw()
            
    def slot_del_artist(self):

        message = QMessageBox.warning(self,
                      QCoreApplication.translate('FastPlotCanvas', '删除标记'),
                      QCoreApplication.translate('FastPlotCanvas',
                                        '''<p>确定要删除吗？'''),
                      QMessageBox.Yes | QMessageBox.No)
        if (message == QMessageBox.Yes):
#            实现删除取值标注中的线或文字时能同时删除
            if type(self.picked_del_artist) == Line2D:
                ax = self.picked_del_artist.axes
                if ax:
                    list_text = ax.findobj(Annotation)
                    for text in list_text:
                        if (self.picked_del_artist.get_gid() and
                            self.picked_del_artist.get_gid() == text.get_gid()):
                            text.remove()
            if type(self.picked_del_artist) == Annotation:
                ax = self.picked_del_artist.axes
                if ax:
                    list_line = ax.findobj(Line2D)
                    for line in list_line:
                        if (self.picked_del_artist.get_gid() and
                            self.picked_del_artist.get_gid() == line.get_gid()):
                            line.remove()
            self.picked_del_artist.remove()
            self.draw()

    def slot_up_axis(self):
        
        if self.axis_menu_on and self.fig.axes:
            for i, axis in enumerate(self.fig.axes):
                if axis == self.axis_menu_on and i > 0:
                    self.restore_axes_info()
                    paraname, index = self.sorted_paralist[i]
                    self.sorted_paralist[i] = self.sorted_paralist[i - 1]
                    self.sorted_paralist[i - 1] = (paraname, index)
                    self.count_axes = len(self.sorted_paralist)
                    self.signal_adjust_win.emit()
                    self.plot_total_data()
                    break
    
    def slot_down_axis(self):
        
        if self.axis_menu_on and self.fig.axes:
            for i, axis in enumerate(self.fig.axes):
                if axis == self.axis_menu_on and i < (len(self.fig.axes) - 1):
                    self.restore_axes_info()
                    paraname, index = self.sorted_paralist[i]
                    self.sorted_paralist[i] = self.sorted_paralist[i + 1]
                    self.sorted_paralist[i + 1] = (paraname, index)
                    self.count_axes = len(self.sorted_paralist)
                    self.signal_adjust_win.emit()
                    self.plot_total_data()
                    break
    
    def slot_del_axis(self):
        
        if self.axis_menu_on and self.fig.axes:
            for i, axis in enumerate(self.fig.axes):
                if axis == self.axis_menu_on:
                    paraname, index = self.sorted_paralist[i]
                    if (self._data_dict and 
                        CONFIG.OPTION['data dict scope plot'] and
                        paraname in self._data_dict):
                        pn = self._data_dict[paraname][0]
                        if pn != 'NaN':
                            paraname = pn
                    message = QMessageBox.warning(self,
                                                  QCoreApplication.translate('FastPlotCanvas', '删除曲线'),
                                                  QCoreApplication.translate('FastPlotCanvas', '确定要删除曲线：' + paraname + '吗？'),
                                                  QMessageBox.Yes | QMessageBox.No)
                    if (message == QMessageBox.Yes):
                        self.restore_axes_info()
                        self.delete_para_data(i)
                        self.count_axes = len(self.sorted_paralist)
                        self.signal_adjust_win.emit()
                        self.plot_total_data()
                    break

    def slot_sel_data_inter(self):
        
#        if self.fig.axes:
        self.setCursor(Qt.SizeHorCursor)
        self.current_cursor_inaxes = Qt.SizeHorCursor
        self.cid_drag_data_inter = self.mpl_connect('motion_notify_event',
                                                    self.slot_onmove_data_inter)
        self.cid_release_data_inter = self.mpl_connect('button_release_event',
                                                       self.slot_release_data_inter)
        
    def slot_onmove_data_inter(self, event):
        
        if event.inaxes and event.button == 1:
            if self.data_span:
#                返回四个点的位置N×2的numpy
                xy = self.data_span.get_xy()
                xy[2][0] = event.xdata
                xy[3][0] = event.xdata
                self.data_span.set_xy(xy)
                self.draw()
            else:
                self.data_span = self.current_axes.axvspan(event.xdata, event.xdata,
                                                           facecolor = 'g', alpha = 0.5)
#                self.data_span = self.current_axes.axvspan(event.xdata, event.xdata,
#                                                           facecolor = 'g', alpha = 0.5, hatch = '/')
    
    def slot_release_data_inter(self, event):
        
        if event.button == 1:
            self.setCursor(Qt.ArrowCursor)
            self.current_cursor_inaxes = Qt.ArrowCursor
            if self.cid_drag_data_inter and self.cid_release_data_inter:
                self.mpl_disconnect(self.cid_drag_data_inter)
                self.mpl_disconnect(self.cid_release_data_inter)
                self.cid_release_data_inter = None
                self.cid_drag_data_inter = None
#                返回四个点的位置N×2的numpy
                xy = self.data_span.get_xy()
                st = xy[0][0]
                et = xy[3][0]
                if st > et:
                    st = xy[3][0]
                    et = xy[0][0]
                self.slot_export_tinterval_data_fig(mdates.num2date(st).replace(tzinfo=None),
                                                    mdates.num2date(et).replace(tzinfo=None))
                self.data_span.remove()
                self.data_span = None
                self.signal_added_artist.emit('vspan')
                self.draw()

    def slot_connect_display_paravalue(self):
        
        if self.fig.axes and self.aux_lines == []:
            ax = self.fig.axes[0]
            time = (15 * ax.get_xlim()[0] + ax.get_xlim()[1]) / 16
            datatime_sel = mdates.num2date(time)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            real_time = ''
#            当时间不一致时，选择第一个不为空的时刻作为真实时刻
            for para in list_paravalue_info:
                if para[0] != '':
                    real_time = para[0]
                    break
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.signal_cursor_xdata.emit(real_time, list_paravalue_info)
                for axis in self.fig.axes:
                    line = axis.axvline(rt,
                                        gid = 'getvalue',
                                        c = 'black',
                                        ls = '--',
                                        marker = 'd',
                                        markerfacecolor = 'green',
                                        markersize = 8)
                    self.aux_lines.append(line)
                self.draw()
        self.cid_dppv_move = self.mpl_connect('motion_notify_event',
                                              self.slot_display_paravalue)
        self.cid_dppv_press = self.mpl_connect('button_press_event',
                                               self.slot_display_paravalue)
    
    def slot_diaconnect_display_paravalue(self):
        
        if self.aux_lines:
            for line in self.aux_lines:
                line.remove()
            self.aux_lines = []
            self.draw()
        self.mpl_disconnect(self.cid_dppv_move)
        self.mpl_disconnect(self.cid_dppv_press)

    def slot_display_paravalue(self, event):
        
        if event.inaxes and event.button == 1 and not self.marker_event_active:
            datatime_sel = mdates.num2date(event.xdata)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            real_time = ''
#            当时间不一致时，选择第一个不为空的时刻作为真实时刻
            for para in list_paravalue_info:
                if para[0] != '':
                    real_time = para[0]
                    break
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.signal_cursor_xdata.emit(real_time, list_paravalue_info)
                if self.aux_lines:
                    for line in self.aux_lines:
                        line.set_xdata([rt, rt])
                else:
                    for axis in self.fig.axes:
                        line = axis.axvline(rt,
                                            gid = 'getvalue',
                                            c = 'black',
                                            ls = '--',
                                            marker = 'd',
                                            markerfacecolor = 'green',
                                            markersize = 8)
                        self.aux_lines.append(line)
                self.draw()
                
    def slot_clear_canvas(self):
        
        FTDataPlotCanvasBase.slot_clear_canvas(self)
        self._count_value_mark = 0
            
    def my_format(self, x, pos=None):
        
        x = matplotlib.dates.num2date(x)
        return Time_Model.datetime_to_timestr(x)
            
    def plot_paras(self, datalist, sorted_paras):

        self.restore_axes_info()
        is_plot = self.process_data(datalist, sorted_paras, self.dict_filetype)
        
        if is_plot:
            self.count_axes = len(self.sorted_paralist)
#            发出信号让绘图窗口变化大小适应画布
            self.signal_adjust_win.emit()
            self.plot_total_data()
            
    def plot_total_data(self):
        
        self.fig.clf()
        
        matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
        matplotlib.rcParams['ytick.direction'] = 'in'
#        支持中文显示
#        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        count = len(self.sorted_paralist)

#        axeslist = []
        first_axis = None
        self.color_index = 0
        for i, para_tuple in enumerate(self.sorted_paralist):
            self.signal_progress.emit(int(i/count*100))
            paraname, index = para_tuple
            ax = None
            if i == 0:
                ax = self.fig.add_subplot(count, 1, 1)
                first_axis = ax
            else:
                ax = self.fig.add_subplot(count, 1, i+1, sharex = first_axis)
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
                            lw = 1,
                            gid = 'dataline_' + paraname)
                else:
                    ax.plot(self.time_series_list[index], 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1,
                            gid = 'dataline_' + paraname)
            else:
                ax.plot(self.time_series_list[index], 
                        self.total_data[index].data[paraname],
                        color = self.curve_colors[self.color_index],
                        lw = 1,
                        gid = 'dataline_' + paraname)
                
            if i != (count - 1):
                plt.setp(ax.get_xticklabels(), visible = False)
            else:
                ax.set_xlabel('时间', fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
#                if xlim:
#                    ax.set_xlim(xlim)
#                若已指定fontproperties属性，则fontsize不起作用
                plt.setp(ax.get_xticklabels(),
                         horizontalalignment = 'center',
                         rotation = 'horizontal',
                         fontproperties = CONFIG.FONT_MSYH)
#                ax.set_xlabel('Time', fontproperties = self.font_times)
            plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
#            ax.legend(fontsize = self.default_fontsize,
#                      loc=(0,1), ncol=1, frameon=False, borderpad = 0.15,
#                      prop = CONFIG.FONT_MSYH)
            ax.legend(loc=(0,1), ncol=1, frameon=False, borderpad = 0.15,
                      prop = CONFIG.FONT_MSYH)
            ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.grid(which='major',linestyle='--',color = '0.45')
            ax.grid(which='minor',linestyle='--',color = '0.75')
#            一共有十种颜色可用
            if self.color_index == 9:
                self.color_index = 0
            else:
                self.color_index += 1
        
        self.init_axes_lim = {}
        self.init_axes_lim = self.get_current_axes_lim()
        self.refresh_axes_status()
        self.adjust_figure()
        
#    根据存储的坐标信息，把重画后的坐标状态还原
    def refresh_axes_status(self):
        
        axes = self.fig.axes
        if axes and (len(axes) == len(self.sorted_paralist)):
            for i, para_tuple in enumerate(self.sorted_paralist):
                ax = axes[i]
                paraname, index = para_tuple
                if paraname in self.axes_info:
                    if index == self.axes_info[paraname]['scr_index']:
                        ax.set_xlim(self.axes_info[paraname]['xlim'])
                        ax.set_ylim(self.axes_info[paraname]['ylim'])
                        self.refresh_axes_artist_status(self.axes_info[paraname], ax)
                        
    def refresh_axes_artist_status(self, dict_axis_info, ax):
        
        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        datalines = dict_axis_info['datalines']
#        数据曲线的属性设置
#        不用判断是否是数据线，因为当前还未加入任何标记线
        lines = ax.get_lines()
        for curve in lines:
            for i, dl in enumerate(datalines):
                if curve.get_gid() == dl['line_gid']:
                    curve.set_label(datalines[i]['label'])
                    curve.set_linestyle(datalines[i]['ls'])
                    curve.set_color(datalines[i]['color'])
                    curve.set_linewidth(datalines[i]['lw'])
                    curve.set_marker(datalines[i]['line_mark'])
                    break
                    
        if ax.get_legend():
#            设置图注
            hs, ls = ax.get_legend_handles_labels()
            i = 0
            for j, curve in enumerate(lines):
                for i, dl in enumerate(datalines):
                    if curve.get_gid() == dl['line_gid']:
                        ls[j] = datalines[i]['label']
                        hs[j].set_color(datalines[i]['color'])
#            似乎获得图注labels时是返回曲线的label而不是当前状态，所以需要用下面这个设置下
            ax.legend(hs, ls, loc=(0,1), fontsize = ax.get_legend()._fontsize,
                      ncol=4, frameon=False, borderpad = 0.15,
                      prop = CONFIG.FONT_MSYH)
        
        arb_marklines = dict_axis_info['arb_marklines']
        for ml in arb_marklines:
            ax.add_line(Line2D(ml['xdata'],
                               ml['ydata'],
                               gid = 'arb_markline',
                               c = ml['color'],
                               ls = ml['ls'],
                               lw = ml['lw'],
                               marker = ml['line_mark'],
                               picker = 5))
            
        h_marklines = dict_axis_info['h_marklines']
        for ml in h_marklines:
            line = ax.axhline(ml['ydata'],
                              gid = 'h_markline',
                              c = ml['color'],
                              ls = ml['ls'],
                              lw = ml['lw'],
                              marker = ml['line_mark'],
                              picker = 5)
            line.set_xdata(ml['xdata'])
            
        v_marklines = dict_axis_info['v_marklines']
        for ml in v_marklines:
            line = ax.axvline(ml['xdata'],
                              gid = 'v_markline',
                              c = ml['color'],
                              ls = ml['ls'],
                              lw = ml['lw'],
                              marker = ml['line_mark'],
                              picker = 5)
            line.set_ydata(ml['ydata'])
            
        marktexts = dict_axis_info['marktexts']
        for mt in marktexts:
            ax.annotate(text = mt['content'],
                        gid = 'marktext',
                        xy =  mt['xy'],
                        xytext = mt['xytext'],
                        color = mt['color'],
                        rotation = mt['rotation'],
                        size = mt['fontsize'],
                        bbox = dict(boxstyle = 'square, pad = 0.5',
                                    fc = 'w', ec = mt['color'],
                                    visible = mt['bbox_visible']),
                        arrowprops = dict(arrowstyle = '->',
                                          color = mt['color'],
                                          visible = mt['arrow_visible']),
                        picker = 1,
                        fontproperties = font)
        self.refresh_axes_valuemark_status(dict_axis_info, ax)
    
#    更新取值标注的状态    
    def refresh_axes_valuemark_status(self, dict_axis_info, ax):
        
        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        valuemark_ts = dict_axis_info['valuemark_texts']
        valuemark_ls = dict_axis_info['valuemark_lines']
        for vm_gid in valuemark_ts:
            line = ax.axvline(valuemark_ls[vm_gid]['xdata'],
                              gid = vm_gid,
                              c = valuemark_ls[vm_gid]['color'],
                              ls = valuemark_ls[vm_gid]['ls'],
                              lw = valuemark_ls[vm_gid]['lw'],
                              marker = valuemark_ls[vm_gid]['line_mark'],
                              picker = 5)
            line.set_ydata(valuemark_ls[vm_gid]['ydata'])
            
            ax.annotate(text = valuemark_ts[vm_gid]['content'],
                        gid = vm_gid,
                        xy =  valuemark_ts[vm_gid]['xy'],
                        xytext = valuemark_ts[vm_gid]['xytext'],
                        color = valuemark_ts[vm_gid]['color'],
                        rotation = valuemark_ts[vm_gid]['rotation'],
                        size = valuemark_ts[vm_gid]['fontsize'],
                        bbox = dict(boxstyle = 'square, pad = 0.5',
                                    fc = 'w', ec = valuemark_ts[vm_gid]['color'],
                                    visible = valuemark_ts[vm_gid]['bbox_visible']),
                        arrowprops = dict(arrowstyle = '->',
                                          color = valuemark_ts[vm_gid]['color'],
                                          visible = valuemark_ts[vm_gid]['arrow_visible']),
                        picker = 1,
                        fontproperties = font)
            
    def adjust_figure(self):
        
        h = self.height()
        w = self.width()
#        设置图四边的空白宽度 
        bottom_gap = round(50 / h, 2)
        right_gap = round((w - 40) / w, 2)       
        left_gap = round(70 / w, 2)
        top_gap = round((h - 40) / h, 2)

        self.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
                                 right=right_gap,top=top_gap,hspace=0.16)
        self.draw()
        
    def adjust_savefig(self):
        
#        图注高度
        legend_h = 18
#        坐标高度
        axis_h = 100
#        画布尺寸
        h = self.count_axes * (axis_h + legend_h) + legend_h
        w = 650
        bottom_gap = round(legend_h * 2 / h, 2)
        right_gap = round((w - 10) / w, 2)
        left_gap = round(50 / w, 2)
        top_gap = round((h - legend_h) / h, 2)
        hs = round(legend_h / (axis_h + legend_h), 2)
        self.resize(w, h)
        self.fig.subplots_adjust(left = left_gap, bottom = bottom_gap,
                                 right = right_gap, top = top_gap, hspace = hs)
        
    def restore_axes_info(self):
        
        axes = self.fig.axes
        if axes and (len(axes) == len(self.sorted_paralist)):
            self.axes_info = {}
            for i, pn_info in enumerate(self.sorted_paralist):
                pn, scr_index = pn_info
                self.axes_info[pn] = {}
                self.axes_info[pn]['scr_index'] = scr_index
                self.axes_info[pn]['xlim'] = axes[i].get_xlim()
                self.axes_info[pn]['ylim'] = axes[i].get_ylim()
                self.restore_axes_artist_info(self.axes_info[pn], axes[i])
                
    def restore_axes_artist_info(self, dict_axis_info, axis):
        
        dict_axis_info['marktexts'] = []
        dict_axis_info['datalines'] = []
        dict_axis_info['arb_marklines'] = []
        dict_axis_info['h_marklines'] = []
        dict_axis_info['v_marklines'] = []
        dict_axis_info['valuemark_texts'] = {}
        dict_axis_info['valuemark_lines'] = {}
#        存储文字标注的属性
        annotations = axis.findobj(Annotation)
        if annotations:
            marktext_info = {}
            for anno in annotations:
                marktext_info = {}
                marktext_info['content'] = anno.get_text()
                marktext_info['xy'] = anno.xy
                marktext_info['xytext'] = anno.get_position()
                marktext_info['color'] = anno.get_color()
                marktext_info['rotation'] = anno.get_rotation()
                marktext_info['fontsize'] = anno.get_fontsize()
#                marktext_info['fontproperties'] = anno.get_fontproperties()
                marktext_info['bbox_visible'] = anno.get_bbox_patch().get_visible()
                marktext_info['arrow_visible'] = anno.arrow_patch.get_visible()
                if anno.get_gid() == 'marktext':
                    dict_axis_info['marktexts'].append(marktext_info)
                if anno.get_gid() and anno.get_gid().find('_value') != -1:
                    dict_axis_info['valuemark_texts'][anno.get_gid()] = marktext_info
#        存储标注线的属性
        lines = axis.findobj(Line2D)
        if lines:
            markline_info = {}
            for line in lines:
                markline_info = {}
                markline_info['color'] = line.get_color()
                markline_info['ls'] = line.get_linestyle()
                markline_info['lw'] = line.get_linewidth()
                markline_info['line_mark'] = line.get_marker()
                if line.get_gid() and line.get_gid().find('dataline') != -1:
                    markline_info['line_gid'] = line.get_gid()
                    markline_info['label'] = line.get_label()
                    dict_axis_info['datalines'].append(markline_info)
                if line.get_gid() == 'arb_markline':
                    markline_info['xdata'] = line.get_xdata()
                    markline_info['ydata'] = line.get_ydata()
                    dict_axis_info['arb_marklines'].append(markline_info)
                if line.get_gid() == 'h_markline':
                    markline_info['xdata'] = line.get_xdata()
                    markline_info['ydata'] = line.get_ydata()[0]
                    dict_axis_info['h_marklines'].append(markline_info)
                if line.get_gid() == 'v_markline':
                    markline_info['xdata'] = line.get_xdata()[0]
                    markline_info['ydata'] = line.get_ydata()
                    dict_axis_info['v_marklines'].append(markline_info)
                if line.get_gid() and line.get_gid().find('_value') != -1:
                    markline_info['xdata'] = line.get_xdata()[0]
                    markline_info['ydata'] = line.get_ydata()
                    dict_axis_info['valuemark_lines'][line.get_gid()] = markline_info

    def save_plot_temp_artist_info(self, dict_axis_info, axis):
        
        def is_in_range(f, rg):
            if f >= rg[0] and f <= rg[1]:
                return True
            else:
                return False

        abs_2_rel = lambda f, rg : (f - rg[0]) / (rg[1] - rg[0])
            
        def is_in_view(xl, yl, artist):
            if type(artist) == Annotation:
                xy = artist.xy
                xytext = artist.get_position()
#                只有文字位置和锚点都在坐标内，才算在坐标内
                if (is_in_range(xy[0], xl) and is_in_range(xy[1], yl) and
                    is_in_range(xytext[0], xl) and is_in_range(xytext[1], yl)):
                    return True
                else:
                    return False
                
            if type(artist) == Line2D:
                if artist.get_gid() and artist.get_gid().find('dataline') != -1:
                    return True
                if artist.get_gid() == 'arb_markline':
                    xdata = artist.get_xdata()
                    ydata = artist.get_ydata()
                    if (is_in_range(xdata[0], xl) and is_in_range(ydata[0], yl) and
                        is_in_range(xdata[1], xl) and is_in_range(ydata[1], yl)):
                        return True
                    else:
                        return False
                if artist.get_gid() == 'h_markline':
                    yd = artist.get_ydata()[0]
                    if is_in_range(yd, yl):
                        return True
                    else:
                        return False
                if artist.get_gid() == 'v_markline':
                    xd = artist.get_xdata()[0]
                    if is_in_range(xd, xl):
                        return True
                    else:
                        return False
                if artist.get_gid() and line.get_gid().find('_value') != -1:
                    xd = artist.get_xdata()[0]
                    if is_in_range(xd, xl):
                        return True
                    else:
                        return False
        
        ax_xlim = axis.get_xlim()
        ax_ylim = axis.get_ylim()
        dict_axis_info['marktexts'] = []
        dict_axis_info['datalines'] = []
        dict_axis_info['arb_marklines'] = []
        dict_axis_info['h_marklines'] = []
        dict_axis_info['v_marklines'] = []
        dict_axis_info['valuemark_texts'] = {}
        dict_axis_info['valuemark_lines'] = {}
#        存储文字标注的属性
        annotations = axis.findobj(Annotation)
        if annotations:
            marktext_info = {}
            for anno in annotations:
                if is_in_view(ax_xlim, ax_ylim, anno):
                    marktext_info = {}
                    marktext_info['content'] = anno.get_text()
                    axy = anno.xy
                    marktext_info['xy'] = (abs_2_rel(axy[0], ax_xlim), abs_2_rel(axy[1], ax_ylim))
                    xyt = anno.get_position()
                    marktext_info['xytext'] = (abs_2_rel(xyt[0], ax_xlim), abs_2_rel(xyt[1], ax_ylim))
                    marktext_info['color'] = anno.get_color()
                    marktext_info['rotation'] = anno.get_rotation()
                    marktext_info['fontsize'] = anno.get_fontsize()
    #                marktext_info['fontproperties'] = anno.get_fontproperties()
                    marktext_info['bbox_visible'] = anno.get_bbox_patch().get_visible()
                    marktext_info['arrow_visible'] = anno.arrow_patch.get_visible()
                    if anno.get_gid() == 'marktext':
                        dict_axis_info['marktexts'].append(marktext_info)
                    if anno.get_gid() and anno.get_gid().find('_value') != -1:
                        dict_axis_info['valuemark_texts'][anno.get_gid()] = marktext_info
#        存储标注线的属性
        lines = axis.findobj(Line2D)
        if lines:
            markline_info = {}
            for line in lines:
                if is_in_view(ax_xlim, ax_ylim, line):
                    markline_info = {}
                    markline_info['color'] = line.get_color()
                    markline_info['ls'] = line.get_linestyle()
                    markline_info['lw'] = line.get_linewidth()
                    markline_info['line_mark'] = line.get_marker()
                    if line.get_gid() and line.get_gid().find('dataline') != -1:
                        dict_axis_info['datalines'].append(markline_info)
                    if line.get_gid() == 'arb_markline':
                        arb_xdata = line.get_xdata()
                        arb_ydata = line.get_ydata()
                        markline_info['xdata'] = [abs_2_rel(arb_xdata[0], ax_xlim), abs_2_rel(arb_xdata[1], ax_xlim)]
                        markline_info['ydata'] = [abs_2_rel(arb_ydata[0], ax_ylim), abs_2_rel(arb_ydata[1], ax_ylim)]
                        dict_axis_info['arb_marklines'].append(markline_info)
                    if line.get_gid() == 'h_markline':
                        h_ydata = line.get_ydata()
                        markline_info['xdata'] = line.get_xdata()
                        markline_info['ydata'] = abs_2_rel(h_ydata[0], ax_ylim)
                        dict_axis_info['h_marklines'].append(markline_info)
                    if line.get_gid() == 'v_markline':
                        v_xdata = line.get_xdata()
                        markline_info['xdata'] = abs_2_rel(v_xdata[0], ax_xlim)
                        markline_info['ydata'] = line.get_ydata()
                        dict_axis_info['v_marklines'].append(markline_info)
                    if line.get_gid() and line.get_gid().find('_value') != -1:
                        vl_xdata = line.get_xdata()
                        markline_info['xdata'] = abs_2_rel(vl_xdata[0], ax_xlim)
                        markline_info['ydata'] = line.get_ydata()
                        dict_axis_info['valuemark_lines'][line.get_gid()] = markline_info
                        
    def plot_temp_artist_status(self, dict_axis_info, ax):
        
        rel_2_abs = lambda f, rg : rg[0] + f * (rg[1] - rg[0])
            
        ax_xlim = ax.get_xlim()
        ax_ylim = ax.get_ylim()
        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        datalines = dict_axis_info['datalines']
#        数据曲线的属性设置
#        不用判断是否是数据线，因为当前还未加入任何标记线
        lines = ax.get_lines()
        dlines = []
        for line in lines:
            if line.get_gid() and line.get_gid().find('dataline') != -1:
                dlines.append(line)
        for i, curve in enumerate(dlines):
            curve.set_linestyle(datalines[i]['ls'])
            curve.set_color(datalines[i]['color'])
            curve.set_linewidth(datalines[i]['lw'])
            curve.set_marker(datalines[i]['line_mark'])
                    
        if ax.get_legend():
#            设置图注
            hs, ls = ax.get_legend_handles_labels()
            for i, curve in enumerate(dlines):
                hs[i].set_color(datalines[i]['color'])
#            似乎获得图注labels时是返回曲线的label而不是当前状态，所以需要用下面这个设置下
            ax.legend(hs, ls, loc=(0,1), fontsize = ax.get_legend()._fontsize,
                      ncol=4, frameon=False, borderpad = 0.15,
                      prop = CONFIG.FONT_MSYH)
        
        arb_marklines = dict_axis_info['arb_marklines']
        for ml in arb_marklines:
            ax.add_line(Line2D([rel_2_abs(ml['xdata'][0], ax_xlim), rel_2_abs(ml['xdata'][1], ax_xlim)],
                               [rel_2_abs(ml['ydata'][0], ax_ylim), rel_2_abs(ml['ydata'][1], ax_ylim)],
                               gid = 'arb_markline',
                               c = ml['color'],
                               ls = ml['ls'],
                               lw = ml['lw'],
                               marker = ml['line_mark'],
                               picker = 5))
            
        h_marklines = dict_axis_info['h_marklines']
        for ml in h_marklines:
            line = ax.axhline(rel_2_abs(ml['ydata'], ax_ylim),
                              gid = 'h_markline',
                              c = ml['color'],
                              ls = ml['ls'],
                              lw = ml['lw'],
                              marker = ml['line_mark'],
                              picker = 5)
            line.set_xdata(ml['xdata'])
            
        v_marklines = dict_axis_info['v_marklines']
        for ml in v_marklines:
            line = ax.axvline(rel_2_abs(ml['xdata'], ax_xlim),
                              gid = 'v_markline',
                              c = ml['color'],
                              ls = ml['ls'],
                              lw = ml['lw'],
                              marker = ml['line_mark'],
                              picker = 5)
            line.set_ydata(ml['ydata'])
            
        marktexts = dict_axis_info['marktexts']
        for mt in marktexts:
            ax.annotate(text = mt['content'],
                        gid = 'marktext',
                        xy =  (rel_2_abs(mt['xy'][0], ax_xlim), rel_2_abs(mt['xy'][1], ax_ylim)),
                        xytext = (rel_2_abs(mt['xytext'][0], ax_xlim), rel_2_abs(mt['xytext'][1], ax_ylim)),
                        color = mt['color'],
                        rotation = mt['rotation'],
                        size = mt['fontsize'],
                        bbox = dict(boxstyle = 'square, pad = 0.5',
                                    fc = 'w', ec = mt['color'],
                                    visible = mt['bbox_visible']),
                        arrowprops = dict(arrowstyle = '->',
                                          color = mt['color'],
                                          visible = mt['arrow_visible']),
                        picker = 1,
                        fontproperties = font)
        self.plot_temp_valuemark_status(dict_axis_info, ax)
    
#    更新取值标注的状态    
    def plot_temp_valuemark_status(self, dict_axis_info, ax):
        
        def rel_2_abs(f, rg):
            
            return rg[0] + f * (rg[1] - rg[0])
        
        ax_xlim = ax.get_xlim()
        ax_ylim = ax.get_ylim()
        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        valuemark_ts = dict_axis_info['valuemark_texts']
        valuemark_ls = dict_axis_info['valuemark_lines']
        for vm_gid in valuemark_ts:
            
            xdata = ax_xlim[0] + valuemark_ls[vm_gid]['xdata'] * (ax_xlim[1] - ax_xlim[0])
            datatime_sel = mdates.num2date(xdata)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            index = 0
            for i, axis in enumerate(self.fig.axes):
                if ax == axis:
                    index = i
                    break
            real_time = list_paravalue_info[index][0]
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                line = ax.axvline(rt,
                                  gid = '_valuemark' + str(self._count_value_mark),
                                  c = valuemark_ls[vm_gid]['color'],
                                  ls = valuemark_ls[vm_gid]['ls'],
                                  lw = valuemark_ls[vm_gid]['lw'],
                                  marker = valuemark_ls[vm_gid]['line_mark'],
                                  picker = 5)
                line.set_ydata(valuemark_ls[vm_gid]['ydata'])
                
                ax.annotate(text = '时间 = ' + real_time + '\n' + list_paravalue_info[index][1] + ' = ' + str(list_paravalue_info[index][2]),
                            gid = '_valuemark' + str(self._count_value_mark),
                            xy =  (rel_2_abs(valuemark_ts[vm_gid]['xy'][0], ax_xlim), rel_2_abs(valuemark_ts[vm_gid]['xy'][1], ax_ylim)),
                            xytext = (rel_2_abs(valuemark_ts[vm_gid]['xytext'][0], ax_xlim), rel_2_abs(valuemark_ts[vm_gid]['xytext'][1], ax_ylim)),
                            color = valuemark_ts[vm_gid]['color'],
                            rotation = valuemark_ts[vm_gid]['rotation'],
                            size = valuemark_ts[vm_gid]['fontsize'],
                            bbox = dict(boxstyle = 'square, pad = 0.5',
                                        fc = 'w', ec = valuemark_ts[vm_gid]['color'],
                                        visible = valuemark_ts[vm_gid]['bbox_visible']),
                            arrowprops = dict(arrowstyle = '->',
                                              color = valuemark_ts[vm_gid]['color'],
                                              visible = valuemark_ts[vm_gid]['arrow_visible']),
                            picker = 1,
                            fontproperties = font)
                self._count_value_mark += 1

    def save_plot_temp(self):
        
        axes = self.fig.axes
        if axes:
            temp = {}
            dialog = SaveTemplateDialog(self)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                temp_name = dialog.temp_name
                if temp_name:
                    temp['figure_type'] = self.__class__.__name__
                    temp['temp_axes'] = []
                    for i, axis in enumerate(axes):
                        axis_name = 'temp_axis' + str(i)
                        temp[axis_name] = {}
                        temp['temp_axes'].append(temp[axis_name])
                        self.save_plot_temp_artist_info(temp[axis_name], axis)
                    try:
                        with open(CONFIG.SETUP_DIR + '\\data\\plot_temps\\' + temp_name + '.json', 'w') as file:
                            json.dump(temp, file)
                            self.fig.savefig(CONFIG.SETUP_DIR + '\\data\\plot_temps\\' + temp_name + '.png')
                        QMessageBox.information(self,
                                                QCoreApplication.translate('FastPlotCanvas', '保存提示'), 
                                                QCoreApplication.translate('FastPlotCanvas', '保存成功'))
                    except:
                        QMessageBox.information(self,
                                                QCoreApplication.translate('FastPlotCanvas', '保存提示'),
                                                QCoreApplication.translate('FastPlotCanvas', '保存失败！'))
                else:
                    QMessageBox.information(self,
                                            QCoreApplication.translate('FastPlotCanvas', '输入提示'),
                                            QCoreApplication.translate('FastPlotCanvas', '未输入模板名'))
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('FastPlotCanvas', '保存提示'),
                    QCoreApplication.translate('FastPlotCanvas', '没有发现图片'))
            
    def apply_plot_temp(self, temp_name):
        
#        导入模板信息
        try:
            plot_temp_info = {}
            with open(CONFIG.SETUP_DIR + '\\data\\plot_temps\\' + temp_name + '.json', 'r') as file:
                plot_temp_info = json.load(file)
                axes_info = plot_temp_info['temp_axes']
            if axes_info and self.fig.axes:
                if plot_temp_info['figure_type'] == self.__class__.__name__:
                    if len(axes_info) == len(self.fig.axes):
                        axes = self.fig.axes
                        for i, ax_info in enumerate(axes_info):
                            self.plot_temp_artist_status(ax_info, axes[i])
                        self.draw()
                    else:
                        QMessageBox.information(self,
                                                QCoreApplication.translate('FastPlotCanvas', '模板应用提示'),
                                                QCoreApplication.translate('FastPlotCanvas', '坐标个数不对，模板不可用！'))
                else:
                    QMessageBox.information(self,
                                            QCoreApplication.translate('FastPlotCanvas', '模板应用提示'),
                                            QCoreApplication.translate('FastPlotCanvas', '模板无法应用此类型图！'))
        except:
            QMessageBox.information(self,
                                    QCoreApplication.translate('FastPlotCanvas', '模板应用提示'),
                                    QCoreApplication.translate('FastPlotCanvas', '模板应用时出现错误！'))
        
#class SingleAxisPlotCanvasBase(FTDataPlotCanvasBase):
#    
#    def __init__(self, parent = None):
#    
#        super().__init__(parent)
#        self.count_axes = 1
#        
#    def slot_axis_setting(self):
#        
#        dialog = Base_AxisSettingDialog(self, self.axis_menu_on)
#        return_signal = dialog.exec_()
#        if (return_signal == QDialog.Accepted):
#            self.draw()
#            
#    def plot_paras(self, datalist, sorted_paras, xpara = None):
#
#        is_plot = self.process_data(datalist, sorted_paras)
#        xpara = "FCM1_Voted_Mach"
#        for index in self.total_data:
#            
#            if xpara not in self.total_data[index].data_paralist:
#                
#                print_message = self.total_data[index].filedir
#                QMessageBox.information(self,
#                        QCoreApplication.translate('PlotCanvas', '绘图提示'),
#                        QCoreApplication.translate('PlotCanvas', print_message+'绘图失败'))
#                return
#                
#        
#        if xpara == None:
#            xdata = "self.time_series_list[index]"
#        else:
#            xdata = "self.total_data[index].data[xpara]"
#            
#        
#        if is_plot:
#            self.fig.clf()
#            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
#            matplotlib.rcParams['ytick.direction'] = 'in'
##            支持中文显示
##            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
#            matplotlib.rcParams['axes.unicode_minus'] = False
#            
#            count = len(self.sorted_paralist)
#            self.count_curves = count
#    
#            axeslist = []
##            self.color_index = 0
#            for i, para_tuple in enumerate(self.sorted_paralist):
#                self.signal_progress.emit(int(i/count*100))
#                paraname, index = para_tuple
#                ax = None
#                if i == 0:
#                    ax = self.fig.add_subplot(count, 1, 1)
#                else:
#                    ax = self.fig.add_subplot(count, 1, i+1, sharex = axeslist[0])
#                axeslist.append(ax)
#                
#                if (self._data_dict and 
#                    CONFIG.OPTION['data dict scope plot'] and
#                    paraname in self._data_dict):
#                    pn = self._data_dict[paraname][0]
#                    unit = self._data_dict[paraname][1]
#                    if pn != 'NaN':
#                        if unit != 'NaN' and unit != '1':
#                            pn = pn + '(' + unit + ')'
#                        ax.plot(eval(xdata), 
#                                self.total_data[index].data[paraname],
#                                label = pn,
#                                color = self.curve_colors[self.color_index],
#                                lw = 1)
#                    else:
#                        ax.plot(eval(xdata), 
#                                self.total_data[index].data[paraname],
#                                color = self.curve_colors[self.color_index],
#                                lw = 1)
#                else:
#                    ax.plot(eval(xdata), 
#                            self.total_data[index].data[paraname],
#                            color = self.curve_colors[self.color_index],
#                            lw = 1)
#                
#                if i != (count - 1):
#                    plt.setp(ax.get_xticklabels(), visible = False)
#                else:
#                    xlabel = xpara
#                    if (self._data_dict and 
#                    CONFIG.OPTION['data dict scope plot'] and
#                    paraname in self._data_dict):
#                        xlabel = self._data_dict[xpara][0]
#                        xunit = self._data_dict[xpara][1]
#                    if xlabel != 'NaN':
#                        if xunit != 'NaN' and xunit != '1':
#                            xlabel = xlabel + '(' + xunit + ')'
#                    
#                    ax.set_xlabel(xlabel, fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
##                    若已指定fontproperties属性，则fontsize不起作用
#                    plt.setp(ax.get_xticklabels(),
#                             horizontalalignment = 'center',
#                             rotation = 'horizontal',
#                             fontproperties = CONFIG.FONT_MSYH)
##                    ax.set_xlabel('Time', fontproperties = self.font_times)
#                plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
##                ax.legend(fontsize = self.default_fontsize,
##                          loc=(0,1), ncol=1, frameon=False, borderpad = 0.15,
##                          prop = CONFIG.FONT_MSYH)
#                ax.legend(loc=(0,1), ncol=1, frameon=False, borderpad = 0.15,
#                          prop = CONFIG.FONT_MSYH)
##                ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
#                ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
#                ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
#                ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
#                ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
#                ax.grid(which='major',linestyle='--',color = '0.45')
#                ax.grid(which='minor',linestyle='--',color = '0.75')
#    #                一共有十种颜色可用
#                if self.color_index == 9:
#                    self.color_index = 0
#                else:
#                    self.color_index += 1
#            
#            self.init_axes_lim = {}
#            self.init_axes_lim = self.get_current_axes_lim()
#            self.adjust_figure()
#            self.xaxes_flag = xpara #标志x轴是否为时间
#            
#    def adjust_figure(self):
#        
#        h = self.height()
#        w = self.width()
##        设置图四边的空白宽度 
#        bottom_gap = round(50 / h, 2)
#        right_gap = round((w - 40) / w, 2)       
#        left_gap = round(70 / w, 2)
#        m = int(self.count_curves / 4)
#        if self.count_curves % 4 != 0:
#            m += 1
#        top_gap = round((h - 20 * m) / h, 2)
#
#        self.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
#                                 right=right_gap,top=top_gap,hspace=0.16)
#        self.draw()
#        
#    def adjust_savefig(self):
#        
##        图注高度
#        legend_h = 18
##        坐标高度
#        axis_h = 300
##        画布尺寸
#        h = (axis_h + legend_h) + legend_h
#        w = 650
#        bottom_gap = round(legend_h * 2 / h, 2)
#        right_gap = round((w - 10) / w, 2)
#        left_gap = round(50 / w, 2)
#        m = int(self.count_curves / 4)
#        if self.count_curves % 4 != 0:
#            m += 1
#        top_gap = round((h - legend_h * m) / h, 2)
#        hs = round(legend_h / (axis_h + legend_h), 2)
#        self.resize(w, h)
#        self.fig.subplots_adjust(left = left_gap, bottom = bottom_gap,
#                                 right = right_gap, top = top_gap, hspace = hs)

class SingleAxisPlotCanvas(FTDataPlotCanvasBase):
    
    signal_adjust_win = pyqtSignal()
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
        self.count_axes = 1
        self.data_timerange = {'enable' : True,
                               'whole_stime' : '',
                               'whole_etime' : '',
                               'view_stime' : '',
                               'view_etime' : ''}
        
    def slot_axis_setting(self):
        
        dialog = SingleUtAxisSettingDialog(self, self.axis_menu_on, self.data_timerange)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.data_timerange = dialog.data_timerange
            self.plot_total_data()
            self.draw()
        
    def slot_clear_canvas(self):
        
        self.count_axes = 1
        self.data_timerange = {'enable' : True,
                               'whole_stime' : '',
                               'whole_etime' : '',
                               'view_stime' : '',
                               'view_etime' : ''}
        FTDataPlotCanvasBase.slot_clear_canvas(self)
        
    def plot_paras(self, datalist, sorted_paras):

#        self.restore_axes_info()
        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
            self.count_axes = 1
            self.signal_adjust_win.emit()
            
            x_paraname, x_index = self.sorted_paralist[0]
            tr = self.total_data[x_index].time_range
            self.data_timerange['whole_stime'] = self.data_timerange['view_stime'] = tr[0]
            self.data_timerange['whole_etime'] = self.data_timerange['view_etime'] = tr[1]
            
            self.plot_total_data()
        
#    默认以第一个参数为x轴坐标
    def plot_total_data(self):

#        数据长度是通过判断时间是否一致来确定的，因此较特殊，后续需要改进
        if self.is_same_length:
            self.fig.clf()
            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
            matplotlib.rcParams['ytick.direction'] = 'in'
#            支持中文显示
#            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['axes.unicode_minus'] = False
            
            ax = self.fig.add_subplot(1, 1, 1)
            count = len(self.sorted_paralist)
            s_paralist = self.sorted_paralist
            if count != 1:
                s_paralist = s_paralist[1:]
                count = count - 1
            self.count_curves = count
            self.color_index = 0
            
            x_paraname, x_index = self.sorted_paralist[0]
            x_data = self.total_data[x_index].data[x_paraname]
            if self.data_timerange['view_stime'] and self.data_timerange['view_etime']:
                tr, x_data = self.total_data[x_index].get_trange_data(self.data_timerange['view_stime'], self.data_timerange['view_etime'], [x_paraname], False)
                
            for i, para_tuple in enumerate(s_paralist):
                self.signal_progress.emit(int(i/count*100))
                paraname, index = para_tuple
                y_data = self.total_data[index].data[paraname]
                if self.data_timerange['view_stime'] and self.data_timerange['view_etime']:
                    tr, y_data = self.total_data[index].get_trange_data(self.data_timerange['view_stime'], self.data_timerange['view_etime'], [paraname], False)
                    self.data_timerange['view_stime'] = tr[0]
                    self.data_timerange['view_etime'] = tr[1]
                
                if (self._data_dict and 
                    CONFIG.OPTION['data dict scope plot'] and
                    paraname in self._data_dict):
                    pn = self._data_dict[paraname][0]
                    unit = self._data_dict[paraname][1]
                    if pn != 'NaN':
                        if unit != 'NaN' and unit != '1':
                            pn = pn + '(' + unit + ')'
                        ax.plot(x_data, 
                                y_data,
                                label = pn,
                                color = self.curve_colors[self.color_index],
                                ls = 'None',
                                marker = '.',
                                gid = 'dataline_' + paraname)
                    else:
                        ax.plot(x_data, 
                                y_data,
                                label = paraname,
                                color = self.curve_colors[self.color_index],
                                ls = 'None',
                                marker = '.',
                                gid = 'dataline_' + paraname)
                else:
                    ax.plot(x_data, 
                            y_data,
                            label = paraname,
                            color = self.curve_colors[self.color_index],
                            ls = 'None',
                            marker = '.',
                            gid = 'dataline_' + paraname)
#                一共有十种颜色可用
                if self.color_index == 9:
                    self.color_index = 0
                else:
                    self.color_index += 1
            
                
            xlabel = x_paraname
            if (self._data_dict and 
                CONFIG.OPTION['data dict scope plot'] and
                x_paraname in self._data_dict):
                xlabel = self._data_dict[x_paraname][0]
                xunit = self._data_dict[x_paraname][1]
                if xlabel != 'NaN':
                    if xunit != 'NaN' and xunit != '1':
                        xlabel = xlabel + '(' + xunit + ')'
            
            ax.set_xlabel(xlabel, fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
    
#            ax.set_xlabel('时间', fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
#            若已指定fontproperties属性，则fontsize不起作用
            plt.setp(ax.get_xticklabels(),
                 horizontalalignment = 'center',
                 rotation = 'horizontal',
                 fontproperties = CONFIG.FONT_MSYH)
            plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
            ax.legend(loc=(0,1), ncol=4, frameon=False, borderpad = 0.15,
                      prop = CONFIG.FONT_MSYH)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.grid(which='major',linestyle='--',color = '0.45')
            ax.grid(which='minor',linestyle='--',color = '0.75')
                
            self.init_axes_lim = {}
            self.init_axes_lim = self.get_current_axes_lim()
            self.adjust_figure()
        else:
            QMessageBox.information(self,
                                    QCoreApplication.translate('SingleAxisPlotCanvas', '绘图提示'),
                                    QCoreApplication.translate('SingleAxisPlotCanvas', '数据长度不一致'))
            
    def adjust_figure(self):
        
        h = self.height()
        w = self.width()
#        设置图四边的空白宽度 
        bottom_gap = round(50 / h, 2)
        right_gap = round((w - 40) / w, 2)       
        left_gap = round(70 / w, 2)
        m = int(self.count_curves / 4)
        if self.count_curves % 4 != 0:
            m += 1
        top_gap = round((h - 20 * m) / h, 2)

        self.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
                                 right=right_gap,top=top_gap,hspace=0.16)
        self.draw()
        
    def adjust_savefig(self):
        
#        图注高度
        legend_h = 18
#        坐标高度
        axis_h = 300
#        画布尺寸
        h = (axis_h + legend_h) + legend_h
        w = 650
        bottom_gap = round(legend_h * 2 / h, 2)
        right_gap = round((w - 10) / w, 2)
        left_gap = round(50 / w, 2)
        m = int(self.count_curves / 4)
        if self.count_curves % 4 != 0:
            m += 1
        top_gap = round((h - legend_h * m) / h, 2)
        hs = round(legend_h / (axis_h + legend_h), 2)
        self.resize(w, h)
        self.fig.subplots_adjust(left = left_gap, bottom = bottom_gap,
                                 right = right_gap, top = top_gap, hspace = hs)
        
class SingleAxisXTimePlotCanvas(FastPlotCanvas):
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
        self.del_curve_acitons = []
        self.count_curves = 0
        
    def custom_context_menu(self, event):
#        如果重载函数内有单独使用self变量的情况，调用重载函数时需要加上self作为参数
        menu = PlotCanvasBase.custom_context_menu(self, event)
        if event.inaxes:
            self.del_curve_acitons = []
            menu.addSeparator()
            del_curve_menu = QMenu(menu)
            del_curve_menu.setTitle(QCoreApplication.
                                    translate('SingleAxisXTimePlotCanvas', '删除曲线'))
            ax = event.inaxes
            lines = ax.get_lines()
            for line in lines:
                if line.get_gid() and line.get_gid().find('dataline') != -1:
                    action = del_curve_menu.addAction(line.get_label())
                    self.del_curve_acitons.append((action, line.get_gid()))
            del_curve_menu.triggered.connect(self.slot_del_curve)
            menu.addMenu(del_curve_menu)
        menu.addSeparator()
        menu.addActions([self.action_display_data_info,
                         self.action_mark_data])
        return menu
    
    def slot_del_curve(self, action):
        
        pn = ''
        for ac, gid in self.del_curve_acitons:
            if action == ac:
                pn = gid[9 : ]
                break
        for i, para_info in enumerate(self.sorted_paralist):
            para_name, index = para_info
            if para_name == pn:
                self.restore_axes_info()
                self.delete_para_data(i)
                self.count_axes = len(self.sorted_paralist)
                self.signal_adjust_win.emit()
                self.plot_total_data()
                break
        
    def slot_onpress_mark_data(self, event):

        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        if event.inaxes and event.button == 1:
            datatime_sel = mdates.num2date(event.xdata)
            list_paravalue_info = self.get_paravalue(datatime_sel)
            real_time = ''
#            当时间不一致时，选择第一个不为空的时刻作为真实时刻
            for para in list_paravalue_info:
                if para[0] != '':
                    real_time = para[0]
                    break
            
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.current_axes.axvline(rt, c = self.current_markline_color,
                                          ls = self.current_markline_style,
                                          marker = self.current_markline_marker,
                                          picker = 5,
                                          gid = '_valuemark' + str(self._count_value_mark))
                dis_str = '时间 = ' + real_time
                for para_info in list_paravalue_info:
                    dis_str += '\n' + para_info[1] + ' = ' + str(para_info[2])
                self.current_axes.annotate(text = dis_str,
                                           xy = (rt, event.inaxes.get_ylim()[0]),
                                           color = self.current_text_color,
                                           size = self.current_text_size,
                                           picker = 1,
                                           bbox = dict(boxstyle = 'square, pad = 0.5', 
                                                       fc = 'w', ec = self.current_text_color,
                                                       visible = self.current_text_bbox),
                                           arrowprops = dict(arrowstyle = '->',
                                                             color = self.current_text_color,
                                                             visible = self.current_text_arrow),
                                           fontproperties = font,
                                           gid = '_valuemark' + str(self._count_value_mark))
                self._count_value_mark += 1
                self.draw()
            else:
                QMessageBox.information(self,
                                        QCoreApplication.translate('FastPlotCanvas', '绘图提示'),
                                        QCoreApplication.translate('FastPlotCanvas', '时间：' + Time_Model.datetime_to_timestr(datatime_sel) + '处无数据'))
        if event.button == 1:
            self.slot_disconnect()
            
    def set_line_props(self, event):
        
        line = event.artist
        xdata = line.get_xdata()
        dialog = LineSettingDialog(self, line)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.current_markline_color = dialog.line_color
            self.current_markline_style = dialog.line_ls
            self.current_markline_marker = dialog.line_marker
            if dialog.text_mark and xdata[0] != dialog.line_xdata[0]:
                datatime_sel = mdates.num2date(dialog.line_xdata[0])
                list_paravalue_info = self.get_paravalue(datatime_sel)
                real_time = ''
    #            当时间不一致时，选择第一个不为空的时刻作为真实时刻
                for para in list_paravalue_info:
                    if para[0] != '':
                        real_time = para[0]
                        break
                
                if real_time != '':
                    rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                    line.set_xdata([rt, rt])
                    dialog.text_mark.xy = (rt, event.mouseevent.inaxes.get_ylim()[0])
                    dis_str = '时间 = ' + real_time
                    for para_info in list_paravalue_info:
                        dis_str += '\n' + para_info[1] + ' = ' + str(para_info[2])
                    dialog.text_mark.set_text(dis_str)
                    dialog.text_mark.set_position((rt, event.mouseevent.inaxes.get_ylim()[0]))
                else:
                    line.set_xdata(xdata)
                    QMessageBox.information(self,
                                            QCoreApplication.translate('FastPlotCanvas', '绘图提示'),
                                            QCoreApplication.translate('FastPlotCanvas', '时间：' + Time_Model.datetime_to_timestr(datatime_sel) + '处无数据'))
            self.draw()
        
    def slot_connect_display_paravalue(self):
        
        FTDataPlotCanvasBase.slot_connect_display_paravalue(self)
        
    def slot_diaconnect_display_paravalue(self):
        
        FTDataPlotCanvasBase.slot_diaconnect_display_paravalue(self)

    def slot_display_paravalue(self, event):
        
        FTDataPlotCanvasBase.slot_display_paravalue(self, event)
        
    def slot_clear_canvas(self):
        
        FTDataPlotCanvasBase.slot_clear_canvas(self)
        self.del_curve_acitons = []
        self.count_curves = 0
        
    def plot_paras(self, datalist, sorted_paras):

        self.restore_axes_info()
        is_plot = self.process_data(datalist, sorted_paras, self.dict_filetype)
        
        if is_plot:
            self.count_axes = 1
            self.signal_adjust_win.emit()
            self.plot_total_data()
            
    def plot_total_data(self):

        self.fig.clf()
        if len(self.sorted_paralist) > 0:
            
            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
            matplotlib.rcParams['ytick.direction'] = 'in'
    #            支持中文显示
    #            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['axes.unicode_minus'] = False
            
            ax = self.fig.add_subplot(1, 1, 1)
            count = len(self.sorted_paralist)
            self.count_curves = count
        
            self.color_index = 0
            for i, para_tuple in enumerate(self.sorted_paralist):
                self.signal_progress.emit(int(i/count*100))
                paraname, index = para_tuple
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
                                lw = 1,
                                gid = 'dataline_' + paraname)
                    else:
                        ax.plot(self.time_series_list[index], 
                                self.total_data[index].data[paraname],
                                color = self.curve_colors[self.color_index],
                                lw = 1,
                                gid = 'dataline_' + paraname)
                else:
                    ax.plot(self.time_series_list[index], 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1,
                            gid = 'dataline_' + paraname)
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
                
            self.init_axes_lim = {}
            self.init_axes_lim = self.get_current_axes_lim()
            self.refresh_axes_status()
            self.adjust_figure()
        else:
            self.draw()

#    根据存储的坐标信息，把重画后的坐标状态还原
    def refresh_axes_status(self):
        
        ax = self.fig.axes
        if ax and self.axes_info:
            ax[0].set_xlim(self.axes_info['axis']['xlim'])
            self.refresh_axes_artist_status(self.axes_info['axis'], ax[0])
            
#    更新取值标注的状态    
    def refresh_axes_valuemark_status(self, dict_axis_info, ax):
        
        font = matplotlib.font_manager.FontProperties(
                fname = CONFIG.SETUP_DIR + r'\data\fonts\msyh.ttf',
                size = 8)
        valuemark_ts = dict_axis_info['valuemark_texts']
        valuemark_ls = dict_axis_info['valuemark_lines']
        for vm_gid in valuemark_ts:

            datatime_cur = mdates.num2date(valuemark_ls[vm_gid]['xdata'])
            list_paravalue_info = self.get_paravalue(datatime_cur)
            real_time = ''
#            当时间不一致时，选择第一个不为空的时刻作为真实时刻
            for para in list_paravalue_info:
                if para[0] != '':
                    real_time = para[0]
                    break
            
            rt = None
            dis_str = ''
            if real_time != '':
                dis_str = '时间 = ' + real_time
                for para_info in list_paravalue_info:
                    dis_str += '\n' + para_info[1] + ' = ' + str(para_info[2])
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
            else:
                dis_str = valuemark_ts[vm_gid]['content']
                rt = valuemark_ls[vm_gid]['xdata']
            
            line = ax.axvline(rt,
                              gid = vm_gid,
                              c = valuemark_ls[vm_gid]['color'],
                              ls = valuemark_ls[vm_gid]['ls'],
                              lw = valuemark_ls[vm_gid]['lw'],
                              marker = valuemark_ls[vm_gid]['line_mark'],
                              picker = 5)
            line.set_ydata(valuemark_ls[vm_gid]['ydata'])
            
            ax.annotate(text = dis_str,
                        gid = vm_gid,
                        xy =  valuemark_ts[vm_gid]['xy'],
                        xytext = valuemark_ts[vm_gid]['xytext'],
                        color = valuemark_ts[vm_gid]['color'],
                        rotation = valuemark_ts[vm_gid]['rotation'],
                        size = valuemark_ts[vm_gid]['fontsize'],
                        bbox = dict(boxstyle = 'square, pad = 0.5',
                                    fc = 'w', ec = valuemark_ts[vm_gid]['color'],
                                    visible = valuemark_ts[vm_gid]['bbox_visible']),
                        arrowprops = dict(arrowstyle = '->',
                                          color = valuemark_ts[vm_gid]['color'],
                                          visible = valuemark_ts[vm_gid]['arrow_visible']),
                        picker = 1,
                        fontproperties = font)

    def adjust_figure(self):
        
        h = self.height()
        w = self.width()
#        设置图四边的空白宽度 
        bottom_gap = round(50 / h, 2)
        right_gap = round((w - 40) / w, 2)       
        left_gap = round(70 / w, 2)
        m = int(self.count_curves / 4)
        if self.count_curves % 4 != 0:
            m += 1
        top_gap = round((h - 20 * m) / h, 2)

        self.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
                                 right=right_gap,top=top_gap,hspace=0.16)
        self.draw()
        
    def adjust_savefig(self):
        
#        图注高度
        legend_h = 18
#        坐标高度
        axis_h = 300
#        画布尺寸
        h = (axis_h + legend_h) + legend_h
        w = 650
        bottom_gap = round(legend_h * 2 / h, 2)
        right_gap = round((w - 10) / w, 2)
        left_gap = round(50 / w, 2)
        m = int(self.count_curves / 4)
        if self.count_curves % 4 != 0:
            m += 1
        top_gap = round((h - legend_h * m) / h, 2)
        hs = round(legend_h / (axis_h + legend_h), 2)
        self.resize(w, h)
        self.fig.subplots_adjust(left = left_gap, bottom = bottom_gap,
                                 right = right_gap, top = top_gap, hspace = hs)
        
    def restore_axes_info(self):
        
        axes = self.fig.axes
        
        if axes:
            self.axes_info = {}
            self.axes_info['axis'] = {'xlim' : axes[0].get_xlim(), 'ylim' : axes[0].get_ylim()}
            self.restore_axes_artist_info(self.axes_info['axis'], axes[0])
        
class StackAxisPlotCanvas(SingleAxisXTimePlotCanvas):
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
#        不显示右键的坐标设置
#        self.action_axis_setting.setVisible(False)

#        缩放
        self.cid_press_pan = None
        self.cid_move_pan = None
        self.cid_release_pan = None
        self.init_cursor_pos = None
        self.init_xlim = None
        self.init_ylim = None
#        坐标设置相关的变量
        self.selected_sta_axis = None
        self.selected_sta_axis_index = 0
        self.num_yscales = 0
        self.num_scales_between_ylabel = 0
        self.num_view_yscales = 0
        self.num_yview_scales = 0
        
    def custom_context_menu(self, event):
#        如果重载函数内有单独使用self变量的情况，调用重载函数时需要加上self作为参数
        menu = FastPlotCanvas.custom_context_menu(self, event)
        return menu
    
#    pick函数
    def on_pick(self, event):
        
        FastPlotCanvas.on_pick(self, event)
        
        if event.mouseevent.dblclick and type(event.artist) == Text:
            ylabel = event.artist
#            注意，主坐标是第一个坐标，该坐标是没有画曲线的
            axes = self.fig.axes
            for i, axis in enumerate(axes):
                if ylabel.get_text() == axis.get_ylabel():
                    self.change_sel_axis(axis, i - 1)
                    self.draw()
#                    layout_info = (self.num_yscales, self.num_scales_between_ylabel,
#                                   self.num_view_yscales, self.num_yview_scales, i - 1)
#                    dialog = StackAxisSettingDialog(self, axis, layout_info)
#                    return_signal = dialog.exec_()
#                    if (return_signal == QDialog.Accepted):
#                        event.canvas.draw()
                        
    def slot_axis_setting(self):
        
        if self.selected_sta_axis:
            layout_info = (self.num_yscales, self.num_scales_between_ylabel,
                           self.num_view_yscales, self.num_yview_scales,
                           self.selected_sta_axis_index)
            dialog = StackAxisSettingDialog(self, self.selected_sta_axis, layout_info)
            return_signal = dialog.exec_()
            if (return_signal == QDialog.Accepted):
                self.draw()
        else:
            QMessageBox.information(self,
                    QCoreApplication.translate('StackAxisPlotCanvas', '绘图提示'),
                    QCoreApplication.translate('StackAxisPlotCanvas', '未选择坐标！'))
            
    def slot_up_axis(self):
        
        if self.selected_sta_axis:
            i = self.selected_sta_axis_index
            if i > 0:
                self.selected_sta_axis_index = i - 1
                self.restore_axes_info()
                paraname, index = self.sorted_paralist[i]
                self.sorted_paralist[i] = self.sorted_paralist[i - 1]
                self.sorted_paralist[i - 1] = (paraname, index)
                self.count_axes = len(self.sorted_paralist)
                self.signal_adjust_win.emit()
                self.plot_total_data()
    
    def slot_down_axis(self):
        
        if self.selected_sta_axis:
            i = self.selected_sta_axis_index
            if i < (len(self.sorted_paralist) - 1):
                self.selected_sta_axis_index = i + 1
                self.restore_axes_info()
                paraname, index = self.sorted_paralist[i]
                self.sorted_paralist[i] = self.sorted_paralist[i + 1]
                self.sorted_paralist[i + 1] = (paraname, index)
                self.count_axes = len(self.sorted_paralist)
                self.signal_adjust_win.emit()
                self.plot_total_data()
    
    def slot_del_axis(self):
        
        if self.selected_sta_axis:
            paraname, index = self.sorted_paralist[self.selected_sta_axis_index]
            if (self._data_dict and 
                CONFIG.OPTION['data dict scope plot'] and
                paraname in self._data_dict):
                pn = self._data_dict[paraname][0]
                if pn != 'NaN':
                    paraname = pn
            message = QMessageBox.warning(self,
                  QCoreApplication.translate('FastPlotCanvas', '删除曲线'),
                  QCoreApplication.translate('FastPlotCanvas', '确定要删除曲线：' + paraname + '吗？'),
                  QMessageBox.Yes | QMessageBox.No)
            if (message == QMessageBox.Yes):
                self.restore_axes_info()
                self.delete_para_data(self.selected_sta_axis_index)
                self.count_axes = len(self.sorted_paralist)
                self.signal_adjust_win.emit()
                self.plot_total_data()
                        
#    重载缩放函数
    def slot_pan(self):
        
        self.cid_press_pan = self.mpl_connect('button_press_event',
                                              self.slot_press_pan)
        self.cid_move_pan = self.mpl_connect('motion_notify_event',
                                             self.slot_move_pan)
        self.cid_release_pan = self.mpl_connect('button_release_event',
                                                self.slot_release_pan)
        
    def slot_press_pan(self, event):
        
        if event.inaxes and (event.button == 1 or event.button == 3):
            ax = self.selected_sta_axis
            ax_inv = ax.transData.inverted()
            x0data, self.real_init_cursor_ypos = ax_inv.transform(event.inaxes.transData.transform((event.xdata, event.ydata)))
            y0data = (ax.get_yticks()[2] + ax.get_yticks()[0]) / 2
            self.init_cursor_pos = (x0data, y0data)
            self.init_xlim = ax.get_xlim()
            init_ylim = ax.get_ylim()
            x_frac = (self.init_cursor_pos[0] - self.init_xlim[0]) / (self.init_xlim[1] - self.init_xlim[0])
            y_frac = (self.real_init_cursor_ypos - init_ylim[0]) / (init_ylim[1] - init_ylim[0])
            self.init_view_ylim = (ax.get_yticks()[0], ax.get_yticks()[2])
            self.init_pos_frac = (x_frac, y_frac)
    
    def slot_move_pan(self, event):
#        将self.init_cursor_pos作为判据是由于当使用完对话框后关闭event的button始终为1
        if event.inaxes and (event.button == 1 or event.button == 3) and self.init_cursor_pos:
            ax = self.selected_sta_axis
            ax_inv = ax.transData.inverted()
            new_pos = ax_inv.transform(event.inaxes.transData.transform((event.xdata, event.ydata)))
            dx = new_pos[0] - self.init_cursor_pos[0]
            dy = new_pos[1] - self.real_init_cursor_ypos
            xl, xr = ax.get_xlim()
            yl, yu = ax.get_ylim()
#            平移
            if event.button == 1:
#                每次执行完该函数，鼠标所在的x值就是最初的x值
                xl -= dx
                xr -= dx
                yl = ax.get_yticks()[0] - dy
                yu = ax.get_yticks()[2] - dy
#            缩放
            if event.button == 3:
                new_xpos_frac = (new_pos[0] - xl) / (xr - xl)
                xl = self.init_cursor_pos[0] - (self.init_cursor_pos[0] - self.init_xlim[0]) * pow(10, self.init_pos_frac[0] - new_xpos_frac)
                xr = self.init_cursor_pos[0] + (self.init_xlim[1] - self.init_cursor_pos[0]) * pow(10, self.init_pos_frac[0] - new_xpos_frac)
                new_ypos_frac = (new_pos[1] - yl) / (yu - yl)
                yl = self.init_cursor_pos[1] - (self.init_cursor_pos[1] - self.init_view_ylim[0]) * pow(10, self.init_pos_frac[1] - new_ypos_frac)
                yu = self.init_cursor_pos[1] + (self.init_view_ylim[1] - self.init_cursor_pos[1]) * pow(10, self.init_pos_frac[1] - new_ypos_frac)
#                yl, yu = self.tran_ra_va(ax,
#                                         self.selected_sta_axis_index,
#                                         yl, yu)
            ax.set_xlim(xl, xr)
            yl, yu = self.reg_ylim(yl, yu)
            self.adjust_view_axis(ax, self.selected_sta_axis_index, yl, yu)
                
            self.draw()
            
    def slot_release_pan(self, event):
        
        self.init_cursor_pos = None
        self.init_xlim = None
        self.init_ylim = None
        self.init_ylim_factor = None
        
    def slot_disconnect_pan(self):
        
        if self.cid_press_pan and self.cid_move_pan and self.cid_release_pan:
            self.mpl_disconnect(self.cid_press_pan)
            self.mpl_disconnect(self.cid_move_pan)
            self.mpl_disconnect(self.cid_release_pan)
            self.cid_press_pan = None
            self.cid_move_pan = None
            self.cid_release_pan = None
        
    def slot_clear_canvas(self):
        
        SingleAxisXTimePlotCanvas.slot_clear_canvas(self)
        self.selected_sta_axis = None
        self.selected_sta_axis_index = 0
        
    def plot_paras(self, datalist, sorted_paras):

        self.restore_axes_info()
        is_plot = self.process_data(datalist, sorted_paras, self.dict_filetype)
        
        if is_plot:
            self.count_axes = len(self.sorted_paralist)
            self.signal_adjust_win.emit()
            self.plot_total_data()
            
    def plot_total_data(self):
        
#        y坐标的实际刻度数
        self.num_yscales = 22
#        y轴标签间间隔的刻度数
        self.num_scales_between_ylabel = 3
#        每个坐标用多少个实际刻度显示，取偶数
        self.num_view_yscales = 4
#        坐标的刻度用几个实际刻度显示，目前只显示三个刻度值，所以除以2
        self.num_yview_scales = self.num_view_yscales / 2
                            
        self.fig.clf()
        self.color_index = 0
        count = len(self.sorted_paralist)
        if count > 7:
            n = count - 7
            self.num_yscales = 22 + self.num_scales_between_ylabel * (n - 1) + self.num_view_yscales
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
        host.set_xlabel('时间', fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
        host.grid(which='major',linestyle='--',color = '0.45')
        host.grid(which='minor',linestyle='--',color = '0.75')
        host.xaxis.set_major_formatter(FuncFormatter(self.my_format))
        host.xaxis.set_major_locator(MaxNLocator(nbins=6))
        host.xaxis.set_minor_locator(AutoMinorLocator(n=2))
        host.yaxis.set_major_locator(LinearLocator(numticks=self.num_yscales+1))

        for i, para_tuple in enumerate(self.sorted_paralist):
            self.signal_progress.emit(int(i/count*100))
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
                            lw = 1,
                            gid = 'dataline_' + paraname)
                    ax.set_ylabel(pn, fontproperties = CONFIG.FONT_MSYH,
                                  color = self.curve_colors[self.color_index])
                else:
                    ax.plot(self.time_series_list[index], 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1,
                            gid = 'dataline_' + paraname)
                    ax.set_ylabel(pn, fontproperties = CONFIG.FONT_MSYH, 
                                  color = self.curve_colors[self.color_index])
            else:
                ax.plot(self.time_series_list[index], 
                        self.total_data[index].data[paraname],
                        color = self.curve_colors[self.color_index],
                        lw = 1,
                        gid = 'dataline_' + paraname)
                ax.set_ylabel(paraname, fontproperties = CONFIG.FONT_MSYH, 
                              color = self.curve_colors[self.color_index])
            
            if i == 0:
                self.change_sel_axis(ax, 0)
            ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
            ax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.tick_params(axis='y', colors=self.curve_colors[self.color_index])
            plt.setp(ax.get_xticklabels(), visible = False)
            ax.yaxis.tick_left()
            ax.yaxis.set_label_position('left')
            ax.spines['left'].set_color(self.curve_colors[self.color_index])
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            llimit, ulimit = ax.get_ylim()
            yl, yu = self.reg_ylim(llimit, ulimit)
            flag = i
            if flag % 2 == 1:
                ax.spines['left'].set_position(('axes', -0.14))
            else:
                ax.spines['left'].set_position(('axes', -0.03))
            self.adjust_view_axis(ax, i, yl, yu)

#                一共有十种颜色可用
            if self.color_index == 9:
                self.color_index = 0
            else:
                self.color_index += 1
                
        self.init_axes_lim = {}
        self.init_axes_lim = self.get_current_axes_lim()
        self.refresh_axes_status()
        self.adjust_figure()
        
#    根据存储的坐标信息，把重画后的坐标状态还原
    def refresh_axes_status(self):
        
        axes = self.fig.axes
#        参考坐标内是不画曲线的
        if axes and ((len(axes) - 1) == len(self.sorted_paralist)):
            axes = axes[1 : ]
            for i, para_tuple in enumerate(self.sorted_paralist):
                ax = axes[i]
                paraname, index = para_tuple
                if paraname in self.axes_info:
                    if index == self.axes_info[paraname]['scr_index']:
                        
                        ax.set_xlim(self.axes_info[paraname]['xlim'])
                        yl, yu = self.axes_info[paraname]['ylim']
                        
                        ax.tick_params(axis = 'y', colors = self.axes_info[paraname]['color'])
                        ax.spines['left'].set_color(self.axes_info[paraname]['color'])
                        ax.set_ylabel(self.axes_info[paraname]['ylabel'], fontproperties = CONFIG.FONT_MSYH, 
                                      color = self.axes_info[paraname]['color'])

                        self.adjust_view_axis(ax, i, yl, yu)
                        self.refresh_axes_artist_status(self.axes_info[paraname], ax)
            if 'sel_sta_axis' in self.axes_info:         
                if self.axes_info['sel_sta_axis'] < len(self.sorted_paralist):
                    self.change_sel_axis(axes[self.axes_info['sel_sta_axis']], self.axes_info['sel_sta_axis'])
                else:
                    self.change_sel_axis(axes[len(self.sorted_paralist) - 1], len(self.sorted_paralist) - 1)

    def adjust_figure(self):
        
        h = self.height()
        w = self.width()
#        设置图四边的空白宽度 
        bottom_gap = round(50 / h, 2)
        right_gap = round((w - 40) / w, 2)       
        left_gap = 0.21
        top_gap = round((h - 40) / h, 2)

        self.fig.subplots_adjust(left=left_gap,bottom=bottom_gap,
                                 right=right_gap,top=top_gap,hspace=0.16)
        self.draw()
        
    def adjust_savefig(self):
        
#        图注高度
        legend_h = 18
#        画布尺寸
        if self.count_axes <= 7:
            h = legend_h * 3 + (3 * (7 - 1) + 4) * 20
        else:
            h = legend_h * 3 + (3 * (self.count_axes - 1) + 4) * 20
        w = 650
        bottom_gap = round(legend_h * 2 / h, 2)
        right_gap = round((w - 10) / w, 2)
        left_gap = 0.21
        top_gap = round((h - legend_h) / h, 2)
        self.resize(w, h)
        self.fig.subplots_adjust(left = left_gap, bottom = bottom_gap,
                                 right = right_gap, top = top_gap)
        
    def restore_axes_info(self):

        axes = self.fig.axes
        if axes and ((len(axes) - 1) == len(self.sorted_paralist)):
            axes = axes[1 : ]
            self.axes_info = {}
            self.axes_info['sel_sta_axis'] = self.selected_sta_axis_index
            for i, pn_info in enumerate(self.sorted_paralist):
                pn, scr_index = pn_info
                self.axes_info[pn] = {}
                self.axes_info[pn]['scr_index'] = scr_index
                self.axes_info[pn]['ylabel'] = axes[i].get_ylabel()
                self.axes_info[pn]['xlim'] = axes[i].get_xlim()
                self.axes_info[pn]['ylim'] = (axes[i].get_yticks()[0], axes[i].get_yticks()[2])
                self.axes_info[pn]['color'] = axes[i].spines['left'].get_edgecolor()
                self.restore_axes_artist_info(self.axes_info[pn], axes[i])
        
#    规整可视坐标的上下限
    def reg_ylim(self, yl, yu):
        
        old_view_scale = (yu - yl) / (self.num_view_yscales / self.num_yview_scales)
        new_view_scale = self.reg_scale(old_view_scale)
        base_mid = int((yl + yu) / 2 / new_view_scale)
        bias_mid = (yl + yu) / 2 / new_view_scale - base_mid
#                正数的四舍五入，实数的则要考虑负数的情况，这里bias_mid肯定是正数
        if bias_mid > 0.5:
            base_mid += 1
        mid = base_mid * new_view_scale
        lb = mid - new_view_scale
        ub = mid + new_view_scale
        
        return (lb, ub)
    
    def tran_ra_va(self, ax, ax_index, yl, yu):
        
        real_scale = (yu - yl) / self.num_yscales
        view_yl = yl + (self.num_yscales - self.num_scales_between_ylabel * ax_index - self.num_view_yscales) * real_scale
        view_yu = yu - self.num_scales_between_ylabel * ax_index * real_scale
        return (view_yl, view_yu)
    
#    显示可视坐标
    def adjust_view_axis(self, ax, ax_index, view_yl, view_yu):
        
        real_scale = (view_yu - view_yl) / self.num_view_yscales
        ax.set_yticks([view_yl, (view_yl + view_yu) / 2, view_yu])
        ax.spines['left'].set_bounds(view_yl, view_yu)
        ax.set_ylabel(ax.get_ylabel(),
                      y = 1 - (self.num_scales_between_ylabel * ax_index + self.num_yview_scales) / self.num_yscales,
                      picker = 1)
        ax.set_ylim(view_yl - (self.num_yscales - self.num_scales_between_ylabel * ax_index - self.num_view_yscales) * real_scale, 
                    view_yu + self.num_scales_between_ylabel * ax_index * real_scale)
        plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)
        
#    规整刻度值
    def reg_scale(self, scale):
        
        base_values = [1, 2, 5]
        digits = 0
        init_value = scale
        result = 0
        abs_scale = scale = abs(scale)
        if scale >= 1:
            while scale != 0:
                scale = int(scale / 10)
                digits += 1
            t_delta = -1
            for base in base_values:
                delta = abs(base * pow(10, digits - 1) - abs_scale) 
                if t_delta == -1:
                    t_delta = delta
                    result =  base * pow(10, digits - 1)
                else:
                    if delta < t_delta:
                        t_delta = delta
                        result =  base * pow(10, digits - 1)
        elif scale != 0:
            while scale < 1:
                scale = scale * 10
                digits += 1
            t_delta = -1
            for base in base_values:
                delta = abs(base * pow(10, -digits) - abs_scale) 
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
    
    def change_sel_axis(self, ax, ax_index):
        
#        以下代码实现添加选中效果
        if self.selected_sta_axis:
            self.selected_sta_axis.set_ylabel(self.selected_sta_axis.get_ylabel(),
                                              bbox = None)
            self.selected_sta_axis = ax
            self.selected_sta_axis_index = ax_index
            self.selected_sta_axis.set_ylabel(self.selected_sta_axis.get_ylabel(),
                                              bbox = dict(boxstyle = 'round,pad=0.5', fc = 'none'))
        else:
            self.selected_sta_axis = ax
            self.selected_sta_axis_index = ax_index
            self.selected_sta_axis.set_ylabel(self.selected_sta_axis.get_ylabel(),
                                              bbox = dict(boxstyle = 'round,pad=0.5', fc = 'none'))
    
    def visible_axis_sel_status(self, flag):
        
        if flag:
            self.selected_sta_axis.set_ylabel(self.selected_sta_axis.get_ylabel(),
                                              bbox = dict(boxstyle = 'round,pad=0.5', fc = 'none'))
        else:
            self.selected_sta_axis.set_ylabel(self.selected_sta_axis.get_ylabel(),
                                              bbox = None)
            
    def get_current_axes_lim(self):
        
        axes_lim = {}
        label = ''
        if self.fig.axes:
            for i, ax in enumerate(self.fig.axes):
                if i != 0:
                    label = 'axis_' + str(i)
                    ylim = (ax.get_yticks()[0], ax.get_yticks()[2])
                    axes_lim[label] = (ax, i - 1, ax.get_xlim(), ylim)
                
        return axes_lim
                
    def set_axes_init_lim(self, axes_lim : dict):
        
        if axes_lim:
            for label, ax_info in axes_lim.items():
                ax, ax_i, xlim, ylim = ax_info
                ax.set_xlim(xlim[0], xlim[1])
                self.adjust_view_axis(ax, ax_i, ylim[0], ylim[1])
            self.draw()




