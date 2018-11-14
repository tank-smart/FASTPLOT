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
import json
# =============================================================================
# Qt imports
# =============================================================================
from PyQt5.QtCore import QObject, QSize, Qt, QCoreApplication, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QCloseEvent, QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QMenuBar, 
                             QFileDialog, QMessageBox, QMenu, QToolBar, 
                             QAction, QStatusBar, QStackedWidget,
                             QDockWidget, QVBoxLayout, QDialog)

# =============================================================================
# Package views imports
# =============================================================================
from views.plot_window import PlotWindow
from views.paralist_window import ParalistWindow
from models.datafile_model import Normal_DataFile, GPS_DataFile
from views.data_sift_window import DataSiftWindow
from views.data_process_window import DataProcessWindow
from views.mathematics_window import MathematicsWindow
from views.para_temp_window import ParaTempWindow
from views.data_dict_window import DataDictWindow
from views.custom_dialog import FileProcessDialog, OptionDialog, ImportDataFileDialog
import views.config_info as CONFIG
# =============================================================================
# Main Window
# =============================================================================
class MainWindow(QMainWindow):   

    signal_import_datafiles = pyqtSignal(dict)
    
# =============================================================================
# 初始化
# =============================================================================
    def __init__(self, parent = None):
        
        super().__init__(parent)
#        设置窗口图标
        self.setWindowIcon(QIcon(CONFIG.ICON_WINDOW))

#        已导入的文件
        self.current_files = []
#        文件路径映射的文件类型
        self.dict_filetype = {}
#        所涉及的结果文件，列表类型
        self.resultfile_group = {}
#        功能窗口之前显示的页面
        self.last_page = None

# =============================================================================
# UI模块
# =============================================================================
    def setup(self):
        
#        主窗口的默认有右键菜单，默认的右键菜单不满足要求，因此采用以下语句停用
        self.setContextMenuPolicy(Qt.NoContextMenu)

        self.load_config_info()

#        定义主窗口
#        主窗口内统一使用一种字体
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.setEnabled(True)
        self.setGeometry(50, 50, 1050, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(QSize(1050, 600))
        
#        创建参数列表窗口
        self.paralist_window = ParalistWindow(self)
        self.paralist_window.setup()
        self.paralist_window.setMinimumWidth(200)

#        创建绘图界面
        self.plot_fun_win = QDockWidget(self)
        self.plot_fun_win.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable)
        self.plot_fun_win.setWindowTitle(QCoreApplication.
                                         translate('MainWindow', '绘图'))
        self.plot_fun_win.setMinimumWidth(800)
        self.plot_wid = QWidget(self)
        self.vlayout_pw = QVBoxLayout(self.plot_wid)
        self.vlayout_pw.setContentsMargins(2, 2, 2, 2)
#        self.stacked_window = QStackedWidget(self.syn_window_contents)
#        self.data_process_page = DataProcessWindow(self.syn_window_contents)
#        self.data_process_page.setup()
#        self.stacked_window.addWidget(self.data_process_page)
#        self.data_sift_page = DataSiftWindow(self.syn_window_contents)
#        self.data_sift_page.setup()
#        self.stacked_window.addWidget(self.data_sift_page)
        self.plot_page = PlotWindow(self.plot_wid)
        self.plot_page.setup()
#        self.stacked_window.addWidget(self.plot_page)
#        self.mathematics_page = MathematicsWindow(self.syn_window_contents)
#        self.mathematics_page.setup()
#        self.stacked_window.addWidget(self.mathematics_page)
#        self.para_temp_page = ParaTempWindow(self.syn_window_contents)
#        self.para_temp_page.setup()
#        self.stacked_window.addWidget(self.para_temp_page)
#        self.data_dict_page = DataDictWindow(self.syn_window_contents)
#        self.data_dict_page.signal_data_dict_changed.connect(
#                self.slot_data_dict_changed)
#        self.data_dict_page.setup()
#        self.stacked_window.addWidget(self.data_dict_page)
        self.vlayout_pw.addWidget(self.plot_page)
        self.plot_fun_win.setWidget(self.plot_wid)
#        参数选择界面
        self.data_process_fun_win = QDockWidget(self)
#        让dock窗口不可依靠
        self.data_process_fun_win.setAllowedAreas(Qt.NoDockWidgetArea)
        self.data_process_fun_win.setMinimumSize(QSize(800, 500))
        self.data_process_fun_win.setGeometry(150, 150, 800, 500)
        self.data_process_fun_win.setWindowTitle(QCoreApplication.
                                                 translate('MainWindow', '参数选择'))
        self.data_process_wid = QWidget(self)
        self.vlayout_dpw = QVBoxLayout(self.data_process_wid)
        self.vlayout_dpw.setContentsMargins(2, 2, 2, 2)
        self.data_process_page = DataProcessWindow(self.data_process_wid)
        self.data_process_page.setup()
        self.vlayout_dpw.addWidget(self.data_process_page)
        self.data_process_fun_win.setWidget(self.data_process_wid)
#        数据筛选界面
        self.data_sift_fun_win = QDockWidget(self)
        self.data_sift_fun_win.setAllowedAreas(Qt.NoDockWidgetArea)
        self.data_sift_fun_win.setMinimumSize(QSize(800, 500))
        self.data_sift_fun_win.setGeometry(200, 180, 800, 500)
        self.data_sift_fun_win.setWindowTitle(QCoreApplication.
                                              translate('MainWindow', '数据筛选'))
        self.data_sift_wid = QWidget(self)
        self.vlayout_dsw = QVBoxLayout(self.data_sift_wid)
        self.vlayout_dsw.setContentsMargins(2, 2, 2, 2)
        self.data_sift_page = DataSiftWindow(self.data_sift_wid)
        self.data_sift_page.setup()
        self.vlayout_dsw.addWidget(self.data_sift_page)
        self.data_sift_fun_win.setWidget(self.data_sift_wid)
#        数学计算界面
        self.mathematics_fun_win = QDockWidget(self)
        self.mathematics_fun_win.setAllowedAreas(Qt.NoDockWidgetArea)
        self.mathematics_fun_win.setMinimumSize(QSize(800, 500))
        self.mathematics_fun_win.setGeometry(250, 210, 800, 500)
        self.mathematics_fun_win.setWindowTitle(QCoreApplication.
                                                translate('MainWindow', '数学计算'))
        self.mathematics_wid = QWidget(self)
        self.vlayout_mw = QVBoxLayout(self.mathematics_wid)
        self.vlayout_mw.setContentsMargins(2, 2, 2, 2)
        self.mathematics_page = MathematicsWindow(self.mathematics_wid)
        self.mathematics_page.setup()
        self.vlayout_mw.addWidget(self.mathematics_page)
        self.mathematics_fun_win.setWidget(self.mathematics_wid)
#        参数模板界面
        self.para_temp_fun_win = QDockWidget(self)
        self.para_temp_fun_win.setAllowedAreas(Qt.NoDockWidgetArea)
        self.para_temp_fun_win.setMinimumSize(QSize(800, 500))
        self.para_temp_fun_win.setGeometry(300, 240, 800, 500)
        self.para_temp_fun_win.setWindowTitle(QCoreApplication.
                                              translate('MainWindow', '参数模板'))
        self.para_temp_wid = QWidget(self)
        self.vlayout_ptw = QVBoxLayout(self.para_temp_wid)
        self.vlayout_ptw.setContentsMargins(2, 2, 2, 2)
        self.para_temp_page = ParaTempWindow(self.para_temp_wid)
        self.para_temp_page.setup()
        self.vlayout_ptw.addWidget(self.para_temp_page)
        self.para_temp_fun_win.setWidget(self.para_temp_wid)
#        数据字典界面
        self.data_dict_fun_win = QDockWidget(self)
        self.data_dict_fun_win.setAllowedAreas(Qt.NoDockWidgetArea)
        self.data_dict_fun_win.setMinimumSize(QSize(800, 500))
        self.data_dict_fun_win.setGeometry(350, 270, 800, 500)
        self.data_dict_fun_win.setWindowTitle(QCoreApplication.
                                              translate('MainWindow', '数据字典'))
        self.data_dict_wid = QWidget(self)
        self.vlayout_ddw = QVBoxLayout(self.data_dict_wid)
        self.vlayout_ddw.setContentsMargins(2, 2, 2, 2)
        self.data_dict_page = DataDictWindow(self.data_dict_wid)
        self.data_dict_page.signal_data_dict_changed.connect(
                self.slot_data_dict_changed)
        self.data_dict_page.setup()
        self.vlayout_ddw.addWidget(self.data_dict_page)
        self.data_dict_fun_win.setWidget(self.data_dict_wid)
        
#        允许嵌套dock
        self.setDockNestingEnabled(True)
#        设置主窗口布局
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paralist_window)
#        self.addDockWidget(Qt.RightDockWidgetArea, self.plot_fun_win)
        self.splitDockWidget(self.paralist_window, self.plot_fun_win,
                             Qt.Horizontal)
        self.data_process_fun_win.setFloating(True)
        self.data_process_fun_win.setHidden(True)
        self.data_sift_fun_win.setFloating(True)
        self.data_sift_fun_win.setHidden(True)
        self.mathematics_fun_win.setFloating(True)
        self.mathematics_fun_win.setHidden(True)
        self.para_temp_fun_win.setFloating(True)
        self.para_temp_fun_win.setHidden(True)
        self.data_dict_fun_win.setFloating(True)
        self.data_dict_fun_win.setHidden(True)
        self.setDockOptions(QMainWindow.AnimatedDocks)
        
#        创建菜单栏
        self.menubar = QMenuBar(self)
        self.menu_file = QMenu(self.menubar)
#        self.menu_open = QMenu(self.menu_file)
#        self.menu_edit = QMenu(self.menubar)
        self.menu_view = QMenu(self.menubar)
#        self.menu_panels = QMenu(self.menu_view)
#        self.menu_panels.setIcon(QIcon(CONFIG.ICON_PANELS))
        self.menu_tools = QMenu(self.menubar)
#        self.menu_data_analysis = QMenu(self.menu_tools)
#        self.menu_data_analysis.setIcon(QIcon(CONFIG.ICON_DATA_ANA))
#        self.menu_data_manage = QMenu(self.menu_tools)
#        self.menu_data_manage.setIcon(QIcon(CONFIG.ICON_DATA_MAN))
#        self.menu_window = QMenu(self.menubar)
        self.menu_help = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        
#        创建状态栏
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
#        创建工具栏
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar_plot = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar_plot)

        
#        创建动作
        self.action_open_normal_datafile = QAction(self)
        self.action_open_normal_datafile.setIcon(QIcon(CONFIG.ICON_OPEN_NORDATA))
        self.action_open_datafile = QAction(self)
#        self.action_open_datafile.setIcon(QIcon(CONFIG.ICON_OPEN_NORDATA))
        self.action_file_process = QAction(self)
        self.action_exit = QAction(self)
        self.action_exit.setIcon(QIcon(CONFIG.ICON_EIXT))
        self.action_mathematics = QAction(self)
        self.action_mathematics.setIcon(QIcon(CONFIG.ICON_MATHEMATICS))
        self.action_data_process = QAction(self)
        self.action_data_process.setIcon(QIcon(CONFIG.ICON_DATA_PROC))
        self.action_data_sift = QAction(self)
        self.action_data_sift.setIcon(QIcon(CONFIG.ICON_DATA_SIFT))        
        self.action_para_templates = QAction(self)
        self.action_para_templates.setIcon(QIcon(CONFIG.ICON_PARA_TEMP))
        self.action_data_dict = QAction(self)
        self.action_data_dict.setIcon(QIcon(CONFIG.ICON_PARA_DICT))
        self.action_options = QAction(self)
        self.action_options.setIcon(QIcon(CONFIG.ICON_SETTING))
        self.action_about = QAction(self)
        self.action_about.setIcon(QIcon(CONFIG.ICON_ABOUT))
#        self.action_plot = QAction(self)
#        self.action_plot.setIcon(QIcon(CONFIG.ICON_PLOT_WIN))
        self.action_show_paralist_window = QAction(self)
        self.action_show_paralist_window.setCheckable(True)
        self.action_show_paralist_window.setChecked(True)
        self.action_show_plot_window = QAction(self)
        self.action_show_plot_window.setCheckable(True)
        self.action_show_plot_window.setChecked(True)
        self.action_help_doc = QAction(self)
        self.action_help_video = QAction(self)
        
        self.action_add_sa_fig = QAction(self)
        self.action_add_sa_fig.setIcon(QIcon(CONFIG.ICON_SINGLE_AXIS))
        self.action_add_ma_fig = QAction(self)
        self.action_add_ma_fig.setIcon(QIcon(CONFIG.ICON_MULT_AXIS))
        self.action_add_sta_fig = QAction(self)
        self.action_add_sta_fig.setIcon(QIcon(CONFIG.ICON_STACK_AXIS))
#        self.action_add_ux_fig = QAction(self)
#        self.action_add_ux_fig.setIcon(QIcon(CONFIG.ICON_STACK_AXIS))
        
#        将动作添加到对应的菜单下       
#        self.menu_open.addAction(self.action_open_normal_datafile)
        self.menu_file.addActions([self.action_open_normal_datafile,
                                   self.action_open_datafile,
                                   self.action_file_process])
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_tools.addActions([self.action_data_process,
                                    self.action_data_sift,
#                                    self.action_plot,
                                    self.action_mathematics,
                                    self.action_para_templates,
                                    self.action_data_dict,
                                    self.action_options])
#        self.menu_tools.addAction(self.action_options)
#        self.menu_panels.addActions([self.action_show_paralist_window,
#                                    self.action_show_plot_window])
        self.menu_view.addActions([self.action_show_paralist_window,
                                    self.action_show_plot_window])
#        self.menu_data_analysis.addActions([self.action_data_process,
#                                            self.action_data_sift])
#        self.menu_data_manage.addActions([self.action_para_templates,
#                                          self.action_data_dict])
        self.menu_help.addActions([self.action_help_doc,
                                   self.action_help_video,
                                   self.action_about])

#        添加菜单栏
        self.menubar.addAction(self.menu_file.menuAction())
#        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
#        self.menubar.addAction(self.menu_window.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
#        添加工具栏
        self.toolbar.addAction(self.action_open_normal_datafile)
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.action_data_process,
                                 self.action_data_sift,
                                 self.action_mathematics])
#        self.toolbar.addActions([self.action_data_process,
#                                 self.action_data_sift])
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.action_para_templates,
                                          self.action_data_dict])
#        self.toolbar.addSeparator()
#        self.toolbar.addAction(self.action_about)
        
        self.toolbar_plot.addActions([self.action_add_sa_fig,
                                      self.action_add_ma_fig,
                                      self.action_add_sta_fig])
        
#        将绘图页面显示为初始页面
#        self.stacked_window.setCurrentIndex(2)
#        self.last_page = self.action_plot
#        self.action_plot.setChecked(True)
#        self.plot_fun_win.setWindowTitle(QCoreApplication.
#                                            translate('MainWindow', '绘图'))
#
        self.retranslate()
        
# =======连接信号与槽
# =============================================================================
#       主窗口的信号连接        
        self.action_open_normal_datafile.triggered.connect(
                self.slot_open_normal_datafile)
        self.action_open_datafile.triggered.connect(
                self.slot_open_datafile)
#        文件分析
        self.action_file_process.triggered.connect(self.slot_file_process)
#        按下按钮显示相应的页面
        self.action_data_process.triggered.connect(self.slot_show_page)
        self.action_data_sift.triggered.connect(self.slot_show_page)
#        self.action_plot.triggered.connect(self.slot_show_page)
        self.action_mathematics.triggered.connect(self.slot_show_page)
        self.action_para_templates.triggered.connect(self.slot_show_page)
        self.action_data_dict.triggered.connect(self.slot_show_page)
#        按下视图菜单栏下的关闭动作
        self.action_show_paralist_window.triggered.connect(
                self.slot_show_paralist_window)
        self.action_show_plot_window.triggered.connect(
                self.slot_show_plot_window)
#        程序的关于信息
        self.action_about.triggered.connect(self.slot_about)
#        程序帮助
        self.action_help_doc.triggered.connect(self.slot_help_doc)
        self.action_help_video.triggered.connect(self.slot_help_video)
#        程序退出
        self.action_exit.triggered.connect(self.slot_exit)
#        设置
        self.action_options.triggered.connect(self.slot_options)
#        增加画布窗口
        self.action_add_sa_fig.triggered.connect(self.plot_page.slot_add_sa_fig)
        self.action_add_ma_fig.triggered.connect(self.plot_page.slot_add_ma_fig)
        self.action_add_sta_fig.triggered.connect(self.plot_page.slot_add_stack_fig)
#        self.action_add_ux_fig.triggered.connect(self.plot_page.slot_add_ux_fig)
        
        self.signal_import_datafiles.connect(
                self.paralist_window.slot_import_datafiles)

# =============================================================================
#       参数窗口与主窗口和其他窗口的信号连接
#        self.paralist_window.signal_quick_plot.connect(
#                self.action_plot.trigger)
        self.paralist_window.signal_quick_plot.connect(
                self.plot_page.slot_plot)
        self.paralist_window.visibilityChanged.connect(
                self.slot_paralist_window_close)
        self.paralist_window.signal_into_analysis.connect(
                self.data_process_page.slot_import_paras)
        self.paralist_window.signal_into_analysis.connect(
                self.action_data_process.trigger)
        self.paralist_window.signal_delete_files.connect(
                self.slot_delete_files)
        self.paralist_window.signal_into_mathematics.connect(
                self.mathematics_page.plain_text_edit_conmandline.insertPlainText)
        self.paralist_window.signal_into_mathematics.connect(
                self.action_mathematics.trigger)
        self.paralist_window.signal_into_data_dict.connect(
                self.data_dict_page.slot_add_dict)
        self.paralist_window.signal_into_data_dict.connect(
                self.action_data_dict.trigger)
#        参数选择窗口与主窗口和其他窗口的信号与槽连接
        self.data_process_page.signal_request_temps.connect(
                self.slot_send_temps)
        self.data_process_page.signal_save_temp.connect(
                self.para_temp_page.slot_add_para_template)
#        self.data_process_page.signal_para_for_plot.connect(
#                self.action_plot.trigger)
        self.data_process_page.signal_para_for_plot.connect(
                self.plot_page.slot_plot)
        self.data_process_page.signal_send_status.connect(
                self.slot_display_status_info)
        self.data_process_page.signal_close_dock.connect(
                self.data_process_fun_win.close)
#        数据筛选窗口的信号槽连接
        self.data_sift_page.signal_close_ds_dock.connect(
                self.data_sift_fun_win.close)
#        数据字典窗口与主窗口和其他窗口的信号与槽连接
        self.data_dict_page.signal_close_dd_dock.connect(
                self.data_dict_fun_win.close)
#        绘图窗口与主窗口和其他窗口的信号与槽连接
        self.plot_page.signal_send_status.connect(
                self.slot_display_status_info)

        self.plot_fun_win.visibilityChanged.connect(
                self.slot_syn_window_close)
#        数据计算窗口与主窗口和其他窗口的信号与槽连接 
        self.mathematics_page.signal_plot_result_para.connect(
                self.plot_page.slot_plot)
#        self.mathematics_page.signal_plot_result_para.connect(
#                self.action_plot.trigger)
        self.mathematics_page.signal_sendto_ananlysis.connect(
                self.data_process_page.slot_import_datafactory)
        self.mathematics_page.signal_sendto_ananlysis.connect(
                self.action_data_process.trigger)
#        数据模板窗口的信号与槽连接
        self.para_temp_page.signal_close_pt_dock.connect(
                self.para_temp_fun_win.close)

# =============================================================================
# Slots模块            
# =============================================================================
    def closeEvent(self, event : QCloseEvent):

        message = QMessageBox.warning(self,
                      QCoreApplication.translate('MainWindow', '退出'),
                      QCoreApplication.translate('MainWindow',
                                        '''<p>确定要退出吗？'''),
                      QMessageBox.Yes | QMessageBox.No)
        if (message == QMessageBox.Yes):
            self.para_temp_page.output_temps()
#            self.data_dict_page.output_data_dict()
            self.data_dict_page.save_data_dict()
            self.output_config_info()
            event.accept()
        else:
            event.ignore()

#    打开数据文件并将文件信息存入
    def slot_open_normal_datafile(self):

        import_file_dirs = {}
        ex_files = []
        nor_datafiles = []
        file_dir_l = []
        init_dir = CONFIG.OPTION['dir of quick import']
        if os.path.exists(init_dir):
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, QCoreApplication.translate('MainWindow', '快速导入'), 
                    init_dir,
                    QCoreApplication.translate('MainWindow', '普通试飞数据文件(*.txt)'))
        else:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, QCoreApplication.translate('MainWindow', '快速打开'),
                    CONFIG.SETUP_DIR,
                    QCoreApplication.translate('MainWindow', '普通试飞数据文件(*.txt)'))
        if file_dir_list:
            file_dir_list = [file.replace('/','\\') for file in file_dir_list]
            if os.path.exists(file_dir_list[0]):
                CONFIG.OPTION['dir of quick import'] = os.path.dirname(file_dir_list[0])
            for file_dir in file_dir_list:
                if not(file_dir in self.current_files):
                    try:
                        normal_file = Normal_DataFile(file_dir)
                        import_file_dirs[file_dir] = normal_file.paras_in_file
                        file_dir_l.append(file_dir)
                        self.dict_filetype[file_dir] = 'normal datafile'
                    except:
#                        这样处理不太好，如果不是文件本身错误而仅是代码错误也会一并认为是文件本身错误
                        nor_datafiles.append(file_dir)
                else:
                    ex_files.append(file_dir)
            if nor_datafiles:
                print_info = '以下文件不是普通试飞数据文件：'
                for file in nor_datafiles:
                    print_info += ('<br>' + file)
                QMessageBox.information(self,
                                        QCoreApplication.translate('MainWindow', '导入文件提示'),
                                        QCoreApplication.translate('MainWindow', print_info))
            if ex_files:
                print_info = '以下文件已存在：'
                for file in ex_files:
                    print_info += ('<br>' + file)
#                ms_box = QMessageBox(QMessageBox.NoIcon,
#                                     QCoreApplication.translate('MainWindow', '导入文件提示'),
#                                     QCoreApplication.translate('MainWindow', print_info),
#                                     QMessageBox.Ok,
#                                     self)
#                ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
#                ms_box.exec_()
                QMessageBox.information(self,
                                        QCoreApplication.translate('MainWindow', '导入文件提示'),
                                        QCoreApplication.translate('MainWindow', print_info))
        if file_dir_l:
            self.current_files += file_dir_l
            self.slot_current_files_change()
        if import_file_dirs:
            self.signal_import_datafiles.emit(import_file_dirs)
            
    def slot_open_datafile(self):
        import_file_dirs = {}
        ex_files = []
        nor_datafiles = []
        file_dir_l = []
        dialog = ImportDataFileDialog(self)
        return_signal = dialog.exec_()
        if return_signal == QDialog.Accepted:
#            数据文件路径
            datafile_dir = dialog.datafile_dir
            file_dir_list = [datafile_dir]
            if file_dir_list:
                file_dir_list = [file.replace('/','\\') for file in file_dir_list]
#                if os.path.exists(file_dir_list[0]):
#                    CONFIG.OPTION['dir of quick import'] = os.path.dirname(file_dir_list[0])
                for file_dir in file_dir_list:
                    if not(file_dir in self.current_files):
                        datafile_type = dialog.datafile_type
                        try:
                            if datafile_type == 'GPS datafile':
                                gps_file = GPS_DataFile(datafile_dir)
                                import_file_dirs[file_dir] = gps_file.paras_in_file
                                file_dir_l.append(file_dir)
                                self.dict_filetype[file_dir] = 'GPS datafile'
                        except:
    #                        这样处理不太好，如果不是文件本身错误而仅是代码错误也会一并认为是文件本身错误
                            nor_datafiles.append(file_dir)
                    else:
                        ex_files.append(file_dir)
                if nor_datafiles:
                    print_info = '以下文件不是选定的数据文件：'
                    for file in nor_datafiles:
                        print_info += ('<br>' + file)
                    QMessageBox.information(self,
                                            QCoreApplication.translate('MainWindow', '导入文件提示'),
                                            QCoreApplication.translate('MainWindow', print_info))
                if ex_files:
                    print_info = '以下文件已存在：'
                    for file in ex_files:
                        print_info += ('<br>' + file)
    #                ms_box = QMessageBox(QMessageBox.NoIcon,
    #                                     QCoreApplication.translate('MainWindow', '导入文件提示'),
    #                                     QCoreApplication.translate('MainWindow', print_info),
    #                                     QMessageBox.Ok,
    #                                     self)
    #                ms_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    #                ms_box.exec_()
                    QMessageBox.information(self,
                                            QCoreApplication.translate('MainWindow', '导入文件提示'),
                                            QCoreApplication.translate('MainWindow', print_info))
            if file_dir_l:
                self.current_files += file_dir_l
                self.slot_current_files_change()
            if import_file_dirs:
                self.signal_import_datafiles.emit(import_file_dirs)
            
#            数据类型，普通试飞数据、GPS数据、QAR数据、自定义数据
#            datafile_type = dialog.datafile_type
#            if datafile_type == 'GPS datafile':
#                print(datafile_dir)
#                gps_file = GPS_DataFile(datafile_dir)
#                df = gps_file.cols_input(datafile_dir, gps_file.paras_in_file)
#            print(df)
#                
#            print(datafile_type)
#            
##            只有当数据类型为自定义数据时，以下参数才有数据
##            导入起始行 - 1
#            skiprows = dialog.skiprows
#            print(skiprows)
##            时间列为0时表示无时间
#            timecol = dialog.timecol
#            print(timecol)
##            分隔符
#            sep = dialog.sep
#            print(sep)
##            时间格式
#            time_format = dialog.time_format
#            print(time_format)

#    与关于退出有关的显示
    def slot_exit(self):
        
        QApplication.closeAllWindows()
            
#    显示About信息
    def slot_about(self):
        
        def developers():
            ms_box = QMessageBox(QMessageBox.NoIcon,
                                 QCoreApplication.translate('MainWindow', '开发人员'),
                                 QCoreApplication.translate('MainWindow',
                                                           '''
                                                           <p><b>FastPlot</b>软件开发团队</p>
                                                           <p>策划：米毅</p>
                                                           <p>管理：戴维</p>
                                                           <p>技术：冯德林</p>
                                                           <p>开发：王学良，严骅，汤文亚，刘洋，张启鹏，何航帆，王康乐</p>
                                                           <p>需求：李峥，田大成，王奕融</p>
                                                           <p>测试：待定</p>
                                                           '''),
                                 QMessageBox.Yes,
                                 self)
            btn_list = ms_box.buttons()
            btn_list[0].setText(QCoreApplication.translate('MainWindow', '确定'))
            ms_box.exec_()

        ms_box = QMessageBox(QMessageBox.NoIcon,
                             QCoreApplication.translate('MainWindow', '关于' + CONFIG.SOFTNAME),
                             QCoreApplication.translate('MainWindow',
                                                        '<p><b>' + CONFIG.SOFTNAME +
                                                        '''</b></p>
                                                        <br>试飞数据分析软件
                                                        <p>试飞中心 | 试飞工程部
                                                        <br><img src= \'''' + CONFIG.FTCC_LOGO + 
                                                        '\' width=\'240\' height=\'30\'></p>'),
#                                                        <br>Copyright copy; COMAC Flight Test Center.
                             QMessageBox.Close,
                             self)
        ms_box.setIconPixmap(QPixmap(CONFIG.ICON_WINDOW))
        btn = ms_box.addButton(QCoreApplication.translate('MainWindow', '开发人员'), QMessageBox.ActionRole)
        btn.clicked.connect(developers)
        btn_list = ms_box.buttons()
        btn_list[0].setText(QCoreApplication.translate('MainWindow', '关闭'))
        ms_box.exec_()
        
    def slot_delete_files(self, files : list):
        
        if files:
            for file in files:
                self.current_files.remove(file)
                del self.dict_filetype[file]
            self.slot_current_files_change()

#    响应参数窗口显示动作
    def slot_show_paralist_window(self):
        
        if self.paralist_window.isHidden():
            self.paralist_window.setHidden(False)
        else:
            self.paralist_window.setHidden(True)

#        参数窗口关闭后需要把视图下的勾选去掉
    def slot_paralist_window_close(self, isclose):
        
        if isclose:
            self.action_show_paralist_window.setChecked(True)
        else:
            self.action_show_paralist_window.setChecked(False)
        
#    响应参数窗口显示动作
    def slot_show_plot_window(self):
        
        if self.plot_fun_win.isHidden():
            self.plot_fun_win.setHidden(False)
        else:
            self.plot_fun_win.setHidden(True)

#        参数窗口关闭后需要把视图下的勾选去掉
    def slot_syn_window_close(self, isclose):
        
        if isclose:
            self.action_show_plot_window.setChecked(True)
        else:
            self.action_show_plot_window.setChecked(False)

#    显示用户选择的界面
    def slot_show_page(self):
        
#        接收发出信号的那个对象
        sender = QObject.sender(self)
        if (sender == self.action_data_process):
            self.data_process_fun_win.setHidden(False)
            self.data_process_fun_win.activateWindow()
        if (sender == self.action_data_sift):
            self.data_sift_fun_win.setHidden(False)
            self.data_sift_fun_win.activateWindow()
        if (sender == self.action_mathematics):
            self.mathematics_fun_win.setHidden(False)
            self.mathematics_fun_win.activateWindow()
        if (sender == self.action_para_templates):
            self.para_temp_fun_win.setHidden(False)
            self.para_temp_fun_win.activateWindow()
        if (sender == self.action_data_dict):
            self.data_dict_fun_win.setHidden(False)
            self.data_dict_fun_win.activateWindow()
    
    def slot_send_temps(self, type_temp : str):
        
        dict_files = self.paralist_window.get_dict_files_tree()
        if type_temp == 'para_template':
            self.data_process_page.slot_sel_temp(dict_files, self.para_temp_page.paras_temps)
#        if type_temp == 'plot_template':
#            self.plot_page.slot_sel_temp(dict_files, self.data_manage_page.plot_temps)
            
    def slot_file_process(self):
        
        if self.current_files:
            dialog = FileProcessDialog(self, self.current_files)
            dialog.signal_send_status.connect(self.slot_display_status_info)
            return_signal = dialog.exec_()
            if return_signal == QDialog.Accepted:
                QMessageBox.information(self,
                        QCoreApplication.translate('MainWindow', '保存提示'),
                        QCoreApplication.translate('MainWindow', '保存成功！'))
        else:
            QMessageBox.information(self,
                                    QCoreApplication.translate('MainWindow', '文件处理提示'),
                                    QCoreApplication.translate('MainWindow', '未导入数据文件'))
        
    def slot_current_files_change(self):
        
        self.data_sift_page.slot_update_current_files(self.current_files, self.dict_filetype)
        self.mathematics_page.plain_text_edit_conmandline.slot_update_current_files(self.current_files, self.dict_filetype)
        self.plot_page._current_files = self.current_files
        self.plot_page._dict_filetype = self.dict_filetype
        self.data_process_page._dict_filetype = self.dict_filetype
        
    def slot_data_dict_changed(self, data_dict : dict):
        
        self.plot_page._data_dict = data_dict
        self.paralist_window._data_dict = data_dict
        self.data_process_page._data_dict = data_dict
        self.para_temp_page._data_dict = data_dict
    
#    用于将信息显示在状态栏，也可以用于清除状态栏信息
    def slot_display_status_info(self, message : str, timeout : int):
        
        if message:
            self.statusbar.clearMessage()
            self.statusbar.showMessage(message, timeout)
            
    def slot_help_doc(self):
        
        if os.path.exists(CONFIG.DIR_HELP_DOC):
            os.startfile(CONFIG.DIR_HELP_DOC)
        else:
            QMessageBox.warning(self,
                      QCoreApplication.translate('MainWindow', '帮助文档错误'),
                      QCoreApplication.translate('MainWindow', '未发现帮助文档，请联系开发人员！'),
                      QMessageBox.Yes)
    
    def slot_help_video(self):
        
        if os.path.exists(CONFIG.DIR_HELP_VIDEO):
            os.startfile(CONFIG.DIR_HELP_VIDEO)
        else:
            QMessageBox.warning(self,
                      QCoreApplication.translate('MainWindow', '视频教程错误'),
                      QCoreApplication.translate('MainWindow', '未发现视频教程，请联系开发人员！'),
                      QMessageBox.Yes)
            
    def slot_options(self):
        
        dialog = OptionDialog(self)
        return_signal = dialog.exec_()
        if (return_signal == QDialog.Accepted):
            for index in range(self.plot_page.tab_widget_figure.count()):
                self.plot_page.tab_widget_figure.widget(index).canva.update_config_info()

# =============================================================================
# 功能函数模块
# =============================================================================
    def load_config_info(self):
        
#        导入配置信息
        try:
            with open(CONFIG.SETUP_DIR + r'\data\configuration.json', 'r') as file:
                OPTION = json.load(file)
#                便于开发人员增加配置变量，
                for option_info in OPTION:
                    CONFIG.OPTION[option_info] = OPTION[option_info]
        except IOError:
            QMessageBox.information(self,
                                    QCoreApplication.translate('MainWindow', '软件配置提示'),
                                    QCoreApplication.translate('MainWindow', '配置文件错误！将还原默认设置'))
        
    def output_config_info(self):
        
        try:
    #        打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(CONFIG.SETUP_DIR + r'\data\configuration.json', 'w') as file:
    #            将内存中的模板一一写入文件
                json.dump(CONFIG.OPTION, file)
        except IOError:
            QMessageBox.information(self,
                                    QCoreApplication.translate('MainWindow', '软件配置提示'),
                                    QCoreApplication.translate('MainWindow', '无法保存软件配置！'))
# =============================================================================
# 汉化
# =============================================================================
    def retranslate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', CONFIG.SOFTNAME))
        self.menu_file.setTitle(_translate('MainWindow', '文件'))
#        self.menu_open.setTitle(_translate('MainWindow', '打开'))
#        self.menu_edit.setTitle(_translate('MainWindow', '编辑'))
        self.menu_view.setTitle(_translate('MainWindow', '视图'))
#        self.menu_panels.setTitle(_translate('MainWindow', '面板'))
        self.menu_tools.setTitle(_translate('MainWindow', '工具'))
#        self.menu_data_analysis.setTitle(_translate('MainWindow', '参数选择'))
#        self.menu_data_manage.setTitle(_translate('MainWindow', '数据管理'))
#        self.menu_window.setTitle(_translate('MainWindow', '窗口'))
        self.menu_help.setTitle(_translate('MainWindow', '帮助'))
        self.toolbar.setWindowTitle(_translate('MainWindow', '工具栏'))
        self.action_open_normal_datafile.setText(_translate('MainWindow', '快速导入'))
        self.action_open_normal_datafile.setToolTip(_translate('MainWindow', '快速导入'))
        self.action_open_datafile.setText(_translate('MainWindow', '数据导入'))
        self.action_file_process.setText(_translate('MainWindow', '文件数据导出'))
        self.action_exit.setText(_translate('MainWindow', '退出'))
        self.action_mathematics.setText(_translate('MainWindow', '数学计算'))
        self.action_data_process.setText(_translate('MainWindow', '参数选择'))
        self.action_data_sift.setText(_translate('MainWindow', '数据筛选'))
        self.action_para_templates.setText(_translate('MainWindow', '参数模板'))
        self.action_data_dict.setText(_translate('MainWindow', '数据字典'))
        self.action_options.setText(_translate('MainWindow', '软件设置'))
        self.action_about.setText(_translate('MainWindow', '关于FastPlot'))
#        self.action_plot.setText(_translate('MainWindow', '绘图'))
        self.action_show_paralist_window.setText(_translate('MainWindow', '参数浏览器'))
        self.action_show_plot_window.setText(_translate('MainWindow', '绘图界面'))
        self.action_help_doc.setText(_translate('MainWindow', 'FastPlot帮助文档'))
        self.action_help_video.setText(_translate('MainWindow', 'FastPlot视频教程'))
        self.action_add_ma_fig.setText(_translate('MainWindow', '添加多坐标图'))
        self.action_add_sa_fig.setText(_translate('MainWindow', '添加单坐标图'))
        self.action_add_sta_fig.setText(_translate('MainWindow', '添加重叠图'))
        
def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setup()
    mainwindow.show()
    return app.exec_()