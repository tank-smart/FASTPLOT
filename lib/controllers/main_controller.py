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
#
# =============================================================================

import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from views.mainwindow import MainWindow
from models.project_model import ProjectModel


class MainController(object):
    
    def __init__(self):
        
        self.app = QApplication(sys.argv)
        self.mw = MainWindow()
        self.project = ProjectModel()
    
    def link_mainwindow_anction(self):
        
        self.mw.action_open_normal_datafile.triggered.connect(self.control_open_normal_datafile)
        self.mw.mw_paralist_dock.line_edit_search_para.textChanged.connect(self.control_search_para)
        self.mw.action_export_data.triggered.connect(self.control_export_data)
        
    def control_start(self):    
        
        self.mw.setup()
        self.link_mainwindow_anction()
        self.mw.show()
        return self.app.exec_()

    def control_open_normal_datafile(self):
        
#        选择文件，可进行多选
        file_name, ok = QFileDialog.getOpenFileNames(self.mw, 'Open', r'E:\\')
        self.project.open_normal_datafiles(file_name)
        self.mw.mw_paralist_dock.display_file_group(self.project.get_datafile_for_tree())

    def control_search_para(self, para_name):
        
        result = self.project.search_para(para_name)
        self.mw.mw_paralist_dock.display_file_group(result)
        self.mw.mw_paralist_dock.tree_widget_display_datafile.expandAll()

    def control_export_data(self):
        self.mw.view_data_export()  

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
