# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-16
# 编码人员：王学良
# 简述：主窗口类
#
# =======使用说明
# 。。。
#
# =======日志
# 
# =============================================================================


# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QRect, Qt, QCoreApplication, pyqtSignal)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication,QWidget, QMainWindow, QMenuBar, 
                             QMessageBox, QMenu, QToolBar, 
                             QAction, QStatusBar, QHBoxLayout)

# =============================================================================
# Package views imports
# =============================================================================
from stacked_widget import StackedWidget
from paralist_dock import ParalistDock

# =============================================================================
# Main Window
# =============================================================================
class MainWindow(QMainWindow):

    #此处定义常量
    
    #此处定义信号
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(r"E:\Demo\lib\icon\window.png"))
        
    def setup(self):
#        定义主窗口
        self.setEnabled(True)
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))

#        创建堆叠窗口        
        self.mw_stacked_widget = StackedWidget()
        self.mw_stacked_widget.setup()
        self.mw_stacked_widget.hide()

#        创建参数列表窗口
        self.mw_paralist_dock = ParalistDock()
        self.mw_paralist_dock.setup()
        self.addDockWidget(Qt.DockWidgetArea(1), self.mw_paralist_dock)

#        设置主窗口布局
        self.mainwindow_layout = QWidget(self)
        self.mainwindow_layout.setObjectName("mainwindow_layout")        
        self.horizontalLayout = QHBoxLayout(self.mainwindow_layout)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.mw_stacked_widget)
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
        self.menu_analysis = QMenu(self.menubar)
        self.menu_analysis.setObjectName("menu_analysis")
        self.menu_mathematics = QMenu(self.menu_analysis)
        self.menu_mathematics.setObjectName("menu_mathematics")
        self.menu_data_manipulation = QMenu(self.menu_analysis)
        self.menu_data_manipulation.setObjectName("menu_data_manipulation")
        self.menu_data_manage = QMenu(self.menu_analysis)
        self.menu_data_manage.setObjectName("menu_data_manage")
        self.menu_plot = QMenu(self.menubar)
        self.menu_plot.setObjectName("menu_plot")
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
        self.action_open_normal_datafile.setIcon(QIcon(r"E:\Demo\lib\icon\open.ico"))
        self.action_export_data = QAction(self)
        self.action_export_data.setObjectName("action_export_data")
        self.action_export_data.setIcon(QIcon(r"E:\Demo\lib\icon\export.ico"))
        self.action_exit = QAction(self)
        self.action_exit.setObjectName("action_exit")
        self.action_simple_math = QAction(self)
        self.action_simple_math.setObjectName("action_simple_math")
        self.action_testpoint_manage = QAction(self)
        self.action_testpoint_manage.setObjectName("action_testpoint_manage")
        self.action_synchronization = QAction(self)
        self.action_synchronization.setObjectName("action_synchronization")
        self.action_tuning = QAction(self)
        self.action_tuning.setObjectName("action_tuning")
        self.action_para_manage = QAction(self)
        self.action_para_manage.setObjectName("action_para_manage")
        self.action_temp_manage = QAction(self)
        self.action_temp_manage.setObjectName("action_temp_manage")
        self.action_options = QAction(self)
        self.action_options.setObjectName("action_options")
        self.action_options.setIcon(QIcon(r"E:\Demo\lib\icon\setting.ico"))
        self.action_about = QAction(self)
        self.action_about.setObjectName("action_about")
        self.action_about.setIcon(QIcon(r"E:\Demo\lib\icon\information.ico"))
        self.action_quick_plot = QAction(self)
        self.action_quick_plot.setObjectName("action_quick_plot")
        self.action_quick_plot.setIcon(QIcon(r"E:\Demo\lib\icon\quick_plot.ico"))
        self.action_custom_defined_plot = QAction(self)
        self.action_custom_defined_plot.setObjectName("action_custom_defined_plot")
        self.action_multi_source_plot = QAction(self)
        self.action_multi_source_plot.setObjectName("action_multi_source_plot")
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
        self.menu_tools.addAction(self.action_options)
        self.menu_help.addAction(self.action_about)
        self.menu_mathematics.addAction(self.action_simple_math)
        self.menu_data_manipulation.addAction(self.action_testpoint_manage)
        self.menu_data_manipulation.addAction(self.action_synchronization)
        self.menu_data_manipulation.addAction(self.action_tuning)
        self.menu_data_manage.addAction(self.action_para_manage)
        self.menu_data_manage.addAction(self.action_temp_manage)
        self.menu_analysis.addAction(self.menu_mathematics.menuAction())
        self.menu_analysis.addAction(self.menu_data_manipulation.menuAction())
        self.menu_analysis.addAction(self.menu_data_manage.menuAction())
        self.menu_plot.addAction(self.action_quick_plot)
        self.menu_plot.addAction(self.action_custom_defined_plot)
        self.menu_plot.addAction(self.action_multi_source_plot)
#        添加菜单栏
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_analysis.menuAction())
        self.menubar.addAction(self.menu_plot.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu_window.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
#        添加工具栏
        self.toolbar.addAction(self.action_open_normal_datafile)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_export_data)
        self.toolbar.addAction(self.action_quick_plot)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_about)

        self.retranslate()
#        QMetaObject.connectSlotsByName(self)
        
# =======连接信号与槽
        self.mw_paralist_dock.signal_close.connect(self.slot_paralist_dock_close)
#        下列动作与槽的连接，对于只在UI层的流程不在控制器类里管理
        self.action_export_data.triggered.connect(self.slot_show_export_data_page)
        self.action_paralist_dock_isclosed.triggered.connect(self.view_paralist_dock_isclosed)
        self.action_about.triggered.connect(self.view_about)
        self.action_exit.triggered.connect(self.view_exit)


# =============================================================================
# Views
# =============================================================================

# =============================================================================
#    与关于退出有关的显示
    def view_exit(self):
        
        QApplication.closeAllWindows()
            
# =============================================================================
#    与关于数据导入有关的显示
            
    def view_data_export(self):
        self.mw_stacked_widget.show()
        list_sel_para = []
        list_temp = self.mw_paralist_dock.tree_widget_display_datafile.selectedItems()
        if list_temp:
            for item in list_temp:
                if item.parent():
                    list_sel_para.append(item.text(0))
        self.mw_stacked_widget.qwidget_data_export.display_sel_para(list_sel_para)
                

# =============================================================================
#    与关于信息显示有关的显示
            
#    显示About信息
    def view_about(self):
        QMessageBox.about(self,
            QCoreApplication.translate("MainWindow", "关于演示程序"),
            QCoreApplication.translate("MainWindow", """<b>演示程序</b>
            <br>试飞数据绘图软件
            <br>Copyright &copy; FTCC
            <p>由试飞中心试飞工程部绘图软件开发团队开发维护
            """))

# =============================================================================
#    与参数窗口有关的显示
        
#    响应参数窗口显示动作
    def view_paralist_dock_isclosed(self):
        if self.mw_paralist_dock.isHidden():
            self.mw_paralist_dock.setHidden(False)
        else:
            self.mw_paralist_dock.setHidden(True)

# =============================================================================
# Slots            
# =============================================================================

#        参数窗口关闭后需要把视图下的勾选去掉
    def slot_paralist_dock_close(self):
        self.action_paralist_dock_isclosed.setChecked(False)
        
    def slot_show_export_data_page(self):
        self.mw_stacked_widget.show_page(0)
#        self.action_export_data.


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
        self.menu_analysis.setTitle(_translate("MainWindow", "分析"))
        self.menu_mathematics.setTitle(_translate("MainWindow", "数学计算"))
        self.menu_data_manipulation.setTitle(_translate("MainWindow", "数据操作"))
        self.menu_data_manage.setTitle(_translate("MainWindow", "数据管理"))
        self.menu_plot.setTitle(_translate("MainWindow", "绘图"))
        self.mw_paralist_dock.setWindowTitle(_translate("MainWindow", "参数窗口"))
        self.mw_paralist_dock.line_edit_search_para.setPlaceholderText(_translate("MainWindow", "过滤器"))
        self.toolbar.setWindowTitle(_translate("MainWindow", "工具栏"))
        self.action_open_normal_datafile.setText(_translate("MainWindow", "通用数据"))
        self.action_open_normal_datafile.setToolTip(_translate("MainWindow", "打开通用数据"))
        self.action_export_data.setText(_translate("MainWindow", "导出数据"))
        self.action_export_data.setToolTip(_translate("MainWindow", "导出数据文件"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_simple_math.setText(_translate("MainWindow", "简单计算"))
        self.action_testpoint_manage.setText(_translate("MainWindow", "试验点"))
        self.action_synchronization.setText(_translate("MainWindow", "时间同步"))
        self.action_tuning.setText(_translate("MainWindow", "调频"))
        self.action_para_manage.setText(_translate("MainWindow", "参数"))
        self.action_temp_manage.setText(_translate("MainWindow", "模板"))
        self.action_options.setText(_translate("MainWindow", "选项"))
        self.action_about.setText(_translate("MainWindow", "关于"))
        self.action_quick_plot.setText(_translate("MainWindow", "快速绘图"))
        self.action_custom_defined_plot.setText(_translate("MainWindow", "自定义绘图"))
        self.action_multi_source_plot.setText(_translate("MainWindow", "并行绘图"))
        self.action_paralist_dock_isclosed.setText(_translate("MainWindow", "参数窗口"))