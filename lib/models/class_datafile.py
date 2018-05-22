# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 20:30:39 2018
class_datafile.py
Pattern datafile
@author: Yan Hua
"""
import pandas as pd
import time
time1=time.time()
#——————class DataFile————————
#说明：通用文件类，是所有其它文件类的基类
#功能：数据文件的导入导出功能
#properties：
#filename: 输入输出的文件名
#sep: 定义文件的分隔符，sep='\s+' '\t' ',' ';' 'all', 其中'all'为匹配任意分隔符
#functions:
#all_input(self,filename="",sep=""):一次直接读入整个文件，返回dataframe
#chunkAll_input(self,filename="",sep="",chunksize=50000)：分段读入整个文件，返回dataframe
#chunk_input(self,filename="",sep="",chunksize=50000)：分段读入文件，返回generator可迭代访问每段读入的dataframe
#save_file(self,filename,df,sep='\t')：dataframe数据保存为文本文件
#df_tolist(self,df)：dataframe转为列表



class DataFile(object):
    def __init__(self,filename="",sep="\s+"):
        self.filename=filename
        self.sep=sep
       
#all_input:一次导入整个数据文件（文件过大时会卡死），如不指定filename，sep会使用类属性        
    def all_input(self,filename="",sep=""):
        if filename=="":
            filename=self.filename
        if sep=="":
            sep=self.sep
        if filename.endswith(('.txt','.csv')):
            with open(filename,'rb') as f:
                if sep=='all':
                    df=pd.read_table(f,sep='\s+|\t|,|;',engine='python')
                else:
                    df=pd.read_table(f,sep=sep,engine='c')
        if filename.endswith(('.xls','.xlsx')):
            with open(filename,'rb') as f:
                df=pd.read_excel(f)
        return df

#chunkAll_input: 分段导入整个数据文件，chunksize指定每次读入的行数,返回完整的dataframe
    def chunkAll_input(self,filename="",sep="",chunksize=50000):
        if filename=="":
            filename=self.filename
        if sep=="":
            sep=self.sep
        loop = True
        #chunksize = 50000
        chunks = []
        with open(filename,'rb') as f:
            if filename.endswith(('.txt','.csv')):
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
            if filename.endswith(('.xls','.xlsx')):
                df=pd.read_excel(f)
        return df
    
#chunk_input: 分段导入数据文件，chunksize指定每次读入的行数，返回每一段读取的chunk
        #使用Yield使函数返回generator，可通过迭代获取yield指定的chunk，chunk为dataframe类型
    def chunk_input(self,filename="",sep="",chunksize=50000):
        if filename=="":
            filename=self.filename
        if sep=="":
            sep=self.sep
        loop=True
        with open(filename,'rb') as f:
            if filename.endswith(('.txt','.csv')):
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
            if filename.endswith(('.xls','.xlsx')):
                Nskip=0
                while loop:
                        chunk=pd.read_excel(f,header=None,skiprows=Nskip,nrows=chunksize)
                        if chunk.empty:
                            break
                        Nskip+=chunksize
                        yield chunk
                    
#save_file: 保存数据到文件，保存的数据格式为df:pandas dataframe或series    
    def save_file(self,filename,df,sep='\t'):
        df.to_csv(filename,sep,index=False,encoding="utf-8")

#DftoList:  将dataframe类型数据转换为二维列表[[],[],...]        
    def df_tolist(self,df):
        return df.values.tolist()
    
    def config(self):
        pass

#——————class normal_DataFile————————
#说明：一般试飞数据文件类，继承自DtaFile类
#功能：一般试飞数据文件的导入导出和配置功能
#properties：
#父类属性
#info_list: 数据文件信息列表

#functions:
#父类函数 
#get_info(self,filename=""):获取数据文件名信息，返回信息列表
#header_input(self,filename="",sep="")：读取数据文件第一行（参数名）
#cols_input(self,filename="",cols=[],sep="\s+")：按列读取数据文件，cols指定参数名列表，按cols指定的参数名列读取数据
#save_file(self,filename,df,sep='\t')：dataframe数据保存为文本文件
#df_tolist(self,df)：dataframe转为列表

class normal_DataFile(DataFile):
    def __init__(self,filename="",sep="\s+"):
        super(normal_DataFile,self).__init__(filename,sep)
        self.info_list=self.get_info(filename)
        
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
    
    def config(self):
        pass


if __name__ == "__main__":
    #filename=u"D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    #filename=u"D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664003-16.txt"
    filename=u"C:/Users/admin/Desktop/5008问题汇总.xlsx"
    iofile=normal_DataFile(filename)
    reader=iofile.chunk_input(chunksize=50)
    for chunk in reader:
        print(chunk)
    filename2=u"D:/flightdata/FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    para_name=iofile.header_input(filename2)
    para_list=para_name.iloc[:,1:10].values.tolist()[0]
    iofile.filename=filename2
    df=iofile.cols_input(cols=para_list)
    #df=all_input(filename)
    #df=header_input(filename,sep='all')
   # df=cols_input(filename,["time","HF_FSECU_1_L354_HLS_OMS_Status_Flap_Inoperative","FCM3_Voted_True_Airspeed"])
    #df=cols_input(filename,[u"日期"])
    #iofile.save_file(u"C:/Users/admin/Desktop/exp.txt",df)
    time2=time.time()
    print(time2-time1)        
    
   