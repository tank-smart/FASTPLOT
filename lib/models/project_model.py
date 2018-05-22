# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-20
# 编码人员：王学良
# 简述：项目类
#
# =======使用说明
# 
#
# =======日志
# 1.2018-05-20 王学良创建文件

# =======后续改进
# 暂时只实现选择文件夹载入项目，后续需要实现选择项目文件载入项目
# =============================================================================

import os
from models.class_datafile import normal_DataFile

class ProjectModel(object):
    
    def __init__(self):
        
#        项目路径
        self.project_dir = None
#        项目名称
        self.project_name = None
#        项目所涉及的数据文件，列表类型，
        self.datafile_group = {}
#        项目所涉及的结果文件，列表类型
        self.resultfile_group = []

# =============================================================================
# 主功能函数
# =============================================================================
    def new_project(self, project_dir, project_name):

#        为了简化，只有两个输入都非空时才赋值，后续应细化下        
        if (project_dir and project_name):
            self.project_dir = project_dir
            self.project_name = project_name
            total_pro_dir = self.get_total_pro_dir()
#            创建项目目录
            os.mkdir(total_pro_dir)
            os.mkdir(total_pro_dir + '\\' + 'datafile')
            os.mkdir(total_pro_dir + '\\' + 'resultfile')

#    从提供的项目路径中载入项目 ,同时直接覆盖原有的项目       
    def open_project(self, sel_dir):
       
        if (sel_dir and self.is_project(sel_dir)):
#            从sel_dir中分离出项目路径和项目名称 
            temp_str = sel_dir.split('\\')
            self.project_name = temp_str[len(temp_str) - 1]
            temp_str = sel_dir.split('\\' + self.project_name)
            self.project_dir = temp_str[0]
            return True
        else:
            return False

    def import_datafile(self, file_name):
        if file_name:  #file_name is a list
            for each_file in file_name:
                file_temp=normal_DataFile(each_file)
                para_name=file_temp.header_input(each_file,sep='\s+') #DataFrame: input the first row of data file
#                pos=each_file.rindex('/')
#                root_name=each_file[pos+1:]
                para_list=para_name.values.tolist()[0]
                self.datafile_group[each_file] = para_list
                
    def get_datafile_group(self):
        return self.datafile_group
# =============================================================================
# 辅助函数        
# =============================================================================
#    判断是否为一个项目
    def is_project(self, sel_dir):
        
        if sel_dir:
            pro_dir = self.get_total_pro_dir()
            data_dir = sel_dir + '\\' + 'datafile'
            result_dir = sel_dir + '\\' + 'resultfile'
    #        如果是当前项目也返回假
            if (pro_dir == sel_dir or not(os.path.isdir(data_dir)) 
                or not(os.path.isdir(result_dir))):
                return False
            else:
                return True
        else:
            return False

#    因为把一个文件夹当做项目，所以增加了获得完全路径的函数        
    def get_total_pro_dir(self):
        if (self.project_dir and self.project_name):
            return (self.project_dir + '\\' + self.project_name)
        else:
            return None
        
