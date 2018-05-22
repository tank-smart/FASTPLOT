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
# 1.2018-05-16 王学良创建文件
# =============================================================================


# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import (QSize, QRect, Qt, QMetaObject, QCoreApplication,
                          pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QMenuBar, QMessageBox,
                             QFileDialog, QMenu, QToolBar, QAction, QStatusBar,
                             QHBoxLayout)

# =============================================================================
# Package views imports
# =============================================================================
from stacked_widget import StackedWidget
from paralist_dock import ParalistDock
from new_project_dialog import NewProjectDialog

# =============================================================================
# Main Window
# =============================================================================
class MainWindow(QMainWindow):

    #此处定义常量
    
    #此处定义信号
    
    def __init__(self):
        QMainWindow.__init__(self)
        
    def setup(self):
#        定义主窗口
        self.setEnabled(True)
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))

#        创建堆叠窗口        
        self.mw_stacked_widget = StackedWidget()
        self.mw_stacked_widget.setup()

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
        self.menu_import = QMenu(self.menu_file)
        self.menu_import.setObjectName("menu_import")
        self.menu_export = QMenu(self.menu_file)
        self.menu_export.setObjectName("menu_export")
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
        self.action_new = QAction(self)
        self.action_new.setObjectName("action_new")
        self.action_open = QAction(self)
        self.action_open.setObjectName("action_open")
        self.action_import_normal_datafile = QAction(self)
        self.action_import_normal_datafile.setObjectName("action_import_normal_datafile")
        self.action_export_data = QAction(self)
        self.action_export_data.setObjectName("action_export_data")
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
        self.action_about = QAction(self)
        self.action_about.setObjectName("action_about")
        self.action_quick_plot = QAction(self)
        self.action_quick_plot.setObjectName("action_quick_plot")
        self.action_custom_defined_plot = QAction(self)
        self.action_custom_defined_plot.setObjectName("action_custom_defined_plot")
        self.action_multi_source_plot = QAction(self)
        self.action_multi_source_plot.setObjectName("action_multi_source_plot")
        self.action_paralist_dock_isclosed = QAction(self)
        self.action_paralist_dock_isclosed.setCheckable(True)
        self.action_paralist_dock_isclosed.setChecked(True)
        self.action_paralist_dock_isclosed.setObjectName("action_paralist_dock_isclosed")
        
#        将动作添加到对应的菜单下
        self.menu_import.addAction(self.action_import_normal_datafile)
        self.menu_export.addAction(self.action_export_data)
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu_import.menuAction())
        self.menu_file.addAction(self.menu_export.menuAction())
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
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_analysis.menuAction())
        self.menubar.addAction(self.menu_plot.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu_window.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.toolbar.addAction(self.action_import_normal_datafile)

        self.retranslate()
#        QMetaObject.connectSlotsByName(self)
        
# =======连接信号与槽
        self.mw_paralist_dock.signal_close.connect(self.slot_paralist_dock_close)


# =============================================================================
# Views
# =============================================================================

# =============================================================================
#    与新建项目有关的显示
    def view_new(self):
        return NewProjectDialog().get_project_info()

    def view_set_window_title(self, title):
        if title:
            self.setWindowTitle(title + ' - Demo')
# =============================================================================
#    与打开项目有关的显示
        
#    响应打开项目的指令，函数返回一个str型的文件路径
    def view_open(self):
        sel_pro = QFileDialog.getExistingDirectory(self, 'Open Program')
        if sel_pro:
            sel_pro = sel_pro.replace('/','\\')
            return sel_pro
        else:
            return None
        
    def view_open_status(self, status, pro_name):
        if status:
            
            tipDialog = QMessageBox(self)
            tipDialog.resize(300,100)
            tipDialog.setWindowTitle("Information")
            tipDialog.setText("Open a project suceessfully!")
            tipDialog.exec_()
        else:
            tipDialog = QMessageBox(self)
            tipDialog.resize(300,100)
            tipDialog.setWindowTitle("Caution")
            tipDialog.setText("Unsuceessfully, It's not a project!")
            tipDialog.exec_()                        

# =============================================================================
#    与关于数据导入有关的显示
            
#    

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
    def control_paralist_dock_isclosed(self):
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


# =============================================================================
# 汉化
# =============================================================================
    def retranslate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "演示程序"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_import.setTitle(_translate("MainWindow", "导入"))
        self.menu_export.setTitle(_translate("MainWindow", "导出"))
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
        self.action_new.setText(_translate("MainWindow", "新建"))
        self.action_open.setText(_translate("MainWindow", "打开"))
        self.action_import_normal_datafile.setText(_translate("MainWindow", "通用数据"))
        self.action_export_data.setText(_translate("MainWindow", "数据文件"))
        self.action_export_data.setToolTip(_translate("MainWindow", "数据文件"))
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
        
# =============================================================================
#     def retranslate(self):
#         _translate = QCoreApplication.translate
#         self.setWindowTitle(_translate("MainWindow", "演示"))
#         self.menu_file.setTitle(_translate("MainWindow", "File"))
#         self.menu_import.setTitle(_translate("MainWindow", "Import"))
#         self.menu_export.setTitle(_translate("MainWindow", "Export"))
#         self.menu_edit.setTitle(_translate("MainWindow", "Edit"))
#         self.menu_view.setTitle(_translate("MainWindow", "View"))
#         self.menu_tools.setTitle(_translate("MainWindow", "Tools"))
#         self.menu_window.setTitle(_translate("MainWindow", "Window"))
#         self.menu_help.setTitle(_translate("MainWindow", "Help"))
#         self.menu_analysis.setTitle(_translate("MainWindow", "Analysis"))
#         self.menu_mathematics.setTitle(_translate("MainWindow", "Mathematics"))
#         self.menu_data_manipulation.setTitle(_translate("MainWindow", "Data Manipulation"))
#         self.menu_data_manage.setTitle(_translate("MainWindow", "Data Manage"))
#         self.menu_plot.setTitle(_translate("MainWindow", "Plot"))
#         self.mw_paralist_dock.setWindowTitle(_translate("MainWindow", "Parameters"))
#         self.mw_paralist_dock.line_edit_search_para.setPlaceholderText(_translate("MainWindow", "Filter"))
#         self.toolbar.setWindowTitle(_translate("MainWindow", "toolBar"))
#         self.action_new.setText(_translate("MainWindow", "New"))
#         self.action_open.setText(_translate("MainWindow", "Open"))
#         self.action_import_normal_datafile.setText(_translate("MainWindow", "Normal Datafile"))
#         self.action_export_data.setText(_translate("MainWindow", "Data File"))
#         self.action_export_data.setToolTip(_translate("MainWindow", "Data File"))
#         self.action_exit.setText(_translate("MainWindow", "Exit"))
#         self.action_simple_math.setText(_translate("MainWindow", "Simple Math..."))
#         self.action_testpoint_manage.setText(_translate("MainWindow", "Test Point"))
#         self.action_synchronization.setText(_translate("MainWindow", "Synchronization"))
#         self.action_tuning.setText(_translate("MainWindow", "Tuning"))
#         self.action_para_manage.setText(_translate("MainWindow", "Parameters"))
#         self.action_temp_manage.setText(_translate("MainWindow", "Templates"))
#         self.action_options.setText(_translate("MainWindow", "Options"))
#         self.action_about.setText(_translate("MainWindow", "About Demo"))
#         self.action_quick_plot.setText(_translate("MainWindow", "Quick Plot"))
#         self.action_custom_defined_plot.setText(_translate("MainWindow", "Custom Defined Plot"))
#         self.action_multi_source_plot.setText(_translate("MainWindow", "Multi-source Plot"))
#         self.action_paralist_dock_isclosed.setText(_translate("MainWindow", "Parameters Dock"))
# =============================================================================
