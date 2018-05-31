# -*- coding: utf-8 -*-
"""
Created on Sun May 20 21:53:22 2018

@author: Yan Hua
"""
import sys
sys.path.append(r"E:\DAGUI\lib")

import matplotlib
#matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
from matplotlib.ticker import FuncFormatter
import pandas as pd
from models.datafile_model import Normal_DataFile
#from datafile_model import Normal_DataFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton


#------------
#use plot_para() to plot 4*1 figure
#use add_toolbar(self,parent=None) to add toolbar, toolbar is qt widget, set parent of toolbar
#use show_toolbar(self,toolbar) or toolbar.show() display the toolbar
class PlotCanvas(FigureCanvas):
    
    def __init__(self,parent=None,width=5,height=4,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=dpi)
        #self.fig=plt.figure()
        self.poslist=[[0.1, 0.77, 0.75, 0.18],[0.1, 0.53, 0.75, 0.18],[0.1, 0.29, 0.75, 0.18],[0.1, 0.05, 0.75, 0.18]]
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
        #self.draw()
        self.show()
        #plt.show()
        if self.pos<3:
            self.pos+=1
        else:
            self.pos=0

        
#    def plot_para_time(self,source=None,para_list=[]):
#        if isinstance(source,(str,unicode)): #！！！！python 2
#            file_plot=Normal_DataFile(source)
#            para_list.insert(0,file_plot.paras_in_file[0])
#            df=file_plot.cols_input(source,para_list)
#        elif isinstance(source,pd.DataFrame):
#            df=source
#        else:
#            return
#        df[para_list[0]]=pd.to_datetime(df[para_list[0]],format='%H:%M:%S:%f')
#        ax1 = self.fig.add_subplot(1,1,1)
#        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S:%f'))#设置时间标签显示格式
#        #plt.xticks(pd.date_range('2014-09-01','2014-09-30'),rotation=90)
#        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f')) # 显示时间坐标的格式
#    
#        #autodates= AutoDateLocator()                # 时间间隔自动选取
#        #plt.gca().xaxis.set_major_locator(autodates)
#        df.plot(para_list[0],ax=ax1,grid=True,fontsize=6)
#        ax1.legend(fontsize=6,loc='lower center', bbox_to_anchor=(0.5,1.01),ncol=2)
#        #self.draw()
#        self.show()
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
    
        
    

if __name__ == "__main__":
    #filename=u"D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    #filename=u"D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664003-16.txt"
    filename=r"E:\\data.txt"
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