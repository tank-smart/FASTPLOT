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
import views.constant as CONSTANT
from views.custom_dialog import (LineSettingDialog, AnnotationSettingDialog,
                                 AxisSettingDialog, FigureCanvasSetiingDialog)
from PyQt5.QtGui import QIcon
#------王--改动结束
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
from matplotlib.ticker import FuncFormatter, AutoMinorLocator, MaxNLocator, LinearLocator, FixedLocator
import pandas as pd
from models.datafile_model import Normal_DataFile
from PyQt5.QtWidgets import QSizePolicy, QMenu, QAction, QMessageBox, QDialog
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
    signal_send_save_paravalue = pyqtSignal()

#------王--改动结束
    
    def __init__(self,parent=None,width=10,height=4,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=dpi)
        #self.fig=plt.figure()
        self.poslist=[[0.1, 0.77, 0.8, 0.18],[0.1, 0.53, 0.8, 0.18],[0.1, 0.29, 0.8, 0.18],[0.1, 0.05, 0.8, 0.18]]
        #self.poslist=[[0.1,0.75,0.8,0.23],[0.1,0.5,0.8,0.23],[0.1,0.25,0.8,0.23],[0.1,0,0.8,0.23]]
        self.pos=0
        #self.axes = fig.add_subplot(111)# 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        #self.axes = fig.add_axes([0,0,1,1])
        FigureCanvas.__init__(self, self.fig)# 初始化父类
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
#        self.toolbar=self.add_toolbar()
        self.toolbar=CustomToolbar(self,parent=None)
        self.toolbar.hide()
#------王--改动开始

#        存储曲线颜色
        prop_cycle = plt.rcParams['axes.prop_cycle']
#        默认的是十种颜色
        self.curve_colors = prop_cycle.by_key()['color']
        self.color_index = 0
#        存储参数数据
        self.total_data = []
        self.time_series_list = []
        self.sorted_paralist = []
#        定义下面这个变量是为了存入模板
        self.paralist = []
        
#        当前鼠标在坐标内的光标样式
        self.current_cursor_inaxes = None
#        当前鼠标所在的坐标
        self.current_axes = None

#        单击右键选到要删除的文字标注或标记线
        self.picked_del_artist = None
        
        self.axis_menu_on = None
        
        self.current_markline_color = 'black'
        self.current_markline_style = '--'
        
        self.cid_press_new_hline = None
        self.cid_press_new_vline = None
        self.cid_move_new_line = None
        self.cid_release_new_line = None
        self.newline = None
        
        self.show_hgrid = True
        self.show_vgrid = True
        
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
        self.action_save_paravalue = QAction(self)
        self.action_save_paravalue.setText(QCoreApplication.
                                         translate('PlotCanvas', '保存此刻参数值'))
        self.action_axis_setting = QAction(self)
        self.action_axis_setting.setText(QCoreApplication.
                                         translate('PlotCanvas', '坐标轴设置'))
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
                                           translate('PlotCanvas', '删除'))
        self.action_del_artist.setIcon(QIcon(CONSTANT.ICON_DEL))
        self.action_add_text = QAction(self)
        self.action_add_text.setIcon(QIcon(CONSTANT.ICON_TEXT))
        self.action_add_text.setText(QCoreApplication.
                                     translate('PlotCanvas', '添加文字'))
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
        
        self.action_save_paravalue.triggered.connect(self.slot_save_paravalue)

        self.mpl_connect('motion_notify_event', self.slot_set_cursor)
        
#        Pick事件在进行缩放移动、框选缩放时不会触发，但是press事件却会触发，不知道为何
        self.mpl_connect('pick_event', self.on_pick)
        
    def slot_set_display_menu(self, is_display):

        self.is_display_menu = is_display
        
    def slot_on_tree_context_menu(self, event):
        
#        禁止缩放过程中弹出右键菜单
        if self.fig.axes and event.button == 3 and self.is_display_menu:
#            只要弹出了右键菜单，就把所有连接都断开
            self.slot_disconnect(event)
            menu = QMenu(self)
            menu.addActions([self.action_show_hgrid, 
                             self.action_show_vgrid,
                             self.action_save_paravalue,
                             self.action_axis_setting,
                             self.action_add_text])
            menu_markline = QMenu(menu)
            menu_markline.setIcon(QIcon(CONSTANT.ICON_ADD_LINE_MARK))
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
                
            if self.is_save_paravalue:
                self.action_save_paravalue.setEnabled(True)
            else:
                self.action_save_paravalue.setEnabled(False)
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
            self.slot_disconnect(event)
    
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
            self.slot_disconnect(event)
        
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
            self.slot_disconnect(event)
        
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
        
        if event.inaxes and event.button == 1:
            self.current_axes.annotate(s = r'Text', 
                                      xy = (event.xdata, event.ydata),
                                      color = self.current_text_color,
                                      style = self.current_text_style,
                                      size = self.current_text_size,
                                      picker = 1)
            self.draw()
        if event.button == 1:
            self.slot_disconnect(event)
        
    def slot_move_annotation(self, event):
        
        if event.inaxes and event.button == 1:
            x0, y0, mx0, my0 = self.annotation_init_loc
            dx = event.xdata - mx0
            dy = event.ydata - my0
            self.picked_annotation.set_position((x0 + dx, y0 + dy))
            self.draw()
            
    def slot_release_annotation(self, event):
         
        if event.button == 1:
            self.slot_disconnect(event)

    def slot_set_cursor(self, event):
        
#        当鼠标在坐标轴内保持当前特定的光标状态，否则为箭头
        if event.inaxes and self.current_cursor_inaxes:
            self.setCursor(self.current_cursor_inaxes)
        else:
            self.setCursor(Qt.ArrowCursor)
#         获得鼠标所在坐标轴
        if event.inaxes:
            self.current_axes = event.inaxes
            
    def slot_connect_display_paravalue(self):
        
        self.is_save_paravalue = True
        self.cid_display_paravalue = self.mpl_connect('motion_notify_event',
                                                      self.slot_display_paravalue)
    
    def slot_diaconnect_display_paravalue(self):
        
        self.is_save_paravalue = False
        self.mpl_disconnect(self.cid_display_paravalue)
        
    def slot_save_paravalue(self):
        
        self.signal_send_save_paravalue.emit()
        
    def slot_display_paravalue(self, event):
        
        if event.inaxes:
            time = mdates.num2date(event.xdata).time().isoformat(timespec='milliseconds')
            datatime_sel = mdates.num2date(event.xdata)
            self.signal_cursor_xdata.emit(time, self.get_paravalue(datatime_sel))
        
#    右键菜单时调用；相应动作完成也调用
    def slot_disconnect(self, event):

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
        self.total_data = []
        self.sorted_paralist = []
        self.time_series_list = []
        self.color_index = 0
        
    def slot_plot_setting(self):
        
#        如果有图才弹出设置窗口
        if self.fig.axes:
            dialog = FigureCanvasSetiingDialog(self, self.fig.axes)
            rs = dialog.exec_()
            if rs == QDialog.Accepted:
                self.draw()

    def my_format(self, x, pos=None):
        x = matplotlib.dates.num2date(x)
        fmt = '%H:%M:%S.%f' 
        label = x.strftime(fmt)
        label = label[0:-3]
        return label

    def process_data(self, datalist, sorted_paras):
        
        if datalist:
#            文件加参数列表
            if type(datalist) == dict:
                for filedir in datalist:
                    file = Normal_DataFile(filedir)
                    datalist[filedir].insert(0,file.paras_in_file[0])
                    df = file.cols_input(filedir, datalist[filedir], '\s+')
                    self.total_data.append(df)
#                    把时间列读出来
                    self.time_series_list.append(pd.to_datetime(df.iloc[:, 0],
                                                            format='%H:%M:%S:%f'))
#            dataframe列表
            if type(datalist) == list:
                self.total_data.extend(datalist)
                for df in datalist:
#                    把时间列读出来
                    self.time_series_list.append(pd.to_datetime(df.iloc[:, 0],
                                                            format='%H:%M:%S:%f'))
            for paraname in sorted_paras:
                count_df = 0
                for count_df, df in enumerate(self.total_data):
                    list_para = df.columns.values.tolist()
                    if paraname in list_para:
                        self.sorted_paralist.append((paraname, count_df))
                        break
            
    def get_paravalue(self, dt):
        
        paravalue = []
        for para_tuple in self.sorted_paralist:
            paraname, index= para_tuple
            get_fre = False
            fre = 1
            first_time = self.time_series_list[index][0]
            length_time = len(self.time_series_list[index])
            while (not get_fre) and fre <= length_time:
                next_time = self.time_series_list[index][fre]
                if (first_time.microsecond == next_time.microsecond and
                    (next_time.second - first_time.second) == 1):
                    get_fre = True
                else:
                    fre += 1
            if not get_fre:
                fre = 0
            temp_line_index = int(((dt.hour - first_time.hour) * 3600 +
                                   (dt.minute - first_time.minute) * 60 +
                                   (dt.second - first_time.second) +
                                   (dt.microsecond - first_time.microsecond) / 1000000) * fre)
            if (temp_line_index >= 0 and temp_line_index < length_time):
                paravalue.append((paraname, self.total_data[index][paraname].iloc[temp_line_index]))
            else:
                paravalue.append((paraname, 'NaN'))
        return paravalue
        
    def subplot_para_wxl(self, datalist, sorted_paras):

        self.process_data(datalist, sorted_paras)
        self.paralist.append(sorted_paras)
        
        self.fig.clf()
        matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
        matplotlib.rcParams['ytick.direction'] = 'in'
        
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
            
            ax.plot(self.time_series_list[index], 
                    self.total_data[index][paraname],
                    color = self.curve_colors[self.color_index],
                    lw = 1)
            
            if i != (count - 1):
                plt.setp(ax.get_xticklabels(), visible = False)
            else:
                plt.setp(ax.get_xticklabels(), fontsize = 8,
                         horizontalalignment = 'center',
                         rotation = 'horizontal')
            plt.setp(ax.get_yticklabels(), fontsize = 8)
            ax.legend(fontsize=8,loc=(0,1) , ncol=1 , frameon=False, borderpad = 0.15)
            ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            ax.xaxis.set_major_locator(MaxNLocator(nbins=8))
            ax.xaxis.set_minor_locator(AutoMinorLocator(n=3))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
            ax.grid(which='major',linestyle='--',color = '0.45')
            ax.grid(which='minor',linestyle='--',color = '0.75')
#            一共有十种颜色可用
            if self.color_index == 9:
                self.color_index = 0
            else:
                self.color_index += 1
            
        self.set_subplot_adjust()
#        Easter Egg
#        if count >= 12:
#            QMessageBox.information(self,
#                                    QCoreApplication.translate('PlotCanvas', 'Easter Egg'),
#                                    QCoreApplication.translate('PlotCanvas', '别再画了，图快画到脚上了！'))
            
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