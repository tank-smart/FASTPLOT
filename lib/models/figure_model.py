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
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
from matplotlib.ticker import FuncFormatter, AutoMinorLocator, MaxNLocator, LinearLocator
import pandas as pd
from models.datafile_model import Normal_DataFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton

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
        axes=df.plot(para_list[0],ax=self.ax,grid=True,fontsize=8,subplots=True,sharex=True)
        for eachax in axes:
            eachax.legend(fontsize=6,loc='lower left', bbox_to_anchor=(0,1.01),ncol=2)
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