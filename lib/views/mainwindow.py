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
                             QDockWidget, QVBoxLayout)

# =============================================================================
# Package views imports
# =============================================================================
from views.plot_window import PlotWindow
from views.paralist_window import ParalistWindow
from models.datafile_model import Normal_DataFile
from views.data_manage_window import DataManageWindow
from views.data_analysis_window import DataAnalysisWindow
from views.mathematics_window import MathematicsWindow
import views.constant as CONSTANT
# =============================================================================
# Main Window
# =============================================================================
class MainWindow(QMainWindow):   

    signal_import_datafiles = pyqtSignal(dict)
    signal_current_files_changed = pyqtSignal(list)
    
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
        self.plot_page = PlotWindow(self.syn_function_window)
        self.plot_page.setup()
        self.stacked_window.addWidget(self.plot_page)
        self.mathematics_page = MathematicsWindow(self.syn_window_contents)
        self.mathematics_page.setup()
        self.stacked_window.addWidget(self.mathematics_page)
        self.data_analysis_page = DataAnalysisWindow(self.syn_window_contents)
        self.data_analysis_page.setup()
        self.stacked_window.addWidget(self.data_analysis_page)
        self.data_manage_page = DataManageWindow(self.syn_window_contents)
        self.data_manage_page.setup()
        self.stacked_window.addWidget(self.data_manage_page)
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
        self.menu_open = QMenu(self.menu_file)
#        self.menu_edit = QMenu(self.menubar)
        self.menu_view = QMenu(self.menubar)
        self.menu_panes = QMenu(self.menu_view)
        self.menu_tools = QMenu(self.menubar)
#        self.menu_window = QMenu(self.menubar)
        self.menu_help = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        
#        创建状态栏
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
#        创建工具栏
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        
#        创建动作
        self.action_open_normal_datafile = QAction(self)
        self.action_open_normal_datafile.setIcon(QIcon(CONSTANT.ICON_OPEN))
        self.action_exit = QAction(self)
        self.action_exit.setIcon(QIcon(CONSTANT.ICON_EIXT))
        self.action_mathematics = QAction(self)
        self.action_mathematics.setIcon(QIcon(CONSTANT.ICON_MATHEMATICS))
        self.action_mathematics.setCheckable(True)
        self.action_data_analysis = QAction(self)
        self.action_data_analysis.setIcon(QIcon(CONSTANT.ICON_DATA_ANA))
        self.action_data_analysis.setCheckable(True)
        self.action_data_manage = QAction(self)
        self.action_data_manage.setIcon(QIcon(CONSTANT.ICON_DATA_MAN))
        self.action_data_manage.setCheckable(True)
        self.action_options = QAction(self)
        self.action_options.setIcon(QIcon(CONSTANT.ICON_SETTING))
        self.action_about = QAction(self)
        self.action_about.setIcon(QIcon(CONSTANT.ICON_ABOUT))
        self.action_plot = QAction(self)
        self.action_plot.setIcon(QIcon(CONSTANT.ICON_PLOT))
        self.action_plot.setCheckable(True)
        self.action_show_paralist_window = QAction(self)
        self.action_show_paralist_window.setCheckable(True)
        self.action_show_paralist_window.setChecked(True)
        self.action_show_syn_window = QAction(self)
        self.action_show_syn_window.setCheckable(True)
        self.action_show_syn_window.setChecked(True)
        
#        将动作添加到对应的菜单下       
        self.menu_open.addAction(self.action_open_normal_datafile)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu_open.menuAction())
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_panes.addActions([self.action_show_paralist_window,
                                    self.action_show_syn_window])
        self.menu_view.addAction(self.menu_panes.menuAction())
        self.menu_tools.addAction(self.action_plot)
        self.menu_tools.addAction(self.action_mathematics)
        self.menu_tools.addAction(self.action_data_analysis)
        self.menu_tools.addAction(self.action_data_manage)
        self.menu_tools.addAction(self.action_options)
        self.menu_help.addAction(self.action_about)

#        添加菜单栏
        self.menubar.addAction(self.menu_file.menuAction())
#        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
#        self.menubar.addAction(self.menu_window.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
#        添加工具栏
        self.toolbar.addAction(self.action_open_normal_datafile)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_data_analysis)
        self.toolbar.addAction(self.action_plot)
        self.toolbar.addAction(self.action_mathematics)
        self.toolbar.addAction(self.action_data_manage)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_about)
        
#        将绘图页面显示为初始页面
        self.stacked_window.setCurrentIndex(0)
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
#        按下按钮显示相应的页面
        self.action_plot.triggered.connect(self.slot_show_page)
        self.action_mathematics.triggered.connect(self.slot_show_page)
        self.action_data_analysis.triggered.connect(self.slot_show_page)
        self.action_data_manage.triggered.connect(self.slot_show_page)
#        按下视图菜单栏下的关闭动作
        self.action_show_paralist_window.triggered.connect(
                self.slot_show_paralist_window)
        self.action_show_syn_window.triggered.connect(
                self.slot_show_syn_window)
#        程序的关于信息
        self.action_about.triggered.connect(self.slot_about)
#        程序退出
        self.action_exit.triggered.connect(self.slot_exit)
#        当有文件导入时，将发送最新文件状态给需要用到窗口
        self.signal_current_files_changed.connect(
                self.data_analysis_page.slot_update_current_files)
        self.signal_current_files_changed.connect(
                self.mathematics_page.plain_text_edit_conmandline.slot_update_current_files)
        
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
                self.data_analysis_page.slot_import_paras)
        self.paralist_window.signal_into_analysis.connect(
                self.slot_show_data_process_page)
        self.paralist_window.signal_delete_files.connect(
                self.slot_delete_files)
#        分析数据窗口与主窗口和其他窗口的信号与槽连接
        self.data_analysis_page.signal_request_temps.connect(
                self.slot_send_temps)
        self.data_analysis_page.signal_save_temp.connect(
                self.data_manage_page.slot_add_para_template)
        self.data_analysis_page.signal_para_for_plot.connect(
                self.plot_page.slot_plot)
        self.data_analysis_page.signal_para_for_plot.connect(
                self.action_plot.trigger)
#        绘图窗口与主窗口和其他窗口的信号与槽连接 
        self.plot_page.signal_request_temps.connect(
                self.slot_send_temps)
        self.plot_page.signal_save_temp.connect(
                self.data_manage_page.slot_add_plot_template)
        self.syn_function_window.visibilityChanged.connect(
                self.slot_syn_window_close)
#        数据计算窗口与主窗口和其他窗口的信号与槽连接 
        self.mathematics_page.signal_plot_result_para.connect(
                self.plot_page.slot_plot)
        self.mathematics_page.signal_plot_result_para.connect(
                self.action_plot.trigger)        

# =============================================================================
# Slots模块            
# =============================================================================
    def closeEvent(self, event : QCloseEvent):

        message = QMessageBox.warning(self,
                      QCoreApplication.translate('ParalistWindow', '退出'),
                      QCoreApplication.translate('ParalistWindow',
                                        '''<p>确定要退出吗？'''),
                      QMessageBox.Yes | QMessageBox.No)
        if (message == QMessageBox.Yes):
            self.data_manage_page.output_temps()
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
                print_info = '<br>以下文件不是数据文件：'
                for file in nor_datafiles:
                    print_info += ('<br>' + file)
                QMessageBox.information(self,
                                        QCoreApplication.translate('MainWindow', '导入文件提示'),
                                        QCoreApplication.translate('MainWindow', print_info))
            if ex_files:
                print_info = '<br>以下文件已存在：'
                for file in ex_files:
                    print_info += ('<br>' + file)
                QMessageBox.information(self,
                                        QCoreApplication.translate('MainWindow', '导入文件提示'),
                                        QCoreApplication.translate('MainWindow', print_info))
        if file_dir_l:
            self.current_files += file_dir_l
            self.signal_current_files_changed.emit(self.current_files)
        if import_file_dirs:
            self.signal_import_datafiles.emit(import_file_dirs)

#    与关于退出有关的显示
    def slot_exit(self):
        
        QApplication.closeAllWindows()
            
#    显示About信息
    def slot_about(self):
        
        QMessageBox.about(self,
            QCoreApplication.translate('MainWindow', '关于FastPlot'),
            QCoreApplication.translate('MainWindow', '''<b>FastPlot</b>
            <br>试飞数据绘图软件
            <br>Copyright &copy; FTCC
            <p>由试飞中心试飞工程部绘图软件开发团队开发维护
            '''))
        
    def slot_delete_files(self, files : list):
        
        if files:
            for file in files:
                self.current_files.remove(file)
            self.signal_current_files_changed.emit(self.current_files)

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
            
    def slot_show_data_process_page(self):
        
        self.action_data_analysis.trigger()
        self.data_analysis_page.combo_box_analysis_type.setCurrentIndex(0)
        
#    显示用户选择的界面
    def slot_show_page(self):
        
#        接收发出信号的那个对象
        sender = QObject.sender(self)
        if (sender == self.action_plot):
            if (self.last_page == self.action_plot):
#                再次按下同一按钮且按钮是选择状态，按钮会自动弹起，
#                但这不是期望的，所以设置动作仍被选择
                self.action_plot.setChecked(True)                  
            else:
#                将上一选中动作按钮弹起
                self.last_page.setChecked(False)
                self.show_page(0)
#                将新的选择记住
                self.last_page = self.action_plot
                self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '绘图'))
                
        if (sender == self.action_mathematics):
            if (self.last_page == self.action_mathematics):
                self.action_mathematics.setChecked(True)                  
            else:
                self.last_page.setChecked(False)
                self.show_page(1)
                self.last_page = self.action_mathematics
                self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数学计算')) 
        if (sender == self.action_data_analysis):
            if (self.last_page == self.action_data_analysis):
                self.action_data_analysis.setChecked(True)                  
            else:
                self.last_page.setChecked(False)
                self.show_page(2)
                self.last_page = self.action_data_analysis
                self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数据分析'))
        if (sender == self.action_data_manage):
            if (self.last_page == self.action_data_manage):
                self.action_data_manage.setChecked(True)                  
            else:
                self.last_page.setChecked(False)
                self.show_page(3)
                self.last_page = self.action_data_manage
                self.syn_function_window.setWindowTitle(QCoreApplication.
                                                    translate('MainWindow', '数据管理'))
    
    def slot_send_temps(self, type_temp : str):
        
        dict_files = self.paralist_window.get_dict_files_tree()
        if type_temp == 'para_template':
            self.data_analysis_page.slot_sel_temp(dict_files, self.data_manage_page.paras_temps)
        if type_temp == 'plot_template':
            self.plot_page.slot_sel_temp(dict_files, self.data_manage_page.plot_temps)

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
    
    def show_page(self, pageindex):
        
        if self.stacked_window.isHidden():
            self.stacked_window.show()
            self.stacked_window.setCurrentIndex(pageindex)
        else:
            self.stacked_window.setCurrentIndex(pageindex)    
# =============================================================================
# 汉化
# =============================================================================
    def retranslate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', 'FastPlot'))
        self.menu_file.setTitle(_translate('MainWindow', '文件'))
        self.menu_open.setTitle(_translate('MainWindow', '打开'))
#        self.menu_edit.setTitle(_translate('MainWindow', '编辑'))
        self.menu_view.setTitle(_translate('MainWindow', '视图'))
        self.menu_panes.setTitle(_translate('MainWindow', '面板'))
        self.menu_tools.setTitle(_translate('MainWindow', '工具'))
#        self.menu_window.setTitle(_translate('MainWindow', '窗口'))
        self.menu_help.setTitle(_translate('MainWindow', '帮助'))
        self.toolbar.setWindowTitle(_translate('MainWindow', '工具栏'))
        self.action_open_normal_datafile.setText(_translate('MainWindow', '通用数据'))
        self.action_open_normal_datafile.setToolTip(_translate('MainWindow', '打开通用数据'))
        self.action_exit.setText(_translate('MainWindow', '退出'))
        self.action_mathematics.setText(_translate('MainWindow', '数学计算'))
        self.action_data_analysis.setText(_translate('MainWindow', '数据分析'))
        self.action_data_manage.setText(_translate('MainWindow', '数据管理'))
        self.action_options.setText(_translate('MainWindow', '选项'))
        self.action_about.setText(_translate('MainWindow', '关于'))
        self.action_plot.setText(_translate('MainWindow', '绘图'))
        self.action_show_paralist_window.setText(_translate('MainWindow', '参数浏览器'))
        self.action_show_syn_window.setText(_translate('MainWindow', '功能模块'))
        
def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setup()
    mainwindow.show()
    return app.exec_()