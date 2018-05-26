# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-20
# 编码人员：严骅 王学良
# 简述：文件类
#
# =======使用说明
# 
#
# =======日志
#
#
# =======后续改进
# 暂时只实现选择文件夹载入项目，后续需要实现选择项目文件载入项目
# =============================================================================

import pandas as pd

class NormalDatafileModel(object):
    
    def __init__(self):
        
#        文件路径
        self.file_dir = None
#        文件名
        self.filename = None
#        下面的属性目前都是不可更改的，所以定为私有属性，后续做时间同步或升降频可能会变动
#        文件中的参数
        self.paras_in_file = []
#        采样开始时间
        self.time_begin = None
#        采样结束时间
        self.time_end = None
#        采样频率
        self.sample_frequency = None

    def config(self, filename):
        
        self.file_dir = filename

        pos = filename.rindex('/')
        self.filename = filename[pos+1:]
        
        para_name = self.header_input(filename,sep='\s+') #DataFrame: input the first row of data file
        para_list = para_name.values.tolist()[0]
        self.paras_in_file = para_list
        
    
#get_info:根据一般试飞数据文件的文件名获取，试飞数据相关信息，返回信息列表        
    def get_info(self,filename=""):
        if filename:
            lpos=filename.rindex('/')
            rpos=filename.rindex('.')
            info_name=filename[lpos+1:rpos]
            info_list=info_name.split('-')
        return info_list
                       
#header_input: 仅导入数据文件的第一行即参数名行，可与 cols_input函数一起使用
    def header_input(self,filename="",sep=""): 
        if filename=="":
            filename=self.filename
        if sep=="":
            sep=self.sep
        with open(filename,'rb') as f:
            if filename.endswith(('.txt','.csv')):
                if sep=='all':
                    #Use str or object to preserve and not interpret dtype
                    df=pd.read_table(f,sep='\s+|\t|,|;',header=None,nrows=1,engine='python',dtype=object)
                    #or only input the columns index:nrows=0,remove header=None
                else:
                    df=pd.read_table(f,sep=sep,header=None,nrows=1,engine='c',dtype=object)
            if filename.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,header=None)
                df=df.iloc[0,:]  #select the first row
        return df       

#cols_input: 按列读取数据文件，cols指定参数名列表，按cols指定的参数名列读取数据    
    def cols_input(self,filename="",cols=[],sep="\s+"):  #without chunkinput now!!
        if filename=="":
            filename=self.filename
        if sep=="":
            sep=self.sep
        with open(filename,'rb') as f:
            if filename.endswith(('.txt','.csv')):
                if sep=='all':
                    df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,engine='python')
                else:
                    df=pd.read_table(f,sep=sep,usecols=cols,engine='c')
            if filename.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,usecols=cols)
        return df

#save_file: 保存数据到文件，保存的数据格式为df:pandas dataframe或series    
    def save_file(self,filename,df,sep='\t'):
        df.to_csv(filename,sep,index=False,encoding="utf-8")

#DftoList:  将dataframe类型数据转换为二维列表[[],[],...]        
    def DftoList(self,df):
        return df.values.tolist()
    
