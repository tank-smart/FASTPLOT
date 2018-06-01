# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
#说明：通用文件类，是所有其它文件类的基类
#功能：数据文件的导入导出功能
#properties：
#filedir: 文件路径
#sep: 定义文件的分隔符，sep='\s+' '\t' ',' ';' 'all', 其中'all'为匹配任意分隔符
#filename: 文件名

#functions:
#get_name(filedir=""):返回文件路径中的文件名
#all_input(self,filedir="",sep=""):一次直接读入整个文件，返回dataframe
#chunkAll_input(self,filedir="",sep="",chunksize=50000)：分段读入整个文件，返回dataframe
#chunk_input(self,filedir="",sep="",chunksize=50000)：分段读入文件，返回generator可迭代访问每段读入的dataframe
#save_file(self,filedir,df,sep='\t')：dataframe数据保存为文本文件
#df_tolist(self,df)：dataframe转为列表
# =======使用说明
# 
#
# =======日志
#
#
# =============================================================================

import pandas as pd

class DataFile(object):
    def __init__(self,filedir="",sep="\s+"):
        self.filedir=filedir
        self.sep=sep
        self.filename=self.get_name(filedir)

#get_name:根据文件路径获取文件名        
    def get_name(self,filedir=""):
        if filedir=="":
            filedir=self.filedir
        pos = filedir.rindex('\\')
        filename = filedir[pos+1:]
        return filename
    
#all_input:一次导入整个数据文件（文件过大时会卡死），如不指定filedir，sep会使用类属性        
    def all_input(self,filedir="",sep=""):
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        if filedir.endswith(('.txt','.csv')):
            with open(filedir,'r') as f:
                if sep=='all':
                    df=pd.read_table(f,sep='\s+|\t|,|;',engine='python')
                else:
                    df=pd.read_table(f,sep=sep,engine='c')
        if filedir.endswith(('.xls','.xlsx')):
            with open(filedir,'r') as f:
                df=pd.read_excel(f)
        return df

#chunkAll_input: 分段导入整个数据文件，chunksize指定每次读入的行数,返回完整的dataframe
    def chunkAll_input(self,filedir="",sep="",chunksize=50000):
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        loop = True
        #chunksize = 50000
        chunks = []
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    reader=pd.read_table(f,sep='\s+|\t|,|;',engine='python',iterator=True)
                else:
                    reader=pd.read_table(f,sep='\s+',engine='c',iterator=True)
                while loop:
                    try:
                        chunk = reader.get_chunk(chunksize)
                        chunks.append(chunk)
                    except StopIteration:
                        loop = False
                df = pd.concat(chunks, ignore_index=True)
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f)
        return df
    
#chunk_input: 分段导入数据文件，chunksize指定每次读入的行数，返回每一段读取的chunk
        #使用Yield使函数返回generator，可通过迭代获取yield指定的chunk，chunk为dataframe类型
    def chunk_input(self,filedir="",sep="",chunksize=50000):
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        loop=True
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    reader=pd.read_table(f,sep='\s+|\t|,|;',engine='python',iterator=True)
                else:
                    reader=pd.read_table(f,sep='\s+',engine='c',iterator=True)
                while loop:
                    try:
                        chunk = reader.get_chunk(chunksize)
                        yield chunk
                    except StopIteration:
                        loop = False
            if filedir.endswith(('.xls','.xlsx')):
                Nskip=0
                while loop:
                        chunk=pd.read_excel(f,header=None,skiprows=Nskip,nrows=chunksize)
                        if chunk.empty:
                            break
                        Nskip+=chunksize
                        yield chunk
                    
#save_file: 保存数据到文件，保存的数据格式为df:pandas dataframe或series    
    def save_file(self,filedir,df,sep='\t'):
        df.to_csv(filedir,sep,index=False,encoding="utf-8")

#DftoList:  将dataframe类型数据转换为二维列表[[],[],...]        
    def df_tolist(self,df):
        return df.values.tolist()
    
#——————class normal_DataFile————————
#说明：一般试飞数据文件类，继承自DtaFile类
#功能：一般试飞数据文件的导入导出和配置功能
#properties：
#父类属性
#info_list: 数据文件信息列表
#paras_in_file: 数据文件包含的参数名列表
#time_range: 数据文件的起止时间列表[begin,end]
#sample_frequency： 数据文件的采样频率

#functions:
#父类函数 （DataFile.function）
#def get_info(self,filedir=""):获取数据文件名信息，返回信息列表
#def get_paraslist(self,filedir=""):获取文件中所有的的参数列表，返回参数列表
#def get_timerange(self,filedir=""):获取数据文件的起始时间和终止时间，以[begin,end]形式返回列表
#def header_input(self,filedir="",sep="")：读取数据文件第一行（参数名）
#def cols_input(self,filedir="",cols=[],sep="\s+")：按列读取数据文件，cols指定参数名列表，按cols指定的参数名列读取数据
#def save_file(self,filedir,df,sep='\t')：dataframe数据保存为文本文件
#def df_tolist(self,df)：dataframe转为列表

class Normal_DataFile(DataFile):
    def __init__(self,filedir="",sep="\s+"):
        super(Normal_DataFile,self).__init__(filedir,sep)
        self.info_list=self.get_info(filedir)
        self.paras_in_file=self.get_paraslist(filedir)
#        self.time_range=self.get_timerange(filedir)  #！可能造成IO过多，使得速度变慢
        self.sample_frequency=self.info_list[-1]

#get_paralist:获取文件中所有的的参数列表        
    def get_paraslist(self,filedir=""):
        para_name = self.header_input(filedir,sep='\s+')
        para_list = para_name.values.tolist()[0]
        return para_list

#get_timerange:获取数据文件的起始时间和终止时间，以[begin,end]形式返回
    def get_timerange(self,filedir=""):
        if filedir=="":
            filedir=self.filedir
        df_time=self.cols_input(filedir,cols=[self.paras_in_file[0]],sep='\s+')
        time_range=[df_time.iat[0,0],df_time.iat[-1,0]]
        return time_range
        
#get_info:根据一般试飞数据文件的文件名获取，试飞数据相关信息，返回信息列表        
    def get_info(self,filedir=""):
        if filedir:
            lpos=filedir.rindex('\\')
            rpos=filedir.rindex('.')
            info_name=filedir[lpos+1:rpos]
            info_list=info_name.split('-')
        return info_list
                       
#header_input: 仅导入数据文件的第一行即参数名行，可与 cols_input函数一起使用
    def header_input(self,filedir="",sep=""): 
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    #Use str or object to preserve and not interpret dtype
                    df=pd.read_table(f,sep='\s+|\t|,|;',header=None,nrows=1,engine='python',dtype=object)
                    #or only input the columns index:nrows=0,remove header=None
                else:
                    df=pd.read_table(f,sep=sep,header=None,nrows=1,engine='c',dtype=object)
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,header=None)
                df=df.iloc[0,:]  #select the first row
        return df       

#cols_input: 按列读取数据文件，cols指定参数名列表，按cols指定的参数名列读取数据    
    def cols_input(self,filedir="",cols=[],sep="\s+"):  #without chunkinput now!!
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,engine='python')
                else:
                    df=pd.read_table(f,sep=sep,usecols=cols,engine='c')
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,usecols=cols)
        return df

#note: in python 3 change file open mode as 'r' instead of 'rb', as return str not bytes
    
