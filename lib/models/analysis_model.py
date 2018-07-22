# -*- coding: utf-8 -*-
import time
import re
import pandas as pd
from models.datafile_model import Normal_DataFile
#from datafile_model import Normal_DataFile
class DataAnalysis(object):
    def __init__(self):
        pass
    def condition_sift(self,file_list=[], condition="",search_para=[]):
        dict_result={}
        for filedir in file_list:
            df_result=[]
            file_search=Normal_DataFile(filedir)
            para_list=[item for item in search_para if item in file_search.paras_in_file]
            if not para_list:
                df_result
            para_list.insert(0,file_search.paras_in_file[0])
            df_sift=file_search.cols_input(filedir,para_list)
#           df_result=df_sift[eval("df_sift."+condition)]
            try:
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
                dict_result[filedir]=df_result
            except:
                return None
#            dict_result[filedir]=df_result
        return dict_result

#----------------原使用的函数-------------------
#solution1: 任何语法不正确，搜索参数不在文件中（只要有一个参数不在文件中）都会使得字典值为None
#           而参数搜索条件结果为空时，字典值为Empty DataFrame。
#           不适用于 参数1 | 参数2条件 ，且只有其中部分参数存在文件中的情况
#返回值为字典：key为文件路径filedir
#             vaule为元组(list_result,list_forskip)，list_result为符合条件的索引值列表；
#             list_forskip为用于在文件读入时跳过的行号以获得符合条件索引内容

    def condition_sift_old(self,file_list=[], condition="",search_para=[]):
        dict_result={}
#        cond_list=re.split(r"&|\|",condition)
#        print(cond_list)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para
                file_search=Normal_DataFile(filedir)                
                para_list.insert(0,file_search.paras_in_file[0])
                df_sift=file_search.cols_input(filedir,para_list)
                index_all=df_sift.index.tolist() #all index list
#                df_result=df_sift[eval("df_sift."+condition)]
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
#                print(df_result)
                list_result=df_result.index.tolist() #result index list
            except:
                list_result=None
            list_forskip=[item+1 for item in index_all if item not in list_result]
            dict_result[filedir]=(list_result,list_forskip)
            return dict_result



#----------------现使用的函数-------------------
#solution1: 任何语法不正确，搜索参数不在文件中（只要有一个参数不在文件中）都会使得字典值为None
#           而参数搜索条件结果为空时，字典值为Empty DataFrame。
#           不适用于 参数1 | 参数2条件 ，且只有其中部分参数存在文件中的情况        
#返回值为元组：   (sift_session, list_forskip)
#                sift_session为分段的结果类列表session_list(参考class session_list)
#                list_forskip为用于导出整个筛选结果文件的列表(用于rowsinput或者rowscols_input)
                
    def condition_sift_1(self,file_list=[], condition="",search_para=[]):
#        dict_result={}
#        cond_list=re.split(r"&|\|",condition)
#        print(cond_list)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para
                file_search=Normal_DataFile(filedir)                
                para_list.insert(0,file_search.paras_in_file[0])
                df_sift=file_search.cols_input(filedir,para_list)
                index_all=df_sift.index.tolist() #all index list
#                df_result=df_sift[eval("df_sift."+condition)]
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
#                print(df_result)
                list_result=df_result.index.tolist() #result index list
            except:
                list_result=None
#            dict_result[filedir]=df_result
            session_list=[]
            list_forskip=[item+1 for item in index_all if item not in list_result]
            begin=list_forskip[0]-1
            for item in list_forskip:
                item=item-1
                end=item
                if end-begin>1:
                    df_session=df_result.loc[begin+1:end-1]
                    index_session=df_session.index.tolist()
                    indexsession_skip=list_forskip=[item+1 for item in index_all if item not in index_session]
                    
                    session=sift_session(filedir,df_session,indexsession_skip)
                    session_list.append(session)
                begin=end
            if begin!=list_forskip[-1]:
                end=list_forskip[-1]
                if end-begin>1:
                    df_session=df_result.loc[begin+1:end-1]
                    index_session=df_session.index.tolist()
                    indexsession_skip=list_forskip=[item+1 for item in index_all if item not in index_session]
                    
                    session=sift_session(filedir,df_session,indexsession_skip)
                    session_list.append(session)
                    
                
#            dict_result[filedir]=(list_result,list_forskip,session_list)
        return (session_list,list_forskip)
    
    def condition_sift_test(self,file_list=[], condition="",search_para=[]):
        dict_result={}
#        cond_list=re.split(r"&|\|",condition)
#        print(cond_list)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para
                file_search=Normal_DataFile(filedir)                
                para_list.insert(0,file_search.paras_in_file[0])
                df_sift=file_search.cols_input(filedir,para_list)
                index_all=df_sift.index.tolist() #all index list
#                df_result=df_sift[eval("df_sift."+condition)]
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
#                print(df_result)
                list_result=df_result.index.tolist() #result index list
            except:
                list_result=None
#            dict_result[filedir]=df_result
            session_list=[]
            list_forskip=[item+1 for item in index_all if item not in list_result]
            begin=list_forskip[0]-1
            for item in list_forskip:
                item=item-1
                end=item
                if end-begin>1:
                    df_session=df_result.loc[begin+1:end-1]
                    index_session=df_session.index.tolist()
                    indexsession_skip=list_forskip=[item+1 for item in index_all if item not in index_session]
                    begin_time=df_session.iat[0,0]
                    end_time=df_session.iat[-1,0]
                    begin_datetime=pd.to_datetime(begin_time,format='%H:%M:%S:%f')
                    end_datetime=pd.to_datetime(end_time,format='%H:%M:%S:%f')
                    period_time=str(end_datetime-begin_datetime)
                    
                    session_result=(begin_time,end_time,period_time,indexsession_skip)
#                    session=sift_session(filedir,df_session,indexsession_skip)
                    session_list.append(session_result)
                begin=end
            if begin!=list_forskip[-1]:
                end=list_forskip[-1]
                if end-begin>1:
                    df_session=df_result.loc[begin+1:end-1]
                    index_session=df_session.index.tolist()
                    indexsession_skip=list_forskip=[item+1 for item in index_all if item not in index_session]
                    begin_time=df_session.iat[0,0]
                    end_time=df_session.iat[-1,0]
                    begin_datetime=pd.to_datetime(self.begin_time,format='%H:%M:%S:%f')
                    end_datetime=pd.to_datetime(self.end_time,format='%H:%M:%S:%f')
                    period_time=str(end_datetime-begin_datetime)
                    
                    session_result=(begin_time,end_time,period_time,indexsession_skip)
#                    session=sift_session(filedir,df_session,indexsession_skip)
                    session_list.append(session_result)
                    
                
            dict_result[filedir]=session_list
        return dict_result
    
    def condition_sift_2(self,file_list=[], condition="",search_para=[]):
        dict_result={}
        cond_list=re.split(r"&|\|",condition)
        for s in cond_list:
            para_parse=re.split(r">|<|=",s.strip())[0]
            if para_parse not in search_para:
                search_para.append(para_parse)
        condition.split("&")
        for filedir in file_list:
            df_result=[]
            file_search=Normal_DataFile(filedir)
            para_list=[item for item in search_para if item in file_search.paras_in_file]
            if not para_list:
                df_result
            para_list.insert(0,file_search.paras_in_file[0])
            df_sift=file_search.cols_input(filedir,para_list)
#           df_result=df_sift[eval("df_sift."+condition)]
            try:
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
                dict_result[filedir]=df_result
            except:
                return None
#            dict_result[filedir]=df_result
        return dict_result
    
    def downsample(self,df,f,closed='left',label='left'):
        timestr=str(1/f)+'S'
        time=df.columns.tolist()[0]
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
        df_new=df.set_index(pd.to_datetime(df[time],format='%H:%M:%S:%f'),drop=False)
        sample=df_new.resample(timestr,axis=0,closed=closed,label=label).first()
#        result=sample.reset_index(drop=True)
        result=sample
#        df_new.asfreq('1S',method='ffill')
        return result
    
    def upsample(self,df,f):
        timestr=str(1/f)+'S'
        time=df.columns.tolist()[0]
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
        df_new=df.set_index(pd.to_datetime(df[time],format='%H:%M:%S:%f'),drop=False)
        sample=df_new.resample(timestr,axis=0).ffill()
#        result=sample.reset_index(drop=True)
        result=sample
#        df_new.asfreq('1S',method='ffill')
        return result
 
    
def condition_sift(file_list=[], condition="",display_para=[]):
    dict_result={}
    for filedir in file_list:
        para_list=display_para
        file_search=Normal_DataFile(filedir)
        para_list.insert(0,file_search.paras_in_file[0])
        df_sift=file_search.cols_input(filedir,para_list)
#        df_result=df_sift[eval("df_sift."+condition)]
        index=condition.replace("(","(df_sift.")
        df_result=df_sift[eval(index)]
        dict_result[filedir]=df_result
    return dict_result

class sift_session(object):
    def __init__(self, filedir="", df_session=None, skiprows=[]):
        if filedir and df_session is not None:
            self.filedir=filedir
            self.df_session=df_session
            self.begin_time=df_session.iat[0,0]
            self.end_time=df_session.iat[-1,0]
            self.period_time=self.period()
            self.skiprows=skiprows
        
    def period(self):
        begin_datetime=pd.to_datetime(self.begin_time,format='%H:%M:%S:%f')
        end_datetime=pd.to_datetime(self.end_time,format='%H:%M:%S:%f')
        period_time=end_datetime-begin_datetime
        return str(period_time)
    
    def max_value(self, col=None):
        if isinstance(col,(str)):
            return self.df_session[col].max()
        elif isinstance(col,(int)):
            return self.df_session.iloc[:,col].max()
        else:
            return
        
    def min_value(self, col):
        if isinstance(col,(str)):
            return self.df_session[col].min()
        elif isinstance(col,(int)):
            return self.df_session.iloc[:,col].min()
        else:
            return
    
    def output(self, filedir="",mode='w'):
        file_session=Normal_DataFile(self.filedir)
        df_output=file_session.rows_input(self.filedir,sep="",skiprows=self.skiprows)
        if mode=='w':
            file_session.save_file(filedir,df_output,sep='\t')
        if mode=='a':
            file_session.append_file(filedir,df_output,sep='\t')
        
        
        
    

if __name__ == "__main__":
##    TEST1:
#    start = time.clock()
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    file_list=[filename]
#    da=DataAnalysis()
#    condition="(FADEC_LA_Corrected_N1_Speed>=25) & (FADEC_LA_Corrected_N1_Speed<30.01)"
##    condition="(FADEC_LA_Corrected_N1_Speed)"
#    result=da.condition_sift_old(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
#    elapsed = (time.clock() - start)
#    print("Time used:",elapsed)
#    #print(result)
#    
##    for key in result:
##        file_key=Normal_DataFile(key)
##        df=file_key.rowscols_input(key,cols=["FADEC_LA_Corrected_N1_Speed"],skiprows=result[key][1])
##        print(df)
#===============================================
##    TEST2:
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    filetest=Normal_DataFile(filename)
#    result=filetest.get_sample_frequency()
#    time_df=filetest.cols_input(filedir=filename,cols=[filetest.paras_in_file[0]])
#    print(time_df)
#    da=DataAnalysis()
##    result=da.downsample(time_df,4,closed='right')
#    result=da.upsample(time_df,32)
#==================================================
#    TEST3:
    start = time.clock()
    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    file_list=[filename]
    da=DataAnalysis()
    condition="(FADEC_LA_Corrected_N1_Speed>=25) & (FADEC_LA_Corrected_N1_Speed<30.01)"
#    condition="(FADEC_LA_Corrected_N1_Speed)"
    result=da.condition_sift_1(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)
    #print(result)
#===================================================
##    TEST4:
#    start = time.clock()
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    file_list=[filename]
#    da=DataAnalysis()
#    condition="(FADEC_LA_Corrected_N1_Speed>=25) & (FADEC_LA_Corrected_N1_Speed<30.01)"
##    condition="(FADEC_LA_Corrected_N1_Speed)"
#    result=da.condition_sift_test(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
#    elapsed = (time.clock() - start)
#    print("Time used:",elapsed)
#    #print(result)
#    
##    for key in result:
##        file_key=Normal_DataFile(key)
##        df=file_key.rowscols_input(key,cols=["FADEC_LA_Corrected_N1_Speed"],skiprows=result[key][1])
##        print(df)
#    
    