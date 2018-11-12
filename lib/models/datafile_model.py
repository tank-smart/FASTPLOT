# -*- coding: utf-8 -*-
# =============================================================================
# =======概述
# 文件名：datafile_model.py
# 简述：文件类
#
# =======内容
# 包含类：
# class DataFile(object)
# class Normal_DataFile(DataFile)
#
# =======使用说明
# 参考类的使用说明
#
# =======日志

# =======备注
# note1: in python 3 recommend change file open mode as 'r' instead of 'rb', 
# as return str not bytes
# =============================================================================


# =============================================================================
# =======imports
import pandas as pd
import scipy.io as sio
import re
import models.time_model as Time
import time as time

# =======类基本信息
#class DataFile
#说明：通用文件类，是所有其它文件类的基类
#功能：数据文件的导入导出功能
# =====properties：
#filedir: 文件路径
#sep: 定义文件的分隔符，sep='\s+' '\t' ',' ';' 'all', 其中'all'为匹配任意分隔符
#filename: 文件名
# =====functions:
#get_name(filedir=""):返回文件路径中的文件名
#all_input(self,filedir="",sep=""):一次直接读入整个文件，返回dataframe
#chunkAll_input(self,filedir="",sep="",chunksize=50000)：分段读入整个文件，返回dataframe
#chunk_input(self,filedir="",sep="",chunksize=50000)：分段读入文件，返回generator可迭代访问每段读入的dataframe
#rows_input(self,filedir="",sep="",skiprows=None): 跳行读入文件，以此方式按行读入文件，返回dataframe
#save_file(self,filedir,df,sep='\t')：dataframe数据保存为文本文件
#append_file(self,filedir,df,sep='\t'):dataframe数据追加保存为文本文件
#df_tolist(self,df)：dataframe转为列表
# =======使用说明
# 实例化类

class DataFile(object):
    def __init__(self,filedir='',sep='\s+'):
        self.filedir=filedir
        self.sep=sep
        self.filename=self.get_name(filedir)

#get_name:根据文件路径获取文件名        
    def get_name(self,filedir=''):
        if filedir=='':
            filedir=self.filedir
        try:
            pos = filedir.rindex('\\')
        except:
            try:
                pos = filedir.rindex('/')
            except:
                pos = -1
        filename = filedir[pos+1:]
        return filename
    
#all_input:一次导入整个数据文件（文件过大时会卡死），如不指定filedir，sep会使用类属性        
    def all_input(self,filedir='',sep=''):
        if filedir=='':
            filedir=self.filedir
        if sep=='':
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
    def chunkAll_input(self,filedir='',sep='',chunksize=50000):
        if filedir=='':
            filedir=self.filedir
        if sep=='':
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
    def chunk_input(self,filedir='',sep='',chunksize=50000):
        if filedir=='':
            filedir=self.filedir
        if sep=='':
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

#rows_input: 按行读取文件内容，skiprows为需要跳过的行的行号列表。暂时使用此种实现方式，经过测试此方法执行效率最高。
    def rows_input(self,filedir="",sep="",skiprows=None):
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    df=pd.read_table(f,sep='\s+|\t|,|;',header=0, skiprows=skiprows,engine='python')
                else:
                    df=pd.read_table(f,sep='\s+',header=0, skiprows=skiprows,engine='c')
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,header=None,skiprows=skiprows)
        return df
    
    def chunk_rows_input(self,filedir="",sep="",skiprows=None,chunksize=100000):
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        loop=True
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    reader=pd.read_table(f,sep='\s+|\t|,|;',skiprows=skiprows,engine='python',iterator=True)
                else:
                    reader=pd.read_table(f,sep='\s+',skiprows=skiprows,engine='c',iterator=True)
                while loop:
                    try:
                        chunk = reader.get_chunk(chunksize)
                        yield chunk
                    except StopIteration:
                        loop = False
#!!!!
            if filedir.endswith(('.xls','.xlsx')):#excel file solution has not completed
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

#append_file：追加内容方式写文件，可用于分段数据处理后的写入文件        
    def append_file(self,filedir,df,sep='\t'):
        df.to_csv(filedir,sep,mode='a',index=False,encoding="utf-8")
        
    def save_matfile(self, filedir, df):
        sio.savemat(filedir, df.to_dict('list'))

#DftoList:  将dataframe类型数据转换为二维列表[[],[],...]        
    def df_tolist(self,df):
        return df.values.tolist()

# =======类基本信息    
# class normal_DataFile
#说明：一般试飞数据文件类，继承自DtaFile类
#功能：一般试飞数据文件的导入导出和配置功能
# =====properties：
#父类属性 （Datafile.properties）
#info_list: 数据文件信息列表
#paras_in_file: 数据文件包含的参数名列表
#time_range: 数据文件的起止时间列表[begin,end]
#sample_frequency： 数据文件的采样频率
# =====functions:
#父类函数 （DataFile.function）
#def get_info(self,filedir=''):获取数据文件名信息，返回信息列表
#def get_paraslist(self,filedir=''):获取文件中所有的的参数列表，返回参数列表
#def get_timerange(self,filedir=''):获取数据文件的起始时间和终止时间，以[begin,end]形式返回列表
#def header_input(self,filedir='',sep='')：读取数据文件第一行（参数名）
#def cols_input(self,filedir='',cols=[],sep='\s+')：按列读取数据文件，cols指定参数名列表，按cols指定的参数名列读取数据
#def save_file(self,filedir,df,sep='\t')：dataframe数据保存为文本文件
#def df_tolist(self,df)：dataframe转为列表
# =======使用说明
# 实例化类
        
class Normal_DataFile(DataFile):
    def __init__(self,filedir='',sep='\s+'):
        super(Normal_DataFile,self).__init__(filedir,sep)
        self.info_list=self.get_info(filedir)
        self.paras_in_file=self.get_paraslist(filedir)
        self.time_range=self.get_timerange(filedir)  #！可能造成IO过多，使得速度变慢
        self.sample_frequency = self.get_sample_frequency(filedir)

#get_paralist:获取文件中所有的的参数列表        
    def get_paraslist(self,filedir=''):
        para_name = self.header_input(filedir,sep='\s+')
        para_list = para_name.values.tolist()[0]
        return para_list

#get_timerange:获取数据文件的起始时间和终止时间，以[begin,end]形式返回
    def get_timerange(self,filedir=''):
        if filedir=='':
            filedir=self.filedir
#        等同于try...finally，保证无论是否出错都能正确关闭文件
#            rb+模式打开是按二进制方式读取数据的，Python3读取得到的数据类型为byte，
#            需要转码成str型。之所以用rb+模式是因为seek函数只在此模式有效
        with open(filedir, 'rb+') as file:
#            获取起始时间
            start_line = file.readline()
            start_line = file.readline()
#            转码
            start_line = start_line.decode()
            start_time = re.split('\s+', start_line)[0]
#            转换成标准格式==！，此处的索引访问是左闭右开
            start_time = Time.timestr_to_stdtimestr(start_time)
#            获取终止时间
            stop_line = ''
            offset = -120
            while True:
                file.seek(offset, 2)
                lines = file.readlines()
                if (len(lines) >= 2):
                    stop_line = lines[-1]
                    stop_line = stop_line.decode()
                    break
                offset = offset * 2
            stop_time = re.split('\s+', stop_line)[0]
            stop_time = Time.timestr_to_stdtimestr(stop_time)
        time_range=[start_time, stop_time]
        return time_range

    def get_sample_frequency(self,filedir=''):
        if filedir=='':
            filedir=self.filedir
        
        fre = 1
        with open(filedir,'r') as f:
            start_line = f.readline()
            start_line = f.readline()
            start_time = re.split('\s+', start_line)[0]
            get_fre = False
            line = f.readline()
            while (not get_fre) and line:
                t = re.split('\s+', line)[0]
                count = Time.count_between_time(start_time, t, 1)
                if count == 1:
                    get_fre = True
                else:
                    fre += 1
                    line = f.readline()
            if not get_fre:
                fre = 0
        return fre       

    def get_sample_fre(self,filedir=""):
        if filedir=="":
            filedir=self.filedir
        time_df=self.cols_input(filedir=filedir,cols=[self.paras_in_file[0]])
        rows=time_df.shape[0]
        time_interval=(time_df[-1,0]-time_df[0,0])/(rows-1)
        return time_interval
        
#get_info:根据一般试飞数据文件的文件名获取，试飞数据相关信息，返回信息列表        
    def get_info(self,filedir=''):
        if filedir:
            lpos=filedir.rindex('\\')
            rpos=filedir.rindex('.')
            info_name=filedir[lpos+1:rpos]
            info_list=info_name.split('-')
        return info_list
                       
#header_input: 仅导入数据文件的第一行即参数名行，可与 cols_input函数一起使用
    def header_input(self,filedir='',sep=''): 
        if filedir=='':
            filedir=self.filedir
        if sep=='':
            sep=self.sep
#            注意excel文件读取必须为rb模式
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    #Use str or object to preserve and not interpret dtype
                    df=pd.read_table(f,sep='\s+|\t|,|;',header=None,nrows=1,engine='python',dtype=object)
                    #or only input the columns index:nrows=0,remove header=None
                else:
                    df=pd.read_table(f,sep=sep,header=None,nrows=1,engine='c',dtype=object)
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,header=None,nrows=1)
#                df=df.iloc[0,:]  #deprecated as pandas version updated 
        return df       

#cols_input: 按列读取数据文件，cols指定参数名列表，按cols指定的参数名列读取数据    
#    def cols_input(self,filedir='',cols=[],sep='\s+',start_time='',stop_time=''):  #without chunkinput now!!
#        if filedir=='':
#            filedir=self.filedir
#        if sep=='':
#            sep=self.sep
#        with open(filedir,'r') as f:
#            if filedir.endswith(('.txt','.csv')):
#                if sep=='all':
#                    df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,engine='python')
#                else:
#                    df=pd.read_table(f,sep=sep,usecols=cols,engine='c')
#            if filedir.endswith(('.xls','.xlsx')):
#                df=pd.read_excel(f,usecols=cols)
#            if (start_time and stop_time):
#                start_rows = Time.lines_between_times(self.time_range[0],
#                                      start_time, self.sample_frequency)
#                stop_rows = Time.lines_between_times(self.time_range[0],
#                                     stop_time, self.sample_frequency)
#                return df[start_rows : stop_rows].copy()
#            else:
#                return df 

#效率相对较低        
#    def cols_input(self,filedir='',cols=[],sep='\s+',start_time='',stop_time=''):  #without chunkinput now!!
#        st = time.time()
#        if filedir=='':
#            filedir=self.filedir
#        if sep=='':
#            sep=self.sep
#        with open(filedir,'r') as f:
#            if filedir.endswith(('.txt','.csv')):
#                if sep=='all':
#                    df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,engine='python')
#                else:
#                    df=pd.read_table(f,sep=sep,usecols=cols,engine='c')
#            if filedir.endswith(('.xls','.xlsx')):
#                df=pd.read_excel(f,usecols=cols)
##            定义参数顺序
#            df = df[cols]
#            if (start_time and stop_time):
#                start_rows = Time.count_between_time(self.time_range[0],
#                                                             start_time, self.sample_frequency)
#                stop_rows = Time.count_between_time(self.time_range[0],
#                                                            stop_time, self.sample_frequency)
#                et = time.time()
#                print(et - st)
##                按下面的dataframe访问方式是左闭右开，所以右边要加1
#                return df[start_rows : (stop_rows + 1)]
#            else:
#                return df 

    def cols_input(self,filedir='',cols=[],sep='\s+',start_time='',stop_time=''):  #without chunkinput now!!

        if filedir=='':
            filedir=self.filedir
        if sep=='':
            sep=self.sep
#            注意若是excel文件读取需要rb模式
        with open(filedir,'r') as f:
            if (start_time and stop_time):
#                count_between_time函数返回的是两个时间的差值
                start_rows = Time.count_between_time(self.time_range[0],
                                                             start_time, self.sample_frequency)
                stop_rows = Time.count_between_time(self.time_range[0],
                                                            stop_time, self.sample_frequency)
                if filedir.endswith(('.txt','.csv')):
                    if sep=='all':
                        df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,
#                                         range是左闭右开
                                         skiprows=list(range(1,start_rows+1)),
                                         nrows=stop_rows-start_rows+1,
                                         index_col=False,
                                         engine='python')
                    else:
                        df=pd.read_table(f,sep=sep,usecols=cols,
                                         skiprows=list(range(1,start_rows+1)),
                                         nrows=stop_rows-start_rows+1,
                                         index_col=False,
                                         engine='c')
                if filedir.endswith(('.xls','.xlsx')):
                    df=pd.read_excel(f,usecols=cols,
                                     skiprows=list(range(1,start_rows+1)),
                                     nrows=stop_rows-start_rows+1,
                                     index_col=False)
            else:
                if filedir.endswith(('.txt','.csv')):
                    if sep=='all':
                        df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,index_col=False,engine='python')
                    else:
                        df=pd.read_table(f,sep=sep,usecols=cols,index_col=False,engine='c')
                if filedir.endswith(('.xls','.xlsx')):
                    df=pd.read_excel(f,usecols=cols,index_col=False)
                    
#            定义参数顺序
            df = df[cols]
            return df

#rowscols_input：在rows_input基础上增加按列读取文件功能
    def rowscols_input(self,filedir="",sep="",cols=[],skiprows=None):
        if filedir=="":
            filedir=self.filedir
        if sep=="":
            sep=self.sep
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    df=pd.read_table(f,sep='\s+|\t|,|;',usecols=cols,skiprows=skiprows,engine='python')
                else:
                    df=pd.read_table(f,sep='\s+',usecols=cols,skiprows=skiprows,engine='c')
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,header=None,usecols=cols,skiprows=skiprows)
        return df

class GPS_DataFile(DataFile):
    def __init__(self,filedir='',sep='\s+',skiprows=15):
        super().__init__(filedir,sep)
        self.skiprows=skiprows
#        self.info_list=self.get_info(filedir)
        self.paras_in_file=self.get_paraslist(filedir)
#        self.time_range=self.get_timerange(filedir)  #！可能造成IO过多，使得速度变慢
#        self.sample_frequency = self.get_sample_frequency(filedir)

    def header_input(self,filedir='',sep='',skiprows=None): 
        if filedir=='':
            filedir=self.filedir
        if sep=='':
            sep=self.sep
        if skiprows is None:
            skiprows=self.skiprows
#            注意excel文件读取必须为rb模式
        with open(filedir,'r') as f:
            if filedir.endswith(('.txt','.csv')):
                if sep=='all':
                    #Use str or object to preserve and not interpret dtype
                    df=pd.read_table(f,sep='\s+|\t|,|;',header=None,nrows=2,skiprows=skiprows,engine='python',dtype=object)
                    #or only input the columns index:nrows=0,remove header=None
                else:
                    df=pd.read_table(f,sep=sep,header=None,nrows=2,skiprows=skiprows,engine='c',dtype=object)
            if filedir.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f,header=None,nrows=1)
#                df=df.iloc[0,:]  #deprecated as pandas version updated 
        df=df.iloc[0,:]+df.iloc[1,:]
        return df       

    def cols_input(self,filedir='',cols=[],sep='\s+',start_time='',stop_time='',skiprows=None):  #without chunkinput now!!

        if filedir=='':
            filedir=self.filedir
        if sep=='':
            sep=self.sep
        if skiprows is None:
            skiprows=self.skiprows
#            注意若是excel文件读取需要rb模式
        if cols:
            s = time.time()
            num_cols = [cols.index(idx) for idx in cols]
            e = time.time()
            
        with open(filedir,'r') as f:
            if (start_time and stop_time):
#                count_between_time函数返回的是两个时间的差值
                start_rows = Time.count_between_time(self.time_range[0],
                                                             start_time, self.sample_frequency)
                stop_rows = Time.count_between_time(self.time_range[0],
                                                            stop_time, self.sample_frequency)
                if filedir.endswith(('.txt','.csv')):
                    if sep=='all':
                        df=pd.read_table(f,sep='\s+|\t|,|;',usecols=num_cols,
#                                         range是左闭右开
                                         skiprows=skiprows+start_rows+3,
                                         nrows=stop_rows-start_rows+1,
                                         index_col=False,
                                         engine='python')
                    else:
                        df=pd.read_table(f,sep=sep,usecols=num_cols,
                                         skiprows=skiprows+start_rows+3,
                                         nrows=stop_rows-start_rows+1,
                                         index_col=False,
                                         engine='c')
                if filedir.endswith(('.xls','.xlsx')):
                    df=pd.read_excel(f,usecols=num_cols,
                                     skiprows=skiprows+start_rows+3,
                                     nrows=stop_rows-start_rows+1,
                                     index_col=False)
            else:
                if filedir.endswith(('.txt','.csv')):
                    if sep=='all':
                        df=pd.read_table(f,sep='\s+|\t|,|;',usecols=num_cols,skiprows=skiprows+2,index_col=False,engine='python')
                    else:
                        df=pd.read_table(f,sep=sep,usecols=num_cols,skiprows=skiprows+2,index_col=False,engine='c')
                if filedir.endswith(('.xls','.xlsx')):
                    df=pd.read_excel(f,usecols=cols,skiprows=skiprows+2,index_col=False)
            df.columns = cols
#            定义参数顺序
            df = df[cols]
            return df

    def get_paraslist(self,filedir=''):
        para_name = self.header_input(filedir,sep='\s+')
        para_list = para_name.values.tolist()
        return para_list
    
    def get_info(self,filedir=''):
        if filedir:
            lpos=filedir.rindex('\\')
            rpos=filedir.rindex('.')
            info_name=filedir[lpos+1:rpos]
            info_list=info_name.split('-')
        return info_list
    
#DataFile 的统一接口    
class DataFile_Factory(object):
    
    def __new__(cls, filedir='', sep='\s+', filetype = 'normal datafile'):
        if filetype == 'normal datafile':
            instance = Normal_DataFile(filedir, sep)
        elif filetype == 'GPS datafile':
            instance = GPS_DataFile(filedir, sep)
#        if filedir.endswith(('.txt','.csv')):
#            instance = Normal_DataFile(filedir, sep)
#        elif filedir.endswith(('.xls','.xlsx')):
#            instance = Excel_DataFile(filedir, sep)
        return instance
    
    
if __name__ == '__main__':
    filedir = r'D:\flightdata\gps data\970_-20130509-1-gps.txt'
#    DF=DataFile_Factory(filedir)
#    ss=Normal_DataFile(filedir)
    gpsdata = GPS_DataFile(filedir)
    df=gpsdata.header_input(filedir)