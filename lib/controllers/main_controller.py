# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-17
# 编码人员：王学良
# 简述：主控制器
#
# =======使用说明
# 。。。
#
# =======日志
# 1.2018-05-17 王学良创建文件
# =============================================================================

import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QAbstractItemView, QTreeWidgetItem
from views.mainwindow import MainWindow
from models.project_model import ProjectModel


class MainController(object):
    
    def __init__(self):
        
        self.app = QApplication(sys.argv)
        self.mw = MainWindow()
        self.project = ProjectModel()
    
    def link_mainwindow_anction(self):
        
        self.mw.action_new.triggered.connect(self.control_new)
        self.mw.action_open.triggered.connect(self.control_open)
        self.mw.action_about.triggered.connect(self.control_about)
        self.mw.action_paralist_dock_isclosed.triggered.connect(self.control_paralist_dock_isclosed)
        self.mw.action_exit.triggered.connect(self.control_exit)
        self.mw.action_import_normal_datafile.triggered.connect(self.control_import_normal_datafile)
        
    def control_start(self):    
        
        self.mw.setup()
        self.link_mainwindow_anction()
        self.mw.show()
        return self.app.exec_()
    
    def control_new(self):
        
        self.project = ProjectModel()
#        从主窗口中获得路径和名称
        pro_dir, pro_name = self.mw.view_new()
#        给项目对象赋值
        self.project.new_project(pro_dir, pro_name)
#        将窗口标题改成项目路径
        self.mw.view_set_window_title(self.project.get_total_pro_dir())

    def control_open(self):

#        显示项目文件夹选择对话框        
        sel_pro = self.mw.view_open()
#        对原来的项目对象进行重新赋值
        open_status = self.project.open_project(sel_pro)
#        显示项目打开状态
        self.mw.view_open_status(open_status, self.project.get_total_pro_dir())
#        将窗口标题改成项目路径
        self.mw.view_set_window_title(self.project.get_total_pro_dir())

    def control_import_normal_datafile(self):
        file_name, ok=QFileDialog.getOpenFileNames(self.mw,'Load','D:/')  #multi files input
        self.project.import_datafile(file_name)
        self.mw.mw_paralist_dock.display(self.project.get_datafile_group())

    def control_export_data(self):
        pass  
    
    def control_exit(self):
        
        QApplication.closeAllWindows()  

    def control_simple_math(self):
        pass  
    
    def control_testpoint_manage(self):
        pass  
    
    def control_synchronization(self):
        pass  

    def control_tuning(self):
        pass  
    
    def control_para_manage(self):
        pass 
    
    def control_temp_manage(self):
        pass  

    def control_options(self):
        pass  
    
    def control_about(self):
        self.mw.view_about()  
    
    def control_quick_plot(self):
        pass  
    
    def control_custom_defined_plot(self):
        pass 
    
    def control_multi_source_plot(self):
        pass  
    
    def control_paralist_dock_isclosed(self):
        
        self.mw.control_paralist_dock_isclosed() 
