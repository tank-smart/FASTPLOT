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

# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QObject,QSize, QRect, Qt, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QMenuBar, 
                             QFileDialog, QMessageBox, QMenu, QToolBar, 
                             QAction, QStatusBar, QHBoxLayout)

# =============================================================================
# Package views imports
# =============================================================================
from stacked_window import StackedWindow
from paralist_window import ParalistWindow
from models.project_model import ProjectModel

# =============================================================================
# Main Window
# =============================================================================
class MainWindow(QMainWindow):   

# =============================================================================
# 自定义信号模块
# =============================================================================

    
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        super().__init__(parent)
#        设置窗口图标
        self.setWindowIcon(QIcon(r"E:\DAGUI\lib\icon\window.png"))
        self.project = ProjectModel()

# =============================================================================
# UI模块
# =============================================================================
    def setup(self):
#        定义主窗口
        self.setEnabled(True)
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))
        self.setWindowState(Qt.WindowMaximized)

#        创建堆叠窗口        
        self.mw_stacked_window = StackedWindow(self)
        self.mw_stacked_window.setup()
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
        self.action_open_normal_datafile.setIcon(QIcon(r"E:\DAGUI\lib\icon\open.ico"))
        self.action_export_data = QAction(self)
        self.action_export_data.setObjectName("action_export_data")
        self.action_export_data.setIcon(QIcon(r"E:\DAGUI\lib\icon\export.ico"))
        self.action_export_data.setCheckable(True)
        self.action_exit = QAction(self)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setIcon(QIcon(r"E:\DAGUI\lib\icon\exit.png"))
        self.action_mathematics = QAction(self)
        self.action_mathematics.setObjectName("action_mathematics")
        self.action_mathematics.setIcon(QIcon(r"E:\DAGUI\lib\icon\caculator.ico"))
        self.action_mathematics.setCheckable(True)
        self.action_data_manipulation = QAction(self)
        self.action_data_manipulation.setObjectName("action_data_manipulation")
        self.action_data_manipulation.setIcon(QIcon(r"E:\DAGUI\lib\icon\datamanipulate.ico"))
        self.action_data_manipulation.setCheckable(True)
        self.action_data_manage = QAction(self)
        self.action_data_manage.setObjectName("action_data_manage")
        self.action_data_manage.setIcon(QIcon(r"E:\DAGUI\lib\icon\datamanage.ico"))
        self.action_data_manage.setCheckable(True)
        self.action_options = QAction(self)
        self.action_options.setObjectName("action_options")
        self.action_options.setIcon(QIcon(r"E:\DAGUI\lib\icon\setting.ico"))
        self.action_about = QAction(self)
        self.action_about.setObjectName("action_about")
        self.action_about.setIcon(QIcon(r"E:\DAGUI\lib\icon\information.ico"))
        self.action_plot = QAction(self)
        self.action_plot.setObjectName("action_plot")
        self.action_plot.setIcon(QIcon(r"E:\DAGUI\lib\icon\quick_plot.ico"))
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
        self.menu_tools.addAction(self.action_data_manipulation)
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
        self.toolbar.addAction(self.action_export_data)
        self.toolbar.addAction(self.action_plot)
        self.toolbar.addAction(self.action_mathematics)
        self.toolbar.addAction(self.action_data_manipulation)
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
        self.action_data_manipulation.triggered.connect(self.slot_show_page)
        self.action_data_manage.triggered.connect(self.slot_show_page)
#        按下视图菜单栏下的关闭动作
        self.action_paralist_dock_isclosed.triggered.connect(
                self.slot_paralist_dock_isclosed)
#        程序的关于信息
        self.action_about.triggered.connect(self.slot_about)
#        程序退出
        self.action_exit.triggered.connect(self.slot_exit)
# =============================================================================
#       参数窗口的信号连接
#        将参数窗口中选中的参数传递给导出窗口中显示
        self.mw_paralist_window.signal_export_para.connect(
                self.action_export_data.trigger)
        self.mw_paralist_window.signal_export_para.connect(
                self.mw_stacked_window.qwidget_data_export.import_para)
#        绘图
        self.mw_paralist_window.signal_quick_plot.connect(
                self.action_plot.trigger)
        self.mw_paralist_window.signal_quick_plot.connect(
                self.mw_stacked_window.qwidget_plot.plot)
        self.mw_paralist_window.signal_search_para.connect(
                self.slot_search_para)
        self.mw_paralist_window.signal_close.connect(
                self.slot_paralist_dock_close)

# =============================================================================
# Slots模块            
# =============================================================================
#    搜索参数并显示在参数窗口里
    def slot_search_para(self, paraname):
        
        result = self.project.search_para(paraname)
        self.mw_paralist_window.display_file_group(result, True)

#    打开数据文件并将文件信息存入project中
    def slot_open_normal_datafile(self):
        
        file_name, ok = QFileDialog.getOpenFileNames(
                self, 'Open', r'E:\\', "Datafiles (*.txt *.csv *.dat)")
        file_name = [file.replace('/','\\') for file in file_name]
        self.project.open_normal_datafiles(file_name)
        self.mw_paralist_window.display_file_group(
                self.project.get_datafile_for_tree())

#    与关于退出有关的显示
    def slot_exit(self):
        
        QApplication.closeAllWindows()
            
#    显示About信息
    def slot_about(self):
        
        QMessageBox.about(self,
            QCoreApplication.translate("MainWindow", "关于演示程序"),
            QCoreApplication.translate("MainWindow", """<b>演示程序</b>
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
                self.mw_stacked_window.show_page(0)
#                将此次选择记住
                self.last_page = self.action_export_data
            if (sender == self.action_plot):
                self.mw_stacked_window.show_page(1)
                self.last_page = self.action_plot
            if (sender == self.action_mathematics):
                self.mw_stacked_window.show_page(2)
                self.last_page = self.action_mathematics
            if (sender == self.action_data_manipulation):
                self.mw_stacked_window.show_page(3)
                self.last_page = self.action_data_manipulation
            if (sender == self.action_data_manage):
                self.mw_stacked_window.show_page(4)
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
                    self.mw_stacked_window.show_page(0)
#                    将新的选择记住
                    self.last_page = self.action_export_data
            if (sender == self.action_plot):
                if (self.last_page == self.action_plot):
                    self.action_plot.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.mw_stacked_window.show_page(1)
                    self.last_page = self.action_plot
            if (sender == self.action_mathematics):
                if (self.last_page == self.action_mathematics):
                    self.action_mathematics.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.mw_stacked_window.show_page(2)
                    self.last_page = self.action_mathematics
            if (sender == self.action_data_manipulation):
                if (self.last_page == self.action_data_manipulation):
                    self.action_data_manipulation.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.mw_stacked_window.show_page(3)
                    self.last_page = self.action_data_manipulation
            if (sender == self.action_data_manage):
                if (self.last_page == self.action_data_manage):
                    self.action_data_manage.setChecked(True)                  
                else:
                    self.last_page.setChecked(False)
                    self.mw_stacked_window.show_page(4)
                    self.last_page = self.action_data_manage

# =============================================================================
# 功能函数模块
# =============================================================================


# =============================================================================
# 汉化
# =============================================================================
    def retranslate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "演示程序"))
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
        self.action_data_manipulation.setText(_translate("MainWindow", "数据操作"))
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