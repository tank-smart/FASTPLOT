 # -*- coding: utf-8 -*-
# =============================================================================
# =======概述
# 文件名：figure_model.py
# 简述：绘图类
#
# =======内容
# 包含类：
# PlotCanvasBase
# FastPlotCanvas
# SingleAxisPlotCanvasBase
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
import scipy.io as sio
import numpy as np
import pandas as pd
# 用于绘图的包
import matplotlib
matplotlib.use('Qt5Agg')
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
from PyQt5.QtWidgets import (QMenu, QAction, QMessageBox, QDialog, QFileDialog)
# 自定义的包
import views.config_info as CONFIG
from views.custom_dialog import (Base_LineSettingDialog, LineSettingDialog, 
                                 AnnotationSettingDialog, Base_AxisSettingDialog, 
                                 AxisSettingDialog, StackAxisSettingDialog, 
                                 DisplayParaAggregateInfoDialog)
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
        self.mpl_connect('pick_event', self.on_pick)
        
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
                if type(event.artist) == Annotation:
                    self.picked_annotation = event.artist
                    self.create_move_annotation_event(event)
            if event.mouseevent.button == 3:
                if (type(event.artist) == Line2D or type(event.artist) == Annotation):
                    self.picked_del_artist = event.artist

        else:
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
            event.canvas.draw()
    
    def set_annotation_props(self, event):
        
        annotation = event.artist
        dialog = AnnotationSettingDialog(self, annotation)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.current_text_color = dialog.text_color
            self.current_text_size = dialog.text_size
            self.current_text_arrow = dialog.text_arrow
            event.canvas.draw()
    
    def create_move_annotation_event(self, event):
        
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
                                      c = self.current_markline_color,
                                      ls = self.current_markline_style,
                                      marker = self.current_markline_marker,
                                      picker = 5)
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
                                       size = self.current_text_size,
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
        self.fig.clf()
        self.draw()

    def custom_plot(self):
        
        pass
    
#    当新建一种画布类时必须画布布局函数
    def adjust_figure(self):

        raise KeyError('must overload function \'adjust_figure\'(FastPlot).')
        
    def adjust_savefig(self):
        
        raise KeyError('must overload function \'adjust_savefig\'(FastPlot).')
        
    def update_config_info(self):
        
        self.current_markline_color = CONFIG.OPTION['plot markline color']
        self.current_markline_style = CONFIG.OPTION['plot markline style']
        self.current_markline_marker = CONFIG.OPTION['plot markline marker']
        self.current_text_color = CONFIG.OPTION['plot fontcolor']
        self.current_text_size = CONFIG.OPTION['plot fontsize']
        self.current_text_arrow = CONFIG.OPTION['plot font arrow']

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
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
#        当前的数据字典
        self._data_dict = {}
#        参数数据相关变量
#        数据
        self.total_data = {}
#        时间
        self.time_series_list = {}
#        已创建的DataFactory个数
        self.count_created_data = 0
#        顺序排列的参数及其对应的数据索引
        self.sorted_paralist = []
        
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
#                        把时间列读出来，因为matplotlib只识别ndarray，所以进行类型转换
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
                        QCoreApplication.translate('PlotCanvas', '绘图提示'),
                        QCoreApplication.translate('PlotCanvas', print_para))
#            如果要绘制的参数都在，则不执行画图函数
            if len(exit_paras) == len(sorted_paras):
                return False
            else:
                return True

    def slot_clear_canvas(self):
        
        PlotCanvasBase.slot_clear_canvas(self)
        self.total_data = {}
        self.sorted_paralist = []
        self.time_series_list = {}
        self.count_created_data = 0

#    当新建一种画布类时必须重载绘图函数
    def plot_paras(self, datalist, sorted_paras):
        
        raise KeyError('must overload function \'plot_paras\'(FastPlot).')    
        
class FastPlotCanvas(FTDataPlotCanvasBase):
    
    signal_cursor_xdata = pyqtSignal(str, list)
#    signal_send_time = pyqtSignal()
#    signal_send_tinterval = pyqtSignal(tuple)
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
        
        self.cid_display_paravalue = None
        
        self.action_display_data_info = QAction(self)
        self.action_display_data_info.setText(QCoreApplication.
                                              translate('PlotCanvas', '数据聚合'))
        self.action_display_data_info.triggered.connect(self.slot_display_aggregate_info)
        
    def custom_context_menu(self, event):
#        如果重载函数内有单独使用self变量的情况，调用重载函数时需要加上self作为参数
        menu = PlotCanvasBase.custom_context_menu(self, event)
        menu.addSeparator()
        menu.addAction(self.action_display_data_info)
        return menu
    
    def set_line_props(self, event):
        
        line = event.artist
        dialog = LineSettingDialog(self, line)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.current_markline_color = dialog.line_color
            self.current_markline_style = dialog.line_ls
            self.current_markline_marker = dialog.line_marker
            event.canvas.draw()
    
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
            
    def slot_onpress_new_vline(self, event):

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
            real_time, para_values = self.get_paravalue(datatime_sel)
            
            if real_time != '':
                rt = mdates.date2num(Time_Model.str_to_datetime(real_time))
                self.current_axes.axvline(rt, c = self.current_markline_color,
                                          ls = self.current_markline_style,
                                          marker = self.current_markline_marker,
                                          picker = 5)
                self.current_axes.annotate(s = '时间 = ' + real_time + '\n' + para_values[index][0] + ' = ' + str(para_values[index][1]),
                                           xy = (rt, para_values[index][1]),
                                           color = self.current_markline_color,
                                           size = self.current_text_size,
                                           picker = 1,
                                           arrowprops = dict(arrowstyle = '->',
                                                             color = self.current_markline_color,
                                                             visible = self.current_text_arrow),
                                           fontproperties = font)
                self.draw()
        if event.button == 1:
            self.slot_disconnect()

    def slot_connect_display_paravalue(self):
        
        self.cid_display_paravalue = self.mpl_connect('motion_notify_event',
                                                      self.slot_display_paravalue)
    
    def slot_diaconnect_display_paravalue(self):
        
        self.mpl_disconnect(self.cid_display_paravalue)

    def slot_display_paravalue(self, event):
        
        if event.inaxes:
            datatime_sel = mdates.num2date(event.xdata)
            real_time, para_values = self.get_paravalue(datatime_sel)
            self.signal_cursor_xdata.emit(real_time, para_values)
            
    def my_format(self, x, pos=None):
        
        x = matplotlib.dates.num2date(x)
        return Time_Model.datetime_to_timestr(x)
            
    def get_paravalue(self, dt):
        
        paravalue = []
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
            if pv != None:
                paravalue.append((paraname, pv))
            else:
                paravalue.append((paraname, 'NaN'))
        return (time_str, paravalue)

    def plot_paras(self, datalist, sorted_paras):

        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
#            axis0 = self.fig.axes
#            xlim = None
#            if axis0:
#                xlim = axis0[0].get_xlim()
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
                self.signal_progress.emit(int(i/count*100))
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
#                    if xlim:
#                        ax.set_xlim(xlim)
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
                
            self.adjust_figure()
            
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
        
class SingleAxisPlotCanvasBase(FTDataPlotCanvasBase):
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
        self.count_axes = 1
        
    def slot_axis_setting(self):
        
        dialog = Base_AxisSettingDialog(self, self.axis_menu_on)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            self.draw()
            
    def plot_paras(self, datalist, sorted_paras, xpara=None):

        is_plot = self.process_data(datalist, sorted_paras)
        xpara = "FCM1_Voted_Mach"
        for index in self.total_data:
            
            if xpara not in self.total_data[index].data_paralist:
                
                print_message = self.total_data[index].filedir
                QMessageBox.information(self,
                        QCoreApplication.translate('PlotCanvas', '绘图提示'),
                        QCoreApplication.translate('PlotCanvas', print_message+'绘图失败'))
                return
                
        
        if xpara == None:
            xdata = "self.time_series_list[index]"
        else:
            xdata = "self.total_data[index].data[xpara]"
            
        
        if is_plot:
            self.fig.clf()
            matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
            matplotlib.rcParams['ytick.direction'] = 'in'
#            支持中文显示
#            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['axes.unicode_minus'] = False
            
            count = len(self.sorted_paralist)
            self.count_curves = count
    
            axeslist = []
            self.color_index = 0
            for i, para_tuple in enumerate(self.sorted_paralist):
                self.signal_progress.emit(int(i/count*100))
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
                        ax.plot(eval(xdata), 
                                self.total_data[index].data[paraname],
                                label = pn,
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                    else:
                        ax.plot(eval(xdata), 
                                self.total_data[index].data[paraname],
                                color = self.curve_colors[self.color_index],
                                lw = 1)
                else:
                    ax.plot(eval(xdata), 
                            self.total_data[index].data[paraname],
                            color = self.curve_colors[self.color_index],
                            lw = 1)
                
                if i != (count - 1):
                    plt.setp(ax.get_xticklabels(), visible = False)
                else:
                    xlabel = xpara
                    if (self._data_dict and 
                    CONFIG.OPTION['data dict scope plot'] and
                    paraname in self._data_dict):
                        xlabel = self._data_dict[xpara][0]
                        xunit = self._data_dict[xpara][1]
                    if xlabel != 'NaN':
                        if xunit != 'NaN' and xunit != '1':
                            xlabel = xlabel + '(' + xunit + ')'
                    
                    ax.set_xlabel(xlabel, fontproperties = CONFIG.FONT_MSYH, labelpad = 2)
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
#                ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
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
                
            self.adjust_figure()
            self.xaxes_flag = xpara #标志x轴是否为时间
            
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
        self.count_axes = 1
        
    def slot_onpress_new_vline(self, event):

        PlotCanvasBase.slot_onpress_new_vline(self, event)
        
    def plot_paras(self, datalist, sorted_paras):

        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
            self.fig.clf()
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
                
            self.adjust_figure()
            
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
        
class StackAxisPlotCanvas(FastPlotCanvas):
    
    def __init__(self, parent = None):
    
        super().__init__(parent)
#        不显示右键的坐标设置
        self.action_axis_setting.setVisible(False)

#        缩放
        self.cid_press_pan = None
        self.cid_release_pan = None
        self.cursor_xpos = None
        self.xlim = None
#        坐标设置相关的变量
        self.selected_axis = None
        self.num_ygrads = 0
        self.num_ylabel_inter_grads = 0
        self.num_y_subgrads = 0
        self.grads_y_sub = 0
        
#    pick函数
    def on_pick(self, event):
        
        FastPlotCanvas.on_pick(self, event)
        
        if event.mouseevent.dblclick and type(event.artist) == Text:
            ylabel = event.artist
            axes = self.fig.axes
            for i, axis in enumerate(axes):
                if ylabel.get_text() == axis.get_ylabel():
#                    以下代码实现添加选中效果
#                    if self.selected_axis:
#                        self.selected_axis.set_ylabel(self.selected_axis.get_ylabel(), bbox = None)
#                        self.selected_axis = axis
#                        self.selected_axis.set_ylabel(self.selected_axis.get_ylabel(), bbox = dict(boxstyle = 'round,pad=0.5', fc = 'none'))
#                    else:
#                        self.selected_axis = axis
#                        self.selected_axis.set_ylabel(self.selected_axis.get_ylabel(), bbox = dict(boxstyle = 'round,pad=0.5', fc = 'none'))
#                    self.draw()
                    layout_info = (self.num_ygrads, self.num_ylabel_inter_grads,
                                   self.num_y_subgrads, self.grads_y_sub, i - 1)
                    dialog = StackAxisSettingDialog(self, axis, layout_info)
                    return_signal = dialog.exec_()
                    if (return_signal == QDialog.Accepted):
#                    self.axis_menu_on.remove()
                        event.canvas.draw()
                        
#    重载缩放函数
    def slot_pan(self):
        
        self.cid_press_pan = self.mpl_connect('motion_notify_event',
                                              self.slot_press_pan)
        self.cid_release_pan = self.mpl_connect('button_release_event',
                                                    self.slot_release_pan)
        
    def slot_press_pan(self, event):
        
        if event.inaxes and event.button == 1:
            ax = event.inaxes
            if self.cursor_xpos:
                dx = event.xdata - self.cursor_xpos
                if self.count_axes:
                    l, r = ax.get_xlim()
                    ax.set_xlim(l - dx, r - dx)
                self.draw()
            else:
                self.cursor_xpos = event.xdata
        if event.inaxes and event.button == 3:
            ax = event.inaxes
            if self.cursor_xpos and self.xlim:
                dx = event.xdata - self.cursor_xpos
                if self.count_axes:
                    l, r = self.xlim
                    ax.set_xlim(l + dx, r - dx)
                self.draw()
            else:
                self.cursor_xpos = event.xdata
                self.xlim = ax.get_xlim()
            
    def slot_release_pan(self, event):
        
        self.cursor_xpos = None
        self.xlim = None
        
    def slot_disconnect_pan(self):
        
        if self.cid_press_pan and self.cid_release_pan:
            self.mpl_disconnect(self.cid_press_pan)
            self.mpl_disconnect(self.cid_release_pan)
            self.cid_press_pan = None
            self.cid_release_pan = None
            
    def slot_onpress_new_vline(self, event):

        PlotCanvasBase.slot_onpress_new_vline(self, event)
        
    def plot_paras(self, datalist, sorted_paras):

#        y坐标的实际刻度数
        self.num_ygrads = num_ygrads = 22
#        y轴标签间间隔的刻度数
        self.num_ylabel_inter_grads = num_ylabel_inter_grads = 3
#        每个坐标用多少个实际刻度显示，取偶数
        self.num_y_subgrads = num_y_subgrads = 4
#        坐标的刻度用几个实际刻度显示，目前只显示三个刻度值，所以除以2
        self.grads_y_sub = grads_y_sub = num_y_subgrads / 2
        is_plot = self.process_data(datalist, sorted_paras)
        
        if is_plot:
            
            self.fig.clf()
            self.color_index = 0
            count = len(self.sorted_paralist)
            self.count_axes = count
            if count > 7:
                n = count - 7
                self.num_ygrads = num_ygrads = 22 + num_ylabel_inter_grads * (n - 1) + num_y_subgrads
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
            host.yaxis.set_major_locator(LinearLocator(numticks=num_ygrads+1))
            
            axeslist = []
            axeslist.append(host)

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
                ax.tick_params(axis='y', colors=self.curve_colors[self.color_index])
                plt.setp(ax.get_xticklabels(), visible = False)
                ax.yaxis.tick_left()
                ax.yaxis.set_label_position('left')
                ax.spines['left'].set_color(self.curve_colors[self.color_index])
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                llimit, ulimit = ax.get_ylim()
                new_delta = self.num_adjust((ulimit - llimit) / 2)
                base_mid = int((llimit + ulimit) / 2 / new_delta)
                bias_mid = (llimit + ulimit) / 2 / new_delta - base_mid
#                正数的四舍五入，实数的则要考虑负数的情况，这里bias_mid肯定是正数
                if bias_mid > 0.5:
                    base_mid += 1
                mid = base_mid * new_delta
                lb = mid - new_delta
                ub = mid + new_delta
                flag = i
                if flag % 2 == 1:
                    ax.spines['left'].set_position(('axes', -0.14))
                else:
                    ax.spines['left'].set_position(('axes', -0.03))
                ax.set_yticks([lb,(lb + ub) / 2, ub])
                ax.spines['left'].set_bounds(lb, ub)
                ax.set_ylabel(ax.get_ylabel(),
                              y = 1 - (num_ylabel_inter_grads * flag + grads_y_sub) / num_ygrads,
                              picker = 1)
                ax.set_ylim(lb - (num_ygrads - num_ylabel_inter_grads * flag - num_y_subgrads) * new_delta / grads_y_sub, 
                            ub + num_ylabel_inter_grads * flag * new_delta / grads_y_sub)
                plt.setp(ax.get_yticklabels(), fontproperties = CONFIG.FONT_MSYH)

    #                一共有十种颜色可用
                if self.color_index == 9:
                    self.color_index = 0
                else:
                    self.color_index += 1
            
            self.adjust_figure()
            self.draw()

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
        h = self.height()
        w = 650
        bottom_gap = round(legend_h * 2 / h, 2)
        right_gap = round((w - 10) / w, 2)
        left_gap = 0.21
        top_gap = round((h - legend_h) / h, 2)
        self.resize(w, h)
        self.fig.subplots_adjust(left = left_gap, bottom = bottom_gap,
                                 right = right_gap, top = top_gap)
        
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




