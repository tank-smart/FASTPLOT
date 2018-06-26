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
sys.path.append(r"D:\Program Files\git\DAGUI\lib")

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#------王--改动开始
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
from PyQt5.QtCore import pyqtSignal, QDataStream, QIODevice
#------王--改动结束
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
from matplotlib.ticker import FuncFormatter, AutoMinorLocator, MaxNLocator, LinearLocator
import pandas as pd
from models.datafile_model import Normal_DataFile
from PyQt5.QtWidgets import QSizePolicy
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
    signal_disconnect_addline = pyqtSignal()
#    临时信号，用于把拖进来的参数传给绘图窗口绘图
    signal_temp = pyqtSignal(dict)
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
        self.setAcceptDrops(True)
#        定义下面这个变量是为了存入模板
        self.paralist = []
        self.line = None

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
            while (not item_stream.atEnd()):
                paraname = item_stream.readQString()
                file_dir = item_stream.readQString()
                if not (file_dir in paras):
                    paras[file_dir] = []
                    paras[file_dir].append(paraname)
                else:
                    paras[file_dir].append(paraname)  
            self.signal_temp.emit(paras)
            event.acceptProposedAction()
        else:
            event.ignore()

    def slot_use_subline(self, isconnect):
        
        if isconnect:
            self.cid_press = self.fig.canvas.mpl_connect('button_press_event',
                                                         self.slot_press_mouse)
            self.cid_move = self.fig.canvas.mpl_connect('motion_notify_event', 
                                                        self.slot_move_mouse)
        else:
            self.fig.canvas.mpl_disconnect(self.cid_move)
            self.fig.canvas.mpl_disconnect(self.cid_press)     
    
    def slot_press_mouse(self, event):
        
        x = event.xdata
        if self.line:
            pass
        else:
            self.line = event.inaxes.axvline(x, linestyle = '--')
        event.canvas.draw()
        
    def slot_move_mouse(self, event):
        
        if event.button == 1:
            x = event.xdata
            self.line.set_xdata([x, x])
            event.canvas.draw()
        
        
#------王--改动结束

#define the user-defined format for datatime display: HH:MM:SS:ms        
    def my_format(self, x, pos=None):
        x = matplotlib.dates.num2date(x)
        fmt = '%H:%M:%S:%f' 
        label = x.strftime(fmt)
        label = label[0:-3]
        return label

    def plot_para(self,source=None,para_list=[]):
        if isinstance(source,(str)): #python 2 add unicode
            file_plot=Normal_DataFile(source)
            para_list.insert(0,file_plot.paras_in_file[0])
            df=file_plot.cols_input(source,para_list)
        elif isinstance(source,pd.DataFrame):
            df=source
        else:
            return
        df[para_list[0]]=pd.to_datetime(df[para_list[0]],format='%H:%M:%S:%f')
        #ax1 = self.fig.add_subplot(4,1,self.pos)
        ax1=self.fig.add_axes(self.poslist[self.pos])
        #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))#设置时间标签显示格式
        ax1.xaxis.set_major_formatter(FuncFormatter(self.my_format)) #use self-defined format set the xaxis
        #plt.xticks(pd.date_range('2014-09-01','2014-09-30'),rotation=90)
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f')) # 显示时间坐标的格式
    
#        autodates= AutoDateLocator()                # 时间间隔自动选取
#        ax1.xaxis.set_major_locator(autodates)
        df.plot(para_list[0],ax=ax1,grid=True,fontsize=6,rot=0)
        ax1.legend(fontsize=6,loc='lower center', bbox_to_anchor=(0,1.01),ncol=2) #move legend to outside center up
        self.draw()
#        self.show()
        #plt.show()
        if self.pos<3:
            self.pos+=1
        else:
            self.pos=0

    def subplot_para(self,source=None,para_list=[]):
        if isinstance(source,(str)): #python 2 add unicode
            file_plot=Normal_DataFile(source)
            para_list.insert(0,file_plot.paras_in_file[0])
            df=file_plot.cols_input(source,para_list)
        elif isinstance(source,pd.DataFrame):
            df=source
        else:
            return
        df[para_list[0]]=pd.to_datetime(df[para_list[0]],format='%H:%M:%S:%f')
        self.fig.clf()
        #ax1 = self.fig.add_subplot(4,1,self.pos)
        self.ax=self.fig.add_axes([0.1,0.2,0.8,0.6])
#        self.fig.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.95,hspace=0.3)
        #self.fig.subplots_adjust(0.1,0.5,0.9,0.95,0.3)
#        self.ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
        matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
        matplotlib.rcParams['ytick.direction'] = 'in'
        axes=df.plot(para_list[0],ax=self.ax,grid=True,fontsize=6,subplots=True,sharex=True)
        for eachax in axes:
            eachax.legend(fontsize=6,loc='lower left', bbox_to_anchor=(0,1.01),ncol=2)
            eachax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            eachax.xaxis.set_minor_locator(AutoMinorLocator())
            eachax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            eachax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
            for label in eachax.xaxis.get_ticklabels():
                label.set_horizontalalignment('center')
                label.set_rotation('horizontal')
            eachax.grid(which='both',linestyle='--')
#        self.ax.legend(fontsize=6,loc='lower left', bbox_to_anchor=(0,1.01),ncol=2)
#        self.ax.xaxis.set_major_formatter(FuncFormatter(self.my_format)) 
        self.fig.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.95,hspace=0.3)
#        for label in self.ax.xaxis.get_ticklabels():
#            print(label.get_rotation())
#            label.set_horizontalalignment('center')
#            label.set_rotation('horizontal')

#            print(label.horizontalalignment)
        self.draw()
#        self.show()
        #plt.show()
        if self.pos<3:
            self.pos+=1
        else:
            self.pos=0

#------王--改动开始            
    def subplot_para_wxl(self,source=None,para_list=[]):

        self.paralist = para_list.copy()
        
        if isinstance(source,(str)): #python 2 add unicode
            file_plot=Normal_DataFile(source)
            para_list.insert(0,file_plot.paras_in_file[0])
            df=file_plot.cols_input(source,para_list)
        elif isinstance(source,pd.DataFrame):
            df=source
        else:
            return
        df[para_list[0]]=pd.to_datetime(df[para_list[0]],format='%H:%M:%S:%f')
        self.fig.clf()
        #ax1 = self.fig.add_subplot(4,1,self.pos)
        self.ax=self.fig.add_axes([0.1,0.1,0.8,0.8])
#        self.fig.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.95,hspace=0.3)
        #self.fig.subplots_adjust(0.1,0.5,0.9,0.95,0.3)
#        self.ax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
        matplotlib.rcParams['xtick.direction'] = 'in' #设置刻度线向内
        matplotlib.rcParams['ytick.direction'] = 'in'
#        axes=df.plot(para_list[0],ax=self.ax,grid=True,fontsize=6,subplots=True,sharex=True)
        axes=df.plot(para_list[0],ax=self.ax,grid=True,fontsize=8,subplots=True,sharex=True)
        for eachax in axes:
            eachax.legend(fontsize=8,loc=(0,1) , ncol=1 , frameon=False,
                          markerscale = 2, edgecolor = "inherit")
            eachax.xaxis.set_major_formatter(FuncFormatter(self.my_format))
            eachax.xaxis.set_major_locator(LinearLocator(numticks=10))
            eachax.xaxis.set_minor_locator(AutoMinorLocator(n=2))
            eachax.yaxis.set_major_locator(LinearLocator(numticks=5))
            eachax.yaxis.set_minor_locator(AutoMinorLocator(n=2))
            for label in eachax.xaxis.get_ticklabels():
                label.set_horizontalalignment('center')
                label.set_rotation('horizontal')
            eachax.grid(which='major',linestyle='--',color = '0.45')
            eachax.grid(which='minor',linestyle='--',color = '0.75')
#        self.ax.legend(fontsize=6,loc='lower left', bbox_to_anchor=(0,1.01),ncol=2)
#        self.ax.xaxis.set_major_formatter(FuncFormatter(self.my_format)) 
        self.fig.subplots_adjust(left=0.07,bottom=0.07,right=0.95,top=0.95,hspace=0.2)
#        for label in self.ax.xaxis.get_ticklabels():
#            print(label.get_rotation())
#            label.set_horizontalalignment('center')
#            label.set_rotation('horizontal')

#            print(label.horizontalalignment)
        self.draw()
#        self.show()
        #plt.show()
        if self.pos<3:
            self.pos+=1
        else:
            self.pos=0

    def slot_resize_canvas(self, size):

        if self.fig.axes:
            print("\nXXX\nScrollArea")
            print("Width" + str(size.width()) + " Height" + str(size.height()))
            print("PlotArea")
            print("Width" + str(self.width()) + " Height" + str(self.height()))
            print('')
            self.resize(size.width(), self.height())
        else:
            print("Initial")
            print("Width" + str(size.width()) + " Height" + str(size.height()))
            self.resize(size)

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
        
    

if __name__ == "__main__":
    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    #filename=u"D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664003-16.txt"
    #filename=u"C:/Users/admin/Desktop/5008问题汇总.xlsx"
    #df=chunk_input(filename,sep='all')
    #df=all_input(filename)
    file_plot=Normal_DataFile(filename)
    para_name=file_plot.header_input(filename,sep='all')
    #df=cols_input(filename,["time","HF_FSECU_1_L354_HLS_OMS_Status_Flap_Inoperative","FCM3_Voted_True_Airspeed"])
        #df=cols_input(filename,[u"日期"]
    #df.plot("time","FCM3_Voted_True_Airspeed")
    #plt.show()
    #plt.figure()
    #plt.plot(df["time"],df["FCM3_Voted_True_Airspeed"])
    #plt.show()
    #para_list=["time","HF_FSECU_1_L354_HLS_OMS_Status_Flap_Inoperative","FCM3_Voted_True_Airspeed"]
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