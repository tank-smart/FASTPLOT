# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 简述：绘图窗口类
#
# =======使用说明
# 
#
# =======日志
# 
# =============================================================================
import sys
#测试用
sys.path.append('E:\FASTPLOT\lib')

import pandas as pd
# =============================================================================
# Package views imports
# =============================================================================
from models.datafile_model import Normal_DataFile, DataFile_Factory
import models.time_model as Time_Model

class DataFactory(object):
    
#    通过文件路径+参数列表或者DataFrame初始化
    def __init__(self, data_source = None, sel_para = [], filetype = None):

# yanhua modified        
        self.filedir = None
        if type(data_source) == str and filetype is not None :
#            确定数据类型
            self.data_type = 'DataFile'
            self.filedir = data_source
#            file = Normal_DataFile(data_source)
            file = DataFile_Factory(data_source, filetype = filetype)
            if sel_para:
#                参数列表是包括时间参数的
                self.data_paralist = [file.paras_in_file[0]] + sel_para
            else:
                self.data_paralist = file.paras_in_file
            self.data = file.cols_input(data_source, self.data_paralist)
#            按指定顺序排列
            self.data = self.data[self.data_paralist]
#            确定起止时间
            self.time_range = file.time_range
#            确定采样频率
            self.sample_frequency = file.sample_frequency
            self.time_format = file.time_format
        elif type(data_source) == pd.DataFrame:
#            确定数据类型
            self.data_type = 'DataFrame'
#            确定数据
            if sel_para:
                pl = self.data.columns.values.tolist()
                sel_para.insert(pl[0])
                self.data = self.data[sel_para]
            else:
                self.data = data_source
#            确定数据中的参数列表
            self.data_paralist = self.data.columns.values.tolist()
#            确定起止时间
            stime = Time_Model.timestr_to_stdtimestr(data_source.iloc[0, 0])
            etime = Time_Model.timestr_to_stdtimestr(data_source.iloc[-1, 0])
            self.time_range = [stime, etime]
#            确定采样频率
            get_fre = False
            fre = 1
            first_time = self.data.iloc[0, 0]
            length_time = len(self.data)
            while (not get_fre) and fre <= length_time:
                next_time = self.data.iloc[fre, 0]
                count = Time_Model.count_between_time(first_time, next_time, 1)
                if count == 1:
                    get_fre = True
                else:
                    fre += 1
            if not get_fre:
                fre = 0
            self.sample_frequency = fre
            self.time_format = Time_Model.time_format(first_time)
#            使用时间作为索引的series数据
        elif type(data_source) == pd.Series:
#            确定数据类型
            self.data_type = 'Series'
#            确定数据
            
            self.data = data_source.reset_index()
#            确定数据中的参数列表
            self.data_paralist = self.data.columns.values.tolist()
#            确定起止时间
            stime = Time_Model.timestr_to_stdtimestr(data_source.iloc[0, 0])
            etime = Time_Model.timestr_to_stdtimestr(data_source.iloc[-1, 0])
            self.time_range = [stime, etime]
#            确定采样频率
            get_fre = False
            fre = 1
            first_time = self.data.iloc[0, 0]
            length_time = len(self.data)
            while (not get_fre) and fre <= length_time:
                next_time = self.data.iloc[fre, 0]
                count = Time_Model.count_between_time(first_time, next_time, 1)
                if count == 1:
                    get_fre = True
                else:
                    fre += 1
            if not get_fre:
                fre = 0
            self.sample_frequency = fre

#    time为datatime类型或字符串时间
#    返回一个元组（时间，参数值列表）
#    对于参数值列表，若paraname不为空，返回参数值；若为空，返回一个元组型的列表，第一个元素是时间
    def get_time_paravalue(self, time = None, paraname = None):
        
        if Time_Model.is_in_range(self.time_range[0], self.time_range[1], time):
            time_index = Time_Model.count_between_time(self.time_range[0],
                                                       time, 
                                                       self.sample_frequency)
            para_data = self.data.iloc[time_index, :]
            time_str = Time_Model.timestr_to_stdtimestr(para_data[0])
            if paraname:
                return (time_str, para_data[paraname])
            else:
                paravalue = []
                for paraname in self.data_paralist:
                    paravalue.append((paraname, para_data[paraname]))
                return (time_str, paravalue)
        else:
            return ('', None)
        
    def get_paralist(self):
        
        if len(self.data_paralist) > 1:
            return self.data_paralist[1:]
        else:
            return None
        
    def get_time_index(self):
        
        if len(self.data_paralist) > 1:
            return self.data_paralist[0]
        else:
            return None
        
    def get_sub_data(self, paralist, is_with_time = True):
        
        if is_with_time:
            paralist.insert(0, self.get_time_index())
        return self.data[paralist]
        
    def is_extended_by(self, data_factory):
        
        if (Time_Model.compare(data_factory.time_range[0], self.time_range[0]) == 0 and
            Time_Model.compare(data_factory.time_range[1], self.time_range[1]) == 0 and
            data_factory.sample_frequency == self.sample_frequency):
            return True
        else:
            return False
        
    def extend_data(self, data_factory):
        
        if self.is_extended_by(data_factory):
            extend_paras = []
            sr_df_paralist = data_factory.get_paralist()
            for pa in sr_df_paralist:
                if not(pa in self.data_paralist):
                    extend_paras.append(pa)
                    self.data_paralist.append(pa)
#            需要先判断参数是否重复
            self.data = pd.concat([self.data, data_factory.data[extend_paras]],
                                  axis = 1,join = 'outer', ignore_index = False)
        else:
            raise ValueError('DataFactory dimension inconsistent(FastPlot).')

#    判断两个DataFactory是否一致，通过判断数据是否在同一块内存上
    def is_equal(self, data_factory):
        
        if id(self.data) == id(data_factory.data):
            return True
        else:
            return False
        
#    返回的是实际时间段及其数据
    def get_trange_data(self, stime = None, etime = None, paralist = [], is_with_time = True):
        
        if stime and etime:
            bool_re = Time_Model.compare(stime, etime)
#            判断是否能判断，同时也能判断是否输入了正确的时间
            if bool_re:
                lim_stime = self.time_range[0]
                lim_etime = self.time_range[1]
                st = stime
                et = etime
#                如果开始时间小于结束时间就对调
                if bool_re == 1:
                    st = etime
                    et = stime
#                跟数据中时间段的求交集
                if Time_Model.compare(st, lim_stime) == -1:
                    st = lim_stime
                    if Time_Model.compare(et, lim_stime) == -1:
                        return (None, None)
                    else:
                        if Time_Model.compare(et, lim_etime) == 1:
                            et = lim_etime
                else:
                    if Time_Model.compare(st, lim_etime) == 1:
                        return (None, None)
                    else:
                        if Time_Model.compare(et, lim_etime) == 1:
                            et = lim_etime
#                因为是以采样点为起始时间，则得到的index是最靠近且小于终止时间的那个采样点的index
                stime_index = Time_Model.count_between_time(lim_stime,
                                                            st,
                                                            self.sample_frequency)
                etime_index = Time_Model.count_between_time(lim_stime,
                                                            et,
                                                            self.sample_frequency)
                print(lim_stime)
                print(et)
#                更新起始时间，保证只取在选择时间范围的数据
                getted_stime = self.data.iloc[stime_index, 0]
                if Time_Model.compare(getted_stime, st) == -1:
                    stime_index += 1
                std_stime = Time_Model.timestr_to_stdtimestr(self.data.iloc[stime_index, 0])
                std_etime = Time_Model.timestr_to_stdtimestr(self.data.iloc[etime_index, 0])
                if paralist:
                    if is_with_time:
                        paralist.insert(0, self.get_time_index())
    #                按下面的dataframe访问方式是左闭右开，所以右边要加1
                    return ((std_stime, std_etime), 
                            self.data[paralist][stime_index : (etime_index + 1)])
                else:
                    if is_with_time:
                        return ((std_stime, std_etime), 
                                self.data[stime_index : (etime_index + 1)])
                    else:
                        return ((std_stime, std_etime), 
                                self.data[self.get_paralist()][stime_index : (etime_index + 1)])
            else:
                return (None, None)
        else:
            return (None, None)
        
    def delete_col(self, index : str):
        
        if type(index) == str and index != '':
            para_list = self.get_paralist()
            if para_list and (index in para_list):
                self.data = self.data.drop(index, axis = 1)
                self.data_paralist = self.data.columns.values.tolist()

#---------yanhua加        
    def get_shape(self):
        return self.data.shape
    
#    def _add_(self, other):
#        if isinstance(other, self):
#            if self.is_extended_by(self, other):
#                data = self.data.iloc[:,1]+other.data.iloc[:,1]
#                time = self.data.iloc[:,0]
#                df = pd.Dataframe({'Time' : time, 'Result' : data})
#                result = DataFactory(df)
#                return result
#            elif self.data.shape == other.data.shape:
                
            
    
#---------yanhua          
        
if __name__ == '__main__':
    
    file_dir = r'D:\flightdata\FTPD-C919-10101-PD-170318-G-02-CAOWEN-664002-16.txt'
    file = Normal_DataFile(file_dir)
    
#    d = DataFactory(file_dir, ['FCM1_Voted_Mach'])
    
    df = file.cols_input(file_dir, [file.paras_in_file[0]])
    dd = DataFactory(df)
    print(dd.time_format)
    
#    print('Dt: %s' % d.data_type)
#    print(d.get_time_index())
#    print(d.time_range)
#    d.get_sub_data(['FCM1_Voted_Mach'])
#    print('Fre: %d' % d.sample_frequency)
#    print(d.get_time_paravalue('10:59'))
#    c = d.get_trange_data(None,None,[],False)
#    print(c.columns)
#    dd.extend_data(d)
#    print(dd.data_paralist)