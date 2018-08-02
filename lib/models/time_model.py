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
# =============================================================================
from datetime import datetime as Pytime

#必须先判断时间格式，才能调用
def str_to_intlist(time : str):
    
    result_time = None
    tran_format = ['%H:%M:%S:%f', '%H:%M:%S.%f', '%H', '%H:%M', '%H:%M:%S']
    for format_time in tran_format:
        try:
            result_time = Pytime.strptime(time, format_time)
#            匹配成功后跳出循环
            break
        except:
            pass
        finally:
            pass
    
    return [result_time.hour, result_time.minute, result_time.second, result_time.microsecond]

#必须先判断时间格式，才能调用
def timecount_between_strtimes(start_time : str, stop_time : str, fre : int):
    
    start = str_to_datetime(start_time)
    stop = str_to_datetime(stop_time)
    return int(((stop.hour - start.hour) * 3600 +
                (stop.minute - start.minute) * 60 +
                (stop.second - start.second) +
                (stop.microsecond - start.microsecond) / 1000000) * fre)

#必须先判断时间格式，才能调用
def timecount_between_datetimes(start_time : Pytime, stop_time : Pytime, fre : int):
    
    return int(((stop_time.hour - start_time.hour) * 3600 +
                 (stop_time.minute - start_time.minute) * 60 +
                 (stop_time.second - start_time.second) +
                 (stop_time.microsecond - start_time.microsecond) / 1000000) * fre)

#    比较两个时间的大小，time1大于time2返回1，等于返回0，小于返回-1
def compare(time1 : str, time2 : str):
    
    t1 = str_to_intlist(time1)
    t2 = str_to_intlist(time2)
    l = len(t1)
#    当前位前边的位都是相等的
    equal = True
    for i in range(l):
#        前边的位相等，当前位大于
        if t1[i] > t2[i] and equal:
            return 1
        if t1[i] < t2[i] and equal:
            return -1
    return 0

def is_in_range(start : str, stop : str, time : str):
    st1 = compare(start, time)
    st2 = compare(time, stop)
    if st1 != 1 and st2 != 1:
        return True
    else:
        return False
    
def is_std_format(time : str):
    
    tran_format = ['%H:%M:%S:%f', '%H:%M:%S.%f', '%H', '%H:%M', '%H:%M:%S']
    for format_time in tran_format:
        try:
            Pytime.strptime(time, format_time)
            return True
        except:
            pass
        finally:
            pass
    return False

def str_to_datetime(time : str):
    
    tran_format = ['%H:%M:%S:%f', '%H:%M:%S.%f', '%H', '%H:%M', '%H:%M:%S']
    for format_time in tran_format:
        try:
            return Pytime.strptime(time, format_time)
        except:
            pass
        finally:
            pass
    return None

def datetime_to_timestr(dt : Pytime):
    
    if dt:
        return dt.time().isoformat(timespec='milliseconds')
    else:
        return ''
    
def timestr_to_stdtimestr(time : str):
    
    return datetime_to_timestr(str_to_datetime(time))
    
if __name__ == '__main__':
#    print(is_in_range('6:13','12:13:47.291','6:14:47.291'))
#    print(is_std_format('12:13:47*'))
    t = str_to_datetime('6:13')
    print(datetime_to_timestr(t))
    
    
    