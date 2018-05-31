# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：项目类
#
# =======使用说明
# 
#
# =======日志
# 

# =======后续改进
# 暂时只实现选择文件夹载入项目，后续需要实现选择项目文件载入项目
# =============================================================================

# =============================================================================
# Stdlib imports
# =============================================================================
import re

# =============================================================================
# Package views imports
# =============================================================================
<<<<<<< HEAD
from models.datafile_model import Normal_DataFile
=======
from models.normal_datafile_model import NormalDatafileModel
>>>>>>> 058f8ba1896ebc91db7f8433a6b6b1975d8dc28d

# =============================================================================
# ProjectModel
# =============================================================================
class ProjectModel(object):

# =============================================================================
# 初始化    
# =============================================================================
    def __init__(self):
        
#        项目所涉及的数据文件，列表类型，
        self.datafile_group = []
#        项目所涉及的结果文件，列表类型
        self.resultfile_group = []

# =============================================================================
# 功能函数模块
# =============================================================================
#    将导入的文件存入项目类的数据文件组中
    def open_normal_datafiles(self, filename_list):
        
        if filename_list:
            for filename in filename_list:
                file = Normal_DataFile(filename)
                self.datafile_group.append(file)
                
#    在数据文件中搜索参数，返回参数的列表
    def search_para(self, para_name):
        
        result = {}
        if (para_name and self.datafile_group):
            pattern = re.compile('.*' + para_name + '.*')
            for file in self.datafile_group:
#                字典的推导式
                 search_paras = [para for para
                                 in file.paras_in_file
                                 if re.match(pattern, para)]
                 if search_paras:
                     result[file.filedir] = search_paras
        else:
            result = self.get_datafile_for_tree()
        
        return result
        
                
    def get_datafile_for_tree(self):
        
        datafiles = {}
        for file in self.datafile_group:
            datafiles[file.filedir] = file.paras_in_file
        return datafiles

# =============================================================================
# 辅助函数模块      
# =============================================================================
        
