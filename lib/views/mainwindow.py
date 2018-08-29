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
from PyQt5.QtCore import QObject, QSize, Qt, QCoreApplication, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QCloseEvent
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QMenuBar, 
                             QFileDialog, QMessageBox, QMenu, QToolBar, 
                             QAction, QStatusBar, QStackedWidget,
                             QDockWidget, QVBoxLayout, QDialog)

# =============================================================================
# Package views imports
# =============================================================================
from views.plot_window import PlotWindow
from views.paralist_window import ParalistWindow
from models.datafile_model import Normal_DataFile
from views.data_sift_window import DataSiftWindow
from views.data_process_window import DataProcessWindow
from views.mathematics_window import MathematicsWindow
from views.para_temp_window import ParaTempWindow
from views.data_dict_window import DataDictWindow
from views.custom_dialog import FileProcessDialog
import views.constant as CONSTANT
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
        self.setWindowIcon(QIcon(CONSTANT.ICON_WINDOW))

#        已导入的文件
        self.current_files = []
#        所涉及的结果文件，列表类型
        self.resultfile_group = {}
#        软件的配置信息
        self.config_info = {'INIT DIR OF IMPORTING FILES' : ''}
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

#        创建堆叠窗口
        self.syn_function_window = QDockWidget(self)
        self.syn_function_window.setMinimumWidth(800)
        self.syn_window_contents = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.syn_window_contents)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.stacked_window = QStackedWidget(self.syn_window_contents)
        self.data_process_page = DataProcessWindow(self.syn_window_contents)
        self.data_process_page.setup()
        self.stacked_window.addWidget(self.data_process_page)
        self.data_sift_page = DataSiftWindow(self.syn_window_contents)
        self.data_sift_page.setup()
        self.stacked_window.addWidget(self.data_sift_page)
        self.plot_page = PlotWindow(self.syn_window_contents)
        self.plot_page.setup()
        self.stacked_window.addWidget(self.plot_page)
        self.mathematics_page = MathematicsWindow(self.syn_window_contents)
        self.mathematics_page.setup()
        self.stacked_window.addWidget(self.mathematics_page)
        self.para_temp_page = ParaTempWindow(self.syn_window_contents)
        self.para_temp_page.setup()
        self.stacked_window.addWidget(self.para_temp_page)
        self.data_dict_page = DataDictWindow(self.syn_window_contents)
        self.data_dict_page.signal_data_dict_changed.connect(
                self.slot_data_dict_changed)
        self.data_dict_page.setup()
        self.stacked_window.addWidget(self.data_dict_page)
        self.verticalLayout.addWidget(self.stacked_window)
        self.syn_function_window.setWidget(self.syn_window_contents)

#        允许嵌套dock
        self.setDockNestingEnabled(True)
#        设置主窗口布局
        self.addDockWidget(Qt.LeftDockWidgetArea, self.paralist_window)
        self.splitDockWidget(self.paralist_window, self.syn_function_window,
                           Qt.Horizontal)
#        self.mainwindow_central_widget = QWidget(self)        
#        self.horizontalLayout = QHBoxLayout(self.mainwindow_central_widget)
#        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
#        self.horizontalLayout.setSpacing(0)
#        self.horizontalLayout.addWidget(self.stacked_window)
#        self.setCentralWidget(self.mainwindow_central_widget)
        
#        创建菜单栏
        self.menubar = QMenuBar(self)
        self.menu_file = QMenu(self.menubar)
#        self.menu_open = QMenu(self.menu_file)
#        self.menu_edit = QMenu(self.menubar)
        self.menu_view = QMenu(self.menubar)
        self.menu_panels = QMenu(self.menu_view)
        self.menu_panels.setIcon(QIcon(CONSTANT.ICON_PANELS))
        self.menu_tools = QMenu(self.menubar)
#        self.menu_data_analysis = QMenu(self.menu_tools)
#        self.menu_data_analysis.setIcon(QIcon(CONSTANT.ICON_DATA_ANA))
        self.menu_data_manage = QMenu(self.menu_tools)
        self.menu_data_manage.setIcon(QIcon(CONSTANT.ICON_DATA_MAN))
#        self.menu_window = QMenu(self.menubar)
        self.menu_help = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        
#        创建状态栏
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
#        创建工具栏
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
#        self.toolbar1 = QToolBar(self)
#        self.addToolBar(Qt.TopToolBarArea, self.toolbar1)

        
#        创建动作
        self.action_open_normal_datafile = QAction(self)
        self.action_open_normal_datafile.setIcon(QIcon(CONSTANT.ICON_OPEN_NORDATA))
        self.action_file_process = QAction(self)
        self.action_exit = QAction(self)
        self.action_exit.setIcon(QIcon(CONSTANT.ICON_EIXT))
        self.action_mathematics = QAction(self)
        self.action_mathematics.setIcon(QIcon(CONSTANT.ICON_MATHEMATICS))
        self.action_data_process = QAction(self)
        self.action_data_process.setIcon(QIcon(CONSTANT.ICON_DATA_PROC))
        self.action_data_sift = QAction(self)
        self.action_data_sift.setIcon(QIcon(CONSTANT.ICON_DATA_SIFT))        
        self.action_para_templates = QAction(self)
        self.action_para_templates.setIcon(QIcon(CONSTANT.ICON_PARA_TEMP))
        self.action_data_dict = QAction(self)
        self.action_data_dict.setIcon(QIcon(CONSTANT.ICON_PARA_DICT))
#        self.action_options = QAction(self)
#        self.action_options.setIcon(QIcon(CONSTANT.ICON_SETTING))
        self.action_about = QAction(self)
        self.action_about.setIcon(QIcon(CONSTANT.ICON_ABOUT))
        self.action_plot = QAction(self)
        self.action_plot.setIcon(QIcon(CONSTANT.ICON_PLOT))
        self.action_show_paralist_window = QAction(self)
        self.action_show_paralist_window.setCheckable(True)
        self.action_show_paralist_window.setChecked(True)
        self.action_show_syn_window = QAction(self)
        self.action_show_syn_window.setCheckable(True)
        self.action_show_syn_window.setChecked(True)
        self.action_help_doc = QAction(self)
        self.action_help_video = QAction(self)
        
#        将动作添加到对应的菜单下       
#        self.menu_open.addAction(self.action_open_normal_datafile)
        self.menu_file.addActions([self.action_open_normal_datafile,
                                   self.action_file_process])
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_tools.addActions([self.action_data_process,
                                    self.action_data_sift,
                                    self.action_plot,
                                    self.action_mathematics,
                                    self.menu_data_manage.menuAction()])
#        self.menu_tools.addAction(self.action_options)
        self.menu_panels.addActions([self.action_show_paralist_window,
                                    self.action_show_syn_window])
        self.menu_view.addAction(self.menu_panels.menuAction())
#        self.menu_data_analysis.addActions([self.action_data_process,
#                                            self.action_data_sift])
        self.menu_data_manage.addActions([self.action_para_templates,
                                          self.action_data_dict])
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
        self.toolbar.addActions([self.action_plot,
                                 self.action_data_process,
                                 self.action_mathematics])
#        self.toolbar.addActions([self.action_data_process,
#                                 self.action_data_sift])
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.action_para_templates,
                                          self.action_data_dict])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_about)
        
#        将绘图页面显示为初始页面
        self.stacked_window.setCurrentIndex(2)
        self.last_page = self.action_plot
        self.action_plot.setChecked(True)
        self.syn_function_window.setWindowTitle(QCoreApplication.
                                            translate('MainWindow', '绘图'))

        self.retranslate()
        
# =======连接信号与槽
# =============================================================================
#       主窗口的信号连接        
        self.action_open_normal_datafile.triggered.connect(
                self.slot_open_normal_datafile)
#        文件分析
        self.action_file_process.triggered.connect(self.slot_file_process)
#        按下按钮显示相应的页面
        self.action_data_process.triggered.connect(self.slot_show_page)
        self.action_data_sift.triggered.connect(self.slot_show_page)
        self.action_plot.triggered.connect(self.slot_show_page)
        self.action_mathematics.triggered.connect(self.slot_show_page)
        self.action_para_templates.triggered.connect(self.slot_show_page)
        self.action_data_dict.triggered.connect(self.slot_show_page)
#        按下视图菜单栏下的关闭动作
        self.action_show_paralist_window.triggered.connect(
                self.slot_show_paralist_window)
        self.action_show_syn_window.triggered.connect(
                self.slot_show_syn_window)
#        程序的关于信息
        self.action_about.triggered.connect(self.slot_about)
#        程序帮助
        self.action_help_doc.triggered.connect(self.slot_help_doc)
        self.action_help_video.triggered.connect(self.slot_help_video)
#        程序退出
        self.action_exit.triggered.connect(self.slot_exit)
        
        
        self.signal_import_datafiles.connect(
                self.paralist_window.slot_import_datafiles)

# =============================================================================
#       参数窗口与主窗口和其他窗口的信号连接
        self.paralist_window.signal_quick_plot.connect(
                self.action_plot.trigger)
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
#        self.paralist_window.signal_into_data_dict.connect(
#                self.data_dict_page.slot_add_dict)
#        self.paralist_window.signal_into_data_dict.connect(
#                self.action_data_dict.trigger)
#        数据分析窗口与主窗口和其他窗口的信号与槽连接
        self.data_process_page.signal_request_temps.connect(
                self.slot_send_temps)
        self.data_process_page.signal_save_temp.connect(
                self.para_temp_page.slot_add_para_template)
        self.data_process_page.signal_para_for_plot.connect(
                self.action_plot.trigger)
        self.data_process_page.signal_para_for_plot.connect(
                self.plot_page.slot_plot)
        self.data_process_page.signal_send_status.connect(
                self.slot_display_status_info)
#        数据字典窗口与主窗口和其他窗口的信号与槽连接
        
#        绘图窗口与主窗口和其他窗口的信号与槽连接
        self.plot_page.plotcanvas.signal_send_status.connect(
                self.slot_display_status_info)

        self.syn_function_window.visibilityChanged.connect(
                self.slot_syn_window_close)
#        数据计算窗口与主窗口和其他窗口的信号与槽连接 
        self.mathematics_page.signal_plot_result_para.connect(
                self.plot_page.slot_plot)
        self.mathematics_page.signal_plot_result_para.connect(
                self.action_plot.trigger)
        self.mathematics_page.signal_sendto_ananlysis.connect(
                self.data_process_page.slot_import_datafactory)
        self.mathematics_page.signal_sendto_ananlysis.connect(
                self.action_data_process.trigger)

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
            self.data_dict_page.output_data_dict()
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
        init_dir = self.config_info['INIT DIR OF IMPORTING FILES']
        if init_dir:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, 'Open', init_dir, 'Datafiles (*.txt *.csv *.dat)')
        else:
            file_dir_list, unkonwn = QFileDialog.getOpenFileNames(
                    self, 'Open', CONSTANT.SETUP_DIR, 'Datafiles (*.txt *.csv *.dat)')
        if file_dir_list:
            file_dir_list = [file.replace('/','\\') for file in file_dir_list]
            if os.path.exists(file_dir_list[0]):
                self.config_info['INIT DIR OF IMPORTING FILES'] = os.path.dirname(file_dir_list[0])
            for file_dir in file_dir_list:
                if not(file_dir in self.current_files):
                    try:
                        normal_file = Normal_DataFile(file_dir)
                        import_file_dirs[file_dir] = normal_file.paras_in_file
                        file_dir_l.append(file_dir)
                    except:
#                        这样处理不太好，如果不是文件本身错误而仅是代码错误也会一并认为是文件本身错误
                        nor_datafiles.append(file_dir)
                else:
                    ex_files.append(file_dir)
            if nor_datafiles:
                print_info = '以下文件不是数据文件：'
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
                             QCoreApplication.translate('MainWindow', '关于FastPlot(beta 0.1)'),
                             QCoreApplication.translate('MainWindow',
                                                       '<img src=\'' + CONSTANT.FTCC_LOGO + 
                                                       '''' width='360' height='46'>
                                                       <p><b>FastPlot(beta 0.1)</b></p>
                                                       <br>试飞数据分析软件
                                                       <p>试飞中心 | 试飞工程部
                                                       <br>Copyright &copy; COMAC Flight Test Center.</p>
                                                       '''),
                             QMessageBox.Close,
                             self)
        btn = ms_box.addButton(QCoreApplication.translate('MainWindow', '开发人员'), QMessageBox.ActionRole)
        btn.clicked.connect(developers)
        btn_list = ms_box.buttons()
        btn_list[0].setText(QCoreApplication.translate('MainWindow', '关闭'))
        ms_box.exec_()
        
    def slot_delete_files(self, files : list):
        
        if files:
            for file in files:
                self.current_files.remove(file)
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
    def slot_show_syn_window(self):
        
        if self.syn_function_window.isHidden():
            self.syn_function_window.setHidden(False)
        else:
            self.syn_function_window.setHidden(True)

#        参数窗口关闭后需要把视图下的勾选去掉
    def slot_syn_window_close(self, isclose):
        
        if isclose:
            self.action_show_syn_window.setChecked(True)
        else:
            self.action_show_syn_window.setChecked(False)

#    显示用户选择的界面
    def slot_show_page(self):
        
#        接收发出信号的那个对象
        sender = QObject.sender(self)
        if (sender == self.action_data_process):
            pageindex = 0
            self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数据分析'))
        if (sender == self.action_data_sift):
            pageindex = 1
            self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数据筛选'))
        if (sender == self.action_plot):
            pageindex = 2
#            将新的选择记住
            self.syn_function_window.setWindowTitle(QCoreApplication.
                                                translate('MainWindow', '绘图'))
        if (sender == self.action_mathematics):
            pageindex = 3
            self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数学计算')) 
        if (sender == self.action_para_templates):
            pageindex = 4
            self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '参数模板')) 
        if (sender == self.action_data_dict):
            pageindex = 5
            self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数据字典')) 
        self.stacked_window.setCurrentIndex(pageindex)
    
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
        
        self.data_sift_page.slot_update_current_files(self.current_files)
        self.mathematics_page.plain_text_edit_conmandline.slot_update_current_files(self.current_files)
        self.plot_page.plotcanvas._current_files = self.current_files
        
    def slot_data_dict_changed(self, data_dict : dict):
        
        self.plot_page.plotcanvas._data_dict = data_dict
    
#    用于将信息显示在状态栏，也可以用于清除状态栏信息
    def slot_display_status_info(self, message : str, timeout : int):
        
        if message:
            self.statusbar.clearMessage()
            self.statusbar.showMessage(message, timeout)
            
    def slot_help_doc(self):
        
        if os.path.exists(CONSTANT.DIR_HELP_DOC):
            os.startfile(CONSTANT.DIR_HELP_DOC)
        else:
            QMessageBox.warning(self,
                      QCoreApplication.translate('MainWindow', '帮助文档错误'),
                      QCoreApplication.translate('MainWindow', '未发现帮助文档，请联系开发人员！'),
                      QMessageBox.Yes)
    
    def slot_help_video(self):
        
        if os.path.exists(CONSTANT.DIR_HELP_VIDEO):
            os.startfile(CONSTANT.DIR_HELP_VIDEO)
        else:
            QMessageBox.warning(self,
                      QCoreApplication.translate('MainWindow', '视频教程错误'),
                      QCoreApplication.translate('MainWindow', '未发现视频教程，请联系开发人员！'),
                      QMessageBox.Yes)

# =============================================================================
# 功能函数模块
# =============================================================================
    def load_config_info(self):
        
#        导入配置信息
        try:
            with open(CONSTANT.SETUP_DIR + r'\data\config_info.txt', 'r') as file:
                while file.readline():
    #                readline函数会把'\n'也读进来
                     name = file.readline()
    #                 去除'\n'
                     name = name.strip('\n')
                     config = file.readline()
                     config = config.strip('\n')
                     if name == 'INIT DIR OF IMPORTING FILES':
                         if os.path.exists(config):
                             self.config_info[name] = config
                         else:
                             self.config_info[name] = ''
                     else:
                         self.config_info[name] = config
        except IOError:
            pass
        
    def output_config_info(self):
        
#        判断是否有模板存在
        if self.config_info:
#                打开保存模板的文件（将从头写入，覆盖之前的内容）
            with open(CONSTANT.SETUP_DIR + r'\data\config_info.txt', 'w') as file:
#                将内存中的模板一一写入文件
                for name in self.config_info:
                    file.write('========\n')
                    file.write(name)
                    file.write('\n')
                    file.write(self.config_info[name])
                    file.write('\n')
    
#    def show_page(self, pageindex):
#        
#        if self.stacked_window.isHidden():
#            self.stacked_window.show()
#            self.stacked_window.setCurrentIndex(pageindex)
#        else:
#            self.stacked_window.setCurrentIndex(pageindex)    
# =============================================================================
# 汉化
# =============================================================================
    def retranslate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', 'FastPlot(beta 0.1)'))
        self.menu_file.setTitle(_translate('MainWindow', '文件'))
#        self.menu_open.setTitle(_translate('MainWindow', '打开'))
#        self.menu_edit.setTitle(_translate('MainWindow', '编辑'))
        self.menu_view.setTitle(_translate('MainWindow', '视图'))
        self.menu_panels.setTitle(_translate('MainWindow', '面板'))
        self.menu_tools.setTitle(_translate('MainWindow', '工具'))
#        self.menu_data_analysis.setTitle(_translate('MainWindow', '数据分析'))
        self.menu_data_manage.setTitle(_translate('MainWindow', '数据管理'))
#        self.menu_window.setTitle(_translate('MainWindow', '窗口'))
        self.menu_help.setTitle(_translate('MainWindow', '帮助'))
        self.toolbar.setWindowTitle(_translate('MainWindow', '工具栏'))
        self.action_open_normal_datafile.setText(_translate('MainWindow', '打开通用数据'))
        self.action_open_normal_datafile.setToolTip(_translate('MainWindow', '打开通用数据'))
        self.action_file_process.setText(_translate('MainWindow', '文件导出'))
        self.action_exit.setText(_translate('MainWindow', '退出'))
        self.action_mathematics.setText(_translate('MainWindow', '数学计算'))
        self.action_data_process.setText(_translate('MainWindow', '数据分析'))
        self.action_data_sift.setText(_translate('MainWindow', '数据筛选'))
        self.action_para_templates.setText(_translate('MainWindow', '参数模板'))
        self.action_data_dict.setText(_translate('MainWindow', '数据字典'))
#        self.action_options.setText(_translate('MainWindow', '选项'))
        self.action_about.setText(_translate('MainWindow', '关于FastPlot'))
        self.action_plot.setText(_translate('MainWindow', '绘图'))
        self.action_show_paralist_window.setText(_translate('MainWindow', '参数浏览器'))
        self.action_show_syn_window.setText(_translate('MainWindow', '功能模块'))
        self.action_help_doc.setText(_translate('MainWindow', 'FastPlot帮助文档'))
        self.action_help_video.setText(_translate('MainWindow', 'FastPlot视频教程'))
        
def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setup()
    mainwindow.show()
    return app.exec_()