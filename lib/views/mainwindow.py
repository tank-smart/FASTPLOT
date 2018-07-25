# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：主窗口类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================

# =============================================================================
# Stdlib imports
# =============================================================================
import sys
import os

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QObject,QSize, QRect, Qt, QCoreApplication, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QCloseEvent
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QMenuBar, 
                             QFileDialog, QMessageBox, QMenu, QToolBar, 
                             QAction, QStatusBar, QHBoxLayout, QStackedWidget)

# =============================================================================
# Package views imports
# =============================================================================
from views.data_export_window import DataExportWindow
from views.plot_window import PlotWindow
from views.paralist_window import ParalistWindow
from models.datafile_model import Normal_DataFile
from views.data_manage_window import DataManageWindow
from views.data_analysis_window import DataAnalysisWindow
import views.src_icon as ICON
# =============================================================================
# Main Window
# =============================================================================
class MainWindow(QMainWindow):   

    signal_import_datafiles = pyqtSignal(dict)
    signal_send_export_temps = pyqtSignal(dict, dict)
    signal_send_plot_temps = pyqtSignal(dict, dict)
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)
#        设置窗口图标
        self.setWindowIcon(QIcon(ICON.ICON_WINDOW))

#        所涉及的结果文件，列表类型
        self.resultfile_group = []
#        导出参数的模板
        self.para_export_temps = {}
#        绘图的模板
        self.plot_temps = {}
#        软件的配置信息
        self.config_info = {"INIT DIR OF IMPORTING FILES" : ""}

# =============================================================================
# UI模块
# =============================================================================
    def setup(self):
        
#        加载参数模板到内存，给para_export_temps赋值
        self.load_temps()
#        定义主窗口
#        主窗口内统一使用一种字体
        font = QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.setEnabled(True)
        self.setMinimumSize(QSize(900, 600))
        self.setWindowState(Qt.WindowMaximized)

#        创建堆叠窗口        
        self.mw_stacked_window = QStackedWidget(self)
        self.data_export_page = DataExportWindow(self)
        self.data_export_page.setup()
        self.mw_stacked_window.addWidget(self.data_export_page)
        self.plot_page = PlotWindow(self)
        self.plot_page.setup()
        self.mw_stacked_window.addWidget(self.plot_page)
        self.mathematics_page = QWidget(self)
        self.mw_stacked_window.addWidget(self.mathematics_page)
        self.data_analysis_page = DataAnalysisWindow(self)
        self.data_analysis_page.setup()
        self.mw_stacked_window.addWidget(self.data_analysis_page)
        self.data_manage_page = DataManageWindow(self)
        self.data_manage_page.setup()
        self.mw_stacked_window.addWidget(self.data_manage_page)
        self.mw_stacked_window.setCurrentIndex(0)
        self.mw_stacked_window.hide()

#        创建参数列表窗口
        self.mw_paralist_window = ParalistWindow(self)
        self.mw_paralist_window.setup()
        self.addDockWidget(Qt.DockWidgetArea(1), self.mw_paralist_window)

#        设置主窗口布局
        self.mainwindow_layout = QWidget(self)
        self.mainwindow_layout.setObjectName("mainwindow_layout")        
        self.horizontalLayout = QHBoxLayout(self.mainwindow_layout)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.mw_stacked_window)
        self.setCentralWidget(self.mainwindow_layout)
        
#        创建菜单栏
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_open = QMenu(self.menu_file)
        self.menu_open.setObjectName("menu_open")
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName("menu_edit")
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        self.menu_tools = QMenu(self.menubar)
        self.menu_tools.setObjectName("menu_tools")
        self.menu_window = QMenu(self.menubar)
        self.menu_window.setObjectName("menu_window")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.setMenuBar(self.menubar)
        
#        创建状态栏
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
#        创建工具栏
        self.toolbar = QToolBar(self)
        self.toolbar.setObjectName("toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        
#        创建动作
        self.action_open_normal_datafile = QAction(self)
        self.action_open_normal_datafile.setObjectName("action_open_normal_datafile")
        self.action_open_normal_datafile.setIcon(QIcon(ICON.ICON_OPEN))
        self.action_export_data = QAction(self)
        self.action_export_data.setObjectName("action_export_data")
        self.action_export_data.setIcon(QIcon(ICON.ICON_EXPORT))
        self.action_export_data.setCheckable(True)
        self.action_exit = QAction(self)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setIcon(QIcon(ICON.ICON_EIXT))
        self.action_mathematics = QAction(self)
        self.action_mathematics.setObjectName("action_mathematics")
        self.action_mathematics.setIcon(QIcon(ICON.ICON_MATHEMATICS))
        self.action_mathematics.setCheckable(True)
        self.action_data_analysis = QAction(self)
        self.action_data_analysis.setObjectName("action_data_analysis")
        self.action_data_analysis.setIcon(QIcon(ICON.ICON_DATA_ANA))
        self.action_data_analysis.setCheckable(True)
        self.action_data_manage = QAction(self)
        self.action_data_manage.setObjectName("action_data_manage")
        self.action_data_manage.setIcon(QIcon(ICON.ICON_DATA_MAN))
        self.action_data_manage.setCheckable(True)
        self.action_options = QAction(self)
        self.action_options.setObjectName("action_options")
        self.action_options.setIcon(QIcon(ICON.ICON_SETTING))
        self.action_about = QAction(self)
        self.action_about.setObjectName("action_about")
        self.action_about.setIcon(QIcon(ICON.ICON_ABOUT))
        self.action_plot = QAction(self)
        self.action_plot.setObjectName("action_plot")
        self.action_plot.setIcon(QIcon(ICON.ICON_PLOT))
        self.action_plot.setCheckable(True)
        self.action_paralist_dock_isclosed = QAction(self)
        self.action_paralist_dock_isclosed.setCheckable(True)
        self.action_paralist_dock_isclosed.setChecked(True)
        self.action_paralist_dock_isclosed.setObjectName("action_paralist_dock_isclosed")
        
#        将动作添加到对应的菜单下       
        self.menu_open.addAction(self.action_open_normal_datafile)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu_open.menuAction())
        self.menu_file.addAction(self.action_export_data)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_view.addAction(self.action_paralist_dock_isclosed)
        self.menu_tools.addAction(self.action_plot)
        self.menu_tools.addAction(self.action_mathematics)
        self.menu_tools.addAction(self.action_data_analysis)
        self.menu_tools.addAction(self.action_data_manage)
        self.menu_tools.addAction(self.action_options)
        self.menu_help.addAction(self.action_about)

#        添加菜单栏
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu_window.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
#        添加工具栏
        self.toolbar.addAction(self.action_open_normal_datafile)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_plot)
        self.toolbar.addAction(self.action_export_data)
        self.toolbar.addAction(self.action_mathematics)
        self.toolbar.addAction(self.action_data_analysis)
        self.toolbar.addAction(self.action_data_manage)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_about)

        self.retranslate()
        
# =======连接信号与槽
# =============================================================================
#       主窗口的信号连接        
        self.action_open_normal_datafile.triggered.connect(
                self.slot_open_normal_datafile)
#        按下按钮显示相应的页面
        self.action_export_data.triggered.connect(self.slot_show_page)
        self.action_plot.triggered.connect(self.slot_show_page)
        self.action_mathematics.triggered.connect(self.slot_show_page)
        self.action_data_analysis.triggered.connect(self.slot_show_page)
        self.action_data_manage.triggered.connect(self.slot_show_page)
#        按下视图菜单栏下的关闭动作
        self.action_paralist_dock_isclosed.triggered.connect(
                self.slot_paralist_dock_isclosed)
#        程序的关于信息
        self.action_about.triggered.connect(self.slot_about)
#        程序退出
        self.action_exit.triggered.connect(self.slot_exit)
        
        self.signal_import_datafiles.connect(self.mw_paralist_window.slot_import_datafiles)
# =============================================================================
#       参数窗口的信号连接
#        将参数窗口中选中的参数传递给导出窗口中显示
        self.mw_paralist_window.signal_export_para.connect(
                self.action_export_data.trigger)
        self.mw_paralist_window.signal_export_para.connect(
                self.data_export_page.slot_import_para)
#        绘图
        self.mw_paralist_window.signal_quick_plot.connect(
                self.action_plot.trigger)
        self.mw_paralist_window.signal_quick_plot.connect(
                self.plot_page.slot_plot)
        self.mw_paralist_window.signal_close.connect(
                self.slot_paralist_dock_close)
#        数据导出窗口与主窗口的信号与槽连接
        self.data_export_page.signal_get_export_temps.connect(
                self.slot_send_export_temps)
        self.signal_send_export_temps.connect(
                self.data_export_page.slot_sel_temp)
        self.data_export_page.signal_save_temp.connect(
                self.slot_save_export_temp)
#        数据导出窗口与主窗口的信号与槽连接 
        self.plot_page.signal_get_plot_temps.connect(
                self.slot_send_plot_temps)
        self.signal_send_plot_temps.connect(
                self.plot_page.slot_sel_temp)
        self.plot_page.signal_save_temp.connect(
                self.slot_save_plot_temp)
        

# =============================================================================
# Slots模块            
# =============================================================================
    def closeEvent(self, event : QCloseEvent):
        self.output_temps()
        event.accept()

#    打开数据文件并将文件信息存入
    def slot_open_normal_datafile(self):
        
        file_dirs = {}
        init_dir = self.config_info["INIT DIR OF IMPORTING FILES"]
        if init_dir:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, 'Open', init_dir, "Datafiles (*.txt *.csv *.dat)")
        else:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, 'Open', r'E:\\', "Datafiles (*.txt *.csv *.dat)")
        if file_dir_list:
            file_dir_list = [file.replace('/','\\') for file in file_dir_list]
            if os.path.exists(file_dir_list[0]):
                self.config_info["INIT DIR OF IMPORTING FILES"] = os.path.dirname(file_dir_list[0])
            for file_dir in file_dir_list:
                try:
                    nor_file = Normal_DataFile(file_dir)
                    file_dirs[file_dir] = nor_file.paras_in_file
                except:
                    info = "文件" + "<br>" + file_dir + "<br>打开失败"
                    QMessageBox.information(self,
                        QCoreApplication.translate("DataExportWindow", "打开文件提示"),
                        QCoreApplication.translate("DataExportWindow", info)) 
        self.signal_import_datafiles.emit(file_dirs)

#    与关于退出有关的显示
    def slot_exit(self):
        
        QApplication.closeAllWindows()
            
#    显示About信息
    def slot_about(self):
        
        QMessageBox.about(self,
            QCoreApplication.translate("MainWindow", "关于FastPlot"),
            QCoreApplication.translate("MainWindow", """<b>FastPlot</b>
            <br>试飞数据绘图软件
            <br>Copyright &copy; FTCC
            <p>由试飞中心试飞工程部绘图软件开发团队开发维护
            """))

#    响应参数窗口显示动作
    def slot_paralist_dock_isclosed(self):
        
        if self.mw_paralist_window.isHidden():
            self.mw_paralist_window.setHidden(False)
        else:
            self.mw_paralist_window.setHidden(True)

#        参数窗口关闭后需要把视图下的勾选去掉
    def slot_paralist_dock_close(self):
        
        self.action_paralist_dock_isclosed.setChecked(False)
        
#    显示用户选择的界面
    def slot_show_page(self):
        
#        接收发出信号的那个对象
        sender = QObject.sender(self)
        if self.mw_stacked_window.isHidden():
#            软件启动时堆叠窗口是不显示的
            self.mw_stacked_window.setHidden(False)
            if (sender == self.action_export_data):
#                显示页面
                self.show_page(0)
#                将此次选择记住
                self.last_page = self.action_export_data
            if (sender == self.action_plot):
                self.show_page(1)
                self.last_page = self.action_plot
            if (sender == self.action_mathematics):
                self.show_page(2)
                self.last_page = self.action_mathematics
            if (sender == self.action_data_analysis):
                self.show_page(3)
                self.last_page = self.action_data_analysis
            if (sender == self.action_data_manage):
                self.show_page(4)
                self.last_page = self.action_data_manage               
        else:
            if (sender == self.action_export_data):
                if (self.last_page == self.action_export_data):
#                    再次按下同一按钮且按钮是选择状态，按钮会自动弹起，
#                    但这不是我们期望的，所以设置动作仍被选择
                    self.action_export_data.setChecked(True)
                else:
#                    将上一选中动作按钮弹起
                    self.last_page.setChecked(False)
                    self.show_page(0)
#                    将新的选择记住
                    self.last_page = self.action_export_data
            if (sender == self.action_plot):
                if (self.last_page == self.action_plot):
                    self.action_plot.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.show_page(1)
                    self.last_page = self.action_plot
            if (sender == self.action_mathematics):
                if (self.last_page == self.action_mathematics):
                    self.action_mathematics.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.show_page(2)
                    self.last_page = self.action_mathematics
            if (sender == self.action_data_analysis):
                if (self.last_page == self.action_data_analysis):
                    self.action_data_analysis.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.show_page(3)
                    self.last_page = self.action_data_analysis
            if (sender == self.action_data_manage):
                if (self.last_page == self.action_data_manage):
                    self.action_data_manage.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.show_page(4)
                    self.last_page = self.action_data_manage
    
    def slot_save_export_temp(self, temp):

        if temp:
            for name in temp:
                self.para_export_temps[name] = temp[name]
    
    def slot_send_export_temps(self):
        
        dict_files = self.mw_paralist_window.get_dict_files_tree()
        self.signal_send_export_temps.emit(dict_files, self.para_export_temps)
        
    def slot_save_plot_temp(self, temp):

        if temp:
            for name in temp:
                self.plot_temps[name] = temp[name]
    
    def slot_send_plot_temps(self):
        
        dict_files = self.mw_paralist_window.get_dict_files_tree()
        self.signal_send_plot_temps.emit(dict_files, self.plot_temps)

# =============================================================================
# 功能函数模块
# =============================================================================
#    从文件中加载参数模板进入内存
    def load_temps(self):
        
#        导入导出参数的模板
        try:
            with open(r"E:\\DAGUI\\data\\templates_export_paras.txt", 'r') as file:
                while file.readline():
    #                readline函数会把'\n'也读进来
                     name = file.readline()
    #                 去除'\n'
                     name = name.strip('\n')
                     str_paralist = file.readline()
                     str_paralist = str_paralist.strip('\n')
                     paralist = str_paralist.split(' ')
                     self.para_export_temps[name] = paralist
        except IOError:
#            对抛出的文件错误，不予理睬
            pass
        
#        导入绘图模板
        try:
            with open(r"E:\\DAGUI\\data\\templates_plot.txt", 'r') as file:
                while file.readline():
    #                readline函数会把'\n'也读进来
                     name = file.readline()
    #                 去除'\n'
                     name = name.strip('\n')
                     str_paralist = file.readline()
                     str_paralist = str_paralist.strip('\n')
                     paralist = str_paralist.split(' ')
                     self.plot_temps[name] = paralist
        except IOError:
            pass
        
#        导入配置信息
        try:
            with open(r"E:\\DAGUI\\data\\config_info.txt", 'r') as file:
                while file.readline():
    #                readline函数会把'\n'也读进来
                     name = file.readline()
    #                 去除'\n'
                     name = name.strip('\n')
                     config = file.readline()
                     config = config.strip('\n')
                     if name == "INIT DIR OF IMPORTING FILES":
                         if os.path.exists(config):
                             self.config_info[name] = config
                         else:
                             self.config_info[name] = ""
                     else:
                         self.config_info[name] = config
        except IOError:
            pass 
    
#    将内存中的模板导出到文件
    def output_temps(self):

#        判断是否有模板存在
        if self.para_export_temps:
#                打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(r"E:\\DAGUI\\data\\templates_export_paras.txt", 'w') as file:
#                将内存中的模板一一写入文件
                for temp in self.para_export_temps:
                    file.write("========\n")
                    file.write(temp)
                    file.write('\n')
                    paralist = ''
                    index = 1
                    length = len(self.para_export_temps[temp])
                    for para in self.para_export_temps[temp]:
                        if index == length:
                            paralist += (para + '\n')
                        else:
                            paralist += (para + ' ')
                        index += 1
                    file.write(paralist)
                    
#        判断是否有模板存在
        if self.plot_temps:
#                打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(r"E:\\DAGUI\\data\\templates_plot.txt", 'w') as file:
#                将内存中的模板一一写入文件
                for temp in self.plot_temps:
                    file.write("========\n")
                    file.write(temp)
                    file.write('\n')
                    paralist = ''
                    index = 1
                    length = len(self.plot_temps[temp])
                    for para in self.plot_temps[temp]:
                        if index == length:
                            paralist += (para + '\n')
                        else:
                            paralist += (para + ' ')
                        index += 1
                    file.write(paralist)

#        判断是否有模板存在
        if self.config_info:
#                打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(r"E:\DAGUI\data\config_info.txt", 'w') as file:
#                将内存中的模板一一写入文件
                for name in self.config_info:
                    file.write("========\n")
                    file.write(name)
                    file.write('\n')
                    file.write(self.config_info[name])
                    file.write('\n')

    def show_page(self, pageindex):
        if self.mw_stacked_window.isHidden():
            self.mw_stacked_window.show()
            self.mw_stacked_window.setCurrentIndex(pageindex)
        else:
            self.mw_stacked_window.setCurrentIndex(pageindex)
    
# =============================================================================
# 汉化
# =============================================================================
    def retranslate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "FastPlot"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_open.setTitle(_translate("MainWindow", "打开"))
        self.menu_edit.setTitle(_translate("MainWindow", "编辑"))
        self.menu_view.setTitle(_translate("MainWindow", "视图"))
        self.menu_tools.setTitle(_translate("MainWindow", "工具"))
        self.menu_window.setTitle(_translate("MainWindow", "窗口"))
        self.menu_help.setTitle(_translate("MainWindow", "帮助"))
        self.mw_paralist_window.setWindowTitle(_translate("MainWindow", "参数窗口"))
        self.mw_paralist_window.line_edit_search_para.setPlaceholderText(_translate("MainWindow", "过滤器"))
        self.toolbar.setWindowTitle(_translate("MainWindow", "工具栏"))
        self.action_open_normal_datafile.setText(_translate("MainWindow", "通用数据"))
        self.action_open_normal_datafile.setToolTip(_translate("MainWindow", "打开通用数据"))
        self.action_export_data.setText(_translate("MainWindow", "导出数据"))
        self.action_export_data.setToolTip(_translate("MainWindow", "导出数据文件"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_mathematics.setText(_translate("MainWindow", "数学计算"))
        self.action_data_analysis.setText(_translate("MainWindow", "数据分析"))
        self.action_data_manage.setText(_translate("MainWindow", "数据管理"))
        self.action_options.setText(_translate("MainWindow", "选项"))
        self.action_about.setText(_translate("MainWindow", "关于"))
        self.action_plot.setText(_translate("MainWindow", "绘图"))
        self.action_paralist_dock_isclosed.setText(_translate("MainWindow", "参数窗口"))
        
def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setup()
    mainwindow.show()
    return app.exec_()