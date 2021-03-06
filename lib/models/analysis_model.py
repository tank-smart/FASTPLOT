# -*- coding: utf-8 -*-
#import time      #用于时间测试

#=======================================
#重要修改：DataAnalysis增加init(time_format)
#===========================================
import re
import pandas as pd
from models.datafile_model import Normal_DataFile, DataFile_Factory
from models.data_model import DataFactory
import models.time_model as Time

class DataAnalysis(object):
    def __init__(self, time_format = '%H:%M:%S:%f'):
        self.time_format = time_format
    
#================数据筛选================================
    def condition_sift_preserved(self,file_list=[], condition="",search_para=[]):
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

#----------------现使用的函数-------------------
#solution1: 
#搜索函数：condition_sift(self,file_list=[], condition="",search_para=[]):
#           速度很快，任何语法不正确，搜索参数不在文件中（只要有一个参数不在文件中）都会使得字典值为None
#           而参数搜索条件结果为空时，字典值为Empty DataFrame。
#           不适用于 参数1 | 参数2条件 ，且只有其中部分参数存在文件中的情况
#返回值为字典：key为文件路径filedir
#             vaule为筛选得到的dataframe
        
#导出搜索结果文件函数：sift_output(self, filedir="", fileout="", mode='w', index_list=None, skip_list=None):
#filedir为搜索文件路径；fileout为导出文件路径；mode为导出模式，'w'为普通写文件模式，'a'为追加写文件模式；
#index_list为选择索引方式导出数据文件；skip_list为选择跳过索引方式导出数据文件；index_list和skip_list只能使用其中之一

    def condition_sift(self,file_list=[], condition="",search_para=[]):
        dict_result={}
#        cond_list=re.split(r"&|\|",condition)
#        print(cond_list)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para.copy()
                file_search=Normal_DataFile(filedir)                
                para_list.insert(0,file_search.paras_in_file[0])
                df_sift=file_search.cols_input(filedir,para_list)
#                index_all=df_sift.index.tolist() #all index list
#                df_result=df_sift[eval("df_sift."+condition)]
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
                skip_list=(df_sift.index.drop(df_result.index)+1).tolist()#quick select skip index

#                print(df_result)
#                list_result=df_result.index.tolist() #result index list
            except:
                 return None
#            list_forskip=[item+1 for item in index_all if item not in list_result]
#            dict_result[filedir]=(list_result,list_forskip)
            dict_result[filedir]=(df_result,skip_list)
        return dict_result
    
    def condition_sift_wxl(self, file_list=[], dict_filetype={}, condition="",search_para=[]):
        dict_result={}
        flag=0
        for para in search_para:
            if para in condition:
                flag=1
                break
        if flag==0:
            return None
            
            
#        cond_list=re.split(r"&|\|",condition)
#        print(cond_list)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para.copy()
#                file_search=Normal_DataFile(filedir)
                file_search = DataFile_Factory(filedir, **dict_filetype[filedir])
                input_list=[]
                for para in para_list:
                    if para in file_search.paras_in_file:
                        input_list.append(para)
                if input_list:
                    input_list.insert(0,file_search.paras_in_file[0])
                    df_sift=file_search.cols_input(filedir,input_list)
    #                index_all=df_sift.index.tolist() #all index list
    #                df_result=df_sift[eval("df_sift."+condition)]
                    index=condition.replace("(","(df_sift.")
                    df_result=df_sift[eval(index)]
    #                skip_list=(df_sift.index.drop(df_result.index)+1).tolist()#quick select skip index
                    re_list = df_result.index.tolist()
    #                print(df_result)
    #                list_result=df_result.index.tolist() #result index list
                else:
                    re_list = []
            except:
                 return None
#            list_forskip=[item+1 for item in index_all if item not in list_result]
#            dict_result[filedir]=(list_result,list_forskip)
#            dict_result[filedir]=(df_result,skip_list)
            if re_list!=[]:
                
                inter_list = []
                begin = forward_index = re_list[0]
                for i, index in enumerate(re_list):
                    if (index - forward_index > 1): 
                        inter_list.append((begin,forward_index))
                        begin = index
                    if (i == len(re_list) - 1):
                        inter_list.append((begin,index))
                    forward_index = index
                time_intervals = []
                for t_inter in inter_list:
                    stime_index, etime_index = t_inter
                    begin_datetime=pd.to_datetime(df_sift.iloc[stime_index, 0],format=file_search.time_format)
                    end_datetime=pd.to_datetime(df_sift.iloc[etime_index, 0],format=file_search.time_format)
                    period_time=end_datetime-begin_datetime
                    time_intervals.append((df_sift.iat[stime_index, 0],
                                           df_sift.iat[etime_index, 0],
                                           str(period_time)))
                dict_result[filedir] = time_intervals
            else:
                dict_result[filedir] = []
        return dict_result
        
    def sift_output(self, filedir="", fileout="", mode='w', index_list=None, skip_list=None):
        
        if index_list!=None:
            file_session=Normal_DataFile(filedir)
            df_all=file_session.all_input(filedir)
            df_output=df_all.loc[index_list]
            if mode=='w':
                file_session.save_file(fileout,df_output,sep='\t')
            if mode=='a':
                file_session.append_file(fileout,df_output,sep='\t')
            
        if skip_list!=None:
            file_session=Normal_DataFile(filedir)
            df_output=file_session.rows_input(filedir,skiprows=skip_list)
            if mode=='w':
                file_session.save_file(fileout,df_output,sep='\t')
            if mode=='a':
                file_session.append_file(fileout,df_output,sep='\t')



#----------------可选用的函数-------------------
#solution1: 任何语法不正确，搜索参数不在文件中（只要有一个参数不在文件中）都会使得字典值为None
#           而参数搜索条件结果为空时，字典值为Empty DataFrame。
#           不适用于 参数1 | 参数2条件 ，且只有其中部分参数存在文件中的情况        
#返回值为元组：   (sift_session, list_forskip)
#                sift_session为分段的结果类列表session_list(参考class session_list)
#                list_forskip为用于导出整个筛选结果文件的列表(用于rowsinput或者rowscols_input)
                
    def condition_sift_class(self,file_list=[], condition="",search_para=[]):
#        dict_result={}
#        cond_list=re.split(r"&|\|",condition)
#        print(cond_list)
#        for s in cond_list:
#            para_parse=re.split(r">|<|=",s.strip())[0]
#            if para_parse not in search_para:
#                search_para.append(para_parse)
        for filedir in file_list:
            try:
                para_list=search_para.copy()
                file_search=Normal_DataFile(filedir)                
                para_list.insert(0,file_search.paras_in_file[0])
                df_sift=file_search.cols_input(filedir,para_list)
                index_all=df_sift.index.tolist() #all index list
#                df_result=df_sift[eval("df_sift."+condition)]
                index=condition.replace("(","(df_sift.")
                df_result=df_sift[eval(index)]
#                print(df_result)
            except:
                return None
#            dict_result[filedir]=df_result
    
            session_list=[]
            #list_forskip=[item+1 for item in index_all if item not in list_result]
            skip_index=df_sift.index.drop(df_result.index)+1
            list_forskip=skip_index.tolist()
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
            return (session_list,list_forskip)
        
                
#            dict_result[filedir]=(list_result,list_forskip,session_list)
#        return (session_list,list_forskip)

#----------------可选用的函数-------------------
#solution1: 任何语法不正确，搜索参数不在文件中（只要有一个参数不在文件中）都会使得字典值为None
#           而参数搜索条件结果为空时，字典值为Empty DataFrame。
#           不适用于 参数1 | 参数2条件 ，且只有其中部分参数存在文件中的情况        
#返回值为字典：key为文件路径filedir
#             vaule为元组(begin_time,end_time,period_time,indexsession_skip)
    def condition_sift_tuple(self,file_list=[], condition="",search_para=[]):
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
#            start = time.clock()
            list_forskip=[item+1 for item in index_all if item not in list_result]
#            elapsed = (time.clock() - start)
#            print(elapsed)
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
#================================================================
#========================数据升降频===============================
#升降频方法
#最初版本    
    def downsample_old(self,df,f,closed='left',label='left'):
        timestr=str(1/f)+'S'
        timecol=df.columns.tolist()[0]
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
        df_new=df.set_index(pd.to_datetime(df[timecol],format='%H:%M:%S:%f'),drop=False)
        sample=df_new.resample(timestr,axis=0,closed=closed,label=label).first()
#        result=sample.reset_index(drop=True)
        result=sample
#        df_new.asfreq('1S',method='ffill')
        return result


#现使用的降频函数，使用periodindex表示时间。将resample表示为ms后，这种方法似乎降频完美    
    def downsample_nochange(self,df,f,closed='left',label='left'):
        timestr=str(round(1000/f,3))+'ms'
        timecol=df.columns.tolist()[0]
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
        df_new=df.set_index(pd.to_datetime(df[timecol],format=self.time_format),drop=False)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
#        print(df_used)
        sample=df_used.resample(timestr,axis=0,closed=closed,label=label,convention='s').ffill()
#        result=sample.reset_index(drop=True) #可以恢复原索引
        result=sample
#        new_start=result.index[0]
#        delta=old_start-new_start
#        result.index=result.index+delta
#        df_new.asfreq('1S',method='ffill')
        return result
    
    def downsample(self,df,f,closed='left',label='left'):
        timestr=str(round(1000/f,3))+'ms'
        col = df.columns
        timecol=df.columns.tolist()[0]
        df[timecol]=pd.to_datetime(df[timecol],format=self.time_format)
        df_new=df.set_index(timecol,drop=True)
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
#        df_new=df.set_index(pd.to_datetime(df[timecol],format=self.time_format),drop=True)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
#        print(df_used)
        sample=df_used.resample(timestr,axis=0,closed=closed,label=label,convention='s').ffill()
        #可以恢复原索引
#        result.iloc[:,0] = result.iloc[:,0].apply(lambda x: x.strftime(self.time_format))
        sample.index=sample.index.to_timestamp().strftime(self.time_format)
        result=sample.reset_index()
        result.columns = col
#        result=sample.reset_index() 
#        print(result)
#        result=sample
#        new_start=result.index[0]
#        delta=old_start-new_start
#        result.index=result.index+delta
#        df_new.asfreq('1S',method='ffill')
        return result

    def downsample_stdout(self,df,f,closed='left',label='left'):
        timestr=str(round(1000/f,3))+'ms'
        timecol=df.columns.tolist()[0]
        df[timecol]=pd.to_datetime(df[timecol],format=self.time_format)
        df_new=df.set_index(timecol,drop=True)
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
#        df_new=df.set_index(pd.to_datetime(df[timecol],format=self.time_format),drop=True)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
#        print(df_used)
        sample=df_used.resample(timestr,axis=0,closed=closed,label=label,convention='s').ffill()
        #可以恢复原索引
#        result.iloc[:,0] = result.iloc[:,0].apply(lambda x: x.strftime(self.time_format))
        sample.index=sample.index.to_timestamp().strftime('%H:%M:%S.%f')
        result=sample.reset_index() 
        return result    
    
    def downsample_synchro(self,df,f,closed='left',label='left'):
        timestr=str(round(1000/f,3))+'ms'
        timecol=df.columns.tolist()[0]
        df_new=df.set_index(timecol,drop=True)
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
#        df_new=df.set_index(pd.to_datetime(df[timecol],format=self.time_format),drop=True)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
        sample=df_used.resample(timestr,axis=0,closed=closed,label=label,convention='s').ffill()
        #可以恢复原索引
#        result.iloc[:,0] = result.iloc[:,0].apply(lambda x: x.strftime(self.time_format))
#        sample.index=sample.index.to_timestamp().strftime('%H:%M:%S.%f')
        result=sample 
        return result    
    

#现使用的升频函数，较为完美的升频方法    
    def upsample_nochange(self,df,f):
        timestr=str(round(1000/f,3))+'ms'
        timecol=df.columns.tolist()[0]
        df[timecol]=pd.to_datetime(df[timecol],format=self.time_format)
        df_new=df.set_index(df[timecol],drop=False)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
        sample=df_used.resample(timestr,axis=0).interpolate(method='linear')
#        对索引时间值会改变的数据，如我们现使用的数据，现resample再通过线性插值填充NAN值会更加合理，如下两行
#        sample=df_used.resample(timestr,axis=0).first()
#        sample=sample.interpolate()
        result=sample.round(8)
#        pandas has bug in converting periodindex to string when date_format is '%H:%M:%S:%f'
        result[timecol]=result.index.to_timestamp().strftime(self.time_format)
#        result=result.reset_index(drop=True)
        return result
    
    def upsample(self,df,f):
        timestr=str(round(1000/f,3))+'ms'
        col =df.columns
        timecol=df.columns.tolist()[0]
        df[timecol]=pd.to_datetime(df[timecol],format=self.time_format)
        df_new=df.set_index(timecol,drop=True)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
        sample=df_used.resample(timestr,axis=0).interpolate(method='linear')
#        对索引时间值会改变的数据，如我们现使用的数据，现resample再通过线性插值填充NAN值会更加合理，如下两行
#        sample=df_used.resample(timestr,axis=0).first()
#        sample=sample.interpolate()
        result=sample.round(8)
#        pandas has bug in converting periodindex to string when date_format is '%H:%M:%S:%f'
        result.index=result.index.to_timestamp().strftime(self.time_format)
        result=result.reset_index()
        result.columns = col
        return result
    
    def upsample_synchro(self,df,f):
        timestr=str(round(1000/f,3))+'ms'
        timecol=df.columns.tolist()[0]
#        df[timecol]=pd.to_datetime(df[timecol],format=self.time_format)
        df_new=df.set_index(df[timecol],drop=True)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[0],end=df_new.index[-1],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
        sample=df_used.resample(timestr,axis=0).interpolate(method='linear')
#        对索引时间值会改变的数据，如我们现使用的数据，现resample再通过线性插值填充NAN值会更加合理，如下两行
#        sample=df_used.resample(timestr,axis=0).first()
#        sample=sample.interpolate()
        result=sample.round(8)
#        pandas has bug in converting periodindex to string when date_format is '%H:%M:%S:%f'
#        result[timecol]=result.index.to_timestamp().strftime(self.time_format)
#        result=result.reset_index()
        return result
#=======================================================================
#=========================数据时间同步===================================
#时间同步方法
        
    def init_time(self, df):
        time_format = Time.time_format(df.iat[0,0])
        timeseries = pd.to_datetime(df.iloc[:,0],format=time_format)
        index_start = Time.str_to_datetime(df.iat[0,0])
        dtime = index_start - Time.str_to_datetime('00:00:00:000')
        timeseries = timeseries - dtime
        df.iloc[:,0] = timeseries.apply(lambda x: x.strftime(time_format))
        return df
    
    def init_time_synchro(self, df):
        time_format = Time.time_format(df.iat[0,0])
        timeseries = pd.to_datetime(df.iloc[:,0],format=time_format)
        index_start = Time.str_to_datetime(df.iat[0,0])
        dtime = index_start - Time.str_to_datetime('00:00:00:000')
        timeseries = timeseries - dtime
        df.iloc[:,0] = timeseries
        return df
    
    def inter_lenth(self, df_list):
        return min([len(df) for df in df_list])
    
    def synchro_nonconcat(self, df_list, lenth):
        df_newlist = []
        for df in df_list:
            df = df.iloc[0:lenth-1,:]
            df_newlist.append(df)
        return df_newlist
        
    def synchro_concat(self, df_list, lenth):
        df_newlist = []
        for df in df_list:
            df = df.iloc[0:lenth-1,:]
            df = df.set_index(df.columns[0])
#            print(df)
            df_newlist.append(df)
        result = pd.concat(df_newlist, axis=1, join='outer', join_axes=[df_newlist[0].index])
        result = result.reset_index()
        return result

    def synchro_inter(self,df_list,f,closed='left',label='left'):
        timestr=str(round(1000/f,3))+'ms'
        timecol=df.columns.tolist()[0]
#        df[time]=pd.to_datetime(df[time],format='%H:%M:%S:%f')
        df_new=df.set_index(pd.to_datetime(df[timecol],format='%H:%M:%S:%f'),drop=False)
        new_index=pd.PeriodIndex(df_new.index,start=df_new.index[1],end=df_new.index[-2],freq='us')
#        print(new_index)
        df_used=df_new.set_index(new_index)
        return df_used
    
def whole_synchro(df_list, f, output = 'list'):
    df_result = []
    lenth = inter_lenth(df_list)
    for df in df_list:
        datafac = DataFactory(df)
        ana = DataAnalysis(datafac.time_format)
        datafac.data = ana.init_time_synchro(datafac.data)
        if datafac.sample_frequency>f:
            datafac.data = ana.downsample_synchro(datafac.data, f)
        elif datafac.sample_frequency<f:
            datafac.data = ana.upsample_synchro(datafac.data, f)
        else:
            datafac.data = ana.downsample_synchro(datafac.data, f)
#            datafac.data = datafac.data
        datafac.data = datafac.data.iloc[0:lenth,:]
        df_result.append(datafac.data)
    if output == 'list':
        return df_result
    elif output =='dataframe':
        result = pd.concat(df_result, axis=1, join='outer', join_axes=[df_result[0].index])
         
        result.index = result.index.to_timestamp().strftime(datafac.time_format)
        result_df = result.reset_index()
        return result_df
        
        
            
def inter_lenth(df_list):
    return min([len(df) for df in df_list])
    
#================================================================
        
#====================class sift_session==========================
#用于筛选结果展示的类
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
#=============================================================        
        
        
    

if __name__ == "__main__":
##    TEST1:
#    start = time.clock()
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    file_list=[filename]
#    da=DataAnalysis()
#    condition="(FADEC_LA_Corrected_N1_Speed>=0) & (FADEC_LA_Corrected_N1_Speed<20.01)"
##    condition="(FADEC_LA_Corrected_N1_Speed)"
#    result=da.condition_sift(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
#    for filedir in result:
#        index_list=result[filedir][0].index.tolist()
#        skip_list=result[filedir][1]
##        da.sift_output(filedir, r"D:\index.txt",index_list=index_list)
#        da.sift_output(filedir, r"D:\skipindex.txt",skip_list=skip_list)
#        
#    elapsed = (time.clock() - start)
#    print("Time used:",elapsed)
#    #print(result)
#    
##    for key in result:
##        file_key=Normal_DataFile(key)
##        df=file_key.rowscols_input(key,cols=["FADEC_LA_Corrected_N1_Speed"],skiprows=result[key][1])
##        print(df)
#===============================================
##    TEST2(up/down resample):
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    filetest=Normal_DataFile(filename)
#    result=filetest.get_sample_frequency()
#    time_df=filetest.cols_input(filedir=filename,cols=filetest.paras_in_file[0:10])
##    print(time_df)
#    da=DataAnalysis()
##    result=da.downsample(time_df,4,closed='left')
#    result=da.upsample(time_df,32)
##    result=result.round(8)
#    fileout=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-32.txt"
#    filetest.save_file(fileout,result)
#==================================================
##    TEST3:
#    start = time.clock()
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    file_list=[filename]
#    da=DataAnalysis()
#    condition="(FADEC_LA_Corrected_N1_Speed>=25) & (FADEC_LA_Corrected_N1_Speed<30.01)"
##    condition="(FADEC_LA_Corrected_N1_Speed)"
#    result=da.condition_sift_class(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
#    elapsed = (time.clock() - start)
#    print("Time used:",elapsed)
#    #print(result)
#===================================================
##    TEST4:
#    start = time.clock()
#    filename=u"D:\\flightdata\\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
#    file_list=[filename]
#    da=DataAnalysis()
#    condition="(FADEC_LA_Corrected_N1_Speed>=25) & (FADEC_LA_Corrected_N1_Speed<30.01)"
##    condition="(FADEC_LA_Corrected_N1_Speed)"
#    result=da.condition_sift_tuple(file_list,condition,["FADEC_LA_Corrected_N1_Speed"])
#    elapsed = (time.clock() - start)
#    print("Time used:",elapsed)
#    #print(result)
#    
##    for key in result:
##        file_key=Normal_DataFile(key)
##        df=file_key.rowscols_input(key,cols=["FADEC_LA_Corrected_N1_Speed"],skiprows=result[key][1])
##        print(df)
#======================================================
#    TEST5(synchro):
    filename1=r"C:\ftcc\FlightData\170323_664\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt"
    filename2=r"C:\ftcc\FlightData\gps data\970_-20130509-1-gps.txt"
    filetest1=DataFile_Factory(filename1,filetype = 'normal datafile')
    filetest2=DataFile_Factory(filename2,filetype = 'GPS datafile')
#    fre=filetest.get_sample_frequency()
    df1 = filetest1.cols_input(filedir=filename1,cols=filetest1.paras_in_file[0:2])
    df2 = filetest2.cols_input(filedir=filename2,cols=filetest2.paras_in_file[0:2])
#    da1=DataAnalysis(filetest1.time_format)
#    da2=DataAnalysis(filetest2.time_format)
#    rdf1 = da1.init_time(df1)
#    df2_m = da2.init_time(df2)
#    rdf2 = da2.downsample_stdout(df2_m, 16)
#    rdf1 = da1.downsample_stdout(rdf1, 16)
#    lenth = da1.inter_lenth([rdf1,rdf2])
#    result = da1.synchro_concat([rdf1,rdf2], lenth)
#    result=da.downsample(time_df,4,closed='left') 
    result = whole_synchro([df1,df2], 16 , output='dataframe')
    
    